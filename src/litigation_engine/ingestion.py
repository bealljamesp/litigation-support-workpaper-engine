# src/litigation_engine/ingestion.py

from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd


class TransactionIngestor:
    """Ingests and validates raw transactional exception logs for ERISA

    litigation support, enforcing strict schemas and vectorized cleaning.
    """

    REQUIRED_COLUMNS: list[str] = [
        "transaction_id",
        "plan_id",
        "transaction_date",
        "breach_type",
        "disputed_amount",
    ]

    @classmethod
    def ingest_csv(cls, file_path: str | Path) -> pd.DataFrame:
        """Ingests a transactional CSV log, enforces schema requirements,

        and performs vectorized type casting and anomaly validation.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Transactional log not found at path: {path}")

        # High-performance read leveraging optimized C engine
        df = pd.read_csv(
            path,
            dtype={
                "transaction_id": "string",
                "plan_id": "string",
                "breach_type": "string",
                "disputed_amount": "float64",
            },
            parse_dates=["transaction_date"],
        )

        cls._validate_schema(df)
        cls._vectorized_clean(df)
        return df

    @classmethod
    def _validate_schema(cls, df: pd.DataFrame) -> None:
        """Validates that all mandatory evidentiary columns are present."""
        missing_cols = [col for col in cls.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(
                f"Schema violation: Missing required columns: {missing_cols}"
            )

    @classmethod
    def _vectorized_clean(cls, df: pd.DataFrame) -> None:
        """Executes vectorized cleaning and validation without explicit loops

        or pandas.apply().
        """
        # Vectorized null check across mandatory columns
        null_mask = df[cls.REQUIRED_COLUMNS].isna().any(axis=1)
        if null_mask.any():
            raise ValueError(
                f"Data integrity failure: Found null values across {null_mask.sum()} mandatory transaction records."
            )

        # Zero-copy extraction and validation of disputed amounts via NumPy C-contiguous buffer
        amounts: npt.NDArray[np.float64] = df["disputed_amount"].to_numpy(
            dtype=np.float64, copy=False
        )
        if np.any(amounts < 0.0):
            raise ValueError(
                "Evidentiary corruption: Negative transaction amounts detected in exception log."
            )
