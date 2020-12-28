#!/usr/bin/env python
from pathlib import Path
import os
import sys
import json
import subprocess

if __name__ == "__main__":

    args = sys.argv[1:]
    tags = []
    paths = []
    for i, arg in enumerate(args):
        if arg == "-t":
            tags.append(args[i+1])
        if arg == "-d":
            paths.append(args[i+1])
        
    if len(paths) == 0:
        paths.append(os.path.curdir)
    #todo: add prefix support cmdline option
    prefix = "#"
    tags = [prefix+tag if not tag[0] == prefix else tag for tag in tags]
    files = []

    #todo: add extension cmdline option
    extensions = ["*.cpp", "*.c", "*.hpp", "*.h", "*.py"]
    tagged = {}
    tagit = {}
    for in_path in paths:
        for extension in extensions:
            for path in Path(in_path).rglob(extension):
                files.append(path)

    for f in files:
        try:
            dirname = os.path.dirname(f)
            basename = os.path.basename(f)
            
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
                                author_cmd = "cd "+dirname+";git log -L "+l_num+","+l_num+":"+basename
                                log = subprocess.check_output(author_cmd, shell=True)
                                for l_line in log.splitlines(False):
                                    str_line = l_line.decode("utf-8")
                                    if "Author: " in str_line:
                                        author = str_line.split("Author: ")[1][0:]
                            except:
                                pass

                            if author not in tagged:
                                tagged[author] = {}
                            if tag not in tagged[author]:
                                tagged[author][tag] = []
                            
                            tagged[author][tag].append(str(f)+":"+l_num+":"+line[pos+len(tag):])
        except:
            print("error: failed to read "+str(f)+" "+str(sys.exc_info()[0]))

    logs = {}
    try:
        for tag in tags:
            log_cmd = "git log --all --grep=\""+tag+"\""
            log = subprocess.check_output(log_cmd, shell=True)
            log = log.decode("utf-8")
            if len(log) > 0:
                logs[tag] = log
    except:
        pass

    tagit["tagged"] = tagged
    tagit["commits"] = logs
    print(json.dumps(tagit, indent=4))
        
