import os
import time
import psutil
import json
import platform
import datetime
from hurry.filesize import size,si
from time import sleep
class App:
    def main(self):
        if self.status == "ST_NOM":
            self.data = {"STATUS":"ST_NOM","CPU":psutil.cpu_percent(0.5),"RP":psutil.virtual_memory().percent,"FD":size(psutil.disk_usage("/").free,system=si),"TD":size(psutil.disk_usage("/").total,system=si)}
            self.sendJSON()
    status = "ST_NOM"
    useEmu = True
    data = {}
    def sendJSON(self):
        if self.useEmu:
            DispEmu.parseJSON(self.data)
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
    def parseJSON(self,json):
        buf = []
        if self.state == 0:
            buf.append("sd")
            buf.append("asd")
        if self.state == 1:
            buf.append("CPU " + str(json["CPU"])+"%")
            buf.append("RAM " + str(json["RP"])+"% used")
        if self.state == 2:
            buf.append("HD "+str(json["FD"])+"/"+str(json["TD"])+" Free")
            buf.append("OS "+platform.platform(True,True))
        self.println(buf)
        if self.state == 2 :
            self.state = 0
        else:
            self.state = self.state + 1
DispEmu = DispEmc()
ss = App()
while True:
    ss.main()
    sleep(0.5)
