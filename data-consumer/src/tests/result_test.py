from result import Success, Failure, Unit, Result


class TestResult:

  def test_result_is_successful(self):

    result = Success("one-two")

    assert result.is_successful() is True
    assert result.value == "one-two"

  def test_result_is_successful_empty(self):
    result = Success(Unit())

    assert result.is_successful() is True
    assert type(result.value) is Result.Unit

  def test_result_is_not_successful(self):
    result = Failure("one-two")

    assert result.is_successful() is False
    assert result.error == "one-two"

  def test_create_successful_result_from_function(self):
    def a_function() -> str:
      return "alpha" + "beta"
    result: Result[str] = Result.from_function(a_function)

    assert result.is_successful() is True
    assert result.value == "alphabeta"

  def test_create_failure_result_from_function(self):
    def a_function() -> float:
      return 4/0
    result: Result[str] = Result.from_function(a_function)

    assert result.is_successful() is False
    assert result.error == "division by zero"
