import os
import csv
import json


# Columnas definidas por el PDF
COLUMNS_DB = [
    'tipo_documento', 'documento', 'nombre', 'producto', 'poliza', 'periodo', 'valor_asegurado',
    'valor_prima', 'doc_cobro', 'fecha_ini', 'fecha_fin', 'dias', 'telefono_1', 'telefono_2',
    'telefono_3', 'ciudad', 'departamento', 'fecha_venta', 'fecha_nacimiento', 'tipo_trans',
    'beneficiarios', 'genero', 'sucursal', 'tipo_cuenta', 'ultimos_digitos_cuenta',
    'entidad_bancaria', 'nombre_banco', 'estado_debito', 'causal_rechazo', 'codigo_canal',
    'descripcion_canal', 'codigo_estrategia', 'tipo_estrategia', 'correo_electronico',
    'fecha_entrega_colmena', 'mes_a_trabajar', 'id', 'nombre_db', 'telefono', 'whatsapp',
    'texto', 'email', 'fisica', 'mejor_canal', 'contactar_al'
]

# Intervalos exactos del PDF
INTERVALOS = [
    (0, 10), (10, 13), (13, 28), (28, 128), (128, 143), (143, 165), (165, 187),
    (187, 201), (201, 221), (221, 226), (226, 241), (241, 256), (256, 271), (271, 321),
    (321, 371), (371, 494), (494, 548), (548, 568), (568, 575), (575, 615),
    (615, 625), (625, 1615)
]

def cortar_campos(linea):
    return [linea[ini:fin].strip() for ini, fin in INTERVALOS]

def mejor_canal_y_contacto(campos_dict):
    canales = {
        'texto': campos_dict['texto'] == '1',
        'email': campos_dict['email'] == '1',
        'telefono': campos_dict['telefono'] == '1',
        'whatsapp': campos_dict['whatsapp'] == '1',
        'fisica': campos_dict['fisica'] == '1'
    }

    prioridad = ['texto', 'email', 'telefono', 'whatsapp', 'fisica']
    mejor = next((canal for canal in prioridad if canales.get(canal)), '')

    contacto = ''
    if mejor in ['texto', 'telefono', 'whatsapp']:
        contacto = (
            campos_dict.get('telefono_1') or
            campos_dict.get('telefono_2') or
            campos_dict.get('telefono_3') or
            campos_dict.get('correo_electronico', '')
        )
        if not contacto:
            mejor = 'email'
            contacto = campos_dict.get('correo_electronico', '')
    elif mejor == 'email':
        contacto = campos_dict.get('correo_electronico', '')

    return mejor, contacto

def procesar_txt(path_txt):
    nombre_archivo = os.path.basename(path_txt)
    registros = []

    # Leer todo el contenido como una cadena
    with open(path_txt, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Dividir en bloques de 1615 caracteres
    lineas = [contenido[i:i+1615] for i in range(0, len(contenido), 1615)]

    for idx, linea in enumerate(lineas):
        if len(linea) < 1615:
            print(f"⚠️ Línea {idx+1} muy corta ({len(linea)}). Saltando...")
            continue

        campos = cortar_campos(linea)
        if len(campos) != len(INTERVALOS):
            print(f"⚠️ Línea {idx+1} inválida (se esperaban {len(INTERVALOS)} campos). Saltando...")
            continue

        campos_dict = {
            'tipo_documento': campos[1],
            'documento': campos[2],
            'nombre': campos[3],
            'producto': campos[4][:5],
            'poliza': campos[4][5:],
            'periodo': campos[5][:1],
            'valor_asegurado': campos[5][1:],
            'valor_prima': campos[6],
            'doc_cobro': campos[7],
            'fecha_ini': campos[8],
            'fecha_fin': '',
            'dias': campos[9],
            'telefono_1': campos[10],
            'telefono_2': campos[11],
            'telefono_3': campos[12],
            'ciudad': campos[13],
            'departamento': campos[14],
            'fecha_venta': campos[15][:10],
            'fecha_nacimiento': campos[15][10:20],
            'tipo_trans': campos[15][20:23],
            'beneficiarios': campos[15][23:],
            'genero': campos[16][:1],
            'sucursal': campos[16][1:],
            'tipo_cuenta': '',
            'ultimos_digitos_cuenta': campos[17],
            'entidad_bancaria': campos[18],
            'nombre_banco': campos[19],
            'estado_debito': campos[20],
            'causal_rechazo': campos[21],
            'codigo_canal': '',
            'descripcion_canal': '',
            'codigo_estrategia': '',
            'tipo_estrategia': '',
            'correo_electronico': '',
            'fecha_entrega_colmena': '',
            'mes_a_trabajar': '',
            'id': '',
            'nombre_db': nombre_archivo,
            'telefono': '',
            'whatsapp': '',
            'texto': '',
            'email': '',
            'fisica': '',
            'mejor_canal': '',
            'contactar_al': ''
        }

        mejor, contacto = mejor_canal_y_contacto(campos_dict)
        campos_dict['mejor_canal'] = mejor
        campos_dict['contactar_al'] = contacto

        registros.append(campos_dict)

    print(f"✅ Total de líneas procesadas correctamente: {len(registros)}")
    return registros

def guardar_csv(registros, ruta_destino):
    with open(ruta_destino, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS_DB)
        writer.writeheader()
        writer.writerows(registros)

def guardar_json(registros, ruta_destino):
    with open(ruta_destino, 'w', encoding='utf-8') as f:
        json.dump(registros, f, ensure_ascii=False, indent=4)
