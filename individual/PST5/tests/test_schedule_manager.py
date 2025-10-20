# tests/test_schedule_manager.py
import pytest # type: ignore
import os
from app.schedule import ScheduleManager
from app.student import StudentUser

# A pytest fixture creates a clean environment for each test function.
@pytest.fixture
def fresh_manager():
    """Creates a fresh ScheduleManager instance using a temporary test data file."""
    test_file = "test_data.json"
    # ARRANGE: Ensure no old test file exists.
    if os.path.exists(test_file):
        os.remove(test_file)
    return ScheduleManager(data_path=test_file)

def test_create_course(fresh_manager):
    fresh_manager.add_teacher("Mr. Smith", "Piano")  # add teacher with id 1
    fresh_manager.add_course("Beginner Piano", "Piano", 1)
    assert len(fresh_manager.courses) == 1
    assert fresh_manager.courses[0].name == "Beginner Piano"

def test_record_payment_and_history(fresh_manager):
    # Create dummy data
    fresh_manager.students.append(StudentUser(1, "Alice", []))

    fresh_manager.record_payment(1, 100.00, "Credit Card")
    history = fresh_manager.get_payment_history(1)

    assert len(history) == 1
    assert history[0]['amount'] == 100.00
    assert history[0]['method'] == "Credit Card"

    
def test_export_report(fresh_manager, tmp_path):
    """Test that export_report() creates a CSV file."""
    fresh_manager.finance_log = [
        {"student_id": 1, "amount": 50, "method": "Card", "timestamp": "2025-10-19T10:00:00"}
    ]
    out = tmp_path / "finance_report.csv"
    ok = fresh_manager.export_report("finance", str(out))
    assert ok is True
    assert out.exists()

# tests/test_schedule_manager.py
# ... (fixture setup) ...
