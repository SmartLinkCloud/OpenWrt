# Firmware compiling

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get clean

    sudo apt-get install gcc g++ binutils patch bzip2 flex bison make autoconf gettext texinfo unzip sharutils subversion libncurses5-dev ncurses-term zlib1g-dev libssl

    mkdir openwrt
    cd openwrt

    svn checkout svn://svn.openwrt.org/openwrt/trunk
    cd trunk

    svn update

    cp feeds.conf.default feeds.conf
    
    sudo vim feeds.conf
add:
    src-git wifidog https://github.com/wifidog/wifidog-gateway.git
    
    ./scripts/feeds update -a
    ./scripts/feeds install -a


dts:

	/dts-v1/; 
	 
	/include/ "mt7620a.dtsi"  

	/ {  
		compatible = "HiWiFi,HC5661", "ralink,mt7620a-soc";  
		model = "HC5661 MIPS Ralink MT7620A"; 
	  
		chosen {   
	    	bootargs = "console=ttyS0,115200"; 
		};   
	 
		palmbus@10000000 {   
			sysc@0 {  
				ralink,gpiomux = "i2c", "jtag";
				ralink,uartmux = "gpio";    
				ralink,wdtmux = <1>; 
			};
			 
			gpio0: gpio@600 {
				status = "okay"; 
			}; 
			gpio2: gpio@660 {
				status = "okay";
			}; 
			gpio3: gpio@688 {
				status = "okay";   
			}; 
	    
			spi@b00 {
				status = "okay";
				 
				m25p80@0 {     
					#address-cells = <1>;     
					#size-cells = <1>;
					compatible = "w25q128";     
					reg = <0 0>; 
					linux,modalias = "m25p80", "w25q128";     
					spi-max-frequency = <10000000>;      

					partition@0 {      
						label = "u-boot";      
						reg = <0x0 0x30000>;      
						read-only; 
					}; 
				
					partition@30000 {      
						label = "u-boot-env";      
						reg = <0x30000 0x10000>;      
						read-only;     
					}; 
	     
					factory: partition@40000 {      
						label = "factory"; 
						reg = <0x40000 0x10000>;  
						read-only; 
					}; 
	     
					partition@50000 {      
						label = "firmware"; 
						reg = <0x50000 0xfb0000>; 
					}; 
				}; 
			}; 
		}; 
	
		ehci@101c0000 {   
			status = "okay"; 
		};
		 
		ohci@101c1000 {   
			status = "okay";  
		};   
	 
		sdhci@10130000 {   
			status = "okay";  
		};   

		pcie@10140000 {   
			status = "okay";  
		};   
	 
		wmac@10180000 {   
			ralink,mtd-eeprom = <&factory 0>;  
		}; 

		ethernet@10100000 {   
			pinctrl-names = "default";   
			pinctrl-0 = <&ephy_pins>; 
			mtd-mac-address = <&factory 0x4>;   
			ralink,port-map = "wllll"; 
		};   

		pinctrl {   
			state_default: pinctrl0 {    
				gpio {     
					ralink,group = "uartf", "wled", "nd_sd";     
					ralink,function = "gpio"; 
				};  
	 
	 
				pa {
					ralink,group = "pa";     
					ralink,function = "pa"; 
				}; 
			}; 
		}; 

		gpio-keys-polled {   
			compatible = "gpio-keys-polled";   
			#address-cells = <1>;   
			#size-cells = <0>;   
			poll-interval = <20>;   
			reset {    
				label = "reset"; 
				gpios = <&gpio0 12 1>;    
				linux,code = <0x198>; 
			}; 
		}; 
	  
		gpio-leds {   
			compatible = "gpio-leds";   
			power1 {    
				label = "HC5661:blue:power";    
				gpios = <&gpio0 9 1>;   
				};   
			wlan1 {    
				label = "HC5661:blue:wifi";    
				gpios = <&gpio3 0 1>;   
				};   
			internet {    
				label = "HC5661:blue:internet";    
				gpios = <&gpio0 11 1>;   
			}; 
		}; 
	}; 


    make menuconfig
    sudo make V=99

# Errors

e4defrag.c:201:2: error: #error fallocate64 not available!
 #error fallocate64 not available!

