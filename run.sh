NOTE----> Change folder names accordingly and make sure to DELETE all the old sentence and sentence_data files and
also the old folders (maybe just replace data_fixed entirely?)

cd Spoken
python save_variants_folder.py "/home2/aadya.ranjan/Data_Fixed/Spoken"
python result_calculation.py

cd Written
python save_variants_folder.py "/home2/aadya.ranjan/Data_Fixed/Written"
python result_calculation.py
