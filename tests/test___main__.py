import os
import click.testing
import src.pe2loaddata.__main__


def test_with_file(test_files):
    runner = click.testing.CliRunner()

    command = src.pe2loaddata.__main__.main
    result = runner.invoke(command, [
        test_files["config_file"],
        "--index-file",
        test_files["index_file"],
        "test.csv"

    ])

    assert result.exit_code == 0

    os.remove("test.csv")

def test_with_directory(test_files):
    runner = click.testing.CliRunner()

    command = src.pe2loaddata.__main__.main

    result = runner.invoke(command, [
        test_files["config_file"],
        "--index-directory",
        test_files["index_directory"],
        "test.csv"
    ])
    assert result.exit_code == 0

    os.remove("test.csv")

def test_with_import(test_files):
    assert not os.path.exists("test.csv")
    src.pe2loaddata.__main__.headless(test_files["config_file"],"test.csv",index_file=test_files["index_file"],index_directory=test_files["index_directory"])
    assert os.path.exists("test.csv")
    os.remove("test.csv")