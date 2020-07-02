.Silent:

now:=$(shell date +"%Y%m%d")
all:
	if [ -d $(now) ]; then \
		echo $(now); \
		tail -n +2 ./module_data_left >> $(now)/module_data_left; \
		tail -n +2 ./module_data_right >> $(now)/module_data_right; \
		else \
		echo $(now); \
		mkdir $(now); \
		echo "Copying..."; \
		cp ./module_data_left $(now); \
		cp ./module_data_right $(now); \
		fi
	cat ./module_data > ./module_data_left
	cat ./module_data > ./module_data_right
	cat ./module_data > ./module_data_foot
	cat ./module_data > ./module_data_shank
	cp -r ./template/* $(now)
	echo "Done!"

collect: collect.py
	python collect.py

get:
	if [ -d $2 ]; then \
		echo $2;\
		#cp ./$2/module_data_left > ./module_data_left;\
		#cp ./$2/module_data_right > ./module_data_right;\
		else \
		echo $2; \
		echo 'no such directory';\
		fi
	bash ./preprocess.sh

