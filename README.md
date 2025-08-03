# 📚 T-SQL Desafios Agendados

Um sistema automatizado para gerar e enviar desafios de T-SQL personalizados via email, usando IA para criar exercícios práticos e avançados que ajudam no desenvolvimento de habilidades em banco de dados SQL Server.

## 🎯 Funcionalidades

- **Geração automática de desafios**: Cria exercícios práticos de T-SQL usando IA (POE API)
- **Envio por email**: Envia desafios formatados em HTML diretamente para seu email
- **Resolução posterior**: Gera e envia a solução do desafio após um tempo determinado
- **Histórico inteligente**: Mantém contexto dos desafios anteriores para progressão gradual
- **Foco em performance**: Exercícios focados em otimização, views, stored procedures e análise de plano de execução

## 🚀 Como Funciona

O sistema trabalha em duas etapas:

1. **Geração do Desafio**: 
   - Analisa o desafio anterior (se houver)
   - Gera um novo desafio focado em T-SQL avançado
   - Envia por email com formatação HTML
   - Salva o histórico para contexto futuro

2. **Envio da Resolução**:
   - Gera a solução detalhada do desafio
   - Envia em email separado para não "entregar" a resposta imediatamente

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **fastapi-poe**: Integração com IA para geração de conteúdo
- **smtplib**: Envio de emails
- **JSON**: Armazenamento de histórico
- **HTML/CSS**: Formatação dos emails

## ⚙️ Configuração

### 1. Pré-requisitos

```bash
pip install -r requirements.txt
```

### 2. Variáveis de Ambiente

Configure as seguintes variáveis de ambiente:

```bash
# Email de destino (onde receberá os desafios)
EMAIL=seu-email@gmail.com

# Senha de aplicativo do Gmail (não sua senha normal)
APP_PASSWORD=sua-senha-de-aplicativo

# Email remetente (pode ser o mesmo do EMAIL)
REMETENTE=seu-email@gmail.com

# Chave da API do POE
POE_API_KEY=sua-chave-poe-api

# Nome do bot no POE (opcional, padrão: "botsupremooo")
BOT_NAME=seu-bot-preferido
```

### 3. Configuração do Gmail

Para usar o Gmail como remetente:

1. Habilite a **verificação em duas etapas** na sua conta Google
2. Gere uma **senha de aplicativo** específica para este projeto
3. Use esta senha de aplicativo na variável `APP_PASSWORD`

### 4. Configuração da POE API

1. Acesse [poe.com](https://poe.com)
2. Obtenha sua chave de API
3. Configure na variável `POE_API_KEY`

## 🏃‍♂️ Como Usar

### Execução Manual

```bash
python gerar_desafio.py
```

### Agendamento Automático

Para receber desafios diariamente, você pode usar:

**Windows (Task Scheduler)**:
1. Abra o Agendador de Tarefas
2. Crie uma nova tarefa
3. Configure para executar `python gerar_desafio.py` no horário desejado

**Linux/Mac (Crontab)**:
```bash
# Adicionar ao crontab para execução diária às 8h
0 8 * * * /usr/bin/python3 /caminho/para/gerar_desafio.py
```

## 📋 Estrutura dos Desafios

Os desafios são focados em:

### 🎯 Habilidades Desenvolvidas

1. **Views Performáticas**
   - Evitar funções escalares
   - Uso apropriado de `WITH (NOLOCK)`
   - Otimização de `JOINs`
   - Implementação de `CTEs`
   - Filtragem eficiente com `WHERE`

2. **Stored Procedures Avançadas**
   - Parâmetros de entrada e saída
   - Nomenclatura padronizada
   - Tratamento de erros com `TRY...CATCH`
   - Documentação e modularização

3. **Análise de Performance**
   - Leitura de plano de execução
   - Identificação de gargalos
   - Dicas de otimização

4. **Técnicas Avançadas de JOIN**
   - `INNER JOIN`, `LEFT JOIN`
   - `EXISTS`, `NOT EXISTS`
   - Subconsultas eficientes

## 📁 Estrutura do Projeto

```
tsql-desafios-agendados/
│
├── gerar_desafio.py        # Script principal
├── requirements.txt        # Dependências Python
├── README.md              # Documentação
│
├── historico.json         # Histórico de conversas com IA (gerado automaticamente)
├── desafio_anterior.txt   # Último desafio gerado (gerado automaticamente)
├── desafio_tsql.txt       # Histórico de todos os desafios (gerado automaticamente)
└── resolucao_tsql.txt     # Resolução do último desafio (gerado automaticamente)
```

## 📧 Formato dos Emails

### Email do Desafio
- **Assunto**: "📬 Seu Desafio T-SQL do Dia - Aprenda e Pratique!"
- **Formato**: HTML com sintaxe SQL destacada
- **Conteúdo**: Descrição do problema, tabelas de exemplo, dicas

### Email da Resolução
- **Assunto**: "📩 Só abra se já tentou resolver o desafio!"
- **Formato**: HTML com código SQL da solução
- **Conteúdo**: Solução passo a passo com explicações

## 🔧 Personalização

### Modificar Prompts

Edite as funções `gerar_prompt_desafio()` e `gerar_prompt_resolucao()` no arquivo `gerar_desafio.py` para personalizar:

- Nível de dificuldade
- Foco específico (performance, funcionalidades, etc.)
- Estilo de explicação
- Tipos de exercícios

### Alterar Formatação do Email

Modifique a função `enviar_email()` para customizar:

- Estilo CSS
- Layout HTML
- Cores e fontes
- Estrutura do conteúdo

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar problemas:

1. Verifique se todas as variáveis de ambiente estão configuradas
2. Confirme se a API do POE está funcionando
3. Teste o envio de email manualmente
4. Consulte os logs de erro no console

## 🔮 Próximas Funcionalidades

- [ ] Interface web para configuração
- [ ] Múltiplos níveis de dificuldade
- [ ] Integração com outros provedores de IA
- [ ] Dashboard de progresso
- [ ] Exercícios interativos
- [ ] Comunidade de usuários

---

**Desenvolvido com ❤️ para a comunidade T-SQL**

> "A prática leva à perfeição, especialmente em SQL!" 🚀
