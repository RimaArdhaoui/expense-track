import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE" 

class Config:
    # NOTE: in a real deployment this must come from an environment
    # variable / secret manager, never be hardcoded or committed.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    DATABASE = os.environ.get("DATABASE", os.path.join(BASE_DIR, "expenses.db"))
