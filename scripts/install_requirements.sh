#! /bin/bash

# Determine sudo
if hash "sudo" &>/dev/null; then
    sudo="sudo"
else
    sudo=""
fi

os=$(uname)
if [[ ! $os == "Linux" ]] && [[ ! $os == "Darwin" ]]; then
    echo "This script does not support this OS."
    echo "Try consulting https://github.com/hyunwoongko/python-mecab-kor/issues"
    exit 0
fi

install_requirements(){
    # TODO: if not [automake --version]
    if [ "$os" == "Linux" ]; then
        if [ "$(grep -Ei 'debian|buntu|mint' /etc/*release)" ]; then
            $sudo apt-get update && $sudo apt-get install -y build-essential wget python3-devel
        elif [ "$(grep -Ei 'fedora|redhat' /etc/*release)" ]; then
            $sudo yum groupinstall -y  'Development Tools' -y && $sudo yum install -y wget python3-devel
        fi
    elif [ "$os" == "Darwin" ]; then
        if [[ $(command -v brew) == "" ]]; then
            echo "This script require Homebrew!"
            echo "Try https://brew.sh/"
            exit 0
        fi
        brew install wget
    fi
}

install_requirements