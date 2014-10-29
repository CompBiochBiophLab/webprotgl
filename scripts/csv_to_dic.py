#! /usr/bin/python3

import csv
import os
import pickle
import re
import sys

csv_name    = os.path.join("scripts", "variables.csv")
#pickle_name = os.path.join(sys.argv[1], "private", "html.pickle")
pickle_name = sys.argv[1]

dic = dict()
typ = dict()
used = dict()
rx_accept = re.compile("(\w[\w|\s/-]*\w)$")
with open(csv_name, newline="") as csvfile:
  sheet = csv.reader(csvfile, delimiter=",", quotechar="\"")
  for (disabled, type, key, pro, pre, tst) in sheet:
    if disabled:
      if disabled != "no":
        continue
      else:
        used[key] = ["global"]
    if not rx_accept.match(key):
      raise Exception("Invalid key [" + str(key) + "]")
    if key in dic:
      raise Exception("Double variable: " + str(key))

    if not pro and key != "_base_path_":
      raise Exception("Missing translation for: [" + str(key) + "]")
    if not tst:
      tst = pro
    if not pre:
      pre = pro

    dic[key] = [tst, pre, pro]
    if type in typ:
      typ[type].append(key)
    else:
      typ[type] = [key]
    continue

#print(dic)
# Parse .html, .css, .py files looking for {...} variables
rx_filter  = re.compile(".+\.(html|css|py)$")
rx_var     = re.compile("({)?{(__)?(_?[a-zA-Z][^}]*)}", re.DOTALL)
rx_skipped = re.compile(".*/(?:testing|scripts|preprod|production)")
rx_special = re.compile("paper_review_(spd|lvl)_(\'|\") \+ str")
#used = dict()
for root, ign, files in os.walk(".", followlinks=True):
 
  match = rx_skipped.match(root)
  if match:
    print("Skipping folder: " + str(root))
    continue

  for file in files:
    match = rx_filter.match(file)
    if match:
      #print(file + " is a " + match.group(1) + " file")
      fullpath = os.path.join(root, file)
      try:
        with open(fullpath, "r") as content:
          text = content.read()
          for g_var in rx_var.findall(text):
            if g_var[0] or g_var[1]:
              continue
            key = g_var[2]
            if rx_special.match(key):
              continue
            if key in used:
              used[key].append(fullpath)
            else:
              used[key] = [fullpath]
      except Exception as e:
        print(e)

# Compare both sets for missing or useless keys
missing = set(used) - set(dic)
print("Missing:")
print(sorted(missing))

useless = set(dic) - set(used)
print("Useless:")
print(sorted(useless))

# Write files
single = dict()
idx = 0
if sys.argv[2] == "preprod":
  idx = 1
elif sys.argv[2] == "production":
  idx = 2
for key in dic:
  single[key] = dic[key][idx]

with open(pickle_name, "wb") as pickle_out:
  pickle.dump(single, pickle_out)
  pickle_out.close()
  print("Picked to " + pickle_name)

#with open("vars_testing.txt", "w") as out_tst:
  #for cls in sorted(typ):
    #out_tst.write("# " + str(cls) + "\n")
    #m_l = 0
    #for key in typ[cls]:
      #if len(key) > m_l:
        #m_l = len(key)
    #for key in typ[cls]:
      #out_tst.write("{{0:{0}}}{{1}}\n".format(m_l+2).format(key, dic[key][0]))
    #out_tst.write("\n")
  #out_tst.close()
  #print("Texted")
