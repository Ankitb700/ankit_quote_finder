
#main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json,glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
 
Builder.load_file('design2.kv')
 
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def login(self,uname,pword):
        with open("user.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_sucess"
        else:
             self.ids.login_wrong.text = "wrong username or password"

 
class RootWidget(ScreenManager):
    pass

class SignupScreen(Screen):
    def add_user(self,uname,pword):
        with open("user.json") as file:
            users = json.load(file)
        

        users[uname] = {'username':uname,'password':pword,
        'created':datetime.now().strftime("%y-%m-%d %H-%M-%S")} 
        with open("user.json","w") as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_sucess"

class SignUpScreenSucess(Screen):
    def go_to_login(self):

        self.manager.transition.direction= "right"
        self.manager.current = "Login_screen"

class LoginScreenSucess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Login_screen"
    
    def get_quote(self,feel):
        feel = feel.lower()
        available_feelings  = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt",encoding ="utf8" ) as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try Another Feelings"
    
    class ImageButton(ButtonBehavior, HoverBehavior,Image):
        pass

class MainApp(App):
    def build(self):
        return RootWidget()
 
if __name__ == "__main__":
    MainApp().run()