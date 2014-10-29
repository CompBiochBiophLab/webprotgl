#! /usr/bin/python3

from os import fchmod, makedirs, path

import json
import os
import pickle
import re
import shutil
import subprocess
import sys

try:
  import argparse
  parser = argparse.ArgumentParser(description="Prepare for test/prod")
  parser.add_argument("config", metavar="C", choices=["testing", "preprod", "production"], default="testing", help="Target configuration")

  args = parser.parse_args()
  root = args.config
except Exception as e:
  root = sys.argv[1] #"production"

print("Compiling for " + root)
database = "webglprotein.db"

if not path.exists(root):
  makedirs(root)

print("Updating dictionary")
dic_path = os.path.join(root, "dict.pickle")
rval = subprocess.call(["python3", "scripts/csv_to_dic.py", dic_path, root], cwd=".")
print(rval)

with open(dic_path, "rb") as fil:
  vars = pickle.load(fil)
  fil.close()

# Folders / Files to copy
paths = ["__init__.py", "runserver.py", \
  "database", "server", "static", "templates"]
for source in paths:
  try:
    (s, d) = source
    source = s
    dest = path.join(root, d)
  except Exception as e:
    dest = path.join(root, source)
  if path.isfile(source):
    print("Copying file " + source + " to " + dest)
#    if source == "templates":
#      # Pre-format files
#
    shutil.copy(source, dest)
  else:
    print("Copying folder " + source)
    if path.exists(dest):
      shutil.rmtree(dest)
    shutil.copytree(source, dest)

# Update static files
print("Updating javascript")
js_in = ["jquery_binary.js", "base.js", \
  "webgl/boundingbox.js", "webgl/camera.js", "webgl/fast.js", \
  "webgl/shader.js", "webgl/shaderparameter.js", "webgl/shape.js", \
  "webgl/basicshapes.js", "webgl/transform.js", "webgl/movementmanager.js", \
  "jdataview.js", "protein.js"]
js_last = "protgl.js"
js_out = "webglprotein.js"
if root == "testing":
  js_in.append(js_last)
  for script in js_in:
    source = os.path.join("scripts", script)
    dest   = os.path.join(root, "static", script)
    if script == js_last:
      dest = os.path.join(root, "static", js_out)
    base   = os.path.dirname(dest)
    if not os.path.exists(base):
      os.makedirs(base)
    shutil.copy(source, dest)
else:
  # Concatenate files
  js_temp = os.path.abspath(os.path.join("scripts", "js.temp"))
  with open(js_temp, "w") as destination:
    for script in js_in:
      source = os.path.join("scripts", script)
      shutil.copyfileobj(open(source, "r"), destination)

    # Last one is special: remove SNIP-SNAP code!
    source = os.path.join("scripts", "protgl.js")
    rx_snipsnap = re.compile("//SNIP.+?//SNAP", re.MULTILINE | re.DOTALL)
    with open(source, "r") as snipsnap:
      contents = snipsnap.read()
      destination.write(rx_snipsnap.sub("", contents))
  destination.close()

  final = os.path.abspath(os.path.join(root, "static", js_out))
  uglipath = os.path.abspath(os.path.join("scripts", "uglify", "bin"))
  print(uglipath)

  new_env = os.environ
  new_env["PATH"] += ":"+uglipath
  exec = subprocess.Popen(["uglifyjs", "-o", final, js_temp], \
    cwd=uglipath, env=new_env)
  exec.wait()

  if exec.returncode != 0:
    print("Failed to uglify my js!")
    exit(0)

print("Updating shaders") # -> shaders.json
with open(os.path.join(root, "static", "shaders.json"), "w") as output:
  shaders = dict()
  shad_path = os.path.join("scripts", "shaders")
  for file in os.listdir(shad_path):
    (name, ext) = os.path.splitext(file)
    typ = ""
    tuple = dict()
    if name in shaders:
      tuple = shaders[name]
    if (ext == ".fragment"):
      typ = "f"
    elif ext == ".vertex":
      typ = "v"
    if not typ:
      continue
    with open(os.path.join(shad_path, file)) as value:
      tuple[typ] = value.read()
    shaders[name] = tuple
  for key in shaders:
    tuple = shaders[key]
    if not "f" in tuple or not "v" in tuple:
      del shaders[key]
  json.dump(shaders, output)

# # Update CSS files
# normal = "static/normal.css"
# with open(path.join(root, normal), "wb") as normalout:
#   for source in ["static/basic.css", "static/header.css", "static/main.css", "static/menu.css"]:
#     try:
#       with open(source, "rb") as content:
#         body = content.read()
#         updated = body.decode("UTF-8").format(**vars).encode("UTF-8")
#         normalout.write(updated)
#     except Exception as e:
#       print("Failed to update CSS file")
#       print(e)
#       exit(1)
# 
# # Create backup folder
# backup = path.join(root, vars["_backup_root_"])
# subprocess.call(["mkdir", backup])
# subprocess.call(["chmod", "777", backup])

# Create log file
logfile = path.join(root, "webglprotein.log")
subprocess.call(["touch", logfile])
subprocess.call(["chmod", "666", logfile])

# Create database
print("Creating database")
database = path.join(root, database)
script = open("scripts/database.sql", "r")
proc = subprocess.Popen(["sqlite3", database], stdin=script)
proc.wait()
script.close()

# Prepare database
script = open("scripts/"+root+"_database.sql", "r")
proc = subprocess.Popen(["sqlite3", database], stdin=script)
proc.wait()
script.close()

proc = subprocess.Popen(["chmod", "775", root])
proc.wait()

subprocess.call(["chmod", "664", database])

# print("Copying dictionary")
# subprocess.call(["cp", dic_path, os.path.join(root, "private", "html.pickle")])
# 
print("Done")
