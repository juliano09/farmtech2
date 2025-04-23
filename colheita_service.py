#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Monitoramento de Eficiência da Colheita de Cana
Serviço para operações com colheitas
"""

import json
import os
import re
from datetime import datetime

from colheita import Colheita
from config import ARQUIVO_JSON, TIPOS_COLHEITA, obter_caminho_relatorio

class ColheitaService:
    """Serviço para gerenciar operações de colheitas"""
    
    def __init__(self):
        """Inicializa o serviço"""
        self.colheitas = []
    
    def adicionar_colheita(self, colheita):
        """
        Adiciona uma colheita à lista
        
        Args:
            colheita (Colheita): A colheita a ser adicionada
            
        Returns:
            bool: True se adicionou com sucesso, False se já existe uma colheita com o mesmo ID
        """
        # Verifica se já existe uma colheita com o mesmo ID
        for i, c in enumerate(self.colheitas):
            if c.id_lote == colheita.id_lote:
                # Substitui a colheita existente
                self.colheitas[i] = colheita
                return True
        
        # Adiciona nova colheita
        self.colheitas.append(colheita)
        return True
    
    def remover_colheita(self, id_lote):
        """
        Remove uma colheita da lista
        
        Args:
            id_lote (str): ID do lote a ser removido
            
        Returns:
            bool: True se removeu com sucesso, False se não encontrou
        """
        for i, c in enumerate(self.colheitas):
            if c.id_lote == id_lote:
                del self.colheitas[i]
                return True
        
        return False
    
    def obter_colheita(self, id_lote):
        """
        Busca uma colheita pelo ID do lote
        
        Args:
            id_lote (str): ID do lote a ser buscado
            
        Returns:
            Colheita: A colheita encontrada ou None se não encontrar
        """
        for c in self.colheitas:
            if c.id_lote == id_lote:
                return c
        
        return None
    
    def listar_colheitas(self):
        """
        Lista todas as colheitas
        
        Returns:
            list: Lista de objetos Colheita
        """
        return self.colheitas
    
    def calcular_estatisticas(self):
        """
        Calcula estatísticas das colheitas
        
        Returns:
            dict: Dicionário com estatísticas
        """
        if not self.colheitas:
            return {
                'total': 0,
                'manual': {'total': 0, 'eficiencia_media': 0},
                'mecanica': {'total': 0, 'eficiencia_media': 0},
                'diferenca': 0,
                'recomendacoes': ['Não há dados suficientes para análise.']
            }
        
        # Separar colheitas por tipo
        colheitas_manuais = [c for c in self.colheitas if c.tipo == 'manual']
        colheitas_mecanicas = [c for c in self.colheitas if c.tipo == 'mecanica']
        
        # Calcular médias
        efic_manual = sum(c.eficiencia for c in colheitas_manuais) / len(colheitas_manuais) if colheitas_manuais else 0
        efic_mecanica = sum(c.eficiencia for c in colheitas_mecanicas) / len(colheitas_mecanicas) if colheitas_mecanicas else 0
        
        # Diferença entre tipos
        diferenca = abs(efic_manual - efic_mecanica)
        
        # Gerar recomendações
        recomendacoes = []
        if colheitas_manuais and colheitas_mecanicas:
            if efic_manual > efic_mecanica:
                recomendacoes.append(f"A colheita manual está {diferenca:.2f}% mais eficiente que a mecânica.")
                recomendacoes.append("Verifique a calibração das máquinas colhedoras.")
                recomendacoes.append("Revise o treinamento dos operadores.")
            elif efic_mecanica > efic_manual:
                recomendacoes.append(f"A colheita mecânica está {diferenca:.2f}% mais eficiente que a manual.")
                recomendacoes.append("Analise os procedimentos da colheita manual.")
                recomendacoes.append("Considere treinar melhor a equipe de campo.")
            else:
                recomendacoes.append("Ambos os métodos de colheita apresentam eficiência similar.")
        elif colheitas_manuais:
            recomendacoes.append("Existem apenas registros de colheita manual. Considere registrar colheitas mecânicas para comparação.")
        elif colheitas_mecanicas:
            recomendacoes.append("Existem apenas registros de colheita mecânica. Considere registrar colheitas manuais para comparação.")
        
        # Retornar estatísticas
        return {
            'total': len(self.colheitas),
            'manual': {
                'total': len(colheitas_manuais),
                'eficiencia_media': round(efic_manual, 2)
            },
            'mecanica': {
                'total': len(colheitas_mecanicas),
                'eficiencia_media': round(efic_mecanica, 2)
            },
            'diferenca': round(diferenca, 2),
            'recomendacoes': recomendacoes
        }
    
    def salvar_json(self):
        """
        Salva as colheitas em um arquivo JSON
        
        Returns:
            bool: True se salvou com sucesso, False caso contrário
        """
        try:
            # Certifique-se de que o diretório existe
            os.makedirs(os.path.dirname(ARQUIVO_JSON), exist_ok=True)
            
            # Converte colheitas para dicionários
            dados = [c.para_dict() for c in self.colheitas]
            
            with open(ARQUIVO_JSON, 'w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar arquivo JSON: {e}")
            return False
    
    def carregar_json(self):
        """
        Carrega colheitas do arquivo JSON
        
        Returns:
            bool: True se carregou com sucesso, False caso contrário
        """
        try:
            if not os.path.exists(ARQUIVO_JSON):
                return False
            
            with open(ARQUIVO_JSON, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            
            # Converte dicionários para objetos Colheita
            self.colheitas = [Colheita.de_dict(d) for d in dados]
            
            return True
        except Exception as e:
            print(f"Erro ao carregar arquivo JSON: {e}")
            return False
    
    def gerar_relatorio(self):
        """
        Gera um relatório das colheitas
        
        Returns:
            str: Caminho do arquivo gerado ou None em caso de erro
        """
        caminho_relatorio = obter_caminho_relatorio()
        
        try:
            # Certifique-se de que o diretório existe
            os.makedirs(os.path.dirname(caminho_relatorio), exist_ok=True)
            
            with open(caminho_relatorio, 'w', encoding='utf-8') as arquivo:
                arquivo.write("==================================================\n")
                arquivo.write("      RELATÓRIO DE EFICIÊNCIA DE COLHEITA DE CANA\n")
                arquivo.write(f"      Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                arquivo.write("==================================================\n\n")
                
                # Se não houver colheitas, informa no relatório
                if not self.colheitas:
                    arquivo.write("Nenhuma colheita registrada para gerar relatório.\n")
                    return caminho_relatorio
                
                # Estatísticas
                estatisticas = self.calcular_estatisticas()
                
                arquivo.write(f"RESUMO DAS COLHEITAS\n")
                arquivo.write(f"Total de registros: {estatisticas['total']}\n")
                arquivo.write(f"Colheitas manuais: {estatisticas['manual']['total']}\n")
                arquivo.write(f"Colheitas mecânicas: {estatisticas['mecanica']['total']}\n\n")
                
                arquivo.write(f"EFICIÊNCIA\n")
                
                media_geral = sum(c.eficiencia for c in self.colheitas) / len(self.colheitas) if self.colheitas else 0
                
                arquivo.write(f"Eficiência média total: {media_geral:.2f}%\n")
                arquivo.write(f"Eficiência média (manual): {estatisticas['manual']['eficiencia_media']}%\n")
                arquivo.write(f"Eficiência média (mecânica): {estatisticas['mecanica']['eficiencia_media']}%\n")
                arquivo.write(f"Diferença de eficiência: {estatisticas['diferenca']}%\n\n")
                
                arquivo.write("RECOMENDAÇÕES\n")
                for rec in estatisticas['recomendacoes']:
                    arquivo.write(f"- {rec}\n")
                arquivo.write("\n")
                
                arquivo.write("==================================================\n")
                arquivo.write("DETALHES DAS COLHEITAS\n")
                arquivo.write("==================================================\n\n")
                
                # Detalhes de cada colheita
                for i, c in enumerate(self.colheitas, 1):
                    arquivo.write(f"Colheita #{i}\n")
                    arquivo.write(f"Lote: {c.id_lote}\n")
                    arquivo.write(f"Tipo: {c.tipo.capitalize()}\n")
                    arquivo.write(f"Data: {c.data}\n")
                    arquivo.write(f"Previsto: {c.previsto} toneladas\n")
                    arquivo.write(f"Colhido: {c.colhido} toneladas\n")
                    arquivo.write(f"Eficiência: {c.eficiencia}%\n")
                    arquivo.write(f"Perda: {c.perda}%\n")
                    if c.obs:
                        arquivo.write(f"Observações: {c.obs}\n")
                    arquivo.write("\n" + "-" * 50 + "\n\n")
                
                arquivo.write("\n\nFim do relatório.")
            
            return caminho_relatorio
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            return None

    # Métodos auxiliares para validação de entrada
    @staticmethod
    def validar_entrada_numerica(mensagem, minimo=None, maximo=None, tipo=float):
        """
        Solicita e valida uma entrada numérica do usuário
        
        Args:
            mensagem (str): Mensagem a ser exibida
            minimo (numeric, optional): Valor mínimo aceitável
            maximo (numeric, optional): Valor máximo aceitável
            tipo (type, optional): Tipo do valor (int ou float)
            
        Returns:
            numeric: Valor validado
        """
        while True:
            try:
                valor = tipo(input(mensagem))
                
                if minimo is not None and valor < minimo:
                    print(f"Valor deve ser maior ou igual a {minimo}.")
                    continue
                    
                if maximo is not None and valor > maximo:
                    print(f"Valor deve ser menor ou igual a {maximo}.")
                    continue
                    
                return valor
            except ValueError:
                print("Valor inválido. Digite um número.")

    @staticmethod
    def validar_entrada_data(mensagem, obrigatorio=False):
        """
        Solicita e valida uma entrada de data do usuário
        
        Args:
            mensagem (str): Mensagem a ser exibida
            obrigatorio (bool): Se True, não aceita valor vazio
            
        Returns:
            str: Data validada ou data atual se vazio e não obrigatório
        """
        while True:
            entrada = input(mensagem)
            
            if not entrada:
                if obrigatorio:
                    print("Data é obrigatória.")
                    continue
                return datetime.now().strftime("%d/%m/%Y")
                
            # Verifica se está no padrão DD/MM/AAAA
            padrao = re.compile(r'^\d{2}/\d{2}/\d{4}$')
            if not padrao.match(entrada):
                print("Formato de data inválido. Use DD/MM/AAAA.")
                continue
                
            # Verifica se a data é válida
            try:
                dia, mes, ano = map(int, entrada.split('/'))
                datetime(ano, mes, dia)
                return entrada
            except ValueError:
                print("Data inválida. Verifique dia, mês e ano.")

    @staticmethod
    def validar_entrada_tipo_colheita(mensagem):
        """
        Solicita e valida o tipo de colheita
        
        Args:
            mensagem (str): Mensagem a ser exibida
            
        Returns:
            str: Tipo de colheita validado
        """
        while True:
            tipo = input(mensagem).lower()
            if tipo in TIPOS_COLHEITA:
                return tipo
            else:
                print(f"Tipo inválido. Opções: {', '.join(TIPOS_COLHEITA)}")