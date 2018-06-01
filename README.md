# htbapi
First of all you have to edit the config. Username and password are used to login.
```
{
  "search": {
    "username": "PinkPanther",
    "userid": 9539
  },
  "api": {
    "username": "ju256",
    "password": "123456",
    "email": "asdf@asdf.com",
    "userid": 4361
  }
}
```

### Initialization
```py
from htb_api import *
import json

htbapi = HTBAPI(configfile="config", loglevel=2)
htbapi.init()
```

### Information about active machines and challenges
```py
htbapi.machines
# machine object contains: Name, User owns, System owns, Difficulty, "solved" (0 = no user, system flag, 1 = got user flag, pwned)
htbapi.challenges
#challenge object contains: Name, Category, Solves, Difficulty, "solved" (0 = unsolved, 1 = solved)
#Difficulty is based on ratings
```
### Profile information
```py
htbapi.ownership #ownership percentage
htbapi.rank
print htbapi.profile
#{"activechallenges": 56.0, "ownedsystems": 16.0, "ownedchallenges": 35.0, "activemachines": 20.0, "ownedusers": 18.0}
```

### Ownership calculation
```
(ActiveSystemOwns + (ActiveUserOwns / 2) + (challengeOwns / 10)) / (activeMachines + (activeMachines / 2) + (totalChallenges / 10)) * 100
```
```py
htbapi.calcownership(json.dumps(htbapi.profile))
```

The htb.py example will calculate the easiest ways to reach the next HTB rank based on the difficulty of the machines and challenges

```
[+] Login Successful
[*] Parsing profile
[*] Parsing machines
[*] Parsing challenges
[+] Done with parsing challenges and machines!

----------ju256----------
- Rank: Elite Hacker
- Ownership: 80.06%

[*] Searching for different ways to reach Guru
[+] Calculated the 3 easiest ways to reach Guru


[+] Machines:  TartarSauce system, Rabbit system, Fighter user, Fulcrum user, Fighter system
[+] 2 user, 3 system, 0 challenges
[+] Difficulty: 72.0%


[+] Machines:  TartarSauce system, Rabbit system, Fighter user, Fulcrum user
[+] Challenges:  misDIRection (Misc), Senseless Behaviour (Stego), Marshal in the Middle (Forensics), Reminiscent (Forensics), BitsNBytes (Stego), Retro (Stego)
[+] 2 user, 2 system, 6 challenges
[+] Difficulty: 51.4%


[+] Machines:  TartarSauce system, Rabbit system, Fighter user
[+] Challenges:  misDIRection (Misc), Senseless Behaviour (Stego), Marshal in the Middle (Forensics), Reminiscent (Forensics), BitsNBytes (Stego), Retro (Stego), Hidden in Colors (Stego), Keep Tryin' (Forensics), Blue Shadow (Forensics), Crack This! (Reversing), Infinite Descent (Crypto)
[+] 1 user, 2 system, 11 challenges
[+] Difficulty: 50.07%
```
# The script is completely based on HTML scraping. If HTB decides to change their design the script doesn't work until it gets adjusted.
