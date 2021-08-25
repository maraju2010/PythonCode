import time
import sys
from FinesseApi import FinesseApi
from Layout import Layout
from TeamObject import TeamObject
from backup import backup

class App(object):

        def __init__(self,pub,username,password,TeamName=None,takebackup=False):
            self.TEAM_TABLE = []
            self.Tmp = {}
            self.Teams = 1
            self.getLayout = 1
            self.setLayout = 1
            self.looptimer = 5
            self.loopList = ["Teams","getLayout","setLayout"]
            self.pub = pub
            self.takebackup=takebackup
            self.teamname = TeamName
            self.username = username
            self.password = password


        def getTeams(self):
            API="/finesse/api/Teams"
            try:
                self.__GET(API,Fteam=True)
            except Exception as e:
                print("##### exception in response from server: %s #####" % (e))

        def findLayout(self,Team,Name):
            API = "/finesse/api/Team/<id>/LayoutConfig"
            newAPI = API.replace("<id>",Team)
            self.__GET(newAPI,Name,Team,Flayout=True)

        def updateLayout(self,ins):
            API = "/finesse/api/Team/<id>/LayoutConfig"
            newAPI = API.replace("<id>",ins.Id)
            self.__PUT(newAPI,ins)

        def __GET(self,path,Name=None,Team=None,Fteam=False,Flayout=False):
             api = FinesseApi(self.pub,self.username,self.password)

             url = api.SCHEME + "://" + api.PRIMARY_FINESSE_SERVER  + path
             response = api.GET(url,api.username,api.password)

             if "exception-5XX" in response:
                 print("##### exception in response from server %s: %s #####" % (api.PRIMARY_FINESSE_SERVER,response))
             else:
                 if Flayout==True:
                     if Team:
                         if self.takebackup:
                                execmsg = backup.output_to_file(Name,response.text,api.PRIMARY_FINESSE_SERVER)
                                print(execmsg)
                         else:
                             t = TeamObject(api.PRIMARY_FINESSE_SERVER,Team,response.text,self.Tmp.get(Team))
                             self.TEAM_TABLE.append(t)
                         #self.Tmp[Team].append(response.text)
                 if Fteam==True:
                    if response.status_code==200:
                        ly = Layout()
                        self.Tmp = ly._parse(response.text)
                        print("##### received response from server %s: %s #####" % (api.PRIMARY_FINESSE_SERVER,response.status_code))
                    else:
                        print("##### received response from server %s: %s #####" % (api.PRIMARY_FINESSE_SERVER,response.status_code))

        def  __PUT(self,path,ins):
                api = FinesseApi(self.pub,self.username,self.password)
                url = api.SCHEME + "://" + api.PRIMARY_FINESSE_SERVER  + path
                response = api.PUT(url,api.username,api.password,data=ins.Layout)
                if "exception-5XX" in response:
                    print("##### exception in response from server %s: %s #####" % (api.PRIMARY_FINESSE_SERVER,response))
                else:
                    if  response.status_code==200:
                        print("##### received response from server %s: %s #####" % (api.PRIMARY_FINESSE_SERVER,response.status_code))
                    else:
                        print("##### exception in response from server %s: %s #####" % (api.PRIMARY_FINESSE_SERVER,response.status_code))

        def _run(self):
           try:
                for  i in self.loopList:
                    if i=="Teams":
                        self.getTeams()
                    if i=="getLayout":
                        for k,v in self.Tmp.items():
                            if self.teamname == "ALL":
                                self.findLayout(k,v[0])
                            elif  v[0]==self.teamname:
                                self.findLayout(k,v[0])
                            elif self.takebackup:
                                self.findLayout(k,v[0])
                            else:
                                pass

                    if i=="setLayout":
                        if self.takebackup:
                            pass
                        else:
                            for j in self.TEAM_TABLE:
                                if j.systemlayout=="false":
                                    self.updateLayout(j)
                    time.sleep(self.looptimer)
           except Exception as e:
                print("##### Exception raised while executing loop : %s" %(e))
                sys.exit(1)

def test():
    """Test program for Finesse Layout update.
    Usage: python App.py [-d] ... [finessepub [username [password]]]
    """
    print("##### Inputs received from command prompt %s #####" %(sys.argv[1:]))
    if sys.argv[1]=="-d" and len(sys.argv[1:5])==4:
        finessePub = ""
        if sys.argv[1:]:
            finessePub = sys.argv[2]

        username = ""
        if sys.argv[2:]:
            username = sys.argv[3]

        password=""
        if sys.argv[3:]:
            password = sys.argv[4]

        takebackup=False
        TeamName = ""
        if len(sys.argv[1:])==5:
            arg5 = sys.argv[5]
            if arg5=="takebackup":
                takebackup=True
            if arg5=="ALL":
                TeamName = "ALL"
            if arg5!="takebackup" and arg5!="ALL":
                TeamName = arg5

        try:
            if takebackup:
                print("##### enable layout backup workflow #####")
            else:
                print("##### enable layout update workflow #####")
            a= App(finessePub,username,password,TeamName,takebackup)
            print("##### Application Initialized #####")
            a._run()
        except Exception as e:
            print("#### exception while initializing Application : %s ####" %(e))
            sys.exit(1)
    else:
        print("#### exception while initializing Application : %s ####" %("""Usage for backup: python App.py -d finessepub  username  password takebackup"""))
        print("#### exception while initializing Application : %s ####" %("""Usage: python App.py -d finessepub  username  password """))

        sys.exit(1)

if __name__ == "__main__":
    test()
