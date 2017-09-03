var MISSILE_FLIGHT_TIME_SECONDS = 3*60;
var LRR_READOUT_INTERVALS = [[180, 165], [165, 150], [150, 120],
                             [120, 60], [60, 30], [30, 0]];

var alive = true;
var enemies = {};

function setCountdown(enemyName, timeRemaining) {
  if (timeRemaining === null) {
    return;
  } else {
    markButtonLaunched(enemyName);
    var e = enemies[enemyName];
    if (e.countdown === null) {
      e.countdown = $('<span class="countdown" />');
      e.container.find('.launch-button').html(e.countdown);
    }
    if (timeRemaining === 0) {
      markEnemyDead(enemyName);
    } else {
      e.countdown.text(timeRemaining);
    }
  }
}

function markButtonLaunched(enemyName) {
  var $b = enemies[enemyName].container.find('.launch-button');
  $b.addClass('launched');
  $b.prop('disabled', true);
}

// Standard Normal variate using Box-Muller transform.
// Stolen from https://stackoverflow.com/a/36481059
function normalvariate() {
    var u = 1 - Math.random(); // Subtraction to flip [0, 1) to (0, 1].
    var v = 1 - Math.random();
    return Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
}

function stopChart(enemyName) {
  enemies[enemyName].chart.stop();
  setTimeout(function() {
    var c = enemies[enemyName].container.find('.ews-canvas')[0];
    var cx = c.getContext('2d');
    cx.fillStyle = 'black'; cx.beginPath(); cx.rect(0, 0, c.width, c.height); cx.fill();
    enemies[enemyName].container.find('.lrr-readouts').css({'color': 'black'});
  }, 700);
}

function markEnemyDead(enemyName) {
  markButtonLaunched(enemyName);
  var $b = enemies[enemyName].container.find('.launch-button');
  $b.text(String.fromCharCode(9760));
  $b.addClass('dead');
  setTimeout(function(){stopChart(enemyName);}, (MISSILE_FLIGHT_TIME_SECONDS+10)*1000);
}

var integerTime = 0;
function integerTime2Date(t) {
  var result = new Date()
  result.setSeconds(result.getSeconds() - (integerTime-t));
  return result;
}

function noteUpdates(data) {
  integerTime = data.discrete_time;
  if (!data.alive) {
    var dyingNow = alive;
    alive = false;
    if (dyingNow) {
      die();
    }
  }
  Object.entries(data.enemy_info).forEach(function([enemyName, info]) {
    updateEnemyInfo(enemyName, info)
  });
}

function updateEnemyInfo(enemyName, info) {
  var e = enemies[enemyName];
  if (!info.alive) {
    markEnemyDead(enemyName);
  }
  noteEWSReadings(enemyName, info.readings);
  setCountdown(enemyName, info.time_to_impact);
}

var lastAlarmTime = 0;
var alarm = new Audio('/static/klaxon.mp3');
var soundAlarm = alarm.play;
var soundExplosion = function(v, t) {
  $('#ytHider').append($('<iframe width="560" height="315" src="https://www.youtube.com/embed/vxNnUU3eRD0?start=10&autoplay=1" frameborder="0" allowfullscreen></iframe>'));
}

function die() {
  console.log('dying now');
  var $content = $('#content');
  soundExplosion();
  Object.keys(enemies).forEach(markButtonLaunched);
  setTimeout(function() {
    console.log('stopping charts');
    Object.keys(enemies).forEach(stopChart);
    setTimeout(function() {
      console.log('inner callback');
      $('#content').empty();
      $('body').css({'transition': 'background-color 20000ms linear'})
      $('body').css({'background-color': '#333'});
    }, 2000);
  }, 5000);
}

function noteEWSReadings(enemyName, readings) {
  var e = enemies[enemyName];

  Object.entries(readings).forEach(function([t, reading]) {
    e.hypothesisSet.updateRelativeRepresentativenesses(t, reading);
    e.timeSeries.append(integerTime2Date(t).getTime(), 100 * ((reading ? 1 : -1) + normalvariate()/10));
  });

  LRR_READOUT_INTERVALS.forEach(function(interval) {
    var lrr = Math.round(e.hypothesisSet.getMaxLogRelativeRepresentativenessInRange(integerTime-interval[0], integerTime-interval[1]));
    e.container.find(`.lrr-readouts td[data-for-interval="${interval}"]`).text(Number.isFinite(lrr) ? lrr.toString() : "--");
    e.container.find(`.lrr-readouts tr[data-for-interval="${interval}"]`).css({'background-color': (lrr > 4 ? '#a00' : 'initial')});
    if (interval[0] == 150 && lrr > 50 && integerTime - lastAlarmTime > 6) {
      lastAlarmTime = integerTime;
      alarm.play();
    }
  });

}

function request_updates_until_dead() {
  $.get('./update', {'since': integerTime},
    function(data) {
      noteUpdates(JSON.parse(data));
      if (alive) {
        setTimeout(function(){request_updates_until_dead()}, 100);
      }
    });
}

ENEMY_CONTAINER_TEMPLATE = `
  <div class="enemy-container" id="{{enemyName}}">
    <h2 class="enemy-name">{{enemyName}}</h2>
    <button class="launch-button">&#9762;</button>
    <canvas class="ews-canvas" width="500" height="200" />
    <table class="lrr-readouts">
      <tr>
        <th> Representativeness </th>
        <th> of launch in last ____ seconds </th>
      </tr>
      ${LRR_READOUT_INTERVALS.sort(function(a,b){return a-b}).map(
        function(interval) {
          return `
            <tr data-for-interval="${interval}">
              <td data-for-interval="${interval}"> 0 </td>
              <td> ${interval.join("-")} </td>
            </tr>`
        }
      ).join('')}
    </table>
  </div>
`

function add_enemy(enemyName) {
  var e = {'hypothesisSet': new HypothesisSet(MISSILE_FLIGHT_TIME_SECONDS), 'countdown': null};

  e.container = $(Mustache.render(ENEMY_CONTAINER_TEMPLATE, {'enemyName': enemyName}));
  $('#content').append(e.container);

  e.container.find('.launch-button').on('click', function(){
    markButtonLaunched(enemyName);
    $.get('launch/'+enemyName);
  });

  e.chart = new SmoothieChart({
    grid: {
      millisPerLine: 10000,
      verticalSections: 0
    },
    horizontalLines: [
      {color:'#ffffff',lineWidth:1,value:0},
      {color:'#880000',lineWidth:2,value:100},
      {color:'#008800',lineWidth:2,value:-100}
    ],
    millisPerPixel: 50,
    maxValue: 150,
    minValue: -180,
    timestampFormatter: SmoothieChart.timeFormatter,
    labels: {disabled: true}
  });
  e.chart.streamTo(e.container.find('.ews-canvas')[0], 1000/*delay*/);

  e.timeSeries = new TimeSeries();

  e.chart.addTimeSeries(e.timeSeries, {lineWidth:2,strokeStyle:'#ffff00'});

  enemies[enemyName] = e;
}

$(function() {

  $.get('enemies', function(data) {
    JSON.parse(data).forEach(function(enemyName) {
      add_enemy(enemyName);
    })
    request_updates_until_dead();
  });

});
