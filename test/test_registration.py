import pytest
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch
from patient import (
    is_valid_name,
    is_valid_age,
    is_valid_contact,
    is_valid_email,
    is_valid_vaccination_center,
    is_vaccine_eligible,
    contact_exists,
    email_exists
)

valid_vaccines = ['AF', 'BV', 'CZ', 'DM', 'EC']

# ------------------- Valid Test Cases -------------------
def test_valid_name():
    assert is_valid_name("Yu Jie Xiang")

def test_valid_age():
    assert is_valid_age("12")
    assert is_valid_age("119")

def test_valid_contact():
    assert is_valid_contact("01112345678")

def test_valid_email():
    assert is_valid_email("test@example.com")

def test_valid_vc():
    assert is_valid_vaccination_center("VC1")
    assert is_valid_vaccination_center("vc2")

def test_valid_vaccine_code():
    assert "AF" in valid_vaccines
    assert "BV" in valid_vaccines
    assert "EC" in valid_vaccines

def test_invalid_vaccine_code():
    assert "XYZ" not in valid_vaccines
    assert "" not in valid_vaccines
    assert "aa" not in valid_vaccines

def test_age_12_can_take_AF():
    assert is_vaccine_eligible("AF", 12)

def test_age_45_can_take_CZ():
    assert is_vaccine_eligible("CZ", 45)

# 在 pytest 中使用多个 @patch 装饰器时，mock 对象的注入是从下往上传参的。
@patch("patient.get_connection")
def test_contact_not_exists(mock_conn):
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = []  # 模拟数据库中没有该手机号
    assert contact_exists("0111234567") == False

@patch("patient.get_connection")
def test_email_not_exists(mock_conn):
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = []  # 模拟数据库中没有该邮箱
    assert email_exists("notfound@example.com") == False

# ------------------- Invalid Test Cases -------------------
def test_invalid_vc():
    assert not is_valid_vaccination_center("VC3")

def test_invalid_name():
    assert not is_valid_name("Yu123")

def test_invalid_age_too_young():
    assert not is_valid_age("11")

def test_invalid_age_too_old():
    assert not is_valid_age("120")

def test_invalid_vaccine_code():
    assert not is_vaccine_eligible("XYZ", 30)

def test_invalid_age_vaccine_BV():
    assert not is_vaccine_eligible("BV", 17)

def test_invalid_contact_format():
    assert not is_valid_contact("123abc456")
    assert not is_valid_contact("123")

@patch("patient.get_connection")
def test_duplicate_contact(mock_conn):
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [(0,)]
    assert contact_exists("0111234567")

@patch("patient.get_connection")
def test_duplicate_email(mock_conn):
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [(1,)]
    assert email_exists("test@example.com")

def test_invalid_email_format():
    assert not is_valid_email("invalid-email")
    assert not is_valid_email("email.com")
    assert not is_valid_email("@domain.com")
