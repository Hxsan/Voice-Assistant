
from PyP100 import PyL530

# l530 = PyL530.L530("192.168.1.75", "hasanahmed2004@outlook.com", "Hasan123") #Creating a L530 bulb object

# l530.handshake() #Creates the cookies required for further methods
# l530.login() #Sends credentials to the plug and creates AES Key and IV for further methods

# #All the bulbs have the PyP100 functions and additionally allows for setting brightness, colour and white temperature
# l530.setBrightness(20) #Sends the set brightness request
# l530.setColorTemp(2700) #Sets the colour temperature to 2700 Kelvin (Warm White)
# l530.setColor(20, 10) #Sends the set colour request from 0 -> 360 degrees for hue

colours = {
    'red' : 360, 'pink': 330,
    'magenta': 300, 'purple': 270,
    'blue': 240, 'turquoise': 210,
    'teal' : 180, 'seagreen': 150,
    'green': 120, 'lime': 90,
    'yellow': 60, 'orange': 30
    }

transcription = "teal people like men blue".split()
templst = []
for i in transcription:
    if i in colours:
        templst.append(i)

l530 = PyL530.L530("192.168.1.75", "hasanahmed2004@outlook.com", "Hasan123") #Creating a L530 bulb object

l530.handshake() #Creates the cookies required for further methods
l530.login() #Sends credentials to the plug and creates AES Key and IV for further methods

#All the bulbs have the PyP100 functions and additionally allows for setting brightness, colour and white temperature
l530.setBrightness(100) #Sends the set brightness request
l530.setColorTemp(2700) #Sets the colour temperature to 2700 Kelvin (Warm White)
l530.setColor(colours[f"{templst[0]}"], 100) #Sends the set colour request from 0 -> 360 degrees for hue
    
"""
https://github.com/fishbigger/TapoP100
Tapo light control library, uses obejct oriented programming to create a lightbulb object
"""