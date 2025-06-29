from typing import Callable

from domain.data_shipment import DataShipment
from result import Result

StoreShipment = Callable[[DataShipment], Result[Result.Unit]]
