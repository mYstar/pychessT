'use strict'

const path = require('path')
const autoprefixer = require('autoprefixer')

module.exports = {
  entry: {
    index: './src/index.js',
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'chesst/static'),
    publicPath: '',
    clean: true,
  },
  mode: 'development',
  devtool: 'inline-source-map',
  optimization: {
    runtimeChunk: 'single',
  },
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [
            'style-loader',
            'css-loader',
            {
                loader: 'postcss-loader',
                options: {
                    postcssOptions: {
                        plugins: [
                            autoprefixer
                        ]
                    }
                }
            },
            'sass-loader',
        ],
      },
      {
        test: /\.(svg|png)$/i,
        type: 'asset/resource',
      },
      {
        test: /\.(ttf|woff|woff2)$/i,
        type: 'asset/resource',
      },
    ],
  },
};