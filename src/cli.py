import argparse
from convert import convert_notebooks_in_directory


def main():

    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebooks to Python scripts recursively"
    )
    parser.add_argument("root", help="Root directory containing notebooks", default=".")
    parser.add_argument(
        "-f", "--format_from", help="Format to convert from", default="ipynb"
    )
    parser.add_argument("-t", "--format_to", help="Format to convert to", default="py")
    parser.add_argument(
        "-e",
        "--exclude",
        help="Patterns to exclude (can be used multiple times)",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--remove-solutions",
        help="Remove all cell content tagged with '# Solution' and remove 'solution' from written files names",
        default=False,
        action="store_true",
    )

    args = parser.parse_args()

    convert_notebooks_in_directory(
        args.root, args.format_from, args.format_to, args.exclude, args.remove_solutions
    )


if __name__ == "__main__":
    main()
