import streamlit as st
import urllib.parse

# 1. CONFIGURAÇÃO DA PÁGINA (Identidade Visual da Shopee)
st.set_page_config(
    page_title="Ponto de Coleta Shopee & Variedades", 
    page_icon="🟠", 
    layout="wide"
)

# Dados reais fornecidos pelo proprietário Daniel Pereira
DANIEL_NOME = "Daniel Pereira"
DANIEL_ZAP = "5516991768327"
DANIEL_EMAIL = "Danielj.pereira2@gmail.com"
DANIEL_ENDERECO = "Av. General Teles, Jardim Guanabara, Franca - SP, CEP: 14405-277"

# 2. DESIGN ESTILIZADO EM CSS (Look profissional para o LinkedIn)
st.markdown("""
    <style>
    .banner-shopee {
        background: linear-gradient(135deg, #EE4D2D 0%, #FF7337 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(238,77,45,0.2);
    }
    .card-produto {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        border-top: 5px solid #EE4D2D;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
    }
    .preco-produto {
        font-size: 22px;
        color: #EE4D2D;
        font-weight: bold;
        margin: 10px 0;
    }
    .badge-categoria {
        background-color: #f5f5f5;
        color: #555;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BANNER PRINCIPAL DE MARKETING
st.markdown(f"""
    <div class="banner-shopee">
        <h1>🟠 PONTO DE COLETA OFICIAL SHOPEE</h1>
        <p style="font-size: 18px; margin-top: 5px;">
            Deixe ou retire seus pacotes Shopee aqui na <b>Espaço Variedades de Daniel Pereira</b>!
        </p>
        <p style="font-size: 14px; opacity: 0.9;">📍 {DANIEL_ENDERECO}</p>
    </div>
""", unsafe_allow_html=True)

# 4. GERAÇÃO AUTOMÁTICA DA VITRINE (Simulando o catálogo de ~70 produtos por categoria)
categorias = ["Camisetas & Roupas", "Chinelos & Calçados", "Fones & Eletrônicos", "Bonés & Óculos Ray-Ban"]
vitrine_produtos = []

# Loop estruturado para povoar dinamicamente os 70 produtos requisitados
for i in range(1, 71):
    if i <= 20:
        cat = "Camisetas & Roupas"
        nome = f"Camiseta Streetwear Oversized Premium Mod. {i}"
        preco = 49.90 + (i * 1.5)
    elif i <= 35:
        cat = "Chinelos & Calçados"
        nome = f"Chinelo Nuvem Ergonômico Antiderrapante Sl. {i-20}"
        preco = 35.00 + (i * 0.8)
    elif i <= 55:
        cat = "Fones & Eletrônicos"
        nome = f"Fone de Ouvido Bluetooth TWS Pro Mod. {i-35}"
        preco = 79.90 + (i * 2.1)
    else:
        cat = "Bonés & Óculos Ray-Ban"
        nome = f"Óculos de Sol Estilo Ray-Ban Classic / Boné Aba Curva {i-55}"
        preco = 119.00 + (i * 1.2)
        
    vitrine_produtos.append({"id": i, "categoria": cat, "nome": nome, "preco": preco})

# 5. ESTRUTURA INTERNA: NAVEGAÇÃO POR ABAS DO PROJETO
aba_vitrine, aba_coleta, aba_sobre = st.tabs(["🛒 Vitrine Comercial", "📦 Logística Shopee (Coleta)", "ℹ️ Informações de Contato"])

# --- ABA 1: VITRINE DE PRODUTOS ---
with aba_vitrine:
    st.subheader("🛍️ Explore Nossa Vitrine Interativa")
    
    # Filtros de busca no painel superior
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        busca = st.text_input("🔍 O que você está procurando hoje?", placeholder="Ex: Fone Bluetooth, Camiseta...")
    with col_f2:
        categoria_selecionada = st.selectbox("📂 Filtrar por Categoria", ["Todas"] + categorias)
        
    # Filtragem lógica dos dados
    produtos_filtrados = [
        p for p in vitrine_produtos 
        if (categoria_selecionada == "Todas" or p["categoria"] == categoria_selecionada)
        and (busca.lower() in p["nome"].lower())
    ]
    
    # Paginação inteligente para exibição limpa (Mostra 1 por vez de forma rotativa se preferir, ou em grade controlada)
    st.write(f"Exibindo **{len(produtos_filtrados)}** produtos encontrados no estoque.")
    
    # Renderização da grade de produtos (3 colunas por linha)
    for idx in range(0, len(produtos_filtrados), 3):
        cols = st.columns(3)
        for col_idx in range(3):
            pos = idx + col_idx
            if pos < len(produtos_filtrados):
                prod = produtos_filtrados[pos]
                with cols[col_idx]:
                    st.markdown(f"""
                        <div class="card-item">
                            <span class="badge-categoria">{prod['categoria']}</span>
                            <h3 style="font-size:16px; margin: 10px 0 5px 0; color:#333;">{prod['nome']}</h3>
                            <div class="preco-produto">R$ {prod['preco']:.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Botão individual de interesse via WhatsApp
                    texto_reserva = f"Olá Daniel, vi na vitrine o produto: {prod['nome']} (R$ {prod['preco']:.2f}) e gostaria de saber se está disponível para retirada!"
                    link_reserva = f"https://whatsapp.com{DANIEL_ZAP}&text={urllib.parse.quote(texto_reserva)}"
                    st.markdown(f'<a href="{link_reserva}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:6px; border-radius:5px; cursor:pointer;">📲 Consultar Disponibilidade</button></a>', unsafe_allow_html=True)

# --- ABA 2: LOGÍSTICA DE COLETA SHOPEE ---
with aba_coleta:
    st.subheader("📦 Sistema Integrado de Postagem e Retirada")
    st.info("Utilize este canal para despachar suas vendas da Shopee ou coletar suas compras feitas no app.")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown("""
        ### ✅ Vantagens de Deixar seu Pacote Aqui:
        * **Sem Filas:** Processamento ágil em menos de 1 minuto.
        * **Segurança Total:** Ambientes monitorados para garantir a integridade dos seus pacotes.
        * **Notificação Automática:** Assim que biparmos seu pacote, o app da Shopee atualiza na hora.
        """)
        
    with col_c2:
        st.markdown("### 🔍 Rastreamento Rápido no Ponto")
        codigo_shopee = st.text_input("Insira o Código de Rastreamento da Shopee (Ex: BR26...):")
        if st.button("Verificar Status no Ponto de Coleta"):
            if codigo_shopee:
                st.success(f"Pacote **{codigo_shopee}** identificado com sucesso! Aguardando coleta da transportadora parceira Pegaki/Shopee Express.")
            else:
                st.warning("Por favor, digite um código válido.")

# --- ABA 3: INFORMAÇÕES CORPORATIVAS ---
with aba_sobre:
    st.subheader("👤 Sobre o Administrador & Endereço")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown(f"""
        **Proprietário Oficial:** {DANIEL_NOME}  
        📬 **E-mail Corporativo:** [{DANIEL_EMAIL}](mailto:{DANIEL_EMAIL})  
        📍 **Endereço Homologado:** {DANIEL_ENDERECO}  
        
        *Nota: Ponto comercial de fácil acesso situado no Jardim Guanabara em Franca - SP, com fachada identificada e balcão exclusivo de atendimento Shopee.*
        """)
    
        with col_a2:
        # Link Direto para o WhatsApp verificado
         texto_geral = "Olá Daniel Pereira, gostaria de obter mais informações sobre o horário de funcionamento do Ponto de Coleta da Shopee."
         link_geral = f"https://wa.me {5516991768327} ?texte+{urllib.parse.quote(texto_geral)}"             
         st.markdown(f"""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px;">
        <h4>Atendimento Direto via WhatsApp</h4>
        <p>Precisa de suporte logístico imediato ou quer encomendar algum item de loja?</p>
        <a href="{link_geral}" target="_blank">
            <button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">
                Falar com Daniel no WhatsApp
            </button>
        </a>
    </div>
         """, unsafe_allow_html=True)