#!/bin/bash
cd /home/ec2-user/proyecto-viajes
# Mata procesos anteriores de gunicorn y arranca el nuevo
pkill gunicorn
gunicorn --bind 0.0.0.0:5000 app:app -D