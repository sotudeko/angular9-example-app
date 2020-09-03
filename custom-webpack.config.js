const CopyModulesPlugin = require("copy-modules-webpack-plugin");

module.exports = {
  plugins: [
    new CopyModulesPlugin({
      destination: 'webpack-modules',
      includePackageJsons: true
    })
  ]
}
