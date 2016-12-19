P1 DSMR sensor
--------------

This script takes raw DSMR v4 as input from stdin, parses the readings and
writes them to a Firebase database. See `config.py` for the necessary
configuration.

This script runs under Python 3.5.


Manual Usage
-----

To run, invoke `cat /dev/<tty-device> | python src/p1-sensor.py` from the
command line, where `<tty-device>` is the serial device you want to read input
from. On my Raspberry Pi, this is `ttyUSB0`.

To change the default baud-rate run: `stty -F /dev/<tty-device> <baud-rate>`.
See `bash/p1-service.sh` for example usage.


Systemd installation
--------------------

The `systemd` folder contains two services that can be installed to run the
Python script on boot as a service:
 - `p1sensor.service` Enables the Python script to start at boot.
 - `p1failurelog@.service` Gets executed when the `p1sensor` fails for whatever
    reason.

Edit the paths in these scripts to point to the correct directory with bash
scripts. Then to install the services, copy both service files to
`/usr/lib/systemd/system` and run:

```
sudo systemctl enable p1sensor
```


Email error reports
-----------------------

`bash/failure-mailer.sh` can be used to email error logs from `journalctl`.
To be able to use this script, you should have `postfix` installed and
configured. Make sure you enter the correct destination email address inside the
script.
