'use strict';

var path = require('path'),
    del = require('del'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    sass = require('gulp-sass'),
    concat = require('gulp-concat'),
    minifyCss = require('gulp-minify-css')
    ;

var config = {
    common: {
        staticfiles_dirs: './gulp',
        css_dirname: 'css',
        img_dirname: 'img'
    },
    sass: {
        src: './**/static/**/scss',
        entry_point: 'styles.scss'
    },
    css: {
        src: './**/static/**/css/*.css'
    },
    css_concat: {
        src: './gulp/css',
        concat_file: 'styles.min.css',
        concat_opts: {}
    }
};

var utils = function() {};
utils.log = function() {};
utils.log.error = function(error) {
    gutil.log(gutil.colors.red(error.message));
};


gulp.task('clean', function() {
    gutil.log('Cleaning whole build directory...');

    return del([
        path.join(config.common.staticfiles_dirs, '*')
    ]);
});


gulp.task('css:scss', ['clean'], function() {
    return gulp.src(path.join(config.sass.src, config.sass.entry_point))
        .pipe(
            sass({
                style: 'compressed'
            })
                .on('error', utils.log.error)
        )
        .pipe(gulp.dest(path.join(config.common.staticfiles_dirs, config.common.css_dirname)));
});


gulp.task('css:concat', ['css:scss'], function() {
    return gulp.src(path.join(config.common.staticfiles_dirs, config.common.css_dirname, '**', '*.css'))
        .pipe(concat(config.css_concat.concat_file, config.css_concat.concat_opts))
        .pipe(minifyCss())
        .pipe(gulp.dest(path.join(config.common.staticfiles_dirs, config.common.css_dirname)));
});


gulp.task('css', ['css:concat'], function() {
    gutil.log('Cleangin css directory...');

    return del([
        path.join(config.common.staticfiles_dirs, config.common.css_dirname, '**', '*'),
        '!' + path.join(config.common.staticfiles_dirs, config.common.css_dirname, config.css_concat.concat_file)
    ]);
});


gulp.task('watch', function() {
    gulp.watch(path.join(config.sass.src, config.sass.entry_point), ['css']);
});


gulp.task('default', ['css']);
