#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de conexão com Oracle usando o driver oracledb em modo "thin"
Este modo não requer a instalação do Oracle Client
"""

import oracledb

# Configuração da conexão
username = "RM564440"
password = "290379" 
host = "oracle.fiap.com.br"
port = 1521
sid = "ORCL"

print("Testando conexão com Oracle (modo thin)...")
print(f"Servidor: {host}:{port}")
print(f"SID: {sid}")
print(f"Usuário: {username}")

try:
    # Usar o modo "thin" que não requer Oracle Client
    # Formato esperado do DSN: host:port/service_name
    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=f"{host}:{port}/{sid}"
    )
    
    print("\n✅ Conexão estabelecida com sucesso!")
    
    # Executa uma consulta simples para confirmar
    cursor = connection.cursor()
    cursor.execute("SELECT 'Teste de conexão bem-sucedido' FROM DUAL")
    resultado = cursor.fetchone()
    print(f"Resultado: {resultado[0]}")
    
    # Listar tabelas disponíveis (se existirem)
    print("\nTabelas disponíveis:")
    cursor.execute("""
        SELECT table_name 
        FROM user_tables 
        ORDER BY table_name
    """)
    
    tabelas = cursor.fetchall()
    if tabelas:
        for i, tabela in enumerate(tabelas, 1):
            print(f"{i}. {tabela[0]}")
    else:
        print("Nenhuma tabela encontrada no esquema do usuário.")
    
    # Fecha a conexão
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"\n❌ Erro ao conectar: {e}")
    print("\nVerifique:")
    print("1. Se oracledb está instalado corretamente (pip install oracledb)")
    print("2. Se as credenciais estão corretas")
    print("3. Se o servidor Oracle está acessível pela rede")