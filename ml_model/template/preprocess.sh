sed 's/ÿ//g' module_data_left | sed '/,,/d' > module_data_foot
sed 's/ÿ//g' module_data_right | sed '/,,/d' > module_data_shank
python preprocess.py module_data_foot
python preprocess.py module_data_shank
python connect.py ./
