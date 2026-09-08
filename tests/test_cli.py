"""Entry point behavior: version output, usage errors, feedback, installed script."""

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


def test_main_reports_scaffold_location(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    status = main(["init"])

    assert status == 0
    assert str(tmp_path) in capsys.readouterr().out


def test_main_reports_created_post(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    main(["init"])
    capsys.readouterr()

    status = main(["new-post", "--title", "Hello There"])

    assert status == 0
    assert "hello_there.md" in capsys.readouterr().out


def test_main_reports_refresh_summary(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    main(["init"])
    (tmp_path / "data" / "a_post.md").write_text(
        "---\ntitle: A post\ndate: 2026-09-07\nid: a_post\n---\n\nbody\n",
        encoding="utf-8",
    )
    capsys.readouterr()

    status = main(["refresh"])

    assert status == 0
    assert "a_post" in capsys.readouterr().out


def test_main_returns_one_with_message_on_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    status = main(["new-post", "--title", "No blog here"])

    output = capsys.readouterr()
    assert status == 1
    assert "data" in output.err


def test_main_init_with_name_writes_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    status = main(["init", "--name", "Inkwell"])

    assert status == 0
    assert "name: Inkwell" in (tmp_path / "blog.yaml").read_text(encoding="utf-8")
