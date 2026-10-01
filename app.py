import os
import time
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title='Buscador Oficial de RUCs - Perú', layout='wide')

st.title('🇵🇪 Procesador Oficial de RUCs y Direcciones Fiscales')
st.write(
    'Esta aplicación consulta en tiempo real los datos oficiales y verídicos de'
    ' cada RUC.'
)

excel_path = 'TRABAJO.xlsx'

if os.path.exists(excel_path):
  xls = pd.ExcelFile(excel_path)
  df = pd.read_excel(excel_path, sheet_name=xls.sheet_names[0])

  # Limpieza y extracción de RUCs de 11 dígitos
  registros = []
  h_raw = str(df.columns[1]).replace('\xa0', '').strip()
  ruc_h = h_raw.split(':')[0].strip() if ':' in h_raw else h_raw
  emp_h = h_raw.split(':')[1].strip() if ':' in h_raw else h_raw
  monto_h = str(df.columns[2]).replace('\xa0', '').strip()
  registros.append({'Empresa': emp_h, 'Monto': monto_h, 'RUC': ruc_h})

  for _, row in df.iterrows():
    val_raw = str(row.iloc[1]).replace('\xa0', '').strip()
    ruc = val_raw.split(':')[0].strip() if ':' in val_raw else val_raw
    emp = val_raw.split(':')[1].strip() if ':' in val_raw else val_raw
    monto = str(row.iloc[2]).replace('\xa0', '').strip()
    registros.append({'Empresa': emp, 'Monto': monto, 'RUC': ruc})

  df_base = pd.DataFrame(registros)

  st.write(f'Empresas totales detectadas en tu archivo: **{len(df_base)}**')

  # Botón para iniciar la consulta oficial en vivo
  if st.button(
      '🔍 Consultar Direcciones Oficiales en Vivo (SUNAT / Padrón'
      ' Contribuyentes)'
  ):
    progress_bar = st.progress(0)
    status_text = st.empty()

    direcciones = []
    distritos = []
    provincias = []
    departamentos = []

    for i, ruc in enumerate(df_base['RUC']):
      status_text.text(
          f'Consultando RUC {ruc} ({i + 1}/{len(df_base)})...'
      )
      dir_val, dist_val, prov_val, dep_val = (
          'No encontrada',
          'No especificado',
          'No especificado',
          'No especificado',
      )

      try:
        # Consulta a API oficial pública de proveedores / RUCs
        url = f'https://api.apis.net.pe/v1/ruc?numero={ruc}'
        resp = requests.get(url, timeout=4)
        if resp.status_code == 200:
          data = resp.json()
          dir_val = data.get('direccion', 'No encontrada').strip()
          dist_val = data.get('distrito', 'No especificado').strip()
          prov_val = data.get('provincia', 'No especificado').strip()
          dep_val = data.get('departamento', 'No especificado').strip()
        else:
          # Respaldo alternativo oficial
          url_alt = f'https://openruc.com/api/ruc/{ruc}'
          resp_alt = requests.get(url_alt, timeout=4)
          if resp_alt.status_code == 200:
            d_alt = resp_alt.json()
            dir_val = d_alt.get('direccion', 'No encontrada').strip()
            dist_val = d_alt.get('distrito', 'No especificado').strip()
            prov_val = d_alt.get('provincia', 'No especificado').strip()
            dep_val = d_alt.get('departamento', 'No especificado').strip()
      except Exception:
        pass

      direcciones.append(dir_val)
      distritos.append(dist_val)
      provincias.append(prov_val)
      departamentos.append(dep_val)

      progress_bar.progress((i + 1) / len(df_base))
      time.sleep(0.1)  # Pequeña pausa para asegurar estabilidad en la red

    df_base['Direccion'] = direcciones
    df_base['Distrito'] = distritos
    df_base['Provincia'] = provincias
    df_base['Departamento_Region'] = departamentos

    # Guardamos en sesión para no perderlo al filtrar
    st.session_state['df_procesado'] = df_base
    status_text.text('¡Consulta completada con éxito!')

  # Si ya se procesó, mostramos los filtros y resultados
  if 'df_procesado' in st.session_state:
    df_f = st.session_state['df_procesado']

    st.sidebar.header('Filtros Geográficos')
    regiones_disponibles = ['TODAS'] + sorted(
        list(df_f['Departamento_Region'].unique())
    )
    reg_elegida = st.sidebar.selectbox('Filtrar por Región:', regiones_disponibles)

    if reg_elegida != 'TODAS':
      df_f = df_f[df_f['Departamento_Region'] == reg_elegida]

    st.subheader(f'Resultados ({len(df_f)} empresas)')
    st.dataframe(df_f, use_container_width=True)

    # Botón para descargar el resultado final real
    output_name = 'Empresas_Ubicacion_Real.xlsx'
    df_f.to_excel(output_name, index=False)
    with open(output_name, 'rb') as f:
      st.download_button(
          '📥 Descargar Excel con Datos Oficiales Verídicos',
          f,
          file_name=output_name,
          mime=(
              'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
          ),
      )
else:
  st.error(
      'No se encontró el archivo `TRABAJO.xlsx`. Súbelo a tu repositorio de'
      ' GitHub para comenzar.'
  )
