const path = require('path');

module.exports = {
    devtool: 'source-map',
    entry: {
      'main': './client/src/main.js',
      'admin-main': './client/src/adminMain.js'
    },
    externals: {
        react: 'React',
        'react-dom': 'ReactDOM'
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'app/static/scripts'),
        library: 'VirtualTreasureChest',
        libraryTarget: 'var'
    },
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader"
          }
        }
      ]
    }
  };