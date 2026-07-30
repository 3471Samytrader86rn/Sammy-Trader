import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="SAMMY TRADER", page_icon="📈", layout="centered")

st.title("📈 SAMMY TRADER - Análise de Sinais")
st.caption("IA de Análise Visual para Opções Binárias")

# Sidebar para API Key
st.sidebar.header("Configuração")
api_key = st.sidebar.text_input("Cole sua Gemini API Key:", type="password")

ativo = st.selectbox("Selecione o Ativo:", ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/CAD", "Outro"])
tempo = st.selectbox("Tempo gráfico:", ["M1", "M5"])

uploaded_file = st.file_uploader("Tire foto ou envie o print do gráfico:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gráfico Carregado", use_container_width=True)

if st.button("🚀 Analisar Gráfico", type="primary"):
    if not api_key:
        st.error("Por favor, informe sua Gemini API Key na barra lateral!")
    elif uploaded_file is None:
        st.warning("Envie uma imagem do gráfico para analisar.")
    else:
        with st.spinner("Analisando padrão de velas e indicadores..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                prompt = f"""
                Você é o SAMMY TRADER, uma IA especialista em análise gráfica de opções binárias.
                Análise o gráfico da imagem para o ativo {ativo} no tempo {tempo}.
                
                Instruções:
                1. Aplique a estratégia do quadrante de 5 velas (velas 3, 4 e 5 para regra da minoria na 6ª vela).
                2. Valide com suporte, resistência e tendência visíveis.
                3. Responda de forma clara com:
                   - SINAL: [COMPRAR / VENDER / AGUARDAR]
                   - JUSTIFICATIVA CURTA: Explicando a contagem das cores das velas.
                   - MOMENTO DE ENTRADA: Ex (Na virada da vela).
                """
                
                response = model.generate_content([prompt, image])
                st.success("Análise Concluída!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Erro ao processar: {e}")
