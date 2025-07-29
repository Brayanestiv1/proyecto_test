import os
from django.http import JsonResponse
from core.parser import procesar_txt, guardar_csv, guardar_json
from core.utils import insertar_registros

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def procesar_archivo(request):
    if request.method != "POST":
        return JsonResponse({"error": "Solo se permite método POST."}, status=405)

    try:
        data = json.loads(request.body)
        nombre_archivo = data.get("archivo")

        if not nombre_archivo:
            return JsonResponse({"error": "Falta el campo 'archivo'."}, status=400)

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path_txt = os.path.join(base_dir, "pruebas", nombre_archivo)
        path_csv = os.path.join(base_dir, "salida.csv")
        path_json = os.path.join(base_dir, "salida.json")

        registros = procesar_txt(path_txt)
        guardar_csv(registros, path_csv)
        guardar_json(registros, path_json)
        insertados = insertar_registros(registros)

        return JsonResponse({
            "archivo": nombre_archivo,
            "csv": "salida.csv",
            "json": "salida.json",
            "registros_procesados": len(registros),
            "registros_insertados": insertados,
            "estado": "OK"
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
