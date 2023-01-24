import os
import subprocess
import tempfile
import warnings
from datetime import datetime

import matplotlib
import nbformat
from matplotlib import pyplot as plt
from termcolor import colored

warnings.filterwarnings("ignore", "", UserWarning)
matplotlib.use("Agg")

stop_at_error = False  # If True script will stop if error is raised
exclude_notebooks = False
exclude_python_scripts = False


def notebook_run(path):
    """
    Execute a notebook via nbconvert and collect output.
    Returns (parsed nb object, execution errors)
    """
    dirname, __ = os.path.split(path)
    os.chdir(dirname)
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = [
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--ExecutePreprocessor.timeout=60",
            "--output",
            fout.name,
            path,
        ]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [
        output
        for cell in nb.cells
        if "outputs" in cell
        for output in cell["outputs"]
        if output.output_type == "error"
    ]

    return nb, errors


fullpath = os.path.join(os.getcwd())

checker = {}
number = 0

start_check = datetime.now()

for root, dirs, files in sorted(os.walk(fullpath)):
    for name in sorted(files):
        if (
            name[-3:] == ".py"
            and not exclude_python_scripts
            and not name == "check_examples.py"
        ):
            fn = os.path.join(root, name)
            os.chdir(root)
            number += 1
            if stop_at_error is True:
                print(fn)
                exec(open(fn).read())
                checker[name] = "okay"
            else:
                try:
                    exec(open(fn).read())
                    checker[name] = "okay"
                except Exception as e:
                    print(e)
                    checker[name] = "failed"
        elif name[-6:] == ".ipynb" and not exclude_notebooks:
            fn = os.path.join(root, name)
            os.chdir(root)
            number += 1
            if stop_at_error is True:
                print(fn)
                notebook_run(fn)
                checker[name] = "okay"
            else:
                try:
                    notebook_run(fn)
                    checker[name] = "okay"
                except Exception as e:
                    print(e)
                    checker[name] = "failed"
        plt.close()

print("******* TEST RESULTS ***********************************")

print(
    "\n{0} examples tested in {1}.\n".format(
        number, datetime.now() - start_check
    )
)

f = 0
for k, v in checker.items():
    if v == "failed":
        print(k, colored(v, "red"))
        f += 1
    else:
        print(k, colored(v, "green"))

print()
if f > 0:
    print("{0} of {1} examples failed!".format(f, number))
else:
    print("Congratulations! All examples are fine.")
