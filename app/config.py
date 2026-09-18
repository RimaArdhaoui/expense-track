import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GITHUB_TOKEN = "ghp_9f8A2kLpQ7rT4vXcN1mZbY6wJdS3eR0uHiOg"
AWS_ACCESS_KEY_ID = "AKIAZP7HXJQR9K2LMNOP"

class Config:
    # NOTE: in a real deployment this must come from an environment
    # variable / secret manager, never be hardcoded or committed.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    DATABASE = os.environ.get("DATABASE", os.path.join(BASE_DIR, "expenses.db"))
