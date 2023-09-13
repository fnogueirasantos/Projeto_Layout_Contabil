import csv
import zipfile
import os
import warnings
warnings.filterwarnings("ignore")

def transforma_dados_e_cria_zip(df,cabecalho):
    df = df.dropna()
    df['Partida'] = '*P'
    df['Centro de Custo'] = df['Centro de Custo'].astype('str')
    df['Nº Documento'] = ''
    df['Conta de Contra Partida'] = ''
    df['Coligada'] = df['Coligada'].astype('int')
    df['Filial'] = df['Filial'].astype('int')
    df['Código do Histórico'] = df['Código do Histórico'].astype('int')
    # Use o método replace para substituir os pontos por vírgulas
    df['Valor'] = df['Valor'].map('{:.2f}'.format).str.replace('.', ',')

    df = df[['Coligada','Partida','Nº Documento','Conta de Débito','Conta de Crédito','Conta de Contra Partida','Valor','Código do Histórico','Complemento do Histórico','Filial','Centro de Custo']]
    
    coligadas = sorted(list(df['Coligada'].unique()))
    
    # Criar um arquivo ZIP para salvar os CSVs
    with zipfile.ZipFile('dados.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for x in coligadas:
            df_filtrado = df[df['Coligada'] == x].copy()  # Crie uma cópia do DataFrame filtrado
            df_filtrado.drop(columns=['Coligada'], inplace=True)
            dados = []
            for indice, linha in df_filtrado.iterrows():
                lista_valores = linha.tolist()
                dados.append(lista_valores)

            # Nome do arquivo CSV que vamos salvar
            nome_do_arquivo = f'Col{x}' + '_import.csv'

            # Escreva o cabeçalho no arquivo CSV
            with open(nome_do_arquivo, 'w', newline='') as arquivo_csv:
                escritor_csv = csv.writer(arquivo_csv, delimiter=';')
                escritor_csv.writerow(cabecalho)

            # Abrir o arquivo novamente para adicionar os dados
            with open(nome_do_arquivo, 'a', newline='') as arquivo_csv:
                escritor_csv = csv.writer(arquivo_csv, delimiter=';')
                escritor_csv.writerows(dados)
            
            # Adicione o arquivo CSV ao arquivo ZIP
            zipf.write(nome_do_arquivo, arcname=nome_do_arquivo)
            
    return 'dados.zip'  # Retorna o nome do arquivo ZIP gerado

def transforma_dados(df, cabecalho):
    df['Partida'] = '*P'
    df['Nº Documento'] = ''
    df['Conta de Contra Partida'] = ''
    df['Centro de Custo'] = df['Centro de Custo'].astype('string')
    df = df.dropna()
    # Use o método replace para substituir os pontos por vírgulas
    df['Valor'] = df['Valor'].map('{:.2f}'.format).str.replace('.', ',')
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
