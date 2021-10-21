# Raspberry Pi NAS control panel
 A control panel for the Raspberry Pi 3B (should work on the 4B aswell) controlled by a "5 way + 2 buttons Switch" and a 0.91 OLED Display

Menu composition:
 - Mount partitions 	
	 - Submenu with mountable partitions  
		 - Confirmation screen   
 - Connection
	 - TO DO
 - NAS info
 - Battery info
 - Screen off
 - Reboot
	 - Confirmation screen   
 - Shutdown
	 - Confirmation screen   


## Installation on clean Raspberry Pi OS (Full or lite)
**Configuration of the OLED screen**
Download libraries:
```sh
sudo apt-get install python-smbus
sudo apt-get install i2c-tools
sudo pip3 install Adafruit_BBIO
```

Check OLED I2C connection
```sh
sudo i2cdetect -y 1
```

Download framework for OLED screen:
```sh
sudo python -m pip install --upgrade pip setuptools wheel
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
```
Install framework for OLED screen:
```sh
cd Adafruit_Python_SSD1306
sudo python3 setup.py install
```

**Installing the Raspberry Pi NAS Panel**
Download script (execute on home directory):
```sh
git clone https://github.com/federicoftl/rpi_nas_panel.git
```

**Execution and autostart on boot**
Normal execution:
```sh
cd rpi_nas_panel
python3 version.py
```
> Note: Change `version` with your desired version name.

Autostart
```sh
crontab -e
```

> Add "@reboot python3 /home/pi/rpi_nas_panel/desiredversion.py" (without quotes) into crontab.
> Note: Change `version` with your desired version name.

