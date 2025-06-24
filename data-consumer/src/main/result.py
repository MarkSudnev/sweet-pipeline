from typing import Optional, Callable, Any


class Result[T]:

  def __init__(self, value: Optional[T], error: Optional[str]):
    self.__value: Optional[T] = value
    self.__error: Optional[str] = error

  def is_successful(self) -> bool:
    return self.__error is None

  @property
  def value(self) -> Optional[T]:
    return self.__value

  @property
  def error(self) -> Optional[str]:
    return self.__error

  @classmethod
  def from_function[T](cls, func: Callable[[], T]) -> "Result[T]":
    try:
      return Success(func())
    except Exception as e:
      return Failure(str(e))

  class Unit:
    pass


class Success[T](Result):

  def __init__(self, value: T):
    super().__init__(value=value, error=None)


class Failure(Result):

  def __init__(self, error: str):
    super().__init__(value=None, error=error)




def Unit():
  return Result.Unit()

