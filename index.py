import argparse
import asyncio
import logging
from cluster import ClusterConnection, GroupOperation
from constants import HOSTS
logging.getLogger().setLevel(logging.DEBUG)


async def default_scenario():
    """default scenario
    """
    conn = ClusterConnection(HOSTS)
    await conn.group_handle(GroupOperation.ADD, "group1")
    await conn.group_handle(GroupOperation.ADD, "group2")


async def add_group_error_scenario():
    """Scenario where when adding raises conflict"""
    conn = ClusterConnection(HOSTS)
    await conn.group_handle(GroupOperation.ADD, "group1")
    await conn.group_handle(GroupOperation.ADD, "group2")


async def remove_group_error_scenario():
    """Scenario where removing raises error"""
    conn = ClusterConnection(HOSTS)
    await conn.group_handle(GroupOperation.DELETE, "group2")
    await conn.delete_group("group2")


async def custom_scenario(
    hosts_to_add: int = 0, groups_to_add: int = 0, groups_to_remove: int = 0
):
    """Scenario with custom input

    Args:
        hosts_to_add (int, optional): hosts to add. Defaults to 0.
        groups_to_add (int, optional): groups to add. Defaults to 0.
        groups_to_remove (int, optional): groups to remove. Defaults to 0.
    """
    hosts = [f"node_{i}" for i in range(hosts_to_add)]
    conn = ClusterConnection(hosts)

    for i in range(groups_to_add):
        await conn.group_handle(GroupOperation.ADD, "group_{i}")

    for i in range(groups_to_remove):
        await conn.group_handle(GroupOperation.DELETE, "group_{i}")


async def main(
    scenario: str = "default",
    hosts_to_add: int = 0,
    groups_to_add: int = 0,
    groups_to_remove: int = 0,
):
    """Entrypoint

    Args:
        scenario (str, optional): . Defaults to "default".
        hosts_to_add (int, optional): . Defaults to 0.
        groups_to_add (int, optional): . Defaults to 0.
        groups_to_remove (int, optional): . Defaults to 0.
    """
    if scenario == "default":
        await default_scenario()
    elif scenario == "add_group_error":
        await add_group_error_scenario()
    elif scenario == "remove_group_error":
        await remove_group_error_scenario()
    elif scenario == "custom":
        await custom_scenario(hosts_to_add, groups_to_add, groups_to_remove)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='API Consumer.',formatter_class=argparse.ArgumentDefaultsHelpFormatter,)
    arg_parser.add_argument("--scenario", type=str, default="default", choices=["default", "add_group_error", "remove_group_error", "custom"], help="Scenario to run")
    arg_parser.add_argument("--n-nodes", type=int, default=0, help="Only used when scenario is custom")
    arg_parser.add_argument("--add-n-groups", type=int, default=0, help="Only used when scenario is custom")
    arg_parser.add_argument("--remove-n-groups", type=int, default=0, help="Only used when scenario is custom")

    args = arg_parser.parse_args()

    use_default_hosts = True
    if args.n_nodes != 0:
        use_default_hosts = False

    use_default_groups = True
    if args.add_n_groups != 0:
        use_default_hosts = False

    if use_default_hosts and use_default_groups:
        asyncio.run(main(scenario=args.scenario))
    else:
        asyncio.run(main(scenario=args.scenario, hosts_to_add=args.n_nodes, groups_to_add=args.add_n_groups, groups_to_remove=args.remove_n_groups))
