from typing import Dict, Any
from urllib.parse import urlparse

import psycopg2

from infrastructure.postgres_shipment_storage import PostgresStatementExecutor


def PostgresCLient(connection_string: str) -> PostgresStatementExecutor:

  connection_params: Dict[str, Any] = parse_connection_string(connection_string)
  connection = psycopg2.connect(**connection_params)

  def _execute(sql_statement: str) -> None:
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    connection.commit()

  return _execute

def parse_connection_string(connection_string: str) -> Dict[str, Any]:
  parsed_uri = urlparse(connection_string)
  params = {"database": parsed_uri.path[1:]}
  auth, address = parsed_uri.netloc.split("@")
  username, password = auth.split(":")
  address_components = address.split(":")
  port = address_components[1] if len(address_components) > 1 else 5432
  params.update({
    "host": address_components[0],
    "port": port,
    "user": username,
    "password": password
  })
  return params

