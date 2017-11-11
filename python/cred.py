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

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
import sys
import argparse

class Credentials:

    def __init__(self, database="irs990", port=3306):
        parser = argparse.ArgumentParser()
        parser.add_argument("--hostname", action="store")
        parser.add_argument("--username", action="store")
        parser.add_argument("--password", action="store")
        parser.add_argument("--prod",action="store_true")
        parser.add_argument("--database", action="store", default="irs990")
        parser.add_argument("--port", type=int, action="store", default=3306)
        args = parser.parse_args()

        self.host = args.hostname
        self.username = args.username
        self.password = args.password
        self.port = args.port
        self.database = args.database
        self.prod = args.prod

    def getEngineStr(self):
        return "mysql://%s:%s@%s/%s" % (self.username, self.password, self.host, self.database)
