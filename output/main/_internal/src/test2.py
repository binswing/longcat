from test import myClass
import threading

def on_connect(result):
    print("Connected with result code "+str(result))

myclass = myClass
myClass.add_listener(on_connect)

myclass.connect()
myclass.connect()
myclass.connect()
myclass.connect()
myclass.connect()
