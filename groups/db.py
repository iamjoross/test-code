from typing import Any
from groups.schema import GroupSchema
from interfaces import DatabaseInterface, GroupAlreadyExists, GroupNotFound

"""
This Class mocks a database for persistence
"""

class GroupDatabase(DatabaseInterface):
  def __init__(self, auto_commit: bool = True) -> None:
    """Create new instance of GroupDatabase


    Args:
        auto_commit (bool, optional): mocks the auto_commit behavior of a databasel; when True (default), all changes are  saved to the db automatically; when False, all changes are saved in a temporary db shadowing the real persistent state to imitate actual behvaior in sqlalchemy. Defaults to True.
    """
    self.db: dict[str, Any] = {}
    self.auto_commit:bool = auto_commit

    self._shadow_db: dict[str, Any] = {}
    if not self.auto_commit:
      self._shadow_db = self.db.copy()

  def __len__(self) -> int:
    """Returns length of the object

    Returns:
        int: length of Groups
    """
    if self.auto_commit:
      return len(self.db)
    return len(self._shadow_db)

  def add(self, json: dict[str, str]) -> str | GroupAlreadyExists:
    """Add to Group database

    Args:
        json (dict[str, str]): json payload

    Raises:
        GroupAlreadyExists: Error raised if group already exists

    Returns:
        str | GroupAlreadyExists: group id or error
    """
    group: GroupSchema = GroupSchema(**json)
    db: dict[str, Any] = self.db.copy()
    if not self.auto_commit:
      db = self._shadow_db.copy()

    group_exists = self._search(group.groupId)

    if group_exists:
      raise GroupAlreadyExists("Group already exists")

    db[group.groupId] = group

    if not self.auto_commit:
      self._shadow_db = db.copy()
    else:
      self.db = db.copy()

    return group.groupId

  def _search(self, key: str) -> bool:
    """Search helper function

    Args:
        key (str): group id to search

    Returns:
        bool
    """
    db = self.db
    if not self.auto_commit:
      db = self._shadow_db

    if key in db:
      return True
    return False

  def query(self, key: str) -> GroupSchema | None:
    """Gets or query for a group in group database

    Args:
        key (str): gorup key to query

    Returns:
        GroupSchema | None: the group or None
    """
    db = self.db
    if not self.auto_commit:
      db = self._shadow_db

    group_exists= self._search(key)
    if group_exists:
      return db[key]
    return None

  def delete(self, key: str) -> str:
    """Deletes the gorup in the database

    Args:
        key (str): group id to delete

    Raises:
        GroupNotFound: Group does not exist

    Returns:
        str: deleted group id
    """
    db: dict[str, Any] = self.db.copy()
    if not self.auto_commit:
      db = self._shadow_db.copy()

    group_exists= self._search(key)
    if not group_exists:
      raise GroupNotFound('Group does not exist')
    popped: GroupSchema = db[key]
    del db[key]

    if not self.auto_commit:
      self._shadow_db = db.copy()
    else:
      self.db = db.copy()

    return popped.groupId

  def rollback(self) -> None:
    """Imitate sqlalchemy rollback function
    """
    self._shadow_db = self.db.copy()

  def commit(self) -> None:
    """Imitate sqlalchemy commit function
    """
    self.db = self._shadow_db.copy()



