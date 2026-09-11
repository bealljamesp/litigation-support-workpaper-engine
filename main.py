# main.py

from pathlib import Path

from litigation_engine.aggregation import LitigationAggregator
from litigation_engine.ingestion import TransactionIngestor
from litigation_engine.workpaper import WorkpaperEngine


def run_pipeline(input_csv: str | Path, output_dir: str | Path) -> None:
    """Executes the full litigation support pipeline: ingestion, vectorized

    aggregation, workpaper generation, and trial exhibit export.
    """
    print(
        "[+] Initializing Litigation Support Workpaper Engine (ERISA Sec. 406/408)..."
    )

    # 1. Ingest and Validate Raw Logs
    print(f"[+] Ingesting transactional logs from: {input_csv}")
    raw_df = TransactionIngestor.ingest_csv(input_csv)
    print(
        f"[+] Successfully validated {len(raw_df):,} records against evidentiary schema."
    )

    # 2. Vectorized Aggregation
    print("[+] Computing prohibited transactions and cumulative liability...")
    aggregated_df = LitigationAggregator.compute_prohibited_transfers(
        raw_df, group_cols=["plan_id", "breach_type"], value_col="disputed_amount"
    )

    # 3. Generate Analytical Workpaper
    case_caption = "EBSA v. Vertex Retirement Services LLC (Case No. 2:26-cv-0406)"
    workpaper_text = WorkpaperEngine.generate_summary_workpaper(
        aggregated_df, case_caption
    )

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    workpaper_file = out_path / "summary_workpaper.txt"
    workpaper_file.write_text(workpaper_text)
    print(f"[+] Workpaper written to: {workpaper_file}")

    # 4. Export Evidentiary Trial Exhibit CSV
    exhibit_file = out_path / "trial_exhibit_schedule_a.csv"
    WorkpaperEngine.export_exhibit_csv(aggregated_df, exhibit_file)
    print(f"[+] Trial exhibit CSV exported to: {exhibit_file}")
    print("[+] Pipeline execution completed successfully.")


if __name__ == "__main__":
    # Default execution path pointing to sample data directory
    sample_input = Path("data/sample_transactions.csv")
    output_directory = Path("output")

    if not sample_input.is_file():
        # Create a mock sample dataset if none exists for immediate demonstration
        sample_input.parent.mkdir(parents=True, exist_ok=True)
        import pandas as pd

        mock_data = pd.DataFrame(
            {
                "transaction_id": ["TXN-1001", "TXN-1002", "TXN-1003"],
                "plan_id": ["Plan_Alpha", "Plan_Alpha", "Plan_Beta"],
                "transaction_date": ["2026-03-01", "2026-03-05", "2026-03-10"],
                "breach_type": ["406(a)", "406(a)", "406(b)"],
                "disputed_amount": [12500.00, 48200.50, 15000.00],
            }
        )
        mock_data.to_csv(sample_input, index=False)
        print(f"[+] Generated mock sample log at: {sample_input}")

    run_pipeline(sample_input, output_directory)
