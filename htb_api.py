import requests
import json
from HTMLParser import HTMLParser

ranks={'Noob':0.0,'Script Kiddie':5.0,'Hacker':20.0,'Pro Hacker':45.0,'Elite Hacker':70.0,'Guru':90.0}

class cli_colors:
    header = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

log_OK = 0
log_INFO = 1
log_ERROR = 2
log_HEADING = 3
log_NULL = 4
#log_type: 0 = okgood | 1 = info | 2 = error | 3 = heading | 4 = standard print

ranks=[0.0,5.0,20.0,45.0,70.0,90.0,100.0]
ranks_string = ['Noob','Script Kiddie', 'Hacker', 'Pro Hacker', 'Elite Hacker', 'Guru', 'Omniscient']

class HTBAPI(object):
    def __init__(self, configfile="config",loglevel=2):
        self.configfile = configfile
        self.loglevel = loglevel
        self.cfg = self.config()
        
    def init(self):
      self.s = self.login()
      self.profile, self.rank = self.parseprofile()
      self.ownership = self.calcownership()
      self.currentrank, self.nextrank, self.nextownership = self.get_ranks()
      self.get_m_c() 

    def log(self,msg, log_type=4):
      msg = self.html_unescape(msg)
      if log_type == 4:
        print msg
      elif log_type == 3:
        if self.loglevel == 2:
          print cli_colors.bold+cli_colors.green + "----------"+ str(msg) + "----------" + cli_colors.endc 
        elif self.loglevel == 1:
          print "----------"+ str(msg) + "----------"
        else:
          return
      elif log_type == 2:
        if self.loglevel == 2:
          print cli_colors.fail + "[-] "+cli_colors.endc + str(msg)
        else:
          print "[-] " + str(msg)
      elif log_type == 1:
        if self.loglevel == 2:
          print cli_colors.blue + "[*] "+cli_colors.endc + str(msg)
        elif self.loglevel == 1:
          print "[*] " + str(msg)
        else:
          return
      elif log_type == 0:
        if self.loglevel == 2:
          print cli_colors.green + "[+] "+cli_colors.endc + str(msg)
        elif self.loglevel == 1:
          print "[+] " + str(msg)
        else:
          return

    def html_unescape(self,s):
      return HTMLParser().unescape(s) 

    def get_ranks(self):
      i = 0
      for rank in ranks:
        if self.ownership < float(rank):
          return ranks_string[i-1], ranks_string[ranks_string.index(self.rank)+1], ranks[i]
        i+=1
      
      return ranks_string[0], ranks_string[1], ranks[1]

    def config(self):
      try:
        cfg = json.loads(open(self.configfile,"r").read())
        api = cfg['api']
        self.userid = int(api['userid'])
        self.username = str(api['username'])
        self.password = str(api['password'])
        self.email = str(api['email'])
        search = cfg['search']
        self.searchuserid = search['userid']
        self.searchusername = search['username']

        self.searchprofileurl = "https://www.hackthebox.eu/home/users/profile/"+str(self.searchuserid)
        return cfg
      except:
        self.log(self.configfile+" not found",log_ERROR)
        
    def login(self):
        s=requests.Session()
        r=s.get("https://www.hackthebox.eu/login") #get csrf-token
        #csrftoken=r.content.split('name="_token" value="')[0].split('"')[0]
        #csrftoken=r.content[:5190][5150:].split("'")[0]
        csrftoken=r.content.split('name="_token" value=')[1].split(">")[0].replace('"', "")
        data={'_token':csrftoken,'email':self.email,'password':self.password}
        r=s.post("https://www.hackthebox.eu/login",data=data)
        if not r.status_code == 200 or not s.get(self.searchprofileurl).status_code == 200:
          self.log("Login failed",log_ERROR)
          exit(-1)     
        else:
          self.log("Login Successful",log_OK)
          return s

    def parseprofile(self):
      self.log("Parsing profile",log_INFO)
      s = self.s
      r = s.get("https://www.hackthebox.eu/home/users/points/"+str(self.searchuserid))
      if not r.status_code == 200:
        self.log("Error while trying to parse the profile",log_ERROR)
      html = r.content
      ownedusers = float(html.split("<p>Owned Users: <code>")[1].split("/")[0])
      activemachines = float(html.split("<p>Owned Users: <code>")[1].split("</code>")[0].split("/")[1])
      ownedsystems = float(html.split("<p>Owned Systems: <code>")[1].split("</code>")[0].split("/")[0])
      ownedchallenges = float(html.split("<p>Owned Challenges: <code>")[1].split("/")[0])
      activechallenges = float(html.split("<p>Owned Challenges: <code>")[1].split("</code>")[0].split("/")[1])
 
      
      profile = json.dumps({'ownedusers':ownedusers,'ownedsystems':ownedsystems,'activemachines':activemachines,'ownedchallenges':ownedchallenges,'activechallenges':activechallenges})
      r = s.get("https://www.hackthebox.eu/home/users/profile/"+str(self.searchuserid))
      rank = r.content.split('</span> <span class="c-white">')[1].split('</span>')[0]

      
      return profile, rank

    def calcownership(self,_profile=""):
       if _profile == "" or _profile == None:
         profile=json.loads(self.profile)
       else:
         profile=json.loads(_profile)

       return (float(profile['ownedsystems']) + (float(profile['ownedusers']) / 2.) + (float(profile['ownedchallenges']) / 10.)) / (float(profile['activemachines']) + (float(profile['activemachines']) / 2.) + (float(profile['activechallenges']) / 10.)) * 100.

    def ratingtodifficulty(self,ratinglist):
      oa_ratings = 0.
      score = 0.
      i = 1.
      for r in ratinglist:
        oa_ratings += r
        score += (r * i)
        i+=1.
      difficulty = int(round((float(score) / float(oa_ratings * 10.)) * 100.))
      return difficulty

    def get_machines(self):
      self.log("Parsing machines", log_INFO)
      machines = []
      s = self.s
      r=s.get("https://www.hackthebox.eu/home/machines/list")
      machinesparse = r.content.split("https://www.hackthebox.eu/home/machines/profile/")
      machinelist = []
      idlist = []
      for machine in machinesparse:
          m = machine.split('">')[1].split("</a>")[0]
          if not "<" in m:
            machinelist.append(m)
            machineid = int(machine.split('">')[0])
            idlist.append(machineid)

      userownssplit = r.content.split('$("#userowned')
      systemownssplit = r.content.split('$("#systemowned')

      userownslist = []
      systemownslist = []
      for userowns in userownssplit:
        if "([" in userowns:
          try:
           uo = int(userowns.split("([")[1].split(",")[0])
           userownslist.append(uo)
          except:
            continue

      for systemowns in systemownssplit:
        if "([" in systemowns:
          try:
           so = int(systemowns.split("([")[1].split(",")[0])
           systemownslist.append(so)
          except:
            continue        
      
      for i in range(0,len(machinelist)):
        machine = {}
        machine['name'] = machinelist[i]
        machine['id'] = idlist[i]
        machine['url'] = "https://www.hackthebox.eu/home/machines/profile/"+str(idlist[i])
        machine['userowns'] = userownslist[i]
        machine['systemowns'] = systemownslist[i]
        machines.append(machine)
      for machine in machines:
        r=s.get(machine['url'])
        difficulty = int(r.content.split('/10">')[1].split("width: ")[1].split("%")[0])
        machine['difficulty'] = difficulty
      
      r=s.get("https://www.hackthebox.eu/home/users/profile/"+str(self.searchuserid))
      for machine in machines:
        machine['solved'] = r.content.count(">"+machine['name']+"<")
              
      return json.dumps(machines)  

    def get_challenges(self):
       self.log("Parsing challenges",log_INFO)
       s = self.s
       challenges = []
       categories = ['Reversing','Crypto', 'Stego','Pwn','Web','Misc','Forensics']
       for category in categories:
         r=s.get("https://www.hackthebox.eu/home/challenges/"+category)
         htmlsplit = r.content.split(" [by <a")
         
         ratingsplitlist = r.content.split('$("#diffchart')
         difficultylist = []
         for rating in ratingsplitlist:
           ratinglist = []
           rlist = rating.split("[")[1].split("]")[0].replace(" ","").split(",")
           if len(rlist) >= 2:
             rlist = rlist[:-1]
             for elem in rlist:
               ratinglist.append(int(elem))

           if len(ratinglist) > 0:
             difficultylist.append(self.ratingtodifficulty(ratinglist))  
         
         solvesplit = r.content.split(" solvers]")
         solvelist = []
         for solves in solvesplit:
           if '">[' in solves:
             solvelist.append(int(solves.split('">[')[1]))

         i = 0 
         for c in htmlsplit:
             if "] </span> " in c:
               challenge = {}
               challenge['name'] = (c.split("] </span> ")[1])
               challenge['category'] = category
               challenge['difficulty'] = difficultylist[i]
               challenge['solves'] = solvelist[i]
               challenges.append(challenge)
             i+=1
       r=s.get("https://www.hackthebox.eu/home/users/profile/"+str(self.searchuserid))
       for challenge in challenges:
         challenge['solved'] = r.content.count("> "+challenge['name']+" <")
       return json.dumps(challenges)
       
    def get_m_c(self):
      self.machines = self.get_machines()
      self.challenges = self.get_challenges()
      self.log("Done with parsing challenges and machines!",log_OK)
   
      
      
      
          

 


