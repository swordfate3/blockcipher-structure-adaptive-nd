from blockcipher_ai_eval.experiments import (
    difference_for_profile,
    literature_difference_profiles,
)


def test_literature_difference_profiles_include_core_cipher_settings():
    profiles = literature_difference_profiles()

    assert profiles["speck32_gohr2019"].difference == 0x00400000
    assert profiles["speck32_gohr2019"].word_difference == ("0x0040", "0x0000")
    assert profiles["speck32_gohr2019"].difference_kind == "xor"
    assert profiles["speck32_gohr2019"].pairs_per_sample == 1
    assert profiles["speck32_gohr2019"].polytope_size == 2

    present = profiles["present_wang_jain2021"]
    assert present.differences == (
        0x0700000000000700,
        0x7000000000007000,
        0x0070000000000070,
        0x0007000000000007,
    )

    assert (
        profiles["sm4_yu2023_conv_resnet"].difference
        == 0x00000000000000000000000000000001
    )
    assert profiles["sm4_li_sun_2025_19r_family"].kind == "difference_family"


def test_difference_profile_schema_can_describe_recent_non_xor_families():
    profiles = literature_difference_profiles()

    rx = profiles["simon32_rx_neural2025_schema"]
    assert rx.difference_kind == "rx"
    assert rx.pairs_per_sample > 1
    assert rx.polytope_size == 2
    assert rx.differences == ()

    polytope = profiles["speck32_polytopic2026_schema"]
    assert polytope.difference_kind == "polytope"
    assert polytope.polytope_size == 4
    assert polytope.pairs_per_sample == 1


def test_difference_for_profile_returns_selected_present_member():
    assert (
        difference_for_profile("present_wang_jain2021", member_index=2)
        == 0x0070000000000070
    )


def test_difference_for_profile_rejects_fixed_lookup_for_family_profile():
    try:
        difference_for_profile("sm4_li_sun_2025_19r_family")
    except ValueError as exc:
        assert "not a fixed input difference" in str(exc)
    else:
        raise AssertionError("expected family profile to reject fixed lookup")
