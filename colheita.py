#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Monitoramento de Eficiência da Colheita de Cana
Modelo/Entidade Colheita
"""

from datetime import datetime
import re
from config import TIPOS_COLHEITA, LIMITES_TONELADAS

class Colheita:
    """Representa uma colheita de cana-de-açúcar"""
    
    def __init__(self, id_lote, tipo, data, previsto, colhido, obs="", eficiencia=None, perda=None):
        """
        Inicializa uma nova colheita
        
        Args:
            id_lote (str): Identificador único do lote
            tipo (str): Tipo de colheita ('manual' ou 'mecanica')
            data (str): Data da colheita no formato DD/MM/AAAA
            previsto (float): Quantidade prevista em toneladas
            colhido (float): Quantidade colhida em toneladas
            obs (str, optional): Observações sobre a colheita
            eficiencia (float, optional): Eficiência calculada
            perda (float, optional): Perda calculada
        """
        # Validações
        if not self._validar_id_lote(id_lote):
            raise ValueError("ID do lote inválido")
        
        if not self._validar_tipo(tipo):
            raise ValueError(f"Tipo de colheita inválido. Deve ser um dos seguintes: {', '.join(TIPOS_COLHEITA)}")
        
        if not self._validar_data(data):
            raise ValueError("Data inválida. Use o formato DD/MM/AAAA")
        
        if not self._validar_previsto(previsto):
            raise ValueError(f"Quantidade prevista inválida. Deve ser entre {LIMITES_TONELADAS[0]} e {LIMITES_TONELADAS[1]}")
        
        if not self._validar_colhido(colhido):
            raise ValueError(f"Quantidade colhida inválida. Deve ser entre {LIMITES_TONELADAS[2]} e {LIMITES_TONELADAS[3]}")
        
        # Atribuição
        self.id_lote = id_lote
        self.tipo = tipo.lower()
        self.data = data
        self.previsto = float(previsto)
        self.colhido = float(colhido)
        self.obs = obs
        
        # Calcular eficiência e perda se não fornecidos
        if eficiencia is None or perda is None:
            self._calcular_eficiencia()
        else:
            self.eficiencia = float(eficiencia)
            self.perda = float(perda)
    
    def _validar_id_lote(self, id_lote):
        """Valida o ID do lote"""
        return isinstance(id_lote, str) and id_lote.strip() != ""
    
    def _validar_tipo(self, tipo):
        """Valida o tipo de colheita"""
        return tipo.lower() in TIPOS_COLHEITA
    
    def _validar_data(self, data):
        """Valida se a data está no formato correto"""
        # Verifica se está no padrão DD/MM/AAAA
        padrao = re.compile(r'^\d{2}/\d{2}/\d{4}$')
        if not padrao.match(data):
            return False
        
        # Verifica se a data é válida
        try:
            dia, mes, ano = map(int, data.split('/'))
            datetime(ano, mes, dia)
            return True
        except ValueError:
            return False
    
    def _validar_previsto(self, previsto):
        """Valida a quantidade prevista"""
        try:
            valor = float(previsto)
            return LIMITES_TONELADAS[0] <= valor <= LIMITES_TONELADAS[1]
        except (ValueError, TypeError):
            return False
    
    def _validar_colhido(self, colhido):
        """Valida a quantidade colhida"""
        try:
            valor = float(colhido)
            return LIMITES_TONELADAS[2] <= valor <= LIMITES_TONELADAS[3]
        except (ValueError, TypeError):
            return False
    
    def _calcular_eficiencia(self):
        """Calcula a eficiência e perda da colheita"""
        if self.previsto <= 0:
            self.eficiencia = 0.0
            self.perda = 0.0
            return
        
        self.eficiencia = (self.colhido / self.previsto) * 100
        if self.eficiencia > 100:  # Se colheu mais do que o previsto
            self.eficiencia = 100.0
            self.perda = 0.0
        else:
            self.perda = 100 - self.eficiencia
        
        # Arredonda para 2 casas decimais
        self.eficiencia = round(self.eficiencia, 2)
        self.perda = round(self.perda, 2)
    
    def para_dict(self):
        """Converte o objeto para um dicionário"""
        return {
            'id_lote': self.id_lote,
            'tipo': self.tipo,
            'data': self.data,
            'previsto': self.previsto,
            'colhido': self.colhido,
            'eficiencia': self.eficiencia,
            'perda': self.perda,
            'obs': self.obs
        }
    
    @classmethod
    def de_dict(cls, dicionario):
        """Cria um objeto Colheita a partir de um dicionário"""
        return cls(
            id_lote=dicionario['id_lote'],
            tipo=dicionario['tipo'],
            data=dicionario['data'],
            previsto=dicionario['previsto'],
            colhido=dicionario['colhido'],
            obs=dicionario.get('obs', ''),
            eficiencia=dicionario.get('eficiencia'),
            perda=dicionario.get('perda')
        )
    
    def __str__(self):
        """Representação em string do objeto"""
        return (f"Colheita do Lote {self.id_lote} - {self.tipo.capitalize()} - {self.data}\n"
                f"Previsto: {self.previsto:.2f}t | Colhido: {self.colhido:.2f}t\n"
                f"Eficiência: {self.eficiencia:.2f}% | Perda: {self.perda:.2f}%")