import numpy as np
import matplotlib.pyplot as plt
from .io import TTCData


def snap_to_levels(values: np.ndarray, levels: list[float]) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    levels_array = np.asarray(levels, dtype=float)

    # Compute absolute differences between each value and each level
    diffs = np.abs(values[:, None] - levels_array[None, :])

    # For each value, find index of nearest level
    nearest_idx = np.argmin(diffs, axis=1)

    # Map indices back to actual level values
    snapped = levels_array[nearest_idx]

    return snapped


def snap_channel_levels(ttc: TTCData, name: str, levels: list[float]) -> TTCData:
    idx = ttc.channels.index(name)

    new_data = ttc.data.copy()
    col = new_data[:, idx]
    new_data[:, idx] = snap_to_levels(col, levels)

    return TTCData(
        filepath=ttc.filepath,
        tire_name=ttc.tire_name,
        run_number=ttc.run_number,
        rim_width=ttc.rim_width,
        channels=ttc.channels,
        units=ttc.units,
        data=new_data
    )


def select_condition_block(ttc: TTCData, 
                           fz_level: float,
                           p_level: float,
                           v_level: float,
                           ia_level: float,
                           fz_name: str = "FZ",
                           p_name: str = "P",
                           v_name: str = "V",
                           ia_name: str = "IA") -> np.ndarray:
    
    fz_idx = ttc.channels.index(fz_name)
    p_idx = ttc.channels.index(p_name)
    v_idx = ttc.channels.index(v_name)
    ia_idx = ttc.channels.index(ia_name)

    fz = ttc.data[:, fz_idx]
    p = ttc.data[:, p_idx]
    v = ttc.data[:, v_idx]
    ia = ttc.data[:, ia_idx]

    mask_fz = np.isclose(np.abs(fz), abs(fz_level), atol=1e-6)
    mask_p = np.isclose(p, p_level, atol=1e-6)
    mask_v = np.isclose(v, v_level, atol=1e-6)
    mask_ia = np.isclose(ia, ia_level, atol=1e-6)

    mask = mask_fz & mask_p & mask_v & mask_ia
    return mask


def snap_fz_levels(ttc: TTCData, levels: list[float]) -> np.ndarray:
    fz_index = ttc.channels.index("FZ")
    new_data = ttc.data.copy()
    
    fz = new_data[:, fz_index]
    new_data[:, fz_index] = snap_to_levels(fz, levels)

    return TTCData(
        filepath=ttc.filepath,
        tire_name=ttc.tire_name,
        run_number=ttc.run_number,
        rim_width=ttc.rim_width,
        channels=ttc.channels,
        units=ttc.units,
        data=new_data
    )


def snap_p_levels(ttc: TTCData, levels: list[float]) -> np.ndarray:
    p_index = ttc.channels.index("P")
    new_data = ttc.data.copy()
    
    p = new_data[:, p_index]
    new_data[:, p_index] = snap_to_levels(p, levels)

    return TTCData(
        filepath=ttc.filepath,
        tire_name=ttc.tire_name,
        run_number=ttc.run_number,
        rim_width=ttc.rim_width,
        channels=ttc.channels,
        units=ttc.units,
        data=new_data
    )


def snap_v_levels(ttc: TTCData, levels: list[float]) -> np.ndarray:
    v_index = ttc.channels.index("V")
    new_data = ttc.data.copy()
    
    v = new_data[:, v_index]
    new_data[:, v_index] = snap_to_levels(v, levels)

    return TTCData(
        filepath=ttc.filepath,
        tire_name=ttc.tire_name,
        run_number=ttc.run_number,
        rim_width=ttc.rim_width,
        channels=ttc.channels,
        units=ttc.units,
        data=new_data
    )


def snap_ia_levels(ttc: TTCData, levels: list[float]) -> np.ndarray:
    ia_index = ttc.channels.index("IA")
    new_data = ttc.data.copy()
    
    ia = new_data[:, ia_index]
    new_data[:, ia_index] = snap_to_levels(ia, levels)

    return TTCData(
        filepath=ttc.filepath,
        tire_name=ttc.tire_name,
        run_number=ttc.run_number,
        rim_width=ttc.rim_width,
        channels=ttc.channels,
        units=ttc.units,
        data=new_data
    )


def plot_fy_vs_sa_by_fz_under_conditions(ttc: TTCData,
                                         fz_levels: list[float],
                                         p_levels: list[float],
                                         v_levels: list[float],
                                         ia_levels: list[float],
                                         target_p: float,
                                         target_v: float,
                                         target_ia: float):
    
    ttc_s = snap_channel_levels(ttc, "FZ", fz_levels)
    ttc_s = snap_channel_levels(ttc_s, "P", p_levels)
    ttc_s = snap_channel_levels(ttc_s, "V", v_levels)
    ttc_s = snap_channel_levels(ttc_s, "IA", ia_levels)

    sa_idx = ttc_s.channels.index("SA")
    fy_idx = ttc_s.channels.index("FY")

    plt.figure()
    for fz_level in fz_levels:
        mask = select_condition_block(ttc_s,
                                     fz_level = fz_level,
                                     p_level = target_p,
                                     v_level = target_v,
                                     ia_level = target_ia)
        
        print(f"FZ Level {fz_level}: {mask.sum()} points")
        
        sa = ttc_s.data[mask, sa_idx]
        fy = ttc_s.data[mask, fy_idx]

        order = np.argsort(sa)
        sa_sorted = sa[order]
        fy_sorted = fy[order]

        plt.plot(sa_sorted, fy_sorted, label=f"FZ = {fz_level:.0f} N")

    plt.xlabel("SA (deg)")
    plt.ylabel("FY (N)")
    plt.title(f"Run {ttc_s.run_number}: FY vs SA (P={target_p:.0f} kPa, V={target_v:.0f} km/h, IA={target_ia:.0f} deg)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()