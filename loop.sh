#!/bin/bash
while true; do
  python3 /home/pi/Microbot/start.py &
  wait $!
  cd /home/pi/Microbot
  git reset --hard HEAD
  git pull
  sleep 10000
  sudo reboot
done
exit