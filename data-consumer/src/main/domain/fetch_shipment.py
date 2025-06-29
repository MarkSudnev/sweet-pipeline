from typing import Callable

from domain.data_shipment import DataShipment
from domain.file_location import FileLocation
from result import Result

FetchShipment = Callable[[FileLocation], Result[DataShipment]]
