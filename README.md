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
**_Plot_**: single curve defined by a 4-tuple of the form

```
(x_array, y_array, const_list, const_dict)
```


**_Fit function_**: (aka fitfn, `FitFunction`) callable object used for
fitting, which takes the form

```
(x, params, const_list, const_dict) -> y
```
where
* `x`: value of the independent variable; a real number
* `params`: list of parameters the functional form of the fit
depends on \(to be optimized\)
* `const_list`: ordered list of constants related to the particular
**_plot_** or optimization
* `const_dict`: dictionary of named constants related to the
particular **_plot_** or optimization
* `y`: value of the dependent variable (the fit); a real number

A **_fit function_** has the field
```python
self.num_fit_params
```
which gives the number of fit parameters necessary to evaluate the
function.

_Coming soon: MORE_
	
### Usage
_Coming soon._

### Future developments
_Coming soon._
