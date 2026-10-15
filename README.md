# Transporte Saúde

Sistema web para gerenciamento de viagens de transporte de saúde, desenvolvido com Python, Flask e SQLite.

## Sobre o projeto

O Transporte Saúde é meu primeiro projeto pessoal, desenvolvido a partir de uma necessidade identificada no meu ambiente de trabalho. Seu objetivo é facilitar a organização e o acompanhamento das viagens, centralizando informações sobre motoristas, veículos, hospitais e agendamentos em uma única aplicação.

O projeto surgiu como uma oportunidade de aplicar conhecimentos de programação e banco de dados na resolução de um problema prático, buscando tornar os processos de registro e consulta de informações mais organizados.

Atualmente, curso Análise e Desenvolvimento de Sistemas e estou no segundo trimestre. O desenvolvimento deste sistema faz parte da minha evolução como desenvolvedor, permitindo consolidar conhecimentos e adquirir experiência prática na construção de aplicações web.

## Funcionalidades

- **Gerenciamento de motoristas:** cadastro com nome, CNH, categoria da habilitação e telefone.
- **Gerenciamento de veículos:** cadastro de tipo, ano, placa e capacidade de passageiros.
- **Cadastro de hospitais e clínicas:** armazenamento de código, nome, cidade, telefone, endereço e tipo.
- **Agendamento de viagens:** registro de data, horário de saída, ponto de partida, destino, hospital relacionado e observações.
- **Próximas viagens:** consulta dos deslocamentos agendados, organizados por data e horário.
- **Histórico de viagens:** consulta das viagens anteriores.
- **Impressão de viagens:** visualização das informações em uma página preparada para impressão.
- **Arquivamento de cadastros:** desativação de motoristas, veículos e hospitais sem a exclusão direta dos registros.
- **Persistência de dados:** armazenamento das informações em um banco de dados SQLite.

## Tecnologias utilizadas

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Implementação da lógica e das funcionalidades |
| Flask | Desenvolvimento das rotas e integração com a interface web |
| SQLite | Armazenamento e gerenciamento dos dados |
| SQL | Consultas e operações no banco de dados |
| HTML | Estrutura das páginas da aplicação |
| Git e GitHub | Controle de versão e hospedagem do código-fonte |

## Estrutura do projeto

```text
transporte-saude/
├── app.py
├── funcoes.py
├── database/
│   └── projeto_viagens.db
├── templates/
│   ├── index.html
│   ├── cadastrar_hospital.html
│   ├── cadastrar_motorista.html
│   ├── cadastrar_veiculo.html
│   ├── cadastrar_viagem.html
│   ├── historico_viagens.html
│   └── imprimir_viagens.html
├── .gitignore
└── README.md
```

### Organização do código

- `app.py`: define as rotas da aplicação Flask, recebe os dados dos formulários, realiza operações no banco de dados e conecta a lógica à interface.
- `funcoes.py`: reúne funções para cadastro, consulta e gerenciamento dos registros.
- `database/projeto_viagens.db`: banco de dados SQLite utilizado pela aplicação.
- `templates/`: contém os arquivos HTML responsáveis pelas páginas e formulários do sistema.

## Como executar localmente

### Pré-requisitos

- Python instalado.
- Git instalado.

### 1. Clonar o repositório

```bash
git clone https://github.com/jpedrocamposdev/transporte-saude.git
cd transporte-saude
```

### 2. Criar um ambiente virtual

No Windows, execute:

```powershell
python -m venv .venv
```

### 3. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar o Flask

```powershell
python -m pip install Flask
```

### 5. Executar a aplicação

Com o ambiente virtual ativado e o banco de dados disponível no caminho esperado pelo código, execute:

```powershell
python app.py
```

Acesse a aplicação pelo navegador:

http://127.0.0.1:5000

**Observação:** o banco de dados disponibilizado no repositório é destinado à demonstração e deve conter apenas dados fictícios. Recomenda-se manter uma cópia local antes de realizar testes que alterem ou excluam registros.

## Desenvolvimento e uso de inteligência artificial

A lógica da aplicação, incluindo as funcionalidades implementadas em `app.py` e `funcoes.py`, foi desenvolvida por mim como parte do meu processo de aprendizado em Python, Flask e SQLite.

Para a criação dos templates HTML, utilizei o auxílio do modelo Gemini 3.6, pois ainda não havia estudado essa parte do desenvolvimento web em profundidade. O auxílio da ferramenta permitiu avançar na construção da interface enquanto continuo desenvolvendo meus conhecimentos nessa área.

O objetivo é compreender progressivamente todas as partes do sistema, aprimorando tanto a lógica da aplicação quanto a interface e sua estrutura interna.

## Melhorias futuras

Como projeto em desenvolvimento, algumas melhorias que pretendo explorar são:

- Implementação de autenticação e controle de acesso.
- Aprimoramento da validação dos dados.
- Desenvolvimento de testes automatizados.
- Melhoria no tratamento de erros.
- Implementação de filtros e recursos de pesquisa.
- Evolução da interface e da experiência de uso.
- Aprimoramento dos procedimentos de backup e integridade do banco de dados.

## Autor

**jpedrocamposdev**

Estudante de Análise e Desenvolvimento de Sistemas — segundo trimestre.

GitHub: [@jpedrocamposdev](https://github.com/jpedrocamposdev)

---

Projeto pessoal desenvolvido com foco no aprendizado prático e na aplicação da programação para resolver necessidades do cotidiano profissional.
