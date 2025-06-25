from typing import Callable

from src.main.domain.data_shipment import DataShipment
from src.main.result import Result

StoreShipment = Callable[[DataShipment], Result[Result.Unit]]
