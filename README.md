# CAMP: Short-Read Quality Control

Overview
--------

This module runs a series of standard quality-control steps on metagenomic short read data. It is both self-contained (ex. instructions included for the setup of a versioned environment, etc.), and compatible with other CAMP modules (ex. ingests and spawns standardized input/output config files, etc.). 

There are two filtration steps in the module- i) for general poor quality (Phred scores, length, Ns, adapters, polyG/X) and ii) for host reads- followed by a sequencing error correction step. The properties of the QC-ed FastQs are summarized in aggregate by a MultiQC report. 

Approach
--------
<INSERT PIPELINE IMAGE>

Installation
------------

1. Clone repo from `Github tutorial <https://github.com/MetaSUB-CAMP/camp_short-read-quality-control>`_.

2. Set up the conda environment using ``configs/conda/short-read-quality-control.yaml``. 

3. If you don't already have Trimmomatic installed through conda or as a standalone JAR, download its precompiled binary. You'll need to update the path to said binary in the paramters.yaml file.
```
git clone https://github.com/usadellab/Trimmomatic.git
```
4. Make sure the installed pipeline works correctly. ``pytest`` only generates temporary outputs so no files should be created.
```
cd camp_short-read-quality-control
conda env create -f configs/conda/short-read-quality-control.yaml
conda activate short-read-quality-control
pytest .tests/unit/
```    
      
5. Download and untar the relevant databases -- make sure to update the path to these files in the ``parameters.yaml``

```
wget https://s3.us-east-1.wasabisys.com/camp-databases/v0.1.1/human_genome_bt2idx/GRCh38_noalt_as.tar.gz; tar -zxvf GRCh38_noalt_as.tar.gz
```

Quickstart
----------

Running each CAMP module takes the same three steps, listed below.

1. As with all CAMP modules, update the parameters.yaml file:

<TABLE OF PARAMETERS AND DESCRIPTIONS>

2. Generate your samples.csv file in the following format:

<SAMPLES.CSV FORMAT>

3. Deploy!
::
<SNAKEMAKE COMMAND>

Module details
-------------------------------

**Input**: ``/path/to/samples.csv`` provided by the user.

**Output**: 1) An output config file summarizing the locations of the error-corrected FastQs, 2) the MultiQC report summarizing the properties for the QC-ed FastQ, and 3) summary statistics about the dataset after each error correction step indicating how many reads and/or bases were pruned

- ``/path/to/work/dir/short_read_qc/final_reports/samples.csv`` for ingestion by the next module

- ``/path/to/work/dir/short_read_qc/final_reports/*_multiqc_report.html``, where ``*`` is 'pre' or 'post'-module

- ``/path/to/work/dir/short_read_qc/final_reports/read_stats.csv``


**Structure**:
```
└── workflow
    ├── Snakefile
    ├── short-read-quality-control.py
    ├── utils.py
    └── __init__.py
```
- ``workflow/short-read-quality-control.py``: Click-based CLI that wraps the ``snakemake`` and unit test generation commands for clean management of parameters, resources, and environment variables.
- ``workflow/Snakefile``: The ``snakemake`` pipeline. 
- ``workflow/utils.py``: Sample ingestion and work directory setup functions, and other utility functions used in the pipeline and the CLI.

1. Make your own ``samples.csv`` based on the template in ``configs/samples.csv``. Sample test data can be found in ``test_data/``.
    - ``ingest_samples`` in ``workflow/utils.py`` expects Illumina reads in FastQ (may be gzipped) form and de novo assembled contigs in FastA form
    - ``samples.csv`` requires either absolute paths or paths relative to the directory that the module is being run in

2. Download the appropriate host reference genome(s) and make a Bowtie2 index using ``bowtie2-build /path/to/host_reference.fa /path/to/host_reference``, and add the prefix ``/path/to/host_reference`` to ``parameters.yaml``.

3. Update the computational resources available to the pipeline in ``resources.yaml``. 

Command line deployment
-----------------------
To run CAMP on the command line, use the following, where ``/path/to/work/dir`` is replaced with the absolute path of your chosen working directory, and ``/path/to/samples.csv`` is replaced with your copy of ``samples.csv``. 
    - The default number of cores available to Snakemake is 1 which is enough for test data, but should probably be adjusted to 10+ for a real dataset.
    - Relative or absolute paths to the Snakefile and/or the working directory (if you're running elsewhere) are accepted!
```
python /path/to/camp_short-read-quality-control/workflow/short-read-quality-control.py -d /path/to/work/dir -s /path/to/samples.csv
```

* Note: This setup allows the main Snakefile to live outside of the work directory.

Running on a slurm cluster
--------------------------
To run CAMP on a job submission cluster (for now, only Slurm is supported), use the following.
    - ``--slurm`` is an optional flag that submits all rules in the Snakemake pipeline as ``sbatch`` jobs. 
    - In Slurm mode, the ``-c`` flag refers to the maximum number of ``sbatch`` jobs submitted in parallel, **not** the pool of cores available to run the jobs. Each job will request the number of cores specified by threads in ``configs/resources/slurm.yaml``.
```
    sbatch -J jobname -o jobname.log << "EOF"
    #!/bin/bash
    python /path/to/camp_short-read-quality-control/workflow/short-read-quality-control.py --slurm \
        (-c max_number_of_parallel_jobs_submitted) \
        -d /path/to/work/dir \
        -s /path/to/samples.csv
    EOF
```
Quality-checking processed FastQs
----------------------------------

To quality-check the processed FastQs, download and compare the collated MultiQC reports, which can be found at ``/path/to/work/dir/short_read_qc/final_reports/*_multiqc_report/html``. Multiple rounds of preprocessing may be needed to fully get rid of low-quality bases, adapters, and duplicated sequences. 
    - For example, the dataset I worked with required an additional round of ``fastp`` to trim 10 low-quality bases from the 5' and 4 low-quality bases from the 3' end respectively. 
    - I recommend creating a new directory, which I've called ``/path/to/work/dir/short_read_qc/5_retrimming`` and placing reprocessed reads inside them. 
    - Afterwards, I reran FastQC and MultiQC and collated summary statistics (ex. numbers of reads, etc.) from the reprocessed datasets manually. I also updated the location of the reprocessed reads in ``/path/to/work/dir/short_read_qc/final_reports/samples.csv`` to ``/path/to/work/dir/short_read_qc/5_retrimming``.


Dependencies
------------
<LIST ALL DEPENDENCIES>

Credits
-------

* This package was created with `Cookiecutter <https://github.com/cookiecutter/cookiecutter>`_ as a simplified version of the `project template <https://github.com/audreyr/cookiecutter-pypackage>`_.
* Free software: MIT
* Documentation: https://short-read-quality-control.readthedocs.io. 


