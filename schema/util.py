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

def findWithNa(root, search):
    ns = "{http://www.irs.gov/efile}"
    while len(search) > 0:
        cur  = search.pop(0)
        candidate = None

        for elem in cur.split("|"):
            node = "%s%s" % (ns, elem)
            candidate = root.find(node)
            if candidate != None:
                root = candidate
                break
        if candidate == None:
            return None
    return root.text

def getNodeOrNone(root, search):
    ns = "{http://www.irs.gov/efile}"
    while len(search) > 0:
        cur  = search.pop(0)
        candidate = None

        for elem in cur.split("|"):
            node = "%s%s" % (ns, elem)
            candidate = root.find(node)
            if candidate != None:
                root = candidate
                break
        if candidate == None:
            return None
    return root

def findTrueFalse(root, search):
    search_str = "/".join(search)
    ns = "{http://www.irs.gov/efile}"
    while len(search) > 0:
        cur  = search.pop(0)
        candidate = None

        for elem in cur.split("|"):
            node = "%s%s" % (ns, elem)
            candidate = root.find(node)
            if candidate != None:
                root = candidate
                break
        if candidate == None:
            return False

    text = root.text
    if text == "true":
        return True

    if text == "X":
        return True

    if text == "false":
        return False

    raise Exception("Unexpected value %s (%s)" % (search_str, text))
