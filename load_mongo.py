from pymongo import MongoClient

def inserta_mongo_db(conexion, db_mongo, collection_mongo,documento):
    print("Conectado a Mongo DB...")
    try:
        # Conexión a MongoDB Atlas
        client = MongoClient(conexion)
        # Selección de la base de datos
        db = client[db_mongo]  # Asegúrate de que este nombre sea correcto
        print(f"Tipo de db: {type(db)}")  # Agregado para verificar el tipo de 'db'

        # Selección de la colección
        collection = db[collection_mongo]  # Asegúrate de que este nombre sea correcto

        # Inserción del documento en la colección
        resultado = collection.insert_many(documento)
        print(f"Documento insertado: {resultado}")

    except Exception as e:
        print("Error al conectar o insertar en MongoDB:", e)

    finally:
        # Cierre de la conexión
        client.close()
