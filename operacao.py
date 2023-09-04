import csv
import pandas as pd

def transforma_dados(df, cabecalho):
    df['Partida'] = '*P'
    df['Nº Documento'] = ''
    df['Conta de Contra Partida'] = ''
    df['Centro de Custo'] = df['Centro de Custo'].astype('string')
    df = df.dropna()
    # Use o método replace para substituir os pontos por vírgulas
    df['Valor'] = round(df['Valor'],2).astype(str).str.replace('.', ',')
    df = df[['Partida','Nº Documento','Conta de Débito','Conta de Crédito','Conta de Contra Partida','Valor','Código do Histórico','Complemento do Histórico','Filial','Centro de Custo']]

    dados = []
    for indice, linha in df.iterrows():
        lista_valores = linha.tolist()
        dados.append(lista_valores)

     # Nome do arquivo CSV que vamos salvar
    nome_do_arquivo = 'importacao.csv'

    # Escreva o cabeçalho no arquivo CSV
    with open(nome_do_arquivo, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv, delimiter=';')
        escritor_csv.writerow(cabecalho)

    # Abrir o arquivo novamente para adicionar os dados
    with open(nome_do_arquivo, 'a', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv, delimiter=';')
        escritor_csv.writerows(dados)
    return nome_do_arquivo