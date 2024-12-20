# Notebook Converter

Jupyter notebooks are great but, because they keep track of how often each cell has been executed, they are not well suited for version control.
A simple solution is to convert the notebooks to plain Python files and tracking only those.
This is what this program is for: it uses Jupytext to convert all .ipynb files within a directory and all of its subdirectories to .py and vice versa.

## Installation

Simply install via pip
```
pip install git+https://github.com/OleBialas/Python-Notebook-Converter
```

## Usage

Use the `-f/--format_from` and `t/--format_to` arguments to specify the direction.

To convert all notebooks within the current folder and all subdirectories:

```sh
notebook-converter . -f notebook -t python
```

To do the opposite conversion from python to notebooks:

```sh
notebook-converter . -f python -t notebook
```

Note that this will only convert Python files containing a header that indicates the file was created by Jupytext.

We can also exclude files and folders using the `-e/--exclude`. For example, if the directory contains a `.venv` folder that contains a virtual environment with Python libraries that we want to ignore:

```sh
notebook-converter . -f notebook -t python --exclude .venv
```

The `--exclude` argument can be used multiple times to exclude several files or folders.

Finally, one can remove solutions from the output notebook or Python file by including the `--remove-solutions` flag. This will remove the content of each cell that contains the comment `# Solution(s)` and remove `solution(s)` from the output file name:

```sh
notebook-converter . -f notebook -t python --remove-solutions
```