import streamlit as st
from google import genai
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Sammy Trader - Análise de Sinais", layout="wide")

st.title("📈 SAMMY TRADER - Análise de Sinais")
st.caption("IA de Análise Visual para Opções Binárias")

# Sidebar para API Key
st.sidebar.title("Configuração")
api_key_input = st.sidebar.text_input("Cole sua Gemini API Key:", type="password")

# Seleção de opções
ativo = st.selectbox("Selecione o Ativo:", ["EUR/USD", "EUR/JPY (OTC)", "USD/JPY", "GBP/USD"])
tempo_grafico = st.selectbox("Tempo gráfico:", ["M1", "M5", "S5"])

# Upload da imagem
uploaded_file = st.file_uploader("Tire foto ou envie o print do gráfico:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gráfico Carregado", use_container_width=True)

# Botão de Análise
if st.button("🚀 Analisar Gráfico", type="primary"):
    if not api_key_input:
        st.error("Por favor, informe sua Gemini API Key na barra lateral!")
    elif uploaded_file is None:
        st.warning("Envie uma imagem do gráfico para realizar a análise.")
    else:
        try:
            with st.spinner("Analisando padrão de velas e indicadores..."):
                # Inicializa o cliente com a nova SDK oficial
                client = genai.Client(api_key=api_key_input)
                
                prompt = f"""
                Você é um especialista em análise técnica de opções binárias.
                Analise esta imagem do gráfico para o ativo {ativo} no tempo {tempo_grafico}.
                
                Forneça uma análise rápida e objetiva:
                1. Tendência atual (Alta, Baixa ou Lateral).
                2. Padrões de velas/candlesticks identificados.
                3. Recomendação de sinal: CALL (COMPRA), PUT (VENDA) ou AGUARDAR.
                4. Motivo da análise.
                """
                
                # Chamada do modelo Gemini 2.5 Flash
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image, prompt]
                )
                
                st.success("Análise Concluída!")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Erro ao processar a análise: {e}")
