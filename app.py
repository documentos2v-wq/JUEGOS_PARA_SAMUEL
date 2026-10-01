import os
import time
import pandas as pd
import requests


def consultar_ruc_oficial(ruc):
  # Consulta a API pública oficial que desglosa distrito, provincia y departamento
  url = f'https://api.apis.net.pe/v1/ruc?numero={ruc}'
  try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
      data = response.json()
      direccion = data.get('direccion', '').strip()
      distrito = data.get('distrito', '').strip()
      provincia = data.get('provincia', '').strip()
      departamento = data.get('departamento', '').strip()

      partes = [p for p in [direccion, distrito, provincia, departamento] if p]
      if partes:
        return ' - '.join(partes)
  except Exception:
    pass

  # Respaldo secundario con OpenRUC si la primera api falla
  try:
    url_alt = f'https://openruc.com/api/ruc/{ruc}'
    response_alt = requests.get(url_alt, timeout=5)
    if response_alt.status_code == 200:
      data_alt = response_alt.json()
      direccion = data_alt.get('direccion', '').strip()
      distrito = data_alt.get('distrito', '').strip()
      provincia = data_alt.get('provincia', '').strip()
      departamento = data_alt.get('departamento', '').strip()

      partes = [p for p in [direccion, distrito, provincia, departamento] if p]
      if partes:
        return ' - '.join(partes)
      elif direccion:
        return direccion
  except Exception:
    pass

  return 'No encontrada'


def procesar_excel():
  excel_path = 'TRABAJO.xlsx'
  if not os.path.exists(excel_path):
    print(f'Error: No se encuentra {excel_path}')
    return

  xls = pd.ExcelFile(excel_path)
  df = pd.read_excel(excel_path, sheet_name=xls.sheet_names[0])

  registros = []

  # Encabezado
  h_raw = str(df.columns[1]).replace('\xa0', '').strip()
  ruc_h = h_raw.split(':')[0].strip() if ':' in h_raw else h_raw
  emp_h = h_raw.split(':')[1].strip() if ':' in h_raw else h_raw
  monto_h = str(df.columns[2]).replace('\xa0', '').strip()
  registros.append({'Empresa': emp_h, 'Monto': monto_h, 'RUC': ruc_h})

  # Resto de filas
  for _, row in df.iterrows():
    val_raw = str(row.iloc[1]).replace('\xa0', '').strip()
    ruc = val_raw.split(':')[0].strip() if ':' in val_raw else val_raw
    emp = val_raw.split(':')[1].strip() if ':' in val_raw else val_raw
    monto = str(row.iloc[2]).replace('\xa0', '').strip()
    registros.append({'Empresa': emp, 'Monto': monto, 'RUC': ruc})

  df_base = pd.DataFrame(registros)
  print(f'Procesando ubicación para {len(df_base)} empresas...')

  direcciones = []
  for idx, ruc in enumerate(df_base['RUC']):
    ubi = consultar_ruc_oficial(ruc)
    direcciones.append(ubi)
    if (idx + 1) % 25 == 0:
      print(f'Progreso: {idx + 1} / {len(df_base)} RUCs consultados...')
    time.sleep(0.2)

  df_base['Direccion_Completa'] = direcciones

  # Guardar resultado final
  output_file = 'TRABAJO_FINAL_UBICACION.xlsx'
  df_base.to_excel(output_file, index=False)
  print(f'\n¡Proceso completado con éxito! Archivo generado: {output_file}')


if __name__ == '__main__':
  procesar_excel()
