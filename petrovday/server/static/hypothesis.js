var Hypothesis = (function() {


  ALPHA = 0.1;
  MISSILE_FRACTIONAL_READING_P = function(dt) {return dt/MISSILE_FLIGHT_TIME_SECONDS;};

  function Hypothesis(launchTime) {
    this.launchTime = launchTime;
    this.logRelativeRepresentativeness = 0;
  }

  Hypothesis.prototype.updateRelativeRepresentativeness = function(t, x) {
    var self = this;
    if (t < self.launchTime) {
      return;
    } else {
      var p = ALPHA + (1-ALPHA)*MISSILE_FRACTIONAL_READING_P(t-self.launchTime);
      if (p > 1) {
        self.logRelativeRepresentativeness = null;
      } else {
        self.logRelativeRepresentativeness += ((x==1) ? (Math.log(p)-Math.log(ALPHA)) : (Math.log(1-p)-Math.log(1-ALPHA)));
      }
    }
  };

  return Hypothesis;
})()

var HypothesisSet = (function() {

  function range(start, stop) {
    var result = new Array(stop-start);
    for (var i=start; i<stop; i++) {
      result[i-start] = i;
    }
    return result;
  }

  function HypothesisSet() {
    this.hypotheses = {};
  }

  HypothesisSet.prototype.updateRelativeRepresentativenesses = function(t, x) {
    var self = this;
    self.hypotheses[t] = new Hypothesis(t);
    Object.getOwnPropertyNames(self.hypotheses).forEach(function(t_h) {
      self.hypotheses[t_h].updateRelativeRepresentativeness(t, x);
      if (self.hypotheses[t_h].logRelativeRepresentativeness === null) {
        delete self.hypotheses[t_h];
      }
    });
  };

  HypothesisSet.prototype.getLogRepresentativeness = function(t) {
    return self.hypotheses.hasOwnProperty(i) ? self.hypotheses[i].logRelativeRepresentativeness : null;
  }

  HypothesisSet.prototype.getMaxLogRelativeRepresentativenessInRange = function(start, stop) {
    var self = this;
    var result = undefined;
    return Math.max.apply(null,
      range(start, stop)
        .map(function(i){return self.hypotheses.hasOwnProperty(i) ? self.hypotheses[i].logRelativeRepresentativeness : null;})
        .filter(function(x){return x !== null;})
    );
  };

  return HypothesisSet;
})();
