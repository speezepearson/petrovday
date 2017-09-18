import random
import math
import datetime as dt
from petrovday.randomprocess import white_noise

def real_close(x, y, epsilon=1e-9):
  return abs(x-y) < epsilon

class TestWhiteNoise:

  def test_readings_for_same_time_are_consistent(self):
    r = white_noise([1])
    t1 = 1234
    t2 = 5.678
    x1 = r(t1)
    x2 = r(t2)

    assert x1 == r(t1)
    assert x2 == r(t2)

  def test_processes_with_same_seed_produce_identical_samples(self):
    r1 = white_noise([1], seed=1)
    r2 = white_noise([1], seed=1)
    assert r1(1.234) == r2(1.234)

  def test_processes_with_different_seeds_produce_different_samples(self):
    r1 = white_noise([1], seed=1)
    r2 = white_noise([1], seed=2)
    assert r1(1.234) != r2(1.234)

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
      r = white_noise([1], seed=0)
      xs = [r(t) for t in range(10**4)]
      for threshold in [-3, -1, 0, 1, 3]:
        self.assert_plausible(xs, threshold)

    def test_distribution_at_checkpoints_looks_about_right_for_nonunit(self):
      r = white_noise([.001], [10], seed=0)
      xs = [r(t*.001)/10 for t in range(10**4)]
      for threshold in [-3, -1, 0, 1, 3]:
        self.assert_plausible(xs, threshold)

    def test_distribution_varies_linearly_between_checkpoints(self):
      r = white_noise([1], seed=0)
      assert real_close(r(.5)-r(0), r(1)-r(.5))
