from flask import Flask, render_template, request
import boto3
from boto3.dynamodb.conditions import Attr
import decimal

app = Flask(__name__)

# Configuración de DynamoDB
# Si estás en EC2 con un IAM Role, no necesitas credenciales aquí.
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # Ajusta tu región
tabla = dynamodb.Table('Tabla-Estados')

# Helper para manejar números de DynamoDB (Decimal)
def handle_decimal(obj):
    if isinstance(obj, list):
        return [handle_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: handle_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    return obj

def obtener_datos_dynamo():
    try:
        response = tabla.scan()
        items = response.get('Items', [])
        return handle_decimal(items)
    except Exception as e:
        print(f"Error al conectar con DynamoDB: {e}")
        return []

@app.route('/', methods=['GET'])
def index():
    query = request.args.get('q', '').lower()
    clima_filtro = request.args.get('clima', '')
    precio_filtro = request.args.get('precio', '')

    todos_los_estados = obtener_datos_dynamo()
    resultados = []

    for estado in todos_los_estados:
        # 1. Filtro de búsqueda por nombre
        match_query = query in estado.get('Estado', '').lower()
        
        # 2. Filtro de clima
        match_clima = not clima_filtro or clima_filtro in estado.get('Clima', '')
        
        # 3. Filtro de presupuesto
        # Asegúrate que en DynamoDB el costo sea un número o string convertible
        costo = float(estado.get('Costo Total', 0))
        match_precio = True
        if precio_filtro == 'low': match_precio = costo < 5000
        elif precio_filtro == 'mid': match_precio = 5000 <= costo <= 8000
        elif precio_filtro == 'high': match_precio = costo > 8000

        if match_query and match_clima and match_precio:
            resultados.append(estado)

    return render_template('index.html', estados=resultados, query=query)

@app.route('/estado/<nombre>')
def detalle(nombre):
    # En lugar de scan, aquí usamos get_item para eficiencia (Búsqueda por Key)
    try:
        response = tabla.get_item(Key={'Estado': nombre})
        estado = handle_decimal(response.get('Item'))
        return render_template('detalle.html', estado=estado)
    except Exception as e:
        print(e)
        return "Estado no encontrado", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)