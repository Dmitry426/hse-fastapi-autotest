import json
import logging
import os

import subprocess
from pathlib import Path

from hse_fastapi_autotest.services.helpers.utils import ensure_path, extract_repo_name
from hse_fastapi_autotest import PROJECT_ROOT

logger = logging.getLogger(__name__)

JUNK_PATHS = [".idea"]


def run_tests(
    repo_url: str = "https://github.com/AnyNoth1ng/PEN_HSE_FastApi.git",
    repo_path: str = PROJECT_ROOT / "temp_repos",
):
    """Run pytest with test directory, repo URL, and HTML output directory arguments."""
    repo_name = extract_repo_name(repo_url)
    project_destination = ensure_path(repo_path)

    html_output_dir = project_destination / repo_name
    lint_test_dir = project_destination / repo_name

    run_pytest(
        repo_url=repo_url,
        project_destination=project_destination,
        html_output_dir=html_output_dir,
    )

    run_flake8_and_generate_report(
        directory_path=lint_test_dir, output_directory=html_output_dir / "flake8_report"
    )

    run_pylint_and_generate_json_report(
        directory_path=lint_test_dir, output_directory=html_output_dir / "pylint_report"
    )

    find_and_report_junk_folders(directory_path=lint_test_dir)


def run_pytest(repo_url: str, project_destination: Path, html_output_dir: Path):
    """Run pytest with test directory, repo URL"""
    pytest_args = [
        "pytest",
        "-v",
        PROJECT_ROOT / "hse_fastapi_autotest",
        f"--repo_url={repo_url}",
        f"--tested_app_dir={project_destination}",
        f"--html={html_output_dir}/e2e_test_result.html",
        "--self-contained-html",
    ]
    result = subprocess.run(pytest_args)
    print(result.stdout)


def run_flake8_and_generate_report(
    directory_path: Path = PROJECT_ROOT / "temp_repos",
    output_directory: Path = PROJECT_ROOT / "temp_repos",
):
    try:
        result = subprocess.run(
            [
                "flake8",
                directory_path,
                "--format=html",
                f"--htmldir={output_directory}",
            ],
            text=True,
        )

        if result.returncode == 0:
            logger.info("flake8 passed without any issues.")
        else:
            logger.info(
                f"flake8 found issues. HTML report generated in '{output_directory}'"
            )

    except Exception as e:
        logger.info(f"Error running flake8: {e}")


def run_pylint_and_generate_json_report(
    directory_path: Path = PROJECT_ROOT / "hse_mlops_hw",
    output_directory: Path = PROJECT_ROOT / "reports/hse_mlops_hw/pylint",
):
    try:
        output_directory.mkdir(parents=True, exist_ok=True)

        pylint_command = ["pylint", str(directory_path), "--output-format=json"]
        pylint_process = subprocess.run(pylint_command, capture_output=True, text=True)

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
            with open(json_report_path, "w") as json_file:
                json.dump(json_output, json_file, indent=2)

            print(f"pylint found issues. JSON report saved to '{json_report_path}'")

    except subprocess.CalledProcessError as e:
        print(f"Error running pylint: {e}")


def find_and_report_junk_folders(directory_path: Path):
    try:

        junk_report = []

        for root, dirs, files in os.walk(directory_path):
            for junk_path in JUNK_PATHS:
                if junk_path in dirs:
                    junk_report.append(f"Junk folder '{junk_path}' found in '{root}'")

        if junk_report:
            junk_folder_path = directory_path / "junk_report"
            junk_folder_path.mkdir(exist_ok=True)

            report_file_path = junk_folder_path / "junk_report.txt"
            with open(report_file_path, 'w') as report_file:
                for report_line in junk_report:
                    report_file.write(report_line + '\n')

            print(f"Junk report saved to '{report_file_path}'")
        else:
            print("No junk folders found in the repository.")

    except Exception as e:
        print(f"Error during the analysis: {e}")


if __name__ == "__main__":
    run_tests()
