#!/bin/bash
# Entramos al directorio donde CodeDeploy dejó los archivos
cd /home/ec2-user/proyecto-viajes

# Detenemos cualquier proceso previo de la app para liberar el puerto 5000
pkill gunicorn || true

# Iniciamos Gunicorn. 
# -w 4: 4 workers para mayor eficiencia
# -b: vincula al puerto 5000
# -D: corre como demonio (background)
gunicorn -w 4 -b 0.0.0.0:5000 app:app -D