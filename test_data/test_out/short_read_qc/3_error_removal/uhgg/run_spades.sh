set -e
true
true
/lustre2/home/lam4003/bin/anaconda/envs/short-read-quality-control/bin/spades-hammer /home/lam4003/bin/camp_short-read-quality-control/test_data/test_out/short_read_qc/3_error_removal/uhgg/corrected/configs/config.info
/home/lam4003/bin/anaconda/envs/short-read-quality-control/bin/python /lustre2/home/lam4003/bin/anaconda/envs/short-read-quality-control/share/spades/spades_pipeline/scripts/compress_all.py --input_file /home/lam4003/bin/camp_short-read-quality-control/test_data/test_out/short_read_qc/3_error_removal/uhgg/corrected/corrected.yaml --ext_python_modules_home /lustre2/home/lam4003/bin/anaconda/envs/short-read-quality-control/share/spades --max_threads 12 --output_dir /home/lam4003/bin/camp_short-read-quality-control/test_data/test_out/short_read_qc/3_error_removal/uhgg/corrected --gzip_output
true
/home/lam4003/bin/anaconda/envs/short-read-quality-control/bin/python /lustre2/home/lam4003/bin/anaconda/envs/short-read-quality-control/share/spades/spades_pipeline/scripts/breaking_scaffolds_script.py --result_scaffolds_filename /home/lam4003/bin/camp_short-read-quality-control/test_data/test_out/short_read_qc/3_error_removal/uhgg/scaffolds.fasta --misc_dir /home/lam4003/bin/camp_short-read-quality-control/test_data/test_out/short_read_qc/3_error_removal/uhgg/misc --threshold_for_breaking_scaffolds 3
true
