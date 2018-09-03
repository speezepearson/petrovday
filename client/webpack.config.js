var path = require('path');

var basicConfig = {
  "module": {
    "rules": [
      {
        "test": /\.jsx?$/,
        "exclude": /node_modules/,
        "use": {
          "loader": 'babel-loader'
        }
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  }
}

var serverConfig = Object.assign({}, basicConfig, {
  target: 'node',
  entry: './src/server.js',
  output: {
    path: path.resolve(__dirname),
    filename: 'index.js'
  }
});

var clientConfig = Object.assign({}, basicConfig, {
  target: 'web',
  entry: './src/index.jsx',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'app.js'
  }
});

module.exports = [ serverConfig, clientConfig ];
