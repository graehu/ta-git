#!/usr/bin/env python
from pathlib import Path
import os
import sys
import json
import subprocess
import collections.abc
import datetime

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

if __name__ == "__main__":

    args = sys.argv[1:]
    tags = []
    paths = []
    num_context = 4
    tag_format = """
* {date} - [`"{path}"`]({path_link}) - {tag_line}
* [{sha}]({origin_commit_link})
{context}
"""
    log_format = """
``` git
{log}
```
"""
    md_path = "ta-git.md"
    for i, arg in enumerate(args):
        if arg == "-t":
            tags.append(args[i+1])
        if arg == "-d":
            paths.append(args[i+1])
        if arg == "-c":
            num_context = args[i+1]
        if arg == "-md":
            md_path = args[i+1]

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


    origin_http = subprocess.check_output("git config --get remote.origin.url", shell=True)
    origin_http = origin_http.decode("utf-8").rstrip()
    origin_ssh = ""
    if("http" in origin_http):
        origin_ssh = origin_http.split("://")[1]
        origin_ssh = "git@"+origin_ssh.replace("/", ":", 1)
    else:
        origin_ssh = origin_http
        origin_http = "https://"+origin_ssh.split("@", 1)[1].replace(":", "/", 1)
    origin_base = os.path.basename(origin_http)
    for f in files:
        try:
            dirname = os.path.dirname(f)
            basename = os.path.basename(f)

            with open(f, "r") as r_file:
                lines = r_file.readlines()
                for line, i in zip(lines, range(0, len(lines))):
                    lower_line = line.lower()
                    context = []
                    if num_context:
                        context = lines[i:min(len(lines), i+num_context)]
                    for tag in tags:
                        if tag in lower_line:
                            l_num = str(i+1)
                            author = "No Author"
                            date = ""
                            commit = ""
                            log = ""
                            try:
                                # check to see if we can find an author in git
                                author_cmd = "cd "+dirname+";"
                                author_cmd += "git log "
                                author_cmd += "--date=iso8601 "
                                author_cmd += "-L "+l_num+","+l_num+":"+basename+" "
                                log = subprocess.check_output(author_cmd, shell=True)
                                log = log.decode("utf-8")
                                for str_line in log.split("\n"):
                                    if str_line.startswith("Author: "):
                                        author = str_line.split("Author: ")[1][0:]
                                    if str_line.startswith("Date: "):
                                        date = str_line.split("Date:   ")[1][0:]
                                    if str_line.startswith("commit "):
                                        commit = str_line.split("commit ")[1][0:]
                            except:
                                print("error: "+str(sys.exc_info()[0]))

                            if author not in tagged:
                                tagged[author] = {}
                            if tag not in tagged[author]:
                                tagged[author][tag] = {}
                            if "lines" not in tagged[author][tag]:
                                tagged[author][tag]["lines"] = {}
                            if "logs" not in tagged[author][tag]:
                                tagged[author][tag]["logs"] = {}

                            line_message = line.lstrip().rstrip()
                            line_str = str(f)+":"+l_num
                            if context:
                                context.insert(0, "\n``` "+basename.split(".")[-1]+"\n")
                                context.append("\n```")
                            tagged[author][tag]["lines"].update({line_str: {
                                "path": line_str,
                                "path_link": line_str.replace(":", "#L"),
                                "origin_path_link": origin_http.replace(".git", "/")+line_str.replace(":", "#L"),
                                "date": date.split(" ")[0],
                                "tag_line": line_message,
                                "sha": commit,
                                "origin_commit_link": origin_http.replace(".git", "/commit/")+commit,
                                "context": "".join(context)
                                }})
                            tagged[author][tag]["logs"].update({commit: {"date": date, "author": author, "log": log, "sha": commit}})
        except:
            print("error: failed to read "+str(f)+" "+str(sys.exc_info()[0]))

    try:
        for tag in tags:
            log_cmd = "git log --all --grep=\""+tag+"\""
            log = subprocess.check_output(log_cmd, shell=True)
            log = log.decode("utf-8")
            if len(log) > 0:
                author = "No Author"
                date = ""
                commit = ""
                log = ""
                for str_line in log.split("\n"):
                    if str_line.startswith("Author: "):
                        author = str_line.split("Author: ")[1][0:]
                    if str_line.startswith("Date: "):
                        date = str_line.split("Date:   ")[1][0:]
                    if str_line.startswith("commit "):
                        commit = str_line.split("commit ")[1][0:]
                if author not in tagged:
                    tagged[author] = {}
                if tag not in tagged[author]:
                    tagged[author][tag] = {}
                if "logs" not in tagged[author][tag]:
                    tagged[author][tag]["logs"] = {}

                tagged[author][tag]["logs"].update({commit: {"date": date, "author": author, "log": log, "sha": commit}})
    except:
        pass

    tagit["tagged"] = tagged
    markdown = ["# Ta-git"]
    for author, tags in tagged.items():
        markdown.append("## "+author)
        for tag, locations in tags.items():
            markdown.append("### "+tag)
            markdown.append("---------")
            items = []
            for key, value in locations["lines"].items():
                items.append([value["date"], value])
            items.sort(key=lambda x: x[0], reverse=True)
            for item in items:
                item[0] = item[0].split(" ")[0]
                markdown.append(tag_format.format_map(item[1]))
            items = []
            markdown.append("## logs")
            for key, value in locations["logs"].items():
                items.append([value["date"], value])
            items.sort(key=lambda x: x[0], reverse=True)
            for item in items:
                item[0] = item[0].split(" ")[0]
                markdown.append(log_format.format_map(item[1]))
    md_dir = os.path.dirname(md_path)
    if md_dir:
        os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(md_path, "w") as out_md:
        out_md.write("\n".join(markdown))
