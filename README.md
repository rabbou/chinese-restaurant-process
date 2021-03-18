# The Chinese Restaurant Process
###### Computational Biology
###### Ruben Abbou & Jack Potrykus

# Overview

In this repository, we provide a python package complete with utilities to simulate draws from a Chinese Restaurant Process, as well as a vignette covering motivation _for_, algorithm overview and example use-cases _of_, and simulations _from_ the Chinese Restaurant Process.

# Directory Structure

```
 chinese-restaurant-rpocess               # Repository root
  ├── assets                              # Images and animations
  ├── doc                                 # sphinx-autodoc preferences and output
  ├── src                                 # Source code for package
  │   ├── chinese_restaurant_process.py   # Provides class ChineseRestaurantProcess
  │   ├── chinese_restaurant_mixture.py   # Provides class ChineseRestaurantMixture
  └── vignette                            # Rmarkdown and bibtex files for the vignette
```

# Using the Package

The package is extensively documented -- see `package_crp_manual.pdf` for documentation on every method in each class.
Example usage of each class is can be seen in the vignette, or in the `if __name__ == "__main__":` block at the end of each of the files in `src`.
