import streamlit as st
import pandas as pd
import random
import time
from fpdf import FPDF

# Configuração da Página
st.set_page_config(page_title="DanielFit Tracker", layout="wide")

# Estilização CSS Customizada (Corrigida)
st.markdown("""
<style>
.metric-box {
    background-color: #1e1e1e;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    border-bottom: 4px solid #00FF7F;
}
.metric-medical {
    background-color: #1e1e1e;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    border-bottom: 4px solid #FF3B30;
}
.text-value {
    font-size: 28px;
    font-weight: bold;
    color: #fff;
}
.text-label {
    font-size: 12px;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# 1. CABEÇALHO DO APLICATIVO
st.title("🏃 DanielFit Tracker")
st.subheader("Painel de Corrida & Telemetria Médica")
st.write("Simulador de performance física e monitoramento biométrico cardiovascular em tempo real.")
st.markdown("---")

# 2. ENTRADA DE DADOS DO USUÁRIO
col_u1, col_u2, col_u3 = st.columns(3)
with col_u1:
    nome_atleta = st.text_input("Atleta:", value="Visitante")
with col_u2:
    idade_atleta = st.number_input("Idade:", min_value=10, max_value=100, value=25)
with col_u3:
    peso_atleta = st.number_input("Peso (kg):", min_value=30, max_value=200, value=75)

# Cálculo de Frequência Cardíaca Máxima
fc_maxima = 220 - idade_atleta

# 3. CONTROLES DO CRONÔMETRO
st.markdown("### ⏱️ Controle do Treino")
col_btn1, col_btn2 = st.columns(2)

if 'corrida_ativa' not in st.session_state:
    st.session_state.corrida_ativa = False
if 'tempo_decorrido' not in st.session_state:
    st.session_state.tempo_decorrido = 0

with col_btn1:
    if st.button("▶️ INICIAR CORRIDA", use_container_width=True):
        st.session_state.corrida_ativa = True

with col_btn2:
    if st.button("⏹️ PARAR & SALVAR", use_container_width=True):
        st.session_state.corrida_ativa = False

# Placeholders para métricas e gráficos
placeholder_metricas = st.empty()
placeholder_grafico = st.empty()

# DataFrame Inicial
df_historico = pd.DataFrame({
    "Tempo (s)": list(range(0, 11)),
    "Frequência Cardíaca (BPM)": [random.randint(70, 98) for _ in range(11)],
    "Velocidade (km/h)": [0.0] + [round(random.uniform(8.0, 12.5), 1) for _ in range(10)]
})

# LOOP EM TEMPO REAL
if st.session_state.corrida_ativa:
    st.session_state.tempo_decorrido += 1
    velocidade_atual = round(random.uniform(9.0, 14.0), 1)
    distancia_atual = round((st.session_state.tempo_decorrido * velocidade_atual) / 3600, 3)
    bpm_atual = int(65 + (velocidade_atual * 8) + random.randint(-5, 5))
    spO2_atual = random.randint(96, 99)
    calorias_atuais = int(st.session_state.tempo_decorrido * 0.2 * (peso_atleta / 75))

    with placeholder_metricas.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Tempo Decorrido", f"{st.session_state.tempo_decorrido}s")
        c2.metric("Distância", f"{distancia_atual} km")
        c3.metric("Frequência Cardíaca", f"{bpm_atual} BPM")
        c4.metric("SpO2", f"{spO2_atual}%")

    time.sleep(1)
    st.rerun()

st.markdown("---")

# 4. EXPORTAÇÃO E GERAÇÃO DE PDF
st.markdown("### 📄 Exportação de Relatório de Saúde")

def gerar_pdf(nome, idade, peso, tempo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Relatorio de Desempenho Clinico - DanielFit", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Atleta: {nome}", ln=True)
    pdf.cell(200, 10, txt=f"Idade: {idade} anos | Peso: {peso} kg", ln=True)
    pdf.cell(200, 10, txt=f"Tempo Total Treinado: {tempo} segundos", ln=True)
    pdf.cell(200, 10, txt=f"Frequencia Cardiaca Maxima Estimada: {220 - idade} BPM", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Status: Avaliacao Cardiovascular Integrada com Sucesso.", ln=True)
    
    # Retorna o arquivo em formato de bytes para download
    return pdf.output(dest='S').encode('latin-1')

pdf_bytes = gerar_pdf(nome_atleta, idade_atleta, peso_atleta, st.session_state.tempo_decorrido)

st.download_button(
    label="📥 Baixar Relatório em PDF",
    data=pdf_bytes,
    file_name=f"Relatorio_{nome_atleta}.pdf",
    mime="application/pdf"
)