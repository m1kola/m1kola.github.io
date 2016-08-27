var gulp = require('gulp');
var sass = require('gulp-sass');
var config = require('../config');
var autoprefixer = require('gulp-autoprefixer');
var simpleCopyTask = require('../lib/simplyCopy');
var gutil = require('gulp-util');
var es = require('event-stream');

gulp.task('styles', ['styles:sass', 'styles:css']);

gulp.task('styles:css', simpleCopyTask('css/**/*'));

gulp.task('styles:sass', function () {
    return es.merge(config.apps.map(
        function(app) {
            return gulp.src(app.scssSourcePaths())
                .pipe(sass({
                    errLogToConsole: true,
                    includePaths: app.scssIncludePaths(),
                    outputStyle: 'expanded'
                }))
                .pipe(autoprefixer({
                    browsers: ['last 3 versions', 'not ie <= 8'],
                    cascade: false
                }))
                .pipe(gulp.dest(function(file) {
                    // e.g. pages/scss/core.scss -> pages/css/core.css
                    // Changing the suffix is done by Sass automatically
                    return app.processDestFile(file)
                        .replace('/scss/', '/css/');
                }))
                .on('error', gutil.log);
        }
    ));
});
