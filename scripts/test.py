from ttc_tools.io import load_ttc_data
from ttc_tools.process import plot_fy_vs_sa_by_fz_under_conditions

def main():
    filepath = "B2356run6.dat"
    ttc = load_ttc_data(filepath)

    fz_levels = [-220.0, -440.0, -660.0, -880.0, -1100.0]
    p_levels = [55.0, 83.0]
    v_levels = [24, 40, 72]
    ia_levels = [0.0, 2.0, 4.0]

    target_p = 83.0
    target_v = 40.0
    target_ia = 4.0

    plot_fy_vs_sa_by_fz_under_conditions(
        ttc=ttc,
        fz_levels=fz_levels,
        p_levels=p_levels,
        v_levels=v_levels,
        ia_levels=ia_levels,
        target_p=target_p,
        target_v=target_v,
        target_ia=target_ia
    )


if __name__ == "__main__":   main()