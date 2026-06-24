import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

# 1. Configuración básica de la página
st.set_page_config(
    page_title="E-Commerce Analytics Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Plataforma Analítica Regional E-commerce")
st.markdown("---")

# 2. Carga de Datos (Usamos cache para que no recargue en cada clic)
@st.cache_data
def load_data():
    # Ajusta estas rutas dependiendo desde dónde ejecutes streamlit run
    ruta_transacciones = '../data/consolidado_transformado.csv'
    ruta_clientes = '../data/clientes_segmentados_final.csv'
    
    df_transacciones = pd.read_csv(ruta_transacciones) if os.path.exists(ruta_transacciones) else pd.DataFrame()
    df_clientes = pd.read_csv(ruta_clientes) if os.path.exists(ruta_clientes) else pd.DataFrame()
    
    return df_transacciones, df_clientes

df_transacciones, df_clientes = load_data()

# 3. Estructura de Vistas Diferenciadas (Requisito del Proyecto)
# Creamos tres pestañas, una para cada equipo
tab_gerencia, tab_marketing, tab_operaciones = st.tabs([
    "📈 Gerencia Comercial", 
    "🎯 Marketing", 
    "📦 Operaciones y Bodega"
])

# --- VISTA 1: GERENCIA COMERCIAL ---
with tab_gerencia:
    st.header("Indicadores Macro por País")
    if not df_transacciones.empty:
        # Filtro interactivo
        paises = st.multiselect("Seleccionar País", options=df_transacciones['pais'].unique(), default=df_transacciones['pais'].unique())
        df_filtrado = df_transacciones[df_transacciones['pais'].isin(paises)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Ingresos Totales por País (USD)")
            ventas_pais = df_filtrado.groupby('pais')['precio_final_usd'].sum().reset_index()
            fig1 = px.bar(ventas_pais, x='pais', y='precio_final_usd', color='pais', text_auto='.2s')
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            st.subheader("Ticket Promedio por Categoría")
            ticket_cat = df_filtrado.groupby(['categoria', 'pais'])['precio_final_usd'].mean().reset_index()
            fig2 = px.bar(ticket_cat, x='categoria', y='precio_final_usd', color='pais', barmode='group')
            st.plotly_chart(fig2, use_container_width=True)

# --- VISTA 2: MARKETING ---
with tab_marketing:
    st.header("Comportamiento y Segmentación de Clientes")
    if not df_clientes.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribución de Segmentos (K-Means)")
            # Asumimos que la columna se llama 'segmento_marketing' como definimos antes
            if 'segmento_marketing' in df_clientes.columns:
                conteo_segmentos = df_clientes['segmento_marketing'].value_counts().reset_index()
                fig3 = px.pie(conteo_segmentos, values='count', names='segmento_marketing', hole=0.4)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.warning("La columna 'segmento_marketing' no se encontró en los datos.")
                
        with col2:
            st.subheader("Valor Monetario vs Recencia por Segmento")
            if 'pca_1' in df_clientes.columns:
                 # Si guardaste las variables PCA, las usamos, si no, usamos recencia vs valor monetario
                 fig4 = px.scatter(df_clientes, x='recencia', y='valor_monetario', color='segmento_marketing',
                                   size='frecuencia', hover_data=['id_usuario'])
                 st.plotly_chart(fig4, use_container_width=True)

# --- VISTA 3: OPERACIONES DE BODEGA ---
with tab_operaciones:
    st.header("Logística y Predicción de Despachos")
    if not df_transacciones.empty:
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Retraso Promedio por Bodega (Días Reales)")
            if 'dias_demora_real' in df_transacciones.columns:
                retrasos = df_transacciones.groupby(['pais', 'id_bodega'])['dias_demora_real'].mean().reset_index()
                fig5 = px.box(df_transacciones, x='pais', y='dias_demora_real', color='pais')
                st.plotly_chart(fig5, use_container_width=True)
                
        with col2:
            st.subheader("Simulador de Predicción (Random Forest)")
            st.info("Utiliza el modelo entrenado para estimar el tiempo de despacho.")
            
            # Lógica de carga de modelos
            try:
                ruta_modelo = '../models/regresion_despacho_model.pkl'
                ruta_columnas = '../models/columnas_regresion.pkl'
                ruta_encoder = '../models/encoder_bodegas.pkl'
                
                if os.path.exists(ruta_modelo) and os.path.exists(ruta_columnas) and os.path.exists(ruta_encoder):
                    modelo_rf = joblib.load(ruta_modelo)
                    columnas_rf = joblib.load(ruta_columnas)
                    le_bodegas = joblib.load(ruta_encoder)
                    
                    with st.form("form_prediccion"):
                        sel_pais = st.selectbox("País Origen", df_transacciones['pais'].unique())
                        sel_bodega = st.selectbox("ID Bodega", df_transacciones['id_bodega'].astype(str).unique())
                        sel_cat = st.selectbox("Categoría del Producto", df_transacciones['categoria'].unique())
                        sel_vol = st.slider("Volumen de Compras del Día en la Bodega", min_value=1, max_value=1000, value=150)
                        
                        submit = st.form_submit_button("Estimar Tiempo de Despacho")
                        
                    if submit:
                        # 1. Preparar DataFrame de entrada
                        input_df = pd.DataFrame({
                            'pais': [sel_pais],
                            'categoria': [sel_cat],
                            'volumen_compra_dia': [sel_vol],
                            'id_bodega': [sel_bodega]
                        })
                        
                        # 2. Codificar bodega
                        input_df['id_bodega_encoded'] = le_bodegas.transform(input_df['id_bodega'])
                        X_input = input_df[['pais', 'categoria', 'volumen_compra_dia', 'id_bodega_encoded']]
                        
                        # 3. One-Hot Encoding y alinear columnas
                        X_encoded = pd.get_dummies(X_input, columns=['pais', 'categoria'])
                        X_final = X_encoded.reindex(columns=columnas_rf, fill_value=0)
                        
                        # 4. Predecir
                        prediccion = modelo_rf.predict(X_final)[0]
                        
                        st.success(f"📦 Tiempo estimado de entrega: **{prediccion:.1f} días**")
                        st.caption(f"Margen de error estimado del modelo: ± 1.36 días")
                else:
                    st.warning("No se encontraron los archivos del modelo en la carpeta /models/ (.pkl).")
            except Exception as e:
                st.error(f"Error al cargar el módulo de predicción: {e}")