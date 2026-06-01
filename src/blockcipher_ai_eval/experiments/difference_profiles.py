from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DifferenceProfile:
    name: str
    cipher: str
    kind: str
    differences: tuple[int, ...]
    source: str
    word_difference: tuple[str, ...] = ()
    note: str = ""

    @property
    def difference(self) -> int:
        if self.kind != "fixed":
            raise ValueError(f"profile {self.name} is not a fixed input difference")
        return self.differences[0]


def literature_difference_profiles() -> dict[str, DifferenceProfile]:
    return {
        "speck32_gohr2019": DifferenceProfile(
            name="speck32_gohr2019",
            cipher="speck32",
            kind="fixed",
            differences=(0x00400000,),
            word_difference=("0x0040", "0x0000"),
            source="Gohr 2019 SPECK32/64 neural distinguisher",
            note="Input difference 0x0040/0000 for Gohr N5-N8 distinguishers.",
        ),
        "present_wang_jain2021": DifferenceProfile(
            name="present_wang_jain2021",
            cipher="present80",
            kind="multi_fixed",
            differences=(
                0x0700000000000700,
                0x7000000000007000,
                0x0070000000000070,
                0x0007000000000007,
            ),
            source="Wang differentials via Jain/Kohli/Mishra 2020/2021",
            note="Four high-probability PRESENT input differential classes.",
        ),
        "present_wang_jain2021_1": DifferenceProfile(
            name="present_wang_jain2021_1",
            cipher="present80",
            kind="fixed",
            differences=(0x0700000000000700,),
            source="Wang differentials via Jain/Kohli/Mishra 2020/2021",
        ),
        "present_wang_jain2021_2": DifferenceProfile(
            name="present_wang_jain2021_2",
            cipher="present80",
            kind="fixed",
            differences=(0x7000000000007000,),
            source="Wang differentials via Jain/Kohli/Mishra 2020/2021",
        ),
        "present_wang_jain2021_3": DifferenceProfile(
            name="present_wang_jain2021_3",
            cipher="present80",
            kind="fixed",
            differences=(0x0070000000000070,),
            source="Wang differentials via Jain/Kohli/Mishra 2020/2021",
        ),
        "present_wang_jain2021_4": DifferenceProfile(
            name="present_wang_jain2021_4",
            cipher="present80",
            kind="fixed",
            differences=(0x0007000000000007,),
            source="Wang differentials via Jain/Kohli/Mishra 2020/2021",
        ),
        "sm4_yu2023_conv_resnet": DifferenceProfile(
            name="sm4_yu2023_conv_resnet",
            cipher="sm4",
            kind="fixed",
            differences=(0x00000000000000000000000000000001,),
            word_difference=(
                "0x00000000",
                "0x00000000",
                "0x00000000",
                "0x00000001",
            ),
            source="Yu/Wu/Zhang 2023 SM4 convolutional residual network",
            note="Plaintext difference used for SM4 3-8 round neural distinguishers.",
        ),
        "sm4_li_sun_2025_19r_family": DifferenceProfile(
            name="sm4_li_sun_2025_19r_family",
            cipher="sm4",
            kind="difference_family",
            differences=(),
            word_difference=(
                "a''0 in {x xor e79393d6 | PrT(0000003c, x) > 0}",
                "0xe793932d",
                "0x6fb9b98f",
                "0x882a2a9e",
            ),
            source="Li/Sun 2025 key-recovery-friendly SM4 differential family",
            note="Constrained family; not directly usable as a fixed neural input difference.",
        ),
    }


def difference_for_profile(name: str, member_index: int = 0) -> int:
    profile = literature_difference_profiles()[name]
    if profile.kind == "difference_family":
        raise ValueError(f"profile {name} is not a fixed input difference")
    try:
        return profile.differences[member_index]
    except IndexError as exc:
        raise ValueError(f"profile {name} has no member {member_index}") from exc
