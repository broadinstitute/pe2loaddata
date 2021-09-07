import os
import click.testing
import src.pe2loaddata.__main__


def test_with_file():
    runner = click.testing.CliRunner()

    command = src.pe2loaddata.__main__.main

    result = runner.invoke(command, [
        "tests/data/config.yml",
        "--index-file",
        "tests/data/images/Index.idx.xml",
        "test.csv"

    ])

    assert result.exit_code == 0

    os.remove("test.csv")

def test_with_directory():
    runner = click.testing.CliRunner()

    command = src.pe2loaddata.__main__.main

    result = runner.invoke(command, [
        "tests/data/config.yml",
        "--index-directory",
        "tests/data/images/",
        "test.csv"
    ])
    assert result.exit_code == 0

    os.remove("test.csv")

def test_with_import():
    assert not os.path.exists("test.csv")
    src.pe2loaddata.__main__.headless("tests/data/config.yml","test.csv",index_file="tests/data/images/Index.idx.xml",index_directory=os.curdir)
    assert os.path.exists("test.csv")
    os.remove("test.csv")