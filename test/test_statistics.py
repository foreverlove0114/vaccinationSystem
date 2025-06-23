import pytest
from unittest.mock import patch, MagicMock
from stats import show_statistics

# 模拟患者列表与疫苗接种状态
def mock_patient_data(vc_name, patients):
    """
    模拟患者数据和其疫苗剂次数。
    patients: List of tuples (patient_id, dose_count)
    """
    vc_rows = [(vc_name,)]  # For unique VC
    stat_rows = [(pid, dose_count) for pid, dose_count in patients]
    return vc_rows, stat_rows

@patch("stats.get_vaccine_type")
@patch("stats.get_connection")
def test_vc_with_no_patients(mock_conn, mock_get_vaccine_type, capsys):
    mock_cursor = MagicMock()
    # VC exists but no patients
    mock_cursor.fetchall.side_effect = [
        [("VC1",)],  # unique VCs
        []           # No patient records
    ]
    mock_conn.return_value.cursor.return_value = mock_cursor

    show_statistics()
    captured = capsys.readouterr()
    assert "VC: VC1" in captured.out
    assert "Total Patients: 0" in captured.out

@patch("stats.get_vaccine_type")
@patch("stats.get_connection")
def test_vc_all_completed(mock_conn, mock_get_vaccine_type, capsys):
    # Assume all patients completed 2 doses
    vc_rows, stat_rows = mock_patient_data("VC2", [(1, 2), (2, 2), (3, 2)])
    mock_cursor = MagicMock()
    mock_cursor.fetchall.side_effect = [vc_rows, stat_rows]
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_get_vaccine_type.side_effect = ["AF", "BV", "CZ"]

    show_statistics()
    captured = capsys.readouterr()
    assert "VC: VC2" in captured.out
    assert "Total Patients: 3" in captured.out
    assert "Completed Vaccination: 3" in captured.out
    assert "Waiting for Dose 2: 0" in captured.out

@patch("stats.get_vaccine_type")
@patch("stats.get_connection")
def test_vc_all_d1_only(mock_conn, mock_get_vaccine_type, capsys):
    vc_rows, stat_rows = mock_patient_data("VC3", [(1, 1), (2, 1)])
    mock_cursor = MagicMock()
    mock_cursor.fetchall.side_effect = [vc_rows, stat_rows]
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_get_vaccine_type.side_effect = ["AF", "DM"]

    show_statistics()
    captured = capsys.readouterr()
    assert "VC: VC3" in captured.out
    assert "Total Patients: 2" in captured.out
    assert "Completed Vaccination: 0" in captured.out
    assert "Waiting for Dose 2: 2" in captured.out

@patch("stats.get_vaccine_type")
@patch("stats.get_connection")
def test_vc_mixed_statuses(mock_conn, mock_get_vaccine_type, capsys):
    vc_rows, stat_rows = mock_patient_data("VC4", [(1, 2), (2, 1), (3, 0)])
    mock_cursor = MagicMock()
    mock_cursor.fetchall.side_effect = [vc_rows, stat_rows]
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_get_vaccine_type.side_effect = ["AF", "AF", "AF"]

    show_statistics()
    captured = capsys.readouterr()
    assert "VC: VC4" in captured.out
    assert "Total Patients: 3" in captured.out
    assert "Completed Vaccination: 1" in captured.out
    assert "Waiting for Dose 2: 2" in captured.out

@patch("stats.get_vaccine_type")
@patch("stats.get_connection")
def test_vc_with_ec_patient(mock_conn, mock_get_vaccine_type, capsys):
    vc_rows, stat_rows = mock_patient_data("VC5", [(1, 1), (2, 2), (3, 1)])
    mock_cursor = MagicMock()
    mock_cursor.fetchall.side_effect = [vc_rows, stat_rows]
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_get_vaccine_type.side_effect = ["EC", "AF", "EC"]

    show_statistics()
    captured = capsys.readouterr()
    assert "VC: VC5" in captured.out
    assert "Total Patients: 3" in captured.out
    assert "Completed Vaccination: 3" in captured.out
    assert "Waiting for Dose 2: 0" in captured.out
