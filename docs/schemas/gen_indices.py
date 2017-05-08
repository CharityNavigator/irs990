import glob
import os.path
dirs = sorted(glob.glob("*"))

with open("index.md", "w") as o:
    o.write("# Schema change logs\n\n")
    o.write("The IRS has issued numerous versions of the 990 schema. Some of these versions are available in zipped archives on the [IRS public schema page](https://www.irs.gov/pub/irs-schema/). These archives contain human-readable change logs in HTML format, which we have republished here for your convenience.\n\n")
    o.write("## Versions\n\n")
    for d in dirs:
        if not (os.path.isdir(d)):
            continue
        o.write("* [%s](%s/index)\n" % (d, d))
        with open("./%s/index.md" % d, "w") as p:
            p.write("# Change logs for '%s'\n\n" % d)
            files = glob.glob("./%s/*.html" % d)
            for f in files:
                fn = f.split("/")[-1]
                name = fn.split(".")[0]
                p.write("* [%s](%s)\n" % (name, fn))
