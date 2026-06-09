from elasticsearch import Elasticsearch
from collections import defaultdict
from dotenv import load_dotenv
import requests
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

es = Elasticsearch("http://localhost:9200")


def enviar_telegram(mensagem):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML"
    }

    resposta = requests.post(
        url,
        json=payload,
        timeout=10
    )

    print("Status:", resposta.status_code)

    return resposta.status_code == 200

def gerar_relatorio():

    total_eventos = es.count(
        index=".ds-filebeat-*",
        query={
            "range": {
                "@timestamp": {
                    "gte": "now-12h"
                }
            }
        }
    )["count"]

    unique_attackers = es.search(
        index=".ds-filebeat-*",
        size=0,
        aggs={
            "unique_ips": {
                "cardinality": {
                    "field": "src_ip"
                }
            }
        }
    )

    atacantes_unicos = (
        unique_attackers["aggregations"]
        ["unique_ips"]["value"]
    )

    eventos = es.search(
        index=".ds-filebeat-*",
        size=1000,
        query={
            "range": {
                "@timestamp": {
                    "gte": "now-12h"
                }
            }
        }
    )

    credenciais = {}
    ips = {}
    usuarios = {}
    distribuicao_eventos = {}
    timeline = defaultdict(int)

    for hit in eventos["hits"]["hits"]:

        doc = hit["_source"]

        eventid = doc.get(
            "eventid",
            "desconhecido"
        )

        distribuicao_eventos[eventid] = (
            distribuicao_eventos.get(eventid, 0) + 1
        )

        timestamp = doc.get("@timestamp", "")

        if len(timestamp) >= 13:
            hora = timestamp[11:13]
            timeline[hora] += 1

        if eventid == "cowrie.login.success":

            ip = doc.get(
                "src_ip",
                "desconhecido"
            )

            usuario = doc.get(
                "username",
                "desconhecido"
            )

            senha = doc.get(
                "password",
                ""
            )

            ips[ip] = ips.get(ip, 0) + 1

            usuarios[usuario] = (
                usuarios.get(usuario, 0) + 1
            )

            cred = f"{usuario}/{senha}"

            credenciais[cred] = (
                credenciais.get(cred, 0) + 1
            )

    top_ips = sorted(
        ips.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    top_creds = sorted(
        credenciais.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    top_users = sorted(
        usuarios.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    top_eventos = sorted(
        distribuicao_eventos.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    hora_pico = None
    eventos_pico = 0

    for hora, qtd in timeline.items():

        if qtd > eventos_pico:

            eventos_pico = qtd
            hora_pico = hora

    relatorio = []

    relatorio.append("<b>🛡️ RELATÓRIO COWRIE - ÚLTIMAS 12H</b>\n")

    relatorio.append(
        f"📊 <b>Eventos Totais:</b> {total_eventos}"
    )

    relatorio.append(
        f"👤 <b>Atacantes Únicos:</b> {atacantes_unicos}\n"
    )

    relatorio.append("📡 <b>Top IPs</b>")

    for ip, qtd in top_ips:
        relatorio.append(
            f"• <code>{ip}</code> → {qtd}"
        )

    relatorio.append("\n🔑 <b>Top Credenciais</b>")

    for cred, qtd in top_creds:
        relatorio.append(
            f"• <code>{cred}</code> → {qtd}"
        )

    relatorio.append("\n👤 <b>Logins por Usuário</b>")

    for usuario, qtd in top_users:
        relatorio.append(
            f"• <code>{usuario}</code> → {qtd}"
        )

    relatorio.append("\n📊 <b>Distribuição de Eventos</b>")

    for evento, qtd in top_eventos:
        relatorio.append(
            f"• <code>{evento}</code> → {qtd}"
        )

    relatorio.append("\n🔥 <b>Horário de Pico</b>")

    if hora_pico:
        relatorio.append(
            f"• {hora_pico}:00 - {hora_pico}:59 → {eventos_pico} eventos"
        )

    return "\n".join(relatorio)


if __name__ == "__main__":

    relatorio = gerar_relatorio()

    print(relatorio)

    if enviar_telegram(relatorio):
        print("\nRelatório enviado.")
    else:
        print("\nFalha ao enviar relatório.")