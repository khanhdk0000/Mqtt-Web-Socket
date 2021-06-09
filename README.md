---
description: >-
  This repository establishes mqtt connection to adafruit using flask and some
  python libraries.
---

# MQTT Web Socket

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install

```
$ pip install requirements.txt
```

## Usage

```bash
. venv/bin/activate
python3 ws.py
```

## Potential problem

There might be potential bugs if there are other processes overlapping with this one, this flask server runs on **127.0.0.1** and port **5000** by default, make sure there is no other process on this address and port.

## Using real mobile phone for server

Go to Command Prompt (cmd) run `ipconfig` or Wifi setting to get Wifi address. Port number can be 80, it does not matter.

Then change the last line in **ws.py** file as below:

`app.run(host:'<address>', port:80)`

Finally, change the `host` in **constant.py** file as below:

`String host = '<address>:80';`

Note: Make sure your computer and mobile phone connect to the same wifi.



