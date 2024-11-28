import dask.bag as db
from pydub import AudioSegment
import speech_recognition as sr
import os
from transform import calcular_anio
from transform import tipo_providencia
import json

# Función para dividir el audio en segmentos
def dividir_audio_en_segmentos(ruta_audio, duracion_segmento):
    """
    Divide el archivo de audio en segmentos de duración especificada.
    """
    audio = AudioSegment.from_file(ruta_audio)
    segmentos = []
    for i in range(0, len(audio), duracion_segmento):
        segmento = audio[i:i + duracion_segmento]
        segmentos.append(segmento)
    return segmentos

# Función para transcribir cada segmento y eliminar el archivo temporal
def transcribir_segmento(segmento, indice, archivo_audio):
    """
    Transcribe un segmento de audio utilizando SpeechRecognition y elimina el archivo temporal.
    """
    recognizer = sr.Recognizer()
    ruta_temporal = f"{archivo_audio}_segmento_{indice}.wav"
    segmento.export(ruta_temporal, format="wav")
    
    # Realizar la transcripción
    try:
        with sr.AudioFile(ruta_temporal) as source:
            audio_data = recognizer.record(source)
            texto = recognizer.recognize_google(audio_data, language="es-ES")
    except sr.UnknownValueError:
        texto = "[No se pudo entender el audio]"
    except sr.RequestError as e:
        texto = f"[Error en el servicio de reconocimiento de voz: {e}]"
    finally:
        # Eliminar el archivo temporal
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
    
    return texto

# Función para transcribir un solo archivo de audio en paralelo utilizando Dask
def transcribir_audio_en_paralelo_dask(ruta_audio, duracion_segmento):
    """
    Divide un archivo de audio grande en segmentos y los transcribe en paralelo usando Dask.
    """
    # Dividir el audio en segmentos
    segmentos = dividir_audio_en_segmentos(ruta_audio, duracion_segmento)
    archivo_audio = os.path.basename(ruta_audio).split('.')[0]
    
    # Crear un Dask Bag con los segmentos y sus índices
    bag = db.from_sequence(enumerate(segmentos)).map(lambda x: transcribir_segmento(x[1], x[0], archivo_audio))
    
    # Ejecutar el procesamiento en paralelo y obtener los resultados
    resultados = bag.compute()  # Ejecuta en paralelo con Dask
    
    # Unir los resultados en un solo texto
    texto_final = " ".join(resultados)
    return texto_final

# Función para procesar todos los audios de una carpeta
def transcribir_audios_en_carpeta(carpeta, duracion_segmento):
    """
    Procesa todos los archivos de audio en la carpeta especificada.
    """
    trasncripcion = []
    
    #audios = [os.path.join(carpeta, archivo) for archivo in os.listdir(carpeta) if archivo.endswith(('.wav', '.mp3'))]
    #print(audios)

    #for ruta_audio in audios:
    nombre_archivo = os.path.basename(carpeta)

    print(f"Procesando {nombre_archivo}...")
    texto_extraido = transcribir_audio_en_paralelo_dask(carpeta, duracion_segmento)

    codigo = nombre_archivo.split('.')[0]
    anio = calcular_anio(codigo)
    tipo = tipo_providencia(codigo)

    #print(f"Transcripción de {ruta_audio}:\n{texto_extraido}\n")
    trasncripcion.append({
        "providencia" : codigo,
        "tipo": tipo,
        "texto_audio": texto_extraido,
        "anio": anio
       })
    return trasncripcion

def leer_json_a_diccionario(ruta_archivo):
    """
    Lee un archivo JSON y lo convierte en un diccionario
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")
        return None

# Uso del script
#if __name__ == '__main__':
#    carpeta_audios = "C:/Users/Usuario/Documents/Maestria/BigData/Proyecto_Final/audio/"
#    DURACION_SEGMENTO = 30_000  # Duración de cada segmento en milisegundos
#    transcribir_audios_en_carpeta(carpeta_audios, DURACION_SEGMENTO)

