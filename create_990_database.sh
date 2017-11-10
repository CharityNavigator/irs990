#!/bin/sh +x

# Copyright 2017 Charity Navigator.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.

echo "***Initializing database."
mysql -h $1 -P 3306 -u $2 -p$3 < ./sql/setup_db.sql
echo "***Creating database tables (except XML table)."
python ./python/create_db.py --hostname $1 --username $2 --password $3
echo "***Creating XML table."
mysql -h $1 -P 3306 -u $2 -p$3 < ./sql/create_xml_table.sql
echo "***Loading 990 schema crosswalk for stand-alone fields."
python ./python/load_990_singletons.py --hostname $1 --username $2 --password $3
echo "***Loading 990 root crosswalk for field groups."
python ./python/load_990_roots.py --hostname $1 --username $2 --password $3
echo "***Loading 990 stem crosswalk for fields in field groups."
python ./python/load_990_stems.py --hostname $1 --username $2 --password $3
echo "***Done."
