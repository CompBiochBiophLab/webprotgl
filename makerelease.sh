#! /bin/bash

FILE_OUT=static/webglprotein.js
cat static/protgl.js | sed '/[/][/]SNIP/,/[/][/]SNAP/d' > $FILE_OUT
cat static/protein.js >> $FILE_OUT
cat static/base.js >> $FILE_OUT
cat static/jdataview.js >> $FILE_OUT
cat static/jquery_binary.js >> $FILE_OUT
cat static/webgl/boundingbox.js >> $FILE_OUT
cat static/webgl/camera.js >> $FILE_OUT
cat static/webgl/fast.js >> $FILE_OUT
cat static/webgl/mouse.js >> $FILE_OUT
cat static/webgl/shader.js >> $FILE_OUT
cat static/webgl/shaderparameter.js >> $FILE_OUT
cat static/webgl/shape.js >> $FILE_OUT
cat static/webgl/basicshapes.js >> $FILE_OUT
cat static/webgl/transform.js >> $FILE_OUT
cat static/webgl/movementmanager.js >> $FILE_OUT

cat static/index.html | sed 's/protgl.js/webglprotein.js/g' > static/protein.html
