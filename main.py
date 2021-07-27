import kivy
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
import mysql.connector as sql

Builder.load_string("""

<MyLayout>:
    Button:
        text: "Get data"
        on_press: root.get_data()
    RecycleView:
        data: [{'text':"Id:{} CName:{} WName:{} SName:{} Time:{} Date:{}".format(ID,CName,WName,SName,Time,Date)} for ID,CName,WName,SName,Time,Date in root.rows]
        viewclass: "Label"
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'

""")

class MyLayout(BoxLayout):
    rows = ListProperty([("ID","CName","WName","SName","Time","Date")])

    def get_data(self):
        con = sql.connect(host = "localhost", user = "root", password = "oogaboogappbrain123",
        database = "appointment", auth_plugin='mysql_native_password')
        cur = con.cursor()
        cur.execute("SELECT * FROM appt_list ORDER BY ID ASC")
        self.rows = cur.fetchall()
        #print(self.rows)

class MainApp(App):
    data_items = ListProperty([])

    def build(self):
        layout = GridLayout(cols = 2)
        self.CName = TextInput(text = "Enter customer's name")
        self.WName = TextInput(text = "Enter worker's name")
        self.SName = TextInput(text = "Enter service name")
        self.Time  = TextInput(text = "Enter time for the appointment")
        self.Date = TextInput(text = "Enter date for the appointment")
        self.Delete = TextInput(text = "Enter ID where you want to delete")
        submit = Button(text = "Enter", on_press = self.submit)
        #view = Widgets()
        self.button = Button(text="View Schedule")
        uselessButton = Button(text = "This button doesn't do shit click with your own risk", on_press = self.play_sound)
        remove = Button(text = "Remove row", on_press = self.remove)

        layout.add_widget(self.CName)
        layout.add_widget(self.WName)
        layout.add_widget(self.SName)
        layout.add_widget(self.Time)
        layout.add_widget(self.Date)
        layout.add_widget(self.Delete)
        layout.add_widget(submit)

        layout.add_widget(self.button)
        self.button.bind(on_press = self.onButtonPress)

        layout.add_widget(remove)
        layout.add_widget(uselessButton)

        return layout

    def submit(self, obj):
        Cus_Name = self.CName.text
        Worker_Name = self.WName.text
        Service_Name = self.SName.text
        Appt_Time = self.Time.text
        Appt_Date = self.Date.text
        con = sql.connect(host = "localhost", user = "root", password = "oogaboogappbrain123",
        database = "appointment", auth_plugin='mysql_native_password')
        cur = con.cursor()
        query = "INSERT INTO appt_list (CName, WName, SName, Time, Date) VALUES(%s, %s, %s, %s, %s)"
        val = (Cus_Name, Worker_Name, Service_Name, Appt_Time, Appt_Date)
        cur.execute(query, val)
        con.commit()
        con.close()

    def remove(self, obj):
        removeID = self.Delete.text
        con = sql.connect(host = "localhost", user = "root", password = "oogaboogappbrain123",
        database = "appointment", auth_plugin='mysql_native_password')    
        cur = con.cursor()
        query = "DELETE FROM appt_list WHERE ID = %s"
        cur.execute(query, (removeID,))
        con.commit()
        con.close()

    def play_sound(self, obj):
        sound = SoundLoader.load('fart-05.mp3')
        if sound:
            sound.play()

    def onButtonPress(self, button):
        con = sql.connect(host = "localhost", user = "root", password = "oogaboogappbrain123",
        database = "appointment", auth_plugin='mysql_native_password')
        cur = con.cursor()
        cur.execute("SELECT * FROM appt_list ORDER BY ID ASC")
        rows = cur.fetchall()     

        results = MyLayout()

        # Instantiate the modal popup and display
        popup = Popup(title ='Demo Popup',
                      content = results)  
        popup.open()   


if __name__ == '__main__':
    app = MainApp()
    app.run()









