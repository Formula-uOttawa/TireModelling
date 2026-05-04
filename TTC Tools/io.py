# Read TTC .dat files and return data as a TTCData class

import numpy as np
from dataclasses import dataclass

@dataclass
class TTCData:
    filepath: str