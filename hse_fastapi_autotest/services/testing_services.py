__all__ = ("run_pytest", "flake8_html_report",
           "pylint_json_report", "report_junk_folders")

import json
import logging
import os
import subprocess
from pathlib import Path
from typing import List

from hse_fastapi_autotest import PROJECT_ROOT

logger = logging.getLogger(__name__)


def run_pytest(repo_url: str, project_destination: Path, html_output_dir: Path):
    """
    Run pytest with specified parameters.

    Parameters:
    - repo_url (str): The URL of the repository.
    - project_destination (Path): The path to the project destination.
    - html_output_dir (Path): The directory where the HTML test result will be saved.

    Returns:
    None
    """
    pytest_args = [
        "pytest",
        "-v",
        PROJECT_ROOT / "hse_fastapi_autotest",
        f"--repo_url={repo_url}",
        f"--tested_app_dir={project_destination}",
        f"--html={html_output_dir}/e2e_test_result.html",
        "--self-contained-html",
    ]
    result = subprocess.run(pytest_args, check=False)
    print(result.stdout)


def flake8_html_report(
    directory_path: Path = PROJECT_ROOT / "temp_repos",
    output_directory: Path = PROJECT_ROOT / "temp_repos",
) -> None:
    """
    Run flake8 on the specified directory and generate an HTML report.

    Parameters:
    - directory_path (Path): The path to the directory to be analyzed by flake8.
    - output_directory (Path): The directory where the HTML report will be saved.

    Returns:
    None

    """
    try:
        result = subprocess.run(
            [
                "flake8",
                directory_path,
                "--format=html",
                f"--htmldir={output_directory}",
            ],
            text=True,
            check=False,
        )

        if result.returncode == 0:
            logger.info("flake8 passed without any issues.")
        else:
            logger.info(
                f"flake8 found issues. HTML report generated in '{output_directory}'"
            )

    except subprocess.CalledProcessError as e:
        print(f"Error running flake8: {e}")


def pylint_json_report(
    directory_path: Path = PROJECT_ROOT / "hse_mlops_hw",
    output_directory: Path = PROJECT_ROOT / "reports/hse_mlops_hw/pylint",
) -> None:
    """
    Run pylint on the specified directory and generate a JSON report.

    Parameters:
    - directory_path (Path): The path to the directory to be analyzed by pylint.
    - output_directory (Path): The directory where the JSON report will be saved.

    Returns:
    None
    """
    try:
        output_directory.mkdir(parents=True, exist_ok=True)

        pylint_command = ["pylint", str(directory_path), "--output-format=json"]
        pylint_process = subprocess.run(
            pylint_command, capture_output=True, text=True, check=False
        )

        print(pylint_process.stdout)

        if pylint_process.returncode == 0:
            print("pylint passed without any issues.")
        else:
            try:
                json_output = json.loads(pylint_process.stdout)
            except json.JSONDecodeError:
                print("Error: pylint did not produce valid JSON output.")
                return

            json_report_path = output_directory / "report.json"
            with open(json_report_path, "w", encoding="utf-8") as json_file:
                json.dump(json_output, json_file, indent=2)

            print(f"pylint found issues. JSON report saved to '{json_report_path}'")

    except subprocess.CalledProcessError as e:
        print(f"Error running pylint: {e}")


def report_junk_folders(
    directory_path: Path, junk_dirs: List[str] = (".idea",)
) -> None:
    """
    Search for specified junk folders within the given directory and its subdirectories,
    and generate a report if any are found.

    Parameters:
    - directory_path (Path): The path to the directory to be analyzed.
    - junk_dirs (List[str]): List of junk folder names to search for.

    Returns:
    None
    """
    try:
        junk_report = []

        for root, dirs, _ in os.walk(directory_path):
            for junk_path in junk_dirs:
                if junk_path in dirs:
                    junk_report.append(f"Junk folder '{junk_path}' found in '{root}'")

        if junk_report:
            junk_folder_path = directory_path / "junk_report"
            junk_folder_path.mkdir(exist_ok=True)

            report_file_path = junk_folder_path / "junk_report.txt"
            with open(report_file_path, "w", encoding="utf-8") as report_file:
                for report_line in junk_report:
                    report_file.write(report_line + "\n")

            print(f"Junk report saved to '{report_file_path}'")
        else:
            print("No junk folders found in the repository.")

    except subprocess.CalledProcessError as e:
        print(f"Error checking for useless directories : {e}")
