import json
from pathlib import Path
from typing import Callable, Dict, Any

from domain.data_shipment import DataShipment
from domain.store_shipment import StoreShipment
from result import Result, Failure

PostgresStatementExecutor = Callable[[str], None]

_sql_statement_template = """
INSERT INTO alpha ("id", "body", "timestamp") VALUES ('{_id}', '{body}', '{ts}');
"""


def PostgresShipmentStorage(
  executor: PostgresStatementExecutor
) -> StoreShipment:

  def _read_file(location: Path) -> Dict[str, Any]:
    raw: str = location.read_text(encoding="utf-8")
    return json.loads(raw)

  def _generate_sql_statement(data: Dict[str, Any]) -> str:
    body = data["response"].replace("'", "''")
    return _sql_statement_template.format(
      _id=data["id"],
      body=body,
      ts=data["timestamp"]
    )

  def _execute(shipment: DataShipment) -> Result[Result.Unit]:
    data_result: Result[Dict[str, Any]] = Result.from_function(
      lambda: _read_file(shipment.location)
    )
    if not data_result.is_successful():
      return Failure(data_result.error)

    sql_statement_result: Result[str] = Result.from_function(
      lambda : _generate_sql_statement(data_result.value)
    )
    if not sql_statement_result.is_successful():
      return Failure(sql_statement_result.error)

    return Result.from_function(lambda: executor(sql_statement_result.value))

  return _execute
