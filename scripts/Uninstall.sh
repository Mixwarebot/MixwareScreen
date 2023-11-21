#!/bin/bash

echo "Uninstalling MixwareScreen"
echo ""
echo "* Stopping service"
sudo service MixwareScreen stop
echo "* Removing unit file"
sudo rm /etc/systemd/system/MixwareScreen.service
echo "!! Please remove $(dirname `pwd`) manually"
echo "Done"
