#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
MSPATH=$(sed 's/\/scripts//g' <<< $SCRIPTPATH)
MSENV="${MIXWARESCREEN_VENV:-${HOME}/.MixwareScreen-env}"

XSERVER="xinit xinput x11-xserver-utils xserver-xorg-input-evdev xserver-xorg-input-libinput"
FBDEV="xserver-xorg-video-fbdev"
MISC="librsvg2-common libopenjp2-7 libatlas-base-dev wireless-tools libdbus-glib-1-dev autoconf"
OPTIONAL="xserver-xorg-legacy fonts-nanum fonts-ipafont libmpv-dev"
PYQTLIST="python3-pyqt5 python3-pyqt5.qtquick python3-pyqt5.qtserialport qml-module-qt*"

Red='\033[0;31m'
Green='\033[0;32m'
Cyan='\033[0;36m'
Normal='\033[0m'

echo_text ()
{
    printf "${Normal}$1${Cyan}\n"
}

echo_error ()
{
    printf "${Red}$1${Normal}\n"
}

echo_ok ()
{
    printf "${Green}$1${Normal}\n"
}

install_packages()
{
    echo_text "Update package data"
    sudo apt-get update

    echo_text "Checking for broken packages..."
    output=$(dpkg-query -W -f='${db:Status-Abbrev} ${binary:Package}\n' | grep -E ^.[^nci])
    if [ $? -eq 0 ]; then
        echo_text "Detected broken packages. Attempting to fix"
        sudo apt-get -f install
        output=$(dpkg-query -W -f='${db:Status-Abbrev} ${binary:Package}\n' | grep -E ^.[^nci])
        if [ $? -eq 0 ]; then
            echo_error "Unable to fix broken packages. These must be fixed before MixwareScreen can be installed"
            exit 1
        fi
    else
        echo_ok "No broken packages"
    fi

    echo_text "Installing MixwareScreen dependencies"
    sudo apt-get install -y $XSERVER
    if [ $? -eq 0 ]; then
        echo_ok "Installed X"
    else
        echo_error "Installation of X-server dependencies failed ($XSERVER)"
        exit 1
    fi
    sudo apt-get install -y $OPTIONAL
    echo $_
    sudo apt-get install -y $FBDEV
    if [ $? -eq 0 ]; then
        echo_ok "Installed FBdev"
    else
        echo_error "Installation of FBdev failed ($FBDEV)"
        exit 1
    fi
    sudo apt-get install -y $PYTHON
    if [ $? -eq 0 ]; then
        echo_ok "Installed Python dependencies"
    else
        echo_error "Installation of Python dependencies failed ($PYTHON)"
        exit 1
    fi
    sudo apt-get install -y $MISC
    if [ $? -eq 0 ]; then
        echo_ok "Installed Misc packages"
    else
        echo_error "Installation of Misc packages failed ($MISC)"
        exit 1
    fi
	  sudo apt-get install -y $PYQTLIST
    if [ $? -eq 0 ]; then
        echo_ok "Installed PyQt packages"
    else
        echo_error "Installation of PyQt packages failed ($PYQTLIST)"
        exit 1
    fi
}

pip_requirements()
{
    echo_text "Install pip requirements"

    pip --disable-pip-version-check install -r ${MSPATH}/scripts/MixwareScreen-requirements.txt
    if [ $? -gt 0 ]; then
        echo_error "Error: pip install exited with status code $?"
        echo_text "Trying again with new tools..."
        sudo apt-get install -y build-essential cmake
        pip install --upgrade pip setuptools
        pip install -r ${MSPATH}/scripts/MixwareScreen-requirements.txt
        if [ $? -gt 0 ]; then
            echo_error "Unable to install dependencies, aborting install"
            deactivate
            exit 1
        fi
    fi
    # deactivate
    echo_ok "Pip requirements installed"
}

install_systemd_service()
{
    echo_text "Installing MixwareScreen unit file"

    SERVICE=$(<$SCRIPTPATH/MixwareScreen.service)
    MSPATH_ESC=$(sed "s/\//\\\\\//g" <<< $MSPATH)
    MSENV_ESC=$(sed "s/\//\\\\\//g" <<< $MSENV)

    SERVICE=$(sed "s/MS_USER/$USER/g" <<< $SERVICE)
    SERVICE=$(sed "s/MS_ENV/$MSENV_ESC/g" <<< $SERVICE)
    SERVICE=$(sed "s/MS_DIR/$MSPATH_ESC/g" <<< $SERVICE)

    echo "$SERVICE" | sudo tee /etc/systemd/system/MixwareScreen.service > /dev/null
    sudo systemctl unmask MixwareScreen.service
    sudo systemctl daemon-reload
    sudo systemctl enable MixwareScreen
}

modify_user()
{
    sudo usermod -a -G tty $USER
}

update_x11()
{
    if [ -e /etc/X11/Xwrapper.config ]
    then
        echo_text "Updating X11 Xwrapper"
        sudo sed -i 's/allowed_users=console/allowed_users=anybody/g' /etc/X11/Xwrapper.config
    else
        echo_text "Adding X11 Xwrapper"
        echo 'allowed_users=anybody' | sudo tee /etc/X11/Xwrapper.config
    fi
}

start_MixwareScreen()
{
    echo_text "Starting service..."
    sudo systemctl stop MixwareScreen
    sudo systemctl start MixwareScreen
}

if [ "$EUID" == 0 ]
    then echo_error "Please do not run this script as root"
    exit 1
fi
install_packages
pip_requirements
modify_user
install_systemd_service
update_x11
echo_ok "MixwareScreen was installed"
start_MixwareScreen
