# GaitAnalysis
There are three parts in the program.

---
## Hardware
esp8266.ino for esp8266 with Arduino.
mainprogram.ino for Arduino Nano.
MPU6050.ino for testing MPU6050 on Auduino Nano.

---
## ml_model
First, the hardware sends data to index.php.
Index.php records data into module_data_left, module_data_right and call preprocess.sh.
Preprocess.sh removes garbled messages and transfers into module_data_foot and module_data_shank.
After making sure the stabibility of receiving data, enter your motion (e.g. walking, running, stopping and resting) into index.php with browser.
Once the data is enough, type "make" to run Makefile. Makefile names a directory with the date and automatically moves all data into the directory.
Change directory into the directory with the date and run 'preprocess.sh', which will clean the data and connect module_data_foot and module_data_shank by time.
Change directory into the upper directory and run collect.py, which will automatically collect all data from sub-directories.
If you haven't build a svm-model, you should un-quote some code in the previous step and run collect.py. Run feature_select.py to choose the best 6 features and alternate collect.py to select the 6 features. Run collect.py again and use quick.sh (also need to un-quote some code and install libsvm for python) in libsvm to see the best model. Select the best model and edit qq.py to get the model.
Run 'getMotion.py' in libsvm to get the motion of data.

---
## website
time_series.html shows the ongoing data from ml_model, steps and the predicted motions.
