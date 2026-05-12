import pandas as pd
import streamlit as st
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Análisis IoT - Carro",
    page_icon="🚗",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title('🚗 Análisis de datos IoT - Simulación de Carro')
st.markdown("""
Esta aplicación permite analizar los datos de un carro simulado en Wokwi con ESP32.
Las variables analizadas son **velocidad** y **combustible**.
""")

# Create map data for EAFIT
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

# Display map
st.subheader("📍 Ubicación del proyecto - Universidad EAFIT")
st.map(eafit_location, zoom=15)

try:
    # Load CSV automatically
    df1 = pd.read_csv("datos_carro.csv")

    # Ajustar columna de tiempo
    if 'tiempo' in df1.columns:
        df1['tiempo'] = pd.to_datetime(df1['tiempo'])
        df1 = df1.set_index('tiempo')
    elif 'Time' in df1.columns:
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')
    else:
        df1.iloc[:, 0] = pd.to_datetime(df1.iloc[:, 0])
        df1 = df1.set_index(df1.columns[0])

    # Verificar columnas necesarias
    if 'velocidad' not in df1.columns or 'combustible' not in df1.columns:
        st.error("El archivo debe tener las columnas 'velocidad' y 'combustible'.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Visualización",
            "📊 Estadísticas",
            "🔍 Filtros",
            "🗺️ Información del Proyecto"
        ])

        with tab1:
            st.subheader('Visualización de Datos')

            chart_type = st.selectbox(
                "Seleccione tipo de gráfico",
                ["Línea", "Área", "Barra"]
            )

            variables = df1[['velocidad', 'combustible']]

            if chart_type == "Línea":
                st.line_chart(variables)
            elif chart_type == "Área":
                st.area_chart(variables)
            else:
                st.bar_chart(variables)

            if st.checkbox('Mostrar datos crudos'):
                st.dataframe(df1)

        with tab2:
            st.subheader('Análisis Estadístico')

            col1, col2 = st.columns(2)

            with col1:
                st.write("### 🚗 Velocidad")
                st.dataframe(df1["velocidad"].describe())

            with col2:
                st.write("### ⛽ Combustible")
                st.dataframe(df1["combustible"].describe())

            st.subheader("Métricas principales")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Velocidad promedio", f"{df1['velocidad'].mean():.2f} km/h")
            c2.metric("Velocidad máxima", f"{df1['velocidad'].max():.2f} km/h")
            c3.metric("Combustible promedio", f"{df1['combustible'].mean():.2f}%")
            c4.metric("Combustible mínimo", f"{df1['combustible'].min():.2f}%")

        with tab3:
            st.subheader('Filtros de Datos')

            min_vel = float(df1["velocidad"].min())
            max_vel = float(df1["velocidad"].max())
            mean_vel = float(df1["velocidad"].mean())

            if min_vel == max_vel:
                st.warning(f"Todos los valores de velocidad son iguales: {min_vel:.2f}")
                st.dataframe(df1)
            else:
                velocidad_minima = st.slider(
                    'Velocidad mínima',
                    min_vel,
                    max_vel,
                    mean_vel
                )

                filtrado = df1[df1["velocidad"] >= velocidad_minima]

                st.write(f"Registros con velocidad mayor o igual a {velocidad_minima:.2f} km/h:")
                st.dataframe(filtrado)

                csv = filtrado.to_csv().encode('utf-8')
                st.download_button(
                    label="Descargar datos filtrados",
                    data=csv,
                    file_name='datos_filtrados_carro.csv',
                    mime='text/csv',
                )

        with tab4:
            st.subheader("Información del Proyecto")

            col1, col2 = st.columns(2)

            with col1:
                st.write("### Ubicación")
                st.write("**Universidad EAFIT**")
                st.write("- Latitud: 6.2006")
                st.write("- Longitud: -75.5783")
                st.write("- Ciudad: Medellín, Colombia")

            with col2:
                st.write("### Detalles del sistema")
                st.write("- Microcontrolador: ESP32")
                st.write("- Sensor: Potenciómetro")
                st.write("- Variable 1: Velocidad")
                st.write("- Variable 2: Combustible")
                st.write("- Plataforma: Wokwi + InfluxDB + Grafana + Colab + Streamlit")

except Exception as e:
    st.error(f'Error al procesar el archivo: {str(e)}')
    st.info('Verifica que el archivo datos_carro.csv esté en el repositorio junto a Inicio.py.')

# Footer
st.markdown("""
---
Desarrollado para el análisis de datos IoT de una simulación de carro.
""")
