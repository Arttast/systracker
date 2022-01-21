from genericpath import exists
import os
import shlex
import time,argparse, configparser
import psutil,serial
import json
import platform
import datetime
import distro
import ctypes, sys
def is_admin():
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return True
if is_admin():
     winno = False
     from hurry.filesize import size,si
     from time import sleep
     if platform.system() == "Windows":
          import win32serviceutil
     else:
         winno = True
     class App:
         def __init__(self) -> None:
                self.a = False               
                parser = argparse.ArgumentParser()
                parser.add_argument("-c",required=True,help="asd")
                args = parser.parse_args()
                if str(args.c).startswith("v"):
                    self.useEmu = True
                else:
                    try:
                        if len(str(args.c)) == 1:
                         self.sel = serial.Serial("COM"+str(int(args.c[0])))
                         self.useEmu = False
                        elif len(args.c) > 1:
                            self.sel = serial.Serial(shlex.split(args.c))
                    except KeyError:
                        sys.exit("Parse Error")
                if exists("config.ini"):
                    config = configparser.ConfigParser()
                    config.read("config.ini")
                    if "Services" in config:
                        for i in config["Services"]:
                          self.argv["ser"].append(config["Services"][i])

         def handle(self) -> None:
             if not winno:
                 for i in self.argv["ser"]:
                    if win32serviceutil.QueryServiceStatus(i,None)[1] != 4:
                         win32serviceutil.StartService(i)
                         try:
                              self.servres[i] = self.servres[i]+ 1
                         except KeyError:
                              self.servres[i] = 1
             elif self.a == False & winno:
                    self.status = "ST_MSG"
                    self.msg = ["OS Does Not Support:","Services"] 
                    self.a = True
             if winno != True:
                 for i in self.servres:
                     if self.servres[i] > 2:
                         self.status = "ST_MSG"
                         self.msg[0] = "Serv. Restart 3."
                         self.msg[1] = "Srv "+ i
                         self.servres[i] = 0
             pass
             if self.status == "ST_MSG":
                 self.data = {"STATUS":"ST_MSG","MSG0":self.msg[0],"MSG1":self.msg[1]}
                 self.sendJSON()
                 self.status = "ST_NOM"
             if self.status == "ST_NOM":
                 if platform.system() == "Linux":
                     v = distro.name(True)
                 else:
                     v = platform.platform(False,True)
                 self.data = {"STATUS":"ST_NOM","CPU":psutil.cpu_percent(0.5),"RP":psutil.virtual_memory().percent,"FD":size(psutil.disk_usage("/").free,system=si),"TD":size(psutil.disk_usage("/").total,system=si),"CT":str(datetime.datetime.now().time()),"V":v,"py":platform.python_version()}
                 self.sendJSON()
         status = "ST_NOM"
         useEmu = True
         data = {}
         msg = ["",""]
         cp = 0
         argv = {"ser":[]}
         servres = {}
         def sendJSON(self):
             if self.useEmu:
                 DispEmu.parseJSON(self.data,self.status)
                 return 0
             temp = json.dumps(self.data)
             
             self.sel.write(bytes(temp+"\n","ASCII"))
             self.sel.flush()
             
     class DispEmc:
         state = 0
         def println(self,charsa):
             if winno:
                os.system("clear")
             else:
                os.system("cls")
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

     while True:
        ss.handle()
        sleep(0.5)
else:
     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
