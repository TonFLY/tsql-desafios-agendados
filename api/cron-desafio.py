import json
import os
import asyncio
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import BaseHTTPRequestHandler
import fastapi_poe as fp

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Executar a geração e envio do desafio
            result = asyncio.run(executar_desafio())
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "success",
                "message": "Desafio gerado e enviado com sucesso!",
                "timestamp": datetime.now().isoformat(),
                "result": result
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error_response = {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))

# Configurações usando variáveis de ambiente da Vercel
EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
REMETENTE = os.getenv("REMETENTE")
API_KEY = os.getenv("POE_API_KEY")
BOT_NAME = os.getenv("BOT_NAME", "botsupremooo")

# Armazenamento simples em memória (para Vercel)
historico_memoria = []

async def gerar_texto_ia_async(prompt, historico=None):
    global historico_memoria
    
    if historico is None:
        historico = historico_memoria
    
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
    
    # Manter apenas os últimos 6 elementos para não sobrecarregar
    if len(historico) > 6:
        historico = historico[-6:]
    
    historico_memoria = historico
    return resposta.strip()

def gerar_prompt_desafio():
    return """
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
- Crie tabelas e dados de exemplo.
- Explique o desafio de forma didática.
- Dê dicas, possíveis erros e links úteis de estudo.
- **Não entregue a solução!**
- Seja criativo e varie os tipos de desafio.
"""

def gerar_prompt_resolucao(desafio_atual):
    return f"""
Você é um tutor experiente em T-SQL Avançado.

Agora, entregue a solução detalhada do seguinte desafio, explicando passo a passo, com código exemplo e raciocínio claro.

Desafio: {desafio_atual}
"""

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
            Enviado automaticamente via Vercel Cron Job 🚀</p>
        </body>
    </html>
    """

    corpo_html = MIMEText(html_content, "html", "utf-8")
    msg.attach(corpo_html)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(REMETENTE, APP_PASSWORD)
            server.sendmail(REMETENTE, EMAIL.split(","), msg.as_string())
        return f"📧 Email enviado: {assunto}"
    except Exception as e:
        raise Exception(f"Erro ao enviar email: {e}")

async def executar_desafio():
    try:
        # Gerar desafio
        prompt_desafio = gerar_prompt_desafio()
        desafio_atual = await gerar_texto_ia_async(prompt_desafio)
        
        if not desafio_atual:
            return {"error": "Falha ao gerar desafio"}
        
        # Enviar desafio
        resultado_desafio = enviar_email(desafio_atual, "📬 Seu Desafio T-SQL do Dia - Aprenda e Pratique!")
        
        # Gerar resolução
        prompt_resolucao = gerar_prompt_resolucao(desafio_atual)
        resolucao = await gerar_texto_ia_async(prompt_resolucao)
        
        # Enviar resolução
        resultado_resolucao = enviar_email(resolucao, "📩 Resolução do Desafio T-SQL")
        
        return {
            "desafio_enviado": resultado_desafio,
            "resolucao_enviada": resultado_resolucao,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise Exception(f"Erro na execução: {str(e)}")
