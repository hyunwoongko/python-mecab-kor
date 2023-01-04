#! /bin/bash

# Determine sudo
if hash "sudo" &>/dev/null; then
    sudo="sudo"
else
    sudo=""
fi

python="python3"
if hash "pyenv" &>/dev/null; then
    python="python"
fi

os=$(uname)
if [[ ! $os == "Linux" ]] && [[ ! $os == "Darwin" ]]; then
    echo "This script does not support this OS."
    echo "Try consulting https://github.com/hyunwoongko/python-mecab-kor/issues"
    exit 0
fi

install_requirements(){
    if [ "$os" == "Linux" ]; then
        if [ "$(grep -Ei 'debian|buntu|mint' /etc/*release)" ]; then
            $sudo apt-get update && $sudo apt-get install build-essential curl python3-dev libmecab-dev git -y
        elif [ "$(grep -Ei 'fedora|redhat' /etc/*release)" ]; then
            $sudo yum groupinstall 'Development Tools' 'Development Libraries' -y && $sudo yum install curl python3-devel git -y
        fi
    elif [ "$os" == "Darwin" ]; then
        if [[ $(command -v brew) == "" ]]; then
            echo "This script require Homebrew!"
            echo "Try https://brew.sh/"
            exit 0
        fi
        if [[ $(uname -m) == 'arm64' ]]; then
          $sudo arch -arm64 brew install curl git
        else
          $sudo brew install curl git
        fi
    fi
}

install_requirements
