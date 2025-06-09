"""Simple helpers for exporting data to Excel."""

from pandas import DataFrame


def export_dataframe(df: DataFrame, path: str) -> None:
    """Save a DataFrame to the given Excel file path."""
    df.to_excel(path, index=False)
