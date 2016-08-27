var path = require('path');

// var staticRootDir = process.env.CFG_STATIC_ROOT || null;

var App = function(dir, options) {
    this.srcDir = 'static_src';
    this.destDir = 'static';

    this.dir = dir;
    this.options = options || {};
    this.appName = this.options.appName || path.basename(dir);
    this.sourceFiles = path.join('.', this.dir, this.srcDir);
};
App.prototype = Object.create(null);
App.prototype.processDestFile = function(file) {
    var srcDir = path.resolve(this.sourceFiles);

    var destDir = this.destDir;
    if (!path.isAbsolute(destDir)) {
        destDir = path.resolve('.', this.dir, destDir)
    }

    return file.base.replace(srcDir, destDir)
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

var apps = [
    new App('blog/base'),
    new App('blog/content/about')
];

module.exports = {
    apps: apps
};
