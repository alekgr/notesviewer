#!/usr/bin/bash

#########################
# Makefile for building  and uploading to test and real pypi
# This file will not be in pypi but will be in the source repository
# ./Makefile clean
# ./Makefile build
# ./Makefile upload_test
# ./Makefile uplod_real
# ./Makefile help
#########################

testpypi="https://test.pypi.org/legacy/"

current_dir=`pwd`
cd ../

cm_clean()
{		
	# clean dist and build directory
	if [ -d $current_dir/dist ]
	then
		rm -R $current_dir/dist 
	fi
	
	if [ -d $current_dir/build ]
	then
		rm -R $current_dir/build
	fi
}

cm_build()
{
	# build poackage from setup.py
	python3 setup.py sdist bdist_wheel  
	mv build $current_dir
	mv dist  $current_dir
}

cm_upload_test()
{
	# upload to testing pypi 
	python3 -m twine upload --repository-url $testpypi $current_dir/dist/*
}

cm_upload_real()
{
	# upload to production pypi
	python3 -m twine upload $current_dir/dist/*
}

cm_help()
{
	# help command
	echo "usage: Makefile [command]"
	echo "  clean		- Clean dist and build directories"
	echo "  build		- Build dist the package"
	echo "  upload_test 	- Upload to test.pypi.org"
	echo "  upload_real 	- Upload to pypi.org"
	echo "  help          - this help" 

}

# switch case for the command that is chosen
case $1 in
	clean)
		cm_clean;;
	build)
		cm_build;;
	upload_test)
		cm_upload_test;;
	upload_real)
		cm_upload_real;;
	help)
		cm_help;;
	*)
		printf "error: Missing or incorrect commmand\n\n"
		cm_help;;
esac
