import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class ChineseRestaurantProcess:
    """
    Initializes and provides utilities to draw from Chinese Restuarant Process
    """

    def __init__(self, alpha):
        """
        Initialize a ChineseRestaurantProcess class with concentration parameter `alpha`
        Higher choice of `alpha` leads to more tables for fixed number of customers

        Attributes
        ----------
        alpha: float
            concentration parameter
        tables: dict
            keys are table #s (ints), values are arrays, indicating which `n` resulted
            in a customere sitting at that table
        history: list
            list of all previous states of the Process
        n: int
            number of states simulated, plus 1
        """
        self.alpha = alpha
        self.tables = {}
        self.history = []
        self.n = 1

    def __repr__(self):
        df = self.to_pandas()
        ntables = len(df)
        return """Chinese Restaurant Process

Parameters
----------
alpha = {}
n     = {}

Simulation results
------------------
Number of tables = {}
Number of customers at each table:
{}
""".format(
            self.alpha, self.n - 1, ntables, df
        )

    def to_pandas(self):
        return pd.DataFrame.from_dict(
            self.get_table_dict(), orient="index", columns=["Number of Customers"]
        )

    def get_table_names(self):
        """
        Get an array of the names of each table

        Returns
        -------
        np.array
            array of the table names
        """
        return np.array(list(self.tables.keys()))

    def get_table_sizes(self):
        """
        Get an array of the number of people at each table

        Returns
        -------
        np.array
            array of number of people at each table
        """
        return np.array([len(v) for v in self.tables.values()])

    def get_table_dict(self):
        """
        Get a dictionary of pairs from `get_table_names()` and `get_table_sizes()`

        Returns
        -------
        dict:
            keys = table ids (int), values = # of customers at each table (int)
        """
        return {k: len(v) for k, v in self.tables.items()}

    def get_wts(self):
        """
        Returns
        -------
        float:
            probability of sitting at a new table
        array:
            probabilities of sitting at each of the existing tables, conditional on
            _not_ sitting at a new table
        """
        table_sizes = self.get_table_sizes()
        return self.alpha / (self.n - 1 + self.alpha), table_sizes / np.sum(table_sizes)

    def iter(self, niter):
        """
        Iterate the process `niter` times.

        Parameters
        ----------
        niter: int
            number of draws to make from the Process

        Returns
        -------
        ChineseRestaurantProcess:
            Returns `self`, so you can call it inline with assignment, i.e.
        ```python
        crt = ChineseRestaurantProcess(alpha=1).iter(100)
        ```
        """

        def step(self):
            """
            Execute a single step in the Process
            """
            # Get probability of new table and normalized weights of existing tables
            new, probs = self.get_wts()
            if np.random.random() <= new:
                # Add a new table to `self.tables`
                self.tables[len(self.tables)] = np.array([self.n])
            else:
                # Append `self.n` to an existing table
                sel = np.random.choice(np.arange(len(self.tables)), size=1, p=probs)[0]
                self.tables[sel] = np.append(self.tables[sel], self.n)
            # Increment `n` before exiting
            self.n += 1

        for ii in np.arange(niter):
            # Preserve previous states of the Process in `self.history`
            self.history.append(self.get_table_dict())
            step(self)

        return self

    def visualize(self):
        names, sizes = self.get_table_names(), self.get_table_sizes()
        print(names)
        fig = plt.figure(figsize = (8, 5))
        plt.bar(x = names, height = sizes)
        plt.show()


if __name__ == "__main__":
    crt = ChineseRestaurantProcess(alpha=2.5).iter(100)
    print(crt)

    crt.visualize()
