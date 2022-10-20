import pytest
import requests
from groups import Groups
from groups.schema import GroupSchema
from libraries.redis import Redis
from nodes import (
    Node,
    NodesRegistry,
    handle_ON_CLUSTER_ADD_GROUP,
    handle_ON_CLUSTER_COMMIT_GROUP,
    handle_ON_CLUSTER_ROLLBACK_GROUP,
    setup_event_handlers,
)
from event import subscribers


def test_create_node_default():
    id = "host_1"
    node = Node(id)
    assert node.id == id
    assert isinstance(node.groups, Groups)


def test_create_node_no_param():
    with pytest.raises(TypeError) as err:
        node = Node()


def test_node_str_representation():
    id = "host_1"
    node = Node(id)
    assert str(node) == f"<{id}>"


def test_nodes_registry_build_with_hosts():
    hosts = ["host1", "host3"]
    nodes_registry = NodesRegistry.build(hosts)
    assert len(nodes_registry) == len(hosts)


def test_nodes_registry_build_without_hosts():
    nodes_registry = NodesRegistry.build([])
    assert len(nodes_registry) == len([])


@pytest.mark.asyncio
async def test_handle_on_cluster_add_group_default():
    id = "host_1"
    node = Node(id)
    payload = GroupSchema(groupId="group1")
    error = False

    await handle_ON_CLUSTER_ADD_GROUP(node, payload, error)


@pytest.mark.asyncio
async def test_handle_on_cluster_add_group_with_error():
    with pytest.raises(requests.exceptions.HTTPError) as err:
      id = "host_1"
      node = Node(id)
      payload = GroupSchema(groupId="group1")
      error = True

      await handle_ON_CLUSTER_ADD_GROUP(node, payload, error)


@pytest.fixture
def node():
    node = Node("node1")
    group = GroupSchema(groupId="group1")
    node.groups.db._shadow_db.append(group)
    return node


@pytest.fixture
def redis():
    redis = Redis
    redis['processed_nodes'] = []
    return redis


@pytest.mark.asyncio
async def test_handle_on_cluster_commit_group(node, redis):
    node1 = node
    redis["processed_nodes"].append(node1)

    await handle_ON_CLUSTER_COMMIT_GROUP(node1)

    assert len(node1.groups.db._shadow_db) == 1
    assert len(redis["processed_nodes"]) == 1


def test_setup_event_handlers():
    setup_event_handlers()
    assert len(subscribers) == 4
