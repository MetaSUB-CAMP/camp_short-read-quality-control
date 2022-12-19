#! /bin/bash -l
 
#SBATCH --partition=panda_physbio
#SBATCH --job-name=slurm_qc
#SBATCH --time=24:00:00
#SBATCH --mem=100G   # memory requested, units available: K,M,G,T
#SBATCH --cpus-per-task=8
#SBATCH --output slurm_qc-%j.out
#SBATCH --error slurm_qc-%j.err


source ~/.bashrc
mamba activate short-read-quality-control
echo "This is job #:" $SLURM_JOB_ID >> slurm_qc_output.txt
echo "conda activated?"
python /home/chf4012/camp_short-read-quality-control/workflow/short-read-quality-control.py -d /home/chf4012/camp_short-read-quality-control/test_fairbanks_data -s /home/chf4012/camp_short-read-quality-control/test_fairbanks_data/samples_test_fairbank.csv --unlock
exit