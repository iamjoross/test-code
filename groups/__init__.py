from groups.db import GroupDatabase

class Groups:
  """Groups instance
  """
  def __init__(self) -> None:
    """Initializes with GroupDatabase instance attached to mock database persistence
    """
    self.db:GroupDatabase = GroupDatabase(auto_commit=False)

  def __len__(self) -> int:
    """Returns length of the object

    Returns:
        int: length of Groups
    """
    return len(self.db.db)

  def __iter__(self):
    """Iterator

    Yields:
        string: Group id
    """
    for item in self.db.db:
      yield item.groupId
