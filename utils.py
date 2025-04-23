#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Monitoramento de Eficiência da Colheita de Cana
Módulo para manipulação de arquivos JSON e TXT
"""

import os
import json
from datetime import datetime

def salvar_json(dados, caminho_arquivo):
    """
    Salva dados em formato JSON
    
    Args:
        dados: Os dados a serem salvos
        caminho_arquivo (str): Caminho para o arquivo JSON
        
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    try:
        # Certifique-se de que o diretório existe
        diretorio = os.path.dirname(caminho_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
            
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo JSON: {e}")
        return False


def carregar_json(caminho_arquivo):
    """
    Carrega dados de um arquivo JSON
    
    Args:
        caminho_arquivo (str): Caminho do arquivo JSON
        
    Returns:
        dados: Os dados carregados do arquivo, ou uma lista vazia se houver erro
    """
    try:
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        return []
    except Exception as e:
        print(f"Erro ao carregar arquivo JSON: {e}")
        return []


def gerar_relatorio(dados, caminho_arquivo, titulo="RELATÓRIO"):
    """
    Gera um relatório em formato de texto
    
    Args:
        dados (list): Lista de colheitas para incluir no relatório
        caminho_arquivo (str): Caminho para salvar o relatório
        titulo (str): Título do relatório
        
    Returns:
        bool: True se gerou com sucesso, False caso contrário
    """
    try:
        # Certifique-se de que o diretório existe
        diretorio = os.path.dirname(caminho_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
            
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            # Cabeçalho
            arquivo.write("=" * 60 + "\n")
            arquivo.write(f"{titulo.center(60)}\n")
            arquivo.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            arquivo.write("=" * 60 + "\n\n")
            
            # Se não houver dados, informa no relatório
            if not dados:
                arquivo.write("Nenhum dado disponível para este relatório.\n")
                return True
                
            # Estatísticas gerais
            arquivo.write("ESTATÍSTICAS GERAIS\n")
            arquivo.write("-" * 60 + "\n")
            
            # Definindo dados específicos para relatório de colheitas
            if all(isinstance(item, dict) and 'tipo' in item for item in dados):
                # Cálculos específicos para colheitas
                colheitas_manuais = [c for c in dados if c['tipo'] == 'manual']
                colheitas_mecanicas = [c for c in dados if c['tipo'] == 'mecanica']
                
                total_manual = len(colheitas_manuais)
                total_mecanica = len(colheitas_mecanicas)
                
                try:
                    media_eficiencia_manual = sum(c['eficiencia'] for c in colheitas_manuais) / total_manual if total_manual > 0 else 0
                    media_eficiencia_mecanica = sum(c['eficiencia'] for c in colheitas_mecanicas) / total_mecanica if total_mecanica > 0 else 0
                    media_geral = sum(c['eficiencia'] for c in dados) / len(dados) if dados else 0
                except KeyError:
                    # Se a chave 'eficiencia' não existir
                    media_eficiencia_manual = media_eficiencia_mecanica = media_geral = 0
                
                arquivo.write(f"Total de registros: {len(dados)}\n")
                arquivo.write(f"Colheitas manuais: {total_manual}\n")
                arquivo.write(f"Colheitas mecânicas: {total_mecanica}\n\n")
                
                arquivo.write("COMPARATIVO DE EFICIÊNCIA\n")
                arquivo.write(f"Eficiência média total: {media_geral:.2f}%\n")
                arquivo.write(f"Eficiência média (manual): {media_eficiencia_manual:.2f}%\n")
                arquivo.write(f"Eficiência média (mecânica): {media_eficiencia_mecanica:.2f}%\n")
                arquivo.write(f"Diferença: {abs(media_eficiencia_manual - media_eficiencia_mecanica):.2f}%\n\n")
                
                # Análise e recomendações
                arquivo.write("ANÁLISE E RECOMENDAÇÕES\n")
                if media_eficiencia_manual > media_eficiencia_mecanica:
                    diferenca = media_eficiencia_manual - media_eficiencia_mecanica
                    arquivo.write(f"A colheita manual está {diferenca:.2f}% mais eficiente que a mecânica.\n")
                    arquivo.write("Recomendações:\n")
                    arquivo.write("- Verificar a calibração das máquinas colhedoras\n")
                    arquivo.write("- Avaliar a velocidade de operação das colhedoras\n")
                    arquivo.write("- Verificar o treinamento dos operadores\n")
                elif media_eficiencia_mecanica > media_eficiencia_manual:
                    diferenca = media_eficiencia_mecanica - media_eficiencia_manual
                    arquivo.write(f"A colheita mecânica está {diferenca:.2f}% mais eficiente que a manual.\n")
                    arquivo.write("Recomendações:\n")
                    arquivo.write("- Avaliar os procedimentos da colheita manual\n")
                    arquivo.write("- Verificar o treinamento da equipe de campo\n")
                else:
                    arquivo.write("Ambos os métodos de colheita apresentam eficiência similar.\n")
                arquivo.write("\n")
            
            # Detalhes de cada registro
            arquivo.write("=" * 60 + "\n")
            arquivo.write("DETALHES DOS REGISTROS\n")
            arquivo.write("=" * 60 + "\n\n")
            
            for i, item in enumerate(dados, 1):
                arquivo.write(f"Registro #{i}\n")
                for chave, valor in item.items():
                    arquivo.write(f"{chave.capitalize()}: {valor}\n")
                arquivo.write("-" * 40 + "\n\n")
            
            arquivo.write("\n\nFim do relatório.")
        return True
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return False


def exportar_csv(dados, caminho_arquivo, cabecalho=None):
    """
    Exporta dados para um arquivo CSV
    
    Args:
        dados (list): Lista de dicionários com os dados
        caminho_arquivo (str): Caminho para salvar o arquivo CSV
        cabecalho (list, optional): Lista com os nomes das colunas
        
    Returns:
        bool: True se exportou com sucesso, False caso contrário
    """
    try:
        # Certifique-se de que o diretório existe
        diretorio = os.path.dirname(caminho_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
            
        # Se não houver dados, retorna
        if not dados:
            print("Nenhum dado para exportar.")
            return False
            
        # Se o cabeçalho não for fornecido, usa as chaves do primeiro dicionário
        if not cabecalho and isinstance(dados[0], dict):
            cabecalho = list(dados[0].keys())
            
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            # Escreve o cabeçalho
            if cabecalho:
                arquivo.write(','.join(cabecalho) + '\n')
                
            # Escreve os dados
            for item in dados:
                if isinstance(item, dict):
                    linha = ','.join(str(item.get(campo, '')) for campo in cabecalho)
                    arquivo.write(linha + '\n')
                else:
                    arquivo.write(','.join(str(valor) for valor in item) + '\n')
                    
        return True
    except Exception as e:
        print(f"Erro ao exportar para CSV: {e}")
        return False