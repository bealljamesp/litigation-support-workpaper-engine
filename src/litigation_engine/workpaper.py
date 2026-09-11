# src/litigation_engine/workpaper.py

from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd


class WorkpaperEngine:
    """Generates structured, audit-ready workpapers and evidentiary trial

    exhibits from aggregated ERISA violation logs.
    """

    @staticmethod
    def generate_summary_workpaper(
        aggregated_df: pd.DataFrame, case_caption: str
    ) -> str:
        """Transforms aggregated violation data into a formatted, text-based

        analytical workpaper suitable for inclusion in investigative reports.
        """
        # Zero-copy extraction for high-performance statistical summation
        loss_array: npt.NDArray[np.float64] = aggregated_df[
            "total_loss_amount"
        ].to_numpy(dtype=np.float64, copy=False)
        count_array: npt.NDArray[np.int64] = aggregated_df[
            "transaction_count"
        ].to_numpy(dtype=np.int64, copy=False)

        total_disputed: float = float(np.sum(loss_array))
        total_transactions: int = int(np.sum(count_array))

        # Construct formal analytical workpaper header and summary block
        workpaper_lines = [
            "=" * 80,
            "EXHIBIT WORKPAPER: EBSA LITIGATION SUPPORT SUPPORTING ANALYSIS",
            f"CASE CAPTION: {case_caption}",
            "STATUTORY AUTHORITY: ERISA SECTION 406 / 408 ENFORCEMENT",
            "=" * 80,
            "SUMMARY STATISTICS:",
            f"  - Total Prohibited Transactions Identified: {total_transactions:,}",
            f"  - Cumulative Disputed Restitution Amount:   ${total_disputed:,.2f}",
            "-" * 80,
            "DETAILED PLAN-LEVEL BREAKDOWN:",
            "-" * 80,
        ]

        # Vectorized string formatting for table generation without explicit loops over rows
        formatted_table = aggregated_df.to_string(index=False)
        workpaper_lines.append(formatted_table)
        workpaper_lines.append("=" * 80)
        workpaper_lines.append("END OF WORKPAPER - CERTIFIED TRUE AND CORRECT")
        workpaper_lines.append("=" * 80)

        return "\n".join(workpaper_lines)

    @classmethod
    def export_exhibit_csv(
        cls, aggregated_df: pd.DataFrame, output_path: str | Path
    ) -> Path:
        """Exports structured workpaper tables into CSV format for trial

        exhibit indexing.
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        aggregated_df.to_csv(path, index=False)
        return path
