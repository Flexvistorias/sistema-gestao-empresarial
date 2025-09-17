#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gestão Empresarial v6.3
Otimizado para deploy no Render.com
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# Configuração da aplicação
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sistema-gestao-empresarial-2025')
app.config['DATABASE'] = 'sistema_gestao.db'

# Habilitar CORS para todas as rotas
CORS(app, origins=['*'])

# Template HTML principal
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Gestão Empresarial v6.3</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1"></script>
    <style>
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .card-hover {
            transition: all 0.3s ease;
        }
        .card-hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .tab-button {
            transition: all 0.3s ease;
        }
        .tab-button.active {
            background: #3b82f6;
            color: white;
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="gradient-bg text-white shadow-lg">
        <div class="container mx-auto px-4 py-6">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold">
                        <i class="fas fa-building mr-2"></i>
                        Sistema de Gestão Empresarial
                    </h1>
                    <p class="text-blue-100">Versão 6.3 - Deploy no Render.com</p>
                </div>
                <div id="user-info" class="hidden">
                    <div class="flex items-center">
                        <span id="username" class="mr-3"></span>
                        <button onclick="logout()" class="bg-red-500 hover:bg-red-600 px-4 py-2 rounded">
                            <i class="fas fa-sign-out-alt mr-1"></i>
                            Sair
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Login Form -->
    <div id="login-section" class="min-h-screen flex items-center justify-center">
        <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
            <div class="text-center mb-6">
                <i class="fas fa-user-shield text-4xl text-blue-600 mb-4"></i>
                <h2 class="text-2xl font-bold text-gray-800">Acesso ao Sistema</h2>
                <p class="text-gray-600">Faça login para continuar</p>
            </div>
            
            <form id="login-form" onsubmit="login(event)">
                <div class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2">
                        <i class="fas fa-user mr-1"></i>
                        Usuário
                    </label>
                    <input type="text" id="username-input" class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500" required>
                </div>
                
                <div class="mb-6">
                    <label class="block text-gray-700 text-sm font-bold mb-2">
                        <i class="fas fa-lock mr-1"></i>
                        Senha
                    </label>
                    <input type="password" id="password-input" class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500" required>
                </div>
                
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    <i class="fas fa-sign-in-alt mr-2"></i>
                    Entrar
                </button>
            </form>
            
            <div class="mt-4 p-3 bg-blue-50 rounded">
                <p class="text-sm text-blue-800">
                    <i class="fas fa-info-circle mr-1"></i>
                    <strong>Credenciais padrão:</strong><br>
                    Usuário: admin<br>
                    Senha: admin123
                </p>
            </div>
        </div>
    </div>

    <!-- Main Application -->
    <div id="app-section" class="hidden">
        <!-- Navigation Tabs -->
        <nav class="bg-white shadow-sm border-b">
            <div class="container mx-auto px-4">
                <div class="flex space-x-1">
                    <button onclick="showTab('dashboard')" class="tab-button active px-4 py-3 text-sm font-medium rounded-t-lg">
                        <i class="fas fa-chart-pie mr-1"></i>
                        Dashboard
                    </button>
                    <button onclick="showTab('cadastros')" class="tab-button px-4 py-3 text-sm font-medium rounded-t-lg">
                        <i class="fas fa-users mr-1"></i>
                        Cadastros
                    </button>
                    <button onclick="showTab('vendas')" class="tab-button px-4 py-3 text-sm font-medium rounded-t-lg">
                        <i class="fas fa-shopping-cart mr-1"></i>
                        Vendas
                    </button>
                    <button onclick="showTab('relatorios')" class="tab-button px-4 py-3 text-sm font-medium rounded-t-lg">
                        <i class="fas fa-chart-bar mr-1"></i>
                        Relatórios
                    </button>
                    <button onclick="showTab('configuracoes')" class="tab-button px-4 py-3 text-sm font-medium rounded-t-lg">
                        <i class="fas fa-cog mr-1"></i>
                        Configurações
                    </button>
                </div>
            </div>
        </nav>

        <!-- Tab Contents -->
        <div class="container mx-auto px-4 py-6">
            <!-- Dashboard Tab -->
            <div id="dashboard" class="tab-content active">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Dashboard</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-lg shadow card-hover">
                        <div class="flex items-center">
                            <div class="p-3 rounded-full bg-blue-100 text-blue-600">
                                <i class="fas fa-users text-xl"></i>
                            </div>
                            <div class="ml-4">
                                <p class="text-gray-500 text-sm">Clientes</p>
                                <p class="text-2xl font-bold text-gray-800" id="total-clientes">15</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white p-6 rounded-lg shadow card-hover">
                        <div class="flex items-center">
                            <div class="p-3 rounded-full bg-green-100 text-green-600">
                                <i class="fas fa-shopping-cart text-xl"></i>
                            </div>
                            <div class="ml-4">
                                <p class="text-gray-500 text-sm">Vendas</p>
                                <p class="text-2xl font-bold text-gray-800" id="total-vendas">28</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white p-6 rounded-lg shadow card-hover">
                        <div class="flex items-center">
                            <div class="p-3 rounded-full bg-yellow-100 text-yellow-600">
                                <i class="fas fa-dollar-sign text-xl"></i>
                            </div>
                            <div class="ml-4">
                                <p class="text-gray-500 text-sm">Faturamento</p>
                                <p class="text-2xl font-bold text-gray-800" id="total-faturamento">R$ 8.450</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white p-6 rounded-lg shadow card-hover">
                        <div class="flex items-center">
                            <div class="p-3 rounded-full bg-purple-100 text-purple-600">
                                <i class="fas fa-chart-line text-xl"></i>
                            </div>
                            <div class="ml-4">
                                <p class="text-gray-500 text-sm">Crescimento</p>
                                <p class="text-2xl font-bold text-gray-800">+12%</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div class="bg-white p-6 rounded-lg shadow">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">Vendas por Mês</h3>
                        <canvas id="vendas-chart" height="200"></canvas>
                    </div>
                    
                    <div class="bg-white p-6 rounded-lg shadow">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">Status do Sistema</h3>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center">
                                <span class="text-gray-600">Banco de Dados</span>
                                <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">Online</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-gray-600">API</span>
                                <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">Funcionando</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-gray-600">Última Atualização</span>
                                <span class="text-gray-500 text-sm">{{ datetime.now().strftime('%d/%m/%Y %H:%M') }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Cadastros Tab -->
            <div id="cadastros" class="tab-content">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Cadastros</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div class="bg-white p-6 rounded-lg shadow card-hover">
                        <div class="text-center">
                            <i class="fas fa-users text-4xl text-blue-600 mb-4"></i>
                            <h3 class="text-lg font-bold text-gray-800 mb-2">Clientes</h3>
                            <p class="text-gray-600 text-sm mb-4">Gerencie seus clientes e valores especiais</p>
                            <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
                                Gerenciar
                            </button>
                        </div>
                    </div>
                    
                    <div class="bg-white p-6 rounded-lg shadow card-hover">
                        <div class="text-center">
                            <i class="fas fa-cogs text-4xl text-green-600 mb-4"></i>
                            <h3 class="text-lg font-bold text-gray-800 mb-2">Serviços</h3>
                            <p class="text-gray-600 text-sm mb-4">Configure tipos de vistoria e serviços</p>
                            <button class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">
                                Gerenciar
                            </button>
                        </div>
                    </div>
                    
                    <div class="bg-white p-6 rounded-lg shadow card-hover">
                        <div class="text-center">
                            <i class="fas fa-user-shield text-4xl text-purple-600 mb-4"></i>
                            <h3 class="text-lg font-bold text-gray-800 mb-2">Usuários</h3>
                            <p class="text-gray-600 text-sm mb-4">Controle de acesso e permissões</p>
                            <button class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded">
                                Gerenciar
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Vendas Tab -->
            <div id="vendas" class="tab-content">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Sistema de Vendas</h2>
                
                <div class="bg-white p-6 rounded-lg shadow">
                    <h3 class="text-lg font-bold text-gray-800 mb-4">Nova Venda</h3>
                    
                    <form class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-gray-700 text-sm font-bold mb-2">Cliente</label>
                            <select class="w-full px-3 py-2 border border-gray-300 rounded">
                                <option>Selecione um cliente</option>
                                <option>João Silva</option>
                                <option>Maria Santos</option>
                                <option>Pedro Oliveira</option>
                            </select>
                        </div>
                        
                        <div>
                            <label class="block text-gray-700 text-sm font-bold mb-2">Serviço</label>
                            <select class="w-full px-3 py-2 border border-gray-300 rounded">
                                <option>Selecione um serviço</option>
                                <option>Vistoria Veicular</option>
                                <option>Inspeção Técnica</option>
                                <option>Laudo Técnico</option>
                            </select>
                        </div>
                        
                        <div>
                            <label class="block text-gray-700 text-sm font-bold mb-2">Valor Original</label>
                            <input type="text" class="w-full px-3 py-2 border border-gray-300 rounded" value="R$ 150,00" readonly>
                        </div>
                        
                        <div>
                            <label class="block text-gray-700 text-sm font-bold mb-2">Desconto</label>
                            <input type="text" class="w-full px-3 py-2 border border-gray-300 rounded" placeholder="R$ 0,00">
                        </div>
                        
                        <div class="md:col-span-2">
                            <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded">
                                <i class="fas fa-save mr-2"></i>
                                Registrar Venda
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Relatórios Tab -->
            <div id="relatorios" class="tab-content">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Relatórios</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-white p-6 rounded-lg shadow card-hover">
                        <div class="text-center">
                            <i class="fas fa-file-invoice text-4xl text-blue-600 mb-4"></i>
                            <h3 class="text-lg font-bold text-gray-800 mb-2">Contas a Receber</h3>
                            <p class="text-gray-600 text-sm mb-4">Vendas pendentes e recebidas</p>
                            <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
                                Visualizar
                            </button>
                        </div>
                    </div>
                    
                    <div class="bg-white p-6 rounded-lg shadow card-hover">
                        <div class="text-center">
                            <i class="fas fa-chart-pie text-4xl text-green-600 mb-4"></i>
                            <h3 class="text-lg font-bold text-gray-800 mb-2">Análise de Descontos</h3>
                            <p class="text-gray-600 text-sm mb-4">Diferença entre valor real e vendido</p>
                            <button class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">
                                Visualizar
                            </button>
                        </div>
                    </div>
                    
                    <div class="bg-white p-6 rounded-lg shadow card-hover">
                        <div class="text-center">
                            <i class="fas fa-calendar-alt text-4xl text-purple-600 mb-4"></i>
                            <h3 class="text-lg font-bold text-gray-800 mb-2">Relatórios Mensais</h3>
                            <p class="text-gray-600 text-sm mb-4">Análise mensal de performance</p>
                            <button class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded">
                                Visualizar
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Configurações Tab -->
            <div id="configuracoes" class="tab-content">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Configurações</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-white p-6 rounded-lg shadow">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">Tipos de Vistoria</h3>
                        <div class="space-y-2">
                            <div class="flex justify-between items-center p-2 bg-gray-50 rounded">
                                <span>Vistoria Veicular</span>
                                <button class="text-blue-600 hover:text-blue-800">
                                    <i class="fas fa-edit"></i>
                                </button>
                            </div>
                            <div class="flex justify-between items-center p-2 bg-gray-50 rounded">
                                <span>Inspeção Técnica</span>
                                <button class="text-blue-600 hover:text-blue-800">
                                    <i class="fas fa-edit"></i>
                                </button>
                            </div>
                        </div>
                        <button class="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
                            <i class="fas fa-plus mr-1"></i>
                            Adicionar Tipo
                        </button>
                    </div>
                    
                    <div class="bg-white p-6 rounded-lg shadow">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">Formas de Pagamento</h3>
                        <div class="space-y-2">
                            <div class="flex justify-between items-center p-2 bg-gray-50 rounded">
                                <span>Dinheiro</span>
                                <button class="text-blue-600 hover:text-blue-800">
                                    <i class="fas fa-edit"></i>
                                </button>
                            </div>
                            <div class="flex justify-between items-center p-2 bg-gray-50 rounded">
                                <span>Cartão de Crédito</span>
                                <button class="text-blue-600 hover:text-blue-800">
                                    <i class="fas fa-edit"></i>
                                </button>
                            </div>
                        </div>
                        <button class="mt-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">
                            <i class="fas fa-plus mr-1"></i>
                            Adicionar Forma
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Estado da aplicação
        let currentUser = null;

        // Função de login
        async function login(event) {
            event.preventDefault();
            
            const username = document.getElementById('username-input').value;
            const password = document.getElementById('password-input').value;
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    currentUser = data.user;
                    document.getElementById('username').textContent = currentUser.username;
                    document.getElementById('login-section').classList.add('hidden');
                    document.getElementById('app-section').classList.remove('hidden');
                    document.getElementById('user-info').classList.remove('hidden');
                    
                    // Carregar dados do dashboard
                    loadDashboardData();
                } else {
                    alert('Credenciais inválidas!');
                }
            } catch (error) {
                console.error('Erro no login:', error);
                alert('Erro ao fazer login. Tente novamente.');
            }
        }

        // Função de logout
        function logout() {
            currentUser = null;
            document.getElementById('login-section').classList.remove('hidden');
            document.getElementById('app-section').classList.add('hidden');
            document.getElementById('user-info').classList.add('hidden');
            document.getElementById('username-input').value = '';
            document.getElementById('password-input').value = '';
        }

        // Função para mostrar abas
        function showTab(tabName) {
            // Esconder todas as abas
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Remover classe active de todos os botões
            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(button => button.classList.remove('active'));
            
            // Mostrar aba selecionada
            document.getElementById(tabName).classList.add('active');
            
            // Adicionar classe active ao botão clicado
            event.target.classList.add('active');
        }

        // Carregar dados do dashboard
        function loadDashboardData() {
            // Criar gráfico de vendas
            const ctx = document.getElementById('vendas-chart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                    datasets: [{
                        label: 'Vendas',
                        data: [12, 19, 8, 15, 22, 28],
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        // Inicialização
        document.addEventListener('DOMContentLoaded', function() {
            // Focar no campo de usuário
            document.getElementById('username-input').focus();
        });
    </script>
</body>
</html>
"""

def init_database():
    """Inicializa o banco de dados com dados de exemplo"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Criar tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Criar tabela de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            special_inspection_value DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Criar tabela de vendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            service_name TEXT NOT NULL,
            original_value DECIMAL(10,2) NOT NULL,
            discount_value DECIMAL(10,2) DEFAULT 0,
            final_value DECIMAL(10,2) NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')
    
    # Inserir usuário admin padrão
    admin_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password_hash, email)
        VALUES (?, ?, ?)
    ''', ('admin', admin_password, 'admin@sistema.com'))
    
    # Inserir dados de exemplo
    sample_clients = [
        ('João Silva', 'joao@email.com', '(11) 99999-9999', 'Rua A, 123', 120.00),
        ('Maria Santos', 'maria@email.com', '(11) 88888-8888', 'Rua B, 456', 130.00),
        ('Pedro Oliveira', None, None, None, 110.00)
    ]
    
    for client in sample_clients:
        cursor.execute('''
            INSERT OR IGNORE INTO clients (name, email, phone, address, special_inspection_value)
            VALUES (?, ?, ?, ?, ?)
        ''', client)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Página principal do sistema"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    """Status da API"""
    return jsonify({
        'status': 'online',
        'version': '6.3',
        'database': 'connected',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint de login"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Usuário e senha são obrigatórios'})
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, password_hash FROM users WHERE username = ? AND is_active = 1', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        return jsonify({
            'success': True,
            'user': {
                'id': user[0],
                'username': user[1]
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Credenciais inválidas'})

@app.route('/api/clients', methods=['GET'])
def get_clients():
    """Listar clientes"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM clients ORDER BY name')
    clients = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': client[0],
        'name': client[1],
        'email': client[2],
        'phone': client[3],
        'address': client[4],
        'special_inspection_value': client[5]
    } for client in clients])

@app.route('/api/sales', methods=['GET'])
def get_sales():
    """Listar vendas"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.*, c.name as client_name 
        FROM sales s 
        LEFT JOIN clients c ON s.client_id = c.id 
        ORDER BY s.sale_date DESC
    ''')
    sales = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': sale[0],
        'client_id': sale[1],
        'service_name': sale[2],
        'original_value': sale[3],
        'discount_value': sale[4],
        'final_value': sale[5],
        'sale_date': sale[6],
        'client_name': sale[7]
    } for sale in sales])

@app.route('/api/dashboard/stats', methods=['GET'])
def dashboard_stats():
    """Estatísticas do dashboard"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Contar clientes
    cursor.execute('SELECT COUNT(*) FROM clients')
    total_clients = cursor.fetchone()[0]
    
    # Contar vendas
    cursor.execute('SELECT COUNT(*) FROM sales')
    total_sales = cursor.fetchone()[0]
    
    # Somar faturamento
    cursor.execute('SELECT SUM(final_value) FROM sales')
    total_revenue = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return jsonify({
        'total_clients': total_clients,
        'total_sales': total_sales,
        'total_revenue': float(total_revenue)
    })

if __name__ == '__main__':
    # Inicializar banco de dados
    init_database()
    
    # Configurar porta para o Render
    port = int(os.environ.get('PORT', 5000))
    
    # Executar aplicação
    app.run(host='0.0.0.0', port=port, debug=False)

