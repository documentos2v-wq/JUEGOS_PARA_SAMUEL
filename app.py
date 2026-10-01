import os
import pandas as pd


def cargar_y_limpiar_datos():
  # Ruta del archivo Excel en tu repositorio
  excel_path = 'TRABAJO.xlsx'

  if not os.path.exists(excel_path):
    print(f'Error: No se encuentra el archivo {excel_path} en el repositorio.')
    return None

  # Cargamos el archivo
  xls = pd.ExcelFile(excel_path)
  df = pd.read_excel(excel_path, sheet_name=xls.sheet_names[0])

  print(f'Total de filas encontradas: {len(df)}')

  # Extraemos los datos de manera limpia
  registros = []

  # 1. Procesamos la primera fila (que en tu Excel original está en los encabezados)
  h_raw = str(df.columns[1])
  h_clean = h_raw.replace('\xa0', '').strip()
  if ':' in h_clean:
    ruc_h = h_clean.split(':')[0].strip()
    emp_h = h_clean.split(':')[1].strip()
  else:
    ruc_h = h_clean
    emp_h = h_clean
  monto_h = str(df.columns[2]).replace('\xa0', '').strip()

  registros.append({'Empresa': emp_h, 'Monto': monto_h, 'RUC': ruc_h})

  # 2. Procesamos el resto de las filas del DataFrame
  for _, row in df.iterrows():
    val_raw = str(row.iloc[1])
    val_clean = val_raw.replace('\xa0', '').strip()

    if ':' in val_clean:
      ruc = val_clean.split(':')[0].strip()
      emp = val_clean.split(':')[1].strip()
    else:
      ruc = val_clean
      emp = val_clean

    monto = str(row.iloc[2]).replace('\xa0', '').strip()
    registros.append({'Empresa': emp, 'Monto': monto, 'RUC': ruc})

  # Creamos un DataFrame limpio y ordenado
  df_limpio = pd.DataFrame(registros)
  print('\nPrimeros registros limpios:')
  print(df_limpio.head(10))

  # Guardamos una versión limpia de prueba
  df_limpio.to_excel('TRABAJO_LIMPIO.xlsx', index=False)
  print(
      '\n¡Carga y limpieza exitosa! Archivo guardado como: TRABAJO_LIMPIO.xlsx'
  )

  return df_limpio


if __name__ == '__main__':
  cargar_y_limpiar_datos()
