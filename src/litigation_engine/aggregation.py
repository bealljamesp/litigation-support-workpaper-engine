# src/litigation_engine/aggregation.py

import numpy as np
import numpy.typing as npt
import pandas as pd


class LitigationAggregator:
    """Vectorized calculation engine for ERISA transaction exception aggregation

    and workpaper summary generation.
    """

    @staticmethod
    def compute_prohibited_transfers(
        df: pd.DataFrame, group_cols: list[str], value_col: str
    ) -> pd.DataFrame:
        """Aggregates prohibited transaction amounts using SIMD-aligned pandas/numpy

        operations with zero-copy conversions.
        """
        # Enforce strict zero-copy extraction to C-contiguous array space
        raw_values: npt.NDArray[np.float64] = df[value_col].to_numpy(
            dtype=np.float64, copy=False
        )

        # Vectorized groupby aggregation without explicit loops or apply()
        aggregated = (
            df.groupby(group_cols, observed=False)[value_col]
            .agg(
                transaction_count="count",
                total_loss_amount="sum",
                mean_loss_amount="mean",
                max_loss_amount="max",
            )
            .reset_index()
        )

        # Compute running restitution totals via cumulative vector operations
        loss_array: npt.NDArray[np.float64] = aggregated["total_loss_amount"].to_numpy(
            dtype=np.float64, copy=False
        )
        aggregated["cumulative_liability"] = np.cumsum(loss_array)

        return aggregated
