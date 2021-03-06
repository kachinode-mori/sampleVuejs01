'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_ENDPOINT: '"http://127.0.0.1:8000/api/"'
  // API_ENDPOINT: '"http://52.77.229.232/api/"'
})
