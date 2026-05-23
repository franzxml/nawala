from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
APP_DIR = BASE_DIR / "app"
TEMPLATES_DIR = APP_DIR / "templates"
TEMP_DIR = BASE_DIR / "temp"

ALLOWED_EXTENSION = ".pptx"
CONVERSION_TIMEOUT_SECONDS = 120

