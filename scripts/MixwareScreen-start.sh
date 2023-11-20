#!/bin/bash

SCRIPTPATH=$(dirname $(realpath $0))
if [ -f $SCRIPTPATH/launch_MixwareScreen.sh ]
then
echo "Running "$SCRIPTPATH"/launch_MixwareScreen.sh"
$SCRIPTPATH/launch_MixwareScreen.sh
exit $?
fi

echo "Running MixwareScreen on X in display :0 by default"
/usr/bin/xinit $MS_XCLIENT
