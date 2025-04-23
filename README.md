# 🌱 Sistema de Monitoramento de Eficiência da Colheita de Cana

## 👨‍🎓 Integrantes:
* DAVI ALVES ROCHA
* DANIEL CAFFE ALVES
* LARISSA DUARTE DOS SANTOS
* BRENDA MATOS SANTOS
* JULIANO SOUZA AMARO

## 📜 Descrição

O Brasil é líder mundial na produção de cana-de-açúcar, no entanto, enfrenta um problema crítico relacionado às perdas durante o processo de colheita. Pesquisas mostram que enquanto a colheita manual apresenta perdas de aproximadamente 5%, a colheita mecanizada pode chegar a perdas de até 15%. Essas perdas representam prejuízos significativos, estimados em cerca de R$20 milhões por ano para o setor.

Para pequenos e médios produtores de cana-de-açúcar, o monitoramento e análise dessas perdas é fundamental para garantir a rentabilidade do negócio. Entretanto, muitos produtores não têm acesso a ferramentas tecnológicas que permitam esse controle de forma simples e eficaz.

Nossa solução consiste em um sistema de monitoramento de eficiência de colheita que permite ao produtor registrar dados de colheitas (manuais e mecânicas), calcular automaticamente os percentuais de eficiência e perda, comparar o desempenho entre os diferentes métodos, e gerar relatórios analíticos que auxiliam na tomada de decisão.

O sistema foi desenvolvido com foco na usabilidade e acessibilidade, permitindo que produtores com conhecimento básico de informática possam utilizá-lo sem dificuldades. Além disso, a integração com banco de dados Oracle garante a persistência e segurança das informações.

A inovação do nosso projeto está na capacidade de oferecer uma solução tecnológica completa e integrada, porém simples e direta, que atende às necessidades específicas do setor de produção de cana-de-açúcar, contribuindo para a redução de perdas e o aumento da rentabilidade dos produtores.

## 📁 Estrutura de pastas

A estrutura atual do projeto é:

```
farmtech-2/
├── dados/                # Diretório para armazenamento de dados
│   ├── relatorios/       # Relatórios gerados em formato TXT
│   │   └── relatorio_*.txt
│   └── colheitas.json    # Dados persistentes em JSON
├── colheita.py           # Modelo/Entidade de colheita
├── colheita_service.py   # Serviço para operações com colheitas
├── config.py             # Configurações do sistema
├── db_service.py         # Serviço para operações com banco Oracle
├── main.py               # Programa principal (controlador)
├── README.md             # Este arquivo
├── teste_conexao.py      # Script para testar conexão com Oracle
└── utils.py              # Funções utilitárias
```

## 🔧 Como executar o código

### Pré-requisitos

* Python 3.6 ou superior
* Conexão com Internet (para acessar o banco Oracle da FIAP)

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-colheita-cana.git
   cd sistema-colheita-cana
   ```

2. Instale as dependências:
   ```bash
   pip install oracledb
   ```

3. Configure o acesso ao banco Oracle (se necessário):
   * Edite o arquivo `src/config.py` com suas credenciais

### Execução

1. Execute o programa principal:
   ```bash
   python main.py
   ```

2. No primeiro uso:
   * Selecione a opção 6 para testar a conexão com Oracle
   * Se a conexão estiver ok, selecione a opção 7 para criar a tabela no Oracle

3. Use o menu interativo para:
   * Registrar novas colheitas (opção 1)
   * Visualizar colheitas existentes (opção 2)
   * Gerar relatórios (opção 3)
   * Salvar/carregar dados (opções 4-5)
   * Operações com Oracle (opções 6-9)

## 🧮 Regras de Negócio

1. **Tipos de Colheita**:
   * **Manual**: Tipicamente com perdas de até 5%
   * **Mecânica**: Tipicamente com perdas de até 15%

2. **Cálculo de Eficiência e Perda**:
   * Eficiência (%) = (Quantidade Colhida / Quantidade Prevista) × 100
   * Perda (%) = 100 - Eficiência

3. **Limitações de Dados**:
   * Quantidade prevista mínima: 0.1 toneladas
   * Quantidade máxima: 10.000 toneladas
   * Identificação única para cada lote (não permite duplicatas)

## 🧠 Tecnologias Utilizadas

* Python 3.x
* Oracle Database (via fiap)
* Estruturas de dados: listas, tuplas, dicionários
* Manipulação de arquivos JSON e TXT
* Programação orientada a objetos

## 🔍 Funcionalidades

* Registro de colheitas com validação de dados
* Cálculo automático de eficiência e perdas
* Comparação entre colheita manual e mecânica
* Geração de relatórios analíticos
* Armazenamento persistente usando JSON e Oracle Database
* Interface via linha de comando

---

Desenvolvido como parte da atividade prática de integração Python e Banco de Dados aplicados ao Agronegócio - FIAP 2025.