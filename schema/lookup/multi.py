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

from base import LookupBase
from schema.stem import Stem
from schema.root import Root

class MultiLookup(LookupBase):

    def __init__(self, session, raw):
        LookupBase.__init__(self, session, raw)
        
        stems = session.query(Stem)\
                    .filter(Stem.FormType==self.formType)\
                    .filter(Stem.version==self.version)

        self.initStems(stems)

        roots = session.query(Root)\
                    .filter(Root.FormType==self.formType)\
                    .filter(Root.version==self.version)

        self.initRoots(roots)

    def initRoots(self, roots):
        # A map of table name -> list of paths.
        self.rootDict = {}

        for root in roots:
            self.loadRoot(root, self.rootDict)

    def loadRoot(self, root, dct):
        tbl   = root.tbl
        path  = root.path

        if not tbl in dct.keys():
            dct[tbl] = []

        qualified = self.qualify(path)
        dct[tbl].append(qualified)

    def getRoots(self, tbl):
        paths = self.rootDict[tbl]
        roots = self.getMatches(self.root, paths)
        return roots
