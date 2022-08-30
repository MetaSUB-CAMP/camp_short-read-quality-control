import os
import sys

import subprocess as sp
from tempfile import TemporaryDirectory
import shutil
from pathlib import Path, PurePosixPath

sys.path.insert(0, os.path.dirname(__file__))

import common


def test_multiqc():

    with TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir) / "workdir"
        data_path = PurePosixPath("/pbtech_mounts/homes064/lam4003/bin/camp_short-read-quality-control/.tests/unit/multiqc/data")
        expected_path = PurePosixPath("/pbtech_mounts/homes064/lam4003/bin/camp_short-read-quality-control/.tests/unit/multiqc/expected")

        # Copy data to the temporary workdir.
        shutil.copytree(data_path, workdir)

        # dbg
        print("test_out/short_read_qc/3_summary/multiqc_report.html", file=sys.stderr)

        # Run the test job.
        sp.check_output([
            "python",
            "-m",
            "snakemake", 
            "test_out/short_read_qc/3_summary/multiqc_report.html",
            "-f", 
            "-j1",
            "--keep-target-files",
            "--configfile",
            /pbtech_mounts/homes064/lam4003/bin/camp_short-read-quality-control/configs/parameters.yaml
            /pbtech_mounts/homes064/lam4003/bin/camp_short-read-quality-control/configs/resources.yaml
    
            "--use-conda",
            "--directory",
            workdir,
        ])

        # Check the output byte by byte using cmp.
        # To modify this behavior, you can inherit from common.OutputChecker in here
        # and overwrite the method `compare_files(generated_file, expected_file), 
        # also see common.py.
        common.OutputChecker(data_path, expected_path, workdir).check()
