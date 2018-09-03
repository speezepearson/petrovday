import * as React from 'react';
import smoothie from 'smoothie';

import './early-warning-system.css';

const klaxonWindowSize = 50;
const klaxonFractionUp = .4;
const klaxonFractionDown = .3;

class EarlyWarningSystem extends React.Component {
  constructor(props) {
    super(props);
    this.chart = new smoothie.SmoothieChart({
      grid: {
        millisPerLine: 10000,
        verticalSections: 0
      },
      horizontalLines: [
        {color:'#ffffff',lineWidth:1,value:0},
        {color:'#880000',lineWidth:2,value:100},
        {color:'#008800',lineWidth:2,value:-100}
      ],
      millisPerPixel: 100,
      maxValue: 150,
      minValue: -180,
      timestampFormatter: smoothie.SmoothieChart.timeFormatter,
      labels: {disabled: true}
    });
    this.timeSeries = new smoothie.TimeSeries();
    this.chart.addTimeSeries(this.timeSeries, {lineWidth: 2, strokeStyle: '#ffff00'});
    this.canvasElement = null;
  }
  render() {
    return <canvas ref={(element) => { this.canvasElement = element }} className="ews-canvas" width="500" height="200" />
  }

  componentDidMount() {
    this.chart.streamTo(this.canvasElement, 1000/*delay*/);
  }
  componentWillUnmount() {
    this.chart.stop();
    setTimeout(this.props.stopKlaxon, 1000);
  }

  addReading(timeAgo, reading) {
    var t = new Date()
    t.setSeconds(t.getSeconds() - timeAgo);
    this.timeSeries.append(t, 100 * ((reading ? 1 : -1) + EarlyWarningSystem.normalvariate()/10));

    var recentReadings = this.timeSeries.data
                            .map(([t,x]) => x);
    var nRecentPositives = recentReadings.filter((x) => (x>0)).length;
    console.log(`${nRecentPositives}/${recentReadings.length} recent positives, thresholds ${Math.floor(klaxonFractionDown*recentReadings.length)}-${Math.ceil(klaxonFractionUp*recentReadings.length)}`);
    if (nRecentPositives > klaxonFractionUp*recentReadings.length) {
      this.props.startKlaxon();
    } else if (nRecentPositives < klaxonFractionDown*recentReadings.length) {
      this.props.stopKlaxon();
    }
  }

  // Standard Normal variate using Box-Muller transform.
  // Stolen from https://stackoverflow.com/a/36481059
  static normalvariate() {
      var u = 1 - Math.random(); // Subtraction to flip [0, 1) to (0, 1].
      var v = 1 - Math.random();
      return Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
  }

}

export default EarlyWarningSystem;
