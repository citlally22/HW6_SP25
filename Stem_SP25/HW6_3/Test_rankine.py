# rankine_test.py
# This script tests two different Rankine cycles using the Rankine class.

from rankine import rankine  # Import the Rankine class from rankine.py

def main():
    '''
    Main function to test two different Rankine cycles.
    It creates two Rankine cycle objects:
    1. A cycle with saturated vapor entering the turbine.
    2. A cycle with superheated steam entering the turbine.
    It then prints the summary of each cycle.
    '''

    # Rankine cycle with saturated vapor entering the turbine
    # - High pressure: 8000 kPa
    # - Low pressure: 8 kPa
    # - t_high = None means the steam is saturated vapor at the turbine inlet
    rankine1 = rankine(p_low=8, p_high=8000, t_high=None, name='Rankine Cycle (Saturated Vapor)')
    rankine1.print_summary()  # Print the cycle summary

    # Rankine cycle with superheated steam entering the turbine
    # - High pressure: 8000 kPa
    # - Low pressure: 8 kPa
    # - t_high = 1.7 * 295 (where 295 is assumed to be the saturation temperature in Kelvin)
    #   This results in superheated steam entering the turbine.
    rankine2 = rankine(p_low=8, p_high=8000, t_high=1.7 * 295, name='Rankine Cycle (Superheated Steam)')
    rankine2.print_summary()  # Print the cycle summary

# Ensures that the script runs only when executed directly (not when imported as a module)
if __name__ == "__main__":
    main()