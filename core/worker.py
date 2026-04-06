"""db_worker subprocess manager."""

import atexit
import subprocess
import sys

_proc: subprocess.Popen | None = None  # type: ignore[type-arg]


def start() -> None:
    global _proc  # noqa: PLW0603
    if _proc is not None:
        return
    _proc = subprocess.Popen(  # noqa: S603
        [sys.executable, "manage.py", "db_worker", "--no-reload", "--no-startup-delay"],
    )
    atexit.register(_proc.terminate)


def get_status() -> dict:  # type: ignore[type-arg]
    """Return worker process status as a dict for template rendering."""
    if _proc is None:
        return {"state": "not_started"}
    code = _proc.poll()
    if code is None:
        return {"state": "running", "pid": _proc.pid}
    return {"state": "stopped", "exit_code": code}
