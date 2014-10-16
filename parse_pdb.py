#! /usr/bin/python3

from database.pdb_parser import PDBParser
from urllib import *

if __name__ == "__main__":
  parser = PDBParser()
  parser.parse(open("/home/jrenggli/prog/protdb/static/3M3N", "rb"))

