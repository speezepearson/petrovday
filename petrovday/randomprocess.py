import abc
import random

class RandomProcess:
  def __init__(self, seed=None):
    self.seed = seed if (seed is not None) else random.random()

  @abc.abstractmethod
  def sample(self, x):
    pass

class WeightedSumRandomProcess(RandomProcess):
  def __init__(self, weighted_subprocesses, **kwargs):
    super().__init__(**kwargs)
    self.weighted_subprocesses = weighted_subprocesses

  def sample(self, x):
    return sum(p.sample(x)*w for (w, p) in self.weighted_subprocesses)

class RegularlyInterpolatedRandomProcess(RandomProcess):
  def __init__(self, sample_at_checkpoint, *, origin=0, scale=1, **kwargs):
    super().__init__(**kwargs)
    self.sample_at_checkpoint = sample_at_checkpoint
    self.origin = origin
    self.scale = scale

  def sample(self, x):
    prev_checkpoint = self.origin + self.scale*((x-self.origin)//self.scale)
    next_checkpoint = prev_checkpoint + self.scale

    w = (x - prev_checkpoint) / (next_checkpoint - prev_checkpoint)
    return (self.sample_at_checkpoint(random.Random((self.seed, next_checkpoint)), next_checkpoint) * w +
            self.sample_at_checkpoint(random.Random((self.seed, prev_checkpoint)), prev_checkpoint) * (1-w))

def white_noise(scales, weights=None, **kwargs):
  if weights is None:
    weights = [scale**.5 for scale in scales]

  return WeightedSumRandomProcess([
    (weight, RegularlyInterpolatedRandomProcess(
               sample_at_checkpoint=(lambda r, x: r.normalvariate(0, 1)),
               scale=scale,
               **kwargs))
    for (scale, weight) in zip(scales, weights)
  ])
