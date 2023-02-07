============
CAMP Short-Read Quality Control
============


.. image:: https://readthedocs.org/projects/camp-short-read-quality-control/badge/?version=latest
        :target: https://camp-short-read-quality-control.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/version-0.4.1-brightgreen


Overview
--------

This module is designed to function as both a standalone MAG short-read quality control pipeline as well as a component of the larger CAMP metagenome analysis pipeline. As such, it is both self-contained (ex. instructions included for the setup of a versioned environment, etc.), and seamlessly compatible with other CAMP modules (ex. ingests and spawns standardized input/output config files, etc.). 

There are two filtration steps in the module- i) for general poor quality (Phred scores, length, Ns, adapters, polyG/X) and ii) for host reads- followed by a sequencing error correction step. The properties of the QC-ed FastQs are summarized in aggregate by a MultiQC report. 

Installation
------------

1. Clone repo from `Github tutorial <https://github.com/MetaSUB-CAMP/camp_short-read-quality-control>`_.

2. Set up the conda environment using ``configs/conda/short-read-quality-control.yaml``. 

3. If you don't already have Trimmomatic installed through conda or as a standalone JAR, do the following:
::
    wget https://github.com/usadellab/Trimmomatic/files/5854859/Trimmomatic-0.39.zip

4. Download the appropriate host reference genome(s) and make a Bowtie2 index using ``bowtie2-build /path/to/host_reference.fa /path/to/host_reference``, and add the prefix ``/path/to/host_reference`` to ``parameters.yaml``.
    - For example, I downloaded the latest major release of the human reference genome.
::
    cd Databases/GRCh38_28122022/
    wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/#:~:text=GCA_000001405.15_GRCh38_genomic.fna.gz
    bowtie2-build --threads 20 GCA_000001405.15_GRCh38_genomic.fna.gz GCA_000001405.15_GRCh38_genomic

5. Update the locations of the test datasets in ``samples.csv``, and the relevant parameters in ``test_data/parameters`` and ``configs/parameters.yaml``.

6. Make sure the installed pipeline works correctly. 
::
    # Create and activate conda environment 
    cd camp_short-read-quality-control
    conda env create -f configs/conda/short-read-quality-control.yaml
    conda activate short-read-quality-control
    
    # Run tests on the included sample dataset
    python /path/to/camp_short-read-quality-control/workflow/short-read-quality-control.py test


Using the Module
----------------

**Input**: ``/path/to/samples.csv`` provided by the user.

**Output**: 1) An output config file summarizing the locations of the error-corrected FastQs, 2) the MultiQC report summarizing the properties for the QC-ed FastQ, and 3) summary statistics about the dataset after each error correction step indicating how many reads and/or bases were pruned. For more information, see the demo test output directory in ``test_data/test_out``. 

- ``/path/to/work/dir/short_read_qc/final_reports/samples.csv`` for ingestion by the next module

- ``/path/to/work/dir/short_read_qc/final_reports/*_multiqc_report.html``, where ``*`` is 'pre' or 'post'-module

- ``/path/to/work/dir/short_read_qc/final_reports/read_stats.csv``


**Structure**:
::
    └── workflow
        ├── Snakefile
        ├── short-read-quality-control.py
        ├── utils.py
        └── __init__.py
- ``workflow/short-read-quality-control.py``: Click-based CLI that wraps the ``snakemake`` and other commands for clean management of parameters, resources, and environment variables.
- ``workflow/Snakefile``: The ``snakemake`` pipeline. 
- ``workflow/utils.py``: Sample ingestion and work directory setup functions, and other utility functions used in the pipeline and the CLI.

1. Make your own ``samples.csv`` based on the template in ``configs/samples.csv``.
    - ``ingest_samples`` in ``workflow/utils.py`` expects Illumina reads in FastQ (may be gzipped) form and de novo assembled contigs in FastA form
    - ``samples.csv`` requires either absolute paths or paths relative to the directory that the module is being run in

2. Update the computational resources available to the pipeline in ``resources.yaml``. 

3. To run CAMP on the command line, use the following, where ``/path/to/work/dir`` is replaced with the absolute path of your chosen working directory, and ``/path/to/samples.csv`` is replaced with your copy of ``samples.csv``. 
    - The default number of cores available to Snakemake is 1 which is enough for test data, but should probably be adjusted to 10+ for a real dataset.
    - Relative or absolute paths to the Snakefile and/or the working directory (if you're running elsewhere) are accepted!
::
    python /path/to/camp_short-read-quality-control/workflow/short-read-quality-control.py \
        (-c number_of_cores_allocated) \
        -d /path/to/work/dir \
        -s /path/to/samples.csv
* Note: This setup allows the main Snakefile to live outside of the work directory.

4. To run CAMP on a job submission cluster (for now, only Slurm is supported), use the following.
    - ``--slurm`` is an optional flag that submits all rules in the Snakemake pipeline as ``sbatch`` jobs. 
    - In Slurm mode, the ``-c`` flag refers to the maximum number of ``sbatch`` jobs submitted in parallel, **not** the pool of cores available to run the jobs. Each job will request the number of cores specified by threads in ``configs/resources/slurm.yaml``.
::
    sbatch -J jobname -o jobname.log << "EOF"
    #!/bin/bash
    python /path/to/camp_short-read-quality-control/workflow/short-read-quality-control.py --slurm \
        (-c max_number_of_parallel_jobs_submitted) \
        -d /path/to/work/dir \
        -s /path/to/samples.csv
    EOF

5. To quality-check the processed FastQs, download and compare the collated MultiQC reports, which can be found at ``/path/to/work/dir/short_read_qc/final_reports/*_multiqc_report/html``. Multiple rounds of preprocessing may be needed to fully get rid of low-quality bases, adapters, and duplicated sequences. 
    - For example, the dataset I worked with required an additional round of ``fastp`` to trim 10 low-quality bases from the 5' and 4 low-quality bases from the 3' end respectively. 
    - I recommend creating a new directory, which I've called ``/path/to/work/dir/short_read_qc/5_retrimming`` and placing reprocessed reads inside them. 
    - Afterwards, I reran FastQC and MultiQC and collated summary statistics (ex. numbers of reads, etc.) from the reprocessed datasets manually. I also updated the location of the reprocessed reads in ``/path/to/work/dir/short_read_qc/final_reports/samples.csv`` to ``/path/to/work/dir/short_read_qc/5_retrimming``.

6. If for some reason the module keeps failing, CAMP can print a script containing all of the remaining commands that can be run manually. 
::

    python3 /path/to/camp_short-read-quality-control/workflow/short-read-quality-control.py \
        --dry_run \
        -d /path/to/work/dir \
        -s /path/to/samples.csv > cmds.txt
    python3 /path/to/camp_short-read-quality-control/workflow/short-read-quality-control.py \
        commands cmds.txt

7. To plot grouped bar graph(s) of the number of reads and bases remaining after each quality control step in each sample, set up the dataviz environment and follow the instructions in the Jupyter notebook:
::
    conda env create -f configs/conda/dataviz.yaml
    conda activate dataviz
    jupyter notebook &

Updating the Module
--------------------

What if you've customized some components of the module, but you still want to update the rest of the module with latest version of the standard CAMP? Just do the following from within the module's home directory:
    - The flag with the setting ``-X ours`` forces conflicting hunks to be auto-resolved cleanly by favoring the local (i.e.: your) version.
::
    cd /path/to/camp_short-read-quality-control
    git pull -X ours

Extending the Module
--------------------

We love to see it! This module was partially envisioned as a dependable, prepackaged sandbox for developers to test their shiny new tools in. 

These instructions are meant for developers who have made a tool and want to integrate or demo its functionality as part of a standard short-read-quality-control workflow, or developers who want to integrate an existing short-read-quality-control tool. 

1. Write a module rule that wraps your tool and integrates its input and output into the pipeline. 
    - This is a great `Snakemake tutorial <https://bluegenes.github.io/hpc-snakemake-tips/>`_ for writing basic Snakemake rules.
    - If you're adding new tools from an existing YAML, use ``conda env update --file configs/conda/existing.yaml --prune``.
    - If you're using external scripts and resource files that i) cannot easily be integrated into either `utils.py` or `parameters.yaml`, and ii) are not as large as databases that would justify an externally stored download, add them to ``workflow/ext/`` and use ``rule external_rule`` as a template to wrap them. 
2. Update the ``make_config`` in ``workflow/Snakefile`` rule to check for your tool's output files. Update ``samples.csv`` to document its output if downstream modules/tools are meant to ingest it. 
    - If you plan to integrate multiple tools into the module that serve the same purpose but with different input or output requirements (ex. for alignment, Minimap2 for Nanopore reads vs. Bowtie2 for Illumina reads), you can toggle between these different 'streams' by setting the final files expected by ``make_config`` using the example function ``workflow_mode``.
    - Update the description of the ``samples.csv`` input fields in the CLI script ``workflow/short-read-quality-control.py``. 
3. If applicable, update the default conda config using ``conda env export > config/conda/short-read-quality-control.yaml`` with your tool and its dependencies. 
    - If there are dependency conflicts, make a new conda YAML under ``configs/conda`` and specify its usage in specific rules using the ``conda`` option (see ``first_rule`` for an example).
4. Add your tool's installation and running instructions to the module documentation and (if applicable) add the repo to your `Read the Docs account <https://readthedocs.org/>`_ + turn on the Read the Docs service hook.
5. Run the pipeline once through to make sure everything works using the test data in ``test_data/`` if appropriate, or your own appropriately-sized test data. 
    * Note: Python functions imported from ``utils.py`` into ``Snakefile`` should be debugged on the command-line first before being added to a rule because Snakemake doesn't port standard output/error well when using ``run:``.

5. Increment the version number of the modular pipeline- ``patch`` for bug fixes (changes E), ``minor`` for substantial changes to the rules and/or workflow (changes C), and ``major`` only applies to major releases of the CAMP. 
::

    bump2version --current-version A.C.E patch

6. If you want your tool integrated into the main CAMP pipeline, send a pull request and we'll have a look at it ASAP! 
    - Please make it clear what your tool intends to do by including a summary in the commit/pull request (ex. "Release X.Y.Z: Integration of tool A, which does B to C and outputs D").

.. ..

 <!--- 
 Bugs
 ----
 Put known ongoing problems here
 --->

Credits
-------

* This package was created with `Cookiecutter <https://github.com/cookiecutter/cookiecutter>`_ as a simplified version of the `project template <https://github.com/audreyr/cookiecutter-pypackage>`_.
* Free software: MIT
* Documentation: https://short-read-quality-control.readthedocs.io. 



