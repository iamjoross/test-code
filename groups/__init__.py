from groups.db import GroupDatabase

class Groups:
  """Groups instance
  """
  def __init__(self) -> None:
    """Initializes with GroupDatabase instance attached to mock database persistence
    """
    self.db = GroupDatabase(auto_commit=False)

  def __len__(self):
    return len(self.db.db)

  def __iter__(self):
    """Iterator

    Yields:
        string: Group id
    """
    for item in self.db.db:
      yield item.groupId
