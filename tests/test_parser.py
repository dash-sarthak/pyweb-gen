"""Argument parser behavior: command routing and option defaults."""

from pyweb_gen.parser import build_parser


def test_serve_command_defaults_to_port_8000() -> None:
    args = build_parser().parse_args(["serve"])

    assert args.port == 8000


def test_serve_command_accepts_custom_port() -> None:
    args = build_parser().parse_args(["serve", "--port", "9000"])

    assert args.port == 9000
