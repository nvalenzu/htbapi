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

htbapi = HTBAPI(configfile="config", loglevel=2)
htbapi.init()
```

### Information about active machines and challenges
```py
print htbapi.machines
print htbapi.challenges
```
### Profile information
```py
htbapi.ownership #ownership percentage
htbapi.rank
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
