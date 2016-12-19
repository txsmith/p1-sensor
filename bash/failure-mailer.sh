#!/bin/bash

cat << EOF | mail -s "P1 Sensor error report" <dest-email-address>
Hello,

This is an error-report from your P1-sensor.

$(journalctl -u p1sensor --no-pager --since "15 minutes ago")

EOF
