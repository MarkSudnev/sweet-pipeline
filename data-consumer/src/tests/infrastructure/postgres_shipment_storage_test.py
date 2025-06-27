from pathlib import Path

from src.main.domain.data_shipment import DataShipment
from src.main.infrastructure.postgres_shipment_storage import PostgresShipmentStorage
from src.main.result import Result
from src.tests import get_resource
from src.tests.fixtures import DummyPostgresStatementExecutor


class TestPostgresShipmentStorage:

  def test_postgres_client_is_called_with_proper_statement(self):
    file_location = get_resource("alpha-shipment-example.json")
    shipment = DataShipment(
      location=Path(file_location)
    )
    executor = DummyPostgresStatementExecutor()
    storage = PostgresShipmentStorage(executor=executor)
    result: Result[Result.Unit] = storage(shipment)

    assert result.is_successful() is True
    assert executor.statements[0] == insert_sql_statement

  def test_returns_failure_when_executor_is_failed(self):
    file_location = get_resource("alpha-shipment-example.json")
    shipment = DataShipment(
      location=Path(file_location)
    )

    def executor(_: str) -> None:
      raise Exception("some-error-happened")

    storage = PostgresShipmentStorage(executor=executor)
    result: Result[Result.Unit] = storage(shipment)

    assert result.is_successful() is False
    assert result.error == "some-error-happened"

  def test_returns_failure_when_data_file_is_missed(self):
    shipment = DataShipment(
      location=Path("missing-path")
    )

    executor = DummyPostgresStatementExecutor()
    storage = PostgresShipmentStorage(executor=executor)
    result: Result[Result.Unit] = storage(shipment)

    assert result.is_successful() is False
    assert result.error == "[Errno 2] No such file or directory: 'missing-path'"

  def test_returns_failure_when_data_file_is_in_invalid_format(self):
    file_location = get_resource("alpha-shipment-invalid-example.json")
    shipment = DataShipment(
      location=Path(file_location)
    )
    executor = DummyPostgresStatementExecutor()
    storage = PostgresShipmentStorage(executor=executor)
    result: Result[Result.Unit] = storage(shipment)

    assert result.is_successful() is False

insert_sql_statement = """
INSERT INTO alpha ("id", "body", "timestamp") VALUES ('1a7cb636-0acc-421b-84c2-af07ee1fbcd4', 'Lorem Ipsum', '2025-05-17T21:18:10+00:00');
"""
