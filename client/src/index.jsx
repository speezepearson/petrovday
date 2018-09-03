import * as React from 'react';
import * as ReactDOM from 'react-dom';
import $ from 'jquery';

import Game from './game.jsx';

import './index.css';

$(() =>
ReactDOM.render(
  <Game ref={(g) => {window.game = g}} />,
  document.getElementById('foo')
));
