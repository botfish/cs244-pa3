#!/bin/bash
cp $1 /etc/apache2/mods-available/spdy.conf
service apache2 restart
