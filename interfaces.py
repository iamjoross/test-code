
from abc import ABC, abstractmethod


class NodeAlreadyExists(Exception):
  pass


class NodeNotFound(Exception):
  pass


class GroupAlreadyExists(Exception):
  pass


class GroupNotFound(Exception):
  pass

class DatabaseInterface(ABC):
  @abstractmethod
  def add(self, item): raise NotImplementedError
  @abstractmethod
  def query(self, filter): raise NotImplementedError
  @abstractmethod
  def delete(self, id): raise NotImplementedError




