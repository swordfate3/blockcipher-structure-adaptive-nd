from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import numpy as np

from blockcipher_ai_eval.data.differential import (
    DifferentialDatasetConfig,
    DiskDifferentialDataset,
)
from blockcipher_ai_eval.data.differential.generator import (
    dataset_metadata,
    generate_negative_row,
    generate_positive_row,
)


ProgressCallback = Callable[[str, dict[str, Any]], None]


def make_chunked_differential_dataset(
    config: DifferentialDatasetConfig,
    *,
    cache_dir: str | Path,
    chunk_size: int = 8192,
    reuse: bool = True,
    progress_callback: ProgressCallback | None = None,
    progress_context: dict[str, Any] | None = None,
) -> DiskDifferentialDataset:
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    if config.pairs_per_sample < 1:
        raise ValueError("pairs_per_sample must be at least 1")
    if config.negative_mode not in {"random_ciphertext", "encrypted_random_plaintexts"}:
        raise ValueError(f"unsupported negative_mode: {config.negative_mode}")

    cache_path = Path(cache_dir)
    features_path = cache_path / "features.npy"
    labels_path = cache_path / "labels.npy"
    metadata_path = cache_path / "metadata.json"
    expected_metadata = dataset_metadata(config)
    total_rows = config.samples_per_class * 2
    input_bits = expected_metadata["pair_bits"] * config.pairs_per_sample
    context = dict(progress_context or {})

    if reuse and features_path.exists() and labels_path.exists() and metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if _cache_matches(metadata, expected_metadata, total_rows, input_bits):
            metadata = {**metadata, "cache_status": "reused"}
            _emit_progress(
                progress_callback,
                "cache_reuse",
                context,
                cache_path=cache_path,
                total_rows=total_rows,
                input_bits=input_bits,
                chunk_size=chunk_size,
            )
            features = np.load(features_path, mmap_mode="r")
            labels = np.load(labels_path, mmap_mode="r")
            return DiskDifferentialDataset(
                features=features,
                labels=labels,
                metadata=metadata,
                cache_dir=cache_path,
            )

    cache_path.mkdir(parents=True, exist_ok=True)
    _emit_progress(
        progress_callback,
        "cache_start",
        context,
        cache_path=cache_path,
        samples_per_class=config.samples_per_class,
        total_rows=total_rows,
        input_bits=input_bits,
        chunk_size=chunk_size,
        requested_shuffle=config.shuffle,
        physical_shuffle=False,
    )
    features = np.lib.format.open_memmap(
        features_path,
        mode="w+",
        dtype=np.uint8,
        shape=(total_rows, input_bits),
    )
    labels = np.lib.format.open_memmap(
        labels_path,
        mode="w+",
        dtype=np.uint8,
        shape=(total_rows,),
    )
    rng = np.random.default_rng(config.seed)
    block_bits = config.cipher.block_bits
    mask = (1 << block_bits) - 1

    row_index = 0
    for start in range(0, config.samples_per_class, chunk_size):
        count = min(chunk_size, config.samples_per_class - start)
        chunk_rows = [
            generate_positive_row(config, rng, block_bits, mask) for _ in range(count)
        ]
        features[row_index : row_index + count] = np.asarray(chunk_rows, dtype=np.uint8)
        labels[row_index : row_index + count] = 1
        row_index += count
        _emit_progress(
            progress_callback,
            "cache_positive_chunk",
            context,
            cache_path=cache_path,
            rows_done=row_index,
            class_rows_done=start + count,
            class_total=config.samples_per_class,
            total_rows=total_rows,
            chunk_rows=count,
        )

    for start in range(0, config.samples_per_class, chunk_size):
        count = min(chunk_size, config.samples_per_class - start)
        chunk_rows = [generate_negative_row(config, rng, block_bits) for _ in range(count)]
        features[row_index : row_index + count] = np.asarray(chunk_rows, dtype=np.uint8)
        labels[row_index : row_index + count] = 0
        row_index += count
        _emit_progress(
            progress_callback,
            "cache_negative_chunk",
            context,
            cache_path=cache_path,
            rows_done=row_index,
            class_rows_done=start + count,
            class_total=config.samples_per_class,
            total_rows=total_rows,
            chunk_rows=count,
        )

    _emit_progress(
        progress_callback,
        "cache_flush_start",
        context,
        cache_path=cache_path,
        total_rows=total_rows,
    )
    features.flush()
    labels.flush()
    metadata = {
        **expected_metadata,
        "total_rows": total_rows,
        "input_bits": input_bits,
        "generation_chunk_size": chunk_size,
        "cache_status": "created",
        "requested_shuffle": config.shuffle,
        "physical_shuffle": False,
        "training_shuffle": True,
    }
    metadata_path.write_text(json.dumps(metadata, sort_keys=True, indent=2), encoding="utf-8")
    _emit_progress(
        progress_callback,
        "cache_done",
        context,
        cache_path=cache_path,
        total_rows=total_rows,
        input_bits=input_bits,
        metadata_path=metadata_path,
    )
    return DiskDifferentialDataset(
        features=np.load(features_path, mmap_mode="r"),
        labels=np.load(labels_path, mmap_mode="r"),
        metadata=metadata,
        cache_dir=cache_path,
    )


def _cache_matches(
    metadata: dict[str, object],
    expected_metadata: dict[str, object],
    total_rows: int,
    input_bits: int,
) -> bool:
    for key, value in expected_metadata.items():
        if metadata.get(key) != value:
            return False
    return metadata.get("total_rows") == total_rows and metadata.get("input_bits") == input_bits


def _emit_progress(
    callback: ProgressCallback | None,
    event: str,
    context: dict[str, Any],
    **payload: Any,
) -> None:
    if callback is None:
        return
    serializable = {
        key: str(value) if isinstance(value, Path) else value
        for key, value in {**context, **payload}.items()
    }
    callback(event, serializable)
