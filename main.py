from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
from pathlib import Path
from datetime import datetime
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
Builder.load_file('design.kv')
import random
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and pword == users[uname]["password"]:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password"


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname,
                        'password': pword,
                        'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json",'w') as file:
            json.dump(users,file,indent=2)
        self.manager.current ="sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current ="login_screen"

class LoginScreenSucess(Screen):
    def log_out(self):
        self.manager.transition.direction ='right'
        self.manager.current = "login_screen"
    def get_quote(self,feeling):
        feeling = feeling.lower()
        available_feelings = glob.glob("quotes/*txt")
        available_feelings = [Path(filename).stem for filename in available_feelings]

        if feeling in available_feelings:
            with open(f"quotes/{feeling}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass
class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()
