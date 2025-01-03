import os
import pytest
import smtplib
from unittest.mock import patch, MagicMock
from billify.mail import Mail

def test_mail_env_missing(monkeypatch):
    """
    If EMAIL or EMAIL_KEY is not set, Mail should raise ValueError.
    """
    # Remove environment variables if set
    monkeypatch.delenv("EMAIL", raising=False)
    monkeypatch.delenv("EMAIL_KEY", raising=False)

    data = {
        "name": "Test User",
        "email": "user@example.com",
        "phone": "1234567890",
        "message": "Hello from tests!"
    }

    with pytest.raises(ValueError, match="EMAIL or EMAIL_KEY is not set"):
        Mail(data)

@patch("smtplib.SMTP", autospec=True)
def test_mail_sends_successfully(mock_smtp, monkeypatch):
    """
    If EMAIL and EMAIL_KEY are set, Mail should call smtplib.SMTP
    and successfully send an email.
    """
    # Set environment variables
    monkeypatch.setenv("EMAIL", "testsender@example.com")
    monkeypatch.setenv("EMAIL_KEY", "app_password_123")

    data = {
        "name": "Test User",
        "email": "user@example.com",
        "phone": "1234567890",
        "message": "Hello from tests!"
    }

    # Create a mock for the SMTP connection
    smtp_instance = mock_smtp.return_value.__enter__.return_value

    # Instantiate the Mail class (this triggers send_mail())
    Mail(data)

    # Assertions:
    # 1. Ensure we attempted to connect to smtp.gmail.com:587
    mock_smtp.assert_called_once_with("smtp.gmail.com", port=587, timeout=60)

    # 2. Check that we used starttls()
    smtp_instance.starttls.assert_called_once()

    # 3. Check that we attempted to login with the correct credentials
    smtp_instance.login.assert_called_once_with(
        user="testsender@example.com",
        password="app_password_123"
    )

    # 4. Check that sendmail was called
    smtp_instance.sendmail.assert_called_once()

