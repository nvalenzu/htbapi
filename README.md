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

## Initialization
```
from htb_api import *

htbapi = HTBAPI(configfile="config", loglevel=2)
htbapi.init()
```

## Information about active machines and challenges
