============
CAMP short-read-quality-control
============


.. image:: https://readthedocs.org/projects/camp-short-read-quality-control/badge/?version=latest
        :target: https://camp-short-read-quality-control.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/version-0.1.0-brightgreen


Overview
--------

This module is designed to function as both a standalone MAG short-read-quality-control pipeline as well as a component of the larger CAMP/CAP2 metagenome analysis pipeline. As such, it is both self-contained (ex. instructions included for the setup of a versioned environment, etc.), and seamlessly compatible with other CAMP modules (ex. ingests and spawns standardized input/output config files, etc.). 

The CAMP binning pipeline replicates the functionality of MetaWRAP (one of the original ensemble `binning methods <https://github.com/bxlab/metaWRAP>`_) with i) better dependency conflict management and ii) improved integration with new binning algorithms.

.. ..

 <!--- 
 Add description of your workflow's algorithmic contents 
 --->


Installation
------------

1. Clone repo from `github <https://github.com/b-tierney/camp_short-read-quality-control>_`. 

2. Set up the conda environment (contains, Snakemake) using ``configs/conda/camp_short-read-quality-control.yaml``. 

3. Make sure the installed pipeline works correctly. ``pytest`` only generates temporary outputs so no files should be created.
::
    cd camp_short-read-quality-control
    conda env create -f configs/conda/camp_short-read-quality-control.yaml
    conda activate camp_short-read-quality-control
    pytest .tests/unit/

Using the Module
----------------

**Input**: ``/path/to/samples.csv`` provided by the user.

**Output**: 1) An output config file summarizing 2) the module's outputs. 

- ``/path/to/work/dir/short-read-quality-control/final_reports/samples.csv`` for ingestion by the next module (ex. quality-checking)
.. ..

 <!--- 
 Add description of your workflow's output files 
 --->

**Structure**:
::
    └── workflow
        ├── Snakefile
        ├── short-read-quality-control.py
        ├── utils.py
        └── __init__.py
- ``workflow/short-read-quality-control.py``: Click-based CLI that wraps the ``snakemake`` and unit test generation commands for clean management of parameters, resources, and environment variables.
- ``workflow/Snakefile``: The ``snakemake`` pipeline. 
- ``workflow/utils.py``: 

1. Make your own ``samples.csv`` based on the template in ``configs/samples.csv``. Sample test data can be found in ``test_data/``.
    * ``samples.csv`` requires absolute paths to Illumina reads (currently, ``ingest_samples`` in ``workflow/utils.py`` expects FastQs) and de novo assembled contigs.  

2. Update the relevant parameters in ``configs/parameters.yaml``.

3. Update the computational resources available to the pipeline in ``resources/*.yaml`` where ``*`` is either 'slurm' or 'bash'. 

4. To run CAMP on the command line, use the following, where ``/path/to/work/dir`` is replaced with the absolute path of your chosen working directory, and ``/path/to/samples.csv`` is replaced with your copy of ``samples.csv``. 
::
    python /path/to/camp_short-read-quality-control/workflow/short-read-quality-control.py \
        -w /path/to/camp_short-read-quality-control/workflow/Snakefile \
        -d /path/to/work/dir \
        -s /path/to/samples.csv
- Note: This setup allows the main Snakefile to live outside of the work directory.

5. To run CAMP on a job submission cluster (for now, only Slurm is supported), use the following.
    * ``--slurm`` is an optional flag that submits all rules in the Snakemake pipeline as ``sbatch`` jobs. 
::
    sbatch -j jobname -e jobname.err.log -o jobname.out.log << "EOF"
    #!/bin/bash
    python /path/to/camp_short-read-quality-control/workflow/short-read-quality-control.py --slurm \
        -w /path/to/camp_short-read-quality-control/workflow/Snakefile \
        -d /path/to/work/dir \
        -s /path/to/samples.csv
    EOF

Extending the Module
--------------------

We love to see it! This module was partially envisioned as a dependable, prepackaged sandbox for developers to test their shiny new tools in. 

These instructions are meant for developers who have made a tool and want to integrate or demo its functionality as part of a standard short-read-quality-control workflow, or developers who want to integrate an existing short-read-quality-control tool. 

1. Write a module rule that wraps your tool and integrates its input and output into the pipeline. 
    * This is a great `Snakemake tutorial <https://bluegenes.github.io/hpc-snakemake-tips/>`_ for writing basic Snakemake rules.
    * If you're adding new tools from an existing YAML, use ``conda env update --file configs/conda/camp_short-read-quality-control.yaml --prune``.
2. Update the ``make_config`` in ``workflow/Snakefile`` rule to check for your tool's output files. Update ``samples.csv`` to document its output if downstream modules/tools are meant to ingest it. 
3. If applicable, update the default conda config using ``conda env export > config/conda/camp_short-read-quality-control.yaml`` with your tool and its dependencies. 
    - If there are dependency conflicts, make a new conda YAML under ``configs/conda`` and specify its usage in specific rules using the ``conda`` option (see ``first_rule`` for an example).
4. Add your tool's installation and running instructions to the module documentation and (if applicable) add the repo to your `Read the Docs account <https://readthedocs.org/>`_ + turn on the Read the Docs service hook.
5. Run the pipeline once through to make sure everything works using the test data in ``test_data/`` if appropriate, or your own appropriately-sized test data. Then, generate unit tests to ensure that others can sanity-check their installations.
::
    python /path/to/camp_short-read-quality-control/workflow/short-read-quality-control.py generate_unit_tests \
        -w /path/to/camp_short-read-quality-control/workflow/Snakefile \
        -d /path/to/work/dir \
        -s /path/to/samples.csv

6. Increment the version number of the modular pipeline.
::
    bump2version --allow-dirty --commit --tag major workflow/__init__.py \
                 --current-version A.C.E --new-version B.D.F

7. If you want your tool integrated into the main CAP2/CAMP pipeline, send a pull request and we'll have a look at it ASAP! 
    - Please make it clear what your tool intends to do by including a summary in the commit/pull request (ex. "Release X.Y.Z: Integration of tool A, which does B to C and outputs D").

.. ..

 <!--- 
 Bugs
 ----
 Put known ongoing problems here
 --->


