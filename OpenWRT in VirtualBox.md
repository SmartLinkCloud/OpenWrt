# OpenWRT in VirtualBox



If you are considering to test OpenWRT without a router or you don’t want to flash the router firmware over and over again. Here is the right place for you.

OpenWRT in VirtualBox is an image file run in VirtualBox. By the time I write this article, the VirtualBox & OpenWRT image version are Ver 4.1.20 and 10.03.1 respectively. 
 
 

Download

VirtualBox 4.1.20 for Windows hosts x86/amd64

OperWrt image file for VirtualBox ver 10.03.1 (This one not work for me, ext-2 error and read only file system occur)

 Raw image (This one work for me. See below to convert to vdi format)

 

Convert img to native VirtualBox format

    Unzip the raw image to VirtualBox folder (C:\Program Files\Oracle\VirtualBox)
    Open Ms DOS Command Prompt
    Enter C:\Program Files\Oracle\VirtualBox (This is the location where virtualbox install)
    Enter VBoxManage convertfromraw --format VDI openwrt-x86-generic-combined-ext4.img openwrt.vdi
    Now you have a new vdi file named openwrt.vdi

If you don't want to scratch your head to converting the vdi file. Here I provided a converted vdi which the network is already configure nicely.

 

Install VirtualBox

    Run VirtualBox-4.1.20-80170-Win.exe
    Follow on screen instructions until complete installation (always use default settings)

 

Setup VirtualBox

    Run VirtualBox
    VirtualBox main screen should appear as shown in figure below.
    Click New to create a new Virtual Machine.
    Click Next to continue.

VirtualBox Main Screen

 

    Choose a name for the machine, it can be any name. Here I use OpenWRT
    Choose Linux for the Operating System
    Choose Linux 2.6 for Version
    Click Next to continue  as shown in figure below

Create New Virtual Machine

 

    Select the amount of memory, keep the default setting.
    Click Next to continue

Select the amount of memory

 

    Choose Use existing hard disk since you want to use the OpenWRT image file as the new virtual disk
    Click the file icon to select the OpenWRT image file as shown in figure below
    Click Next to continue
    Finally click Create button to finish

Virtual Hard Disk

 

Starting OpenWRT in VirtualBox

VirtualBox with OpenWRT virtual machine

 

OpenWRT just stop working due to OpenWRT vdi image file does not support SATA Controller. 

VirtualBox stop working under SATA Controller

 

Figure below shows  the Storage settings where OpenWRT vdi image file is loaded under SATA Controller. We must move the image file from SATA Controller to IDE Controller

     Click on Settings icon
    Click on Storage section
    Right click SATA Controller
    Select Remove Controller

VirtualBox SATA Controller Settings not working

 

    Right click IDE Controller
    Select Choose existing disk
    Select OpenWRT vdi image file as shown in figure below

VirtualBox IDE Controller Settings

 

Again OpenWRT stop working as shown in figure below. To solve this problem we have to enable Serial Port with Port Mode disconnected.

VirtualBox stop working without Serial Port enable 

 

Just enable serial port without touching other settings.

VirtualBox Serial Port Settings

 

Start the VM (You must press Enter virtual machine boots but doesn't activate the console), OpenWRT is running as shown in figure below.

OpenWRT in VirtualBox

 

Setting up Network

I configured two network adapters for the virtual machine. The first adapter use "NAT" & the second adapter use "Bridge". The first adapter allows you to download additional OpenWrt software packages via the internet connection of the host system. While the second network adapter is connected to the Ethernet adapter of the host system, which itself could then be connected to the network switch.

VirtualBox Network Adapter1 Settings

VirtualBox Network Adapter2 Settings

 

Modify Network Configuration File

The /etc/config/network configuration must match with the above network system. Use vim to edit the file.
vim /etc/config/network
vim /etc/config/network
# Copyright (C) 2006 OpenWrt.org
 
config interface loopback
        option ifname   lo
        option proto    static
        option ipaddr   127.0.0.1
        option netmask  255.0.0.0
 
config interface wan
        option ifname   eth0
        option proto    dhcp
 
config interface lan
        option ifname   eth1
        option proto    static
        option ipaddr   192.168.1.11
        option netmask  255.255.255.0
Above example set the OpenWRT IP address to 192.168.1.11. Save the file and reboot OpenWRT.
 
 
As shown in figure below, opkg update is able to download package list from internet.
OpenWRT opkg update

 

Here is a working vdi file which the network settings is configure based on above settings.
