import pytest
import numpy as np

from ..synthetic import SyntheticFlares, HotJupiterHost

def test_init_SyntheticFlares():
    sf = SyntheticFlares(hjhost=HotJupiterHost(period=1, first_periastron_time=1), observation_deltat=10,
                     first_observation_time=0, cadence=1, flares_per_day=1)
    assert sf.poisson_parameter == 1/24 # 1 flare per day / 1 obs per hour = 1 flare per day / 24 obs per day
    assert sf.hjhost.first_periastron_time == 1
    assert sf.observation_time.shape[0] == 24*10 + 1 #+1 because end point of observations

    sf = SyntheticFlares(hjhost=HotJupiterHost(period=1), observation_deltat=0,
                             first_observation_time=0, cadence=1, flares_per_day=1)
    assert sf.observation_time.shape[0] == 1 # the start observation will always be included

def test_generate_synthetic_flares():
    # test a working example
    sf = SyntheticFlares(hjhost=HotJupiterHost(period=1, first_periastron_time=1),
                                 observation_deltat=10,
                                 first_observation_time=0,
                                 cadence=1, flares_per_day=1)
    sf.generate_synthetic_flares(phase=0.5, size=1, width=0.001)
    assert sf.all_flares.shape[0] > 10 # 10 spi flares, and about 10 intrinsic ones

    # Test case when an unimplemented model is requested
    with pytest.raises(KeyError):
        sf.generate_synthetic_flares(model="BLA", phase=0.5, size=1, width=0.001)


def test_generate_spi_flares():
    sf = SyntheticFlares(hjhost=HotJupiterHost(period=1, first_periastron_time=.9),
                                 observation_deltat=10,
                                 first_observation_time=0,
                                 cadence=1, flares_per_day=1)

    sf.generate_spi_flares(phase=0.5, size=1, width=0.001)
    assert len(sf.spi_flare_peak_times) == 10
    assert np.array(sf.spi_flare_peak_times) - np.arange(10) == pytest.approx(.91666667)

    sf.generate_spi_flares(phase=0.5, size=0, width=0.001)
    assert len(sf.spi_flare_peak_times) == 0 # earlier spi flares get rewritten


def test_generate_intrinsic_flares():
    # Test the case where too many flares are generated
    sf = SyntheticFlares(hjhost=HotJupiterHost(period=1, first_periastron_time=1),
                                 observation_deltat=10,
                                 first_observation_time=0,
                                 cadence=1, flares_per_day=100)

    with pytest.warns(UserWarning):
        sf.generate_intrinsic_flares()
    assert sf.flare_peak_times.shape[0] == pytest.approx(241, rel=.05) # virtually all times are flaring

    # Test the case where barely one flare is generated
    sf = SyntheticFlares(hjhost=HotJupiterHost(period=1, first_periastron_time=1),
                                 observation_deltat=10,
                                 first_observation_time=0,
                                 cadence=1, flares_per_day=.1)
    sf.generate_intrinsic_flares()
    assert sf.flare_peak_times.shape[0] == pytest.approx(1, rel=1) # one flare or none


def test_generate_observation_time():
    """This should fail one day when
    some attributes become un-writeable
    for safety reasons."""
    sf = SyntheticFlares(hjhost=HotJupiterHost(period=1, first_periastron_time=1),
                             observation_deltat=10,
                             first_observation_time=0,
                             cadence=1, flares_per_day=1)
    sf.first_observation_time = 100
    sf.generate_observation_time()
    assert sf.observation_time.shape[0] == 241
    assert sf.observation_time[0] == 100
    assert np.diff(sf.observation_time) == pytest.approx(1./24.)


def test_random_first_periastron_time():
    sf = SyntheticFlares(hjhost=HotJupiterHost(period=1, first_periastron_time=1),
                         observation_deltat=10,
                         first_observation_time=0,
                         cadence=1, flares_per_day=1)
    sf.random_first_periastron_time()
    assert sf.hjhost.first_periastron_time < 1

    sf = SyntheticFlares(hjhost=HotJupiterHost(period=0.5, first_periastron_time=1),
                         observation_deltat=10,
                         first_observation_time=0,
                         cadence=1, flares_per_day=1)
    sf.random_first_periastron_time()
    assert sf.hjhost.first_periastron_time < 0.5


def test__spi_flares_gauss():
    sf = SyntheticFlares(hjhost=HotJupiterHost(period=1, first_periastron_time=1),
                                     observation_deltat=10,
                                     first_observation_time=0,
                                     cadence=1, flares_per_day=1)

    # Test that the default values warning is raised
    with pytest.warns(UserWarning):
        sf._spi_flares_gauss()
        assert len(sf.spi_flare_peak_times) == 9

    # Test that the too many events warning is raised
    with pytest.warns(UserWarning):
        sf._spi_flares_gauss(size=1000, width=0.6)
        len(sf.spi_flare_peak_times) == 241 # too many events, too wide Gaussian

    with pytest.raises(ValueError):
        sf._spi_flares_gauss(phase=3.)

def test_merge_spi_and_instrinsic_flares():
    # generic setup:
    attribs = {"hjhost":HotJupiterHost(period=1,
                                       first_periastron_time=1),
               "observation_deltat":10,
               "first_observation_time":0,
               "cadence":1,
               "flares_per_day":1}

    # Test that merging without a table will fail
    sf = SyntheticFlares(**attribs)
    with pytest.raises(AttributeError):
        sf.merge_spi_and_instrinsic_flares()

    #  Test that merging without intrinsic flares will fail
    sf = SyntheticFlares(**attribs)
    sf.spi_flare_peak_times = [0,1,2]
    with pytest.raises(AttributeError):
        sf.merge_spi_and_instrinsic_flares()

    # Test that merging without spi flares will fail
    sf = SyntheticFlares(**attribs)
    sf.flare_peak_times = [0,1,2]
    with pytest.raises(AttributeError):
        sf.merge_spi_and_instrinsic_flares()

    # Test a working example
    sf = SyntheticFlares(**attribs)
    sf.spi_flare_peak_times = [0,1,2]
    sf.flare_peak_times = [3,4,5]
    sf.merge_spi_and_instrinsic_flares()
    assert (sf.all_flares.peak_time.values == [3,4,5,0,1,2]).all()
    assert (sf.all_flares.source.values == ["intrinsic", "intrinsic", "intrinsic",
                                            "spi", "spi", "spi"]).all()
