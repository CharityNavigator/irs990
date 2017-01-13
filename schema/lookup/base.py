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

from lxml import etree
class LookupBase:
    ns = "{http://www.irs.gov/efile}"

    def __init__(self, session, raw):
        self.version = raw.Version
        self.formType = raw.FormType
        self.root = etree.fromstring(raw.XML)

    def initStems(self, members):
        self.stemDict = {}
        for member in members:
            self.loadStem(member, self.stemDict)

    def qualify(self, path):
        tokens = path.split("/")

        if tokens[0] == "Return":
            tokens = tokens[1:]
        qualified = [self.ns + token for token in tokens]
        return "/".join(qualified)

    def loadStem(self, cw, dct):
        tbl   = cw.tbl
        field = cw.field
        path  = cw.path

        if not tbl in dct.keys():
            dct[tbl] = {}

        if not field in dct[tbl].keys():
            dct[tbl][field] = []

        qualified = self.qualify(path)
        #print '"%s" -> "%s"' % (path, qualified)
        dct[tbl][field].append(qualified)

    def getMatches(self, root, paths):
        ret = []
        for path in paths:
            ret.extend(root.findall(path))
        return ret

    def getStems(self, tbl, field):
        if not tbl in self.stemDict.keys():
            raise Exception("Unrecognized table \"%s\" for form %s" % (tbl, self.formType))
        
        if not field in self.stemDict[tbl].keys():
            return []
        #raise Exception('Field "%s" not found for table "%s" in version %s' % (field, tbl, self.version))

        stems = self.stemDict[tbl][field]
        return stems 

    def getNodeOrNone(self, tbl, field, root=None):
        if root == None:
            root = self.root

        stems = self.getStems(tbl, field)

        results = self.getMatches(root, stems)

        if len(results) == 0:
            return None

        if len(results) > 1:
            raise Exception("Multiple results where zero or one expected on %s.%s" % (tbl, field))

        return results[0]

    def findWithNa(self, tbl, field, root=None):
        node = self.getNodeOrNone(tbl, field, root)
        if node == None:
            return None


        return node.text

    def getTextAllowingAttribute(self, tbl, field, root=None):
        if root == None:
            root = self.root

        stems = self.getStems(tbl, field)
        ret = []

        for stem in stems:
            components = stem.split("*")
            if len(components) > 2:
                print 'Unrecognized stem "%s"%' % stem

            path = components[0]

            if len(components) == 1:
                ret.extend([elem.text for elem in root.findall(path)])

            else:
                attr = components[1]
                ret.extend([elem.attrib[attr] for elem in root.findall(path)])

        if len(ret) == 0:
            return None

        if len(ret) > 1:
            raise("Found multiple results for %s.%s where one or none expected" % (tbl, field))

        return ret[0]

    def findTrueFalse(self, tbl, field, root=None):
        node = self.getNodeOrNone(tbl, field, root)

        if node == None:
            return False

        text = node.text
        if text == "true":
            return True

        if text == "1":
            return True

        if text == "X":
            return True

        if text == "false":
            return False

        if text == "0":
            return False

        raise Exception(etree.tostring(node))
