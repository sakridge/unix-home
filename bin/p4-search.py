#!/usr/bin/python
import P4
import sys

if __name__ == "__main__":
    p4 = P4.P4()
    p4.connect()

    if (',' in sys.argv[1]):
        from_cl, to_cl = sys.argv[1].split(',')
    else:
        from_cl = sys.argv[1]
        to_cl = sys.argv[1]

    changes = p4.run_changes("...@" + from_cl + ",@" + to_cl)
    for change in reversed(changes):
        cl_descriptions = p4.run_describe(change['change'])[0]

        for fname, rev in zip(cl_descriptions['depotFile'], cl_descriptions['rev']):
            p4.tagged = 0
            diff = p4.run_diff2(fname + "#" + rev, fname + "#" + str(int(rev) - 1))
            p4.tagged = 1
            if sys.argv[2] in diff[1]:
                print cl_descriptions['change'] + " " + fname + "#" + rev
        #print cl_descriptions

