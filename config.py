"""Runtime configuration for StegoSphere.

Set these environment variables before launching the app:
- STEGOSPHERE_SENDER_EMAIL
- STEGOSPHERE_SENDER_PASSWORD
- STEGOSPHERE_SMTP_SERVER (optional, defaults to smtp.gmail.com)
- STEGOSPHERE_SMTP_PORT (optional, defaults to 465)
"""

import os


SENDER_EMAIL = os.getenv("STEGOSPHERE_SENDER_EMAIL", "").strip()
SENDER_PASSWORD = os.getenv("STEGOSPHERE_SENDER_PASSWORD", "").strip()
SMTP_SERVER = os.getenv("STEGOSPHERE_SMTP_SERVER", "smtp.gmail.com").strip()
SMTP_PORT = int(os.getenv("STEGOSPHERE_SMTP_PORT", "465"))


def has_email_credentials() -> bool:
	"""Return True when required outbound email credentials are configured."""
	return bool(SENDER_EMAIL and SENDER_PASSWORD)
