
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse, Response
 
import clima
import dados
import graficos
 
app = FastAPI(
    title="API de Clima",
    description="Dados meteorológicos dos últimos 3 dias, de hoje e dos próximos 3 dias. Padrão: Porto Alegre.",
)
dados.iniciar_banco()
 
 
def atualizar(nome):
    try:
        cidade = clima.buscar_cidade(nome)
        registros = clima.buscar_clima(cidade)
    except clima.CidadeNaoEncontrada:
        raise HTTPException(404, f"Cidade '{nome}' não encontrada")
    except requests.RequestException:
        raise HTTPException(502, "Falha ao consultar o serviço de clima")
    dados.salvar(cidade["rotulo"], registros)
    return cidade, registros
 
 
@app.get("/", include_in_schema=False)
def inicio():
    return RedirectResponse("/docs")
 
 
@app.get("/api/clima", summary="Dados do clima (JSON)")
def api_clima(cidade: str = Query(clima.CIDADE_PADRAO, description="Nome da cidade")):
    info, registros = atualizar(cidade)
    return {"cidade": info["rotulo"], "pais": info["pais"], "dias": registros}
 
 
@app.get(
    "/api/grafico",
    summary="Gráfico do clima (PNG)",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}}},
)
def api_grafico(cidade: str = Query(clima.CIDADE_PADRAO, description="Nome da cidade")):
    info, _ = atualizar(cidade)
    registros = dados.listar(info["rotulo"])
    return Response(graficos.gerar_grafico(info["rotulo"], registros), media_type="image/png")
 