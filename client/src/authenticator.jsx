import * as React from 'react';
import $ from 'jquery';

import Spinner from 'spin';

import './authenticator.css';

class Authenticator extends React.Component {
  constructor(props) {
    super(props);
    this.state = {phase: 'idle', password: '', failed: false};
    this.passwordField = <input type="password" placeholder="Password" />;
  }

  handleChange(e) {
    this.setState({password: e.target.value});
  }

  render() {
    var buttonHolderContents = (
      (this.state.phase === 'idle') ? <button onClick={() => this.authenticate()}>Log In</button> :
      (this.state.phase === 'checking') ? <span className='authenticator__spinner' ref={(el) => new Spinner({color: '#fff', length: 5, width: 2, radius: 5}).spin(el)}>&nbsp;</span> :
      '\u2714'
    )
    return <div className="authenticator">
      <input type="password" placeholder="Password"
             className={'authenticator__password-field' + (this.state.failed ? ' failed' : '')}
             onKeyPress={(e) => {if (e.key==='Enter') this.authenticate()}}
             onChange={(e) => this.handleChange(e)}
             ref={(e) => {if (e !== null) e.focus()}} />
      &nbsp;
      <div className='authenticator__button-holder'>
        {buttonHolderContents}
      </div>
    </div>;
  }

  authenticate(password) {
    this.setState({'phase': 'checking'});
    $.get('authenticate', {'password': this.state.password}, (data) => {
      this.setState({'phase': 'complete'});
      this.props.onSuccessfulAuthentication(JSON.parse(data));
    }).fail(() => {
      this.setState({'phase': 'idle', failed: true});
    });
  }
}

export default Authenticator;
