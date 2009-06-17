#!/bin/bash
ScriptLocation="."
if [[ $0 == '/'* ]];
then ScriptLocation="`dirname $0`"
else ScriptLocation="`pwd`"/"`dirname $0`"
fi

# Installation of PIL 1.1.6
cd $ScriptLocation/../subproducts
tar -xvzf Imaging-1.1.6.tar.gz
cd Imaging-1.1.6
$ScriptLocation/python ./setup.py install
cd ..
rm -f -R Imaging-1.1.6

# Installation of psycopg 2.0.6
cd $ScriptLocation/../subproducts
tar -xvzf psycopg2-2.0.6.tar.gz
cd psycopg2-2.0.6
$ScriptLocation/python ./setup.py install
cd ..
rm -f -R psycopg2-2.0.6
