from blockcipher_ai_eval.models.structure.adaptive_dbitnet import (
    AdaptiveDBitNetBlock,
    AdaptiveDBitNetDistinguisher,
    AdaptiveDBitNetEncoder,
    PairwiseAdaptiveDBitNetDistinguisher,
    StructureAdaptivePairSetDBitNetDistinguisher,
    StructureConditionedDBitNetEncoder,
    adaptive_dbitnet_dilations,
    structure_bit_mask,
    structure_conditioned_dilations,
)

_SPN_COMPAT_EXPORTS = {
    "SpnCellPairSetDBitNetDistinguisher",
    "SpnNibbleConvPairSetDistinguisher",
    "SpnTokenMixerPairSetDistinguisher",
}


def __getattr__(name: str):
    if name in _SPN_COMPAT_EXPORTS:
        from blockcipher_ai_eval.models import spn as spn_models

        value = getattr(spn_models, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "AdaptiveDBitNetBlock",
    "AdaptiveDBitNetDistinguisher",
    "AdaptiveDBitNetEncoder",
    "PairwiseAdaptiveDBitNetDistinguisher",
    "StructureAdaptivePairSetDBitNetDistinguisher",
    "StructureConditionedDBitNetEncoder",
    "adaptive_dbitnet_dilations",
    "structure_bit_mask",
    "structure_conditioned_dilations",
]
