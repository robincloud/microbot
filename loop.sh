#!/bin/bash
while true; do
  python3 /home/pi/Microbot/Run.py &
  wait $!
  sleep 10
done
exit