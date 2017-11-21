#!/bin/bash
while true; do
  python3 /home/pi/Microbot/start.py &
  wait $!
  pkill -9 python
  cd /home/pi/Microbot
  git reset --hard HEAD
  git pull
  sleep 10
done
exit