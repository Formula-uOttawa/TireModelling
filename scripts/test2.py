from ttc_tools.io import load_ttc_data
import numpy as np

def main():
    ttc = load_ttc_data("B2356run6.dat")

    p_idx = ttc.channels.index("P")
    v_idx = ttc.channels.index("V")

    P = ttc.data[:, p_idx]
    V = ttc.data[:, v_idx]

    print("Unique P values (first 10):", np.unique(P)[:10])
    print("Min/Max V:", V.min(), V.max())

if __name__ == "__main__":
    main()