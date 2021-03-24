#!/usr/bin/env python3

import sys
import pandas as pd
from pathlib import Path
from src.camcoil_engine import CamCoil

# INFO:
__author__ = "Michail Vrettas, PhD"
__email__ = "michail.vrettas@gmail.com"


# Main function.
def main(sequence=None, pH=None, f_out=None):
    """
    This is the main function that is called
    to initiate the camcoil_engine prediction.

    :param sequence: (string) of amino-acids.

    :param pH: (float)  determines the specific
    random coil (reference) values that will be
    used to generate the prediciotns.

    :param f_out: (path) if given, the output
    will be saved there instead of the screen.

    :return: None.
    """

    try:
        # Create a CamCoil object.
        r_coil = CamCoil(pH=pH)

        # Predict the random coil values.
        df_data = r_coil.predict(sequence, verbose=True)
    except Exception as e1:
        # Display the message.
        print(f" Program ended with -> {e1}")

        # Exit the program.
        sys.exit(1)
    # _end_try_

    # Check if we want to save the resutls.
    if f_out:
        # Make sure its a Path().
        f_path = Path(Path(f_out) / "random_coil.csv")

        # Save to csv.
        df_data.to_csv(f_path, na_rep='nan')

        # Display a confirmation.
        print(f"Data saved to: {f_path}")
    else:
        # Here we just display on the screen.
        print(df_data)
    # _end_if_

# _end_main_


# Run the main script.
if __name__ == "__main__":

    # Check if we have given input parameters.
    if len(sys.argv) > 1:
        # Local import.
        import argparse

        # Create a parser object
        parser = argparse.ArgumentParser(description=" PyCamcoil (v0.1):  "
        "Generates random coil chemical shift values that are obtained by "
        "analyzing the amino acid sequences in the loop regions.")

        # Input sequence of amino-acids (one-letter-code).
        parser.add_argument("-s", "--seq", type=str, required=True,
                            help="Input sequence (string) of amino-acids "
                                 "(REQUIRED)")

        # Input file with simulation data.
        parser.add_argument("--pH", type=float, default=7.0,
                            help="pH value of reference chemical shifts "
                                 "[default=7.0]")

        # Input file with simulation parameters.
        parser.add_argument("--out", type=str, default=None,
                            help="Output 'path' to save the predicted values. "
                                 "The default file name is 'random_coil.csv' ")

        # Parse the arguments.
        args = parser.parse_args()

        # Call the main function.
        main(args.seq, args.pH, args.out)

    else:
        sys.exit("Error: Not enough input parameters.")
    # _end_if_

# _end_program_
