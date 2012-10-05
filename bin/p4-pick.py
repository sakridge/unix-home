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
        cl_descriptions = p4.run_describe("-s", change['change'])[0]

        for fname, rev in zip(cl_descriptions['depotFile'], cl_descriptions['rev']):
            print fname + "#" + rev
            try:
                p4.run("sync", "-f", fname + "#" + rev)
            except:
                for w in p4.warnings:
                    print w
        #print cl_descriptions

