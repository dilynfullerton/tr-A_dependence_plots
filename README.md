# tr-A_dependence_plots
_Coming soon_: MORE information about this stuff. Oooh weee! I can't wait

### Overview
_Coming soon._

### Dependencies

#### Required:
The following are required for using the full functionality of this program:

* [python 2](https://www.python.org/downloads) (2.7 or higher)
* [SciPy](https://www.scipy.org/install.html)
  * scipy
  * matplotlib
  * numpy

#### Recommended:
All of the above requirements and more are included in the Anaconda
distribution.

* [Anaconda](https://www.continuum.io/downloads)

### Setup
The following should be done to prepare for usage:

1. Clone this repository to the desired directory.

    ```bash
    git clone https://github.com/dilynfullerton/tr-A_depdendence_plots.git
    ```
2. Get familiar with the data defintions used.

### Data definitions
#### _Plot_:  
single curve defined by a 4-tuple.
##### Form:

```
(x_array, y_array, const_list, const_dict)
```
where
* `x_array`: ordered numpy array specifying the values of the
independent variable
* `y_array`: ordered numpy array specifying the values of the
depenent variable (same length as `x_array`)
* `const_list`: ordered list of constants related to the particular
curve
* `const_dict`: dictionary of named constants related to the
particular curve

#### _Plot transform_:
(aka transform) callable object that performs a transformation on a
curve or **_plot_**.
##### Form:

```
t(x_array, y_array, *args) -> (new_x, new_y, *args)
```
where
* `x_array`: (see **_plot_** definition)
* `y_array`: (see **_plot_** definition)
* `new_x`: transformed x array
* `new_y`: transformed y array
* `*args`: other arguments, which are unchanged by the
transformation (but may be referenced by the transformation).

The inclusion of `args` is particularly convenient for working with
a **_plot_**.
```python
new_plot = t(*plot)
```
Alternatively, a **_transform_** could be used independently of
a **_plot_**, as long as `args` is not referenced by the
**_transform_**.

#### _Fit function_:  
(aka fitfn, `FitFunction`) callable object used for fitting.
##### Form:

```
f(x, params, const_list, const_dict) -> y
```
where
* `x`: value of the independent variable; a real number
* `params`: list of parameters the functional form of the fit
depends on \(to be optimized\)
* `const_list`: (see **_plot_** definition)
* `const_dict`: (see **_plot_** definition)
* `y`: value of the dependent variable (the fit); a real number

A **_fit function_** `f` has the field `f.num_fit_params`,
which gives the number of fit parameters necessary to evaluate the
function.

_Coming soon: MORE_
	
### Usage
_Coming soon._

### Future developments
_Coming soon._
