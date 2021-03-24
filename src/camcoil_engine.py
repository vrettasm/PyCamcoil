"""
This module provides a "Python implementation" of the camcoil
program (originally written in C) to estimate the random coil
chemical shift values from a sequence (string) of amino-acids.

The work is described in detail at:

1.  Alfonso De Simone, Andrea Cavalli, Shang-Te Danny Hsu, Wim Vranken
    and Michele Vendruscolo (2009) (https://doi.org/10.1021/ja904937a).
    "Accurate Random Coil Chemical Shifts from an Analysis of Loop
    Regions in Native States of Proteins". Journal of the American
    Chemical Society (JACS), 131 (45), 16332 - 16333.

NOTE:
    The txt files: 'corr_1L', 'corr_2L', 'corr_1R', 'corr_2R',
    are required for the estimation of the random coil values.
    They should be placed in the same directory with the module
    file. If they do not exist the code will exit with an error.

"""

from pathlib import Path
import pandas as pd

from .camcoil_properties import (TARGET_ATOMS,
                                 pH2_prop, pH7_prop, weights)


class CamCoil(object):
    """
    This class implements the CamCoil code in Python.
    """

    # Object variables.
    __slots__ = ("_pH", "_cs", "df")

    # Constructor.
    def __init__(self, pH=7.0):
        """
        Initializes the camcoil object. The pH is given as
        option during the initialization of the object even
        though only two actual implementations exist at the
        moment (i.e., pH=2 and pH=7).

        If the user selects another pH value, this will be
        set automatically to one of these two in the code.

        :param pH: (float) the default pH value is set to 7.0.
        """

        # Check for the correct range.
        if (pH < 0.0) or (pH > 14.0):
            raise ValueError(f"{self.__class__.__name__}: "
                             f"pH value should be in [0, 14]: {pH}.")
        # _end_if_

        # Load the right chemical shifts.
        if pH < 4.0:
            # Assign a fixed pH.
            self._pH = 2.0

            # Get the reference chemical shifts.
            self._cs = pH2_prop
        else:
            # Assign a fixed pH.
            self._pH = 6.1

            # Get the reference chemical shifts.
            self._cs = pH7_prop
        # _end_if_

        # Dictionary of (correction) dataframes.
        self.df = {}

        # Get the parent folder of the module.
        parent_dir = Path(__file__).resolve().parent

        # Load the correction files.
        for f_name in ["corr_1L", "corr_2L", "corr_1R", "corr_2R"]:

            # Make sure the input file is Path.
            f_path = Path(parent_dir / str(f_name + ".txt"))

            # Sanity check.
            if not f_path.is_file():
                raise FileNotFoundError(f"{self.__class__.__name__} : "
                                        f"File {f_path} doesn't exist.")
            # _end_if_

            # Add it to the dictionary.
            self.df[f_name] = pd.read_csv(f_path, header=None,
                                          delim_whitespace=" ",
                                          names=["RES", "ATOM", "CS", "UNKNOWN"])
            # This is to optimize search.
            self.df[f_name] = self.df[f_name].set_index(["RES", "ATOM"])
        # _end-if_

    # _end_def_

    @property
    def pH(self):
        """
        Accessor (getter) of the pH parameter.

        :return: the pH value.
        """
        return self._pH
    # _end_def_

    @pH.setter
    def pH(self, new_value):
        """
        Accessor (setter) of the pH parameter.

        :param new_value: (float).
        """

        # Check for the correct type.
        if isinstance(new_value, float):

            # Check the range of the pH.
            if 0.0 <= new_value <= 14.0:

                # Re-load the right chemical shifts.
                if new_value < 4.0:
                    # Set the fixed pH.
                    self._pH = 2.0

                    # Update the chemical shifts.
                    self._cs = pH2_prop
                else:
                    # Set the fixed pH.
                    self._pH = 6.1

                    # Update the chemical shifts.
                    self._cs = pH7_prop
                # _end_if_

            else:
                raise ValueError(f"{self.__class__.__name__}: "
                                 f"pH value should be in [0, 14]: {new_value}.")
        else:
            raise TypeError(f"{self.__class__.__name__}: "
                            f"pH value should be float: {type(new_value)}.")
        # _end_if_
    # _end_def_

    # Main functionality.
    def predict(self, seq=None, verbose=False):
        """
        Accepts a string amino-acid sequence, and returns
        a prediction with the random coil chemical shifts.

        :param seq: (string) The input amino-acid sequence.

        :param verbose: (bool) If the flag is set to True
        it will print more information on the screen.

        :return: a pandas DataFrame, with the results.
        """

        # Sanity check.
        if seq is None:
            # Show a message.
            raise ValueError(" No input sequence has been given.")
        # _end_if_

        # Make sure there are not empty spaces.
        seq = str(seq).strip()

        # Sanity check.
        if not seq.isalpha():
            # It must contain only characters.
            raise ValueError(f"{self.__class__.__name__}: "
                             f" Input sequence is not valid: {seq}")
        # _end_if_

        # Get the length of the sequence.
        seq_length = len(seq)

        # Check the length of the input.
        if seq_length > 5000:
            raise ValueError(f"{self.__class__.__name__}: "
                             f" Sequence length is too long: {seq_length}")
        # _end_if_

        # Make a quick check for validity.
        for res in seq:
            # Valid residue check.
            if res not in self._cs:
                raise ValueError(f"{self.__class__.__name__}: "
                                 f" Invalid residue name : {res}")
            # _end_if_
        # _end_if_

        # Holds the output values.
        output = []

        # Compute the random coil values.
        for i, res_i in enumerate(seq, start=0):

            # Create a new dictionary. This will
            # hold the chemical shift values for
            # all atoms of the "i-th" residue.
            cs_i = {"RES": res_i,
                    "CA": None, "CB": None, "C": None,
                    "H": None, "HA": None, "N": None}

            # Predict the chemical shifts.
            for atom in TARGET_ATOMS:

                # First get the reference chemical shift.
                cs_i[atom] = getattr(self._cs[res_i], atom)

                # Get the (LOWER) neighbourhood contributions.
                for j in [i - 2, i - 1]:

                    # Check (LOWER) bounds:
                    if j < 0:
                        continue
                    # _end_if_

                    # Backwards link with the i-th residue.
                    b_link_a = seq[j] + res_i

                    if j == i - 1:
                        # Get the weight value.
                        alpha = getattr(weights["-1"], atom)

                        # Get the correction value from the dataframe.
                        corr_val = self.df["corr_1L"].loc[(b_link_a, atom), "CS"]

                        # Add the weighted correction.
                        cs_i[atom] += float(alpha * corr_val)
                    else:
                        # Get the weight value.
                        alpha = getattr(weights["-2"], atom)

                        # Get the correction value from the dataframe.
                        corr_val = self.df["corr_2L"].loc[(b_link_a, atom), "CS"]

                        # Add the weighted correction.
                        cs_i[atom] += float(alpha * corr_val)
                    # _end_if_

                # _end_for_

                # Get the (UPPER) neighbourhood contributions.
                for k in [i + 1, i + 2]:

                    # Check (UPPER) bounds:
                    if k > seq_length - 1:
                        break
                    # _end_if_

                    # Forward link with the i-th residue.
                    a_link_b = res_i + seq[k]

                    if k == i + 1:
                        # Get the weight value.
                        alpha = getattr(weights["+1"], atom)

                        # Get the correction value from the dataframe.
                        corr_val = self.df["corr_1R"].loc[(a_link_b, atom), "CS"]

                        # Add the weighted correction.
                        cs_i[atom] += float(alpha * corr_val)
                    else:
                        # Get the weight value.
                        alpha = getattr(weights["+2"], atom)

                        # Get the correction value from the dataframe.
                        corr_val = self.df["corr_2R"].loc[(a_link_b, atom), "CS"]

                        # Add the weighted correction.
                        cs_i[atom] += float(alpha * corr_val)
                    # _end_if_

                # _end_for_

            # _end_for_

            # Append the results.
            output.append(cs_i)
        # _end_for_

        # Check the flag.
        if verbose:
            # Size of the chunks.
            n = 10

            # Split the amino-acid sequence to chucks of size 'n'.
            chunks = [seq[i:i + n] for i in range(0, seq_length, n)]

            # Print message:
            print(f"SEQUENCE PROCESSED (pH={self.pH}):")

            # Print the sequence in chunks of 10 residues.
            for i, partial in enumerate(chunks, start=1):
                print(f"{i:>3}: {partial}")
            # _end_for_

            # Print an empty line:
            print(" ")
        # _end_if_

        # Return the output in dataframe.
        return pd.DataFrame(data=output)
    # _end_def_

    # Auxiliary.
    def __call__(self, *args, **kwargs):
        """
        This is only a "wrapper" method
        of the "predict" method.
        """
        return self.predict(*args, **kwargs)
    # _end_def_

    # Auxiliary.
    def __str__(self):
        """
        Override to print a readable string presentation of
        the object. This will include its id(.), along with
        its pH field value.

        :return: a string representation of a CamCoil object.
        """
        # Return the f-string.
        return f" CamCoil Id({id(self)}): pH={self._pH}"
    # _end_def_

# _end_class_
