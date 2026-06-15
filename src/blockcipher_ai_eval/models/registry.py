from __future__ import annotations

from collections.abc import Callable
from typing import Any

from torch import nn

from blockcipher_ai_eval.models.baseline import (
    CnnDistinguisher,
    DBitNetDistinguisher,
    GohrSpeckDistinguisher,
    LstmRoundSeqDistinguisher,
    MlpDistinguisher,
    MultiScaleDenseResNetDistinguisher,
    ResNetBitSliceDistinguisher,
    SeResNeXtDistinguisher,
    TransformerEncoderDistinguisher,
)
from blockcipher_ai_eval.models.structure import (
    AdaptiveDBitNetDistinguisher,
    ArxPairSetStatsHybridDistinguisher,
    ArxRoundFunctionHybridPairSetDistinguisher,
    ArxStructureAdaptivePairSetDBitNetDistinguisher,
    ArxTrailMixerPairSetDistinguisher,
    ArxWordMixerPairSetDistinguisher,
    PairwiseAdaptiveDBitNetDistinguisher,
    PresentInceptionMCNDDistinguisher,
    PresentInceptionMCNDGlobalMatrixDistinguisher,
    PresentInceptionMCNDPairStackMatrixDistinguisher,
    PresentMatrixTrailHybridPairSetDistinguisher,
    PresentPairSetStatsHybridDistinguisher,
    PresentPLayerMixerPairSetDistinguisher,
    PresentTrailMixerPairSetDistinguisher,
    SpnCellPairSetDBitNetDistinguisher,
    SpnNibbleConvPairSetDistinguisher,
    SpnTokenMixerPairSetDistinguisher,
    StructureAdaptivePairSetDBitNetDistinguisher,
    StructureAwareMoEDistinguisher,
)

ModelBuilder = Callable[..., nn.Module]

MODEL_REGISTRY: dict[str, type[nn.Module]] = {
    "mlp": MlpDistinguisher,
    "cnn": CnnDistinguisher,
    "dbitnet_dilated_cnn": DBitNetDistinguisher,
    "gohr_resnet_speck": GohrSpeckDistinguisher,
    "lstm_roundseq": LstmRoundSeqDistinguisher,
    "transformer_encoder": TransformerEncoderDistinguisher,
    "resnet_bitslice": ResNetBitSliceDistinguisher,
    "senet_resnext": SeResNeXtDistinguisher,
    "multiscale_dense_resnet": MultiScaleDenseResNetDistinguisher,
    "adaptive_dbitnet": AdaptiveDBitNetDistinguisher,
    "adaptive_dbitnet_pairwise": PairwiseAdaptiveDBitNetDistinguisher,
    "structure_adaptive_pairset_dbitnet": StructureAdaptivePairSetDBitNetDistinguisher,
    "arx_structure_adaptive_pairset_dbitnet": ArxStructureAdaptivePairSetDBitNetDistinguisher,
    "arx_pairset_dbitnet": ArxStructureAdaptivePairSetDBitNetDistinguisher,
    "arx_pairset_stats_hybrid": ArxPairSetStatsHybridDistinguisher,
    "arx_round_function_hybrid_pairset": ArxRoundFunctionHybridPairSetDistinguisher,
    "arx_word_mixer_pairset": ArxWordMixerPairSetDistinguisher,
    "arx_trail_mixer_pairset": ArxTrailMixerPairSetDistinguisher,
    "present_inception_mcnd": PresentInceptionMCNDDistinguisher,
    "present_inception_mcnd_global_matrix": PresentInceptionMCNDGlobalMatrixDistinguisher,
    "present_inception_mcnd_pair_stack_matrix": PresentInceptionMCNDPairStackMatrixDistinguisher,
    "present_matrix_trail_hybrid_pairset": PresentMatrixTrailHybridPairSetDistinguisher,
    "present_pairset_stats_hybrid": PresentPairSetStatsHybridDistinguisher,
    "spn_cell_pairset_dbitnet": SpnCellPairSetDBitNetDistinguisher,
    "spn_nibble_conv_pairset": SpnNibbleConvPairSetDistinguisher,
    "spn_token_mixer_pairset": SpnTokenMixerPairSetDistinguisher,
    "present_p_layer_mixer_pairset": PresentPLayerMixerPairSetDistinguisher,
    "present_trail_mixer_pairset": PresentTrailMixerPairSetDistinguisher,
    "structure_aware_moe": StructureAwareMoEDistinguisher,
}


def get_model_class(model_key: str) -> type[nn.Module]:
    try:
        return MODEL_REGISTRY[model_key]
    except KeyError as exc:
        raise KeyError(f"unknown model key: {model_key}") from exc


__all__ = ["MODEL_REGISTRY", "ModelBuilder", "get_model_class"]
