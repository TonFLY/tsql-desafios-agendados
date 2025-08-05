# 🚀 Deploy na Vercel com Cron Jobs

## 📋 Pré-requisitos
1. Conta na Vercel (gratuita)
2. GitHub account
3. Projeto commitado no GitHub

## 🔧 Configuração das Variáveis de Ambiente na Vercel

Após fazer o deploy, configure essas variáveis no painel da Vercel:

1. Acesse seu projeto na Vercel
2. Vá em **Settings** → **Environment Variables**
3. Adicione as seguintes variáveis:

```
EMAIL=techwellington.dev@gmail.com
APP_PASSWORD=lvrzselkbymilynu
REMETENTE=techwellington.dev@gmail.com
POE_API_KEY=mZ8_Dj_FVF_-Azidopxjibl1w7dfnPu17ylRxQY6IIo
BOT_NAME=botsupremooo
```

## 🚀 Como fazer o Deploy

### Opção 1: Via GitHub (Recomendado)
1. Faça push do código para o GitHub
2. Conecte o repositório à Vercel
3. Deploy automático!

### Opção 2: Via Vercel CLI
```bash
# Instalar Vercel CLI
npm i -g vercel

# Fazer login
vercel login

# Deploy
vercel --prod
```

## ⏰ Configuração do Cron Job

O arquivo `vercel.json` já está configurado com:
- **Horário**: Todo dia às 8h (0 8 * * *)
- **Endpoint**: `/api/cron-desafio`
- **Timeout**: 60 segundos

## 🧪 Testando

### Teste manual:
- `https://seu-projeto.vercel.app/api/test`
- `https://seu-projeto.vercel.app/api/cron-desafio`

### Monitoramento:
- Logs disponíveis no painel da Vercel
- **Functions** → **View Function Logs**

## 💰 Limites do Plano Gratuito

- ✅ **100 execuções de Cron/mês** (3+ por dia)
- ✅ **10GB de bandwidth**
- ✅ **100 builds por dia**
- ⚠️ **10 segundos de execução** (mas configuramos 60s)

## 🎯 Cronograma Sugerido

```json
{
  "crons": [
    {
      "path": "/api/cron-desafio",
      "schedule": "0 8 * * *"  // Todo dia às 8h
    }
  ]
}
```

### Outros exemplos de horários:
- `0 8 * * 1-5` - Segunda a sexta às 8h
- `0 8,20 * * *` - Todo dia às 8h e 20h
- `0 8 * * 1` - Apenas segundas às 8h

## 🔍 Troubleshooting

### Se o cron não executar:
1. Verifique se o plano suporta crons
2. Confirme as variáveis de ambiente
3. Teste o endpoint manualmente
4. Verifique os logs na Vercel

### Se o email não enviar:
1. Confirme a senha de aplicativo do Gmail
2. Verifique se a 2FA está ativa
3. Teste com outro provedor de email

## 📊 Monitoramento

A Vercel oferece:
- **Analytics** de execução
- **Logs** detalhados
- **Alertas** de erro
- **Métricas** de performance
