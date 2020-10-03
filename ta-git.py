#!/usr/bin/env python
from pathlib import Path
import os
import sys
import json
import subprocess

if __name__ == "__main__":

    tags = sys.argv[1:]
    #todo: add prefix support cmdline option
    prefix = "#"
    tags = [prefix+tag if not tag[0] == prefix else tag for tag in tags]
    files = []

    #todo: add extension cmdline option
    extensions = ["*.cpp", "*.c", "*.hpp", "*.h", "*.py"]
    tagged = {}
    for extension in extensions:
        for path in Path(os.path.curdir).rglob(extension):
            files.append(path)

    for f in files:
        try:
            with open(f, "r") as r_file:
                lines = r_file.readlines()
                for line, i in zip(lines, range(0, len(lines))):
                    lower_line = line.lower();
                    for tag in tags:
                        if tag in lower_line:
                            l_num = str(i+1)
                            pos = lower_line.find(tag)
                            author = "No Author"
                            try:
                                # check to see if we can find an author in git
                                author_cmd = "git log -L "+l_num+","+l_num+":"+str(f)
                                log = subprocess.check_output(author_cmd, shell=True)
                                for l_line in log.splitlines(False):
                                    str_line = str(l_line)
                                    if "Author: " in str_line:
                                        author = str_line.split("Author: ")[1][0:-1]
                            except:
                                pass

                            if author not in tagged:
                                tagged[author] = {}
                            if tag not in tagged[author]:
                                tagged[author][tag] = []
                            
                            tagged[author][tag].append(str(f)+":"+l_num+":"+line[pos+len(tag):])
        except:
            print("error: failed to read "+str(f)+" "+str(sys.exc_info()[0]))

    print(json.dumps(tagged, sort_keys=True, indent=4))
