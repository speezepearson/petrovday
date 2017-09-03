ALPHA = 0.1;

class Hypothesis {

  constructor(launchTime, missileFlightTime) {
    this.launchTime = launchTime;
    this.missileFlightTime = missileFlightTime;
    this.logRelativeRepresentativeness = 0;
  }

  updateRelativeRepresentativeness(t, x) {
    var self = this;
    if (t < self.launchTime) {
      return;
    } else {
      var p = ALPHA + (1-ALPHA)*(t-self.launchTime)/self.missileFlightTime;
      if (p > 1) {
        self.logRelativeRepresentativeness = null;
      } else {
        self.logRelativeRepresentativeness += ((x==1) ? (Math.log(p)-Math.log(ALPHA)) : (Math.log(1-p)-Math.log(1-ALPHA)));
      }
    }
  };
}

function range(start, stop) {
  var result = new Array(stop-start);
  for (var i=start; i<stop; i++) {
    result[i-start] = i;
  }
  return result;
}

class HypothesisSet {

  constructor(missileFlightTime) {
    this.missileFlightTime = missileFlightTime;
    this.hypotheses = {};
  }

  updateRelativeRepresentativenesses(t, x) {
    var self = this;
    self.hypotheses[t] = new Hypothesis(t, self.missileFlightTime);
    Object.getOwnPropertyNames(self.hypotheses).forEach(function(t_h) {
      self.hypotheses[t_h].updateRelativeRepresentativeness(t, x);
      if (self.hypotheses[t_h].logRelativeRepresentativeness === null) {
        delete self.hypotheses[t_h];
      }
    });
  };

  getLogRepresentativeness(t) {
    return self.hypotheses.hasOwnProperty(i) ? self.hypotheses[i].logRelativeRepresentativeness : null;
  }

  getMaxLogRelativeRepresentativenessInRange(start, stop) {
    var self = this;
    var result = undefined;
    return Math.max.apply(null,
      range(start, stop)
        .map(function(i){return self.hypotheses.hasOwnProperty(i) ? self.hypotheses[i].logRelativeRepresentativeness : null;})
        .filter(function(x){return x !== null;})
    );
  };
}
