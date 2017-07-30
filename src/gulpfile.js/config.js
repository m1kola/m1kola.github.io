var path = require('path');

var App = function(dir, options) {
    this.dir = dir;
    this.options = options || {};

    this.srcDir = 'static_src';
    this.destDir = this.options.destDir || path.resolve('.', 'static_compiled');
    if (!path.isAbsolute(this.destDir)) {
        this.destDir = path.resolve('.', this.dir, this.destDir);
    }

    this.appName = this.options.appName || path.basename(dir);
    this.sourceFiles = path.join('.', this.dir, this.srcDir);
};
App.prototype = Object.create(null);
App.prototype.processDestFile = function(file) {
    var srcDir = path.resolve(this.sourceFiles);

    return file.base.replace(srcDir, this.destDir);
};
App.prototype.scssIncludePaths = function() {
    return [this.sourceFiles];
};
App.prototype.scssSourcePaths = function() {
    // Assume that any scss we care about is always within the expected 
    // "appname/static_url/appname/scss/" folder.
    // NB: this requires the user to adhere to sass's underscore prefixing
    // to tell the compiler what files are includes.
    return path.join(this.sourceFiles, this.appName, '/scss/**/*.scss');
};

var app_options = {};
if (process.env.CFG_STATIC_ROOT) {
    app_options = {
        destDir: process.env.CFG_STATIC_ROOT
    };
}

var apps = [
    new App('blog/base', app_options),
    new App('blog/content/about', app_options)
];

module.exports = {
    apps: apps
};
