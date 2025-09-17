# Sistema de Gestão Empresarial v6.3

Sistema completo de gestão empresarial otimizado para deploy no Render.com.

## 🚀 Deploy no Render

Este projeto está configurado para deploy automático no Render.com.

### Credenciais Padrão
- **Usuário:** admin
- **Senha:** admin123

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

### Como Usar
1. Faça upload destes arquivos para um repositório GitHub
2. Conecte o repositório ao Render.com
3. O deploy será automático
4. Acesse a URL fornecida pelo Render
5. Faça login com as credenciais padrão

### APIs Disponíveis
- `GET /` - Interface principal
- `GET /api/status` - Status do sistema
- `POST /api/login` - Autenticação
- `GET /api/clients` - Listar clientes
- `GET /api/sales` - Listar vendas
- `GET /api/dashboard/stats` - Estatísticas

### Tecnologias
- **Backend:** Flask + SQLite
- **Frontend:** HTML5 + TailwindCSS + Chart.js
- **Deploy:** Render.com
- **Banco:** SQLite (incluído)

### Suporte
Para suporte técnico, consulte a documentação do projeto ou entre em contato com a equipe de desenvolvimento.

