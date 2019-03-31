#/bin/bash

if [ $CONDA_DEFAULT_ENV != "books-data-science" ]; then 
	echo "run conda activate books-data-science before start jupyter notebook"; 
	exit 1;
fi 

jupyter notebook --NotebookApp.iopub_data_rate_limit=30000000.0
