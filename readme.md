# ta-git

A little tool for finding #tags and who authored them in git. Right now it only finds things in c++ and python files, because that's my use case.
The greater design ambition is to use it to track work related to bugs in a bug database or docs in a doc database.

At some point I'd like to make it easy to tell what commit a line came from, but I don't want to clutter the output too much.
Just including a sha1 couldn't be that useful. Finally it would also be nice to search commits in the current branch for tags.

Used like so:
```shell
./ta-git.py todo
```
Which outputs this when used in my framework:
```json
{
    "Graham Hughes <graehu@gmail.com>": {
        "#todo": [
            "src/graphics/camera/camera.cpp:10:: make this camera more user friendly. probably need to add deceleration\n",
            "src/graphics/camera/camera.cpp:71:: Find out why normalising here isn't going well.\n",
            "src/application/rc_sample/rc_sample.cpp:46:: test this because i don't think it works.\n",
            "src/networking/connection/socket.cpp:157:: do something about this random limit here.\n",
            "src/networking/connection/http_server.cpp:45:: find out exactly how unsafe this is.\n",
            "src/networking/connection/http_server.cpp:51:: test a smaller packet.\n",
            "src/networking/connection/http_server.cpp:153:: this should be a string_view but emacs wont stop complaining.\n",
            "src/networking/connection/http_server.cpp:175:: Move this to a custom handler and support multiple custom handlers.\n",
            "src/networking/connection/http_server.cpp:192:: generate different GUIDs?\n",
            "src/networking/connection/http_server.cpp:224:: check for multiple custom handlers.\n",
            "src/networking/connection/http_server.cpp:240:: move this not handled code into a func, if possible\n",
            "src/networking/connection/http_server.cpp:249:: return access denied code.\n",
            "src/networking/connection/http_server.cpp:269:: this assumes about a 500kbs download speed.\n",
            "src/networking/connection/http_server.cpp:377:: test if this is thread safe\n",
            "src/networking/connection/http_server.cpp:382:: split packets that are too big for websocket, or bail\n",
            "src/physics/rigidBody.cpp:18:: this needs to be done differently.\n",
            "src/utils/log/log.cpp:137:: locks are a bit wide here.\n",
            "src/utils/tmxloader/TMXLoader.cpp:36:: for performance, we may not want to return true for each of these callbacks for the visitor pattern.\n",
            "src/utils/tmxloader/TMXLoader.cpp:53:: get width and height, and tilewidth and tileheight\n",
            "src/utils/tmxloader/TMXLoader.cpp:66:: get spacing and margin\n",
            "src/types/mat4x4f.h:4:: This file does not follow current conventions. Fix this.\n",
            "src/types/quaternion.h:8:: verify epsilon value and usage\n",
            "src/networking/connection/http_server.h:29:: accept multiple handlers\n",
            "src/networking/packet/packet.h:122:: make safe?\n",
            "src/networking/packet/packet.h:129:: make safe?\n",
            "src/networking/utils/dataUtils.h:32:: Find a way to do this in a more generic way\n",
            "src/utils/params.h:18:: remove top level params mutex and add per param mutexes. write only locks?\n",
            "src/utils/params.h:19:: add \"get_param\" returning const param object.\n",
            "src/utils/params.h:20:: auto migrate subscriptions from parents to params that don't exist yet.\n"
        ]
    },
    "No Author": {
        "#todo": [
            "tools/ta-git/ta-git.py:11:: add prefix support cmdline option\n",
            "tools/ta-git/ta-git.py:16:: add extension cmdline option\n",
            "tools/confply/confply/log.py:6:: add formatted() for a formatted log function\n",
            "tools/confply/confply/__init__.py:144:: make this import one tool at a time, like previous import_cache behaviour\n"
        ]
    }
}
```

## todos

* Add a path cmdline option
* Add an extensions cmdline option
* Add a tag prefix cmdline option
* More accurate author, atm it's the last person to modify the line.
