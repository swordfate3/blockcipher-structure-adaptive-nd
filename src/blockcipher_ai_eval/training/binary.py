from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset, TensorDataset

from blockcipher_ai_eval.data.differential import DifferentialDataset, DiskDifferentialDataset


ProgressCallback = Callable[[str, dict[str, Any]], None]


class Lion(torch.optim.Optimizer):
    """Small local Lion optimizer implementation for HPO experiments."""

    def __init__(
        self,
        params,
        lr: float = 1e-4,
        betas: tuple[float, float] = (0.9, 0.99),
        weight_decay: float = 0.0,
    ) -> None:
        defaults = {"lr": lr, "betas": betas, "weight_decay": weight_decay}
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        for group in self.param_groups:
            lr = group["lr"]
            beta1, beta2 = group["betas"]
            weight_decay = group["weight_decay"]
            for parameter in group["params"]:
                if parameter.grad is None:
                    continue
                grad = parameter.grad
                if weight_decay != 0.0:
                    parameter.mul_(1.0 - lr * weight_decay)
                state = self.state[parameter]
                if len(state) == 0:
                    state["exp_avg"] = torch.zeros_like(parameter)
                exp_avg = state["exp_avg"]
                update = exp_avg * beta1 + grad * (1.0 - beta1)
                parameter.add_(update.sign(), alpha=-lr)
                exp_avg.mul_(beta2).add_(grad, alpha=1.0 - beta2)
        return loss


@dataclass(frozen=True)
class TrainingConfig:
    epochs: int = 5
    batch_size: int = 256
    learning_rate: float = 1e-3
    seed: int = 0
    device: str = "auto"
    optimizer: str = "adam"
    amsgrad: bool = False
    weight_decay: float = 0.0
    lr_scheduler: str = "none"
    max_learning_rate: float | None = None
    checkpoint_metric: str = "val_accuracy"
    restore_best_checkpoint: bool = False
    early_stopping_patience: int = 0
    early_stopping_min_delta: float = 0.0
    loss: str = "bce"


@dataclass(frozen=True)
class TrainingResult:
    history: list[dict[str, float]]
    final_metrics: dict[str, float]
    metadata: dict[str, Any]


def predict_binary_probabilities(
    model: nn.Module,
    dataset: DifferentialDataset,
    batch_size: int = 256,
    device: str = "auto",
) -> np.ndarray:
    selected_device = _select_device(device)
    model = model.to(selected_device)
    model.eval()
    loader = _make_loader(dataset, batch_size=batch_size, shuffle=False)

    probabilities: list[float] = []
    with torch.no_grad():
        for features, _batch_labels in loader:
            features = features.to(selected_device)
            logits = model(features).squeeze(1)
            probs = torch.sigmoid(logits).detach().cpu().numpy()
            probabilities.extend(float(item) for item in probs)
    return np.array(probabilities, dtype=np.float32)


def evaluate_binary_classifier(
    model: nn.Module,
    dataset: DifferentialDataset,
    batch_size: int = 256,
    device: str = "auto",
) -> dict[str, float]:
    selected_device = _select_device(device)
    model = model.to(selected_device)
    model.eval()
    loader = _make_loader(dataset, batch_size=batch_size, shuffle=False)
    loss_fn = nn.BCEWithLogitsLoss(reduction="sum")

    total_loss = 0.0
    labels: list[float] = []
    with torch.no_grad():
        for features, batch_labels in loader:
            features = features.to(selected_device)
            batch_labels = batch_labels.to(selected_device)
            logits = model(features).squeeze(1)
            total_loss += float(loss_fn(logits, batch_labels).cpu())
            labels.extend(float(item) for item in batch_labels.cpu().numpy())

    label_array = np.array(labels, dtype=np.float32)
    prob_array = predict_binary_probabilities(model, dataset, batch_size=batch_size, device=str(selected_device))
    predictions = (prob_array >= 0.5).astype(np.float32)
    accuracy = float((predictions == label_array).mean()) if len(label_array) else 0.0
    calibrated_accuracy, calibrated_threshold = _best_threshold_accuracy_and_threshold(
        label_array, prob_array
    )
    return {
        "loss": total_loss / max(1, len(label_array)),
        "accuracy": accuracy,
        "advantage": 2.0 * accuracy - 1.0,
        "auc": _binary_auc(label_array, prob_array),
        "best_accuracy": calibrated_accuracy,
        "calibrated_accuracy": calibrated_accuracy,
        "calibrated_advantage": 2.0 * calibrated_accuracy - 1.0,
        "calibrated_threshold": calibrated_threshold,
    }


def train_binary_classifier(
    model: nn.Module,
    train_dataset: DifferentialDataset,
    validation_dataset: DifferentialDataset,
    config: TrainingConfig,
    progress_callback: ProgressCallback | None = None,
) -> TrainingResult:
    torch.manual_seed(config.seed)
    selected_device = _select_device(config.device)
    model = model.to(selected_device)
    optimizer = _make_optimizer(model, config)
    scheduler = _make_scheduler(optimizer, config, len(train_dataset.labels))
    loss_fn = _make_loss(config.loss)
    train_loader = _make_loader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        seed=config.seed,
    )
    steps_per_epoch = len(train_loader)
    _emit_progress(
        progress_callback,
        "train_start",
        epochs=config.epochs,
        batch_size=config.batch_size,
        train_rows=int(len(train_dataset.labels)),
        validation_rows=int(len(validation_dataset.labels)),
        steps_per_epoch=steps_per_epoch,
        device=str(selected_device),
    )

    history: list[dict[str, float]] = []
    _validate_checkpoint_metric(config.checkpoint_metric)
    best_state_dict: dict[str, torch.Tensor] | None = None
    best_epoch = 0
    best_metric_value: float | None = None
    epochs_without_improvement = 0
    stopped_epoch = 0
    for epoch in range(1, config.epochs + 1):
        _emit_progress(
            progress_callback,
            "epoch_start",
            epoch=epoch,
            epochs=config.epochs,
            steps_per_epoch=steps_per_epoch,
        )
        model.train()
        total_loss = 0.0
        total_seen = 0
        for step, (features, labels) in enumerate(train_loader, start=1):
            features = features.to(selected_device)
            labels = labels.to(selected_device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(features).squeeze(1)
            loss = _compute_loss(loss_fn, logits, labels, config.loss)
            loss.backward()
            optimizer.step()
            if scheduler is not None:
                scheduler.step()
            total_loss += float(loss.detach().cpu()) * len(labels)
            total_seen += len(labels)
            if _should_report_step(step, steps_per_epoch):
                _emit_progress(
                    progress_callback,
                    "train_batch",
                    epoch=epoch,
                    epochs=config.epochs,
                    step=step,
                    steps_per_epoch=steps_per_epoch,
                    train_rows_seen=total_seen,
                    train_rows=int(len(train_dataset.labels)),
                    train_loss=total_loss / max(1, total_seen),
                    learning_rate=_current_learning_rate(optimizer),
                )

        _emit_progress(
            progress_callback,
            "validation_start",
            epoch=epoch,
            epochs=config.epochs,
            validation_rows=int(len(validation_dataset.labels)),
        )
        validation_metrics = evaluate_binary_classifier(
            model,
            validation_dataset,
            batch_size=config.batch_size,
            device=str(selected_device),
        )
        history.append(
            {
                "epoch": float(epoch),
                "train_loss": total_loss / max(1, total_seen),
                "val_loss": validation_metrics["loss"],
                "val_accuracy": validation_metrics["accuracy"],
                "val_auc": validation_metrics["auc"],
                "learning_rate": _current_learning_rate(optimizer),
            }
        )
        current_metric_value = history[-1][config.checkpoint_metric]
        if _is_checkpoint_improved(
            current=current_metric_value,
            best=best_metric_value,
            metric=config.checkpoint_metric,
            min_delta=config.early_stopping_min_delta,
        ):
            best_metric_value = current_metric_value
            best_epoch = epoch
            epochs_without_improvement = 0
            best_state_dict = _clone_state_dict_to_cpu(model)
            _emit_progress(
                progress_callback,
                "checkpoint_improved",
                epoch=epoch,
                metric=config.checkpoint_metric,
                value=current_metric_value,
            )
        else:
            epochs_without_improvement += 1
        _emit_progress(
            progress_callback,
            "epoch_end",
            epoch=epoch,
            epochs=config.epochs,
            train_loss=history[-1]["train_loss"],
            val_loss=history[-1]["val_loss"],
            val_accuracy=history[-1]["val_accuracy"],
            val_auc=history[-1]["val_auc"],
            learning_rate=history[-1]["learning_rate"],
            best_epoch=best_epoch,
            best_checkpoint_metric=best_metric_value,
        )
        if (
            config.early_stopping_patience > 0
            and epochs_without_improvement >= config.early_stopping_patience
        ):
            stopped_epoch = epoch
            _emit_progress(
                progress_callback,
                "early_stopping",
                epoch=epoch,
                patience=config.early_stopping_patience,
                best_epoch=best_epoch,
                metric=config.checkpoint_metric,
                best_value=best_metric_value,
            )
            break

    selected_checkpoint = "last"
    if config.restore_best_checkpoint and best_state_dict is not None:
        model.load_state_dict(best_state_dict)
        model = model.to(selected_device)
        selected_checkpoint = "best"
        _emit_progress(
            progress_callback,
            "checkpoint_restored",
            best_epoch=best_epoch,
            metric=config.checkpoint_metric,
            best_value=best_metric_value,
        )
    _emit_progress(progress_callback, "final_evaluation_start")
    final_metrics = evaluate_binary_classifier(
        model,
        validation_dataset,
        batch_size=config.batch_size,
        device=str(selected_device),
    )
    metadata = {
        "epochs": config.epochs,
        "batch_size": config.batch_size,
        "train_dataset_storage": "disk" if isinstance(train_dataset, DiskDifferentialDataset) else "memory",
        "validation_dataset_storage": "disk" if isinstance(validation_dataset, DiskDifferentialDataset) else "memory",
        "learning_rate": config.learning_rate,
        "optimizer": config.optimizer,
        "amsgrad": config.amsgrad,
        "weight_decay": config.weight_decay,
        "lr_scheduler": config.lr_scheduler,
        "max_learning_rate": config.max_learning_rate,
        "checkpoint_metric": config.checkpoint_metric,
        "restore_best_checkpoint": config.restore_best_checkpoint,
        "early_stopping_patience": config.early_stopping_patience,
        "early_stopping_min_delta": config.early_stopping_min_delta,
        "loss": config.loss,
        "best_epoch": best_epoch,
        "best_checkpoint_metric": best_metric_value,
        "selected_checkpoint": selected_checkpoint,
        "stopped_epoch": stopped_epoch,
        "epochs_ran": len(history),
        "seed": config.seed,
        "device": str(selected_device),
    }
    _emit_progress(
        progress_callback,
        "train_done",
        epochs=config.epochs,
        epochs_ran=len(history),
        accuracy=final_metrics["accuracy"],
        auc=final_metrics["auc"],
        calibrated_accuracy=final_metrics["calibrated_accuracy"],
    )
    return TrainingResult(history=history, final_metrics=final_metrics, metadata=metadata)



def _make_loss(loss: str) -> nn.Module:
    if loss == "bce":
        return nn.BCEWithLogitsLoss()
    if loss == "mse":
        return nn.MSELoss()
    raise ValueError(f"unsupported loss: {loss}")


def _compute_loss(loss_fn: nn.Module, logits: torch.Tensor, labels: torch.Tensor, loss: str) -> torch.Tensor:
    if loss == "mse":
        return loss_fn(torch.sigmoid(logits), labels)
    return loss_fn(logits, labels)


def _make_optimizer(
    model: nn.Module,
    config: TrainingConfig,
) -> torch.optim.Optimizer:
    if config.optimizer == "adam":
        return torch.optim.Adam(
            model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay,
            amsgrad=config.amsgrad,
        )
    if config.optimizer == "adamw":
        return torch.optim.AdamW(
            model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay,
            amsgrad=config.amsgrad,
        )
    if config.optimizer == "lion":
        return Lion(
            model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay,
        )
    raise ValueError(f"unsupported optimizer: {config.optimizer}")


def _make_scheduler(
    optimizer: torch.optim.Optimizer,
    config: TrainingConfig,
    train_size: int,
) -> torch.optim.lr_scheduler.LRScheduler | None:
    if config.lr_scheduler == "none":
        return None
    if config.lr_scheduler == "cyclic":
        steps_per_epoch = max(1, (train_size + config.batch_size - 1) // config.batch_size)
        return torch.optim.lr_scheduler.CyclicLR(
            optimizer,
            base_lr=config.learning_rate,
            max_lr=config.max_learning_rate or config.learning_rate * 10.0,
            step_size_up=max(1, steps_per_epoch // 2),
            cycle_momentum=False,
        )
    if config.lr_scheduler == "cosine_warmup":
        steps_per_epoch = max(1, (train_size + config.batch_size - 1) // config.batch_size)
        total_steps = max(1, config.epochs * steps_per_epoch)
        warmup_steps = max(1, min(total_steps // 10, steps_per_epoch))

        def lr_lambda(step: int) -> float:
            if step < warmup_steps:
                return float(step + 1) / float(warmup_steps)
            progress = float(step - warmup_steps) / float(max(1, total_steps - warmup_steps))
            return 0.5 * (1.0 + math.cos(math.pi * min(1.0, progress)))

        return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lr_lambda)
    raise ValueError(f"unsupported lr scheduler: {config.lr_scheduler}")


def _current_learning_rate(optimizer: torch.optim.Optimizer) -> float:
    return float(optimizer.param_groups[0]["lr"])


def _validate_checkpoint_metric(metric: str) -> None:
    if metric not in {"val_accuracy", "val_auc", "val_loss"}:
        raise ValueError(f"unsupported checkpoint metric: {metric}")


def _clone_state_dict_to_cpu(model: nn.Module) -> dict[str, torch.Tensor]:
    return {
        key: value.detach().cpu().clone()
        for key, value in model.state_dict().items()
    }


def _is_checkpoint_improved(
    *,
    current: float,
    best: float | None,
    metric: str,
    min_delta: float,
) -> bool:
    if best is None:
        return True
    if metric == "val_loss":
        return current < best - min_delta
    return current > best + min_delta


def _make_loader(
    dataset: DifferentialDataset,
    batch_size: int,
    shuffle: bool,
    seed: int = 0,
) -> DataLoader:
    if isinstance(dataset, DiskDifferentialDataset):
        torch_dataset: Dataset = _DiskDifferentialTorchDataset(dataset)
    else:
        features = torch.tensor(dataset.features, dtype=torch.float32)
        labels = torch.tensor(dataset.labels, dtype=torch.float32)
        torch_dataset = TensorDataset(features, labels)
    generator = torch.Generator().manual_seed(seed)
    return DataLoader(
        torch_dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        generator=generator if shuffle else None,
    )


class _DiskDifferentialTorchDataset(Dataset):
    def __init__(self, dataset: DiskDifferentialDataset) -> None:
        self.features = dataset.features
        self.labels = dataset.labels

    def __len__(self) -> int:
        return int(self.labels.shape[0])

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        feature = torch.as_tensor(np.asarray(self.features[index]).copy(), dtype=torch.float32)
        label = torch.tensor(float(self.labels[index]), dtype=torch.float32)
        return feature, label


def _select_device(device: str) -> torch.device:
    if device == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(device)


def _should_report_step(step: int, steps_per_epoch: int) -> bool:
    if steps_per_epoch <= 10:
        return True
    interval = max(1, steps_per_epoch // 10)
    return step == 1 or step == steps_per_epoch or step % interval == 0


def _emit_progress(callback: ProgressCallback | None, event: str, **payload: Any) -> None:
    if callback is None:
        return
    callback(event, payload)


def _binary_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    positive_mask = labels == 1
    positive_count = int(positive_mask.sum())
    negative_count = int((labels == 0).sum())
    if positive_count == 0 or negative_count == 0:
        return 0.5

    order = np.argsort(scores, kind="mergesort")
    sorted_scores = scores[order]
    ranks = np.empty(len(scores), dtype=np.float64)
    start = 0
    while start < len(sorted_scores):
        end = start + 1
        while end < len(sorted_scores) and sorted_scores[end] == sorted_scores[start]:
            end += 1
        average_rank = (start + 1 + end) / 2.0
        ranks[order[start:end]] = average_rank
        start = end

    positive_rank_sum = float(ranks[positive_mask].sum())
    u_statistic = positive_rank_sum - positive_count * (positive_count + 1) / 2.0
    return float(u_statistic / (positive_count * negative_count))


def _best_threshold_accuracy(labels: np.ndarray, scores: np.ndarray) -> float:
    return _best_threshold_accuracy_and_threshold(labels, scores)[0]


def _best_threshold_accuracy_and_threshold(
    labels: np.ndarray, scores: np.ndarray
) -> tuple[float, float]:
    if len(labels) == 0:
        return 0.0, 0.5
    thresholds = np.unique(scores)
    best = 0.0
    best_threshold = 0.5
    for threshold in thresholds:
        predictions = (scores >= threshold).astype(np.float32)
        accuracy = float((predictions == labels).mean())
        if accuracy > best:
            best = accuracy
            best_threshold = float(threshold)
    return best, best_threshold
