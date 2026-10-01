import os
import time
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title='Buscador Multi-Fuente de RUCs - Perú', layout='wide'
)

st.title('🇵🇪 Procesador Inteligente Multi-Fuente de RUCs y Direcciones')
st.write(
    'Esta herramienta cruza información de múltiples plataformas y registros'
    ' oficiales para obtener la dirección, distrito, provincia y región'
    ' verídica de cada empresa.'
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

  st.write(
      f'Total de registros listos para procesar: **{len(df_base)} empresas**'
  )

  if st.button(
      '🚀 Iniciar Extracción Multi-Fuente (Búsqueda en Páginas Oficiales)'
  ):
    progress_bar = st.progress(0)
    status_text = st.empty()

    direcciones = []
    distritos = []
    provincias = []
    departamentos = []

    for i, ruc in enumerate(df_base['RUC']):
      status_text.text(
          f'Consultando RUC {ruc} ({i + 1}/{len(df_base)}) en fuentes'
          ' oficiales...'
      )
      dir_v, dist_v, prov_v, dep_v = (
          'No encontrada',
          'No especificado',
          'No especificado',
          'No especificado',
      )

      # Fuente 1: API oficial principal
      try:
        r = requests.get(f'https://api.apis.net.pe/v1/ruc?numero={ruc}', timeout=3)
        if r.status_code == 200:
          d = r.json()
          if d.get('direccion'):
            dir_v = d.get('direccion', '').strip()
            dist_v = d.get('distrito', 'No especificado').strip()
            prov_v = d.get('provincia', 'No especificado').strip()
            dep_v = d.get('departamento', 'No especificado').strip()
      except Exception:
        pass

      # Fuente 2 de respaldo si la primera no arrojó datos completos
      if dir_v == 'No encontrada' or dep_v == 'No especificado':
        try:
          r2 = requests.get(f'https://openruc.com/api/ruc/{ruc}', timeout=3)
          if r2.status_code == 200:
            d2 = r2.json()
            if d2.get('direccion'):
              dir_v = d2.get('direccion', '').strip()
              dist_v = d2.get('distrito', 'No especificado').strip()
              prov_v = d2.get('provincia', 'No especificado').strip()
              dep_v = d2.get('departamento', 'No especificado').strip()
        except Exception:
          pass

      direcciones.append(dir_v)
      distritos.append(dist_v)
      provincias.append(prov_v)
      departamentos.append(dep_v)

      progress_bar.progress((i + 1) / len(df_base))
      time.sleep(0.15)

    df_base['Direccion'] = direcciones
    df_base['Distrito'] = distritos
    df_base['Provincia'] = provincias
    df_base['Departamento_Region'] = departamentos

    st.session_state['df_multifuente'] = df_base
    status_text.text('¡Extracción multi-fuente finalizada con éxito!')

  # Si ya se procesó, mostramos los resultados interactivos y filtros
  if 'df_multifuente' in st.session_state:
    df_res = st.session_state['df_multifuente']

    st.sidebar.header('Filtros por Región')
    regs = ['TODAS'] + sorted(list(df_res['Departamento_Region'].unique()))
    reg_sel = st.sidebar.selectbox('Seleccione Departamento:', regs)

    if reg_sel != 'TODAS':
      df_res = df_res[df_res['Departamento_Region'] == reg_sel]

    st.subheader(f'Empresas Encontradas ({len(df_res)})')
    st.dataframe(df_res, use_container_width=True)

    # Exportación a Excel limpio
    file_out = 'Empresas_Ubicacion_Verificada.xlsx'
    df_res.to_excel(file_out, index=False)
    with open(file_out, 'rb') as f:
      st.download_button(
          '📥 Descargar Excel Oficial Consolidado',
          f,
          file_name=file_out,
          mime=(
              'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
          ),
      )
else:
  st.error(
      'No se encontró el archivo `TRABAJO.xlsx` en el repositorio. Súbelo para'
      ' continuar.'
  )
