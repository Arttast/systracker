from os import system
import psutil
import json
from hurry.filesize import size,si

class App:
    def __init__(self):
        if self.status == "ST_NOM":
            self.data = {"STATUS":"ST_NOM","CPU":psutil.cpu_percent(0.5),"RP":psutil.virtual_memory().percent,"FD":size(psutil.disk_usage("/").free,system=si),"TD":size(psutil.disk_usage("/").total,system=si)}
            self.sendJSON()
    status = "ST_NOM"
    data = {}
    def sendJSON(self):
        temp = json.dumps(self.data)
        f = open("./test/output.txt","w+t") 
        f.write(temp)
        f.flush()
        f.close()
        




clas = App()