#!/bin/bash
while true; do
  python3 /home/pi/Microbot/Run.py &
  wait $!
  sudo reboot
done
exit