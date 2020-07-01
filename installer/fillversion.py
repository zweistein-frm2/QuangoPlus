#!/usr/bin/python

import sys
import os

def fill_version(filein, fileout,lineinfo):    
    curline = 0
    lines = 0
    with open(filein) as fin, open(fileout, 'w') as fout:
        for line in fin:
            if line.startswith('[Application]'):
                curline = lines
            lines = lines + 1

            if line.startswith('version=') and lines - curline < 4 :
                with open(lineinfo) as fver :
                    versioninfo = fver.readline()
                line = 'version='+versioninfo
            lineout = line
            fout.write(lineout)

def main():
    print(os.getcwd())
    # print command line arguments
    for arg in sys.argv[1:]:
        print(arg)
    fill_version(sys.argv[1],sys.argv[2],sys.argv[3])   
    

if __name__ == "__main__":
    main()