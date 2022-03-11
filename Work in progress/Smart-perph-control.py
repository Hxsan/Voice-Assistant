
from PyP100 import PyL530

l530 = PyL530.L530("192.168.1.76", "hasanahmed2004@outlook.com", "Hasan123") #Creating a L530 bulb object

l530.handshake() #Creates the cookies required for further methods
l530.login() #Sends credentials to the plug and creates AES Key and IV for further methods

#All the bulbs have the PyP100 functions and additionally allows for setting brightness, colour and white temperature
l530.setBrightness(100) #Sends the set brightness request
l530.setColorTemp(2600) #Sets the colour temperature to 2700 Kelvin (Warm White)
l530.setColor(260, 100) #Sends the set colour request from 0 -> 360 degrees for hue

"""
https://github.com/fishbigger/TapoP100
Tapo light control library, uses obejct oriented programming to create a lightbulb object
"""