var path = require("path");
var webpack = require("webpack");

module.exports = {
  entry: {
    vendor: [
      'vue/dist/vue.esm.js',
      'lodash',
      'axios',
      'vue-router',
      'iview',
      'moment'
    ]
  },
  output: {
    path: path.join(__dirname, './comment/js'), // 打包后文件输出的位置
    filename: '[name].dll.js',
    library: '[name]_library'
  },
  plugins: [
    new webpack.DllPlugin({
      path: path.join(__dirname, '.', '[name]-manifest.json'),
      name: '[name]_library'
    }),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false
      }
    })
  ]
};
