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
* `x_array`: (see **_plot_** definition)
* `y_array`: (see **_plot_** definition)
* `next_x`: transformed x array
* `next_y`: transformed y array
* `*args`: other arguments, which are unchanged by the
transformation (but may be referenced by the transformation).

##### Using with _plot_:

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
**_transform_** can be composed. For example, one might with to
apply `t1` and then `t2` to a `plot`.  
This may be done manually:

```python
next_plot = t2(*t1(*plot))
```
Or it may be done using `compose_transforms` from `transforms.py`:

```python
from transforms import compose_transforms
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
* `list_of_plot`: list of **_plot_**
* `next_list_of_plot`: transformed list of **_plot_**

##### Composition:
A series of **_super transform_** may be composed. For example,
one might wish to apply `st1` and then `st2` to a `list_of_plot`.  
This may be done manually:

```python
next_list_of_plot = st2(st1(list_of_plot))
```
Or it may be done using `compose_super_transforms` from
`transforms.py`:

```python
from transforms_s import compose_super_transforms
st_comp = compose_super_transforms([st2, st1])
next_list_of_plot = st_comp(list_of_plot)
```

#### _Fit function_:

(aka **_fitfn_**, `FitFunction`) callable object used for fitting.  
See `FitFunction.py`.

##### Form:

```
f(x, params, const_list, const_dict) -> y
```
* `x`: value of the independent variable; a real number
* `params`: list of parameters the functional form of the fit
depends on \(to be optimized\)
* `const_list`: (see **_plot_** definition)
* `const_dict`: (see **_plot_** definition)
* `y`: value of the dependent variable (the fit); a real number

A **_fit function_** `f` has the field `f.num_fit_params`,
which gives the number of fit parameters necessary to evaluate the
function.

##### Dependence on a constant:

_Coming soon._

##### Combination:

_Coming soon._

#### _Exp_:

_Coming soon._

#### _DataMap_:

See `DataMap.py`.
_Coming soon._

#### _Datum_:

See `Datum.py`
_Coming soon._

#### _Metafitter_:

See `metafit.py`
_Coming soon._

### Usage
---

_Coming soon._

### Future developments
---
_Coming soon._
