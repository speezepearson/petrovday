import * as React from 'react';
import $ from 'jquery';

import Authenticator from './authenticator.jsx';
import EnemyContainer from './enemy-container.jsx';
import Klaxon from './klaxon.js';

import './game.css';

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {phase: 'authenticating', enemyInfos: null, discreteTime: 0};
    this.enemyContainers = {};
    this.klaxon = new Klaxon();
    this.klaxonFlags = new Set();
  }

  render() {
    var contents;
    switch (this.state.phase) {
      case 'authenticating':
        contents = <div>
            <Authenticator onSuccessfulAuthentication={this.updateUntilDead.bind(this)}/>
            <div style={{"textAlign": "center"}}>
              Is this your first shift at the Nuclear Monitoring and Control Station? Read the <a href="/static/tutorial/index.html">NMC Instructional Supplement</a>.
            </div>
          </div>;
        break;
      case 'monitoring':
        contents = Object.entries(this.state.enemyInfos).sort().map(([e, info]) =>
          <EnemyContainer key={e} enemy={e}
                          alive={info.alive}
                          timeToImpact={info.timeToImpact}
                          timeSinceDeath={info.timeOfDeath===null ? null : (this.state.discreteTime - info.timeOfDeath)}
                          startKlaxon={() => this.startKlaxon(e)}
                          stopKlaxon={() => this.stopKlaxon(e)}
                          ref={(ec) => {this.enemyContainers[e] = ec}} />);
        break;
      case 'dead':
        contents = '';
        break;
      default:
        alert('unknown phase: '+this.state.phase);
        contents = ''
    }
    return <div id='content'>{contents}</div>;
  }

  noteUpdate(discreteTime, alive, enemyInfos) {
    this.setState({
      discreteTime: discreteTime,
      phase: (alive ? 'monitoring' : 'dead'),
      enemyInfos: enemyInfos
    });
    Object.entries(this.enemyContainers).map(([e, c]) => c.noteUpdate(this.state.discreteTime, enemyInfos[e]));
  }

  updateUntilDead(initialUpdate=undefined) {
    var self = this;
    if (initialUpdate !== undefined) {
      self.noteUpdate(initialUpdate.discreteTime, initialUpdate.alive, initialUpdate.enemyInfos);
    }
    $.get('./update', {'since': this.state.discreteTime}, (data) => {
      data = JSON.parse(data);
      self.noteUpdate(data.discreteTime, data.alive, data.enemyInfos);
      if (self.state.phase !== 'dead') {
        setTimeout(()=>self.updateUntilDead(), 100);
      }
    });
  }

  startKlaxon(e) {
    this.klaxonFlags.add(e);
    this.klaxon.start();
  }
  stopKlaxon(e) {
    this.klaxonFlags.delete(e);
    if (this.klaxonFlags.size === 0) {
      this.klaxon.stop();
    }
  }
}



export default Game;
