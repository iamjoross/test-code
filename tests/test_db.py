# from random import randint, random

# import pytest

# from db import GroupAlreadyExists, GroupDatabase, GroupNotFound, NodeAlreadyExists, NodeDatabase, NodeNotFound
# from schemas import GroupSchema, NodeSchema


# def test_node_repo_init():
#     node_db = NodeDatabase()
#     assert len(node_db.db) == 0

# def test_node_repo_add():
#   node_db = NodeDatabase()
#   node_length = randint(0, 9999)
#   for i in range(node_length):
#     node_db.add(NodeSchema(id
#     =f"node_{i}"))
#   assert len(node_db.db) == node_length

# def test_node_repo_add_conflict():
#   with pytest.raises(NodeAlreadyExists) as err:
#     node_db = NodeDatabase()
#     node_length = randint(0, 9999)
#     for i in range(node_length):
#       node_db.add(NodeSchema(id
#       =f"node_{i}"))

#     node_db.add(NodeSchema(id
#       =f"node_{node_length - 10}"))
#     assert str(err.value) == 'Node already exists'

# def test_node_repo_query_found():
#   node_db = NodeDatabase()
#   node_length = randint(0, 9999)
#   for i in range(node_length):
#     node_db.add(NodeSchema(id
#     =f"node_{i}"))

#   id_lookup = randint(0, node_length)
#   id_key_lookup = f"node_{id_lookup}"
#   print(id_key_lookup)
#   found = node_db.query(id_key_lookup)
#   print(found)
#   assert found is not None

# def test_node_repo_query_not_found():
#   node_db = NodeDatabase()
#   node_length = randint(0, 9999)
#   for i in range(node_length):
#     node_db.add(NodeSchema(id
#     =f"node_{i}"))

#   id_lookup = node_length + 2
#   id_key_lookup = f"node_{id_lookup}"
#   found = node_db.query(id_key_lookup)

#   assert found is None

# def test_node_repo_delete_item_not_in_db():
#   with pytest.raises(NodeNotFound) as err:
#     node_db = NodeDatabase()
#     node_length = randint(0, 9999)
#     for i in range(node_length):
#       node_db.add(NodeSchema(id
#       =f"node_{i}"))

#     id_lookup = node_length + 2
#     id_key_lookup = f"node_{id_lookup}"

#     res = node_db.delete(id_key_lookup)

#     assert str(err.value) == 'Node does not exist'

# def test_node_repo_delete_item_in_db():
#         node_db = NodeDatabase()
#         node_length = randint(0, 9999)
#         for i in range(node_length):
#           node_db.add(NodeSchema(id
#           =f"node_{i}"))

#         id_lookup = node_length - 2
#         id_key_lookup = f"node_{id_lookup}"

#         res = node_db.delete(id_key_lookup)
#         print(res, id_key_lookup, len(node_db.db), node_length-1)

#         assert res == id_key_lookup
#         assert len(node_db.db) == node_length - 1

# ###############################
# #
# # TESTS FOR GROUP DATABASE
# #
# ###############################

# def test_group_repo_init_default():
#     group_db = GroupDatabase()
#     assert len(group_db.db) == 0
#     assert group_db.auto_commit == True
#     assert group_db._shadow_db == []

# def test_group_repo_init_autcommit_False():
#     group_db = GroupDatabase(auto_commit=False)
#     assert len(group_db.db) == 0
#     assert group_db.auto_commit == False
#     assert group_db._shadow_db == group_db.db

# def test_group_repo_add():
#   group_db = GroupDatabase()
#   group_length = randint(0, 9999)
#   for i in range(group_length):
#     group_db.add(GroupSchema(id
#     =f"group_{i}"))
#   assert len(group_db.db) == group_length

# def test_group_repo_add_conflict():
#   with pytest.raises(GroupAlreadyExists) as err:
#     group_db = GroupDatabase()
#     group_length = randint(0, 9999)
#     for i in range(group_length):
#       group_db.add(GroupSchema(id
#       =f"group_{i}"))

#     group_db.add(NodeSchema(id
#       =f"group_{group_length - 10}"))
#     assert str(err.value) == 'Group already exists'

# def test_group_repo_query_found():
#   group_db = GroupDatabase()
#   group_length = randint(0, 9999)
#   for i in range(group_length):
#     group_db.add(GroupSchema(id
#     =f"group_{i}"))

#   id_lookup = randint(0, group_length)
#   id_key_lookup = f"group_{id_lookup}"
#   found = group_db.query(id_key_lookup)
#   assert found is not None

# def test_group_repo_query_not_found():
#   group_db = GroupDatabase()
#   group_length = randint(0, 9999)
#   for i in range(group_length):
#     group_db.add(GroupSchema(id
#     =f"group_{i}"))

#   id_lookup = group_length + 2
#   id_key_lookup = f"group_{id_lookup}"
#   found = group_db.query(id_key_lookup)

#   assert found is None

# def test_group_repo_delete_item_not_in_db():
#   with pytest.raises(GroupNotFound) as err:
#     group_db = GroupDatabase()
#     group_length = randint(0, 9999)
#     for i in range(group_length):
#       group_db.add(GroupSchema(id
#       =f"group_{i}"))

#     id_lookup = group_length + 2
#     id_key_lookup = f"group_{id_lookup}"

#     res = group_db.delete(id_key_lookup)

#     assert str(err.value) == 'Group does not exist'

# def test_group_repo_delete_item_in_db():
#     group_db = GroupDatabase()
#     group_length = randint(0, 9999)
#     for i in range(group_length):
#       group_db.add(GroupSchema(id
#       =f"group_{i}"))

#     id_lookup = group_length - 2
#     id_key_lookup = f"group_{id_lookup}"

#     res = group_db.delete(id_key_lookup)

#     assert res == id_key_lookup
#     assert len(group_db.db) == group_length - 1



