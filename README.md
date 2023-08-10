# pkp-ticket-exchange
Bot for automatically submitting pukkelpop form when new tickets become available
## usage
First change the constants at the top in exchange_bot.py:
- which tickets you want
- what contact details you want to use
- what the timeouts are when checking for new tickets

then run this to install and run it in a virtualenvironment
``` bash
virtualenv venv -p python3
source ./venv/bin/activate
python exchange_bot.py
```
