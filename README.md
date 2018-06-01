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
