#!/usr/bin/env python

from pathlib import Path

class FS:
    def __init__(self) -> None:
        # Locate the root directory
        self.repo_root = Path(__file__).resolve().parent.parent.parent
        # Core directories
        self.src_dir = self.repo_root / "src"
        self.storage_dir = self.repo_root / "storage"
        self.logs_dir = self.storage_dir / "logs"

        self.log_file = self.logs_dir / "audioclast.log"

        self.ui_dir = self.src_dir / "ui"
        self.tui_py = self.ui_dir / "tui" / "tui.py"
        self.audioclast_pid_file = Path("/tmp/audioclast.pid")

        # Logging Settings
        self.log_max_size_mb = 1  # MB
        self.log_max_backup_count = 5

        self.ensure_directories()

    def ensure_directories(self) -> None:
        """Ensure all required folders exist."""
        self.storage_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.log_file.touch(exist_ok=True)
