# Three.js

Vendored from the npm package `three@0.186.0`. MIT license is retained at
`three/LICENSE.txt`. The module build is unchanged; one indentation space was removed from the core
build to pass whitespace checks. In four addon modules,
bare `from 'three'` imports are rewritten to `/vendor/three/three.module.js` so
the local viewer requires no CDN or inline import map. All imports use the same
package version. Only OrbitControls, GLTFLoader and its two utility dependencies
are included; no package install scripts were executed.
