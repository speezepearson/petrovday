import * as React from 'react';

import './countdown.css';

class Countdown extends React.Component {
  get formattedTime() {
    var t = Math.abs(this.props.time);
    var prefix = (this.props.time < 0) ? '-' : ''
    var minutes = Math.floor(t/60), seconds = Math.floor(t%60);
    if (seconds<10) seconds = '0'+seconds;
    return `${prefix}${minutes}:${seconds}`;
  }

  render() {
    return <span className={`countdown countdown--${this.props.time >= 0 ? 'positive' : 'negative'}`}>{this.formattedTime}</span>;
  }
}

export default Countdown;
