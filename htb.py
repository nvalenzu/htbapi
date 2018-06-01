import json
from htb_api import *
 

#################
CONFIGFILE = "config"
LOGLEVEL = 2	 #0 = no debug info, 1 = debug info, 2 = debug info with colors

MAX_CHALLENGES = 10
EXTRA_SYSTEM_DIFFICULTY = 5
MAX_OPTIONS = 5
#################

log_OK = 0
log_INFO = 1
log_ERROR = 2
log_HEADING = 3
log_NULL = 4


def get_difficulty_sorted_machines(htbapi):
  machines = json.loads(htbapi.machines)
  difficultylist = []
  for machine in machines:
    difficultylist.append(int(machine['difficulty']))
  sorted_dl = sorted(difficultylist)
  sorted_machines = []
  _machines = machines
  for dif in sorted_dl:
    for machine in _machines:
      if machine['difficulty'] == dif:
        if not machine['solved'] == 2:
          if machine['solved'] == 1:
            nmachine = {'name':str(machine['name']),'difficulty':machine['difficulty'],'id':machine['id'],'owntype':'system','type':'machine'}
            sorted_machines.append(nmachine)
          elif machine['solved'] == 0:
            nmachine = {'name':str(machine['name']),'difficulty':machine['difficulty'],'id':machine['id'],'owntype':'user','type':'machine'}
            sorted_machines.append(nmachine)
            nmachine = {'name':str(machine['name']),'difficulty':(machine['difficulty']+EXTRA_SYSTEM_DIFFICULTY),'id':machine['id'],'owntype':'system','type':'machine'}
            sorted_machines.append(nmachine)
        _machines.remove(machine)

  difficultylist = []
  sorted_dl = []
  _sorted_machines = sorted_machines
  sorted_machines = []
  for machine in _sorted_machines:
    difficultylist.append(int(machine['difficulty']))
  sorted_dl = sorted(difficultylist)
  for dif in sorted_dl:
    for machine in _sorted_machines:
      if machine['difficulty'] == dif:
        sorted_machines.append(machine)
        _sorted_machines.remove(machine)
  return sorted_machines

def get_difficulty_sorted_challenges(htbapi):
  challenges = json.loads(htbapi.challenges)
  difficultylist = []
  for challenge in challenges:
    difficultylist.append(int(challenge['difficulty']))
  sorted_dl = sorted(difficultylist)
  sorted_challenges = []
  _challenges = challenges
  for dif in sorted_dl:
    for challenge in _challenges:
      if challenge['difficulty'] == dif:
        if not challenge['solved'] == 1:
          nchallenge = {'name':str(challenge['name']),'difficulty':challenge['difficulty'],'category':challenge['category']}
          sorted_challenges.append(nchallenge)
        _challenges.remove(challenge)
  return sorted_challenges
  
def get_machine_only_solve_min(htbapi,machines_ts):
  slist = []
  u_s_c_owns = {'system':0.0,'user':0.0, 'challenges': 0.0}
  profile = json.loads(htbapi.profile)
  ownership = htbapi.ownership
  for machine in machines_ts:
    if machine['owntype'] == 'user':
      profile['ownedusers'] += 1.
      u_s_c_owns['user'] += 1.
    elif machine['owntype'] == 'system':
      profile['ownedsystems'] += 1.
      u_s_c_owns['system'] += 1.
    _profile = json.dumps(profile)
    nownership = htbapi.calcownership(_profile)
    slist.append(machine)
    if float(nownership) >= float(htbapi.nextownership):
      break
  return slist, u_s_c_owns 

def get_needed_challenges(htbapi,_min_machines_ts_list,challenges_ts):
  ts_list = []
  profile = json.loads(htbapi.profile)
  u_s_c_owns = {'system':0.0,'user':0.0, 'challenges': 0.0}
  _profile = profile
  for machine in _min_machines_ts_list:
    ts_list.append(machine)
    if machine['owntype'] == 'user':
      _profile['ownedusers']+=1.
      u_s_c_owns['user']+=1.
    elif machine['owntype'] == 'system':
      _profile['ownedsystems']+=1.
      u_s_c_owns['system']+=1.
  for i in range(0,len(challenges_ts)):
    challenge = challenges_ts[i]
    challenge['type'] = "challenge"
    ts_list.append(challenge)
    _profile['ownedchallenges']+=1.
    u_s_c_owns['challenges']+=1.
    nownership = htbapi.calcownership(json.dumps(_profile))  
    if float(nownership) >= float(htbapi.nextownership):
      break
  
  return ts_list, u_s_c_owns

def calculate_solve_options(htbapi):
  htbapi.log("Searching for different ways to reach "+htbapi.nextrank,log_INFO)
  options = []
  profile = htbapi.profile
  machines_ts = get_difficulty_sorted_machines(htbapi)
  challenges_ts = get_difficulty_sorted_challenges(htbapi)
  
  u_s_c_owns = {'system':0.0,'user':0.0, 'challenges': 0.0}
  min_machines_ts_list = []

  min_machines_ts_list, u_s_c_owns, = get_machine_only_solve_min(htbapi,machines_ts)
  options.append(min_machines_ts_list)

  _min_machines_ts_list = min_machines_ts_list
  count = 0
  while u_s_c_owns['challenges'] <= MAX_CHALLENGES and count < MAX_OPTIONS: # and ((u_s_c_owns['user'] + u_s_c_owns['system']) >= 1)
    count += 1
    ts_list = []
    min_machines_ts_list = _min_machines_ts_list
    _min_machines_ts_list = min_machines_ts_list[:-1]
    ts_list, u_s_c_owns = get_needed_challenges(htbapi,_min_machines_ts_list,challenges_ts)
    if not ts_list in options:
      options.append(ts_list)
    else:
      break
  return options

def get_u_s_c(objs):
  u_s_c_owns = {'system':0.0,'user':0.0, 'challenges': 0.0}
  for obj in objs:
    if obj['type'] == 'machine':
      if obj['owntype'] == 'user':
        u_s_c_owns['user']+=1.
      elif obj['owntype'] == 'system':
        u_s_c_owns['system']+=1.
    else:
      u_s_c_owns['challenges']+=1.

  return u_s_c_owns
    
def average_difficulty(objs):
  av = 0.
  for obj in objs:
    av += float(obj['difficulty'])
  return round((av / float(len(objs))),2)
  
def get_solve_options(htbapi):
  options = calculate_solve_options(htbapi)
  if not LOGLEVEL == 0:
    htbapi.log("Calculated the "+str(len(options))+" easiest ways to reach "+htbapi.nextrank, log_OK)
  else:
    htbapi.log("Calculated the "+str(len(options))+" easiest ways to reach "+htbapi.nextrank)
  htbapi.log("")
  htbapi.log("")
  for option in options:
    machinestr = "Machines:  "
    for obj in option:
      if obj['type'] == 'machine':
          machinestr += obj['name']+" "+obj['owntype']+", "
    if not LOGLEVEL == 0:
      if not machinestr == "Machines:  ":
        htbapi.log(machinestr[:-2],log_OK)
    else:
      if not machinestr == "Machines:  ":
        htbapi.log(machinestr[:-2])
    if not option == options[0]:   
      challengestr = "Challenges:  "
      for obj in option:
        if obj['type'] == 'challenge':
          challengestr += obj['name']+" ("+obj['category']+"), " 
      if not LOGLEVEL == 0:
        htbapi.log(challengestr[:-2],log_OK)
        u_s_c = get_u_s_c(option)
        htbapi.log(str(int(u_s_c['user']))+" user, "+str(int(u_s_c['system']))+" system, "+str(int(u_s_c['challenges']))+" challenges",log_OK)
        av = average_difficulty(option)
        htbapi.log("Difficulty: "+str(av)+"%",log_OK) 
      else:
        htbapi.log(challengestr[:-2])
        u_s_c = get_u_s_c(option)
        htbapi.log(str(int(u_s_c['user']))+" user, "+str(int(u_s_c['system']))+" system, "+str(int(u_s_c['challenges']))+" challenges")
        av = average_difficulty(option)
        htbapi.log("Difficulty: "+str(av)+"%")
      if not option == options[-1]:
        htbapi.log("")
        htbapi.log("")
    else:
      u_s_c = get_u_s_c(option)
      if not LOGLEVEL == 0:
        htbapi.log(str(int(u_s_c['user']))+" user, "+str(int(u_s_c['system']))+" system, "+str(int(u_s_c['challenges']))+" challenges",log_OK)
        av = average_difficulty(option)
        htbapi.log("Difficulty: "+str(av)+"%",log_OK) 
      else:
        htbapi.log(str(int(u_s_c['user']))+" user, "+str(int(u_s_c['system']))+" system, "+str(int(u_s_c['challenges']))+" challenges")
        av = average_difficulty(option)
        htbapi.log("Difficulty: "+str(av)+"%")
      htbapi.log("")
      htbapi.log("")

def userinfo(htbapi):
  htbapi.log("")
  htbapi.log(htbapi.searchusername,log_HEADING)
  htbapi.log("- Rank: "+htbapi.rank)
  htbapi.log("- Ownership: "+str(round(htbapi.ownership,2))+"%")
  #htbapi.log("Rank: ")
  htbapi.log("") 
    

htbapi = HTBAPI(configfile=CONFIGFILE, loglevel=LOGLEVEL)
htbapi.init()

machines = htbapi.machines
challenges = htbapi.challenges
#htbapi.machines = open("m","r").read()
#htbapi.challenges = open("c","r").read()

userinfo(htbapi)
get_solve_options(htbapi)

