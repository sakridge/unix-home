#!/usr/bin/python
import P4
import sys

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.PURPLE = ''
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.ENDC = ''

def doPrint(depotFile, rev, action):
    color = ''
    endcolor = ''
    if (action == "edit"):
        color = bcolors.BLUE
        endcolor = bcolors.ENDC
    elif (action == "integrate"):
        color = bcolors.YELLOW
        endcolor = bcolors.ENDC
    print ("    %s#%s " + color + "%s" + endcolor) % (depotFile, rev, action)

if __name__ == "__main__":
    p4 = P4.P4()
    p4.connect()

    info = p4.run("info")[0]
    #print info
    changes = p4.run_changes("-c", info['clientName'], "-u", info['userName'], "-s", "pending", "...")
    #print changes
    for change in changes:
        print '%s %s %s \'%s\'' % (change['change'], change['status'], change['user'], ' '.join(change['desc'].split()))
        describe = p4.run_describe("-s", change['change'])[0]
        for depotFile, rev, action in zip(describe['depotFile'], describe['rev'], describe['action']):
            doPrint(depotFile, rev, action)
        shelve_describe = p4.run_describe("-s", "-S", change['change'])[0]
        if (shelve_describe.has_key('depotFile')):
            print "Shelved files ..."
            #print shelve_describe
            for depotFile, rev, action in zip(shelve_describe['depotFile'], shelve_describe['rev'], shelve_describe['action']):
                doPrint(depotFile, rev, action)


