const path = require('path');
const merge = require('webpack-merge');
const webpack = require('webpack');
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin');


function resolve(dir) {
  return path.join(__dirname, '..', dir);
}


// Export a function. Accept the base config as the only param.
module.exports = storybookBaseConfig =>
  // configType has a value of 'DEVELOPMENT' or 'PRODUCTION'
  // You can change the configuration based on that.
  // 'PRODUCTION' is used when building the static version of storybook.

  // Return the altered config
  merge(storybookBaseConfig, {
    resolve: {
      extensions: ['.js', '.vue', '.json'],
      alias: {
        vue$: 'vue/dist/vue.esm.js',
        '@': resolve('src'),
      },
    },
    plugins: [
      new webpack.HotModuleReplacementPlugin(),
      new webpack.NoEmitOnErrorsPlugin(),
      new FriendlyErrorsPlugin(),
    ],
  })
;


/*
// load the default config generator.
const devConfig = require('../build/webpack.base.conf.js');
const utils = require('../build/utils');
const merge = require('webpack-merge');
const webpack = require('webpack');
const config = require('../config');
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin');

// Export a function. Accept the base config as the only param.
module.exports = (storybookBaseConfig) => {
  console.log(devConfig);
  devConfig.entry = storybookBaseConfig.entry;
  devConfig.output = storybookBaseConfig.output;
  console.log(devConfig);

  devConfig.module.rules.push(storybookBaseConfig.module.rules[0]);

  return merge(devConfig, {
    module: {
      rules: utils.styleLoaders({ sourceMap: config.dev.cssSourceMap }),
    },
    plugins: [
      new webpack.HotModuleReplacementPlugin(),
      new webpack.NoEmitOnErrorsPlugin(),
      new FriendlyErrorsPlugin(),
    ],
  });
};
*/
