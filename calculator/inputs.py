"""Supplied CSV adapter; source reading is independent of the operation."""
from pathlib import Path
import pandas as pd


def read_csv_values(path):
    frame = pd.read_csv(Path(path))
    if "value" not in frame.columns:
        raise ValueError("CSV must contain a column named value.")
    return frame["value"].tolist()
