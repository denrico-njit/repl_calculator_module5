import datetime
import pytest
from decimal import Decimal
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


# Test Fixtures 

@pytest.fixture
def single_calculation():
    return Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3")
    )

@pytest.fixture
def multiple_calculations():
    return [
        Calculation(operation="Addition",       operand1=Decimal("2"),  operand2=Decimal("3")),
        Calculation(operation="Subtraction",    operand1=Decimal("10"), operand2=Decimal("4")),
        Calculation(operation="Multiplication", operand1=Decimal("3"),  operand2=Decimal("5")),
    ]


# Testing Initialization

def test_memento_initialization(single_calculation):
    memento = CalculatorMemento(history=[single_calculation])
    assert len(memento.history) == 1
    assert memento.history[0] == single_calculation
    assert isinstance(memento.timestamp, datetime.datetime)

def test_memento_empty_history():
    memento = CalculatorMemento(history=[])
    assert memento.history == []
    assert isinstance(memento.timestamp, datetime.datetime)

def test_memento_multiple_calculations(multiple_calculations):
    memento = CalculatorMemento(history=multiple_calculations)
    assert len(memento.history) == 3


# Testing to_dict

def test_to_dict_contains_required_keys(single_calculation):
    memento = CalculatorMemento(history=[single_calculation])
    result = memento.to_dict()
    assert "history" in result
    assert "timestamp" in result

def test_to_dict_empty_history():
    memento = CalculatorMemento(history=[])
    result = memento.to_dict()
    assert result["history"] == []

def test_to_dict_history_length(multiple_calculations):
    memento = CalculatorMemento(history=multiple_calculations)
    result = memento.to_dict()
    assert len(result["history"]) == 3

def test_to_dict_timestamp_is_isoformat(single_calculation):
    memento = CalculatorMemento(history=[single_calculation])
    result = memento.to_dict()
    # Should not raise
    datetime.datetime.fromisoformat(result["timestamp"])

def test_to_dict_calculation_fields(single_calculation):
    memento = CalculatorMemento(history=[single_calculation])
    result = memento.to_dict()
    calc_dict = result["history"][0]
    assert calc_dict["operation"] == "Addition"
    assert calc_dict["operand1"] == "2"
    assert calc_dict["operand2"] == "3"
    assert calc_dict["result"] == "5"


# Testing from_dict

def test_from_dict_empty_history():
    data = {
        "history": [],
        "timestamp": datetime.datetime.now().isoformat()
    }
    memento = CalculatorMemento.from_dict(data)
    assert memento.history == []

def test_from_dict_restores_timestamp():
    ts = datetime.datetime(2024, 1, 15, 10, 30, 0)
    data = {
        "history": [],
        "timestamp": ts.isoformat()
    }
    memento = CalculatorMemento.from_dict(data)
    assert memento.timestamp == ts

def test_from_dict_restores_calculations():
    data = {
        "history": [
            {
                "operation": "Addition",
                "operand1": "2",
                "operand2": "3",
                "result": "5",
                "timestamp": datetime.datetime.now().isoformat()
            }
        ],
        "timestamp": datetime.datetime.now().isoformat()
    }
    memento = CalculatorMemento.from_dict(data)
    assert len(memento.history) == 1
    assert memento.history[0].operation == "Addition"
    assert memento.history[0].operand1 == Decimal("2")
    assert memento.history[0].operand2 == Decimal("3")
    assert memento.history[0].result == Decimal("5")


# Making sure to_dict and from_dict match

def test_round_trip_empty_history():
    original = CalculatorMemento(history=[])
    restored = CalculatorMemento.from_dict(original.to_dict())
    assert restored.history == []
    assert restored.timestamp == original.timestamp

def test_round_trip_single_calculation(single_calculation):
    original = CalculatorMemento(history=[single_calculation])
    restored = CalculatorMemento.from_dict(original.to_dict())
    assert len(restored.history) == 1
    assert restored.history[0] == single_calculation
    assert restored.timestamp == original.timestamp

def test_round_trip_multiple_calculations(multiple_calculations):
    original = CalculatorMemento(history=multiple_calculations)
    restored = CalculatorMemento.from_dict(original.to_dict())
    assert len(restored.history) == len(multiple_calculations)
    for original_calc, restored_calc in zip(multiple_calculations, restored.history):
        assert original_calc == restored_calc
    assert restored.timestamp == original.timestamp