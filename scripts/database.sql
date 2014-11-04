PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Groups (gid INTEGER NOT NULL, name TEXT NOT NULL,
  CONSTRAINT group_pk PRIMARY KEY(gid), CONSTRAINT group_unique UNIQUE(name));

CREATE TABLE IF NOT EXISTS Users (rid INTEGER NOT NULL, title TEXT NOT NULL,
  first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL,
  password BLOB NOT NULL, salt BLOB NOT NULL,
  CONSTRAINT user_pk PRIMARY KEY(rid), CONSTRAINT user_email UNIQUE(email));

CREATE TABLE IF NOT EXISTS Memberships (gid INTEGER NOT NULL, rid INTEGER NOT NULL,
  CONSTRAINT member_pk PRIMARY KEY(gid, rid),
  FOREIGN KEY (gid) REFERENCES Groups(gid),
  FOREIGN KEY (rid) REFERENCES Users(rid));

CREATE TABLE IF NOT EXISTS Sessions (eid TEXT NOT NULL, expires TIMESTAMP NOT NULL,
  state INTEGER NOT NULL, email TEXT NOT NULL,
  CONSTRAINT session_pk PRIMARY KEY(eid));

CREATE TABLE IF NOT EXISTS Sources (sid INTEGER NOT NULL, name TEXT NOT NULL,
  mimetype TEXT NOT NULL, url TEXT, description TEXT,
  CONSTRAINT source_pk PRIMARY KEY(sid), CONSTRAINT source_unique UNIQUE (name, mimetype));

CREATE TABLE IF NOT EXISTS Proteins (pid INTEGER NOT NULL, name TEXT NOT NULL, title TEXT DEFAULT NULL,
  sid INTEGER NOT NULL, model_date DATETIME DEFAULT NULL, date DATETIME NOT NULL,
  CONSTRAINT protein_pk PRIMARY KEY(pid), CONSTRAINT protein_unique UNIQUE (name, sid),
  FOREIGN KEY (sid) REFERENCES Sources(sid));

CREATE TABLE IF NOT EXISTS Models (pid INTEGER NOT NULL, model INTEGER NOT NULL, version INTEGER NOT NULL,
  date DATETIME NOT NULL, data BLOB NOT NULL,
  CONSTRAINT model_pk PRIMARY KEY (pid, model),
  FOREIGN KEY (pid) REFERENCES Proteins(pid));

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

INSERT OR IGNORE INTO Sources (name, mimetype, url, description) VALUES ("rcsb", "pdb",
  "http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=pdb&compression=NO&structureId={0}",
  "RCSB Protein Data Bank");
