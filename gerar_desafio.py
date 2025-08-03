import fastapi_poe as fp
import asyncio
import time
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# Configurações (usando variáveis de ambiente)
EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
REMETENTE = os.getenv("REMETENTE")
API_KEY = os.getenv("POE_API_KEY")
BOT_NAME = os.getenv("BOT_NAME", "botsupremooo")  # valor padrão se não definir

HISTORICO_PATH = "historico.json"

# Utilitários de histórico
def carregar_historico():
    try:
        with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_historico(historico):
    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

# Geração de texto com IA (POE)
async def gerar_texto_ia_async(prompt, historico=None):
    if historico is None:
        historico = []

    historico.append({"role": "user", "content": prompt})

    resposta = ""
    try:
        async for partial in fp.get_bot_response(
            messages=[fp.ProtocolMessage(role=m["role"], content=m["content"]) for m in historico],
            bot_name=BOT_NAME,
            api_key=API_KEY,
        ):
            if hasattr(partial, "text"):
                resposta += partial.text
            elif hasattr(partial, "content"):
                resposta += partial.content
            else:
                resposta += str(partial)
    except Exception as e:
        print("Erro na chamada da API:", e)
        return ""

    historico.append({"role": "bot", "content": resposta})

    if len(historico) > 10:
        historico = historico[-10:]

    salvar_historico(historico)
    return resposta.strip()

# Utilitários de arquivo
def ler_desafio_anterior():
    try:
        with open("desafio_anterior.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Nenhum."

# Geração de prompts
def gerar_prompt_desafio(desafio_anterior):
    return f"""
Você é um especialista sênior em T-SQL com foco em performance e arquitetura de banco de dados.

Seu papel é criar **um desafio prático e avançado** que ajude o aluno a desenvolver as seguintes habilidades:

1. Criação de *views* altamente performáticas, evitando funções escalares, usando `WITH (NOLOCK)` quando apropriado, otimizando `JOINs`, usando `CTEs`, e filtrando corretamente com `WHERE`.
2. Escrita de *stored procedures* bem estruturadas, com:
   - Parâmetros de entrada e saída;
   - Boas práticas de nomenclatura;
   - Tratamento de erros com `TRY...CATCH`;
   - Comentários e modularização.
3. Leitura e interpretação de plano de execução (dê dicas e armadilhas comuns).
4. Uso de `INNER JOIN`, `LEFT JOIN`, `EXISTS`, `NOT EXISTS`, e boas práticas em filtros e subconsultas.

**Regras para o desafio:**
- Baseie-se no desafio anterior, se houver.
- Crie tabelas e dados de exemplo.
- Explique o desafio de forma didática.
- Dê dicas, possíveis erros e links úteis de estudo.
- **Não entregue a solução!**

Desafio anterior: {desafio_anterior}
"""

def gerar_prompt_resolucao(desafio_atual):
    return f"""
Você é um tutor experiente em T-SQL Avançado.

Agora, entregue a solução detalhada do seguinte desafio, explicando passo a passo, com código exemplo e raciocínio claro.

Desafio: {desafio_atual}
"""

# Envio de e-mail com HTML formatado
def enviar_email(conteudo, assunto):
    msg = MIMEMultipart("alternative")
    msg["From"] = REMETENTE
    msg["To"] = EMAIL
    msg["Subject"] = assunto

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #c7342e;">{assunto}</h2>
            <p>Abaixo está o conteúdo do desafio com o SQL destacado:</p>
            <div style="background: #272822; color: #f8f8f2; padding: 15px; border-radius: 8px; font-family: Consolas, monospace; font-size: 14px; overflow-x: auto; white-space: pre;">
                {conteudo.replace("<", "&lt;").replace(">", "&gt;")}
            </div>
            <p>Copie e cole no seu ambiente SQL para praticar.<br>
            Enviado por seu tutor T-SQL automatizado.</p>
        </body>
    </html>
    """

    corpo_html = MIMEText(html_content, "html", "utf-8")
    msg.attach(corpo_html)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(REMETENTE, APP_PASSWORD)
            server.sendmail(REMETENTE, EMAIL.split(","), msg.as_string())
        print(f"📧 Email enviado: {assunto}")
    except Exception as e:
        print("Erro ao enviar email:", e)

# Geração e envio de desafio
def salvar_e_enviar_desafio():
    desafio_anterior = ler_desafio_anterior()
    prompt_desafio = gerar_prompt_desafio(desafio_anterior)
    historico = carregar_historico()

    desafio_atual = asyncio.run(gerar_texto_ia_async(prompt_desafio, historico))

    with open("desafio_tsql.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n{desafio_atual}\n{'='*50}\n")

    with open("desafio_anterior.txt", "w", encoding="utf-8") as f:
        f.write(desafio_atual)

    enviar_email(desafio_atual, "📬 Seu Desafio T-SQL do Dia - Aprenda e Pratique!")

    prompt_resolucao = gerar_prompt_resolucao(desafio_atual)
    resolucao = asyncio.run(gerar_texto_ia_async(prompt_resolucao, carregar_historico()))

    with open("resolucao_tsql.txt", "w", encoding="utf-8") as f:
        f.write(resolucao)

# Envio da resolução posteriormente
def enviar_resolucao():
    try:
        with open("resolucao_tsql.txt", "r", encoding="utf-8") as f:
            resolucao = f.read()
        enviar_email(resolucao, "📩 Só abra se já tentou resolver o desafio!")
    except FileNotFoundError:
        print("Arquivo de resolução não encontrado.")

# Execução direta
salvar_e_enviar_desafio()
enviar_resolucao()
