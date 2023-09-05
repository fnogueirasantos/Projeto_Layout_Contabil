import streamlit as st
import pandas as pd
import time
import operacao
import csv
import datetime

st.title('Formatação de Layout Contábil')

uploaded_file = st.file_uploader("Carregue o Arquivo:")
if uploaded_file is not None:
    try:
        df_opcoes = pd.read_excel(uploaded_file,dtype={'Centro de Custo': str})
        st.write('Dados Carregados com Sucesso!!')
    except Exception as e:
        st.error(f"Erro ao carregar os dados!!")
    time.sleep(1)

if uploaded_file is not None:
    df_opcoes = pd.read_excel(uploaded_file,dtype={'Centro de Custo': str})
    opcoes = sorted(list(df_opcoes['Coligada'].unique()))
    opcao_coligada = st.selectbox('Selecione a Coligada',(opcoes))
    st.subheader('Definições de Cabeçalho do Arquivo')
    number = st.number_input('Código do Lote', value = 2023, key='int')
    title = st.text_input('Título do Lançamento', 'Importação de lançamento contábil manual')
    select_data = st.date_input("Data de Inclusão:")
    # Verifique se a data foi selecionada
    if select_data:
        data_formatada = select_data.strftime("%d/%m/%Y")
    cabecalho = ['M', number, title, data_formatada]
    st.text(f"Coligada Selecionada: {opcao_coligada}")
    st.text(f"Cabeçalho: {cabecalho}")
    try:
        df_filtro = pd.read_excel(uploaded_file,dtype={'Centro de Custo': str})
        df_filtro = df_filtro.query(f'Coligada == {opcao_coligada}')
        df = operacao.transforma_dados(df_filtro,cabecalho)
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
else:
    pass
if uploaded_file is not None:
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