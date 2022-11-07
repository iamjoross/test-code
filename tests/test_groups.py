import pytest
from groups import Groups
from groups.db import GroupDatabase
from groups.schema import GroupSchema
from interfaces import GroupAlreadyExists, GroupNotFound


##############################
#
# GROUPS
#
##############################


@pytest.fixture
def groups():
  groups = Groups()
  return groups

def test_groups_init_default(groups):
  assert isinstance(groups.db, GroupDatabase)

def test_groups_add(groups):
  group_ids = ["group1", "group2"]
  for id in group_ids:
    group = GroupSchema(groupId=id)
    groups.db.db[id] = group

  for group in groups.db.db:
    assert group in group_ids

##############################
#
# GROUP DATABASE
#
##############################

def test_groupdb_init():
  db = GroupDatabase()
  assert len(db.db) == 0
  assert db.auto_commit == True

def test_groupdb_init_false_commit():
  db = GroupDatabase(auto_commit=False)
  assert len(db.db) == 0
  assert db.auto_commit == False
  assert len(db._shadow_db) == 0
  assert db.db == {}

@pytest.fixture
def db():
  return GroupDatabase()

@pytest.fixture
def db_false_autocommit():
  return GroupDatabase(auto_commit=False)

def test_groupdb_add(db: GroupDatabase):
  id = "group1"
  payload = {"groupId": id}
  resp = db.add(payload)
  assert len(db.db) == 1
  assert len(db._shadow_db) == 0
  assert resp == id


def test_groupdb_false_autocommit_add(db_false_autocommit: GroupDatabase):
  db = db_false_autocommit
  id = "group1"
  payload = {"groupId": id}
  resp = db.add(payload)
  assert len(db.db) == 0
  assert len(db._shadow_db) == 1
  assert resp == id


def test_groupdb_false_autocommit_add_conflict(db_false_autocommit: GroupDatabase):
  with pytest.raises(GroupAlreadyExists) as err:
    db = db_false_autocommit
    id = "group1"
    payload = {"groupId": id}
    resp = db.add(payload)
    resp = db.add(payload)


def test_groupdb_search(db_false_autocommit: GroupDatabase):
  db = db_false_autocommit
  payload1 = {"groupId": "group1"}
  payload2 = {"groupId": "group2"}
  db.add(payload1)
  db.add(payload2)
  resp = db._search("group1")
  assert resp == True

def test_groupdb_search_not_found(db_false_autocommit: GroupDatabase):
  db = db_false_autocommit
  payload1 = {"groupId": "group1"}
  payload2 = {"groupId": "group2"}
  db.add(payload1)
  db.add(payload2)
  resp = db._search("group3")
  assert resp == False

def test_groupdb_query(db_false_autocommit: GroupDatabase):
  db = db_false_autocommit
  payload1 = {"groupId": "group1"}
  payload2 = {"groupId": "group2"}
  db.add(payload1)
  db.add(payload2)
  resp: GroupSchema | None = db.query("group1")
  assert resp.groupId == "group1"

def test_groupdb_query_not_found(db_false_autocommit: GroupDatabase):
  db = db_false_autocommit
  payload1 = {"groupId": "group1"}
  payload2 = {"groupId": "group2"}
  db.add(payload1)
  db.add(payload2)
  resp = db.query("group3")
  assert resp == None

def test_groupdb_false_autocommit_delete(db_false_autocommit: GroupDatabase):
  db = db_false_autocommit
  id = "group1"
  payload = {"groupId": id}
  resp = db.add(payload)
  db.delete(id)

  assert len(db.db) == 0


def test_groupdb_false_autocommit_delete_conflict(db_false_autocommit: GroupDatabase):
  with pytest.raises(GroupNotFound) as err:
    db = db_false_autocommit
    id = "group1"
    payload = {"groupId": id}
    resp = db.add(payload)
    db.delete("group2")



