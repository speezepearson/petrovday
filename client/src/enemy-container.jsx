import * as React from 'react';

import LaunchButton from './launch-button.jsx';
import EarlyWarningSystem from './early-warning-system.jsx';
import { missileFlightTime } from './globals.jsx';
import './enemy-container.css'

class EnemyContainer extends React.Component {
  render() {
    var buttonPhase = (
      (this.props.timeSinceDeath !== null && this.props.timeSinceDeath <= missileFlightTime ) ? (-this.props.timeSinceDeath) :
      (!this.props.alive) ? 'obsolete' :
      (this.props.timeToImpact === null) ? 'ready' :
      this.props.timeToImpact
    );
    return <div className="enemy-container">
      <h2 className="enemy-name">{this.props.enemy}</h2>
      <LaunchButton phase={buttonPhase} enemy={this.props.enemy} />
      <EarlyWarningSystem enemy={this.props.enemy}
                          startKlaxon={this.props.startKlaxon}
                          stopKlaxon={this.props.stopKlaxon}
                          ref={(ews) => {this.ews = ews}} />
    </div>;
  }

  noteUpdate(now, info) {
    Object.entries(info.readings).map(([t,x]) => this.ews.addReading(now-t, x));
  }

}

export default EnemyContainer;
