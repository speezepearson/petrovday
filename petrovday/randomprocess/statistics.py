import itertools

def quantile(xs, q):
  xs = list(sorted(xs))
  i = q*len(xs)
  if i == int(i) or i > (len(xs)-1):
    return xs[int(i)]
  return (
    xs[int(i)] * abs(i - int(i)) +
    xs[int(i+1)] * abs(i - int(i+1))
  )

def median(xs):
  return quantile(xs, .5)

def intervals_exceeding_threshold(f, threshold, sample_points):
  for (is_above_threshold, chunk) in itertools.groupby(sample_points, (lambda x: f(x)>threshold)):
    chunk = list(chunk)
    if is_above_threshold:
      yield (chunk[0], chunk[-1])

assert list(intervals_exceeding_threshold((lambda x: x%5), 3, [.9*n for n in range(20)])) == [(3.6, 4.5), (8.1, 9.9), (13.5, 14.4)], str(list(intervals_exceeding_threshold((lambda x: x%5), 3, [.9*n for n in range(20)])))

if __name__ == '__main__':
  import datetime as dt
  import pprint
  from petrovday.game import make_ews_noise

  N_STUDY_HOURS = 1
  f = make_ews_noise(seed=0)
  intervals = list(intervals_exceeding_threshold(f, 1, (dt.datetime(2017,9,26,0,0,0) + n*dt.timedelta(seconds=1) for n in range(3600*N_STUDY_HOURS))))
  durations = [(high-low)/dt.timedelta(seconds=1) for low,high in intervals]
  print(f'In {N_STUDY_HOURS} hours:')
  print(f'- about {len(intervals)} max-outs')
  print(f'- half of which are shorter than {round(quantile(durations, .51))} seconds')
  print(f'- and 90% of which are shorter than {round(quantile(durations, .91))} seconds')
