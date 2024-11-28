from flask import Flask, render_template, request
from neo4j import GraphDatabase

# Configuración de la conexión a Neo4j
uri = "neo4j+s://2ab2a2fc.databases.neo4j.io"  # Cambia esto por tu URI
user = "neo4j"
password = "N60xwacXrv3nytMqDRy--YkQHDonDOVXT_UCuzJJvhE"

# Crear instancia del controlador de Neo4j
driver = GraphDatabase.driver(uri, auth=(user, password))

# Crear aplicación Flask
app = Flask(__name__)

# Ruta principal
@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        query = request.form.get("query")  # Captura la consulta del usuario
        if query:
            results = search_neo4j(query)  # Busca en la base de datos
    return render_template("index.html", results=results)

# Función para buscar en Neo4j
def search_neo4j(similitud):
    results = []
    similitud =  int(similitud)
    cypher_query = (
        "MATCH (p:Providencia)-[s:SIMILAR_A]-(p2:Providencia) "
        "WHERE s.similitud > $similitud "
        "RETURN p, s, p2"
    )
    with driver.session() as session:
        nodes = session.run(cypher_query, similitud=similitud)
        for record in nodes:
            results.append({
                "p": record["p"],
                "s": record["s"],
                "p2": record["p2"]
            })
    return results

# Cerrar conexión al finalizar
@app.teardown_appcontext
def close_driver(exception):
    driver.close()

if __name__ == "__main__":
    app.run(debug=True)