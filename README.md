# Moodle Converter

This package aims to build a bridge between pythonic calculations and moodle 
formulas. It is designed to be used in a Jupyter Notebook environment.
The Idea is that you can use python to make some calculations and then use
this package to convert the formulas to a moodle compatible format to use in
quizzes.

# Minimal Example
```python
import moodleconverter.converter as mc

eq = "lam * pow(10,3) + 5 * x"

const = {
    "lam": "23",
}
variables = {
    "x": "x",
}

moodle = mc.python_to_moodle(eq, variables, const)
print(moodle)
```

# Installation

As this package is not yet available on PyPi, you have to install it manually with the following command after cloning the repository:
```bash
pip install -e .
```


# Advanced Example
```python
import math
import moodleconverter.converter as mc
from pint import UnitRegistry

ureg = UnitRegistry()

# define the variables
lam = 1e-6 * ureg.meter
T = 6193 * ureg.K
ds = 1.21 * ureg.kilometer
rs = 146 * ureg.kilometer
rho = 0.25

# define the constants
c = 299_792_458 * ureg.meter / ureg.second
h = 6.626e-34 * ureg.joule * ureg.second
k = 1.381e-23 * ureg.joule / ureg.kelvin

# First part of the equation
L_SK = ((2 * h * pow(c,2))/(pow(lam,5))) / (math.exp((h * c)/(lam * k * T)) - 1)
print(f"L_SK = {L_SK:.2e}")

# Second part of the equation
L_E = rho * (pow((ds * 1e6),2)/(4 * pow((rs * 1e6),2))) * L_SK
print(f"L_E = {L_E:.2e}")

# convert to output unit
output_unit = ureg.watt / ureg.meter**2 / ureg.micrometer / ureg.steradian
L_E.ito(output_unit)
print(f"L_E = {L_E:.2f}")

# compare complete equation
calculation = rho * (pow((ds * 1e6),2)/(4 * pow((rs * 1e6),2))) * ((2 * h * pow(c,2))/(pow(lam,5))) / (math.exp((h * c)/(lam * k * T)) - 1) * pow(10, -6)
assert calculation.magnitude == L_E.magnitude

# rewrite the calculation as a string
equation = "rho * (pow((ds * 1e6),2)/(4 * pow((rs * 1e6),2))) * ((2 * h * pow(c,2))/(pow(lam,5))) / (math.exp((h * c)/(lam * k * T)) - 1) * pow(10, -6)"

moodle_constants = {
    "h": "6.626e-34",
    "c": "299_792_458",
    "lam": "1e-6",
    "k": "1.381e-23",
}

moodle_variables = {
    "rho": "rho",
    "ds": "ds",
    "rs": "rs",
    "T": "T",
}

moodle = mc.python_to_moodle(equation, moodle_variables, moodle_constants)
print(moodle)
```