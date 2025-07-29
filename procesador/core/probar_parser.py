from parser import procesar_txt, guardar_csv, guardar_json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
archivo_txt = os.path.join(BASE_DIR, "pruebas", "PRUEBA_20250129.txt")
csv_salida = os.path.join(BASE_DIR, "salida.csv")
json_salida = os.path.join(BASE_DIR, "salida.json")

registros = procesar_txt(archivo_txt)
guardar_csv(registros, csv_salida)
guardar_json(registros, json_salida)

print("✅ Proceso completado.")