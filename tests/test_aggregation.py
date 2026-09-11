# tests/test_aggregation.py

import pandas as pd
import pytest

from litigation_engine.aggregation import LitigationAggregator


def test_compute_prohibited_transfers_tc_agg_01() -> None:
    """
    TC-AGG-01: Validates vector aggregation, cumulative liability tracking,
    and absence of numerical drift.
    """
    data = pd.DataFrame(
        {
            "plan_id": ["Plan_A", "Plan_A", "Plan_B", "Plan_B"],
            "breach_type": ["406(a)", "406(a)", "406(b)", "406(b)"],
            "disputed_amount": [1000.50, 2500.25, 5000.00, 1500.00],
        }
    )

    result = LitigationAggregator.compute_prohibited_transfers(
        data, group_cols=["plan_id", "breach_type"], value_col="disputed_amount"
    )

    # Assertions on structural integrity and calculations
    assert "transaction_count" in result.columns
    assert "cumulative_liability" in result.columns
    assert result.loc[result["plan_id"] == "Plan_A", "total_loss_amount"].iloc[
        0
    ] == pytest.approx(3500.75)
    assert result["cumulative_liability"].iloc[-1] == pytest.approx(10000.75)
