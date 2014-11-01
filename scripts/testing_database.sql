PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO Users (first_name, last_name, email, password, salt) VALUES ("Test", "User", "test+user@jrenggli.com",
  "f2a4b45914f32e4b6119624989411cac53d304b334c984a2311ad5ebaa60af53dbbf5272ff6a5b8caa2a5973f016c286547524889536cbeec9e513289bea26d1",
  "lwqDRLql6ndX5EFNXtT1DaDjZ_lbs1oZ-1Lo136Xp4_hE79eMRFQO2Eus2MV6pZJqlric38xACpGPqi8eQBB2vTK1gVZ60gzzvbBXwLvq89vWkhCUYex_gkLA88Tz-KS");

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

INSERT OR IGNORE INTO Sources (name, mimetype, url, description) VALUES ("test", "pdb",
  "http://www.jrenggli.com/audio/{0}.pdb", "Test server");
