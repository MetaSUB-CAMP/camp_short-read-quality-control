#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=slurm_qc
#SBATCH --time=00:02:00   # HH/MM/SS
#SBATCH --mem=1G   # memory requested, units available: K,M,G,T
#SBATCH --output slurm_qc-%j.out
#SBATCH --error slurm_qc-%j.err
 
source ~/.bashrc
mamba activate short-read-quality-control
echo "This is job #:" $SLURM_JOB_ID >> slurm_qc_output.txt
echo "conda activated?"
python /home/chf4012/camp_short-read-quality-control/workflow/short-read-quality-control.py --slurm -c 5 -d /home/chf4012/camp_short-read-quality-control/test_data -s /home/chf4012/camp_short-read-quality-control/test_data/samples.csv

exit