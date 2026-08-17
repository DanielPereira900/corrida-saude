import time
import math
from io import BytesIO
import streamlit as st
import plotly.graph_objects as go

# Bibliotecas para geração de PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="Corrida Saúde", page_icon="🏃", layout="wide")

st.title("🏃 Dashboard Corrida Saúde & Esteira")
st.markdown("Acompanhe seus dados de treino em tempo real e gere um relatório médico de desempenho.")

# ---------------------------------------------------------
# ESTADO DA SESSÃO (SESSION STATE)
# ---------------------------------------------------------
if "rodando" not in st.session_state:
    st.session_state.rodando = False
if "tempo_inicio" not in st.session_state:
    st.session_state.tempo_inicio = 0.0
if "tempo_decorrido" not in st.session_state:
    st.session_state.tempo_decorrido = 0.0

# ---------------------------------------------------------
# BARRA LATERAL: PERFIL DO ATLETA
# ---------------------------------------------------------
st.sidebar.header("👤 Perfil do Atleta")
nome = st.sidebar.text_input("Nome", "Atleta")
idade = st.sidebar.number_input("Idade", min_value=10, max_value=100, value=30)
peso = st.sidebar.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
altura = st.sidebar.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.75, step=0.01)

# Cálculo de IMC e Frequência Cardíaca Máxima (FCM)
imc = peso / (altura ** 2)
fcm = 220 - idade

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Métrica do Atleta")
st.sidebar.write(f"**IMC:** {imc:.1f}")
st.sidebar.write(f"**FC Máxima Estimada:** {fcm} BPM")

# ---------------------------------------------------------
# CONTROLES DO TREINO
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Controles da Esteira")

velocidade = st.sidebar.slider("Velocidade da Esteira (km/h)", 0.0, 20.0, 8.0, step=0.5)
bpm_simulado = st.sidebar.slider("Batimento Cardíaco (BPM)", 60, 200, 120, step=1)

col_b1, col_b2 = st.sidebar.columns(2)

if col_b1.button("▶️ Iniciar"):
    if not st.session_state.rodando:
        st.session_state.rodando = True
        st.session_state.tempo_inicio = time.time() - st.session_state.tempo_decorrido

if col_b2.button("⏹️ Parar"):
    st.session_state.rodando = False

if st.sidebar.button("🔄 Resetar"):
    st.session_state.rodando = False
    st.session_state.tempo_decorrido = 0.0

# Atualiza tempo se estiver rodando
if st.session_state.rodando:
    st.session_state.tempo_decorrido = time.time() - st.session_state.tempo_inicio

# ---------------------------------------------------------
# PAINEL PRINCIPAL
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

# Cálculo de Distância e Calorias
distancia_km = (velocidade * (st.session_state.tempo_decorrido / 3600.0))
# Fórmula simplificada de queima calórica (MET médio ~ 8 para corrida leve)
calorias = (8 * peso * (st.session_state.tempo_decorrido / 3600.0))

minutos = int(st.session_state.tempo_decorrido // 60)
segundos = int(st.session_state.tempo_decorrido % 60)
tempo_formatado = f"{minutos:02d}:{segundos:02d}"

col1.metric("⏱️ Tempo Decorrido", tempo_formatado)
col2.metric("📍 Distância Percorrida", f"{distancia_km:.2f} km")
col3.metric("🔥 Calorias Estimadas", f"{calorias:.0f} kcal")

st.markdown("---")

# ---------------------------------------------------------
# VELOCÍMETRO E FREQUÊNCIA CARDÍACA (GRÁFICOS)
# ---------------------------------------------------------
g_col1, g_col2 = st.columns(2)

with g_col1:
    fig_vel = go.Figure(go.Indicator(
        mode="gauge+number",
        value=velocidade,
        title={'text': "Velocímetro (km/h)"},
        gauge={
            'axis': {'range': [0, 20]},
            'bar': {'color': "#1E88E5"},
            'steps': [
                {'range': [0, 6], 'color': "#E8F5E9"},
                {'range': [6, 12], 'color': "#FFFDE7"},
                {'range': [12, 20], 'color': "#FFEBEE"}
            ]
        }
    ))
    fig_vel.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_vel, use_container_width=True)

with g_col2:
    # Diagnóstico simplificado de zona cardíaca
    percentual_fcm = (bpm_simulado / fcm) * 100
    if percentual_fcm < 60:
        cor_bpm = "#4CAF50"
        status_bpm = "Aquecimento / Leve"
    elif percentual_fcm < 85:
        cor_bpm = "#FF9800"
        status_bpm = "Zona Aeróbica (Ideal)"
    else:
        cor_bpm = "#F44336"
        status_bpm = "Atenção: Esforço Intenso!"

    fig_bpm = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bpm_simulado,
        title={'text': f"Frequência Cardíaca (BPM)\n[{status_bpm}]"},
        gauge={
            'axis': {'range': [40, 220]},
            'bar': {'color': cor_bpm},
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': fcm
            }
        }
    ))
    fig_bpm.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_bpm, use_container_width=True)

# Loop de atualização automática da tela se a esteira estiver rodando
if st.session_state.rodando:
    time.sleep(1)
    st.rerun()

# ---------------------------------------------------------
# GERAÇÃO DE RELATÓRIO PDF
# ---------------------------------------------------------
def gerar_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Título do PDF
    elements.append(Paragraph("Relatório do Treino - Corrida Saúde", styles['Title']))
    elements.append(Spacer(1, 20))

    # Avaliação do estado do coração
    if percentual_fcm < 60:
        avaliacao_saude = "Excelente para recuperação ou aquecimento."
    elif percentual_fcm <= 85:
        avaliacao_saude = "Dentro da zona cardiovascular saudável e segura."
    else:
        avaliacao_saude = "Frequência muito elevada! Recomenda-se reduzir a intensidade."

    # Tabela com Dados do Atleta e Treino
    dados = [
        ["Parâmetro", "Valor"],
        ["Nome do Atleta", nome],
        ["Idade / Peso / Altura", f"{idade} anos | {peso} kg | {altura} m"],
        ["IMC", f"{imc:.1f}"],
        ["Tempo Total de Treino", tempo_formatado],
        ["Distância Percorrida", f"{distancia_km:.2f} km"],
        ["Velocidade Atual/Média", f"{velocidade} km/h"],
        ["Frequência Cardíaca Média", f"{bpm_simulado} BPM"],
        ["Calorias Gastas", f"{calorias:.0f} kcal"],
        ["Avaliação Cardíaca", avaliacao_saude]
    ]

    tabela = Table(dados, colWidths=[200, 300])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#1E88E5")),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F5F5F5")),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
    ]))

    elements.append(tabela)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<b>Nota Médica:</b> Este relatório é gerado a partir de simulação de dados e parâmetros gerais de desempenho aeróbico.", styles['Italic']))

    doc.build(elements)
    buffer.seek(0)
    return buffer

st.markdown("---")
st.subheader("📄 Relatório Médico e Desempenho")

pdf_bytes = gerar_pdf()
st.download_button(
    label="📥 Baixar Relatório Completo em PDF",
    data=pdf_bytes,
    file_name=f"relatorio_corrida_{nome.lower().replace(' ', '_')}.pdf",
    mime="application/pdf"
)