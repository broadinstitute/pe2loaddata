import click.testing
import src.pe2loaddata.__main__


def test_foo():
    runner = click.testing.CliRunner()

    command = src.pe2loaddata.__main__.main

    result = runner.invoke(command, [
        "tests/data/config.yml",
        "--index-file",
        "tests/data/Index.idx.xml"
    ])

    assert result.exit_code == 0
