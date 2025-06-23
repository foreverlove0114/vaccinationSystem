import pytest
from unittest.mock import patch
from vaccine import administer_vaccine

# Helper: mock input() for interactive testing
def run_with_input(mock_inputs, target_function):
    with patch("builtins.input", side_effect=mock_inputs):
        target_function()

# ---------- VALID TEST CASES ----------
# 在 pytest 中使用多个 @patch 装饰器时，mock 对象的注入是从下往上传参的。
@patch("vaccine.record_vaccination")  # mock_record
@patch("vaccine.get_patient_vaccine_info") # mock_info
def test_valid_dose1(mock_info, mock_record):
    mock_info.return_value = ("AF", None)
    run_with_input(["3", "D1"], administer_vaccine)
    mock_record.assert_called_once_with(3, "D1")

@patch("vaccine.record_vaccination") #模拟 record_vaccination 的执行行为（避免真实写入数据库）
@patch("vaccine.get_patient_vaccine_info") #模拟 get_patient_vaccine_info 的返回值
def test_valid_dose1_ec(mock_info, mock_record):
    mock_info.return_value = ("EC", None)
    run_with_input(["4", "D1"], administer_vaccine)
    mock_record.assert_called_once_with(4, "D1")

@patch("vaccine.record_vaccination") # mock_record
@patch("vaccine.get_patient_vaccine_info") # mock_info
def test_valid_dose2_after_interval(mock_info, mock_record):
    from datetime import datetime, timedelta
    dose1_date = datetime.now().date() - timedelta(days=14)
    mock_info.return_value = ("AF", dose1_date)
    run_with_input(["5", "D2"], administer_vaccine)
    mock_record.assert_called_once_with(5, "D2")

# ---------- INVALID TEST CASES ----------

@patch("vaccine.get_patient_vaccine_info")
def test_dose2_for_ec(mock_info):
    mock_info.return_value = ("EC", None)
    run_with_input(["4", "D2"], administer_vaccine)

@patch("vaccine.get_patient_vaccine_info")
def test_dose2_without_d1(mock_info):
    mock_info.return_value = ("AF", None)
    run_with_input(["5", "D2"], administer_vaccine)

@patch("vaccine.get_patient_vaccine_info")
def test_dose2_before_interval(mock_info):
    from datetime import datetime, timedelta
    dose1_date = datetime.now().date() - timedelta(days=10)  # too early
    mock_info.return_value = ("AF", dose1_date)
    run_with_input(["5", "D2"], administer_vaccine)

def test_invalid_patient_id():
    run_with_input(["abc", "D1"], administer_vaccine)

@patch("vaccine.get_patient_vaccine_info")
def test_invalid_dose_code(mock_info):
    mock_info.return_value = ("AF", None)
    run_with_input(["3", "D3"], administer_vaccine)
