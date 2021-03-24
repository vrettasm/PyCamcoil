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
[download the code](https://github.com/vrettasm/PyCamcoil/archive/ref/heads/master.zip)
in zip format. This option does not require a prior installation of git on the
computer.

2. Alternatively one can clone the project directly using git as follows:

    `$ git clone https://github.com/vrettasm/PyCamcoil.git`

## Required packages

The recommended version is **Python 3.6+**. Some required packages are:

>
> Numpy, Pandas
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

To see the help type:

    $ python3 camcoil.py --help

**Note:**
The input sequence can be given with and without double-quotes.
Example:

    1. $ python3 camcoil.py -s "TESTAMINOSEQ"

is equivalent to:

    2. $ python3 camcoil.py -s TESTAMINOSEQ

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

For any questions / comments please contact me at: vrettasm@gmail.com