from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget # <-- both imports are for the GUI
from threading import Thread

import sys # <-- Used to manage the windows(open/close windows)
import speech_recognition as sr # <-- Used to understand speech input
import subprocess # <-- Used to open applications on the system and manage files
import PyP100 # <-- Used to control smart peripherals and devices
import sqlite3 # <-- Used to manage and create databases
import webbrowser # <-- Used as a web based library to visually represent information
import twilio # <-- Used to send messages via SMS
import pyttsx3 # <-- Used to convert text to speech
import datetime # <-- Used to check the date and time
import time # <-- Will be used for delays 
import requests # <-- Used for accessing web information and relaying it to the program
import hashlib # <-- Used to encrypt and decrypt passwords using hashes

"""
- Log Tweepy results to an external text file with the file name inclu. -> Firstname, Surname, UserID and "Log of Tweepy results" 
- Fight a fuckin bear
- Do the Voice Assistant commands that you said in the analysis, write them outside of the voice assistant object i.e. in the VA class
- Slap in the PyP100 and integrate it into the VA, comments are in the test file for PyP100
- Make pyttsx3 useful, reads out the voice assistant commands only, the ones returned
- Ability to sort folders
- Calculating bills and taxation, reminders system (one section?) - decide 06/03/2022
- Playing music and sending messages (Try to make, if not then say time constraint limitation in eval)
"""


#--- Smaller Variables ---
vers_no = str("3.0")

con = sqlite3.connect('VoiceAI.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Logins(
	UserID INTEGER PRIMARY KEY AUTOINCREMENT,
	Username TEXT UNIQUE,
	Hash TEXT,
	Date_Created TEXT,
    FOREIGN KEY(UserID) REFERENCES Names(UserID)
    );''')

cur.execute('''CREATE TABLE IF NOT EXISTS Names(
	UserID INTEGER PRIMARY KEY AUTOINCREMENT,
	First_name	TEXT,
	Last_name	TEXT,
    Email TEXT UNIQUE
    );''')

con.commit()

#----------Login Page (Finished)----------
class LoginPage(QMainWindow):

    def __init__(self):
        super(LoginPage, self).__init__()
        self.setFixedSize(501,460)
        self.setWindowTitle("VoiceAI - Login " + vers_no) 
        self.Login()

    def Sign_in(self):
        try:
            cur.execute(f'SELECT Username, Hash FROM Logins WHERE Username = "{self.Username_input.text()}";')
            Username, Hash = cur.fetchone()

            con.commit()
            
            passhash = hashlib.new("sha256")
            passhash.update(self.Password_input.text().encode())

            if Username == self.Username_input.text() and Hash == passhash.hexdigest():
                self.w = MainPage()
                self.w.show()
                self.hide()
        
            else:
                self.validation_statement.setText("Invalid login")

        except:
            self.validation_statement.setText("Login is not recognised within the database")
            
        finally:
            con.close()

    
    def register(self):
        self.reg = Register()
        self.reg.show()

    def Login(self):

        #Labels
        self.username = QtWidgets.QLabel(self) #Creates a label for the username
        self.username.setText("Username: ") #Sets the label name as 'Username' 
        self.username.move(40,70) #Sets the position of the label to coordinates (x,y)
        self.username.setStyleSheet(''' font-size: 12px; ''')              

        self.password = QtWidgets.QLabel(self) #Creates a label for the password
        self.password.setText("Password: ") # Sets the label for as 'Password'
        self.password.move(40,120) #Sets the position of the label to coordinates (x,y)
        self.password.setStyleSheet(''' font-size: 12px; ''') 

        self.registertext = QtWidgets.QLabel(self)
        self.registertext.setText("New to VoiceAI?")
        self.registertext.setGeometry(QtCore.QRect(184, 300, 161, 20))
        self.registertext.setStyleSheet(''' font-size: 16px; ''')

        #Login validation statement boxes
        self.validation_statement = QtWidgets.QLabel(self) #Creates a label for the validating statement
        self.validation_statement.setGeometry(QtCore.QRect(60,170,361,30)) #Sets the exact height/width of the statement
        self.validation_statement.setAlignment(QtCore.Qt.AlignCenter)
        self.validation_statement.setText(" ") 
        self.validation_statement.setStyleSheet(''' font-size: 16px; color: Red; ''')
        self.validation_statement.setObjectName("ValidationStatement")

        #Entry boxes
        self.Username_input = QtWidgets.QLineEdit(self)
        self.Username_input.setGeometry(QtCore.QRect(130, 74, 311, 20))
        self.Username_input.setObjectName("Username_input")

        self.Password_input = QtWidgets.QLineEdit(self)
        self.Password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password_input.setGeometry(QtCore.QRect(130, 125, 311, 20))
        self.Password_input.setObjectName("Password_input")

        #Buttons
        self.LoginA = QtWidgets.QPushButton(self)
        self.LoginA.setText("Login!")
        self.LoginA.setGeometry(QtCore.QRect(150, 210, 191, 41))
        self.LoginA.clicked.connect(self.Sign_in)
        self.LoginA.setObjectName("Login")

        self.Register = QtWidgets.QPushButton(self)
        self.Register.setText("Register")
        self.Register.setGeometry(QtCore.QRect(170, 330, 151, 41))
        self.Register.setObjectName("Register")
        self.Register.clicked.connect(self.register)

        #Frame header for Window
        self.WelcomeFrame = QtWidgets.QFrame(self)
        self.WelcomeFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.WelcomeFrame.setGeometry(QtCore.QRect(9, 10, 471, 51))
        self.WelcomeFrame.setObjectName("WelcomeFrame")
        self.WelcomeFrame.setLineWidth(2)

        self.WelcomeLabel = QtWidgets.QLabel(self)
        self.WelcomeLabel.setGeometry(QtCore.QRect(6, 19, 461, 31))
        self.WelcomeLabel.setText("Welcome To VoiceAI: Login")
        self.WelcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.WelcomeLabel.setStyleSheet('''font-size: 24px''')

        # Watermarking the Login Fields
        self.Username_input.setPlaceholderText("Enter your Username")
        self.Password_input.setPlaceholderText("Enter a Valid Password")
#----------END OF CLASS----------

#----------Microphone Object----------
class microphone_obj(object):
    def __call__(self, r, mic):
        r = sr.Recognizer()
        mic = sr.Microphone()

        r.dynamic_energy_threshold = True
        
        output= {
            'transcription':'None',
            'Errors': None,
            'Reactive_Val': 0 
        }

        with mic as source:
            try:
                print("speak now")
                listen = r.listen(source) # ---> can be condensed into one line
                output['transcription'] = r.recognize_google(listen)

            except sr.UnknownValueError:
                print("I didn't catch that! Please try again.")
                output['Errors'] = "UnknownValueError"
                output['transcription'] = "null"
        
        #Recording the pitch of the user using an integer list
        bitarr = listen.get_raw_data(convert_rate= 2, convert_width= 2)
        intarr = []
        for countA in range(len(bitarr)):
            intarr.append(bitarr[countA])
        
        output['Reactive_Val'] = intarr

        return output
#----------END OF CLASS----------

#----------Registration Page----------
class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400,336)
        self.setWindowTitle("VoiceAI - Register " + vers_no)
        self.Registration()

    def Registration(self):
        # Title
        self.Register_title = QtWidgets.QLabel(self)
        self.Register_title.setGeometry(QtCore.QRect(30, 10, 331, 31))
        self.Register_title.setStyleSheet(''' font-size: 14px; ''')
        self.Register_title.setFrameShape(QtWidgets.QFrame.Panel)
        self.Register_title.setAlignment(QtCore.Qt.AlignCenter)
        self.Register_title.setObjectName("Register_title")
        
        """
            Credentials for the User
        """

        # Input box for the first name
        self.First_name_input = QtWidgets.QLineEdit(self)
        self.First_name_input.setGeometry(QtCore.QRect(130, 50, 241, 20))
        self.First_name_input.setObjectName("First_name_input")

        # Input box for the last name
        self.Last_name_input = QtWidgets.QLineEdit(self)
        self.Last_name_input.setGeometry(QtCore.QRect(130, 80, 241, 20))
        self.Last_name_input.setObjectName("Last_name_input")

        # Labels for the first name and the last name
        self.First_name = QtWidgets.QLabel(self)
        self.First_name.setGeometry(QtCore.QRect(40, 50, 71, 16))
        self.First_name.setStyleSheet(''' font-size: 12px; ''')
        self.First_name.setObjectName("First_name")

        self.Last_name = QtWidgets.QLabel(self)
        self.Last_name.setGeometry(QtCore.QRect(40, 80, 71, 16))
        self.Last_name.setStyleSheet(''' font-size: 12px ''')
        self.Last_name.setObjectName("Last_name")

        # Divider line for names and credential fields
        self.x_line = QtWidgets.QFrame(self)
        self.x_line.setGeometry(QtCore.QRect(0, 110, 401, 20))
        self.x_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.x_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.x_line.setObjectName("x_line")

        # Entry boxes for the username and passwords
        self.Username_input = QtWidgets.QLineEdit(self)
        self.Username_input.setGeometry(QtCore.QRect(130, 130, 241, 20))
        self.Username_input.setObjectName("Username_input")

        self.Password_input = QtWidgets.QLineEdit(self)
        self.Password_input.setGeometry(QtCore.QRect(130, 160, 241, 20))
        self.Password_input.setObjectName("Password_input")

        # Labels for Username and Password
        self.username = QtWidgets.QLabel(self)
        self.username.setGeometry(QtCore.QRect(40, 130, 71, 16))
        self.username.setStyleSheet(''' font-size: 12px ''')
        self.username.setObjectName("username")

        self.password = QtWidgets.QLabel(self)
        self.password.setGeometry(QtCore.QRect(40, 160, 71, 16))
        self.password.setStyleSheet(''' font-size: 12px ''')
        self.password.setObjectName("password")

        """
            Parameters for the user account to be created
        """
        
        self.T_and_C = QtWidgets.QRadioButton(self)
        self.T_and_C.setGeometry(QtCore.QRect(20, 240, 361, 17))
        self.T_and_C.setObjectName("T_and_C")

        self.email_label = QtWidgets.QLabel(self)
        self.email_label.setGeometry(QtCore.QRect(40,190,71,16))
        self.email_label.setStyleSheet(''' font-size: 12px ''')
        self.email_label.setObjectName("email_label")

        self.email = QtWidgets.QLineEdit(self)
        self.email.setGeometry(QtCore.QRect(130,190,241,20))
        self.email.setObjectName("email")

        self.Create_User = QtWidgets.QPushButton(self)
        self.Create_User.setGeometry(QtCore.QRect(140, 270, 111, 31))
        self.Create_User.setObjectName("Create_User")
        self.Create_User.clicked.connect(self.reg)

        self.Clear_fields = QtWidgets.QPushButton(self)
        self.Clear_fields.setGeometry(QtCore.QRect(300, 270, 75, 23))
        self.Clear_fields.setObjectName("Clear_fields")
        self.Clear_fields.setText("Clear Fields")
        self.Clear_fields.clicked.connect(self.clearall)

        self.Invalid = QtWidgets.QLabel(self)
        self.Invalid.setGeometry(QtCore.QRect(0,310,401,20))
        self.Invalid.setText(" ")
        self.Invalid.setStyleSheet(''' font-size: 12px; color: Red; ''')
        self.Invalid.setAlignment(QtCore.Qt.AlignCenter)
        self.Invalid.setObjectName("Invalid")

        # Text entries for each label/ entry
        self.Register_title.setText("Register for VoiceAI")
        self.First_name.setText("First Name:")
        self.Last_name.setText("Last Name:")
        self.username.setText("Username:")
        self.password.setText("Password:")
        self.T_and_C.setText("Agree to the collection of data for the sole creation of a user account.")
        self.email_label.setText("Email:")
        self.Create_User.setText("Create User!")

        # Watermark on the field boxes
        self.email.setPlaceholderText("Enter a valid email")
        self.Username_input.setPlaceholderText("Username between 5 and 15 characters")
        self.Password_input.setPlaceholderText("Password more than 8 characters")
        self.First_name_input.setPlaceholderText("Enter your First name")
        self.Last_name_input.setPlaceholderText("Enter your Last name")

    def reg(self):
        check = "@" in list(self.email.text())
        if self.T_and_C.isChecked():
            cur.execute(f'SELECT Username FROM Logins WHERE Username = "{self.Username_input.text()}";')
            result = cur.fetchone()
            if len(self.Username_input.text()) > 15:
                self.Invalid.setText("Error: Username too long")

            elif len(self.Username_input.text()) < 5:
                self.Invalid.setText("Error: Username too short")

            elif len(self.Password_input.text()) < 8:
                self.Invalid.setText("Error: Password too short")

            elif check == False:
                self.Invalid.setText("Error: Email is invalid")

            elif result:
                self.Invalid.setText("Error: Username already exists")
                
            else:
                self.Invalid.setStyleSheet('''font-size: 12px; color: green;''')
                self.Invalid.setText("User Created!")

                passhash = hashlib.new("sha256")
                passhash.update(self.Password_input.text().encode())    

                cur.execute(f'INSERT INTO Logins VALUES(null, "{self.Username_input.text()}", "{passhash.hexdigest()}", "{datetime.date.today()}");')
                cur.execute(f'INSERT INTO Names VALUES(null, "{self.First_name_input.text()}", "{self.Last_name_input.text()}", "{self.email.text()}");')
                con.commit()

        else:
            self.Invalid.setText("Error: Please Accept the terms and conditions")
        
    def clearall(self):
        self.email.clear()
        self.Username_input.clear()
        self.Password_input.clear()
        self.First_name_input.clear()
        self.Last_name_input.clear()


#----------END OF CLASS----------

#----------Main Page (UNFINISHED)-----------
class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(784, 520)
        self.setWindowTitle("VoiceAI - Main Page " + vers_no)
        self.SplashScreen()

    def SplashScreen(self):
        #Frame for header
        self.Header = QtWidgets.QFrame(self) #Initialises a frame object
        self.Header.setGeometry(QtCore.QRect(20, 10, 741, 111))
        self.Header.setFrameShape(QtWidgets.QFrame.StyledPanel) #Gives the frame a recessed look
        self.Header.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Header.setLineWidth(2) #The thickness of the frame borders
        self.Header.setObjectName("Header") #Object name for the frame

        #Header Label
        self.Welcome = QtWidgets.QLabel(self) #Sets the frame text via a label
        self.Welcome.setGeometry(QtCore.QRect(0, 0, 741, 114))
        self.Welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.Welcome.setText("Welcome To VoiceAI") #The label text
        self.Welcome.setStyleSheet(''' font-size: 48px; ''')
        self.Welcome.setObjectName("Welcome") #Object name for the label

        #Border containing the buttons
        self.ButtonHolder = QtWidgets.QFrame(self) #Frame to hold the buttons
        self.ButtonHolder.setGeometry(QtCore.QRect(20, 150, 741, 321))
        self.ButtonHolder.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ButtonHolder.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ButtonHolder.setLineWidth(3) #Sets the width of the frame
        self.ButtonHolder.setObjectName("ButtonHolder") #Callable object name

        #Button for the voice assistant
        self.VoiceAssist = QtWidgets.QPushButton(self.ButtonHolder) #button used to access voice assistant
        self.VoiceAssist.setGeometry(QtCore.QRect(100, 20, 221, 271))
        self.VoiceAssist.setText("Voice Assistant") #The text within the button
        self.VoiceAssist.setStyleSheet(''' font-size: 16px; ''') #Font of the button
        self.VoiceAssist.setObjectName("VoiceAssist") #Callable object name
        self.VoiceAssist.clicked.connect(self.assistant) #Button connected to assistant() function

        #Button for Twitter Scraper
        self.Scraper = QtWidgets.QPushButton(self.ButtonHolder) #Button used to access Twitter scraper
        self.Scraper.setGeometry(QtCore.QRect(440, 20, 211, 271)) 
        self.Scraper.setText("Twitter Scraper") #Sets the button text
        self.Scraper.setStyleSheet(''' font-size: 16px; ''') #The font of the text within the button
        self.Scraper.setObjectName("Scraper") #Callable object name
        self.Scraper.clicked.connect(self.scraper) #Button connected to scraper() function
        
    def assistant(self):
        self.Va = VoiceAssistant()
        self.Va.show()

    def scraper(self):
        self.Ts = TwitterScraper()
        self.Ts.show()
#----------END OF CLASS----------

microphone = microphone_obj() #Instatiate microphone class

#----------Voice Assistant UI----------
class VoiceAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400,300)
        self.setWindowTitle("Voice Assistant " + vers_no)
        self.Voice_Assistant_UI()

    def Voice_Assistant_UI(self):

        #Voice Sensitivity Meter, Detects Loudness
        self.ReactiveVoice = QtWidgets.QProgressBar(self)
        self.ReactiveVoice.setGeometry(QtCore.QRect(30, 20, 81, 251))
        self.ReactiveVoice.setOrientation(QtCore.Qt.Vertical)
        #Sets the maximum level for the progress bar(Voice detection system)
        self.ReactiveVoice.setMaximum(255)
        self.ReactiveVoice.setProperty("value",50)
        #Declaring the Getters for the Voice Assistant
        self.ReactiveVoice.setFormat("")
        self.ReactiveVoice.setObjectName("ReactiveVoice")

        #Instructions on how to use the GUI for the user
        self.VoiceInstructions = QtWidgets.QLabel(self)
        self.VoiceInstructions.setGeometry(QtCore.QRect(150, 20, 231, 41))
        self.VoiceInstructions.setAlignment(QtCore.Qt.AlignCenter)
        self.VoiceInstructions.setWordWrap(True)
        self.VoiceInstructions.setObjectName("VoiceInstructions")

        #Activating the voice assistant
        self.VoiceActivate = QtWidgets.QPushButton(self)
        self.VoiceActivate.setGeometry(QtCore.QRect(150, 70, 231, 51))
        self.VoiceActivate.setDefault(True)
        self.VoiceActivate.setObjectName("VoiceActivate")
        self.VoiceActivate.clicked.connect(self.Voice_Active)

        #Output box to write down what is being said
        self.Outputcont = QtWidgets.QTextBrowser(self)
        self.Outputcont.setGeometry(QtCore.QRect(140, 140, 251, 121))
        self.Outputcont.setObjectName("Outputcont")

        #Statements for the label containers within the class
        self.VoiceInstructions.setText("Press the button below to speak to the voice assistant")
        self.VoiceActivate.setText("Press Me!")

    def Microphone(self):
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        dict = microphone(r,mic)

        self.Outputcont.append("User Said:" + dict['transcription'])

    def Reactive_voice(self):
        intarr = [12,23,56,99,200,156,32,78,99,32,45,66,0]

        for val in range(len(intarr)):
            sl = intarr
            curr = sl[val]
            self.ReactiveVoice.setProperty("value", curr)
            time.sleep(0.5)
    
    def Voice_Active(self):
        Voice = Thread(target=self.Microphone)
        Meter = Thread(target=self.Reactive_voice)

        Voice.start()
        Meter.start()

        Voice.join()
        Meter.join()

#----------END OF CLASS---------


#----------Twitter Scraper UI----------
class TwitterScraper(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(978,410)
        self.setWindowTitle("Twitter Scraper " + vers_no)
        self.Twitter_Scraper()
    
    def Twitter_Scraper(self):
        #The Return box for all the searches
        self.Output_Window = QtWidgets.QTextBrowser(self)
        self.Output_Window.setGeometry(QtCore.QRect(310, 0, 771, 411))
        self.Output_Window.setObjectName("Output_Window")

        #Label and text box for the twitter handle
        self.ID_box = QtWidgets.QLineEdit(self)
        self.ID_box.setGeometry(QtCore.QRect(110, 40, 161, 20))
        self.ID_box.setObjectName("ID_box")

        self.Handle = QtWidgets.QLabel(self)
        self.Handle.setGeometry(QtCore.QRect(20, 40, 81, 16))
        self.Handle.setObjectName("Handle")

        #Label and text box for the Search Query
        self.Query_box = QtWidgets.QLineEdit(self)
        self.Query_box.setGeometry(QtCore.QRect(110, 70, 161, 20))
        self.Query_box.setObjectName("Query_box")

        self.Search_Query = QtWidgets.QLabel(self)
        self.Search_Query.setGeometry(QtCore.QRect(20, 70, 81, 16))
        self.Search_Query.setObjectName("Search_Query")

        #Optional search by microphone feature
        self.Mic_Search = QtWidgets.QPushButton(self)
        self.Mic_Search.setGeometry(QtCore.QRect(280, 70, 21, 23))
        self.Mic_Search.setText("🎤")
        self.Mic_Search.setObjectName("Mic_Search")

        #Number of searches to be accumulated
        self.max_results = QtWidgets.QLineEdit(self)
        self.max_results.setGeometry(QtCore.QRect(110, 100, 81, 20))
        self.max_results.setObjectName("max_results")
        
        self.max_results_label = QtWidgets.QLabel(self)
        self.max_results_label.setGeometry(QtCore.QRect(10, 100, 91, 21))
        self.max_results_label.setObjectName("max_results_label")

        #Submission and logs button
        self.Submit_req = QtWidgets.QPushButton(self)
        self.Submit_req.setGeometry(QtCore.QRect(70, 160, 161, 31))
        self.Submit_req.setObjectName("Submit_req")

        self.req_history = QtWidgets.QPushButton(self)
        self.req_history.setGeometry(QtCore.QRect(60, 200, 181, 23))
        self.req_history.setObjectName("req_history")

        #Searching by parameters
        self.Search_by = QtWidgets.QLabel(self)
        self.Search_by.setGeometry(QtCore.QRect(70, 230, 61, 16))
        self.Search_by.setObjectName("Search_by")

        self.by_TwitterUser = QtWidgets.QRadioButton(self)
        self.by_TwitterUser.setGeometry(QtCore.QRect(100, 250, 101, 17))
        self.by_TwitterUser.setObjectName("by_TwitterUser")
        self.by_TwitterUser.toggled.connect(self.ToggleSearch)
        
        self.by_TwitterAll = QtWidgets.QRadioButton(self)
        self.by_TwitterAll.setGeometry(QtCore.QRect(100, 270, 121, 17))
        self.by_TwitterAll.setObjectName("by_TwitterAll")

        #Exclusion factors for the search
        self.Exclusion = QtWidgets.QLabel(self)
        self.Exclusion.setGeometry(QtCore.QRect(70, 300, 47, 13))
        self.Exclusion.setObjectName("Exclusion")
        
        self.exclu_Retweets = QtWidgets.QCheckBox(self)
        self.exclu_Retweets.setGeometry(QtCore.QRect(100, 320, 70, 17))
        self.exclu_Retweets.setObjectName("exclu_Retweets")
        self.exclu_Retweets.toggled.connect(self.activeExclusion)

        self.Retweets = QtWidgets.QLabel(self)
        self.Retweets.setGeometry(QtCore.QRect(30,130,241,20))
        self.Retweets.setText(" ")
        self.Retweets.setAlignment(QtCore.Qt.AlignCenter)
        self.Retweets.setStyleSheet(''' color: green; ''')

        #Text entries for all the buttons and labels
        self.Handle.setText("Twitter Handle : ")
        self.Search_Query.setText("Search Query:")
        self.Submit_req.setText("Submit request")
        self.req_history.setText("Show request history")
        self.max_results_label.setText("Maximum results:  ")
        self.Search_by.setText("Search By:")
        self.by_TwitterUser.setText("By Twitter User")
        self.by_TwitterAll.setText("The Whole of Twitter")
        self.Exclusion.setText("Exclude: ")
        self.exclu_Retweets.setText("Retweets")

    def ToggleSearch(self):
        if self.by_TwitterUser.isChecked():
            self.Search_Query.hide()
            self.Query_box.hide()
            self.Mic_Search.hide()
        else:
            self.Search_Query.show()
            self.Query_box.show()
            self.Mic_Search.show()
    
    def activeExclusion(self):
        if self.exclu_Retweets.isChecked():
            self.Retweets.setText("Retweets Disabled!")
        else:
            self.Retweets.setText(" ")

#----------END OF CLASS---------

#---------- Tasks and Reminders + Tax calc ----------
class Reminders(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300,400)
        self.setWindowTitle("Task and Reminders " + vers_no)
        self.Reminders()

    def Reminders(self):
        #defede
        when = "i need to do this"

#----------END OF CLASS----------

def window():
    app = QApplication(sys.argv)
    win = LoginPage()
    win.show()
    sys.exit(app.exec_())

window()