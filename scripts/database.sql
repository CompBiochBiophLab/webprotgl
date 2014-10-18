PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Groups (gid INTEGER NOT NULL, name TEXT NOT NULL,
  CONSTRAINT group_pk PRIMARY KEY(gid), CONSTRAINT group_unique UNIQUE(name));

CREATE TABLE IF NOT EXISTS Users (rid INTEGER NOT NULL, username TEXT NOT NULL, name TEXT NOT NULL,
  email TEXT NOT NULL, password BLOB NOT NULL, salt BLOB NOT NULL,
  CONSTRAINT user_pk PRIMARY KEY(rid), CONSTRAINT user_uname UNIQUE(username));

CREATE TABLE IF NOT EXISTS Memberships (gid INTEGER NOT NULL, rid INTEGER NOT NULL,
  CONSTRAINT member_pk PRIMARY KEY(gid, rid));

CREATE TABLE IF NOT EXISTS Sources (sid INTEGER NOT NULL, name TEXT NOT NULL,
  mimetype TEXT NOT NULL, url TEXT, description TEXT,
  CONSTRAINT source_pk PRIMARY KEY(sid), CONSTRAINT source_unique UNIQUE (name, mimetype));

CREATE TABLE IF NOT EXISTS Proteins (pid INTEGER NOT NULL, name TEXT NOT NULL, title TEXT DEFAULT NULL,
  sid INTEGER NOT NULL, model_date DATETIME DEFAULT NULL, date DATETIME NOT NULL,
  CONSTRAINT protein_pk PRIMARY KEY(pid), CONSTRAINT protein_unique UNIQUE (name, sid));

CREATE TABLE IF NOT EXISTS Models (pid INTEGER NOT NULL, model INTEGER NOT NULL, version INTEGER NOT NULL,
  date DATETIME NOT NULL, data BLOB NOT NULL,
  CONSTRAINT model_pk PRIMARY KEY (pid, model));

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

INSERT OR IGNORE INTO Sources (name, mimetype, url, description) VALUES ("rcsb", "pdb",
  "http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=pdb&compression=NO&structureId={0}",
  "RCSB Protein Data Bank");
