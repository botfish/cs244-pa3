# cs244-pa3
Reproducing SPDY Test Results
====================================
The goal of this project is to reproduce some of the graphs found in [this paper](https://www.usenix.org/system/files/conference/nsdi14/nsdi14-paper-wang_xiao_sophia.pdf).

Code and tools for this paper were published by the authors [here](http://wprof.cs.washington.edu/spdy/tool/)

More information about SDPY in general can be found [here](https://www.chromium.org/spdy).

Simple Experiment Reproduction
===================================
1. Start an EC2 instance of our AMI image. The image name is "ReproducingSPDY" and the AMI ID is "ami-dd96a9ed". We used a c3.large instance.
2. Start the instance and SSH into it using ```ssh ubuntu@<DNS name>```
3. ```cd cs244-pa3```
4. ```sudo ./run.sh```
5. The results will be in the “result” folder in cs244-pa3

Complete Environment Setup
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
# deb http://old-releases.ubuntu.com/ubuntu/ CODENAME-backports main restricted universe multiverse
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

Add the server objects to Apache:
```
wget http://wprof.cs.washington.edu/spdy/tool/server.tar.gz
tar -xvf server.tar.gz
sudo cp -r server/* /var/www/
```

Python Dependencies
---------------------------------
The graph maker uses the matplotlib and numpy Python libraries. To install:

```
sudo apt-get install python-matplotlib
```

Note: At this point, you could simply use the code in this repository as it is. Further instructions are included to give insights about how we constructed our setup.

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

Remove lines of code that break the client:
1. Open epload/client_spdy/spdy_client/spdy_client/session.js with your preferred text editor
2. Comment out the lines (by putting // in front):
```
  if (!stream_n.isReady())
    return;
```
The isReady() function does not appear to exist, so this will throw an error if not removed

Test Configurations
====================================
The following instructions are not necessary for running our experiments, they
are here for customized experiments.

Test Parameters Adjustments
-----------------------------------
Vim (or your editor) run.sh
```
vim run.sh
```
Paramters -
* ```bwnet``` Bandwidth (Mbps).
* ```delay``` Delay on a single link, RTT/4 (ms).
* ```loss```  Packet loss rate (%).
* ```arr```   An array of the dependency graph name.

Dependency Graph Generation
-----------------------------------
Make a directory on web server to hold testing web pages
```
sudo mkdir /var/www/pages
```
Copy base web objects to server testing page
```
sudo cp -r rawobj.com /var/www/pages
```
Then run gen_dp.py, for example to generate a dependency graph with
64 10K objects.
```
sudo python gen_dp.py -S 10 -N 64 -O dg/10K64.com_/
```
See ``` python gen_dp.py -h ``` for more details.

Epload Specific Configurations
-----------------------------------
Vim (or your editor) run.js
```
vim epload/emulator/run.js
```
Configurations are done by hardcoding into ```options``` variable.
