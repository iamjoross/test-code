

import logging
from random import randint
from unittest.mock import patch
from cluster import Cluster, ClusterConnection, GroupOperation
from pytest_cases import fixture, parametrize
import pytest

# logging.getLogger().setLevel(logging.DEBUG)


@pytest.fixture(scope="function")
def hosts():
  rand_val = randint(0, 100)
  return [i for i in range(rand_val)]


class TestCluster:

  @pytest.mark.repeat(3)
  def test_init_with_hosts(self, hosts):
    cluster = Cluster(hosts)
    assert len(cluster.node_registry) == len(hosts)

  def test_init_without_hosts(self):
    with pytest.raises(TypeError):
      cluster = Cluster()

class TestClusterConnection:

  @pytest.fixture
  def conn(self, hosts):
    return ClusterConnection(hosts)

  def test_init(self, hosts):
    conn = ClusterConnection(hosts)
    assert len(conn.cluster.node_registry) == len(hosts)
    assert conn.redis is not None

  def test_init_without_hosts(self):
    with pytest.raises(TypeError):
      cluster = ClusterConnection()

  @pytest.mark.asyncio
  async def test_group_handle_add(self, conn:ClusterConnection):
    rand_val = randint(1, 5)
    for i in range(rand_val):
      await conn.group_handle(GroupOperation.ADD, f"group_{i}")

    for node in conn.cluster.node_registry:
      assert len(node.groups) == rand_val

  @pytest.mark.asyncio
  async def test_process_add_group_with_conflict(self, conn: ClusterConnection):
    rand_val = randint(1, 5)
    for i in range(rand_val):
      await conn.group_handle(GroupOperation.ADD, f"group_{i}")
    await conn.group_handle(GroupOperation.ADD, f"group_0")

    for node in conn.cluster.node_registry:
      assert len(node.groups) == rand_val


  @pytest.mark.asyncio
  async def test_process_delete_group(self, conn: ClusterConnection):
    rand_val = randint(1, 5)
    for i in range(rand_val):
      await conn.group_handle(GroupOperation.ADD, f"group_{i}")
    await conn.group_handle(GroupOperation.DELETE, f"group_0")

    for node in conn.cluster.node_registry:
      assert len(node.groups) == (rand_val - 1)

  @pytest.mark.asyncio
  async def test_process_delete_group_with_conflict(self, conn: ClusterConnection):
    rand_val = randint(1, 5)
    for i in range(rand_val):
      await conn.group_handle(GroupOperation.ADD, f"group_{i}")
    await conn.group_handle(GroupOperation.DELETE, f"group_6")

    for node in conn.cluster.node_registry:
      assert len(node.groups) == rand_val



