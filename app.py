import streamlit as st
import pandas as pd
import math

# Configuración (SIEMPRE al inicio)
st.set_page_config(page_title="Sistema Tanque IA", layout="wide")

st.title("💧 Sistema Inteligente de Gestión de Tanques")

# Inputs
radio = st.number_input("Radio (m)", min_value=0.1, value=5.0)
altura = st.number_input("Altura total (m)", min_value=0.1, value=12.0)
nivel = st.number_input("Nivel actual (m)", min_value=0.0, value=6.0)

# Cálculos
volumen_total = math.pi * radio**2 * altura
volumen_actual = math.pi * radio**2 * nivel
porcentaje = (nivel / altura) * 100 if altura > 0 else 0

st.subheader("Resultados")
st.write(f"Volumen total: {volumen_total:.2f} m³")
st.write(f"Volumen actual: {volumen_actual:.2f} m³")
st.write(f"Porcentaje: {porcentaje:.2f}%")

# Alertas
if porcentaje < 20:
    st.error("🔴 Nivel CRÍTICO")
elif porcentaje < 50:
    st.warning("🟡 Nivel medio")
else:
    st.success("🟢 Nivel óptimo")

# Historial
if "historial" not in st.session_state:
    st.session_state.historial = pd.DataFrame(columns=["Nivel", "Porcentaje"])

if st.button("Guardar medición"):
    nueva = pd.DataFrame([[nivel, porcentaje]], columns=["Nivel", "Porcentaje"])
    st.session_state.historial = pd.concat(
        [st.session_state.historial, nueva], ignore_index=True
    )

st.subheader("Historial")
st.dataframe(st.session_state.historial)

if not st.session_state.historial.empty:
    st.line_chart(st.session_state.historial.set_index("Nivel"))

# Predicción simple
if len(st.session_state.historial) > 1:
    consumo = st.session_state.historial["Nivel"].diff().mean() * -1
    if consumo > 0:
        dias = nivel / consumo
        st.info(f"📉 Se vaciará en {dias:.2f} días aprox.")

# Estilos
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.main {
    background-color: #0f172a;
    color: white;
}

h1 {
    text-align: center;
    color: #38bdf8;
}

.stButton>button {
    background-color: #38bdf8;
    color: black;
    border-radius: 10px;
    padding: 10px;
}

.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)