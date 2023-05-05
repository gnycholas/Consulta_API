import csv
import json
import urllib.request

# URL base dconsulta
api_url = 'insira a URL aqui'

# Função para consulta
def consulta_cnpj(cnpj):
    # Constrói a URL completaa ser consultado
    request_url = api_url

    # Configura o cabeçalho da requisição com um User-Agent para evitar problemas de bloqueio
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    # Cria e envia a requisição HTTP para a API BrasilAPI
    req = urllib.request.Request(request_url, headers=headers)

    # Processa a resposta HTTP
    with urllib.request.urlopen(req) as response:
        # Carrega os dados JSON da resposta
        data = json.loads(response.read().decode('utf-8'))

    # Retorna um dicionário com as informações desejadas (CNPJ, UF e município)
    return {
        'campo': data.get('campo_da_base'),
    }

# Abre o arquivo CSV com a lista de CNPJs para consulta
with open('cnpjs.csv') as csvfile:
    cnpj_reader = csv.reader(csvfile)
    
    # Pula o cabeçalho, se houver
    next(cnpj_reader)

    # Cria um novo arquivo CSV para salvar os resultados
    with open('resultado.csv', 'w', newline='') as result_file:
        # Define os campos (colunas) do arquivo de resultados
        fieldnames = ['campos']
        
        # Cria um objeto DictWriter para escrever no arquivo de resultados
        writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        
        # Escreve o cabeçalho no arquivo de resultados
        writer.writeheader()

        # Itera sobre cada CNPJ no arquivo de entrada
        for row in cnpj_reader:
            # Extrai o CNPJ da linha atual
            cnpj = row[0].strip()

            # Tenta consultar a requisição na API
            try:
                resultado = consulta()
                
                # Escreve o resultado no arquivo de resultados
                writer.writerow(resultado)
                
                # Exibe uma mensagem de sucesso
                print(f"Consulta realizada com sucesso para o CNPJ: {cnpj}")
            except Exception as e:
                # Exibe uma mensagem de erro, caso ocorra algum problema
                print(f"Erro ao consultar CNPJ {cnpj}: {e}")
                               