import importlib

from blockcipher_ai_eval.features.pair_features import encode_ciphertext_pair
from blockcipher_ai_eval.features.registry import pair_bits_for_encoding
from blockcipher_ai_eval.models.baseline import MlpDistinguisher
from blockcipher_ai_eval.models.common import build_activation
from blockcipher_ai_eval.models.structure import StructureAwareMoEDistinguisher
from blockcipher_ai_eval.models.structure.spn import SpnTokenMixerPairSetDistinguisher
from blockcipher_ai_eval.models.structure.spn.token_mixer_pairset import (
    SpnTokenMixerPairSetDistinguisher as TokenMixerModuleClass,
)


def test_target_model_architecture_uses_canonical_exports():
    assert MlpDistinguisher.__module__ == "blockcipher_ai_eval.models.baseline.mlp"
    assert (
        StructureAwareMoEDistinguisher.__module__
        == "blockcipher_ai_eval.models.structure.moe"
    )
    assert SpnTokenMixerPairSetDistinguisher is TokenMixerModuleClass
    assert build_activation("relu").__class__.__name__ == "ReLU"


def test_top_level_models_package_does_not_reexport_architectures():
    models_package = importlib.import_module("blockcipher_ai_eval.models")

    assert not hasattr(models_package, "MlpDistinguisher")
    assert models_package.__all__ == []


def test_target_feature_architecture_uses_canonical_exports():
    assert encode_ciphertext_pair.__module__ == "blockcipher_ai_eval.features.pair_features"
    assert pair_bits_for_encoding(64, "ciphertext_pair_xor_spn_aligned_bits") == 256
