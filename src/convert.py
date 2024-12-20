from pathlib import Path
import re
import jupytext


def is_solution(content: str):
    pattern = r"#\s*solution"
    return bool(re.search(pattern, content, re.IGNORECASE))


def remove_solution_content(notebook):
    for cell in notebook["cells"]:
        if is_solution(cell["source"]):
            cell["source"] = ""
    return notebook


def clean_filename(fpath: Path):
    pattern = r"solutions?\b"
    stem = fpath.stem
    stem = re.sub(pattern, "", stem, flags=re.IGNORECASE)  # remove solution(s)
    stem = re.sub(r"[-_\s]+$", "", stem)  # remove trailing space, underscore, dash
    return fpath.parent / (stem + fpath.suffix)


def was_created_by_jupytext(fpath: Path, n_lines: int = 20) -> bool:
    with open(fpath, "r", encoding="utf-8") as f:
        header = "".join(f.readline() for _ in range(n_lines))
        jupytext_pattern = r"#\s*jupytext:"
        return bool(re.search(jupytext_pattern, header))


def python_to_notebook(fpath: Path, remove_solutions: bool = False):
    fpath = Path(fpath)
    if not fpath.exists():
        raise FileNotFoundError(f"File not found: {fpath}")
    print(fpath.suffix)
    if not fpath.suffix == ".py":
        raise ValueError("Input file must be a Python file (.py)")

    if was_created_by_jupytext(fpath):
        notebook = jupytext.read(fpath)
        if remove_solutions:
            notebook = remove_solution_content(notebook)
            fpath = clean_filename(fpath)
        jupytext.write(notebook, fpath.with_suffix(".ipynb"))
        print(f"Successfully converted {fpath} to {fpath.with_suffix('.ipynb')}")
    else:
        print(f"Skipping {fpath} because it is not a Jupytext notebook")


def notebook_to_python(fpath: Path, remove_solutions: bool = False):
    fpath = Path(fpath)
    if not fpath.exists():
        raise FileNotFoundError(f"File not found: {fpath}")
    if not fpath.suffix == ".ipynb":
        raise ValueError("Input file must be an IPython notebook (.ipynb)")
    notebook = jupytext.read(fpath)
    if remove_solutions:
        notebook = remove_solution_content(notebook)
        fpath = clean_filename(fpath)
    jupytext.write(notebook, fpath.with_suffix(".py"), fmt="py:percent")
    print(f"Successfully converted {fpath} to {fpath.with_suffix('.py')}")


def find_files(root_path: Path, extension: str, exclude_patterns: list = []) -> list:
    notebooks = []
    for f in root_path.rglob("*" + extension):
        if not any(exclude in str(f) for exclude in exclude_patterns):
            notebooks.append(f)
    return notebooks


def check_format(format_from: str, format_to: str) -> tuple[str, str]:

    FORMAT_MAPPING = {
        "python": "py",
        ".py": "py",
        "py": "py",
        "notebook": "ipynb",
        ".ipynb": "ipynb",
        "ipynb": "ipynb",
    }

    def normalize_format(fmt: str) -> str:
        try:
            return FORMAT_MAPPING[fmt.lower()]
        except KeyError:
            raise ValueError(f"Can't find suffix for file format {fmt}")

    return normalize_format(format_from), normalize_format(format_to)


def read_gitignore(root_path: Path):
    with open(root_path / ".gitignore", "r") as f:
        lines = [line.strip() for line in f.readlines()]
        patterns = [line for line in lines if line and not line.startswith("#")]
    return patterns


def convert_notebooks_in_directory(
    root_path: str,
    format_from: str,
    format_to: str,
    exclude_patterns: list = [],
    remove_solutions: bool = False,
) -> None:

    format_from, format_to = check_format(format_from, format_to)
    files = find_files(Path(root_path), format_from, exclude_patterns)

    if not files:
        raise FileNotFoundError(f"No {format_from} files found in {root_path}")

    for f in files:
        if format_from == "py" and format_to == "ipynb":
            python_to_notebook(f, remove_solutions)
        elif format_from == "ipynb" and format_to == "py":
            notebook_to_python(f, remove_solutions)
