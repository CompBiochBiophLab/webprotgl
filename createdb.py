#! /usr/bin/python

from database.database import Database

if __name__ == "__main__":
    db = Database()
    db.load()
    db.add_source("RCSB", "pdb",
      "http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=pdb&compression=NO&structureId={0}",
      "RCSB Protein Data Bank")
#    db.add_source("raspbian", "pdb", "http://192.168.2.128:8080/static/{0}.pdb", "Local test host")
    #db.add_user("jrenggli", "jrenggli@gmail.com", 42)
    
    source = db.find_source("rcsb", "pdb")
    #source = db.find_source("raspbian", "pdb")
    if not source:
      raise Exception("Source not found!")
    proteins = ["2KXR"]#,  "3M3N"]
    for name in proteins:
      protein = db.get_protein_info(source,  name)
      if not protein:
        raise Exception("Protein not found!")
      for mid in protein.get_models():
        model = db.load_model(protein, mid)
        print(len(model.getvalue()))
    print("main")


