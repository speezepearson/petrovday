import * as React from 'react';
import $ from 'jquery';

import Countdown from './countdown.jsx';
import { missileFlightTime } from './globals.jsx';

import './launch-button.css';


class LaunchButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {clicked: false}
  }

  render() {
    if (this.props.phase === 'ready') {
      if (this.state.clicked)
        return <button className='launch-button launch-button--ticking'
                       disabled={true}>
                 <Countdown time={missileFlightTime}/>
               </button>;
      else
        return <button className='launch-button launch-button--ready'
                       onClick={(e) => this.launch()}>
                 &#9762;
               </button>;
    } else if (this.props.phase === 'obsolete') {
      return <button className={`launch-button launch-button--obsolete`}
                     disabled={true}>
               &#9760;
             </button>;
    } else {
      return <button className="launch-button launch-button--ticking"
                  disabled={true}>
            <Countdown time={this.props.phase}/>
          </button>;
    }
  }

  launch() {
    $.get('launch/'+this.props.enemy);
    this.setState({clicked: true});
  }

}

export default LaunchButton;
