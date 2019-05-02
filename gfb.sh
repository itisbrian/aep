#!/bin/bash
#############################################################
#   _______     _______ _               ____
#  / ____\ \   / / ____| |        /\   |  _ \
# | (___  \ \_/ / (___ | |       /  \  | |_) |
#  \___ \  \   / \___ \| |      / /\ \ |  _ <
#  ____) |  | |  ____) | |____ / ____ \| |_) |
# |_____/   |_| |_____/|______/_/    \_\____/


#   _____ _    _ _____  _____  ______ __  __ ______
#  / ____| |  | |  __ \|  __ \|  ____|  \/  |  ____|
# | (___ | |  | | |__) | |__) | |__  | \  / | |__
#  \___ \| |  | |  ___/|  _  /|  __| | |\/| |  __|
#  ____) | |__| | |    | | \ \| |____| |  | | |____
# |_____/ \____/|_|    |_|  \_\______|_|  |_|______|


#by:
#Patrick Geary : patrickg@supermicro.com
#Brian Chen : brianchen@supermicro.com


####################################################################
################################################ SUPREME ###############################
echo ""
echo ""
echo -e "           \e[32m███████\e[0m╗\e[32m██\e[0m╗   \e[32m██\e[0m╗\e[32m███████\e[0m╗\e[32m██\e[0m╗      \e[32m█████\e[0m╗ \e[32m██████\e[0m╗ "
echo -e "           \e[32m██\e[0m╔════╝╚\e[32m██\e[0m╗ \e[32m██\e[0m╔╝\e[32m██\e[0m╔════╝\e[32m██\e[0m║     \e[32m██\e[0m╔══\e[32m██\e[0m╗\e[32m██\e[0m╔══\e[32m██\e[0m╗"
echo -e "           \e[32m███████\e[0m╗ ╚\e[32m████\e[0m╔╝ \e[32m███████\e[0m╗\e[32m██\e[0m║     \e[32m███████\e[0m║\e[32m██████\e[0m╔╝"
echo -e "           ╚════\e[32m██\e[0m║  ╚\e[32m██\e[0m╔╝  ╚════\e[32m██\e[0m║\e[32m██\e[0m║     \e[32m██\e[0m╔══\e[32m██\e[0m║\e[32m██\e[0m╔══\e[32m██\e[0m╗"
echo -e "           \e[32m███████\e[0m║   \e[32m██\e[0m║   \e[32m███████\e[0m║\e[32m███████\e[0m╗\e[32m██\e[0m║  \e[32m██\e[0m║\e[32m██████\e[0m╔╝"
echo -e "           ╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ "
echo " "
echo -e " \e[5m                         SYSLAB GREEN FIREBALL AEP Tester.\e[25m"
echo -e "\e[32m                report errors to patrickg@supermicro.com brianchen@supermicro.com \e[0m"
echo " "
echo "--------------------------------------------------------------------------------------------------------------------------------"
sleep 5


#################################################################################################
IP=westworld.bnet
echo "Host : ${IP}"
echo " "
#####################################################################
#installing python 2.7

yum install -y python2

#####################################################################

#==========================================================================================================================
#==========================================================================================================================

function gfbcreate {

mkdir -p /root/green_fireball
mkdir -p /root/green_fireball/run
mkdir -p /root/green_fireball/pg-generic-py
mkdir -p /root/green_fireball/pg-generic-py/pggenericpy
mkdir -p /root/green_fireball/lib
mkdir -p /root/green_fireball/lib/aep_gfb
mkdir -p /root/green_fireball/bin


}
#==========================================================================================================================
#blank wget template

#____________________________________________________________________________________________________________________
#Get 
#wget "http://${IP}/aep/" -O "/root/" &> /dev/null
#if [ $? -ne 0 ]
# then
#	echo "Failed to acquire for GFB." 
#	echo "Exiting." 
#       exit 1
#fi
#echo " installed." 



#==========================================================================================================================

function gfbdownload {

#____________________________________________________________________________________________________________________
# Get Service
wget "http://${IP}/aep/systemd/gfb_validate@.service" -O "/lib/systemd/system/gfb_validate@.service" &> /dev/null
if [ $? -ne 0 ]
 then
	echo "Failed to acquire getty service for GFB. (gfb_validate@.service)" 
	echo "Exiting." 
    exit 1
fi
echo "GFB Service installed." 


wget "http://${IP}/aep/gfb_install" -O "/root/green_fireball/gfb_install" &> /dev/null
if [ $? -ne 0 ]
 then
	echo "Failed to acquire main installer service for GFB. (gfb_install)" 
	echo "Exiting." 
    exit 1
fi
echo "GFB main installer installed." 


wget "http://${IP}/aep/gfb_validate" -O "/root/green_fireball/gfb_validate" &> /dev/null
if [ $? -ne 0 ]
 then
	echo "Failed to acquire main validator service for GFB. (gfb_validate)" 
	echo "Exiting." 
    exit 1
fi
echo "GFB main validator installed." 




#  .o8        o8o              
# "888        `"'              
#  888oooo.  oooo  ooo. .oo.   
#  d88' `88b `888  `888P"Y88b  
#  888   888  888   888   888  
#  888   888  888   888   888  
#  `Y8bod8P' o888o o888o o888o 
                             
                             
                             


#____________________________________________________________________________________________________________________
#Get gfb_reset
wget "http://${IP}/aep/bin/gfb_reset" -O "/root/green_fireball/bin/gfb_reset" &> /dev/null
wget "http://${IP}/aep/bin/gfb_reset" -O "/usr/local/sbin/gfb_reset" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire gfb_reset for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB Reset installed." 


#____________________________________________________________________________________________________________________
#Get gfb_stop
wget "http://${IP}/aep/bin/gfb_stop" -O "/root/green_fireball/bin/gfb_stop" &> /dev/null
wget "http://${IP}/aep/bin/gfb_stop" -O "/usr/local/sbin/gfb_stop" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire gfb_stop for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB Stop installed." 

#____________________________________________________________________________________________________________________
#Get gfb_start
wget "http://${IP}/aep/bin/gfb_start" -O "/root/green_fireball/bin/gfb_start" &> /dev/null
wget "http://${IP}/aep/bin/gfb_start" -O "/usr/local/sbin/gfb_start" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire gfb_start for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB Start installed." 
#____________________________________________________________________________________________________________________
#Get gfb_push
wget "http://${IP}/aep/bin/gfb_push" -O "/root/green_fireball/bin/gfb_push" &> /dev/null
wget "http://${IP}/aep/bin/gfb_push" -O "/usr/local/sbin/gfb_push" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire gfb_push for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB Push installed." 

                                          
                                          
#  .ooooo.  oooo    ooo  .ooooo.   .ooooo.  
# d88' `88b  `88b..8P'  d88' `88b d88' `"Y8 
# 888ooo888    Y888'    888ooo888 888       
# 888    .o  .o8"'88b   888    .o 888   .o8 
# `Y8bod8P' o88'   888o `Y8bod8P' `Y8bod8P' 
                                          
                                          
                                          





#____________________________________________________________________________________________________________________
#Get daxctl
wget "http://${IP}/aep/exec/daxctl" -O "/usr/bin/daxctl" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire for daxctl GFB." 
	echo "Exiting." 
    exit 1
fi
echo "Daxctl installed." 

#____________________________________________________________________________________________________________________
#Get ipmctl
wget "http://${IP}/aep/exec/ipmctl" -O "/usr/bin/ipmctl" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire ipmctl for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "Ipmctl installed." 

#____________________________________________________________________________________________________________________
#Get ndctl
wget "http://${IP}/aep/exec/ndctl" -O "/usr/bin/ndctl" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire ndctl for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "Ndctl installed." 


#____________________________________________________________________________________________________________________
#Get fio
wget "http://${IP}/aep/exec/fio" -O "/usr/local/bin/fio" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire FIO for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "FIO installed." 





# oooo   o8o   .o8       
# `888   `"'  "888       
#  888  oooo   888oooo.  
#  888  `888   d88' `88b 
#  888   888   888   888 
#  888   888   888   888 
# o888o o888o  `Y8bod8P' 
                       
                       
                       



#____________________________________________________________________________________________________________________
#Get GFB init.py
wget "http://${IP}/aep/lib/aep_gfb/__init__.py" -O "/root/green_fireball/lib/aep_gfb/__init__.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire init.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB init.py installed." 

#____________________________________________________________________________________________________________________
#Get aep_gfb.py
wget "http://${IP}/aep/lib/aep_gfb/aep_gfb.py" -O "/root/green_fireball/lib/aep_gfb/aep_gfb.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire aep_gfb.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB aep_gfb.py installed." 

#____________________________________________________________________________________________________________________
#Get config.py
wget "http://${IP}/aep/lib/aep_gfb/config.py" -O "/root/green_fireball/lib/aep_gfb/config.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire config.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB config.py installed." 

#____________________________________________________________________________________________________________________
#Get fio.py
wget "http://${IP}/aep/lib/aep_gfb/fio.py" -O "/root/green_fireball/lib/aep_gfb/fio.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire fio.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB fio.py installed." 

#____________________________________________________________________________________________________________________
#Get generic.py
wget "http://${IP}/aep/lib/aep_gfb/generic.py" -O "/root/green_fireball/lib/aep_gfb/generic.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire generic.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB generic.py installed." 

#____________________________________________________________________________________________________________________
#Get ipmctl.py
wget "http://${IP}/aep/lib/aep_gfb/ipmctl.py" -O "/root/green_fireball/lib/aep_gfb/ipmctl.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire ipmctl.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB ipmctl.py installed." 

#____________________________________________________________________________________________________________________
#Get ndctl.py
wget "http://${IP}/aep/lib/aep_gfb/ndctl.py" -O "/root/green_fireball/lib/aep_gfb/ndctl.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire ndctl.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB ndctl.py installed." 

#____________________________________________________________________________________________________________________
#Get installer
wget "http://${IP}/aep/lib/install" -O "/root/green_fireball/lib/install" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire installer for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB installer installed." 

#____________________________________________________________________________________________________________________
#Get setup.cfg
wget "http://${IP}/aep/lib/setup.cfg" -O "/root/green_fireball/lib/setup.cfg" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire setup.cfg for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB setup.cfg installed." 

#____________________________________________________________________________________________________________________
#Get setup.py
wget "http://${IP}/aep/lib/setup.py" -O "/root/green_fireball/lib/setup.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire setup.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB setup.py installed." 





# oooo   o8o   .o8                .ooo         .o   
# `888   `"'  "888              .88'         .d88   
#  888  oooo   888oooo.        d88'        .d'888   
#  888  `888   d88' `88b      d888P"Ybo. .d'  888   
#  888   888   888   888      Y88[   ]88 88ooo888oo 
#  888   888   888   888      `Y88   88P      888   
# o888o o888o  `Y8bod8P'       `88bod8'      o888o  
                                                  
                                                  
                                                  








#____________________________________________________________________________________________________________________
#Get libdaxctl.so
wget "http://${IP}/aep/lib64/libdaxctl.so" -O "/usr/lib64/libdaxctl.so" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libdaxctl.so for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libdaxctl.so installed." 

#____________________________________________________________________________________________________________________
#Get libdaxctl.so.1
wget "http://${IP}/aep/lib64/libdaxctl.so.1" -O "/usr/lib64/libdaxctl.so.1" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libdaxctl.so.1 for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libdaxctl.so.1 installed." 

#____________________________________________________________________________________________________________________
#Get libdaxctl.so.1.2.0
wget "http://${IP}/aep/lib64/libdaxctl.so.1.2.0" -O "/usr/lib64/libdaxctl.so.1.2.0" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libdaxctl.so.1.2.0 for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libdaxctl.so.1.2.0 installed." 

#____________________________________________________________________________________________________________________
#Get libipmctl.so
wget "http://${IP}/aep/lib64/libipmctl.so" -O "/usr/lib64/libipmctl.so" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libipmctl.so for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libipmctl.so installed." 

#____________________________________________________________________________________________________________________
#Get libipmctl.so.3
wget "http://${IP}/aep/lib64/libipmctl.so.3" -O "/usr/lib64/libipmctl.so.3" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libipmctl.so.3 for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libipmctl.so.3 installed." 

#____________________________________________________________________________________________________________________
#Get libipmctl.so.3.0.0
wget "http://${IP}/aep/lib64/libipmctl.so.3.0.0" -O "/usr/lib64/libipmctl.so.3.0.0" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libipmctl.so.3.0.0 for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libipmctl.so.3.0.0 installed." 

#____________________________________________________________________________________________________________________
#Get libipmctl.so.3.1.0
wget "http://${IP}/aep/lib64/libipmctl.so.3.1.0" -O "/usr/lib64/libipmctl.so.3.1.0" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libipmctl.so.3.1.0 for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libipmctl.so.3.1.0 installed." 

#____________________________________________________________________________________________________________________
#Get libndctl.so
wget "http://${IP}/aep/lib64/libndctl.so" -O "/usr/lib64/libndctl.so" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libndctl.so for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libndctl.so installed." 

#____________________________________________________________________________________________________________________
#Get libndctl.so.6
wget "http://${IP}/aep/lib64/libndctl.so.6" -O "/usr/lib64/libndctl.so.6" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libndctl.so.6 for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libndctl.so.6 installed." 

#____________________________________________________________________________________________________________________
#Get libndctl.so.6.11.0
wget "http://${IP}/aep/lib64/libndctl.so.6.11.0" -O "/usr/lib64/libndctl.so.6.11.0" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libndctl.so.6.11.0 for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libndctl.so.6.11.0 installed." 

#____________________________________________________________________________________________________________________
#Get libndctl.so.6.12.0
wget "http://${IP}/aep/lib64/libndctl.so.6.12.0" -O "/usr/lib64/libndctl.so.6.12.0" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libndctl.so.6.12.0 for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libndctl.so.6.12.0 installed." 

#____________________________________________________________________________________________________________________
#Get libsafec-3.3.so
wget "http://${IP}/aep/lib64/libsafec-3.3.so" -O "/usr/lib64/libsafec-3.3.so" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libsafec-3.3.so for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libsafec-3.3.so installed." 

#____________________________________________________________________________________________________________________
#Get libsafec-3.3.so.3
wget "http://${IP}/aep/lib64/libsafec-3.3.so.3" -O "/usr/lib64/libsafec-3.3.so.3" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libsafec-3.3.so.3 for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libsafec-3.3.so.3 installed." 

#____________________________________________________________________________________________________________________
#Get libsafec-3.3.so.3.0.3
wget "http://${IP}/aep/lib64/libsafec-3.3.so.3.0.3" -O "/usr/lib64/libsafec-3.3.so.3.0.3" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire libsafec-3.3.so.3.0.3 for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "GFB libsafec-3.3.so.3.0.3 installed." 






# ooooooooo.     .oooooo.         ooooooooo.   oooooo   oooo 
# `888   `Y88.  d8P'  `Y8b        `888   `Y88.  `888.   .8'  
#  888   .d88' 888                 888   .d88'   `888. .8'   
#  888ooo88P'  888                 888ooo88P'     `888.8'    
#  888         888     ooooo       888             `888'     
#  888         `88.    .88'        888              888      
# o888o         `Y8bood8P'        o888o            o888o     
                                                           
                                                           
                                                           

                           









#____________________________________________________________________________________________________________________
#Get pg __init__.py
wget "http://${IP}/aep/pg-generic-py/pggenericpy/__init__.py" -O "/root/green_fireball/pg-generic-py/pggenericpy/__init__.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire pg init.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "PG init.py installed." 

#____________________________________________________________________________________________________________________
#Get pg curl.py
wget "http://${IP}/aep/pg-generic-py/pggenericpy/curl.py" -O "/root/green_fireball/pg-generic-py/pggenericpy/curl.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire pg for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "PG installed." 

#____________________________________________________________________________________________________________________
#Get pg generic.py
wget "http://${IP}/aep/pg-generic-py/pggenericpy/generic.py" -O "/root/green_fireball/pg-generic-py/pggenericpy/generic.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire pg generic.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "PG generic.py installed." 

#____________________________________________________________________________________________________________________
#Get pg ipmi.py
wget "http://${IP}/aep/pg-generic-py/pggenericpy/ipmi.py" -O "/root/green_fireball/pg-generic-py/pggenericpy/ipmi.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire pg ipmi.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "PG ipmi.py installed." 

#____________________________________________________________________________________________________________________
#Get pg system.py
wget "http://${IP}/aep/pg-generic-py/pggenericpy/system.py" -O "/root/green_fireball/pg-generic-py/pggenericpy/system.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire pg system.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "PG system.py installed." 

#____________________________________________________________________________________________________________________
#Get pg xml.py
wget "http://${IP}/aep/pg-generic-py/pggenericpy/xml.py" -O "/root/green_fireball/pg-generic-py/pggenericpy/xml.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire pg xml.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "PG xml.py installed." 



#____________________________________________________________________________________________________________________
#Get pg installer
wget "http://${IP}/aep/pg-generic-py/install" -O "/root/green_fireball/pg-generic-py/install" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire pg installer for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "PG isntaller installed." 

#____________________________________________________________________________________________________________________
#Get pg setup.cfg
wget "http://${IP}/aep/pg-generic-py/setup.cfg" -O "/root/green_fireball/pg-generic-py/setup.cfg" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire pg setup.cfg for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "PG setup.cfg installed." 

#____________________________________________________________________________________________________________________
#Get pg setup.py
wget "http://${IP}/aep/pg-generic-py/setup.py" -O "/root/green_fireball/pg-generic-py/setup.py" &> /dev/null
if [ $? -ne 0 ]
then
	echo "Failed to acquire pg setup.py for GFB." 
	echo "Exiting." 
    exit 1
fi
echo "PG setup.py installed." 


}

#==========================================================================================================================
#==========================================================================================================================

function gfbcheck {


echo " "
}

#==========================================================================================================================
#==========================================================================================================================

function gfbchmod	 {

chmod +x /root/green_fireball/bin/gfb_start
chmod +x /root/green_fireball/bin/gfb_stop
chmod +x /root/green_fireball/bin/gfb_reset
chmod +x /root/green_fireball/bin/gfb_push

chmod +x /usr/local/sbin/gfb_start
chmod +x /usr/local/sbin/gfb_stop
chmod +x /usr/local/sbin/gfb_reset
chmod +x /usr/local/sbin/gfb_push

chmod +x /usr/local/bin/fio

chmod +x /usr/bin/ipmctl
chmod +x /usr/bin/ndctl
chmod +x /usr/bin/daxctl

chmod +x /root/green_fireball/gfb_install
chmod +x /root/green_fireball/gfb_validate

chmod +x /root/green_fireball/lib/install



}

gfbcreate
gfbdownload
gfbchmod


ln -s /root/green_fireball/lib/aep_gfb /root/green_fireball/aep_gfb
if [ $? -ne 0 ]
then
	echo "Failed to link directories." 
	echo "Exiting." 
    exit 1
fi
echo "aep_gfb directories linked." 
/usr/bin/systemctl daemon-reload
if [ $? -ne 0 ]
then
	echo "Failed to reload services." 
	echo "Exiting." 
    exit 1
fi


/root/green_fireball/gfb_install



echo "Services reloaded."
echo " " 
echo "--------------------------------------------------------------------------------------------------------------------------------"
echo " "
echo "GFB installer finished."
echo " "
echo "Start               : ./root/green_fireball/bin/gfb_start"
echo "Stop                : ./root/green_fireball/bin/gfb_stop"
echo "Reset               : ./root/green_fireball/bin/gfb_reset"
echo "Push Files to cburn : ./root/green_fireball/bin/gfb_push"
echo " "
echo "GFB will execute on Alt + F7"
echo "'Tests completed successfully.' will be displayed on Alt F7 when all tests are finished."
echo " "
echo "End of installer."
echo "--------------------------------------------------------------------------------------------------------------------------------"