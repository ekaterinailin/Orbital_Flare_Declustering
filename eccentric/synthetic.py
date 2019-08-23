# Python 3.5
# Synthetic data generator.

import numpy as np
import pandas as pd
from warnings import warn
from .helper import find_nearest

class HotJupiterHost(object):
    """Keep the stellar properties in a
    star class."""
    def __init__(self, period=None, first_periastron_time=None):
        self.period = period
        self.first_periastron_time = first_periastron_time

    def __repr__(self):
        return('Hot Jupiter host star, orbital period = {}'.format(self.period))


class SyntheticFlares(object):
    """A synthetic list of flares derived
    from a light curve with a planet with
    known properties.

    Attributes:
    ------------
    hjhost : HotJupiterHost object
    observation_deltat : float
        total observation time in days
    first_observation_time : float
        time of first observation in time series
    cadence : float
        number of observations per hour
    flares_per_day : float
        number of flares observed per day on average
    poisson_parameter : float
        lambda parameter days^-1

    """
    def __init__(self, hjhost=HotJupiterHost(), observation_deltat=None,
                 first_observation_time=0, cadence=None, flares_per_day=None):

        self.hjhost = hjhost
        self.observation_deltat = observation_deltat
        self.first_observation_time = first_observation_time
        self.cadence = cadence
        self.flares_per_day = flares_per_day
        self.poisson_parameter = 1. / 24. / self.cadence * self.flares_per_day # number of flares per observation time interval
        self.generate_observation_time()
        if self.hjhost.first_periastron_time is None:
            self.random_first_periastron_time()

    def random_first_periastron_time(self):
        """Generate a random first periastron time.

        """
        if self.observation_time.shape[0] == 0:
            raise ValueError("No observations times given."
                             " Try adding observation_deltat >0 to the object.")
        start, finish = self.observation_time[[0,-1]]
        random_periastron_time = start  + np.random.rand() * (finish - start)
        self.hjhost.first_periastron_time = start + (random_periastron_time - start) % self.hjhost.period

    def generate_observation_time(self):
        """Generate a series of observation times from
        given start, duration, and cadence.
        """
        self.observation_time = np.linspace(self.first_observation_time,
                                        self.first_observation_time + self.observation_deltat,
                                        int(np.rint(self.observation_deltat * 24 * self.cadence + 1)))

    def generate_synthetic_flares(self, model="Gauss", **kwargs):
        """Generate synthetic flares and construct a
        table of measurements.

        Paramaters:
        -----------
        model : str
            What model to use to generate cluster?
            Default: Gauss
        kwargs : dict
            Keyword arguments to pass to :func:`generate_spi_flares`
        """
        self.generate_intrinsic_flares()
        self.generate_spi_flares(model=model, **kwargs)
        self.merge_spi_and_instrinsic_flares()


    def generate_intrinsic_flares(self):
        """Produces a Poisson process generated list
        of flares at random observation times.
        """

        if self.observation_time.shape[0] < self.flares_per_day * self.observation_deltat:
            warn("More flares expected that observation times generated.\n"
                 "Almost all observations will see flares now.")
        isflares = np.where(np.random.poisson(lam = 1. / 24. / self.cadence * self.flares_per_day,
                                      size = len(self.observation_time)))[0]
        self.flare_peak_times = self.observation_time[isflares]


    def generate_spi_flares(self, model='Gauss', **kwargs):
        """Produces a list of SPI flares
        at random observation times from a model.
        Running the function again rewrites the flare events.

        Parameters:
        --------------
        model : str
            What model to use to generate cluster?
            Default: Gauss
        kwargs : dict
            Keyword arguments to pass to model flare generator.
        """

        models = {"Gauss": self._spi_flares_gauss}
        if model not in models.keys():
            raise KeyError("This model does not exist.")
        models[model](**kwargs)

    def _spi_flares_gauss(self, phase=0.7, width=0.05, size=1):
        """Generates flares from a Gaussian distribution.

        ***
        Could be faster...
        ***


        Parameters:
        -----------
        phase : float
            default 0.7, phase=0.5 is mid-periastron
        width : float
            default .05, sigma of gaussian distribution
        size : int
            number of events drawn from the distribution
        """
        if ((phase==0.7) & (width==.05) & (size==1)):
            string = ("\nYou are using default values for the Gaussian cluster:\n"
                     "phase={}, width={}, and size={}".format(phase, width, size))
            warn(string)

        if size > self.observation_time.shape[0]:
            warn("You generate more SPI flares than there are observations.\n"
                 "These are way too many SPI flares.")

        if ((phase < 0) | (phase > 1)):
            raise ValueError("\nPhase value must be between 0 and 1.")

        first_mid_cluster = self.hjhost.first_periastron_time + (phase - 0.5) * self.hjhost.period

        spi_flare_times = []
        t_i = first_mid_cluster
        while t_i < self.observation_time[-1]:
            spi_flare_times += list(np.random.normal(loc=t_i, scale=width, size=size))
            t_i += self.hjhost.period

        self.spi_flare_peak_times = list(set([find_nearest(self.observation_time, t) for t in spi_flare_times]))

    def merge_spi_and_instrinsic_flares(self):
        """Superimpose intrinsic and SPI flares.
        If SPI flares and intrinsic flares coincide
        drop one of them and call the respective
        flare ambiguous.
        """
        if ((not(hasattr(self,'flare_peak_times'))) | (not(hasattr(self,'spi_flare_peak_times')))):
            raise AttributeError("\nNothing to merge.")

        intrinsic = pd.DataFrame({"source":"intrinsic",
                                  "peak_time":self.flare_peak_times})
        spi = pd.DataFrame({"source":"spi",
                            "peak_time":self.spi_flare_peak_times})
        all_flares = pd.concat([intrinsic, spi])

        # Flag ambiguous flares
        groups = all_flares.groupby("peak_time").count()
        for i in groups[groups.source >1].index.values:
            all_flares.loc[all_flares.peak_time==i, "source"] = "ambiguous"
        self.all_flares = all_flares.drop_duplicates()


    def write_out_synthetic_flare_table(self, path="synth_flares.csv", **kwargs):
        """Write the flare table to a .csv file.
        Not tested.

        Parameters:
        -------------
        path : str
            Path to file
        kwargs : dict
            Keyword arguments to pass to pd.to_csv()
        """
        self.all_flares.to_csv(path, index=False)
        with open(path, 'r+') as file:
            readcontent = file.read()  # store the read value of exe.txt into
                                        # readcontent
            file.seek(0, 0) #Takes the cursor to top line
            header1 = ("#\n# Hot Jupiter host, period [d]\n{}\n"
                       "#\n# Hot Jupiter host, T(first periastron)\n{}"
                       .format(self.hjhost.period, self.hjhost.first_periastron_time))
            header2 = ("#\n# Intrinsic flare time series, lambda(Poisson) [d^-1]\n{}\n"
                       "#\n# Intrinsic flare time series, start [d], finish [d]\n{},{}"
                       .format(self.poisson_parameter, self.observation_time[0],
                               self.observation_time[-1]))
            headers = [header1, header2]
            for header in headers:
                file.write(header + "\n") #convert int to str since write() deals
                                           # with str
            file.write(readcontent) #after content of string are written, I return
                                     #back content that were in the file