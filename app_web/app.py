from flask import Flask, render_template, request
from pymongo import MongoClient
from neo4j import GraphDatabase

app = Flask(__name__)

# Configuración de conexión a MongoDB
client = MongoClient("mongodb+srv://usr_edwin:eanieto93@bigdata2024.7s5ee.mongodb.net/?retryWrites=true&w=majority&appName=BigData2024")
db = client['BigData2024']
collection = db['RelatoriaAudios']


# Configuración de la conexión a Neo4j
uri = "neo4j+s://2ab2a2fc.databases.neo4j.io"  # Cambia esto por tu URI
user = "neo4j"
password = "N60xwacXrv3nytMqDRy--YkQHDonDOVXT_UCuzJJvhE"
driver = GraphDatabase.driver(uri, auth=(user, password))

# Función para ejecutar la consulta en Neo4j
def get_neo4j_data(providencia):
    query = """
    MATCH (p:Providencia)-[s:SIMILAR_A]-(p2:Providencia)
    WHERE p.codigo = $providencia or p2.codigo = $providencia 
    RETURN s
    """
    with driver.session() as session:
        result = session.run(query, providencia=providencia)
        return result.data()  # Devuelve los resultados de la consulta



@app.route('/', methods=['GET', 'POST'])
##@app.route('/')
def search():
    results = []
    per_page = 10  # Número de resultados por página
    page = int(request.args.get('page', 1))  # Página actual, por defecto es 1

    if request.method == 'POST':
        query = {}
        field1 = request.form.get('providencia', '').strip()
        field2 = request.form.get('tipo', '').strip()
        field3 = request.form.get('anio', '').strip()
        field4 = request.form.get('texto_audio', '').strip()

        if field1:
            query['providencia'] = {'$regex': field1, '$options': 'i'}
        if field2:
            query['tipo'] = {'$regex': field2, '$options': 'i'}
        if field3:
            try:
                query['anio'] = int(field3)
            except ValueError:
                pass
        if field4:
            query['texto_audio'] = {'$regex': field4, '$options': 'i'}

        # Calcular resultados con paginación
        total_results = collection.count_documents(query)  # Total de documentos que cumplen el filtro
        total_pages = (total_results + per_page - 1) // per_page  # Redondear hacia arriba

        # Obtener solo los resultados de la página actual
        results = list(
            collection.find(query)
            .skip((page - 1) * per_page)
            .limit(per_page)
        )
    else:
        total_pages = 0
        total_results = 0

    return render_template(
        'search.html',
        results=results,
        page=page,
        total_pages=total_pages,
        total_results=total_results,
    )

@app.route('/providencia/<providencia>', methods=['GET'])
def providencia_detail(providencia):
    # Realiza la consulta a Neo4j usando el valor de providencia
    neo4j_results = get_neo4j_data(providencia)
    
    return render_template('providencia_detail.html', providencia=providencia, results=neo4j_results)



if __name__ == '__main__':
    app.run(debug=True)
