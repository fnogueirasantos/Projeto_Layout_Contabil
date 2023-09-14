import streamlit as st
import pandas as pd
import time
import operacao
import csv
import datetime
import os
import warnings
warnings.filterwarnings("ignore")
# Defina a variável de ambiente PYTHONUTF8 para o encoding padrão UTF-8
os.environ["PYTHONUTF8"] = "1"

st.title('Layout de Importação Contábil')

# Crie um expander com um rótulo
with st.expander("IMPOSTOS"):
    st.makdown("[Modelo Excel de Impostos](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Ffnogueirasantos%2FProjeto_Layout_Contabil%2Fmain%2FLayout_Geral.xlsx&wdOrigin=BROWSELINK)")
    uploaded_file = st.file_uploader("Carregue o Arquivo:",key="impostos")

if uploaded_file is not None:
    try:
        df_opcoes = pd.read_excel(uploaded_file,dtype={'Centro de Custo': str})
        st.write('Dados Carregados com Sucesso!!')
    except Exception as e:
        st.error(f"Erro ao carregar os dados!!")
    time.sleep(1)
    opcao_sheet = st.selectbox('Selecione o Conceito:',('1º Conceito', '2º Conceito','3º Conceito'))
    st.subheader('Definições de Cabeçalho do Arquivo')
    number = st.number_input('Código do Lote', value = 2023, key='int')
    title = st.text_input('Título do Lançamento', 'Importacao de lancamento contabil manual')
    select_data = st.date_input("Data de Inclusão:")
    # Verifique se a data foi selecionada
    if select_data:
        data_formatada = select_data.strftime("%d/%m/%Y")
    cabecalho = ['M', number, title, data_formatada]
    st.text(f"Cabeçalho: {cabecalho}")
    if st.button("Transformar Dados"):
        try:
            # Mostra o spinner enquanto os dados estão sendo carregados e processados
            with st.spinner("Processando os dados..."):
                time.sleep(4)
                df_filtro = pd.read_excel(uploaded_file, dtype={'Centro de Custo': str}, sheet_name=f'{opcao_sheet}')
                zip_file_path = operacao.transforma_dados_e_cria_zip(df_filtro, cabecalho)
        except Exception as e:
            st.error(f"Erro ao carregar os dados: {e}")
        else:
            # Use a função st.download_button para permitir o download do arquivo ZIP
            with open(zip_file_path, 'rb') as f:
                zip_data = f.read()
            st.download_button(
                label="Clique para baixar o arquivo ZIP",
                data=zip_data,
                key="dados_download.zip",
                file_name=f"Import_{opcao_sheet}.zip",
                mime="application/zip"
            )
else:
    pass

st.divider()


with st.expander("LAYOUT GERAL"):
    st.makdown("[Modelo Excel de Impostos](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Ffnogueirasantos%2FProjeto_Layout_Contabil%2Fmain%2FLayout_Geral.xlsx&wdOrigin=BROWSELINK)")
    uploaded_file2 = st.file_uploader("Carregue o Arquivo:",key="geral")

    if uploaded_file2 is not None:
        try:
            df_opcoes = pd.read_excel(uploaded_file2,dtype={'Centro de Custo': str})
            st.write('Dados Carregados com Sucesso!!')
        except Exception as e:
            st.error(f"Erro ao carregar os dados!!")
        time.sleep(1)
        opcoes = sorted(list(df_opcoes['Coligada'].unique()))
        opcao_coligada = st.selectbox('Selecione a Coligada',(opcoes))
        st.subheader('Definições de Cabeçalho do Arquivo')
        number = st.number_input('Código do Lote', value = 2023, key='int')
        title = st.text_input('Título do Lançamento', 'Importacao de lancamento contabil manual')
        select_data = st.date_input("Data de Inclusão:")
        # Verifique se a data foi selecionada
        if select_data:
            data_formatada = select_data.strftime("%d/%m/%Y")
        cabecalho = ['M', number, title, data_formatada]
        st.text(f"Coligada Selecionada: {opcao_coligada}")
        st.text(f"Cabeçalho: {cabecalho}")
        try:
            df_filtro = pd.read_excel(uploaded_file2,dtype={'Centro de Custo': str})
            df_filtro = df_filtro.query(f'Coligada == {opcao_coligada}')
            df = operacao.transforma_dados(df_filtro,cabecalho)
        except Exception as e:
            st.error(f"Erro ao carregar os dados: {e}")
    else:
        pass
    if uploaded_file2 is not None:
        if st.button('Gerar Layout de Importação') and df is not None:
            with st.spinner('Transformação de dados em Progresso...'):
                try:
                    time.sleep(3)
                    st.success('Feito! O Layout está pronto para Download.')
                except Exception as e:
                    st.error(f"Erro durante a transformação dos dados: {e}")
            if df is not None:
                st.download_button(
                    label="Download data as CSV",
                    data=open(df, 'rb').read(),
                    file_name=f'import_Colig_{opcao_coligada}.csv',
                    mime='text/csv',
                )