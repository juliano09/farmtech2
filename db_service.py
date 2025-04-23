#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Monitoramento de Eficiência da Colheita de Cana
Serviço para operações com banco de dados Oracle usando oracledb em modo "thin"
"""

import oracledb

from config import ORACLE_CONFIG
from colheita import Colheita

class OracleService:
    """Serviço para operações com o banco de dados Oracle"""
    
    def __init__(self):
        """Inicializa o serviço"""
        self.disponivel = True
    
    def conectar(self):
        """
        Estabelece conexão com o banco de dados Oracle usando modo "thin"
        que não requer Oracle Client instalado
        
        Returns:
            connection: Objeto de conexão com o banco ou None em caso de erro
        """
        try:
            # Formato de conexão para modo thin: host:port/service_name
            dsn = f"{ORACLE_CONFIG['host']}:{ORACLE_CONFIG['port']}/{ORACLE_CONFIG['sid']}"
            
            # Estabelece a conexão
            connection = oracledb.connect(
                user=ORACLE_CONFIG['user'],
                password=ORACLE_CONFIG['password'],
                dsn=dsn
            )
            
            return connection
        except Exception as e:
            print(f"Erro ao conectar ao banco Oracle: {e}")
            return None
    
    def testar_conexao(self):
        """
        Testa a conexão com o banco Oracle
        
        Returns:
            bool: True se a conexão foi bem-sucedida, False caso contrário
        """
        try:
            conn = self.conectar()
            if conn:
                print("Conexão com o banco Oracle estabelecida com sucesso!")
                # Execute uma consulta simples para confirmar que tudo está funcionando
                cursor = conn.cursor()
                cursor.execute("SELECT 'Teste de conexão bem-sucedido' FROM DUAL")
                resultado = cursor.fetchone()
                print(f"Resultado: {resultado[0]}")
                cursor.close()
                conn.close()
                return True
            else:
                print("Não foi possível conectar ao banco Oracle.")
                return False
        except Exception as e:
            print(f"Erro ao testar conexão: {e}")
            return False
    
    def criar_tabela_colheitas(self):
        """
        Cria a tabela para armazenar os dados de colheitas no Oracle
        
        Returns:
            bool: True se a tabela foi criada com sucesso, False caso contrário
        """
        conn = self.conectar()
        if not conn:
            return False
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            # Verifica se a tabela já existe
            try:
                cursor.execute("SELECT COUNT(*) FROM COLHEITAS_CANA")
                print("A tabela COLHEITAS_CANA já existe.")
                return True
            except oracledb.DatabaseError:
                # Tabela não existe, vamos criar
                pass
            
            # Cria a tabela
            cursor.execute("""
            CREATE TABLE COLHEITAS_CANA (
                ID_COLHEITA NUMBER GENERATED ALWAYS AS IDENTITY,
                ID_LOTE VARCHAR2(50) NOT NULL,
                TIPO VARCHAR2(20) NOT NULL,
                DATA_COLHEITA VARCHAR2(20) NOT NULL,
                QUANTIDADE_PREVISTA NUMBER(10,2) NOT NULL,
                QUANTIDADE_COLHIDA NUMBER(10,2) NOT NULL,
                EFICIENCIA NUMBER(5,2) NOT NULL,
                PERDA NUMBER(5,2) NOT NULL,
                OBSERVACOES VARCHAR2(500),
                DATA_REGISTRO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT PK_COLHEITAS_CANA PRIMARY KEY (ID_COLHEITA),
                CONSTRAINT UK_COLHEITAS_LOTE UNIQUE (ID_LOTE)
            )
            """)
            
            conn.commit()
            print("Tabela COLHEITAS_CANA criada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def inserir_colheita(self, colheita):
        """
        Insere uma colheita no banco de dados Oracle
        
        Args:
            colheita (Colheita): Objeto Colheita a ser inserido
            
        Returns:
            bool: True se a inserção foi bem-sucedida, False caso contrário
        """
        conn = self.conectar()
        if not conn:
            return False
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            # Verifica se já existe uma colheita com o mesmo ID_LOTE
            cursor.execute(
                "SELECT COUNT(*) FROM COLHEITAS_CANA WHERE ID_LOTE = :id_lote",
                id_lote=colheita.id_lote
            )
            
            if cursor.fetchone()[0] > 0:
                # Atualiza a colheita existente
                cursor.execute("""
                UPDATE COLHEITAS_CANA
                SET 
                    TIPO = :tipo,
                    DATA_COLHEITA = :data,
                    QUANTIDADE_PREVISTA = :previsto,
                    QUANTIDADE_COLHIDA = :colhido,
                    EFICIENCIA = :eficiencia,
                    PERDA = :perda,
                    OBSERVACOES = :obs,
                    DATA_REGISTRO = CURRENT_TIMESTAMP
                WHERE 
                    ID_LOTE = :id_lote
                """, 
                    tipo=colheita.tipo,
                    data=colheita.data,
                    previsto=colheita.previsto,
                    colhido=colheita.colhido,
                    eficiencia=colheita.eficiencia,
                    perda=colheita.perda,
                    obs=colheita.obs,
                    id_lote=colheita.id_lote
                )
                print(f"Colheita do lote {colheita.id_lote} atualizada no Oracle.")
            else:
                # Insere nova colheita
                cursor.execute("""
                INSERT INTO COLHEITAS_CANA (
                    ID_LOTE, TIPO, DATA_COLHEITA, 
                    QUANTIDADE_PREVISTA, QUANTIDADE_COLHIDA, 
                    EFICIENCIA, PERDA, OBSERVACOES
                ) VALUES (
                    :id_lote, :tipo, :data, 
                    :previsto, :colhido, 
                    :eficiencia, :perda, :obs
                )
                """,
                    id_lote=colheita.id_lote,
                    tipo=colheita.tipo,
                    data=colheita.data,
                    previsto=colheita.previsto,
                    colhido=colheita.colhido,
                    eficiencia=colheita.eficiencia,
                    perda=colheita.perda,
                    obs=colheita.obs
                )
                print(f"Colheita do lote {colheita.id_lote} inserida no Oracle.")
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir/atualizar colheita: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def consultar_colheitas(self):
        """
        Consulta todas as colheitas no banco de dados
        
        Returns:
            list: Lista de objetos Colheita ou lista vazia em caso de erro
        """
        conn = self.conectar()
        if not conn:
            return []
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT 
                ID_LOTE, TIPO, DATA_COLHEITA, 
                QUANTIDADE_PREVISTA, QUANTIDADE_COLHIDA, 
                EFICIENCIA, PERDA, OBSERVACOES
            FROM 
                COLHEITAS_CANA
            ORDER BY 
                DATA_COLHEITA DESC
            """)
            
            colheitas = []
            for row in cursor:
                colheita = Colheita(
                    id_lote=row[0],
                    tipo=row[1],
                    data=row[2],
                    previsto=row[3],
                    colhido=row[4],
                    eficiencia=row[5],
                    perda=row[6],
                    obs=row[7] if row[7] else ""
                )
                colheitas.append(colheita)
            
            return colheitas
        except Exception as e:
            print(f"Erro ao consultar colheitas: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def excluir_colheita(self, id_lote):
        """
        Exclui uma colheita do banco de dados
        
        Args:
            id_lote (str): ID do lote a ser excluído
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário
        """
        conn = self.conectar()
        if not conn:
            return False
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            cursor.execute(
                "DELETE FROM COLHEITAS_CANA WHERE ID_LOTE = :id_lote",
                id_lote=id_lote
            )
            
            if cursor.rowcount > 0:
                print(f"Colheita do lote {id_lote} excluída do Oracle.")
                conn.commit()
                return True
            else:
                print(f"Colheita do lote {id_lote} não encontrada no Oracle.")
                return False
        except Exception as e:
            print(f"Erro ao excluir colheita: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def salvar_colheitas(self, colheitas):
        """
        Salva uma lista de colheitas no banco de dados
        
        Args:
            colheitas (list): Lista de objetos Colheita a serem salvos
            
        Returns:
            int: Número de colheitas salvas com sucesso
        """
        if not colheitas:
            return 0
        
        contador = 0
        for colheita in colheitas:
            if self.inserir_colheita(colheita):
                contador += 1
        
        return contador