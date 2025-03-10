import flet as ft
import random
from flet import TextField, Checkbox, ElevatedButton, Text
from flet import Page, Row, Column, Card, Container, View
from flet import FontWeight, TextAlign, MainAxisAlignment, CrossAxisAlignment
from flet_core.control_event import ControlEvent


class Home(Column):
    def __init__(self) -> None:
        super().__init__()
        self.width = 400
        self.controls = [
            Text(
                value='Home', 
                size=24, 
                weight=FontWeight.BOLD
            ),
            ElevatedButton(
                text='Login to Snowflake', 
                width=self.width, 
                disabled=False,
                on_click=lambda _: self.page.go("/login")
            )
        ]
        

class Login(Column):
    def __init__(self) -> None:
        super().__init__()
        self.user: str = ''
        self.width = 400
        self.title = Text(
            value='Snowflake Login', 
            size=24, 
            weight=FontWeight.BOLD
        )
        self.user_input = TextField(
            label='Username', 
            text_align=TextAlign.LEFT, 
            width=self.width,
            on_change=self.user_input_change
        )
        self.submit_btn = ElevatedButton(
            text='Login with SSO', 
            width=self.width, 
            disabled=self.user.strip() == '',
            on_click=self.login
        )
        self.error_msg = Text(
            value='', 
            size=12,
            visible=False
        )
        self.controls=[
            self.title,
            self.user_input,
            self.submit_btn,
            self.error_msg
        ]
    
    def user_input_change(self, e):
        self.user = self.user_input.value
        self.submit_btn.disabled = self.user.strip() == ''
        self.update()
        
    def login(self, e: ControlEvent):
        if random.randint(0, 9) % 2 == 0:  # login failed
            self.error_msg.value = 'Error: Invalid username!'
            self.error_msg.visible = True
            self.update()
        else:
            self.error_msg.value = ''
            self.error_msg.visible = False
            self.page.session.set(
                key='sf_conn', 
                value={
                    'user': self.user, 
                    'conn': 'connected'
                }
            )
            self.page.go('/loggedin')
            

class Loggedin(Column):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.width = 400
        self.title = Text(
            value='Snowflake Login', 
            size=24, 
            weight=FontWeight.BOLD
        )
        self.logged_info = Text(
            value=f'You are logged in as {self.user}',
            size=12
        )
        self.logout_btn = ElevatedButton(
            text='log Out', 
            width=self.width, 
            disabled=False,
            on_click=self.logout
        )
        self.controls=[
            self.title,
            self.logged_info,
            self.logout_btn
        ]
    
    def logout(self, e: ControlEvent):
        self.page.session.remove('sf_conn')
        self.page.go('/login')


class MyApp:
    def __init__(self, page: Page):
        self.page = page
        self.page.title = 'Signup'
        self.page.horizontal_alignment = CrossAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 50
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.resizable = False
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

    def add_home_view(self):
        appbar = ft.AppBar(
            title=Text('Data Package Generation Tool'), 
            color='white',
            bgcolor='orange',
        )
        home_view = View(
            route='/', 
            controls=[appbar, Home()],
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
        self.page.views.append(home_view)
    
    def add_login_view(self):
        appbar = ft.AppBar(
            title=Text('Data Package Generation Tool'), 
            color='white',
            bgcolor='orange',
        )
        if self.page.session.get('sf_conn'):
            self.page.go('/loggedin')
            return
        login_view = View(
            route='/login',
            controls=[appbar, Login()],
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
        self.page.views.append(login_view)
    
    def add_loggedin_view(self):
        appbar = ft.AppBar(
            title=Text('Data Package Generation Tool'), 
            color='white',
            bgcolor='orange',
        )
        if not self.page.session.get('sf_conn'):
            self.page.go('/login')
            return
        user = self.page.session.get('sf_conn')['user']
        loggedin_view = View(
            route='/login',
            controls=[appbar, Loggedin(user)],
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
        self.page.views.append(loggedin_view)
    
    def route_change(self, route):
        self.page.views.clear()
        self.add_home_view()
        if self.page.route == '/login':
            self.add_login_view()
        if self.page.route == '/loggedin':
            self.add_loggedin_view()
        self.page.update()
        
    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
        
        

def main(page: Page) -> None:
    MyApp(page)
    page.go(page.route)
    
    
if __name__ == '__main__':
    ft.app(target=main)
