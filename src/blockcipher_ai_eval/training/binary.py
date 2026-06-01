from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from blockcipher_ai_eval.datasets import DifferentialDataset


@dataclass(frozen=True)
class TrainingConfig:
    epochs: int = 5
    batch_size: int = 256
    learning_rate: float = 1e-3
    seed: int = 0
    device: str = "auto"


@dataclass(frozen=True)
class TrainingResult:
    history: list[dict[str, float]]
    final_metrics: dict[str, float]
    metadata: dict[str, Any]


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
    probabilities: list[float] = []
    labels: list[float] = []
    with torch.no_grad():
        for features, batch_labels in loader:
            features = features.to(selected_device)
            batch_labels = batch_labels.to(selected_device)
            logits = model(features).squeeze(1)
            total_loss += float(loss_fn(logits, batch_labels).cpu())
            probs = torch.sigmoid(logits).detach().cpu().numpy()
            probabilities.extend(float(item) for item in probs)
            labels.extend(float(item) for item in batch_labels.cpu().numpy())

    label_array = np.array(labels, dtype=np.float32)
    prob_array = np.array(probabilities, dtype=np.float32)
    predictions = (prob_array >= 0.5).astype(np.float32)
    accuracy = float((predictions == label_array).mean()) if len(label_array) else 0.0
    return {
        "loss": total_loss / max(1, len(label_array)),
        "accuracy": accuracy,
        "advantage": 2.0 * accuracy - 1.0,
        "auc": _binary_auc(label_array, prob_array),
        "best_accuracy": _best_threshold_accuracy(label_array, prob_array),
    }


def train_binary_classifier(
    model: nn.Module,
    train_dataset: DifferentialDataset,
    validation_dataset: DifferentialDataset,
    config: TrainingConfig,
) -> TrainingResult:
    torch.manual_seed(config.seed)
    selected_device = _select_device(config.device)
    model = model.to(selected_device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    loss_fn = nn.BCEWithLogitsLoss()
    train_loader = _make_loader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        seed=config.seed,
    )

    history: list[dict[str, float]] = []
    for epoch in range(1, config.epochs + 1):
        model.train()
        total_loss = 0.0
        total_seen = 0
        for features, labels in train_loader:
            features = features.to(selected_device)
            labels = labels.to(selected_device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(features).squeeze(1)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()
            total_loss += float(loss.detach().cpu()) * len(labels)
            total_seen += len(labels)

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
            }
        )

    final_metrics = evaluate_binary_classifier(
        model,
        validation_dataset,
        batch_size=config.batch_size,
        device=str(selected_device),
    )
    metadata = {
        "epochs": config.epochs,
        "batch_size": config.batch_size,
        "learning_rate": config.learning_rate,
        "seed": config.seed,
        "device": str(selected_device),
    }
    return TrainingResult(history=history, final_metrics=final_metrics, metadata=metadata)


def _make_loader(
    dataset: DifferentialDataset,
    batch_size: int,
    shuffle: bool,
    seed: int = 0,
) -> DataLoader:
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


def _select_device(device: str) -> torch.device:
    if device == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(device)


def _binary_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    positives = scores[labels == 1]
    negatives = scores[labels == 0]
    if len(positives) == 0 or len(negatives) == 0:
        return 0.5
    comparisons = positives[:, None] - negatives[None, :]
    wins = np.sum(comparisons > 0)
    ties = np.sum(comparisons == 0)
    return float((wins + 0.5 * ties) / (len(positives) * len(negatives)))


def _best_threshold_accuracy(labels: np.ndarray, scores: np.ndarray) -> float:
    if len(labels) == 0:
        return 0.0
    thresholds = np.unique(scores)
    best = 0.0
    for threshold in thresholds:
        predictions = (scores >= threshold).astype(np.float32)
        best = max(best, float((predictions == labels).mean()))
    return best
