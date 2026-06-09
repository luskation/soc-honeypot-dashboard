# 🔍 Enrichment Module

> Transformando eventos brutos do honeypot em inteligência acionável.

---

## 📖 Visão Geral

O módulo **Enrichment** tem como objetivo complementar os eventos coletados pelo honeypot com informações externas, permitindo uma análise mais rica dos atacantes, infraestrutura utilizada e possíveis indicadores de comprometimento.

Enquanto o Cowrie registra eventos como tentativas de login, execução de comandos e conexões SSH/Telnet, o enriquecimento adiciona contexto que auxilia na investigação e na geração de relatórios mais completos.

---

## 🎯 Objetivos

* Identificar a origem geográfica dos ataques.
* Avaliar a reputação de IPs maliciosos.
* Correlacionar eventos com fontes de Threat Intelligence.
* Melhorar a qualidade dos alertas enviados ao Telegram.
* Produzir dashboards mais informativos no Kibana.

---

# 🌎 GeoIP Enrichment

## MaxMind GeoLite2

O banco GeoLite2 pode ser utilizado para determinar a localização aproximada de um endereço IP observado pelo honeypot.

### Informações obtidas

| Campo     | Descrição                              |
| --------- | -------------------------------------- |
| País      | País de origem do IP                   |
| Cidade    | Cidade aproximada                      |
| ASN       | Sistema Autônomo responsável pela rede |
| Latitude  | Coordenada geográfica                  |
| Longitude | Coordenada geográfica                  |

### Exemplo

**Evento original**

```json
{
  "src_ip": "185.xxx.xxx.xxx"
}
```

**Evento enriquecido**

```json
{
  "src_ip": "185.xxx.xxx.xxx",
  "country": "Russia",
  "city": "Moscow",
  "asn": "AS12345",
  "latitude": 55.7558,
  "longitude": 37.6176
}
```

### Benefícios

* Mapa de calor dos ataques.
* Distribuição geográfica dos atacantes.
* Correlação por país ou ASN.
* Visualizações geoespaciais no Kibana.

---

# 🚨 IP Reputation

## AbuseIPDB

A integração com o AbuseIPDB permite avaliar a reputação dos IPs observados pelo honeypot.

### Informações obtidas

| Campo                  | Descrição                                 |
| ---------------------- | ----------------------------------------- |
| Abuse Confidence Score | Nível de confiança de atividade maliciosa |
| Total Reports          | Quantidade de denúncias registradas       |
| Last Reported          | Último reporte conhecido                  |
| Categories             | Categorias de abuso associadas            |
| Historical Activity    | Histórico de comportamento suspeito       |

### Exemplo

```json
{
  "src_ip": "185.xxx.xxx.xxx",
  "abuse_score": 98,
  "reports": 152,
  "last_reported": "2026-05-21"
}
```

### Benefícios

* Priorização de alertas.
* Identificação de IPs recorrentes.
* Correlação com campanhas conhecidas.
* Avaliação rápida do risco associado ao atacante.

---

# 📊 Aplicações nos Dashboards

Os dados enriquecidos podem ser utilizados para criar visualizações adicionais no Kibana.

### Possíveis Dashboards

#### 🌍 Attack Origin Map

Mapa interativo exibindo a distribuição geográfica dos ataques.

#### 🛰️ Top Attacking Countries

Países com maior volume de eventos registrados.

#### 🏢 Top ASN Attackers

Organizações e provedores mais frequentemente associados aos ataques.

#### 🚨 High Reputation Risk IPs

Lista dos IPs com maior score de abuso.

#### 📈 Abuse Score Distribution

Distribuição dos níveis de reputação observados.

---

# 🤖 Integração com Telegram

O enriquecimento pode ser utilizado para tornar os alertas mais informativos.

### Exemplo de Alerta

```text
🚨 Novo Login no Honeypot

IP: 185.xxx.xxx.xxx
Usuário: root
Senha: admin

🌍 País: Rússia
🏙 Cidade: Moscou
🏢 ASN: AS12345

🚨 Abuse Score: 98
📄 Reports: 152

🕒 Horário: 14:32 UTC
```

---

# 🚀 Melhorias Futuras

## Threat Intelligence

* Integração com feeds de IOC.
* Correlação com campanhas conhecidas.
* Verificação de IPs em listas de bloqueio.

## Malware Analysis

* Hashing automático de arquivos enviados ao honeypot.
* Integração com VirusTotal.
* Classificação de amostras.

## Command Analysis

* Identificação de comandos suspeitos.
* Agrupamento por comportamento.
* Detecção de padrões automatizados.

## Behavioral Profiling

* Classificação de atacantes por comportamento.
* Identificação de bots e scanners.
* Detecção de atividade persistente.

---

# 🛡️ Resultado Esperado

O enriquecimento transforma um simples registro de eventos em uma plataforma de observação e análise de ameaças, fornecendo contexto adicional para investigação, visualização e resposta a incidentes.

**Cowrie → Elasticsearch → Enrichment → Kibana → Telegram**

Essa abordagem aumenta significativamente o valor analítico do ambiente e aproxima o projeto de uma arquitetura utilizada em operações reais de monitoramento de segurança (SOC).
