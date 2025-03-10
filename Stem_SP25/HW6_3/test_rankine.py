from rankine import rankine.py


def main():
    # Define pressures in kPa
    p_high = 8000  # High pressure
    p_low = 8  # Low pressure

    # Case 1: Saturated Steam (x = 1 at turbine inlet)
    rankine1 = Rankine(p_low=p_low, p_high=p_high, name="Saturated Steam Cycle")

    # Case 2: Superheated Steam (T_high = 1.7 * Tsat)
    Tsat_high = 285.83  # Example Tsat at p_high (you might need to compute this)
    T_high = 1.7 * Tsat_high  # Superheated inlet temperature

    rankine2 = Rankine(p_low=p_low, p_high=p_high, t_high=T_high, name="Superheated Steam Cycle")

    # Calculate efficiencies
    eff1 = rankine1.calc_efficiency()
    eff2 = rankine2.calc_efficiency()

    # Print results
    print("\n===== Rankine Cycle Analysis =====")
    rankine1.print_summary()
    print("\n---------------------------------\n")
    rankine2.print_summary()


if __name__ == "__main__":
    main()


