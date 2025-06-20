from typing import Callable


def DataConsumer(

) -> Callable[[str], None]:

  def _execute(message: str):
    pass

  return _execute
