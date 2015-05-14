# cs244-pa3
Reproducing SPDY Test Results
====================================
The goal of this project is to reproduce some of the graphs found in [this paper](https://www.usenix.org/system/files/conference/nsdi14/nsdi14-paper-wang_xiao_sophia.pdf).

Code and tools for this paper were published by the authors [here](https://www.usenix.org/system/files/conference/nsdi14/nsdi14-paper-wang_xiao_sophia.pdf).

More information about SDPY in general can be found [here](https://www.chromium.org/spdy).

Environment Setup
====================================
The starting system was a VM provided by CS 244 for Project 2.
AMI ID: CS244-Win13-Mininet (ami-7eab204e)
OS: Ubuntu 12.10 LTS 64-bit (in contrast, the original SPDY paper used 12.04)

To use the repositories for this old Ubuntu version, change /etc/apt/sources.list to:
```
## EOL upgrade sources.list
# Required
deb http://old-releases.ubuntu.com/ubuntu/ CODENAME main restricted universe multiverse
deb http://old-releases.ubuntu.com/ubuntu/ CODENAME-updates main restricted universe multiverse
deb http://old-releases.ubuntu.com/ubuntu/ CODENAME-security main restricted universe multiverse

# Optional
#deb http://old-releases.ubuntu.com/ubuntu/ CODENAME-backports main restricted universe multiverse
```

Installing Apache Webserver
-----------------------------------
```
sudo apt-get install apache2
sudo service apache2 restart
```
The paper used Apache 2.2.2 - the lastest version (2.4.7) is not supported by the SPDY module. 2.2.22 should be the default version installed for Ubuntu 12.xx versions.
(Official Ubuntu installation instructions can be found [here](https://help.ubuntu.com/community/ApacheMySQLPHP))

To install the SPDY module:
```
wget https://dl-ssl.google.com/dl/linux/direct/mod-spdy-beta_current_amd64.deb
sudo dpkg -i mod-spdy-beta_current_amd64.deb 
sudo service apache2 restart
```

Installing SDPY Client
-----------------------------------
Install the node.js dependency:
```
sudo apt-get install nodejs npm
sudo npm cache clean -f
sudo npm install -g n
sudo n stable
```

Install the SPDY module of node.js:
```
npm config set registry http://registry.npmjs.org/
sudo npm install spdy
```

Download the client:
```
wget http://wprof.cs.washington.edu/spdy/tool/epload.tar.gz
tar -xvf epload.tar.gz 
```




