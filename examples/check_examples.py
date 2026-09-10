import importlib
import subprocess
import tempfile
import warnings
from datetime import datetime
from pathlib import Path

import matplotlib
import nbformat
import pandas as pd
from termcolor import colored

try:
    import graphviz  # noqa: F401
    from oemof.visio import ESGraphRenderer

    oemof_visio = True
except ImportError:
    ESGraphRenderer = None
    oemof_visio = False

warnings.filterwarnings("ignore", "", UserWarning)
matplotlib.use("Agg")


def notebook_run(path):
    """
    Execute a notebook via nbconvert and collect output.
    Returns (parsed nb object, execution errors)
    """
    path.parent.cwd()

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


def check_single_example(file, solver, doc_path, test_optimize, stop_at_error):
    module_name = file.stem
    examplename = f"{file.parent.name}.{file.name}"
    print(f"Checking example {examplename} with {solver}.")
    try:
        file_module = importlib.import_module(
            f"{file.parent.name}.{module_name}"
        )
        main = file_module.main
    except AttributeError:
        print(f"{file.name}.{examplename} does not have main() function")
        check = "failed because no main() function"
        return check

    if stop_at_error:
        es = main(optimize=test_optimize, solver=solver)
        check = "okay"
    else:
        try:
            es = main(optimize=test_optimize, solver=solver)
            check = "okay"
        except Exception as e:
            print(e)
            check = "failed"
            es = None

    if es is not None and oemof_visio is True:
        esgr = ESGraphRenderer(
            es,
            legend=False,
            filepath=str(Path(doc_path, f"{module_name}")),
            img_format="svg",
        )
        esgr.render()
    return check


def check_all_examples(solvers, test_optimize, stop_at_error):
    fullpath = Path(__file__).parent
    doc_path = Path(fullpath.parent, "docs", "_files")

    checker = {}
    number = 0

    start_check = datetime.now()
    for used_solver in solvers:
        checker[used_solver] = {}
        for f in sorted(fullpath.rglob("*.py")):
            if f.name != "check_examples.py":
                number += 1
                checker[used_solver][f"{f.parent.name}.{f.name}"] = (
                    check_single_example(
                        f, used_solver, doc_path, test_optimize, stop_at_error
                    )
                )

    print("******* TEST RESULTS ***********************************")

    print(
        "\n{0} examples tested in {1}.\n".format(
            number, datetime.now() - start_check
        )
    )

    table = pd.DataFrame(index=solvers, columns=["total", "failed"])

    for used_solver, checker in checker.items():
        print(f"******* TEST RESULTS - {used_solver} ************************")
        failed = 0
        total = 0
        for k, v in checker.items():
            total += 1
            if "failed" in v:
                print(k, colored(v, "red"))
                failed += 1
            else:
                print(k, colored(v, "green"))

        print()
        if failed > 0:
            print(f"{failed} of {total} examples failed with {used_solver}!")
        else:
            print(
                f"Congratulations! All examples are fine with {used_solver}!."
            )
        table.loc[used_solver, "total"] = total
        table.loc[used_solver, "failed"] = failed

    print("******* TEST RESULTS - summary ***********************************")

    print(table)


def check_file(directory, name, solver, test_optimize, stop_at_error):
    base = Path(__file__).parent
    doc_path = Path(base.parent, "docs", "_files")
    file = Path(base, directory, name)
    return check_single_example(
        file, solver, doc_path, test_optimize, stop_at_error
    )


if __name__ == "__main__":
    set_stop_at_error = False  # If True script will stop if error is raised
    set_test_optimize = True
    set_solvers = ["cbc", "highs"]
    check_all_examples(set_solvers, set_test_optimize, set_stop_at_error)
