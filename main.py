from read_audio_dask import transcribir_audios_en_carpeta
from load_mongo import inserta_mongo_db
from transform import calcular_anio
from read_audio_dask import leer_json_a_diccionario


##Parametros de inicio
carpeta_audios = "C:/Users/Usuario/Documents/Maestria/BigData/Proyecto_Final/audio/"
DURACION_SEGMENTO = 30_000
CLIENTE_MONGODB = "mongodb+srv://usr_edwin:eanieto93@bigdata2024.7s5ee.mongodb.net/?retryWrites=true&w=majority&appName=BigData2024"
DB_MONGO = "BigData2024"
COLLECTION_MONGO = "RelatoriaAudios"
RUTA_SIMILITUD = "C:/Users/Usuario/Documents/Maestria/BigData/Proyecto_Final/similitud/Similitud.json"


def main():
    print("Inicio de programa:\n")
    
    #dic_audios = transcribir_audios_en_carpeta(carpeta_audios,DURACION_SEGMENTO)
    #inserta_mongo_db(CLIENTE_MONGODB,DB_MONGO,COLLECTION_MONGO,dic_audios)
    opcion = input("Desea cargar la base de similitud? Y/N")

    if opcion == 'Y':
        print("Cargando en Neo4J...")
        datos_similitud = leer_json_a_diccionario(RUTA_SIMILITUD)
        inserta_mongo_db(CLIENTE_MONGODB,DB_MONGO,'Similitud',datos_similitud)
    elif opcion == 'N':
        print("Fin de la ejecucion...!")
    else:
        print("Opcion no valida...por favor digite N o Y.")


if __name__ == "__main__":
    main()