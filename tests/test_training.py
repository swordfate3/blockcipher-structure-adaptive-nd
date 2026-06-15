import numpy as np

from blockcipher_ai_eval.ciphers import Speck32_64
from blockcipher_ai_eval.data.cache import make_chunked_differential_dataset
from blockcipher_ai_eval.data.differential import DifferentialDatasetConfig
from blockcipher_ai_eval.data.differential.generator import make_differential_dataset
from blockcipher_ai_eval.models.baseline import MlpDistinguisher
from blockcipher_ai_eval.training import (
    TrainingConfig,
    evaluate_binary_classifier,
    train_binary_classifier,
)
from blockcipher_ai_eval.training.binary import _binary_auc


def test_evaluate_binary_classifier_returns_core_metrics():
    dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=Speck32_64(rounds=2, key=0x1918111009080100),
            input_difference=0x0040,
            samples_per_class=16,
            seed=1,
        )
    )
    model = MlpDistinguisher(input_bits=dataset.features.shape[1], hidden_bits=16)

    metrics = evaluate_binary_classifier(model, dataset, batch_size=8)

    assert set(metrics) == {
        "loss",
        "accuracy",
        "advantage",
        "auc",
        "best_accuracy",
        "calibrated_accuracy",
        "calibrated_advantage",
        "calibrated_threshold",
    }
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["best_accuracy"] <= 1.0
    assert 0.0 <= metrics["calibrated_accuracy"] <= 1.0
    assert -1.0 <= metrics["advantage"] <= 1.0
    assert -1.0 <= metrics["calibrated_advantage"] <= 1.0
    assert 0.0 <= metrics["auc"] <= 1.0
    assert 0.0 <= metrics["calibrated_threshold"] <= 1.0


def test_train_binary_classifier_returns_history_and_final_metrics():
    dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=Speck32_64(rounds=2, key=0x1918111009080100),
            input_difference=0x0040,
            samples_per_class=32,
            seed=2,
        )
    )
    model = MlpDistinguisher(input_bits=dataset.features.shape[1], hidden_bits=16)
    config = TrainingConfig(epochs=2, batch_size=16, learning_rate=1e-3, seed=99)

    result = train_binary_classifier(model, dataset, dataset, config)

    assert len(result.history) == 2
    assert result.history[0]["train_loss"] >= 0.0
    assert 0.0 <= result.final_metrics["accuracy"] <= 1.0
    assert result.metadata["epochs"] == 2
    assert result.metadata["batch_size"] == 16


def test_train_binary_classifier_can_restore_best_checkpoint():
    dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=Speck32_64(rounds=2, key=0x1918111009080100),
            input_difference=0x0040,
            samples_per_class=32,
            seed=12,
        )
    )
    model = MlpDistinguisher(input_bits=dataset.features.shape[1], hidden_bits=16)
    config = TrainingConfig(
        epochs=3,
        batch_size=16,
        learning_rate=1e-3,
        seed=99,
        checkpoint_metric="val_accuracy",
        restore_best_checkpoint=True,
    )

    result = train_binary_classifier(model, dataset, dataset, config)

    assert len(result.history) == 3
    assert result.metadata["selected_checkpoint"] == "best"
    assert 1 <= result.metadata["best_epoch"] <= 3
    assert result.metadata["best_checkpoint_metric"] is not None
    assert result.metadata["epochs_ran"] == 3


def test_train_binary_classifier_supports_early_stopping():
    dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=Speck32_64(rounds=2, key=0x1918111009080100),
            input_difference=0x0040,
            samples_per_class=32,
            seed=13,
        )
    )
    model = MlpDistinguisher(input_bits=dataset.features.shape[1], hidden_bits=16)
    events = []
    config = TrainingConfig(
        epochs=5,
        batch_size=16,
        learning_rate=1e-3,
        seed=99,
        checkpoint_metric="val_accuracy",
        restore_best_checkpoint=True,
        early_stopping_patience=1,
        early_stopping_min_delta=1.0,
    )

    result = train_binary_classifier(
        model,
        dataset,
        dataset,
        config,
        progress_callback=lambda event, payload: events.append((event, payload)),
    )

    assert result.metadata["selected_checkpoint"] == "best"
    assert result.metadata["epochs_ran"] < 5
    assert result.metadata["stopped_epoch"] == result.metadata["epochs_ran"]
    assert "early_stopping" in [event for event, _ in events]


def test_train_binary_classifier_reports_epoch_progress():
    dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=Speck32_64(rounds=2, key=0x1918111009080100),
            input_difference=0x0040,
            samples_per_class=16,
            seed=2,
        )
    )
    model = MlpDistinguisher(input_bits=dataset.features.shape[1], hidden_bits=16)
    config = TrainingConfig(epochs=2, batch_size=8, learning_rate=1e-3, seed=99)
    events = []

    train_binary_classifier(
        model,
        dataset,
        dataset,
        config,
        progress_callback=lambda event, payload: events.append((event, payload)),
    )

    event_names = [event for event, _ in events]
    assert event_names[0] == "train_start"
    assert event_names.count("epoch_start") == 2
    assert event_names.count("epoch_end") == 2
    assert event_names[-1] == "train_done"
    assert events[-1][1]["epochs"] == 2


def test_train_binary_classifier_supports_gohr_style_optimizer_options():
    dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=Speck32_64(rounds=2, key=0x1918111009080100),
            input_difference=0x0040,
            samples_per_class=32,
            seed=3,
        )
    )
    model = MlpDistinguisher(input_bits=dataset.features.shape[1], hidden_bits=16)
    config = TrainingConfig(
        epochs=2,
        batch_size=16,
        learning_rate=1e-3,
        seed=99,
        optimizer="adamw",
        amsgrad=True,
        weight_decay=1e-4,
        lr_scheduler="cyclic",
        max_learning_rate=3e-3,
    )

    result = train_binary_classifier(model, dataset, dataset, config)

    assert result.metadata["optimizer"] == "adamw"
    assert result.metadata["amsgrad"] is True
    assert result.metadata["weight_decay"] == 1e-4
    assert result.metadata["lr_scheduler"] == "cyclic"
    assert result.metadata["max_learning_rate"] == 3e-3
    assert result.history[-1]["learning_rate"] <= 3e-3


def test_binary_auc_handles_ties_without_quadratic_comparison_matrix(monkeypatch):
    labels = np.array([1, 0, 1, 0, 1, 0], dtype=np.float32)
    scores = np.array([0.8, 0.1, 0.5, 0.5, 0.2, 0.2], dtype=np.float32)

    def fail_sum(*args, **kwargs):
        raise AssertionError("quadratic comparison matrix path should not call np.sum")

    monkeypatch.setattr(np, "sum", fail_sum)

    assert _binary_auc(labels, scores) == 7.0 / 9.0



def test_train_binary_classifier_supports_lion_and_cosine_warmup():
    dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=Speck32_64(rounds=2, key=0x1918111009080100),
            input_difference=0x0040,
            samples_per_class=32,
            seed=4,
        )
    )
    model = MlpDistinguisher(input_bits=dataset.features.shape[1], hidden_bits=16)
    config = TrainingConfig(
        epochs=2,
        batch_size=16,
        learning_rate=1e-3,
        seed=99,
        optimizer="lion",
        weight_decay=1e-4,
        lr_scheduler="cosine_warmup",
    )

    result = train_binary_classifier(model, dataset, dataset, config)

    assert result.metadata["optimizer"] == "lion"
    assert result.metadata["lr_scheduler"] == "cosine_warmup"
    assert result.history[0]["learning_rate"] >= 0.0


def test_train_binary_classifier_supports_disk_backed_dataset_without_eager_tensor_copy(tmp_path, monkeypatch):
    config = DifferentialDatasetConfig(
        cipher=Speck32_64(rounds=2, key=0x1918111009080100),
        input_difference=0x0040,
        samples_per_class=16,
        seed=5,
    )
    dataset = make_chunked_differential_dataset(config, cache_dir=tmp_path / "dataset", chunk_size=8)
    model = MlpDistinguisher(input_bits=dataset.features.shape[1], hidden_bits=16)
    training_config = TrainingConfig(epochs=1, batch_size=8, learning_rate=1e-3, seed=99)

    import blockcipher_ai_eval.training.binary as binary_training

    original_tensor = binary_training.torch.tensor

    def guarded_tensor(value, *args, **kwargs):
        if value is dataset.features:
            raise AssertionError("disk-backed features should not be eagerly converted")
        return original_tensor(value, *args, **kwargs)

    monkeypatch.setattr(binary_training.torch, "tensor", guarded_tensor)

    result = train_binary_classifier(model, dataset, dataset, training_config)

    assert result.metadata["train_dataset_storage"] == "disk"
    assert result.metadata["validation_dataset_storage"] == "disk"
    assert len(result.history) == 1


def test_train_binary_classifier_supports_mse_probability_loss():
    dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=Speck32_64(rounds=2, key=0x1918111009080100),
            input_difference=0x0040,
            samples_per_class=32,
            seed=6,
        )
    )
    model = MlpDistinguisher(input_bits=dataset.features.shape[1], hidden_bits=16)
    config = TrainingConfig(
        epochs=2,
        batch_size=16,
        learning_rate=1e-4,
        seed=99,
        optimizer="adam",
        weight_decay=1e-5,
        lr_scheduler="cyclic",
        max_learning_rate=2e-3,
        loss="mse",
    )

    result = train_binary_classifier(model, dataset, dataset, config)

    assert result.metadata["loss"] == "mse"
    assert result.metadata["optimizer"] == "adam"
    assert result.metadata["weight_decay"] == 1e-5
    assert result.metadata["lr_scheduler"] == "cyclic"
    assert len(result.history) == 2
