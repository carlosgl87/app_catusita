import streamlit as st
import pandas as pd
import plotly.graph_objs as go


df1 = pd.read_csv('df_carlos_1_vf.csv')
df2 = pd.read_csv('df_carlos_2_vf.csv')

# Título de la aplicación
# st.title("Catusita - Recomendación de Compras ")

# Crear la barra lateral con opciones
st.sidebar.title("Catusita - Recomendaciones Compras")
seccion = st.sidebar.radio("Selecciona una sección:", ["Carga Archivos", "Dashboard", "Recomendaciones"])

# Lógica para mostrar el contenido de cada sección
if seccion == "Carga Archivos":
    st.header("Carga de Archivos")
    data = {
        "SKU": [1234, 1235, 1236, 1237, 1238, 1239],
        "Familia": ['Sakura', 'Sakura', 'Sakura', 'Sakura', 'Sakura', 'Sakura'],
        "Riesgo": [3, 2, 2, 2, 1, 1],
        "LT": [123, 123, 123, 123, 123, 123],
        "Stock": [123, 123, 123, 123, 123, 123],
        "Venta Promedio": [123, 123, 123, 123, 123, 123],
        "Ultimo Ingreso": [123, 123, 123, 123, 123, 123],
        "Fecha Ult. Ingreso": ['01/01/2023', '01/01/2023', '01/01/2023', '01/01/2023', '01/01/2023', '01/01/2023'],
        "Compra rec.": [123, 123, 123, 123, 123, 123],
    }
    df = pd.DataFrame(data)

    # Opción alternativa con st.dataframe para hacer la tabla interactiva
    st.header("Recomendaciones de compra")
    st.write('Ultima Actualizacion: 03/10/2024')
    
    
    with st.expander("Data SUNAT"):
        st.write('Ultima Actualizacion: 03/10/2024')
        #st.dataframe(df)
        uploaded_file = st.file_uploader("Cargar archivo SUNAT", type=["txt", "csv", "xls", "xlsx"])
    
    with st.expander("Data SUNARP"):
        st.write('Ultima Actualizacion: 03/10/2024')
        uploaded_file = st.file_uploader("Cargar archivo SUNARP", type=["txt", "csv", "xls", "xlsx"])
    
    with st.expander("Data Ventas"):
        st.write('Ultima Actualizacion: 03/10/2024')
        uploaded_file = st.file_uploader("Cargar archivo Ventas", type=["txt", "csv", "xls", "xlsx"])

    with st.expander("Data Lista Negra"):
        st.write('Ultima Actualizacion: 03/10/2024')
        uploaded_file = st.file_uploader("Cargar archivo Lista Negra", type=["txt", "csv", "xls", "xlsx"])

    with st.expander("Data Lista Kits"):
        st.write('Ultima Actualizacion: 03/10/2024')
        uploaded_file = st.file_uploader("Cargar archivo Lista Kits", type=["txt", "csv", "xls", "xlsx"])

    with st.expander("Data Lead Times"):
        st.write('Ultima Actualizacion: 03/10/2024')
        uploaded_file = st.file_uploader("Cargar archivo Lead Times", type=["txt", "csv", "xls", "xlsx"])

    with st.expander("Data Inventario"):
        st.write('Ultima Actualizacion: 03/10/2024')
        uploaded_file = st.file_uploader("Cargar archivo Inventario", type=["txt", "csv", "xls", "xlsx"])

    with st.expander("Data Fletes"):
        st.write('Ultima Actualizacion: 03/10/2024')
        uploaded_file = st.file_uploader("Cargar archivo Fletes", type=["txt", "csv", "xls", "xlsx"])


elif seccion == "Dashboard":
    st.header("Dashboard")

    with st.expander("Filtros"):
        # Filtro de selección única
        lista1 = list(df1['fuente_suministro'].unique())
        lista1.insert(0,'todos')
        filtro_1 = st.selectbox(
            "Selecciona Fuente de Suministro:",
            lista1,
            index=23
        )

        if filtro_1=='todos':
            lista2 = list(df1['sku'].unique())
            lista2.insert(0,'todos')
        else:
            lista2 = list(df1[df1['fuente_suministro'] == filtro_1]['sku'].unique())
            lista2.insert(0,'todos')

        filtro_2 = st.selectbox(
            "Selecciona SKU:",
            lista2,
            index=0
        )
            
    # Crear tres columnas para las tarjetas
    col1, col2, col3 = st.columns(3)

    # HTML para tarjetas con estilo
    card_template = """
    <div style="background-color: #f0f0f5; padding: 20px; border-radius: 10px; 
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1); text-align: center; 
            width: 200px; height: 150px; display: flex; flex-direction: column; 
            justify-content: space-between;">
        <p>{title}</p>
        <h3>{content}</h3>
    </div>
    """
    if filtro_1 == 'todos':
        temp1 = df1.copy()
    else:
        temp1 = df1[df1['fuente_suministro']==filtro_1]

    if filtro_2 == 'todos':
        temp2 = temp1.copy()
    else:
        temp2 = df1[df1['sku']==filtro_2]

    ing_sin = temp2['ingreso_usd_sin_recomendacion'].sum()
    ing_con = temp2['ingreso_usd_con_recomendacion'].sum()
    ing_inc = (ing_con - ing_sin) / ing_con
    # Primera tarjeta
    with col1:
        st.markdown(card_template.format(title="Ingresos sin Recomendacion", content=format(ing_sin, ',.0f')), unsafe_allow_html=True)

    # Segunda tarjeta
    with col2:
        st.markdown(card_template.format(title="Ingresos con Recomendacion", content=format(ing_con, ',.0f')), unsafe_allow_html=True)

    # Tercera tarjeta
    with col3:
        st.markdown(card_template.format(title="Incremento", content=format(ing_inc, '.2%')), unsafe_allow_html=True)


    # Datos Grafico
    x = list(temp2['date'].unique())
    y1 = temp2.groupby('date').agg({'ingreso_usd_sin_recomendacion':'sum'})['ingreso_usd_sin_recomendacion']
    y2 = temp2.groupby('date').agg({'ingreso_usd_con_recomendacion':'sum'})['ingreso_usd_con_recomendacion']

    # Crear la figura
    fig = go.Figure()

    # Añadir las líneas
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='Ventas sin Recomendacion', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Ventas con Recomendacion', line=dict(color='orange')))

    # Personalizar el gráfico
    fig.update_layout(title='Ventas con vs sin recomendacion',
                    xaxis_title='X',
                    yaxis_title='Y',
                    showlegend=True)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    st.write('**Alertas Compra**')
    lista_skus = list(temp2['sku'].unique())
    temp_skus = df2[df2['articulo'].isin(lista_skus)].sort_values('index_riesgo').reset_index(drop=True)

    temp_skus = temp_skus.rename(columns={
    'articulo': 'Artículo',
    'stock': 'Inventario',
    'LT_meses': 'Lead Time',
    'compras_recomendadas': 'Recomendación de Compras',
    'demanda_mensual': 'Demanda Mensual',
    'mean_margen': 'Margen Promedio (%)',
    'index_riesgo': 'Índice de Riesgo',
    'riesgo': 'Categoría de Riesgo'})
    

    def highlight_rows(row):
        if row['Categoría de Riesgo'] == 'Rojo':
            return ['background-color: #f69e9b'] * len(row)
        if row['Categoría de Riesgo'] == 'Naranja':
            return ['background-color: #f8dc98'] * len(row)
        elif row['Categoría de Riesgo'] == 'Amarillo':
            return ['background-color: #f6f69b'] * len(row)
        elif row['Categoría de Riesgo'] == 'Verde':
            return ['background-color: #b7f898'] * len(row)
        else:
            return [''] * len(row)
    
    temp_skus_styled = temp_skus.style.format({
        'Inventario': '{:,.0f}',  # Formato para Precio: separar miles y 2 decimales
        'Lead Time': '{:,.0f}',  # Formato para Precio: separar miles y 2 decimales
        'Recomendación de Compras': '{:,.0f}',  # Formato para Precio: separar miles y 2 decimales
        'Demanda Mensual': '{:,.0f}',  # Formato para Precio: separar miles y 2 decimales
        'Margen Promedio (%)': '{:,.2f}',  # Formato para Descuento: porcentaje sin decimales
        'Índice de Riesgo': '{:,.2f}',  # Formato para Descuento: porcentaje sin decimales
    }).apply(highlight_rows, axis=1)  # Aplicar colores a las filas basado en 'Riesgo'

    st.markdown("""
        <style>
        .dataframe th div {
            white-space: normal;
            word-wrap: break-word;
            line-height: 1.1; /* Adjust this value for more spacing if needed */
        }
        </style>
        """, unsafe_allow_html=True)

    st.dataframe(temp_skus_styled, hide_index=True)


elif seccion == "Recomendaciones":

    temp_recom = df2.sort_values('index_riesgo').reset_index(drop=True)

    temp_recom = temp_recom.rename(columns={
    'articulo': 'Artículo',
    'stock': 'Inventario',
    'LT_meses': 'Lead Time',
    'compras_recomendadas': 'Recomendación de Compras',
    'demanda_mensual': 'Demanda Mensual',
    'mean_margen': 'Margen Promedio (%)',
    'index_riesgo': 'Índice de Riesgo',
    'riesgo': 'Categoría de Riesgo'})
    
    def highlight_rows(row):
        if row['Categoría de Riesgo'] == 'Rojo':
            return ['background-color: #f69e9b'] * len(row)
        if row['Categoría de Riesgo'] == 'Naranja':
            return ['background-color: #f8dc98'] * len(row)
        elif row['Categoría de Riesgo'] == 'Amarillo':
            return ['background-color: #f6f69b'] * len(row)
        elif row['Categoría de Riesgo'] == 'Verde':
            return ['background-color: #b7f898'] * len(row)
        else:
            return [''] * len(row)
    
    temp_recom_styled = temp_recom.style.format({
        'Inventario': '{:,.0f}',  # Formato para Precio: separar miles y 2 decimales
        'Lead Time': '{:,.0f}',  # Formato para Precio: separar miles y 2 decimales
        'Recomendación de Compras': '{:,.0f}',  # Formato para Precio: separar miles y 2 decimales
        'Demanda Mensual': '{:,.0f}',  # Formato para Precio: separar miles y 2 decimales
        'Margen Promedio (%)': '{:,.2f}',  # Formato para Descuento: porcentaje sin decimales
        'Índice de Riesgo': '{:,.2f}',  # Formato para Descuento: porcentaje sin decimales
    }).apply(highlight_rows, axis=1)  # Aplicar colores a las filas basado en 'Riesgo'

    temp_recom_styled_cleaned = temp_recom_styled.rename(columns={
        'articulo': 'Artículo',
        'stock': 'Inventario',
        'compras_recomendadas': 'Recomendación de Compras',
        'demanda_mensual': 'Demanda Mensual',
        'mean_margen': 'Margen Promedio (%)',
        'index_riesgo': 'Índice de Riesgo',
        'riesgo': 'Categoría de Riesgo'
    })

    # Opción alternativa con st.dataframe para hacer la tabla interactiva
    st.header("Recomendaciones de compra")
    st.write('Ultima Actualizacion: 03/10/2024')
    st.markdown("""
        <style>
        .dataframe th div {
            white-space: normal;
            word-wrap: break-word;
            line-height: 1.1; /* Adjust this value for more spacing if needed */
        }
        </style>
        """, unsafe_allow_html=True)

    st.dataframe(temp_recom_styled_cleaned, hide_index=True)

    
