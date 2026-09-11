# tests/test_ingestion.py

from pathlib import Path

import pandas as pd
import pytest

from litigation_engine.ingestion import TransactionIngestor


def test_ingest_csv_valid_tc_ing_01(tmp_path: Path) -> None:
    """
    TC-ING-01: Validates successful ingestion and vectorized cleaning of a
    well-formed transaction log.
    """
    file_path = tmp_path / "valid_transactions.csv"
    data = pd.DataFrame(
        {
            "transaction_id": ["TXN-001", "TXN-002"],
            "plan_id": ["Plan_A", "Plan_B"],
            "transaction_date": ["2026-01-15", "2026-01-16"],
            "breach_type": ["406(a)", "406(b)"],
            "disputed_amount": [1500.00, 3200.50],
        }
    )
    data.to_csv(file_path, index=False)

    df = TransactionIngestor.ingest_csv(file_path)
    assert len(df) == 2
    assert "transaction_id" in df.columns
    assert df["disputed_amount"].dtype == "float64"


def test_ingest_csv_invalid_amount_tc_ing_02(tmp_path: Path) -> None:
    """TC-ING-02: Validates that negative transaction amounts trigger an

    evidentiary corruption exception.
    """
    file_path = tmp_path / "invalid_transactions.csv"
    data = pd.DataFrame(
        {
            "transaction_id": ["TXN-001"],
            "plan_id": ["Plan_A"],
            "transaction_date": ["2026-01-15"],
            "breach_type": ["406(a)"],
            "disputed_amount": [-500.00],
        }
    )
    data.to_csv(file_path, index=False)

    with pytest.raises(
        ValueError, match="Evidentiary corruption: Negative transaction amounts"
    ):
        TransactionIngestor.ingest_csv(file_path)
