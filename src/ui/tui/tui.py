#!/usr/bin/env python3

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Static, Header, Footer
from textual.reactive import reactive
from textual.binding import Binding
from textual import events
from vfs.fs import FS
import subprocess
import threading
import time

class LogTail(Static):
    """Displays real-time log updates from fs.log_file."""
    def on_mount(self) -> None:
        self._stop = False
        self.set_interval(1, self.update_log)

    def update_log(self) -> None:
        try:
            with open(FS().log_file, 'r') as f:
                lines = f.readlines()[-20:]
                self.update("".join(lines))
        except Exception as e:
            self.update("Error reading log.")

    def stop(self) -> None:
        self._stop = True


class MainControl(Static):
    is_active = reactive(False)

    def on_mount(self) -> None:
        self.update_status()

    def toggle(self) -> None:
        self.is_active = not self.is_active
        subprocess.run(["audioclast", "on" if self.is_active else "off"])
        self.update_status()

    def update_status(self) -> None:
        status = "ON ✅" if self.is_active else "OFF ❌"
        self.update(f"[b]Audioclast Mic Monitoring:[/b] {status}")
        self.border_title = "ACTIVE" if self.is_active else "INACTIVE"
        self.styles.border = ("green" if self.is_focused else "dim")

    def on_focus(self, event) -> None:
        self.styles.border = "green"

    def on_blur(self, event) -> None:
        self.styles.border = "dim"


class AudioclastTUI(App):
    CSS_PATH = None
    BINDINGS = [
        Binding("tab", "switch_focus", "Switch Panel"),
        Binding("space", "toggle", "Toggle Mic"),
        Binding("ctrl+c", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container():
            self.main = MainControl()
            self.log = LogTail()
            yield Horizontal(self.main, self.log)
        yield Footer()

    def on_mount(self) -> None:
        self.main.focus()

    def action_switch_focus(self) -> None:
        if self.main.has_focus:
            self.log.focus()
        else:
            self.main.focus()

    def action_toggle(self) -> None:
        if self.main.has_focus:
            self.main.toggle()

    def action_quit(self) -> None:
        self.exit()

def main():
    AudioclastTUI().run()

if __name__ == "__main__":
    main()