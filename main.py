#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Monitoramento de Eficiência da Colheita de Cana
Módulo principal - Menu e interface com o usuário
"""

import os
import json
from datetime import datetime

# Estruturas de dados globais
colheitas = []  # Lista para armazenar colheitas em memória

# Definição de constantes
ARQUIVO_JSON = "dados/colheitas.json"
PASTA_RELATORIOS = "dados/relatorios"


# Função para limpar a tela (compatível com Windows e Unix)
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# Função para criar diretórios se não existirem
def criar_estrutura_diretorios():
    os.makedirs("dados", exist_ok=True)
    os.makedirs(PASTA_RELATORIOS, exist_ok=True)


# Função para calcular eficiência da colheita
def calcular_eficiencia(previsto, colhido):
    """
    Calcula a eficiência da colheita e o percentual de perda
    
    Args:
        previsto (float): Quantidade prevista em toneladas
        colhido (float): Quantidade colhida em toneladas
        
    Returns:
        tuple: (eficiencia, perda) ambos em percentual
    """
    if previsto <= 0:
        return 0.0, 0.0
    
    eficiencia = (colhido / previsto) * 100
    perda = 100 - eficiencia
    
    return round(eficiencia, 2), round(perda, 2)


# Funções para manipulação de arquivos JSON
def salvar_colheitas_json():
    """Salva a lista de colheitas em um arquivo JSON"""
    try:
        with open(ARQUIVO_JSON, 'w', encoding='utf-8') as arquivo:
            json.dump(colheitas, arquivo, indent=4, ensure_ascii=False)
        print("\n✅ Dados salvos com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao salvar dados: {e}")


def carregar_colheitas_json():
    """Carrega a lista de colheitas do arquivo JSON"""
    global colheitas
    try:
        if os.path.exists(ARQUIVO_JSON):
            with open(ARQUIVO_JSON, 'r', encoding='utf-8') as arquivo:
                colheitas = json.load(arquivo)
            print(f"📂 {len(colheitas)} colheitas carregadas do arquivo.")
        else:
            colheitas = []
            print("📂 Nenhum arquivo de dados encontrado. Iniciando novo registro.")
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        colheitas = []


# Função para validar entrada numérica
def validar_numero(mensagem, tipo=float):
    """Solicita e valida uma entrada numérica"""
    while True:
        try:
            valor = tipo(input(mensagem))
            return valor
        except ValueError:
            print("❌ Entrada inválida! Por favor, digite um número válido.")


# Função para validar entrada de data
def validar_data(mensagem):
    """Solicita e valida uma data no formato DD/MM/AAAA"""
    while True:
        data = input(mensagem)
        if not data:  # Se vazio, usa a data atual
            return datetime.now().strftime("%d/%m/%Y")
        
        try:
            # Tenta converter para verificar se é uma data válida
            datetime.strptime(data, "%d/%m/%Y")
            return data
        except ValueError:
            print("❌ Formato de data inválido! Use DD/MM/AAAA.")


# Função para registrar nova colheita
def registrar_colheita():
    """Solicita dados do usuário e registra uma nova colheita"""
    limpar_tela()
    print("\n===== REGISTRAR NOVA COLHEITA =====\n")
    
    # Coleta e validação de dados
    id_lote = input("Identificação do lote: ")
    
    # Verifica se o lote já existe
    for c in colheitas:
        if c['id_lote'] == id_lote:
            if input(f"Lote {id_lote} já existe! Sobrescrever? (s/n): ").lower() != 's':
                return
            # Remove o lote existente para sobrescrever
            colheitas.remove(c)
            break
    
    # Validação do tipo de colheita (usando tupla para os tipos válidos)
    tipos_validos = ('manual', 'mecanica')
    tipo = ''
    while tipo not in tipos_validos:
        tipo = input("Tipo de colheita (manual/mecanica): ").lower()
        if tipo not in tipos_validos:
            print("❌ Tipo inválido! Digite 'manual' ou 'mecanica'.")
    
    # Validação de dados numéricos
    previsto = validar_numero("Quantidade prevista (toneladas): ")
    colhido = validar_numero("Quantidade colhida (toneladas): ")
    
    # Validação de data
    data = validar_data("Data da colheita (DD/MM/AAAA) [Enter para hoje]: ")
    
    # Observações
    obs = input("Observações: ")
    
    # Cálculo da eficiência
    eficiencia, perda = calcular_eficiencia(previsto, colhido)
    
    # Cria um dicionário com os dados da colheita
    colheita = {
        'id_lote': id_lote,
        'tipo': tipo,
        'data': data,
        'previsto': previsto,
        'colhido': colhido,
        'eficiencia': eficiencia,
        'perda': perda,
        'obs': obs
    }
    
    # Adiciona à lista de colheitas
    colheitas.append(colheita)
    
    print(f"\n✅ Colheita registrada com sucesso!")
    print(f"Eficiência: {eficiencia}% | Perda: {perda}%")
    input("\nPressione Enter para continuar...")


# Função para listar colheitas
def listar_colheitas():
    """Exibe todas as colheitas registradas"""
    limpar_tela()
    print("\n===== COLHEITAS REGISTRADAS =====\n")
    
    if not colheitas:
        print("Nenhuma colheita registrada.")
        input("\nPressione Enter para continuar...")
        return
    
    # Uso de compreensão de lista para separar por tipo
    colheitas_manuais = [c for c in colheitas if c['tipo'] == 'manual']
    colheitas_mecanicas = [c for c in colheitas if c['tipo'] == 'mecanica']
    
    # Estatísticas gerais usando tuplas para armazenar contagens e médias
    total_manual = len(colheitas_manuais)
    total_mecanica = len(colheitas_mecanicas)
    
    media_eficiencia_manual = sum(c['eficiencia'] for c in colheitas_manuais) / total_manual if total_manual > 0 else 0
    media_eficiencia_mecanica = sum(c['eficiencia'] for c in colheitas_mecanicas) / total_mecanica if total_mecanica > 0 else 0
    
    estatisticas = (
        total_manual,
        total_mecanica,
        media_eficiencia_manual,
        media_eficiencia_mecanica
    )
    
    # Exibição dos dados
    print(f"Total de colheitas: {len(colheitas)}")
    print(f"Colheitas manuais: {estatisticas[0]} (Eficiência média: {estatisticas[2]:.2f}%)")
    print(f"Colheitas mecânicas: {estatisticas[1]} (Eficiência média: {estatisticas[3]:.2f}%)")
    print("\n" + "-" * 70)
    
    # Exibe cada colheita
    for i, c in enumerate(colheitas, 1):
        print(f"{i}. Lote: {c['id_lote']} | Tipo: {c['tipo']} | Data: {c['data']}")
        print(f"   Previsto: {c['previsto']}t | Colhido: {c['colhido']}t")
        print(f"   Eficiência: {c['eficiencia']}% | Perda: {c['perda']}%")
        if c['obs']:
            print(f"   Obs: {c['obs']}")
        print("-" * 70)
    
    input("\nPressione Enter para continuar...")


# Função para gerar relatório de texto
def gerar_relatorio_txt():
    """Gera um relatório em formato de texto"""
    limpar_tela()
    print("\n===== GERAR RELATÓRIO =====\n")
    
    if not colheitas:
        print("Nenhuma colheita registrada para gerar relatório.")
        input("\nPressione Enter para continuar...")
        return
    
    # Nome do arquivo com data e hora atual
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{PASTA_RELATORIOS}/relatorio_{agora}.txt"
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write("==================================================\n")
            arquivo.write("      RELATÓRIO DE EFICIÊNCIA DE COLHEITA DE CANA\n")
            arquivo.write(f"      Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            arquivo.write("==================================================\n\n")
            
            # Estatísticas gerais
            colheitas_manuais = [c for c in colheitas if c['tipo'] == 'manual']
            colheitas_mecanicas = [c for c in colheitas if c['tipo'] == 'mecanica']
            
            total_manual = len(colheitas_manuais)
            total_mecanica = len(colheitas_mecanicas)
            
            media_eficiencia_manual = sum(c['eficiencia'] for c in colheitas_manuais) / total_manual if total_manual > 0 else 0
            media_eficiencia_mecanica = sum(c['eficiencia'] for c in colheitas_mecanicas) / total_mecanica if total_mecanica > 0 else 0
            
            arquivo.write(f"RESUMO DAS COLHEITAS\n")
            arquivo.write(f"Total de registros: {len(colheitas)}\n")
            arquivo.write(f"Colheitas manuais: {total_manual}\n")
            arquivo.write(f"Colheitas mecânicas: {total_mecanica}\n\n")
            
            arquivo.write(f"EFICIÊNCIA\n")
            arquivo.write(f"Eficiência média total: {sum(c['eficiencia'] for c in colheitas) / len(colheitas):.2f}%\n")
            arquivo.write(f"Eficiência média (manual): {media_eficiencia_manual:.2f}%\n")
            arquivo.write(f"Eficiência média (mecânica): {media_eficiencia_mecanica:.2f}%\n")
            arquivo.write(f"Diferença de eficiência: {abs(media_eficiencia_manual - media_eficiencia_mecanica):.2f}%\n\n")
            
            arquivo.write("==================================================\n")
            arquivo.write("DETALHES DAS COLHEITAS\n")
            arquivo.write("==================================================\n\n")
            
            # Detalhes de cada colheita
            for i, c in enumerate(colheitas, 1):
                arquivo.write(f"Colheita #{i}\n")
                arquivo.write(f"Lote: {c['id_lote']}\n")
                arquivo.write(f"Tipo: {c['tipo'].capitalize()}\n")
                arquivo.write(f"Data: {c['data']}\n")
                arquivo.write(f"Previsto: {c['previsto']} toneladas\n")
                arquivo.write(f"Colhido: {c['colhido']} toneladas\n")
                arquivo.write(f"Eficiência: {c['eficiencia']}%\n")
                arquivo.write(f"Perda: {c['perda']}%\n")
                if c['obs']:
                    arquivo.write(f"Observações: {c['obs']}\n")
                arquivo.write("\n" + "-" * 50 + "\n\n")
            
            arquivo.write("\n\nFim do relatório.")
        
        print(f"✅ Relatório gerado com sucesso: {nome_arquivo}")
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
    
    input("\nPressione Enter para continuar...")


# Menu principal
def exibir_menu():
    """Exibe o menu principal do sistema"""
    limpar_tela()
    print("\n==== SISTEMA DE MONITORAMENTO DE EFICIÊNCIA DA COLHEITA DE CANA ====\n")
    print("1. Registrar nova colheita")
    print("2. Listar colheitas registradas")
    print("3. Gerar relatório (TXT)")
    print("4. Salvar dados (JSON)")
    print("5. Carregar dados (JSON)")
    print("6. Sair")
    print("\n" + "=" * 65)


# Função principal
def main():
    """Função principal do programa"""
    # Prepara a estrutura de diretórios
    criar_estrutura_diretorios()
    
    # Tenta carregar dados existentes
    carregar_colheitas_json()
    
    # Loop principal
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção (1-6): ")
        
        if opcao == '1':
            registrar_colheita()
        elif opcao == '2':
            listar_colheitas()
        elif opcao == '3':
            gerar_relatorio_txt()
        elif opcao == '4':
            salvar_colheitas_json()
            input("\nPressione Enter para continuar...")
        elif opcao == '5':
            carregar_colheitas_json()
            input("\nPressione Enter para continuar...")
        elif opcao == '6':
            print("\nSaindo do sistema... Até logo!")
            break
        else:
            print("\n❌ Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")


# Ponto de entrada do programa
if __name__ == "__main__":
    main()