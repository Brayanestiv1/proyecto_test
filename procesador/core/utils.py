from core.models import Registro

def insertar_registros(registros):
    nuevos = []
    for reg in registros:
        # Evita conflicto si el campo ID es primary key
        if not reg.get("id"):
            reg["id"] = f"{reg['documento']}_{reg['poliza']}"

        nuevos.append(Registro(**reg))

    Registro.objects.bulk_create(nuevos, ignore_conflicts=True)
    return len(nuevos)