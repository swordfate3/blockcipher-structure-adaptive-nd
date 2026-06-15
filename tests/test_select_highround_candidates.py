import csv
import importlib.util
import sys
from pathlib import Path


def _load_module():
    script = Path(__file__).resolve().parents[1] / "experiments" / "innovation1" / "select_highround_candidates.py"
    spec = importlib.util.spec_from_file_location("select_highround_candidates", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_select_highround_candidates_emits_confirm_plan(tmp_path: Path):
    module = _load_module()
    summary = tmp_path / "summary.csv"
    summary.write_text(
        "\n".join(
            [
                "cipher,structure,model,architecture,rounds,difference_profile,difference_member,samples_per_class,pairs_per_sample,runs,feature_encoding,calibrated_accuracy_mean,auc_mean",
                "PRESENT-80,SPN,present_matrix_trail_hybrid_pairset,PRESENT-MatrixTrailHybrid-Beam4Deep3-r7,7,present_zhang_wang2022_mcnd,0,65536,16,2,present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits,0.532,0.548",
                "PRESENT-80,SPN,present_trail_mixer_pairset,PRESENT-TrailMixer-Beam4Deep3-r8,8,present_zhang_wang2022_mcnd,0,131072,16,2,present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits,0.506,0.510",
                "PRESENT-80,SPN,present_inception_mcnd_matrix,PRESENT-r6-control,6,present_zhang_wang2022_mcnd,0,32768,16,3,present_pair_xor_cell_matrix_bits,0.88,0.95",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    source_plan = tmp_path / "source.csv"
    source_plan.write_text(
        "\n".join(
            [
                "cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,pairs_per_sample,feature_encoding,negative_mode,train_key,validation_key,key_rotation_interval,sample_structure,integral_active_nibble,difference_profile,difference_member,loss,learning_rate,optimizer,weight_decay,lr_scheduler,max_learning_rate,checkpoint_metric,restore_best_checkpoint,early_stopping_patience,early_stopping_min_delta,pretrain_rounds,pretrain_epochs,model_options,evidence,literature",
                'PRESENT-80,SPN,PRESENT-MatrixTrailHybrid-Beam4Deep3-r7,present_matrix_trail_hybrid_pairset,present_sboxddt_beam4deep3_hybrid,0,140,7,0,65536,16,present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits,encrypted_random_plaintexts,0x0,0xf,1024,zhang_wang_case2_mcnd,0,present_zhang_wang2022_mcnd,0,mse,0.0001,adam,1e-05,cyclic,0.002,val_auc,true,0,0.0,6,6,"{""token_dim"":64}",screen,literature',
                'PRESENT-80,SPN,PRESENT-TrailMixer-Beam4Deep3-r8,present_trail_mixer_pairset,present_sboxddt_beam4deep3_trailmixer,1,125,8,0,131072,16,present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits,encrypted_random_plaintexts,0x0,0xf,1024,zhang_wang_case2_mcnd,0,present_zhang_wang2022_mcnd,0,mse,0.0001,adam,1e-05,cyclic,0.002,val_auc,true,0,0.0,6,6,"{""token_dim"":64}",screen,literature',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "confirm.csv"

    rc = module.main(
        [
            "--summary-glob",
            str(summary),
            "--source-plan",
            str(source_plan),
            "--output",
            str(output),
            "--limit",
            "2",
            "--seeds",
            "0..4",
            "--samples-per-class",
            "262144",
        ]
    )

    assert rc == 0
    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    assert len(rows) == 10
    assert {row["rounds"] for row in rows} == {"7", "8"}
    assert {row["samples_per_class"] for row in rows} == {"262144"}
    assert {row["seed"] for row in rows} == {"0", "1", "2", "3", "4"}
    assert {row["model_key"] for row in rows} == {
        "present_matrix_trail_hybrid_pairset",
        "present_trail_mixer_pairset",
    }
    assert rows[-1]["feature_encoding"] == "present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits"
    assert "High-round confirm selected" in rows[0]["evidence"]
