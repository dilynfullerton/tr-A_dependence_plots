# tr-A_dependence_plots
_Coming soon_: MORE information about this stuff. Oooh weee! I can't wait

### Overview
---
_Coming soon._

### Dependencies
---

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
---
The following should be done to prepare for usage:

1. Clone this repository to the desired directory.

    ```bash
    git clone https://github.com/dilynfullerton/tr-A_depdendence_plots.git
    ```
2. Get familiar with the data defintions used.

### Data definitions
---
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
(aka **_transform_**) callable object that performs a transformation
on a curve or **_plot_**.  
See `transforms.py`.
##### Form:

```
t(x_array, y_array, *args) -> (next_x, next_y, *args)
```
where
* `x_array`: (see **_plot_** definition)
* `y_array`: (see **_plot_** definition)
* `next_x`: transformed x array
* `next_y`: transformed y array
* `*args`: other arguments, which are unchanged by the
transformation (but may be referenced by the transformation).

The inclusion of `args` is particularly convenient for working with
a **_plot_**.
```python
transformed_plot = t(*plot)
```
Alternatively, a **_transform_** could be used independently of
a **_plot_**, as long as `args` is not referenced by the
**_transform_**.  

##### Composition:
Another benefit of the above definition is that a series of
**_transform_** can be composed.  
This may be done manually:
```python
next_plot = t2(*t1(*plot))
```
Or it may be done using `compose_transforms`:
```python
t_comp = compose_transforms([t2, t1])
next_plot = t_comp(*plot)
```

#### _Plot super transform_:
(aka **_super transform_**) callable object that performs a
transformation on a list of **_plot_**. This is a
generalization of **_plot transform_**.
See `transforms_s.py`.
##### Form:

```
st(list_of_plot) -> next_list_of_plot
```
where
* `list_of_plot`: list of **_plot_**
* `next_list_of_plot`: transformed list of **_plot_**

#### _Fit function_:  
(aka **_fitfn_**, `FitFunction`) callable object used for fitting.  
See `FitFunction.py`.
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
---
_Coming soon._

### Future developments
---
_Coming soon._
