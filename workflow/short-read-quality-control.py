'''CLI for the CAMP Short-read Quality Control module.'''


import click
from os import makedirs
from os.path import abspath, exists, join
from snakemake import snakemake, main


def sbatch(workflow, work_dir, samples, env_yamls, pyaml, ryaml, cores, env_dir):
    cfg_wd = 'work_dir=%s' % work_dir
    cfg_sp = 'samples=%s' % samples
    cfg_ey = 'env_yamls=%s' % env_yamls
    main([
        '--snakefile',      workflow, 
        '--config',         *{cfg_wd, cfg_sp, cfg_ey},
        '--configfiles',    *[pyaml, ryaml],
        '--jobs',           str(cores),
        '--use-conda',
        '--conda-frontend', 'conda',
        '--conda-prefix',   env_dir,
        '--cluster',        "sbatch -J {wildcards}.{rulename}.{jobid} \
                             -n {threads} --mem {resources.mem_mb} -o {log}"
    ])


def cmd_line(workflow, work_dir, samples, env_yamls, pyaml, ryaml, cores, env_dir, unit_test_dir):
    snakemake(
        workflow,
        config = {
            'work_dir': work_dir,
            'samples': samples,
            'env_yamls': env_yamls
        },
        configfiles = [
            pyaml,
            ryaml
        ],
        cores = cores,
        use_conda = True,
        conda_prefix = env_dir,
        generate_unit_tests = unit_test_dir
    )


@click.command('run')
@click.option('-w', '--workflow', type = click.Path(), required = True, \
    help = 'Absolute path to the Snakefile')
@click.option('-c', '--cores', type = int, default = 1, show_default = True, \
    help = 'In local mode, the number of CPU cores available to run rules. \n\
    In Slurm mode, the number of sbatch jobs submitted in parallel. ')
@click.option('-d', '--work_dir', type = click.Path(), required = True, \
    help = 'Absolute path to working directory')
@click.option('-s', '--samples', type = click.Path(), required = True, \
    help = 'Sample CSV in format [sample_name,...,]') # Update the samples.csv fields
@click.option('--unit_test', is_flag = True, default = False, \
    help = 'Generate unit tests using Snakemake API')
@click.option('--slurm', is_flag = True, default = False, \
    help = 'Run workflow by submitting rules as Slurm cluster jobs')
def run(workflow, cores, work_dir, samples, unit_test, slurm): 
    # Get the absolute path of the Snakefile to find the profile configs
    main_dir = abspath(workflow).split('/')[:-2] # /path/to/main_dir/workflow/Snakefile

    # Set location of rule (and program) parameters and resources
    pyaml = join('/', *main_dir, 'configs', 'parameters.yaml')
    ryaml = join('/', *main_dir, 'configs', 'resources.yaml')

    # Set up the conda environment directory
    env_dir = join('/', *main_dir, 'conda_envs')
    if not exists(env_dir):
        makedirs(env_dir)
    env_yamls = join('/', *main_dir, 'configs', 'conda')

    # If generating unit tests, set the unit test directory (by default, is pytest's default, .tests)
    unit_test_dir = join('/', *main_dir, '.tests/unit') if unit_test else None

    # Run workflow
    if slurm:
        sbatch(workflow, work_dir, samples, env_yamls, pyaml, ryaml,     \
               cores, env_dir)
    else:
        cmd_line(workflow, work_dir, samples, env_yamls, pyaml, ryaml,   \
                 cores, env_dir, unit_test_dir)


if __name__ == "__main__":
    run()
