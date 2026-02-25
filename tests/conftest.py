import pytest
import shutil
from pathlib import Path

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_directories():
    yield
    # Runs after the entire test session completes
    dirs_to_clean = [
        Path("test_logs"),
        Path("test_history"),
    ]
    for d in dirs_to_clean:
        if d.exists():
            shutil.rmtree(d)