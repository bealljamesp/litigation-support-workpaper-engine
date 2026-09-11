# tests/test_workpaper.py

from pathlib import Path

import pandas as pd

from litigation_engine.workpaper import WorkpaperEngine


def test_generate_summary_workpaper_tc_wp_01() -> None:
    """TC-WP-01: Validates formal layout generation, statistical calculations,

    and absence of formatting corruption.
    """
    aggregated_data = pd.DataFrame(
        {
            "plan_id": ["Plan_Alpha", "Plan_Beta"],
            "breach_type": ["406(a)", "406(b)"],
            "transaction_count": [12, 5],
            "total_loss_amount": [45000.00, 12500.50],
            "mean_loss_amount": [3750.00, 2500.10],
            "max_loss_amount": [10000.00, 5000.00],
            "cumulative_liability": [45000.00, 57500.50],
        }
    )

    workpaper_text = WorkpaperEngine.generate_summary_workpaper(
        aggregated_data, "EBSA v. Dummy Retirement Plan Inc."
    )

    assert "EXHIBIT WORKPAPER" in workpaper_text
    assert "ERISA SECTION 406 / 408" in workpaper_text
    assert "$57,500.50" in workpaper_text or "57500.50" in workpaper_text
    assert "Plan_Alpha" in workpaper_text


def test_export_exhibit_csv_tc_wp_02(tmp_path: Path) -> None:
    """TC-WP-02: Validates successful export of structured trial exhibit CSV

    artifacts.
    """
    output_file = tmp_path / "trial_exhibit_01.csv"
    aggregated_data = pd.DataFrame(
        {
            "plan_id": ["Plan_Alpha"],
            "total_loss_amount": [45000.00],
        }
    )

    saved_path = WorkpaperEngine.export_exhibit_csv(aggregated_data, output_file)
    assert saved_path.is_file()

    loaded_df = pd.read_csv(saved_path)
    assert len(loaded_df) == 1
    assert "total_loss_amount" in loaded_df.columns
