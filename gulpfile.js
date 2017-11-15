var gulp = require('gulp');
    connect = require('gulp-connect');


gulp.task('javascript', function () {
  return gulp.src('src/*.js')
    .pipe(gulp.dest('public/js'))
    .pipe(connect.reload());
})

gulp.task('watch', function () {
  gulp.watch(['src/*.js'], ['javascript'])
})

gulp.task('server', function () {
  connect.server({
      root: 'public',
      livereload: true
  })
})

gulp.task('default', ['javascript', 'watch', 'server'])
