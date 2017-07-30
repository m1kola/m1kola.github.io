var gulp = require('gulp');
var rename = require('gulp-rename');
var gutil = require('gulp-util');
var path = require('path');
var es = require('event-stream');
var config = require('../config');


var simpleCopyTask = function(glob) {
    return function () {
        es.merge(config.apps.map(
            function(app) {
                var sources = path.join(app.sourceFiles, app.appName, glob);

                return gulp.src(sources)
                    .pipe(gulp.dest(function(file) {
                        return app.processDestFile(file);
                    }))
                    .on('error', gutil.log);


            }
        ));
    }
};

module.exports = simpleCopyTask;
