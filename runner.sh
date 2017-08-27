#!/bin/bash
if [ $(redis-cli PING) != "PONG" ]; then
    redis-server &
fi

export FLASK_APP='./app.py'

( cd ./flask_app/tweetscanner && python ./startream.py & )
( cd ./flask_app && flask run )



