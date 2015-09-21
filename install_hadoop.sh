#!/usr/bin/sh

# Shell script to install hadoop with pydoop for OSX
# Reference: https://getblueshift.com/setting-up-hadoop-2-4-and-pig-0-12-on-osx-locally/

brew install python
brew install openssl
pip install importlib
pip install argparse
brew install hadoop
echo 'export JAVA_HOME="$(/usr/libexec/java_home)"' >> ~/.bashrc
echo 'export HADOOP_CONF_DIR=/usr/local/Cellar/hadoop/2.7.1/libexec/etc/hadoop/' >> ~/.bashrc
echo 'export HADOOP_HOME=/usr/local/Cellar/hadoop/2.7.1/libexec/' >> ~/.bashrc
brew update
pip install pydoop

'''
ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys

echo "Please turn on Remote Login in System Sharing"

# Install pig
brew install pig
echo 'export PIG_Home=/usr/local/Cellar/pig/0.15.0' >> ~/.bashrc

source ~/.bashrc
'''