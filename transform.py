
def calcular_anio(codigo):
    # Extraer los últimos dos caracteres de la cadena
    anio_corto = codigo.split('-')[-1]
    
    # Convertir los dos últimos dígitos a un entero
    anio_corto = int(anio_corto)
    anio_completo = 2000 + anio_corto
    
    return anio_completo


def tipo_providencia(filename):
    if filename.startswith('A'):
        return "Auto"
    elif filename.startswith('T'):
        return "Tutela"
    elif filename.startswith('C'):
        return "Constitucionalidad"
    else:
        return "Providencia no encontrada"