#! /bin/bash

FILE_OUT=static/webglprotein.raw
FILE_FINAL=static/webglprotein.js

# JQuery comes first
cat static/jquery_binary.js > $FILE_OUT
cat static/base.js >> $FILE_OUT

# WebGL stuff
cat static/webgl/boundingbox.js >> $FILE_OUT
cat static/webgl/camera.js >> $FILE_OUT
cat static/webgl/fast.js >> $FILE_OUT
cat static/webgl/shader.js >> $FILE_OUT
cat static/webgl/shaderparameter.js >> $FILE_OUT
cat static/webgl/shape.js >> $FILE_OUT
cat static/webgl/basicshapes.js >> $FILE_OUT
cat static/webgl/transform.js >> $FILE_OUT
cat static/webgl/movementmanager.js >> $FILE_OUT

# Specific data
cat static/jdataview.js >> $FILE_OUT
cat static/protein.js >> $FILE_OUT
cat static/protgl.js | sed '/[/][/]SNIP/,/[/][/]SNAP/d' >> $FILE_OUT

rm -f $FILE_FINAL

export PATH="$PATH:/home/jrenggli/prog/3rdparty/UglifyJS/bin"

uglifyjs -o $FILE_FINAL $FILE_OUT

#cat static/index.html | sed 's/protgl.js/webglprotein.js/g' > static/protein.html
