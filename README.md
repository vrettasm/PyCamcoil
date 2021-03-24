# PyCamcoil (version 0.1)
---

This repository provides a "Python implementation" of the camcoil program
(originally written in C) to estimate the random coil chemical shift values
from a sequence (string) of amino-acids.

There might be updates in the future, but this first version is now fully operational.

M. Vrettas, PhD.

## Installation
---

There are two options to install the software.

1. The easiest way is to visit the GitHub web-page of the project and
[download the code](https://github.com/vrettasm/PyCamcoil/archive/master.zip)
in zip format. This option does not require a prior installation of git on the
computer.

2. Alternatively one can clone the project directly using git as follows:

    `$ git clone https://github.com/vrettasm/PyCamcoil.git`

## Required packages

The recommended version is **Python 3.6+**. Some required packages are:

>
> numpy, pathlib, pandas
>

## How to run
---

To execute the program, first navigate to the main directory of the project
(i.e. where the camcoil.py is located), and then run the following command:

    $ python3 camcoil.py -s TESTAMINOSEQ

The output should be:

```
SEQUENCE PROCESSED (pH=6.1):
1: TESTAMINOS
2: EQ
 
   RES        CA        CB          C        H       HA          N
0    T  61.30774  70.08048  174.94060  8.22782  4.42540  115.78010
1    E  56.62326  30.30048  176.72142  8.39908  4.33240  122.87622
2    S  58.30388  63.78776  174.88248  8.30858  4.47402  116.85280
3    T  61.39336  69.90206  174.70254  8.17616  4.42510  116.43512
4    A  52.78414  19.21966  177.31598  8.29420  4.34400  126.55214
5    M  55.63120  32.83290  176.46296  8.22956  4.51812  120.84098
6    I  60.63876  39.09866  175.88120  8.26586  4.27638  120.65694
7    N  53.03970  39.16040  175.29378  8.39686  4.74836  122.90968
8    O  62.63300  33.84500  175.98300      NaN  4.76300  139.06800
9    S  58.07210  63.89002  174.83516  8.29660  4.51762  117.30086
10   E  56.58864  30.32174  176.38200  8.37418  4.34432  122.86766
11   Q  55.71748  29.58952  176.10200  8.20326  4.35074  120.44640
```

To see the full help information, type:

    $ python3 camcoil.py --help

**Note:**
The input sequence can be given with and without double-quotes.
Example:

    1. $ python3 camcoil.py -s "TESTAMINOSEQ"

is equivalent to:

    2. $ python3 camcoil.py -s TESTAMINOSEQ

## Performance
---

The code can also be called independently in any other Python programs
by importing the main module as:

```
# Import the main module.
from src.camcoil_engine import CamCoil

# Create an object.
r_coil = CamCoil()

# Use it to get a dataframe.
df_coil = r_coil("APKAPADGL")

# Display the random coil values.
print(df_coil)

   RES        CA        CB          C        H       HA          N
0    A  51.41214  19.07014  176.52162  8.24460  4.47156  125.51232
1    P  62.60744  31.82580  177.00832  NaN      4.43674  137.18000
2    K  56.14292  32.88032  176.38484  8.31074  4.36828  122.10046
3    A  51.34046  19.11406  176.52994  8.21902  4.47378  125.42938
4    P  62.50610  31.85898  177.01894  NaN      4.44632  137.18000
5    A  52.64648  19.28308  177.36534  8.28882  4.33092  124.59918
6    D  54.28196  41.20876  176.66546  8.28206  4.61802  119.64270
7    G  45.88736  NaN       174.37640  8.27726  4.12000  109.77946
8    L  55.03396  42.38164  177.30200  8.04950  4.37060  122.16668
```

The main module (when is called directly inside a python environment as
above) averages around '0.5' sec per '100' residue amino-acid chain:

    %timeit r_coil("APKAPADGLKMEATKQHNAPVVAPKAPADGLKMEATKQHPVVAPKAPADG"
                   "LKMEATKQHPAPKAPADGLKMEATKQHNAPVVAPKAPADGLKMEATKQOH")

    505 ms ± 35.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

## References
---

The work is described in detail at:

1.  [Alfonso De Simone, Andrea Cavalli, Shang-Te Danny Hsu, Wim Vranken
    and Michele Vendruscolo (2009)](https://doi.org/10.1021/ja904937a).
    "Accurate Random Coil Chemical Shifts from an Analysis of Loop
    Regions in Native States of Proteins". Journal of the American
    Chemical Society (JACS), 131 (45), 16332 - 16333.

### Contact
---

For any questions/comments (*regarding the code*) please contact me at:
vrettasm@gmail.com