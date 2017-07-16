import random
import math
import datetime as dt
from petrovday.randomprocess import RandomProcess

def test_readings_for_same_time_are_consistent():
  r = RandomProcess(noisinesses_by_scale={1: 1})
  t1 = 1234
  t2 = 5.678
  x1 = r.sample(t1)
  x2 = r.sample(t2)

  assert x1 == r.sample(t1)
  assert x2 == r.sample(t2)

def test_processes_with_same_seed_produce_identical_samples():
  r1 = RandomProcess(noisinesses_by_scale={1: 1}, seed=1)
  r2 = RandomProcess(noisinesses_by_scale={1: 1}, seed=1)
  assert r1.sample(1.234) == r2.sample(1.234)

def test_processes_with_different_seeds_produce_different_samples():
  r1 = RandomProcess(noisinesses_by_scale={1: 1}, seed=1)
  r2 = RandomProcess(noisinesses_by_scale={1: 1}, seed=2)
  assert r1.sample(1.234) != r2.sample(1.234)

class TestDistribution:
  @staticmethod
  def phi(x):
    'Cumulative distribution function for the standard normal distribution'
    # stolen from https://docs.python.org/3/library/math.html#math.erf
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
  @classmethod
  def frac(cls, xs, threshold):
    return len([x for x in xs if x<threshold])/len(xs)
  @classmethod
  def frac_stdev(cls, n, threshold):
    return math.sqrt(cls.phi(threshold) * (1-cls.phi(threshold))) / math.sqrt(n)

  @classmethod
  def assert_plausible(cls, xs, threshold):
    m = cls.phi(threshold)
    s = cls.frac_stdev(len(xs), threshold)
    assert (m-5*s < cls.frac(xs, threshold) < m+5*s)

  def test_distribution_at_checkpoints_looks_about_right_for_unit(self):
    r = RandomProcess(noisinesses_by_scale={1: 1}, seed=0)
    xs = [r.sample(t) for t in range(10**4)]
    for threshold in [-3, -1, 0, 1, 3]:
      self.assert_plausible(xs, threshold)

  def test_distribution_at_checkpoints_looks_about_right_for_nonunit(self):
    r = RandomProcess(noisinesses_by_scale={.001: 10}, seed=0)
    xs = [r.sample(t*.001)/10 for t in range(10**4)]
    for threshold in [-3, -1, 0, 1, 3]:
      self.assert_plausible(xs, threshold)

  def test_distribution_varies_linearly_between_checkpoints(self):
    r = RandomProcess(noisinesses_by_scale={1: 1}, seed=0)
    assert r.sample(.5) - r.sample(0) == r.sample(1) - r.sample(.5)

  def test_zeroing_works_for_nonnumbers(self):
    t0 = dt.datetime(2017, 1, 1, 0, 0, 0)
    d = dt.timedelta(1)
    t1 = t0 + 10*d
    r = RandomProcess({d: 1}, zero=t0)
    xs = [r.sample(t1+d*n) for n in range(10**4)]
    for threshold in [-3, -1, 0, 1, 3]:
      self.assert_plausible(xs, threshold)
