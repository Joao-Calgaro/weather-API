# API de Clima

Salva e exibe dados meteorológicos (3 dias passados, hoje e 3 dias futuros) de qualquer cidade. Default: Porto Alegre.
Dados via [Open-Meteo](https://open-meteo.com).

## Como rodar

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Abra http://localhost:8000

## Rotas

| Rota | Descrição |
|------|-----------|
| `GET /api/clima?cidade=Curitiba` | JSON com os 7 dias (e salva no banco) |
| `GET /api/grafico?cidade=Curitiba` | Gráfico em PNG |

Sem o parâmetro `cidade`, usa Porto Alegre. Clique em **Try it out**, edite a cidade e **Execute**.

## Arquivos

- `clima.py` – chamadas API 
- `dados.py` – persistência em SQLite (`clima.db`)
- `graficos.py` – gráfico com matplotlib
- `main.py` – rotas FastAPI
