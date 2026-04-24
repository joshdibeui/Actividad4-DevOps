from flask import Flask, render_template, request
import json
import boto3 # Para cuando conectes DynamoDB real

app = Flask(__name__)

# Función para obtener datos (Simulada desde JSON o DynamoDB)
def obtener_datos():
    try:
        # Para DynamoDB usarías: table.scan()['Items']
        with open('estados.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/', methods=['GET'])
def index():
    todos_los_estados = obtener_datos()
    
    # Capturar parámetros de búsqueda y filtros desde la URL
    query = request.args.get('q', '').lower()
    clima_filtro = request.args.get('clima', '')
    precio_filtro = request.args.get('precio', '')

    resultados = []

    for estado in todos_los_estados:
        # Lógica de búsqueda por texto
        match_query = query in estado['Estado'].lower()
        
        # Lógica de filtro por clima
        match_clima = not clima_filtro or clima_filtro in estado['Clima']
        
        # Lógica de filtro por precio
        costo = float(estado['Costo Total'])
        match_precio = True
        if precio_filtro == 'low': match_precio = costo < 5000
        elif precio_filtro == 'mid': match_precio = 5000 <= costo <= 8000
        elif precio_filtro == 'high': match_precio = costo > 8000

        if match_query and match_clima and match_precio:
            resultados.append(estado)

    return render_template('index.html', estados=resultados, query=query)

# Ruta para ver el detalle de un estado específico
@app.route('/estado/<nombre>')
def detalle(nombre):
    todos = obtener_datos()
    estado_seleccionado = next((e for e in todos if e['Estado'] == nombre), None)
    return render_template('detalle.html', estado=estado_seleccionado)

if __name__ == '__main__':
    app.run(debug=True, port=5000)