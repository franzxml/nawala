import platform
import shutil
from pathlib import Path


def find_libreoffice() -> str | None:
    system_name = platform.system()

    if system_name == "Darwin":
        mac_path = Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")
        if mac_path.exists():
            return str(mac_path)

    if system_name == "Windows":
        windows_paths = [
            Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
            Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"),
        ]
        for path in windows_paths:
            if path.exists():
                return str(path)

    # Linux, macOS dengan PATH custom, atau Windows jika soffice ada di PATH.
    for command in ("libreoffice", "soffice"):
        detected_path = shutil.which(command)
        if detected_path:
            return detected_path

    return None

