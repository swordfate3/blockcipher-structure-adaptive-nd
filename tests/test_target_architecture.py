from blockcipher_ai_eval.features.encodings import encode_ciphertext_pair as legacy_encode_pair
from blockcipher_ai_eval.features.pair_features import encode_ciphertext_pair
from blockcipher_ai_eval.features.registry import pair_bits_for_encoding
from blockcipher_ai_eval.models import MlpDistinguisher, SpnTokenMixerPairSetDistinguisher
from blockcipher_ai_eval.models.baseline import MlpDistinguisher as BaselineMlpDistinguisher
from blockcipher_ai_eval.models.common import build_activation
from blockcipher_ai_eval.models.structure import StructureAwareMoEDistinguisher
from blockcipher_ai_eval.models.structure.moe import (
    StructureAwareMoEDistinguisher as ModularStructureAwareMoEDistinguisher,
)
from blockcipher_ai_eval.models.structure.spn import (
    SpnTokenMixerPairSetDistinguisher as ModularSpnTokenMixerPairSetDistinguisher,
)
from blockcipher_ai_eval.models.structure.spn.token_mixer_pairset import (
    SpnTokenMixerPairSetDistinguisher as TokenMixerModuleClass,
)


def test_target_model_architecture_exports_match_legacy_exports():
    assert BaselineMlpDistinguisher is MlpDistinguisher
    assert ModularStructureAwareMoEDistinguisher is StructureAwareMoEDistinguisher
    assert ModularSpnTokenMixerPairSetDistinguisher is SpnTokenMixerPairSetDistinguisher
    assert TokenMixerModuleClass is SpnTokenMixerPairSetDistinguisher
    assert build_activation("relu").__class__.__name__ == "ReLU"


def test_target_feature_architecture_exports_match_legacy_exports():
    assert encode_ciphertext_pair is legacy_encode_pair
    assert pair_bits_for_encoding(64, "ciphertext_pair_xor_spn_aligned_bits") == 256
