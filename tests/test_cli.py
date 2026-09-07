"""Entry point behavior: version output, usage errors, installed console script."""

import subprocess
import sys
from pathlib import Path

import pytest

from pyweb_gen.cli import main


def console_script() -> Path:
    return Path(sys.executable).with_name("pyweb-gen")


def test_main_prints_package_version_and_exits_zero(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])

    assert exit_info.value.code == 0
    assert "pyweb-gen" in capsys.readouterr().out


def test_main_without_command_prints_usage_and_exits_two(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main([])

    assert exit_info.value.code == 2
    assert "usage" in capsys.readouterr().err


def test_installed_console_script_prints_version() -> None:
    result = subprocess.run(
        [str(console_script()), "--version"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "pyweb-gen" in result.stdout
