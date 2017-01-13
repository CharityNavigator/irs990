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

from schema import *
from schema.base import Credentials, Base
from sqlalchemy import create_engine

cred = Credentials()
engineStr = cred.getEngineStr()
engine = create_engine(engineStr)

tables = ["filing",
          "crosswalk",
          "root",
          "stem",
          "part_i",
          "part_iv",
          "part_vi",
          "part_vii_a",
          "part_ix",
          "sched_l_part_ii",
          "part_x",
          "header",
          "sched_g_part_i",
          "part_iii",
          "part_xii",
          "part_viii"]

for table in tables:
    Base.metadata.tables[table].create(bind = engine)
