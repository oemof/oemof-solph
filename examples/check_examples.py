import os
import subprocess
import tempfile
import warnings
import importlib
from datetime import datetime

import matplotlib
import nbformat
from termcolor import colored

try:
    from oemof.visio import ESGraphRenderer

    oemof_visio = True
except ImportError:
    oemof_visio = False

warnings.filterwarnings("ignore", "", UserWarning)
matplotlib.use("Agg")

stop_at_error = False  # If True script will stop if error is raised
exclude_notebooks = False
exclude_python_scripts = False
has_main_function = True
test_optimize = True


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


fullpath = os.path.dirname(__file__)
doc_path = os.path.join(os.path.dirname(fullpath), "docs", "_files")

checker = {}
number = 0

start_check = datetime.now()

for root, dirs, files in sorted(os.walk(fullpath)):
    if root != fullpath:
        for name in sorted(files):
            if name.endswith(".py"):
                number += 1
                module_name = name[:-3]
                try:
                    file_module = importlib.import_module(
                        f"{os.path.basename(root)}.{module_name}"
                    )
                    main = file_module.main
                    has_main_function = True
                except AttributeError:
                    print(
                        f"{os.path.basename(root)}.{name} does not have main() function"
                    )
                    has_main_function = False

                if stop_at_error is True:
                    es = main(optimize=test_optimize)
                    checker[name] = "okay"
                else:
                    try:
                        es = main(optimize=test_optimize)
                        checker[name] = "okay"
                    except Exception as e:
                        print(e)
                        if has_main_function is False:
                            checker[name] = "failed because no main() function"
                        else:
                            checker[name] = "failed"
                        es = None

                if es is not None and oemof_visio is True:
                    esgr = ESGraphRenderer(
                        es,
                        legend=False,
                        filepath=os.path.join(doc_path, f"{module_name}"),
                        img_format="svg",
                    )
                    esgr.render()


print("******* TEST RESULTS ***********************************")

print(
    "\n{0} examples tested in {1}.\n".format(
        number, datetime.now() - start_check
    )
)

f = 0
for k, v in checker.items():
    if "failed" in v:
        print(k, colored(v, "red"))
        f += 1
    else:
        print(k, colored(v, "green"))

print()
if f > 0:
    print("{0} of {1} examples failed!".format(f, number))
else:
    print("Congratulations! All examples are fine.")
