

from database.protein import Protein
from database.protein_group import ProteinGroup
from database.user import User
from database.user_group import UserGroup

class GroupTests:
  def __init__(self):
    self.p1 = Protein(1, "p1", "P1", 1, -1)
    self.p2 = Protein(2, "p2", "P2", 1, -1)
    self.p3 = Protein(3, "p3", "P3", 2, -1)
    self.p4 = Protein(4, "p4", "P4", 1, -1)
    self.pg1 = ProteinGroup(1, "g1", [], {self.p1, self.p2})
    self.pg2 = ProteinGroup(2, "g2", [], {self.p1, self.p3, self.p4})
    self.pg3 = ProteinGroup(3, "g3", [self.pg1])
    self.pg4 = ProteinGroup(4, "g4", [self.pg1, self.pg2, self.pg3])
    self.ug1 = UserGroup(1, "all", {}, [(self.pg1, 0x01)])
    self.ug2 = UserGroup(2, "jr", {self.ug1}, [])
    self.ug3 = UserGroup(3, "ys", {self.ug1}, [(self.pg2, 0x06), (self.pg3, 0x02)])
    self.u1 = User(1, "jrenggli", "j@r.c", 42, {self.ug2})
    self.u2 = User(2, "yschaerli", "y@r.s", 8282, {self.ug2, self.ug3})
    
  def test_protein_groups(self):
    assert(self.pg1.get_proteins() != self.pg2.get_proteins())
    assert(self.pg1.get_proteins() & self.pg2.get_proteins() == {self.p1})
    assert(self.pg1.get_proteins() == self.pg3.get_proteins())
    assert(self.pg4.get_proteins() & self.pg3.get_proteins() == self.pg4.get_proteins())

  def test_user_groups(self):
    assert(self.ug1.get_proteins() == {self.p1 : 1, self.p2 : 1})
    assert(self.ug2.get_proteins() == self.ug1.get_proteins())
    assert(self.ug3.get_proteins() == {self.p1 : 0x07, self.p2 : 0x03, self.p3 : 0x06, self.p4 : 0x06})
    assert(self.u1.get_proteins() == self.ug2.get_proteins())
    assert(self.u2.get_proteins() == self.ug3.get_proteins())

test = GroupTests()
test.test_protein_groups()
test.test_user_groups()
