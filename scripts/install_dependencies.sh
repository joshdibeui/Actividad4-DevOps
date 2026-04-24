#!/bin/bash
# Actualizamos el sistema e instalamos pip si no existe
sudo dnf update -y
sudo dnf install -y python3-pip
# Instalamos las librerías necesarias para el usuario ec2-user
pip3 install flask boto3 gunicorn