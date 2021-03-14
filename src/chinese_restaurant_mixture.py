import os
import numpy as np
from matplotlib import pyplot as plt
from sklearn.neighbors import KernelDensity
from matplotlib.animation import FuncAnimation
from chinese_restaurant_process import ChineseRestaurantProcess


class ChineseRestaurantMixture(ChineseRestaurantProcess):
    """
    Inherits from ChineseRestaurantProcess class, with the extra utility provided
    simply being a wrapper around the Process.
    """

    def __init__(self, alpha, param_prior, sampler):
        """
        Initialize a ChineseRestaurantMixture class with concentration parameter alpha
        Higher choice of alpha leads to more tables for fixed number of customers

        Attributes
        ----------
        alpha: float
            concentration parameter
        tables: dict
            keys are table #s (ints), values are arrays, indicating which n resulted
            in a customere sitting at that table
        history: list
            list of all previous states of the Process
        n: int
            number of states simulated, plus 1
        param_prior: int -> (int or float)
            since the number of tables is theoretically infinite, this is a function which maps
            table # (int) to a int or float (parameter value). That is, param_prior(k) should
            yield a draw from the prior distribution of theta_k
        sampler: (int or float) -> (int or float)
            function which takes a parameter value from param_prior and samples from a certain
            distribution with given parameter value
        datapoints: np.ndarray (int or float)
            array of the sampled values from the mixture
        """
        super().__init__(alpha)
        self.param_prior = param_prior
        self.sampler = sampler
        self.datapoints = None

    def reset(self):
        """
        Reset the ChineseRestaurantMixture by clearing self.datapoints
        """
        self.datapoints = None

    def sample(self, sample_size, reset=False):
        """
        Sample sample_size points from a Chinese Restaurant Mixture process.

        Arguments
        ---------
        sample_size: int
            number of points to sample
        reset: bool
            whether or not to reset self.datapoints before proceeding
        """
        if reset and self.datapoints is not None:
            self.reset()
        self.iter(sample_size)

        ntables = len(self.tables)
        params = np.array([self.param_prior(idx) for idx in np.arange(ntables)])

        datapoints = np.zeros(self.n)
        offset = 0
        for param, table_size in zip(params, self.get_table_sizes()):
            for ii in np.arange(table_size):
                datapoints[offset + ii] = self.sampler(param)
            offset += table_size

        np.random.shuffle(datapoints)
        self.datapoints = datapoints

    def visualize(self, first_n=None, clear=False):
        """
        Visualize the final state of the Mixture Process as a kernel density estimate

        Arguments
        ---------
        first_n: int
            (optional) visualize the first first_n datapoints (to be used in animate() method).
            Default behavior is to use all datapoints

        Returns
        -------
        plt.figure
            Kernel density estimate of datapoints
        """

        # Fix x-axis and plot xlims before plotting
        x_axis = np.linspace(self.datapoints.min(), self.datapoints.max())
        plt.xlim(self.datapoints.min(), self.datapoints.max())

        # Limit dataset to just the first_n points
        first_n = (len(self.datapoints) - 1) if first_n is None else first_n
        data = self.datapoints[: (first_n + 1)]
        kde = KernelDensity(bandwidth=1.0, kernel="gaussian").fit(data.reshape(-1, 1))
        logprob = kde.score_samples(x_axis.reshape(-1, 1))

        # Set y lims
        plt.ylim(0, np.exp(logprob).max() + 0.1)

        if clear:
            plt.clf()
            plt.plot(x_axis, np.exp(logprob))
        plt.title(
            r"Density estimate after $n = {}$ samples, $\alpha = {}$".format(
                first_n, self.alpha
            )
        )
        plt.xlabel("Observed $X$ values")
        plt.ylabel("Density estimate")
        return plt.fill_between(x_axis, np.exp(logprob), alpha=0.2)

    def animate(self, clear=False):
        """
        Animate the progress of the CRT by looping through self.history and
        producing a bar plot at each interval
        """
        fig = plt.figure(figsize=(8, 5))

        v = lambda idx: self.visualize(idx, clear=clear)
        anim = FuncAnimation(
            fig, v, repeat=False, blit=False, frames=self.n, interval=100
        )
        return anim


if __name__ == "__main__":
    # Parameter prior: in this case, we draw a normal prior for each theta_idx with
    # mean 10 + idx and standard devation 2.5
    param_gen = lambda idx: np.random.normal(loc=10 + idx, scale=2.5, size=1)[0]
    # Sampler for N(theta, theta^2) family
    sampler = lambda param: np.random.normal(loc=param, scale=param, size=1)[0]

    # Produce visualizations and animations for several alpha values
    for alpha in np.array([1.0, 5.0, 20.0, 50.0]):
        # Initialize the ChineseRestaurantMixture class
        crm = ChineseRestaurantMixture(
            alpha=alpha, param_prior=param_gen, sampler=sampler
        )
        # Sample 400 points from the mixture distribution specified
        crm.sample(400)
        print(crm)

        # Example of ChineseRestaurantProcess.visualize() method
        fig = crm.visualize(clear=True)
        plt.savefig(os.path.join("..", "assets", "mixture_a{}.png".format(alpha)))

        # Example of ChineseRestaurantProcess.animate() method
        anim = crm.animate(clear=True)

        # Uncomment to save anim to a GIF file
        anim.save(
            os.path.join("..", "assets", "mixture_a{}.gif".format(alpha)),
            writer="imagemagick",
            fps=30,
        )
