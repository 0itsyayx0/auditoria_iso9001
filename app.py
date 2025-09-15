from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

items_iso = [
    "4.1 Contexto de la organización",
    "4.2 Partes interesadas",
    "4.3 Alcance del SGC",
    "4.4 Procesos del sistema",
    "5.1 Liderazgo",
    "5.2 Política de calidad",
    "5.3 Roles y responsabilidades",
    "6.1 Riesgos y oportunidades",
    "6.2 Objetivos de calidad",
    "7.1 Recursos",
    "7.2 Competencia",
    "7.3 Conciencia",
    "7.4 Comunicación",
    "7.5 Información documentada",
    "8.1 Control operacional",
    "8.2 Requisitos de productos",
    "8.3 Diseño y desarrollo",
    "8.4 Proveedores externos",
    "8.5 Producción",
    "8.6 Liberación de productos",
    "8.7 No conformidades",
    "9.1 Seguimiento y evaluación",
    "9.2 Auditoría interna",
    "9.3 Revisión por la dirección",
    "10.1 Mejora continua",
    "10.2 Acciones correctivas"
]

def init_db():
    conn = sqlite3.connect('auditoria.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            item TEXT,
            cumple INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html', items=items_iso)

@app.route('/evaluar', methods=['POST'])
def evaluar():
    datos = request.json
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('auditoria.db')
    c = conn.cursor()

    resultados = []
    for item, cumple in datos.items():
        c.execute('INSERT INTO resultados (fecha, item, cumple) VALUES (?, ?, ?)', (fecha, item, int(cumple)))
        resultados.append({
            "item": item,
            "cumple": cumple
        })

    conn.commit()
    conn.close()
    return jsonify(resultados)

@app.route('/historial')
def historial():
    conn = sqlite3.connect('auditoria.db')
    c = conn.cursor()
    c.execute('SELECT fecha, item, cumple FROM resultados ORDER BY fecha DESC')
    datos = c.fetchall()
    conn.close()
    return render_template('historial.html', datos=datos)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render asigna PORT dinámico
    app.run(host='0.0.0.0', port=port, debug=True)
