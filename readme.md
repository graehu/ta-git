# ta-git

A little tool for finding #tags and who authored them in git. Right now it only finds things in c++ and python files, because that's my use case.
The greater design ambition is to use it to track work related to bugs in a bug database or docs in a doc database.

At some point I'd like to make it easy to tell what commit a line came from, but I don't want to clutter the output too much.
Just including a sha1 couldn't be that useful. Finally it would also be nice to search commits in the current branch for tags.

Used like so:
```shell
./ta-git.py todo
```

## todos

* Add a path cmdline option
* Add an extensions cmdline option
* Add a tag prefix cmdline option
* More accurate author, atm it's the last person to modify the line.
