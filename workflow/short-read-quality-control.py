'''CLI for the CAMP short-read-quality-control module.'''


import click
from os.path import abspath, exists, join
from snakemake import snakemake
from os import makedirs


@click.command('run')
@click.option('-w', '--workflow', type = click.Path(), required = True, \
    help = 'Absolute path to the Snakefile')
@click.option('-d', '--work_dir', type = click.Path(), required = True, \
    help = 'Absolute path to working directory')
@click.option('-s', '--samples', type = click.Path(), required = True, \
    help = 'Sample CSV in format [sample_name,contig_fasta,fwd_fastq,rev_fastq]')
@click.option('--unit_test', is_flag = True, default = False, \
    help = 'Generate unit tests using Snakemake API')
@click.option('--slurm', is_flag = True, default = False, \
    help = 'Run workflow by submitting rules as Slurm cluster jobs')
@click.option('--cap2', is_flag = True, default = False, \
    help = 'Run workflow in CAP2 mode')
def run(workflow, work_dir, samples, unit_test, slurm, cap2):
    # Get the absolute path of the Snakefile to find the profile configs
    bin_dir = abspath(workflow).split('/')[:-2] # /path/to/bin_dir/workflow/Snakefile

    # Set location of rule (and program) parameters and resources
    pyaml = join('/', *bin_dir, 'configs', 'parameters.yaml')
    ryaml = join('/', *bin_dir, 'resources', 'bash.yaml')

    # Set location of compute cluster profile
    cluster_config = join('/', *bin_dir, 'configs', 'resources', 'slurm.yaml') \
                     if slurm else None
    cluster_subcmd = "sbatch -n {cluster.nCPU} --mem {cluster.mem} \
                     -o {cluster.output}" \
                     if slurm else None

    # If generating unit tests, set the unit test directory (by default, is pytest's default)
    unit_test_dir = join('/', *bin_dir, '.tests/unit') if unit_test else None

    # Set up the conda environment directory
    env_dir = join('/', *bin_dir, 'conda_envs')
    if not exists(env_dir):
        makedirs(env_dir)

    # Run workflow
    snakemake(
        workflow,
        config = {
            'work_dir': work_dir,
            'samples': samples,
            'cap2': cap2,
            'env_yamls': join('/', *bin_dir, 'configs', 'conda')
        },
        configfiles = [
            pyaml,
            ryaml
        ],
        use_conda = True,
        conda_prefix = env_dir,
        generate_unit_tests = unit_test_dir,
        cluster_config = cluster_config,
        cluster = cluster_subcmd
    )


if __name__ == "__main__":
    run()
