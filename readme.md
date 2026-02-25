# Advanced Object-Oriented Calculator

A command-line calculator application built in Python 3.9, demonstrating advanced
object-oriented design patterns, persistent data management with pandas, and
comprehensive test coverage via pytest and GitHub Actions.

---

## Project Structure

```
project-root/
├── app/
│   ├── calculation.py          # Calculation value object (data model)
│   ├── calculator.py           # Core Calculator class (Facade)
│   ├── calculator_config.py    # Configuration management via environment variables
│   ├── calculator_memento.py   # Memento pattern — undo/redo state snapshots
│   ├── calculator_repl.py      # REPL — command-line user interface
│   ├── exceptions.py           # Custom exception hierarchy
│   ├── history.py              # Observer pattern — logging and auto-save
│   ├── input_validators.py     # Input validation and sanitization
│   └── operations.py           # Strategy + Factory patterns — arithmetic operations
├── tests/
│   ├── test_calculation.py
│   ├── test_calculator.py
│   ├── test_calculator_config.py
│   ├── test_calculator_memento.py
│   ├── test_calculator_repl.py
│   ├── test_exceptions.py
│   ├── test_history.py
│   ├── test_input_validators.py
│   └── test_operations.py
├── history/
│   └── calculator_history.csv  # Auto-generated on first save
├── logs/
│   └── calculator.log          # Auto-generated on first run
├── .env                        # Optional environment variable overrides
├── .github/
│   └── workflows/
│       └── python-app.yml      # GitHub Actions CI workflow
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/denrico-njit/repl_calculator_module5.git
cd repl_calculator_module5
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure environment variables

Copy or create a `.env` file in the project root to override default settings:

```env
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1e999
CALCULATOR_DEFAULT_ENCODING=utf-8
```

All settings have sensible defaults and the `.env` file is optional.

### 5. Run the calculator

```bash
python main.py
```

---

## Usage & Commands

Once started, the calculator presents a prompt and accepts the following commands:

| Command      | Description                                      |
|--------------|--------------------------------------------------|
| `add`        | Add two numbers                                  |
| `subtract`   | Subtract the second number from the first        |
| `multiply`   | Multiply two numbers                             |
| `divide`     | Divide the first number by the second            |
| `power`      | Raise the first number to the power of the second|
| `root`       | Calculate the nth root of a number               |
| `history`    | Display all calculations in the current session  |
| `clear`      | Clear the calculation history                    |
| `undo`       | Undo the last calculation                        |
| `redo`       | Redo the last undone calculation                 |
| `save`       | Save history to CSV file                         |
| `load`       | Load history from CSV file                       |
| `help`       | Display available commands                       |
| `exit`       | Save history and exit the application            |

### Example session

```
Calculator started. Type 'help' for commands.

Enter command: add

Enter numbers (or 'cancel' to abort):
First number: 10
Second number: 5

Result: 15

Enter command: history

Calculation History:
1. Addition(10, 5) = 15

Enter command: undo
Operation undone

Enter command: exit
History saved successfully.
Goodbye!
```

---

## Design Patterns

### Facade — `Calculator` class (`app/calculator.py`)

`Calculator` acts as a Facade over the application's subsystems. The REPL interacts
with a single `calc.calculate()` call rather than coordinating configuration,
validation, operation execution, state management, and persistence separately.
Each subsystem remains independently testable while the Facade keeps the interface
simple for client code.

### Strategy — `Operation` and subclasses (`app/operations.py`)

Each arithmetic operation (`Addition`, `Subtraction`, `Multiplication`, `Division`,
`Power`, `Root`) is encapsulated as a class implementing the abstract `Operation`
interface. The `Calculator` holds a reference to the current operation strategy,
which can be swapped at runtime without modifying the core calculation logic.

### Factory — `OperationFactory` (`app/operations.py`)

`OperationFactory.create_operation()` maps user-supplied command strings (e.g.,
`'add'`) to the appropriate `Operation` subclass. New operations can be registered
via `OperationFactory.register_operation()` without modifying existing code,
adhering to the Open/Closed principle.

### Observer — `HistoryObserver`, `LoggingObserver`, `AutoSaveObserver` (`app/history.py`)

After each calculation, `Calculator.notify_observers()` notifies all registered
observers. `LoggingObserver` writes calculation details to the log file;
`AutoSaveObserver` triggers a CSV save if auto-save is enabled. The `Calculator`
class has no knowledge of what observers do — new behaviors can be added by
registering additional observers without touching the core class.

### Memento — `CalculatorMemento` (`app/calculator_memento.py`)

Before each calculation, the current history is snapshot-copied into a
`CalculatorMemento` and pushed onto the undo stack. Undo restores the previous
snapshot; redo reapplies it. This decouples state management from calculation
logic and supports arbitrary undo/redo depth up to `max_history_size`.

---

## Testing

Run the full test suite with coverage:

```bash
pytest --cov=app tests/
```

Enforce 100% coverage (mirrors the CI check):

```bash
coverage report --fail-under=100
```

Tests are organized to mirror the `app/` module structure. Parameterized tests
cover both valid inputs and edge cases (division by zero, negative roots, invalid
input formats, configuration errors, etc.).

---

## Continuous Integration

GitHub Actions runs the test suite and enforces 100% coverage on every push and
pull request to `main`. The workflow file is located at
`.github/workflows/python-app.yml`.

```yaml
name: Python application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov pandas python-dotenv
    - name: Run tests with coverage
      run: |
        pytest --cov=app tests/
    - name: Check coverage
      run: |
        coverage report --fail-under=100
```
