# 🚀 Guia de Deploy no Vercel - Renovação Aluguel Uber

Este documento contém todas as orientações necessárias para fazer o deploy correto da aplicação no Vercel e resolver problemas comuns, especialmente relacionados a imagens quebradas.

## 📋 Índice

- [Problemas Comuns e Soluções](#problemas-comuns-e-soluções)
- [Configuração Inicial](#configuração-inicial)
- [Deploy Automático via GitHub](#deploy-automático-via-github)
- [Deploy Manual via CLI](#deploy-manual-via-cli)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Verificação e Testes](#verificação-e-testes)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Problemas Comuns e Soluções

### ❌ Por que as imagens estão quebrando no Vercel?

As imagens podem quebrar por **3 motivos principais**:

#### 1. **Sensibilidade a maiúsculas/minúsculas (Case Sensitivity)**

⚠️ **O problema mais comum!**

- **Windows/Mac**: `Etiosinterior.jpg` = `etiosinterior.jpg` (ignora diferença)
- **Linux (Vercel)**: `Etiosinterior.jpg` ≠ `etiosinterior.jpg` (diferencia maiúsculas)

**✅ Solução:** 
- Todos os arquivos de imagem devem estar em **minúsculas**
- As referências no código também devem estar em **minúsculas**
- Este repositório já está configurado corretamente

**Exemplo correto:**
```tsx
// ✅ CORRETO - tudo em minúsculas
images: [
  "/images/etioscarro.jpg",
  "/images/etiosinterior.jpg",
  "/images/etiospainel.jpg"
]

// ❌ ERRADO - mistura de maiúsculas
images: [
  "/images/etioscarro.jpg",
  "/images/Etiosinterior.jpg",  // Capital E vai quebrar no Vercel!
  "/images/Etiospainel.jpg"     // Capital E vai quebrar no Vercel!
]
```

#### 2. **Caminho incorreto das imagens**

**⚠️ IMPORTANTE:** No Vite, as imagens estáticas devem estar na pasta `public/images/`:

```
projeto/
├── public/           ← Pasta especial do Vite
│   └── images/       ← Imagens aqui
│       ├── logancarro.jpg
│       └── ...
├── components/
├── index.html
└── ...
```

**Como funciona:**
- Vite copia automaticamente tudo de `public/` para a raiz do `dist/` no build
- `public/images/arquivo.jpg` vira `dist/images/arquivo.jpg`
- No código, referencie como `/images/arquivo.jpg` (sem o "public")

**✅ Referência correta no código:**
```tsx
<img src="/images/logancarro.jpg" alt="Logan" />
```

**❌ NÃO use:**
```tsx
<img src="./images/logancarro.jpg" alt="Logan" />      // Caminho relativo
<img src="public/images/logancarro.jpg" alt="Logan" /> // Não inclua "public"
```

#### 3. **Configuração do Vercel**

O arquivo `vercel.json` garante que:
- As imagens sejam servidas corretamente
- O roteamento SPA funcione
- Headers de segurança sejam aplicados
- Cache seja otimizado

---

## ⚙️ Configuração Inicial

### Pré-requisitos

- Conta no [Vercel](https://vercel.com)
- Repositório no GitHub
- Node.js instalado (versão 18+)

### 1. Instalar dependências

```bash
npm install
```

### 2. Testar localmente

```bash
# Desenvolvimento
npm run dev

# Build de produção
npm run build

# Preview do build
npm run preview
```

Acesse `http://localhost:3000` e verifique se as imagens carregam corretamente.

---

## 🚀 Deploy Automático via GitHub

Esta é a forma **recomendada** para deploy contínuo.

### Passo 1: Conectar ao Vercel

1. Acesse [vercel.com](https://vercel.com)
2. Clique em **"Add New Project"**
3. Selecione **"Import Git Repository"**
4. Escolha seu repositório: `GHDaru/renovacaoalugueluber`
5. Autorize o acesso ao GitHub se necessário

### Passo 2: Configurar o Projeto

O Vercel detectará automaticamente que é um projeto **Vite + React**:

```
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

**⚠️ Importante:** Deixe essas configurações como estão (padrão do Vite).

### Passo 3: Configurar Variáveis de Ambiente

Se sua aplicação usa API keys (como Gemini AI):

1. Na página de configuração do projeto, vá em **"Environment Variables"**
2. Adicione:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** `sua-chave-api-aqui`
3. Selecione os ambientes: Production, Preview, Development

### Passo 4: Deploy!

1. Clique em **"Deploy"**
2. Aguarde 1-2 minutos
3. Seu site estará disponível em: `https://seu-projeto.vercel.app`

### Deploy Automático em Cada Push

Após a configuração inicial:
- ✅ Todo `push` na branch `main` → Deploy em **Produção**
- ✅ Todo `push` em outras branches → Deploy de **Preview**
- ✅ Todo Pull Request → Deploy de **Preview** automático

---

## 💻 Deploy Manual via CLI

Para usuários avançados ou CI/CD customizado:

### 1. Instalar Vercel CLI

```bash
npm install -g vercel
```

### 2. Login

```bash
vercel login
```

### 3. Deploy

```bash
# Deploy de preview
vercel

# Deploy de produção
vercel --prod
```

---

## 🔐 Variáveis de Ambiente

### Arquivo .env.local (desenvolvimento)

Crie um arquivo `.env.local` na raiz:

```env
GEMINI_API_KEY=sua-chave-aqui
```

### Vercel (produção)

Configure via:
1. **Dashboard Vercel** → Projeto → Settings → Environment Variables
2. **CLI:**
   ```bash
   vercel env add GEMINI_API_KEY
   ```

**⚠️ Nunca commite arquivos `.env` para o Git!**

---

## ✅ Verificação e Testes

### Checklist Pós-Deploy

Após o deploy, verifique:

- [ ] Site está acessível na URL do Vercel
- [ ] **Todas as imagens carregam corretamente** (Hero, Frota, etc.)
- [ ] Botões do WhatsApp funcionam
- [ ] Navegação entre seções funciona (Hero, Planos, Frota, etc.)
- [ ] Formulários enviam dados corretamente
- [ ] Layout responsivo funciona em mobile
- [ ] Console do navegador não mostra erros 404 de imagens

### Como verificar imagens quebradas

1. Abra o site no Vercel
2. Abra o **DevTools** do navegador (F12)
3. Vá na aba **Console**
4. Procure por erros `404` ou `Failed to load resource`
5. Se houver erros de imagem, verifique:
   - Nome do arquivo está correto
   - Arquivo existe na pasta `images/`
   - Não há diferença de maiúsculas/minúsculas

**Exemplo de erro comum:**
```
GET https://seu-site.vercel.app/images/Etiosinterior.jpg 404 (Not Found)
```

**Solução:** Renomear arquivo para minúsculas e atualizar código.

---

## 🐛 Troubleshooting

### Problema: Imagens não carregam (404)

**Sintomas:**
- Placeholder cinza no lugar da imagem
- Erro 404 no console: `GET /images/arquivo.jpg 404`

**Soluções:**

1. **Verificar case sensitivity:**
   ```bash
   # Listar arquivos exatos
   ls public/images/
   
   # Renomear se necessário (dentro de public/images/)
   cd public/images/
   mv Arquivo.jpg arquivo.jpg
   ```

2. **Verificar referência no código:**
   ```tsx
   // Buscar todas as referências
   grep -r "images/" components/
   ```

3. **Rebuild e redeploy:**
   ```bash
   npm run build
   vercel --prod
   ```

### Problema: Build falha no Vercel

**Sintomas:**
- Deploy falha com erro de build
- Mensagem: `Build failed`

**Soluções:**

1. **Verificar build local:**
   ```bash
   npm run build
   ```
   Se falhar localmente, corrija os erros primeiro.

2. **Verificar logs no Vercel:**
   - Dashboard → Projeto → Deployments → Último deploy → View Build Logs

3. **Dependências desatualizadas:**
   ```bash
   npm install
   npm update
   ```

### Problema: Variáveis de ambiente não funcionam

**Sintomas:**
- API calls falham
- Funcionalidades que dependem de env vars não funcionam

**Soluções:**

1. **Verificar configuração:**
   - Dashboard Vercel → Settings → Environment Variables
   - Certifique-se de que as variáveis estão configuradas

2. **Prefixo correto:**
   - Para Vite: use `VITE_` como prefixo se necessário
   - Exemplo: `VITE_API_KEY`

3. **Redeploy após adicionar variáveis:**
   ```bash
   vercel --prod
   ```

### Problema: CSS não carrega ou layout quebrado

**Sintomas:**
- Site sem estilização
- Layout desconfigurado

**Soluções:**

1. **Verificar Tailwind CDN:**
   - Certifique-se de que o CDN do Tailwind está no `index.html`

2. **Verificar output do build:**
   ```bash
   npm run build
   ls -la dist/
   ```

3. **Limpar cache do Vercel:**
   - Dashboard → Settings → Clear Build Cache → Redeploy

### Problema: Roteamento SPA não funciona

**Sintomas:**
- Refresh na página dá 404
- Links diretos não funcionam

**Solução:**
- O arquivo `vercel.json` já está configurado com rewrites:
  ```json
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
  ```

---

## 📚 Recursos Adicionais

### Documentação Oficial

- [Vercel Docs](https://vercel.com/docs)
- [Vite Docs](https://vitejs.dev)
- [React Docs](https://react.dev)

### Suporte

- **Vercel Support:** [vercel.com/support](https://vercel.com/support)
- **Issues do projeto:** [GitHub Issues](https://github.com/GHDaru/renovacaoalugueluber/issues)

---

## 🎯 Checklist de Deploy Perfeito

Use este checklist antes de cada deploy:

- [ ] Build local funciona: `npm run build`
- [ ] Preview local funciona: `npm run preview`
- [ ] Todas as imagens estão em **minúsculas** dentro de `public/images/`
- [ ] Referências às imagens no código estão em **minúsculas**
- [ ] Variáveis de ambiente configuradas no Vercel
- [ ] Arquivo `vercel.json` está na raiz
- [ ] `.gitignore` não exclui a pasta `public/`
- [ ] Commit e push das últimas mudanças
- [ ] Deploy realizado
- [ ] Verificação pós-deploy completa

---

## 📝 Notas Importantes

1. **Sempre use minúsculas** para nomes de arquivos de imagem
2. **Teste localmente** antes de fazer deploy
3. **Monitore os logs** de build no Vercel
4. **Use deploy de preview** para testar mudanças antes da produção
5. **Configure variáveis de ambiente** corretamente

---

## 🎉 Sucesso!

Se você seguiu todas as orientações deste guia, seu site deve estar funcionando perfeitamente no Vercel, com todas as imagens carregando corretamente!

**URL do site:** `https://seu-projeto.vercel.app`

Para dúvidas ou problemas, abra uma [issue no GitHub](https://github.com/GHDaru/renovacaoalugueluber/issues).

---

**Última atualização:** Janeiro 2026
**Versão:** 1.0
