import streamlit as st
import pandas as pd

st.title("Sistema de Consulta e Registro de Residência")

# ============================================================
# 1. Carregar base de dados
# ============================================================

CAMINHO_ARQUIVO = r"aplicativo\dados.ods"

st.subheader("Carregando dados...")

try:
    df = pd.read_excel(CAMINHO_ARQUIVO, engine="odf")  
    st.success("Base de dados carregada com sucesso!")
except Exception as e:
    st.error("Erro ao carregar o arquivo.")
    st.code(str(e))
    st.stop()

# Normalizar colunas
df.columns = df.columns.str.strip().str.lower()


# ============================================================
# 2. MENU LATERAL
# ============================================================

st.sidebar.title("Menu")
pagina = st.sidebar.radio(
    "Selecione a página:",
    ["Consultar Dados", "Registrar Escala (Supervisor)", "Registrar Atividade (Residente)"]
)


# ============================================================
# 3. CONSULTAR DADOS (Página 1)
# ============================================================

if pagina == "Consultar Dados":

    st.header("🔎 Consultar Dados")

    st.sidebar.subheader("Filtros")

    # Filtro CRM
    crm_especifico = st.sidebar.text_input("Buscar CRM específico:")

    # Filtro programa
    programas = ["Todos"] + sorted(df["programa"].dropna().unique())
    programa_sel = st.sidebar.selectbox("Programa:", programas)

    # Filtro ano residência
    anos = ["Todos"] + sorted(df["ano_residencia"].dropna().unique())
    ano_sel = st.sidebar.selectbox("Ano de Residência:", anos)

    # Filtro mês
    meses = ["Todos"] + sorted(df["mes"].dropna().unique())
    mes_sel = st.sidebar.selectbox("Mês:", meses)

    # Filtro turno
    turnos = ["Todos"] + sorted(df["turno"].dropna().unique())
    turno_sel = st.sidebar.selectbox("Turno:", turnos)

    # Filtro dia
    dias = ["Todos"] + sorted(df["dia"].dropna().unique())
    dia_sel = st.sidebar.selectbox("Dia:", dias)

    # Filtro escala
    escalas = ["Todos"] + sorted(df["escala"].dropna().unique())
    escala_sel = st.sidebar.selectbox("Escala:", escalas)

    # Aplicação dos filtros
    df_filtrado = df.copy()

    if crm_especifico:
        df_filtrado = df_filtrado[df_filtrado["crm"].astype(str).str.contains(crm_especifico)]

    if programa_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["programa"] == programa_sel]

    if ano_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["ano_residencia"] == ano_sel]

    if mes_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["mes"] == mes_sel]

    if turno_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["turno"] == turno_sel]

    if dia_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["dia"] == dia_sel]

    if escala_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["escala"] == escala_sel]

    # Exibir resultados
    st.subheader("Registros Filtrados")
    st.write(f"Total de registros: **{len(df_filtrado)}**")

    st.dataframe(df_filtrado, use_container_width=True)

    # Download
    if not df_filtrado.empty:
        csv = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Baixar resultados filtrados (CSV)",
            csv,
            "filtro_residencia.csv",
            "text/csv"
        )


# ============================================================
# 4. REGISTRAR ESCALA (Página 2)
# ============================================================

if pagina == "Registrar Escala (Supervisor)":

    st.header("📝 Registrar Escala — Supervisor")

    st.write("Preencha os campos abaixo para registrar uma nova escala:")

    crm = st.text_input("CRM do residente:")
    programa = st.selectbox("Programa:", sorted(df["programa"].dropna().unique()))
    ano_res = st.selectbox("Ano de Residência:", sorted(df["ano_residencia"].dropna().unique()))
    mes = st.selectbox("Mês:", sorted(df["mes"].dropna().unique()))
    dia = st.selectbox("Dia:", sorted(df["dia"].dropna().unique()))
    turno = st.selectbox("Turno:", sorted(df["turno"].dropna().unique()))
    escala = st.text_input("Escala / Atividade:")

    if st.button("Salvar Escala"):
        if crm and escala:
            novo_registro = {
                "crm": crm,
                "programa": programa,
                "ano_residencia": ano_res,
                "mes": mes,
                "dia": dia,
                "turno": turno,
                "escala": escala
            }

            df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)

            st.success("Escala registrada com sucesso!")

            # OPCIONAL: salvar no arquivo (descomente se quiser)
            df.to_excel(CAMINHO_ARQUIVO, index=False, engine="odf")
        else:
            st.error("CRM e Escala são obrigatórios.")

# ============================================================
# 5. REGISTRAR ATIVIDADE (Residente)
# ============================================================

if pagina == "Registrar Atividade (Residente)":

    st.header("📱 Registrar Atividade — Residente")

    st.write("Use este formulário simples para registrar sua atividade do dia:")

    crm = st.text_input("Seu CRM:")
    programa = st.selectbox("Programa:", sorted(df["programa"].dropna().unique()))
    ano_res = st.selectbox("Ano de Residência:", sorted(df["ano_residencia"].dropna().unique()))
    mes = st.selectbox("Mês:", sorted(df["mes"].dropna().unique()))
    dia = st.selectbox("Dia:", sorted(df["dia"].dropna().unique()))
    turno = st.selectbox("Turno:", sorted(df["turno"].dropna().unique()))
    atividade = st.text_input("Escala / Atividade:")

    if st.button("Enviar Atividade"):
        if crm and atividade:
            novo = {
                "crm": crm,
                "programa": programa,
                "ano_residencia": ano_res,
                "mes": mes,
                "dia": dia,
                "turno": turno,
                "escala": atividade  # <- mesmo campo usado para escalas
            }

            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_excel(CAMINHO_ARQUIVO, index=False, engine="odf")

            st.success("Atividade registrada com sucesso!")
        else:
            st.error("CRM e atividade são obrigatórios.")

