#!/bin/bash

echo "Uninstalling MixwareScreen"
echo ""
echo "* Stopping service"
sudo service MixwareScreen stop
echo "* Removing unit file"
sudo rm /etc/systemd/system/MixwareScreen.service
echo "* Removing enviroment"
sudo rm -rf ~/.MixwareScreen-env
echo "!! Please remove $(dirname `pwd`) manually"
echo "Done"
