import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# Configuração da página
st.set_page_config(page_title="SAMMY TRADER - Análise de Sinais", page_icon="📈", layout="centered")

st.title("📈 SAMMY TRADER - Análise de Sinais")
st.caption("IA de Análise Visual para Opções Binárias")

# Menu Lateral - Configurações
st.sidebar.header("Configuração")
api_key = st.sidebar.text_input("Cole sua Gemini API Key:", type="password")

# Campos de seleção de ativo e tempo gráfico
ativo = st.selectbox("Selecione o Ativo:", ["EUR/JPY (OTC)", "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)"])
tempo_grafico = st.selectbox("Tempo gráfico:", ["M1", "M5", "M15"])

# Upload ou foto do gráfico
uploaded_file = st.file_uploader("Tire foto ou envie o print do gráfico:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gráfico Carregado", use_container_width=True)

    if st.button("🚀 Analisar Gráfico", type="primary"):
        if not api_key:
            st.error("Por favor, insira sua API Key do Gemini na barra lateral.")
        else:
            with st.spinner("Analisando padrões visuais do gráfico..."):
                try:
                    # Inicializa o cliente oficial da biblioteca google-genai
                    client = genai.Client(api_key=api_key)

                    prompt = f"""
                    Você é um especialista em análise técnica e Price Action para Opções Binárias.
                    Analise a imagem deste gráfico do ativo {ativo} no tempo gráfico {tempo_grafico}.

                    Forneça uma resposta direta com o seguinte formato:
                    1. 📊 **Tendência Atual:** (De Alta, De Baixa ou Lateral)
                    2. 🔍 **Padrões Identificados:** (Suporte, Resistência, Padrão de Candles)
                    3. 🚨 **Sinal Sugerido:** (COMPRA / CALL ou VENDA / PUT)
                    4. ⏱️ **Tempo de Expiração:** {tempo_grafico}
                    5. ⚠️ **Nível de Confiança:** (Alto, Média, Baixo) + breve justificativa.
                    """

                    # Utiliza o modelo estável mais recente
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[prompt, image]
                    )

                    st.success("Análise Concluída!")
                    st.markdown(response.text)

                except Exception as e:
                    # Caso ocorra erro com o modelo flash, tenta com o modelo pro
                    try:
                        response = client.models.generate_content(
                            model="gemini-2.5-pro",
                            contents=[prompt, image]
                        )
                        st.success("Análise Concluída!")
                        st.markdown(response.text)
                    except Exception as err:
                        st.error(f"Erro ao processar a análise: {str(err)}")
