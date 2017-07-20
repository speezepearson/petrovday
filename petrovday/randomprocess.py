import random
import functools
from typing import TypeVar, Iterable, Tuple, Callable

W = TypeVar('W')
A = TypeVar('A')
R = TypeVar('R')

def weighted_sum(weights_and_functions: Iterable[Tuple[W, Callable[..., R]]]) -> Callable[..., R]:
  (weights, functions) = zip(*weights_and_functions)
  @functools.wraps(functions[0])
  def result(*args, **kwargs):
    return sum(w*f(*args, **kwargs) for (w, f) in zip(weights, functions))
  return result

def regularly_interpolate(sample_at_checkpoint: Callable[[A], R], origin=0, scale=1) -> Callable[[A], R]:
  @functools.wraps(sample_at_checkpoint)
  def result(x: A) -> R:
    prev_checkpoint = origin + scale*((x-origin)//scale)
    next_checkpoint = prev_checkpoint + scale

    w = (x - prev_checkpoint) / (next_checkpoint - prev_checkpoint)
    return (sample_at_checkpoint(next_checkpoint) * w +
            sample_at_checkpoint(prev_checkpoint) * (1-w))
  return result

def pseudorandom_static(f: Callable[[random.Random], R], seed) -> Callable[..., R]:

  def result(*args, **kwargs) -> R:
    return f(random.Random((seed, args, tuple(sorted(kwargs.items())))))

  return result

def white_noise(scales, weights=None, seed=None, **kwargs):
  if weights is None:
    weights = [scale**.5 for scale in scales]

  return weighted_sum([
    (weight, regularly_interpolate(
               sample_at_checkpoint=pseudorandom_static(lambda r: r.normalvariate(0, 1), seed=seed),
               scale=scale,
               **kwargs))
    for (weight, scale) in zip(weights, scales)
  ])
