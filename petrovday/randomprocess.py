import random

class RandomProcess:
  def __init__(self, noisinesses_by_scale, *, zero=0, seed=None):
    self.noisinesses_by_scale = noisinesses_by_scale
    self.seed = seed if (seed is not None) else random.random()
    self.zero = zero

  def sample(self, x) -> float:
    return sum(self._sample_on_scale(x, scale) for scale in self.noisinesses_by_scale.keys())

  def _sample_on_scale(self, x, scale):
    prev_checkpoint = self.zero + scale*((x-self.zero)//scale)
    next_checkpoint = prev_checkpoint + scale

    w = (x - prev_checkpoint) / (next_checkpoint - prev_checkpoint)
    return (self._sample_on_scale_at_checkpoint(next_checkpoint, scale) * w +
            self._sample_on_scale_at_checkpoint(prev_checkpoint, scale) * (1-w))

  def _sample_on_scale_at_checkpoint(self, x, scale):
    return random.Random((self.seed, x)).normalvariate(0, self.noisinesses_by_scale[scale])
