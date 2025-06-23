import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from search import show_patient_status

######################################################################################
# Helper: mock input() for interactive testing
def run_with_input(mock_inputs, target_function):  #Used to mock user input behaviour
    with patch("builtins.input", side_effect=mock_inputs):
        target_function()

# Helper to simulate doses list
def make_dose_list(doses):
    return [{'dose': d['dose'], 'date_administered': d['date']} for d in doses]
######################################################################################

# Valid: Patient found, no doses
@patch("search.get_patient_info")
def test_search_patient_no_doses(mock_info, capsys):
    mock_info.return_value = (
        {
            'patient_id': 1, 'name': 'Jason', 'age': 20, 'contact': '01112345678',
            'email': 'a@gmail.com', 'vc': 'VC1', 'vaccine': 'AF'
        },
        []
    )
    run_with_input(["1"], show_patient_status)
    captured = capsys.readouterr()
    assert "Status: NEW" in captured.out

# Valid: Patient found with D1 only
@patch("search.get_patient_info")
def test_search_patient_d1_only(mock_info, capsys):
    mock_info.return_value = (
        {
            'patient_id': 2, 'name': 'Ali', 'age': 30, 'contact': '01112345678',
            'email': 'b@gmail.com', 'vc': 'VC2', 'vaccine': 'AF'
        },
        make_dose_list([{'dose': 'D1', 'date': datetime.now().date() - timedelta(days=3)}])
    )
    run_with_input(["2"], show_patient_status)
    captured = capsys.readouterr()
    assert "Status: COMPLETED-D1" in captured.out
    assert "return for Dose 2" in captured.out

# Valid: Patient found with D1 and D2
@patch("search.get_patient_info")
def test_search_patient_completed(mock_info, capsys):
    mock_info.return_value = (
        {
            'patient_id': 3, 'name': 'Amy', 'age': 25, 'contact': '01122334455',
            'email': 'c@gmail.com', 'vc': 'VC1', 'vaccine': 'AF'
        },
        make_dose_list([
            {'dose': 'D1', 'date': datetime.now().date() - timedelta(days=20)},
            {'dose': 'D2', 'date': datetime.now().date() - timedelta(days=5)}
        ])
    )
    run_with_input(["3"], show_patient_status)
    captured = capsys.readouterr()
    assert "Status: COMPLETED" in captured.out

# Invalid: patient not found
@patch("search.get_patient_info")
def test_search_patient_not_found(mock_info, capsys):
    mock_info.return_value = (None, [])
    run_with_input(["999"], show_patient_status)
    captured = capsys.readouterr()
    assert "Patient not found" in captured.out

# Invalid: patient ID is not an integer
def test_search_non_integer_id(capsys):
    run_with_input(["abc"], show_patient_status)
    captured = capsys.readouterr()
    assert "Invalid input" in captured.out