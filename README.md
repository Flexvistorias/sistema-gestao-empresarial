# Sistema de Gestão Empresarial v6.3

Sistema completo de gestão empresarial otimizado para deploy no Render.com.

## 🚀 Deploy no Render

Este projeto está configurado para deploy automático no Render.com.

### Autenticação
- Defina as variáveis de ambiente `ADMIN_USERNAME` e `ADMIN_PASSWORD` para acesso.

### Funcionalidades Incluídas
- ✅ Dashboard interativo com gráficos
- ✅ Sistema de login e autenticação
- ✅ Cadastro de clientes com valores especiais
- ✅ Sistema de vendas com descontos
- ✅ Relatórios e análises
- ✅ Configurações do sistema
- ✅ Interface responsiva
- ✅ Banco de dados SQLite integrado

### Estrutura do Projeto
```
├── main.py           # Aplicação Flask principal
├── requirements.txt  # Dependências Python
├── render.yaml      # Configuração do Render
└── README.md        # Este arquivo
```

### Como Usar (Local)
1. Crie um ambiente virtual: `python3 -m venv .venv && source .venv/bin/activate`
2. Instale dependências: `pip install -r requirements.txt`
3. Defina variáveis: `export ADMIN_USERNAME=seu_user ADMIN_PASSWORD=sua_senha`
4. Execute em dev: `python3 main.py` (http://localhost:5000)

### Como Publicar no Render
1. Suba este repositório para o GitHub.
2. No Render, crie um novo serviço Web e selecione o repositório.
3. Confirme: Build `pip install -r requirements.txt`, Start `gunicorn --bind 0.0.0.0:$PORT main:app`.
4. Defina as variáveis `ADMIN_USERNAME` e `ADMIN_PASSWORD` em Settings > Environment.
5. Deploy e acesse a URL fornecida.

### APIs Disponíveis
- `GET /` - Interface principal
- `GET /api/status` - Status do sistema
- `POST /api/login` - Autenticação
- `GET /api/clients` - Listar clientes
- `GET /api/sales` - Listar vendas
- `GET /api/dashboard/stats` - Estatísticas

### Tecnologias
- **Backend:** Flask (dados de demonstração em memória)
- **Frontend:** HTML5 + TailwindCSS + Chart.js
- **Deploy:** Render.com
-- **Banco:** N/A (ponto de extensão para SQLite/PostgreSQL no futuro)

### Suporte
Para suporte técnico, consulte a documentação do projeto ou entre em contato com a equipe de desenvolvimento.

