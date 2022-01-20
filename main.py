import os
import time
import psutil
import json
import platform
import datetime
import distro
from hurry.filesize import size,si
from time import sleep
if platform.system() == "Windows":
    import win32serviceutil
else:
    winno = True
class App:
    def handle(self):
        if winno != True:
            for i in self.servres:
                if self.servres[i] <2:
                    self.status = "ST_MSG"
                    self.msg = "Serv. Restart 3."
        if self.status == "ST_MSG":
            self.data = {"STATUS":"ST_MSG","MSG0":self.msg[0],"MSG1":self.msg[1]}
            self.sendJSON()
            self.status = "ST_NOM"
        if self.status == "ST_NOM":
            if platform.system() == "Linux":
                v = distro.name(True)
            else:
                v = platform.platform(False,True)
            self.data = {"STATUS":"ST_NOM","CPU":psutil.cpu_percent(0.5),"RP":psutil.virtual_memory().percent,"FD":size(psutil.disk_usage("/").free,system=si),"TD":size(psutil.disk_usage("/").total,system=si),"CT":datetime.datetime.now().time(),"V":v,"py":platform.python_version()}
            self.sendJSON()
    status = "ST_NOM"
    useEmu = True
    data = {}
    msg = ()
    argv = {}
    servres = {}
    def connect(self):
        if not winno:
            for i in self.argv["ser"]:
                if win32serviceutil.QueryServiceStatus(self.argv["ser"][i],None) != win32serviceutil.SERVICE_RUNNING:
                    win32serviceutil.RestartService(self.argv["ser"][i])
                    self.servres[self.argv["ser"][i]] = self.servres[self.argv["ser"][i]] + 1
            
    def sendJSON(self):
        if self.useEmu:
            DispEmu.parseJSON(self.data,self.status)
            return 0
        temp = json.dumps(self.data)
        f = open("./test/output.txt","w+t") 
        f.write(temp)
        f.flush()
        f.close()
        
class DispEmc:
    state = 0
    def println(self,charsa):
        os.system("clear")
        buf = [[],[]]
        chars = [1,1]
        chars[1] = list(charsa[1])
        chars[0] = list(charsa[0])
        for i in range(0,2):
            for f in range(0,16):
                if len(chars[i]) <= f:
                    buf[i].append(" ")
                else:
                    buf[i].append(chars[i][f])
        for i in range(0,2):
            buf[i] = "".join(buf[i])
        print("+"+"----------------"+"+")
        print("|"+str(buf[0])+"|")
        print("|"+str(buf[1])+"|")
        print("+"+"----------------"+"+")
    def parseJSON(self,json,st):
        buf = []
        if st == "ST_NOM":
            if self.state == 0:
              buf.append(str(json["CT"]))
              buf.append("Python v"+str(json["py"]))
            if self.state == 1:
                buf.append("CPU " + str(json["CPU"])+"%")
                buf.append("RAM " + str(json["RP"])+"% used")
            if self.state == 2:
                buf.append("HD "+str(json["FD"])+"/"+str(json["TD"])+" Free")
                buf.append("OS "+str(json["V"]))
            self.println(buf)
            if self.state == 2 :
                self.state = 0
            else:
                self.state = self.state + 1
        elif st == "ST_MSG":
            buf.append(str(json["MSG0"]))
            buf.append(str(json["MSG1"]))
            self.println(buf)
            input()
DispEmu = DispEmc()
ss = App()
ss.connect()
while True:
    ss.handle()
    sleep(0.5)
