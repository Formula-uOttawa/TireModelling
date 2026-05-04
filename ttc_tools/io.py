# Read TTC .dat files and return data as a TTCData class


import numpy as np
from dataclasses import dataclass


@dataclass
class TTCData:
    filepath: str
    tire_name: str
    run_number: int
    rim_width: float
    channels: list[str]
    units: list[str]
    data: np.ndarray


def read_ttc_header(filepath: str):
    with open(filepath, "r") as f:
        first_line = f.readline().strip()
        channels_line = f.readline().strip()
        units_line = f.readline().strip()

    tire_name = ""
    rim_width = None
    run_number = None

    if "Tire_Name=" in first_line:
        after = first_line.split("Tire_Name=", 1)[1]   # text after 'Tire_Name='
        tire_part = after.split(";", 1)[0]             # up to next ';'
        tire_name = tire_part.strip()

    if "Rim_Width=" in first_line:
        after = first_line.split("Rim_Width=", 1)[1]   # text after 'Rim_Width='
        rim_part = after.split(";", 1)[0]              # e.g. '7.0'
        rim_width = float(rim_part.strip())

    if "Run" in first_line:
        after = first_line.split("Run", 1)[1]   # text after 'Run'
        run_part = after.split(";", 1)[0]              # e.g. '2'
        run_number = int(run_part.strip())

    channels = channels_line.split()
    units = units_line.split()

    return tire_name, rim_width, run_number, channels, units


def load_ttc_arrays(filepath: str):
    with open(filepath, "r") as f:
        lines = f.readlines()
    
    data_lines = lines[3:]  # skip first 3 header lines
    
    rows = []
    for line in data_lines:
        parts = line.strip().split()
        row = [float(x) for x in parts]
        rows.append(row)

    data_array = np.array(rows)

    return data_array


def load_ttc_data(filepath: str) -> TTCData:
    tire_name, rim_width, run_number, channels, units = read_ttc_header(filepath)
    data = load_ttc_arrays(filepath)
    data = data[1500:, :]  # skip warmup - first 1500 rows of data

    return TTCData(
        filepath=filepath,
        tire_name=tire_name,
        run_number=run_number,
        rim_width=rim_width,
        channels=channels,
        units=units,
        data=data
    )
    