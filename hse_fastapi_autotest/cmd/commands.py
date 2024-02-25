import argparse
import logging
from pathlib import Path

from hse_fastapi_autotest.services.helpers.utils import ensure_path, extract_repo_name
from hse_fastapi_autotest.services.service_layer import (
    find_and_report_junk_folders,
    run_flake8_and_generate_report,
    run_pylint_and_generate_json_report,
    run_pytest,
)

logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser(
        description=(
            "Fast api automation tool for testing. Package is "
            "aimed to test apps based on a given openapi schema."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--repo_url",
        default="https://github.com/AnyNoth1ng/PEN_HSE_FastApi.git",
        help="git repository containing fastapi project url e.g. https://github.com ",
    )

    parser.add_argument(
        "--test_output",
        default=Path("/tmp/tested_repos"),
        help="Output directory where generated report will be stored "
        "alongside with projest.",
    )

    return parser.parse_args()


def run_tests() -> None:
    """Run pytest with test directory, repo URL, and HTML output directory arguments."""

    args = get_args()

    repo_name = extract_repo_name(args.repo_url)
    project_destination = ensure_path(args.test_output)

    html_output_dir = project_destination / repo_name
    lint_test_dir = project_destination / repo_name

    run_pytest(
        repo_url=args.repo_url,
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


if __name__ == "__main__":
    run_tests()