#! /bin/bash

FOLDER=/home/jrenggli/webglprotein/
cp __init__.py $FOLDER
cp database.sqlite $FOLDER

mkdir $FOLDER/database
cp -r database/*.py $FOLDER/database

mkdir $FOLDER/server
cp -r server/*.py $FOLDER/server

mkdir $FOLDER/static
cp static/protein.html $FOLDER/static
cp static/webglprotein.js $FOLDER/static

