=====
Usage
=====

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
