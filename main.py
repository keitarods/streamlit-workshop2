import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from plotly import graph_objects as go

#Carregar variaveis de ambiente
load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

def connect_to_db():
    """
    Função pra conectar ao banco de dados

    """

    engine = create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
                           )
    
    return engine

def run_query(query, engine):
    with engine.connect() as conn:
        return pd.read_sql(query, conn)
    
def create_plot(df, plot_type):
    if plot_type == "bar":
        return go.Figure(data=[go.Bar(x=df["titulo"], y=df["preco"])])
    elif plot_type == "line":
        return go.Figure(data=[go.Scatter(x=df.index, y=df["preco"], mode="lines+markers")])
    elif plot_type == "scatter":
        return go.Figure(data=[go.Scatter(x=df["titulo"], y=df["preco"], mode="markers")])
    elif plot_type =="pie":
        return go.Figure(data=[go.Pie(x=df["titulo"], y=df["preco"])])
    
    #Adicione outros tipos de gráficos conforme for necessário

def main():
    st.title("Dashboard de Preço de Livros")

    engine = connect_to_db()
    query = "SELECT DISTINCT titulo, preco FROM produtos ORDER BY preco DESC"
    df = run_query(query,engine)

    st.write("Produtos:")
    st.dataframe(df)

    uploaded_files = st.file_uploader("Carregar arquivo Excel", type="xslx")
    if uploaded_files is not None:
        excel_data = pd.read_excel(uploaded_files)
        df = pd.concat([df, excel_data]) #"Combinar com dados do banco"
        df = df.nlargest(5,"preco") #Atualizar o dataframe para top 5 apos concatenação

    st.write("Top 5 produtos (atualizado): ")
    st.dataframe(df)

    plot_types = ["bar", "line", "scatter", "pie"]
    plot_type = st.selectbox("Selecione o tipo de gráfico", plot_types)
    plot = create_plot(df, plot_type)
    st.plotly_chart(plot)


    # Função adicional 1: Seleção de data
    st.date_input("Escolha uma data")

    # Função adicional 2: Caixa de texto
    texto = st.text_input("Digite algo")

    # Função adicional 3: Slider
    numero = st.slider("Escolha um número", 0, 100)

    # Função adicional 4: Botão de rádio
    opcao = st.radio("Escolha uma opção", ["Opção 1", "Opção 2", "Opção 3"])

    # Função adicional 5: Checkbox
    check = st.checkbox("Marque a opção")

    # Função adicional 6: Seletor de cor
    cor = st.color_picker("Escolha uma cor")

    # Mostrar as escolhas do usuário
    st.write("Texto digitado:", texto)
    st.write("Número escolhido:", numero)
    st.write("Opção selecionada:", opcao)
    st.write("Checkbox marcado:", check)
    st.write("Cor escolhida:", cor)


if __name__ == "__main__":
    main()
