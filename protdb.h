#pragma once

extern c {

struct Protein {
  int64_t id_;
  char pszName_[16];

  // Null if last element
  Protein* pNext_;
}

Protein* findSimilar(const char* pszProteinName) {

}

}
