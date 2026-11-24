import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
PREVISAO_URL = "https://api.open-meteo.com/v1/forecast"
CIDADE_PADRAO = "Porto Alegre"
DIAS_PASSADOS = 3
DIAS_FUTUROS = 3


class CidadeNaoEncontrada(Exception):
    pass


def buscar_cidade(nome):
    resp = requests.get(
        GEO_URL,
        params={"name": nome, "count": 1, "language": "pt"},
        timeout=10,
    )
    resp.raise_for_status()
    resultados = resp.json().get("results")
    if not resultados:
        raise CidadeNaoEncontrada(nome)

    c = resultados[0]
    estado = c.get("admin1", "")
    rotulo = f"{c['name']}, {estado}" if estado else c["name"]
    return {
        "rotulo": rotulo,
        "pais": c.get("country", ""),
        "latitude": c["latitude"],
        "longitude": c["longitude"],
        "timezone": c.get("timezone", "auto"),
    }


def buscar_clima(cidade):
    resp = requests.get(
        PREVISAO_URL,
        params={
            "latitude": cidade["latitude"],
            "longitude": cidade["longitude"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "timezone": cidade["timezone"],
            "past_days": DIAS_PASSADOS,
            "forecast_days": DIAS_FUTUROS + 1,
        },
        timeout=10,
    )
    resp.raise_for_status()
    diario = resp.json()["daily"]

    registros = []
    for i, data in enumerate(diario["time"]):
        if i < DIAS_PASSADOS:
            tipo = "passado"
        elif i == DIAS_PASSADOS:
            tipo = "hoje"
        else:
            tipo = "futuro"
        registros.append(
            {
                "data": data,
                "temp_max": diario["temperature_2m_max"][i],
                "temp_min": diario["temperature_2m_min"][i],
                "chuva_mm": diario["precipitation_sum"][i],
                "vento_max": diario["wind_speed_10m_max"][i],
                "tipo": tipo,
            }
        )
    return registros
