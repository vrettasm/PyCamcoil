#!/usr/bin/env python3

import sys

# Check the current python version before running.
if sys.version_info < (3, 6):
    sys.exit("Error: this program requires Python 3.6 or greater.")
# _end_if_

from pathlib import Path
from src.camcoil_engine import CamCoil

# INFO:
__version__ = "1.0.0"
__author__ = "Michail Vrettas, PhD"
__email__ = "vrettasm@duck.com"


# Main function.
def main(sequences=None, pH=None, f_out=None):
    """
    This is the main function that is called
    to initiate the camcoil_engine prediction.

    :param sequences: (string) of amino-acids.

    :param pH: (float)  determines the specific
    random coil (reference) values that will be
    used to generate the predictions.

    :param f_out: (path) if given, the output
    will be saved there instead of the screen.

    :return: None.
    """

    try:
        # Create a single CamCoil object.
        r_coil = CamCoil(pH=pH)

        # Process all the input sequences.
        for n, seq_n in enumerate(sequences, start=1):

            # Predict the random coil values.
            df_data = r_coil.predict(seq_n, verbose=True)

            # Check if we want to save the results.
            if f_out:
                # Make sure its a Path().
                f_path = Path(Path(f_out) / f"Seq_{n}_Random_Coil.csv")

                # Save to csv.
                df_data.to_csv(f_path, na_rep="nan")

                # Display a confirmation.
                print(f"Data saved to: {f_path}")
            else:
                # Here we just display on the screen.
                print(df_data)
            # _end_if_

            # Make separate predictions more visible.
            print("-END OF PREDICTION-", end="\n")

        # _end_for_

    except Exception as e1:

        # Exit the program.
        sys.exit(f" Program ended with -> {e1}.")

    # _end_try_

# _end_main_


# Run the main script.
if __name__ == "__main__":

    # Check if we have given input parameters.
    if len(sys.argv) > 1:
        # Local import.
        import argparse

        # Create a parser object.
        parser = argparse.ArgumentParser(description="Generates random coil chemical shift values "
                                                     "that are obtained by analyzing the amino-acid "
                                                     "sequences in the loop regions.")

        # Input sequence of amino-acids (one-letter-code).
        parser.add_argument("-s", "--seq", type=str, nargs='+', required=True,
                            help="Input sequence(s) of amino-acids (REQUIRED)")
        # Input pH value.
        parser.add_argument("--pH", type=float, default=7.0,
                            help="pH value of reference chemical shifts "
                                 "[default=7.0]")

        # Output path to save the random coil chemical shifts.
        parser.add_argument("-o", "--out", type=str, default=None,
                            help="Output 'path' to save the predicted values. "
                                 "The default file name is 'Seq_{n}_Random_Coil.csv' ")

        # Shows the version of the program.
        parser.add_argument("--version", action="version",
                            version=f"PyCamcoil (c), version: {__version__}",
                            help="Print version information and exit.")

        # Parse the arguments.
        args = parser.parse_args()

        # Call the main function.
        main(args.seq, args.pH, args.out)
    else:
        # Display error message.
        sys.exit("Error: Not enough input parameters.")
    # _end_if_

# _end_program_
