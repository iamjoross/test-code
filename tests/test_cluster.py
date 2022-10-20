

import os
from random import randint
import sys
from unittest.mock import patch
import pytest
from cluster import Cluster, ClusterConnection
from interfaces import GroupAlreadyExists

sys.stdout = open(os.devnull, 'w')

@pytest.fixture
def hosts():
  return [
      "node01.app.internal.com",
      "node02.app.internal.com",
      "node03.app.internal.com",
      "node04.app.internal.com",
  ]

class TestCluster:

  def test_init(self, hosts):
    cluster = Cluster(hosts)
    assert len(cluster.node_registry) == len(hosts)

class TestClusterConnection:

  @pytest.fixture
  def conn(self, hosts):
    return ClusterConnection(hosts)


  def test_init(self, hosts):
    conn = ClusterConnection(hosts)
    assert len(conn.cluster.node_registry) == len(hosts)

  @pytest.mark.asyncio
  async def test_process_rollback(self, conn: ClusterConnection, hosts):
    for node in conn.cluster.node_registry:
      conn.redis['processed_nodes'].append(node)
    await conn._process_rollback()
    assert len(conn.redis['processed_nodes']) == 0

  @pytest.mark.asyncio
  async def test_process_commit(self, conn: ClusterConnection, hosts):
    for node in conn.cluster.node_registry:
      conn.redis['processed_nodes'].append(node)
    await conn._process_commit()
    assert len(conn.redis['processed_nodes']) == 0


  @pytest.mark.asyncio
  async def test_process_add_group(self, conn: ClusterConnection, hosts):
    max_range = randint(1, 10)
    for i in range(0, max_range):
      await conn.add_group(f"group_{i}")

    for i in range(0, len(hosts)):
      assert len(conn.cluster.node_registry[0].groups) == max_range

  @pytest.mark.asyncio
  async def test_process_add_group_with_conflict(self, conn: ClusterConnection, hosts):
    max_range = randint(1, 10)
    for i in range(0, max_range):
      await conn.add_group(f"group_{i}")
    await conn.add_group(f"group_0")

    for i in range(0, len(hosts)):
      assert len(conn.cluster.node_registry[0].groups) == max_range

  @pytest.mark.asyncio
  async def test_process_delete_group(self, conn: ClusterConnection, hosts):
    max_range = randint(1, 10)
    for i in range(0, max_range):
      await conn.add_group(f"group_{i}")

    for i in range(0, len(hosts)):
      assert len(conn.cluster.node_registry[0].groups) == max_range

  @pytest.mark.asyncio
  async def test_process_add_group_with_conflict(self, conn: ClusterConnection, hosts):
    max_range = randint(1, 10)
    for i in range(0, max_range):
      await conn.add_group(f"group_{i}")
    await conn.add_group(f"group_0")

    for i in range(0, len(hosts)):
      assert len(conn.cluster.node_registry[0].groups) == max_range

