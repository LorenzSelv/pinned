let mix = require('laravel-mix');

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for your application, as well as bundling up your JS files.
 |
 */

mix.js('core/assets/js/app.js', 'core/static/core')
   .sass('core/assets/sass/app.scss', 'core/static/core');
mix.setPublicPath(__dirname);
mix.copy('node_modules/font-awesome/fonts', 'core/static/core/fonts/vendor/font-awesome');