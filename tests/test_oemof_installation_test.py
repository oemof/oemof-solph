import subprocess


def test_oemof_installation_test_runs_without_errors():
    completed_process = subprocess.run(["oemof_installation_test"])
    assert completed_process.returncode == 0
