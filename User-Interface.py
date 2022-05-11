from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox # <-- both imports are for the GUI
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from threading import Thread  # <-- Used to multithread tasks/ run simultaneously 

import sys # <-- Used to manage the windows(open/close windows)
import speech_recognition as sr # <-- Used to understand speech input
import os # <-- Used to open applications on the system and manage files
from PyP100 import PyL530 # <-- Used to control smart peripherals and devices
import sqlite3 # <-- Used to manage and create databases
import webbrowser # <-- Used as a web based library to visually represent information
import tweepy # <-- Twitter Scraping Library to harvest information from a page
import datetime # <-- Used to check the date and time
import time # <-- Will be used for delays 
import hashlib # <-- Used to encrypt and decrypt passwords using hashes

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

cur.execute('''CREATE TABLE IF NOT EXISTS Reminders(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT,
    Reminder TEXT
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
                self.w = MainPage(self.Username_input.text())
                self.w.show()
                self.hide()
        
            else:
                self.validation_statement.setText("Invalid login")

        except:
            self.validation_statement.setText("Login is not recognised within the database")
    
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
        self.email = QtWidgets.QLineEdit(self)
        self.email.setGeometry(QtCore.QRect(130,190,241,20))
        self.email.setObjectName("email")
        
        self.T_and_C = QtWidgets.QRadioButton(self)
        self.T_and_C.setGeometry(QtCore.QRect(20, 240, 361, 17))
        self.T_and_C.setObjectName("T_and_C")

        self.email_label = QtWidgets.QLabel(self)
        self.email_label.setGeometry(QtCore.QRect(40,190,71,16))
        self.email_label.setStyleSheet(''' font-size: 12px ''')
        self.email_label.setObjectName("email_label")

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

        """
        Label Predefined Text
        """

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

#---------- Reactive bar object ----------

class update_Progress(QObject):
    complete = pyqtSignal()
    incremental = pyqtSignal(int)

    def run(self):
        r = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            sound = r.listen(source)
            one = sound.get_raw_data(convert_rate=2,convert_width=2)
            for i in range(len(one)):
                curr = one[i]
                time.sleep(0.15)
                self.incremental.emit(curr)
            self.complete.emit()

#---------- End of Object ----------

#----------Main Page (UNFINISHED)-----------
class MainPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.username = user
        self.setWindowTitle(f"VoiceAI - Main Page {vers_no} - Username: {self.username}")
        self.setFixedSize(720, 520)
        self.SplashScreen()

    def SplashScreen(self):
        #Frame for header
        self.Header = QtWidgets.QFrame(self) #Initialises a frame object
        self.Header.setGeometry(QtCore.QRect(20, 10, 681, 111))
        self.Header.setFrameShape(QtWidgets.QFrame.StyledPanel) #Gives the frame a recessed look
        self.Header.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Header.setLineWidth(2) #The thickness of the frame borders
        self.Header.setObjectName("Header") #Object name for the frame

        #Header Label
        self.Welcome = QtWidgets.QLabel(self) #Sets the frame text via a label
        self.Welcome.setGeometry(QtCore.QRect(0, 0, 681, 114))
        self.Welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.Welcome.setText("Welcome To VoiceAI") #The label text
        self.Welcome.setStyleSheet(''' font-size: 48px; ''')
        self.Welcome.setObjectName("Welcome") #Object name for the label

        #Border containing the buttons
        self.ButtonHolder = QtWidgets.QFrame(self) #Frame to hold the buttons
        self.ButtonHolder.setGeometry(QtCore.QRect(20, 150, 681, 321))
        self.ButtonHolder.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ButtonHolder.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ButtonHolder.setLineWidth(3) #Sets the width of the frame
        self.ButtonHolder.setObjectName("ButtonHolder") #Callable object name

        #Button for the voice assistant
        self.VoiceAssist = QtWidgets.QPushButton(self.ButtonHolder) #button used to access voice assistant
        self.VoiceAssist.setGeometry(QtCore.QRect(10, 20, 221, 271))
        self.VoiceAssist.setText("Voice Assistant") #The text within the button
        self.VoiceAssist.setStyleSheet(''' font-size: 16px; ''') #Font of the button
        self.VoiceAssist.setObjectName("VoiceAssist") #Callable object name
        self.VoiceAssist.clicked.connect(self.assistant) #Button connected to assistant() function

        #Button for Twitter Scraper
        self.Scraper = QtWidgets.QPushButton(self.ButtonHolder) #Button used to access Twitter scraper
        self.Scraper.setGeometry(QtCore.QRect(240, 20, 211, 271)) 
        self.Scraper.setText("Twitter Scraper") #Sets the button text
        self.Scraper.setStyleSheet(''' font-size: 16px; ''') #The font of the text within the button
        self.Scraper.setObjectName("Scraper") #Callable object name
        self.Scraper.clicked.connect(self.scraper) #Button connected to scraper() function

        self.reminders = QtWidgets.QPushButton(self.ButtonHolder)
        self.reminders.setGeometry(QtCore.QRect(460, 20, 211, 271))
        self.reminders.setText("Tasks and Reminders\nWith Tax Calculator")
        self.reminders.setStyleSheet(''' font-size: 16px; ''')
        self.reminders.setObjectName("T&R_with_calc")
        self.reminders.clicked.connect(self.reminder)
        
    def assistant(self):
        self.Va = self.VoiceAssistant(self.username)
        self.Va.show()

    def scraper(self):
        self.Ts = self.TwitterScraper(self.username)
        self.Ts.show()
    
    def reminder(self):
        self.Tr = self.Reminders(self.username)
        self.Tr.show()
#---------- END OF CLASS ----------


#----------Voice Assistant UI----------
    class VoiceAssistant(QWidget):
        def __init__(self, user):
            super().__init__()
            self.username = user
            self.setFixedSize(400,300)
            self.setWindowTitle(f"Voice Assistant {vers_no} - Username: {self.username}")
            self.Voice_Assistant_UI()

            self.l530 = PyL530.L530("192.168.1.75", "hasanahmed2004@outlook.com", "Hasan123")
            self.l530.handshake()
            self.l530.login()

        def Voice_Assistant_UI(self):

            #Voice Sensitivity Meter, Detects Loudness
            self.ReactiveVoice = QtWidgets.QProgressBar(self)
            self.ReactiveVoice.setGeometry(QtCore.QRect(30, 20, 81, 251))
            self.ReactiveVoice.setOrientation(QtCore.Qt.Vertical)
            #Sets the maximum level for the progress bar(Voice detection system)
            self.ReactiveVoice.setMaximum(256)
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
            self.VoiceActivate.clicked.connect(lambda: [Thread(target=self.Microphone()).start(),self.Reactive_Voice()])

            #Output box to write down what is being said
            self.Outputcont = QtWidgets.QTextBrowser(self)
            self.Outputcont.setGeometry(QtCore.QRect(140, 140, 251, 121))
            self.Outputcont.setObjectName("Outputcont")

            """
            Label Predefined Text
            """

            self.VoiceInstructions.setText("Press the button below to speak to the voice assistant")
            self.VoiceActivate.setText("Press Me!")

        def Microphone(self):
            r = sr.Recognizer()
            mic = sr.Microphone()

            r.dynamic_energy_threshold = True
            
            output= {
                'transcription':'None',
                'Errors': None,
            }

            with mic as source:
                try:
                    self.Outputcont.append("Listening...")
                    QApplication.processEvents()
                    listen = r.listen(source)
                    output['transcription'] = r.recognize_google(listen)
                    self.Outputcont.append(f"\nUser Said: {output['transcription']}")
                    if output['transcription'] == "clear":
                        self.Outputcont.clear()

                except sr.UnknownValueError:
                    output['Errors'] = "UnknownValueError"
                    output['transcription'] = "null"
                    self.Outputcont.append("Assistant Said: I didn't catch that! Please try again.")
                
            self.response = output['transcription']

            if self.Responses == None:
                self.Outputcont.append("Assistant Said: My response has not been programmed yet!")
            else:
                self.Outputcont.append(f"Assistant Said: {self.Responses()}")

        def upd_meter(self,n):
            self.ReactiveVoice.setValue(n)
            
        def Reactive_Voice(self):
            self.thread = QThread()
            self.reactive = update_Progress() #Initiates and moves the object to a thread
            self.reactive.moveToThread(self.thread)

            self.thread.started.connect(self.reactive.run)
            self.reactive.complete.connect(self.thread.quit) #When the thread is done the thread is exited
            self.reactive.complete.connect(self.reactive.deleteLater) #The thread is held in memory until destroyed

            self.thread.finished.connect(self.thread.deleteLater) # Connected to above statement
            self.reactive.incremental.connect(self.upd_meter) #Connected to the progress bar

            self.thread.start() # Starts the thread

            self.VoiceActivate.setEnabled(False) #Disables the button while the thread is running
            self.thread.finished.connect(
                lambda: self.VoiceActivate.setEnabled(True) #Re enables button when the thread is complete
            )

            self.thread.finished.connect(
                lambda: self.ReactiveVoice.setValue(0) #Resets the value of the progress bar to zero
            )
        
        def Responses(self):
            try:
                transcription = self.response
                transcription = transcription.lower().split()
                #print(transcription)
            except:
                return "No values within the response"

            if "open" in transcription:
                if "microsoft" and "word" in transcription:
                    os.startfile("C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE")
                    return "Opening Word..."
                elif "powerpoint" in transcription:
                    os.startfile("C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE")
                    return "Opening Powerpoint..."
                elif "onenote" in transcription:
                    os.startfile("C:/Program Files/Microsoft Office/root\Office16/ONENOTE.EXE")
                    return "Opening OneNote..."
                elif "excel" in transcription:
                    os.startfile("C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE")
                    return "Opening Excel..."
                elif "spotify" in transcription:
                    os.startfile("C:/Users/Hasan/AppData/Local/Microsoft/WindowsApps/Spotify.exe")
                    return "Opening Spotify..."
                elif "chrome" in transcription:
                    os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")
                    return "Opening Spotify..."
                elif "calendar" in transcription: #Write as a failed test (due to system limitations)
                    os.system("Calendar")
                else:
                    return "Program not found on system"
            
            elif "search" in transcription:
                transcription.remove("search")
                if "for" in transcription:
                    transcription.remove("for")
                webbrowser.open(f"https://www.google.com/search?q={' '.join(transcription)}")
                return f"Searching for {' '.join(transcription)}"

            elif "add" and "reminder" in transcription:
                try:
                    transcription.remove("reminder")
                    if "add" in transcription:
                        transcription.remove("add")
                        if "a" in transcription:
                            transcription.remove("a")
                        else:
                            pass
                    elif transcription == None:
                        self.Outputcont.append("Whoopsie that's not a reminder!")
                    
                    cur.execute(f'INSERT INTO Reminders Values(null, "{self.username}", "{" ".join(transcription)}");')
                    con.commit()
                    return "Reminder Added!"
                except:
                    return "I didn't understand that! Maybe my response has not been programmed yet."
            
            elif "set" and "lights" in transcription:
                if "colour" in transcription:
                    colours = {
                    'red' : 360, 'pink': 330,
                    'magenta': 300, 'purple': 270,
                    'blue': 240, 'turquoise': 210,
                    'teal' : 180, 'seagreen': 150,
                    'green': 120, 'lime': 90,
                    'yellow': 60, 'orange': 30
                    }

                    temp_lst = []
                    temp_lst.clear()
                    for i in transcription:
                        if i in colours:
                            temp_lst.append(i)
                    
                    self.l530.setBrightness(100) #Sends the set brightness request
                    self.l530.setColorTemp(2700) #Sets the colour temperature to 2700 Kelvin (Warm White)
                    self.l530.setColor(colours[f"{temp_lst[0]}"], 100) #Sends the set colour request from 0 -> 360 degrees for hue

                    return f"Changing Light Colour to {temp_lst[0]}"
                
                elif "brightness" in transcription:
                    num_lst = []
                    num_lst.clear()
                    for i in range(100):
                        if str(i) in transcription:
                            num_lst.append(i)
                    
                    self.l530.setBrightness(num_lst[0])
                    
                    return f"Setting the brightness to: {num_lst[0]}"
#----------END OF CLASS---------


#---------- Tasks and Reminders + Tax calc ----------
    class Reminders(QWidget):
        def __init__(self,user):
            super().__init__()
            self.username = user
            self.setFixedSize(842, 415)
            self.setWindowTitle(f"Task and Reminders {vers_no} - Username: {self.username}")
            self.Reminders()
            self.TaxCalculator()

        def Reminders(self):
            self.Vert_Divider = QtWidgets.QFrame(self)
            self.Vert_Divider.setGeometry(QtCore.QRect(440, 0, 20, 411))
            self.Vert_Divider.setFrameShape(QtWidgets.QFrame.VLine)
            self.Vert_Divider.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.Vert_Divider.setObjectName("Vert_Divider")
        
            self.Reminders_rect = QtWidgets.QTextBrowser(self)
            self.Reminders_rect.setGeometry(QtCore.QRect(10, 10, 431, 391))
            self.Reminders_rect.setObjectName("Reminders_rect")

            try:
                cur.execute(f'SELECT Reminder FROM Reminders WHERE Username = "{self.username}";')
                
                reminders = cur.fetchall()
                self.Reminders_rect.setAlignment(QtCore.Qt.AlignCenter)
                self.Reminders_rect.append("---------- Reminders ----------")
                self.Reminders_rect.setStyleSheet(''' font-size: 18px; ''')
                counter = 1
                for reminder in reminders:
                    self.Reminders_rect.append(f"{counter}: {reminder[0]}")
                    counter += 1

            except:
                self.Reminders_rect.setStyleSheet(''' font-size: 18px; ''')
                self.Reminders_rect.append("There are no reminders currently within the system, you can create some in the Voice Assistant!")
        
        def TaxCalculator(self):
            self.entry_frame = QtWidgets.QFrame(self)
            self.entry_frame.setGeometry(QtCore.QRect(480, 90, 341, 111))
            self.entry_frame.setFrameShape(QtWidgets.QFrame.Box)
            self.entry_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.entry_frame.setLineWidth(2)
            self.entry_frame.setObjectName("entry_frame")


            self.Tax_Frame = QtWidgets.QFrame(self)
            self.Tax_Frame.setGeometry(QtCore.QRect(480, 30, 341, 51))
            self.Tax_Frame.setFrameShape(QtWidgets.QFrame.Box)
            self.Tax_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.Tax_Frame.setLineWidth(2)
            self.Tax_Frame.setObjectName("Tax_Frame")

            self.Tax_BillsLabel = QtWidgets.QLabel(self.Tax_Frame)
            self.Tax_BillsLabel.setGeometry(QtCore.QRect(0, -1, 341, 51))
            self.Tax_BillsLabel.setStyleSheet(''' font-size: 20px; ''')
            self.Tax_BillsLabel.setAlignment(QtCore.Qt.AlignCenter)


            self.PPA = QtWidgets.QLabel(self)
            self.PPA.setGeometry(QtCore.QRect(480, 220, 121, 16))
            self.PPA.setObjectName("PPA")
            self.PPA.setStyleSheet(''' font-size: 12px; ''')
            
            self.per5_tip = QtWidgets.QLabel(self)
            self.per5_tip.setGeometry(QtCore.QRect(500, 250, 61, 16))
            self.per5_tip.setObjectName("per5_tip")
            self.per5_tip.setStyleSheet(''' font-size: 12px; ''')

            self.per10_tip = QtWidgets.QLabel(self)
            self.per10_tip.setGeometry(QtCore.QRect(500, 280, 61, 16))
            self.per10_tip.setObjectName("per10_tip")
            self.per10_tip.setStyleSheet(''' font-size: 12px; ''')


            self.cust_tip = QtWidgets.QLabel(self)
            self.cust_tip.setGeometry(QtCore.QRect(500, 310, 101, 16))
            self.cust_tip.setObjectName("cust_tip")
            self.cust_tip.setStyleSheet(''' font-size: 12px; ''')

            self.cust_tip_Entry = QtWidgets.QLineEdit(self)
            self.cust_tip_Entry.setGeometry(QtCore.QRect(630, 310, 113, 20))
            self.cust_tip_Entry.setObjectName("cust_tip_Entry")
            self.cust_tip_Entry.setStyleSheet(''' font-size: 12px; ''')

            self.cust_tip_Output = QtWidgets.QLabel(self)
            self.cust_tip_Output.setGeometry(QtCore.QRect(500, 340, 301, 31))
            self.cust_tip_Output.setObjectName("cust_tip_Output")
            self.cust_tip_Output.setStyleSheet(''' font-size: 12px; ''')
            self.cust_tip_Output.setAlignment(QtCore.Qt.AlignCenter)

            self.cust_submit = QtWidgets.QPushButton(self)
            self.cust_submit.setGeometry(QtCore.QRect(750, 310, 51, 21))
            self.cust_submit.setObjectName("cust_Submit")
            self.cust_submit.clicked.connect(self.custom_percent)


            self.PPA_Output = QtWidgets.QLabel(self)
            self.PPA_Output.setGeometry(QtCore.QRect(630, 220, 91, 16))
            self.PPA_Output.setObjectName("PPA_Output")
            self.PPA_Output.setStyleSheet(''' font-size: 12px; ''')

            self.per5_tip_Output = QtWidgets.QLabel(self)
            self.per5_tip_Output.setGeometry(QtCore.QRect(630, 250, 91, 16))
            self.per5_tip_Output.setObjectName("per5_tip_Output")
            self.per5_tip_Output.setStyleSheet(''' font-size: 12px; ''')
            
            self.per10_tip_Output = QtWidgets.QLabel(self)
            self.per10_tip_Output.setGeometry(QtCore.QRect(630, 280, 91, 16))
            self.per10_tip_Output.setObjectName("per10_tip_Output")
            self.per10_tip_Output.setStyleSheet(''' font-size: 12px; ''')


            self.Total = QtWidgets.QLabel(self.entry_frame)
            self.Total.setGeometry(QtCore.QRect(10, 10, 151, 21))
            self.Total.setObjectName("Total")
            self.Total.setStyleSheet(''' font-size: 12px; ''')

            self.Total_Entry = QtWidgets.QLineEdit(self.entry_frame)
            self.Total_Entry.setGeometry(QtCore.QRect(170, 10, 141, 21))
            self.Total_Entry.setObjectName("Total_Entry")

            self.Number_Of_People = QtWidgets.QLabel(self.entry_frame)
            self.Number_Of_People.setGeometry(QtCore.QRect(10, 40, 121, 31))
            self.Number_Of_People.setObjectName("Number_Of_People")
            self.Number_Of_People.setStyleSheet(''' font-size: 12px; ''')
            self.Number_Of_People.setWordWrap(True)
            self.Number_Of_People.setAlignment(QtCore.Qt.AlignCenter)

            self.No_of_People_Entry = QtWidgets.QLineEdit(self.entry_frame)
            self.No_of_People_Entry.setGeometry(QtCore.QRect(170, 40, 113, 20))
            self.No_of_People_Entry.setObjectName("No_of_People_Entry")

            self.Process_Val = QtWidgets.QPushButton(self.entry_frame)
            self.Process_Val.setGeometry(QtCore.QRect(100, 80, 131, 23))
            self.Process_Val.setObjectName("Process_Val")
            self.Process_Val.clicked.connect(self.amounts)

            """
            Label Predefined Text
            """
            self.PPA.setText("Per Person Amount: ")

            self.per5_tip.setText("5% Tip:")
            self.per10_tip.setText("10% Tip:")
            self.cust_tip.setText("Custom Tip (%):")

            self.Tax_BillsLabel.setText("Tax/Bills Calculator")

            self.Total.setText("Enter the Total Amount")
            self.Number_Of_People.setText("Enter the number of people involved: ")
            self.Process_Val.setText("Process Values")

            self.PPA_Output.setText("-~-")
            self.per5_tip_Output.setText("-~-")
            self.per10_tip_Output.setText("-~-")

            self.cust_submit.setText("Submit")
            self.cust_tip_Output.setText(" Output Will Be Here ")

        def amounts(self):
            try:
                Total_am = float(self.Total_Entry.text())
                No_of_people = int(self.No_of_People_Entry.text())

                calc = (Total_am / No_of_people)

                self.PPA_Output.setText(f"£{'{0:.2f}'.format(calc)}")
                self.per5_tip_Output.setText(f"£{'{0:.2f}'.format(calc * 0.05)}")
                self.per10_tip_Output.setText(f"£{'{0:.2f}'.format(calc * 0.10)}")

                self.calc = calc

            except ValueError:
                self.cust_tip_Output.setText("The values entered does not work")

        
        def custom_percent(self):
            try:
                if float(self.cust_tip_Entry.text()) > 100:
                    self.cust_tip_Output.setStyleSheet(''' color : Red; ''')
                    self.cust_tip_Output.setText("100 percent is too high")
                elif float(self.cust_tip_Entry.text()) < 0:
                    self.cust_tip_Output.setStyleSheet(''' color : Red; ''')
                    self.cust_tip_Output.setText("Value cannot be below 0%")
                
                else:
                    self.cust_tip_Output.setStyleSheet(''' color: green; font-size: 12px; ''')
                    self.cust_tip_Output.setText(f"The Custom Tip is: £{'{0:.2f}'.format(self.calc * (float(self.cust_tip_Entry.text())/100))}")

            
            except ValueError:
                self.cust_tip_Output.setText("The input given is invalid")

#----------END OF CLASS----------


#----------Twitter Scraper UI----------
    class TwitterScraper(QWidget):
        keys = []
        with open('C:/Users/Hasan/Desktop/Live-NEA/keys/twitterAPIkeys.txt','r') as f:
            for line in f:
                keys.append(line.rstrip('\n'))

        client = tweepy.Client(
            bearer_token= keys[0],
            consumer_key= keys[1],
            consumer_secret= keys[2],
            access_token= keys[3],
            access_token_secret= keys[4],
            )

        def __init__(self,user):
            super().__init__()
            self.username = user
            self.setFixedSize(984,412)
            self.setWindowTitle(f"Twitter Scraper {vers_no} - Username: {self.username}")
            self.Twitter_Scraper()

        
        def Twitter_Scraper(self):
            #The Return box for all the searches
            self.Output_Window = QtWidgets.QTextBrowser(self)
            self.Output_Window.setGeometry(QtCore.QRect(310, 0, 671, 411))
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
            self.Mic_Search.clicked.connect(lambda: [self.mic_search()])


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
            self.Submit_req.clicked.connect(self.check_type)

            self.req_history = QtWidgets.QPushButton(self)
            self.req_history.setGeometry(QtCore.QRect(60, 200, 181, 23))
            self.req_history.setObjectName("req_history")
            self.req_history.clicked.connect(self.logs)


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

            """
            Label Predefined Text
            """

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

            #Watermarks
            self.ID_box.setPlaceholderText("Enter a Twitter Handle")
            self.Query_box.setPlaceholderText("Enter a search")
            self.max_results.setPlaceholderText("10 to 100")

        def ToggleSearch(self):
            if self.by_TwitterUser.isChecked():
                self.Search_Query.hide()
                self.Query_box.hide()
                self.Mic_Search.hide()
            else:
                self.Search_Query.show()
                self.Query_box.show()
                self.Mic_Search.show()
        
        def clearEntries(self):
            self.ID_box.clear()
            self.Query_box.clear()
            self.max_results.clear()
        
        def activeExclusion(self):
            if self.exclu_Retweets.isChecked():
                self.Retweets.setText("Retweets Disabled!")
            else:
                self.Retweets.setText(" ")
        
        def ID_Grabber(self,client, handle):
            try:
                user = str(client.get_user(username= handle))
                Response = user.split(' ')
                id = Response[1].removeprefix('id=')
                return id
            except:
                self.Output_Window.append("\nID is invalid")

        def by_User(self):
            log = open("Twitter_Logs.txt","a")
            try:
                if "@" in self.ID_box.text():
                    handle = self.ID_box.text().removeprefix("@")
                    id = self.ID_Grabber(self.client,handle)
                else:
                    id = self.ID_Grabber(self.client,self.ID_box.text())
            except:
                print("400 Bad Response")
            
            exclusions = "replies"
            if self.exclu_Retweets.isChecked():
                exclusions = "retweets"
            
            max_results = 10
            try:
                if int(self.max_results.text()) < 10:
                    self.Output_Window.append("\nMax num too low, defaulting to 10")
                elif int(self.max_results.text()) > 300:
                    self.Output_Window.append("\nmax num too high, defaulting to 10")
                else:
                    max_results = int(self.max_results.text())

            except ValueError:
                self.Output_Window.append("The Maximum Number is invalid: Max Results defaulted to 10")

            if id == None:
                self.Output_Window.append("Handle Invalid or Blank")
            else:
                try:
                    self.Output_Window.append("\n"+"\/"*78)
                    self.Output_Window.append(f"Twitter Handle:{self.ID_box.text()}, Results Requested:{max_results}")

                    log.write(f"\nUsername: {self.username}, Max Results: {max_results}, Username: {self.ID_box.text()}")

                    for tweet in tweepy.Paginator(self.client.get_users_tweets, int(id), exclude = exclusions, max_results = 100).flatten(limit = max_results):
                        self.Output_Window.append(f"\n{tweet}")
                        log.write(f"\n{tweet}")
                        self.clearEntries()

                except tweepy.TweepyException:
                    self.Output_Window.append("Request Invalid or API Tweet Cap Reached")
            
            log.close()
        
        def all_twitter(self):
            try:
                query = self.Query_box.text()
            except:
                self.Output_Window.append("API cannot parse query")
            
            max_results = 10
            try:
                if int(self.max_results.text()) < 10:
                    self.Output_Window.append("\nMax num too low, defaulting to 10")
                elif int(self.max_results.text()) > 300:
                    self.Output_Window.append("\nmax num too high, defaulting to 10")
                else:
                    max_results = int(self.max_results.text())
            
            except ValueError:
                self.Output_Window.append("The Maximum Number is invalid: Max Results defaulted to 10")

            self.Output_Window.append("\n"+"\/"*78)
            self.Output_Window.append(f"Search Query:{self.Query_box.text()}, Results Requested:{max_results}")

            for tweet in tweepy.Paginator(self.client.search_recent_tweets, query, max_results = 100).flatten(limit = max_results):
                self.Output_Window.append(f"\n{tweet}")
                
        def mic_search(self):
            self.Output_Window.append("Listening...")
            self.Query_box.setText(" ")
            r = sr.Recognizer()
            mic = sr.Microphone()

            r.dynamic_energy_threshold = True
            
            output= {
                'transcription':'None',
                'Errors': None,
            }

            QApplication.processEvents()
            with mic as source:
                try:
                    listen = r.listen(source)
                    output['transcription'] = r.recognize_google(listen)
                    self.Query_box.setText(output['transcription'])

                except sr.UnknownValueError:
                    self.Output_Window.append("I couldn't understand that, try again")
            
        
        def check_type(self):

            dialog = QMessageBox(self)
            dialog.setWindowTitle("Something went wrong!")
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setText("Seems Like You Didn't Choose a 'Search By' Option!")

            if self.by_TwitterUser.isChecked():
                return self.by_User()
            
            elif self.by_TwitterAll.isChecked():
                return self.all_twitter()
            
            else:
                dialog.exec()
        
        def logs(self):
            try:
                os.startfile("C:/Users/Hasan/Desktop/Live-NEA/Twitter_Logs.txt")
            except:
                self.Output_Window.append("\nThe File does not exist yet")
            


#----------END OF CLASS---------

def window():
    app = QApplication(sys.argv)
    win = LoginPage()
    win.show()
    sys.exit(app.exec_())

window()