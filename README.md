# PlanetAPI

API REST para manipulação de dados dos planetas do filme Star Wars.

# Requisitos
- Python 3.6+
- DynamoDB

# Rodando a aplicação

1. Baixar o projeto do repositório:
    ```
    git clone https://github.com/schirley-jorge/PlanetAPI.git
    ```
2. No arquivo **run_application.sh** colocar as credenciais da AWS:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
3. Executar o script **run_application.sh**:
    ```
    . ./run_application.sh
    ```
    
# Rodando os testes unitários

1. No arquivo **run_unit_tests.sh** colocar as credenciais da AWS:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
2. Executar o script **run_unit_tests.sh**:
    ```
    . ./run_application.sh
    ```
    
# Como usar

Descrição da API: [https://app.swaggerhub.com/apis/schirley.jorge/PlanetAPI/1.0.0#/]

# Arquivos fonte da aplicação:
    - main_handler.py
    - db_connection.py
    - swapi_connection.py
