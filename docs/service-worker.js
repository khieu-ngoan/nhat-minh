/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/3.6.3/workbox-sw.js");

importScripts(
<<<<<<< HEAD
<<<<<<< HEAD
  "//quanict.github.io/nhat-minh/precache-manifest.91791a04bc779b41ff2c8c850c6c66e7.js"
=======
  "/precache-manifest.440f1bfb655c892337267220a4340c37.js"
>>>>>>> bb63fed (update)
=======
  "//quanict.github.io/nhat-minh/precache-manifest.dc2a6ede9f7f9125cab694a772095fcf.js"
>>>>>>> 5b58c0d (update)
);

workbox.clientsClaim();

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.suppressWarnings();
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});

<<<<<<< HEAD
<<<<<<< HEAD
workbox.routing.registerNavigationRoute("//quanict.github.io/nhat-minh/index.html", {
=======
workbox.routing.registerNavigationRoute("/index.html", {
>>>>>>> bb63fed (update)
=======
workbox.routing.registerNavigationRoute("//quanict.github.io/nhat-minh/index.html", {
>>>>>>> 5b58c0d (update)
  
  blacklist: [/^\/_/,/\/[^/]+\.[^/]+$/],
});
