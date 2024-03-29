# Flaring star-planet interactions
## Orbital phase flare de-clustering in close-in star-planet systems

## Abstract

tba

## Introduction

### Flaring star-planet interactions

Stars with masses below about 1.4 $M_\text{Sun}$ possess an outer convection zone. In this zone convective motion and differential rotation of the plasma drives a dynamo that generates magnetic flux. This flux emerges on the surface of the star ([Schatzman 1962](http://articles.adsabs.harvard.edu/full/1962AnAp...25...18S). When these magnetic field lines reconnect in the stellar outer atmosphere, energy is released in an explosion that we call a flare. Reconnection on the surface occurs when an instability is triggered by the stochastic motion of magnetic field lines at the photosphere([Svestka 1976](https://ui.adsabs.harvard.edu/abs/1976sofl.book.....S/abstract), [Priest and Forbes 2002](https://ui.adsabs.harvard.edu/abs/2002A%26ARv..10..313P/abstract)).

But flares can also be caused by a planet that orbits within the Alfvén zone of a star. In that case, the planet triggers the instability by disturbing the magnetic field through which it travels on its orbit ([Lanza 2018](https://ui.adsabs.harvard.edu/abs/2018A%26A...610A..81L/abstract)). 

While the phenomenon is expected to show the same morphology, the origin for these two types of flares are different. We can call the former instrinsic flares, and the latter star-planet interaction flares, or SPI flares. Intrinsic flares are well-studied. Their occurence times are best described as a Poisson process, and their energy distribution follows a power law over several orders of magnitude. These characteristics are not known for SPI flares apart from estimates of maximum flare energy ([Lanza 2018](https://ui.adsabs.harvard.edu/abs/2018A%26A...610A..81L/abstract)). 

In any given light curve of a star with a known planet in close orbit an observed flare could have been caused by either process. How can we tell them apart? One clue is the planet's orbital motion. A statistical clustering of flares around a certain orbital phase is indicative of SPI flares as we expect flares to be induced at the magnetic subplanetary point. Its location is the region where the stellar magnetic flux connects to the planet. On the planet's course around the host star the point moves in and out of the line of sight.

Our goal is to find SPI flares in stacked and scaled light curves of transiting close-in Hot Jupiters around low-mass stars, or else provide upper limits on its effect size. In the following section we describe the data, Kepler light curves with confirmed transits and observed flares. Next, we detail the method by which we intend to distinguish SPI flares from instrinsic flares using a technique widely applied in earthquake research - thinning. We then apply the method to a synthetic but realistic example light curve stack to demonstrate the technique. Finally, we apply the technique to a stack with and without transiting planets.  

## Data

- Synthetic data with realistic values
- Kepler light curves with transiting Hot Jupiters in close orbits around flaring stars
- A control sample of Kepler light curves with transiting Hot Jupiters

### Assumptions about the data

1. The intrinsic flare production process is a Poisson process with a characteristic time scale that depends on the individual flaring activity of the star (source!)
2. Assuming 1. we can also assume periodic boundary conditions that allows us to search for clusters of flares during secondary eclipse.
3. The characteristic time scale for each light curve does not change in the period of observation.
4. The overdensity of flares occurs at similar orbital phases for all star-planet systems.

## Methods

### Scaling and stacking

Light curves with transits have different orbital periods, and typically multiple transits occur in a single light curve for a confirmed exoplanet. We phase-fold all available light curves and stack them. The resulting time dependence of flare occurrences remains a Poisson process with a different characteristic time scale $\lambda$ from the individual light curves.

### Thinning

Thinning is a probabilistic tool to recover a sample of some underlying point process from a set of measurements. Classically, Thinning is used in the context of earthquake research ([van Stiphout, T., J. Zhuang, and D. Marsan 2012](http://www.corssa.org/export/sites/corssa/.galleries/articles-pdf/vanStiphout_et_al.pdf)). Data in this field consists of catalogues containing all earthquake events within a timeframe. Since not all earthquakes are triggered due to a region's seismicity but most are aftershocks, which cluster around the mainshocks, finding the mainshocks is statisically demanding. To estimate the background intensity of the mainshocks the data has to be declustered, removing the the aftershocks in the process ([Zhuang, Ogata, Vere-Jones 2002] (https://doi.org/10.1198/016214502760046925)). One way of declustering is stochastic declustering or Thinning ([van Stiphout, T., J. Zhuang, and D. Marsan 2012](http://www.corssa.org/export/sites/corssa/.galleries/articles-pdf/vanStiphout_et_al.pdf)). using this method, the sample recovered by Thinning consists of the most probable mainshocks given that they are distributed according to a homogenous Poisson process.
In particular, under the assumption that the underlying point process is Poisson, theory exists for Thinning to be applicable in a consistent way ([Vere-Jones 1970] (https://www.jstor.org/stable/2984402)). 

We extend the methodoly to flare occurences in star-planet interactions by identifying mainshocks with intrinsic flares and aftershocks with SPI flares. In contrast to earthquakes, there is no causal structure between intrinsic flares and SPI flares. Nonetheless, the mathematical framework allows for an application lacking the causal structure. We use a variation of the ETAS model ([Ogata 1999] (https://link.springer.com/chapter/10.1007/978-3-0348-8677-2_14)) proposing a combination of a homogenous Poisson process for the intrinsic flares combined with an inhomogeonous Poisson process for the SPI flares. The full model is, hence, an inhomogenous Poisson process with intensity $\lambda(\phi) = \mu + \psi(\phi)$ where $\mu > 0$ is the intrinsic flare rate and $\psi$ a periodic function capturing the SPI flare rate. Thinning is than applied to the data based on this process.


### Poisson process fitting

We fit an inhomogenous Poisson process to the data by using maximum likelihood estimation for the intensity $\lambda$ (see e.g. ([Vere-Jones 1970] (https://www.jstor.org/stable/2984402)) ). The estimated value $\hat{\mu}$ for $\mu$ is then an estimator for the intrinsic flare rate. To make this work, we assume a parametric form of $\psi$ being linked to the distance between planet and star. 


_relevant when dealing with real data_


## Analysis of results

Some notes:

- Circular orbits:
        - If the planet moves inside the Alfven zone, and if we assume that the field structure is mostly dipolar, we expect the magnetic subplanetary point (MSP) to reside at higher latitudes with increasing planetary distance. 
        - The MSP longitudes will lag behind or precede the longitude of the planet 

- Eccentric orbits:
        - 

# To-Dos:

- [] Implement thinning algorithm (J)
- [] Review thinning algorithm (J+K)
- [x] Write description of the problem (K)
- [] Generate synthetic but realistic data sets to determine upper limits (K)
- [] Implement cluster detection in sets of thinned events (K)
- [] Describe mathematical foundations for Poisson process stacking and thinning 





