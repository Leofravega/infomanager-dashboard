"""
Data loader for Barby InfoManager - loads data from Excel
"""
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Try to load from uploads folder first, then fall back to original
UPLOADS_FOLDER = Path(__file__).parent.parent / "uploads"
UPLOADS_FOLDER.mkdir(exist_ok=True)
EXCEL_FILE = UPLOADS_FOLDER / "data.xlsx"
ORIGINAL_FILE = Path(__file__).parent.parent / "Resumen mensual INFOMANAGER (1).xlsx"

def load_monthly_summary():
    """Load monthly summary data from Excel"""
    try:
        # Try to load from uploads folder first
        if EXCEL_FILE.exists():
            file_to_load = EXCEL_FILE
            print(f"📁 Loading from: {file_to_load}")
        elif ORIGINAL_FILE.exists():
            file_to_load = ORIGINAL_FILE
            print(f"📁 Loading from: {file_to_load}")
        else:
            print(f"⚠️  Excel file not found at {ORIGINAL_FILE}")
            return None
        
        df_raw = pd.read_excel(file_to_load, sheet_name='resumen mensual', header=None)
        
        # Extract months from row 2 (columns 1 onwards)
        months = {
            'ENERO': 1, 'FEBRERO': 2, 'MARZO': 3, 'ABRIL': 4,
            'MAYO': 5, 'JUNIO': 6, 'JULIO': 7, 'AGOSTO': 8,
            'SEPTIEMBRE': 9, 'OCTUBRE': 10, 'NOVIEMBRE': 11, 'DICIEMBRE': 12
        }
        
        month_names = []
        month_cols = []
        
        for col_idx in range(1, df_raw.shape[1]):
            month_name = df_raw.iloc[2, col_idx]
            if pd.notna(month_name) and month_name in months:
                month_names.append(month_name)
                month_cols.append(col_idx)
        
        # Extract metrics from column 0 (starting from row 3)
        metrics = []
        metric_rows = []
        
        for row_idx in range(3, min(22, df_raw.shape[0])):
            metric = df_raw.iloc[row_idx, 0]
            if pd.notna(metric) and metric != '':
                metrics.append(metric)
                metric_rows.append(row_idx)
        
        # Build data dictionary
        data = {'Métrica': metrics}
        
        for month_name, col_idx in zip(month_names, month_cols):
            values = []
            for row_idx in metric_rows:
                val = df_raw.iloc[row_idx, col_idx]
                # Try to convert to float
                try:
                    values.append(float(val) if pd.notna(val) else 0)
                except:
                    values.append(0)
            data[month_name] = values
        
        kpi_df = pd.DataFrame(data)
        return kpi_df
    
    except Exception as e:
        print(f"❌ Error loading Excel: {e}")
        print(f"   Tried: {EXCEL_FILE} and {ORIGINAL_FILE}")
        import traceback
        traceback.print_exc()
        return None

def get_kpi_annual_data():
    """Get KPI data arranged for annual tracking visualization"""
    kpi_df = load_monthly_summary()
    
    if kpi_df is None:
        # Create fallback data when Excel fails to load
        print("⚠️  Using fallback sample data (Excel not found)")
        kpi_df = pd.DataFrame({
            'Métrica': ['Inversión total', 'Leads Ingresados', 'Reuniones', 'CPL', 'CPR'],
            'ENERO': [10000, 150, 45, 66.67, 222.22],
            'FEBRERO': [12000, 165, 50, 72.73, 240.00],
            'MARZO': [11500, 160, 48, 71.88, 239.58],
            'ABRIL': [13000, 175, 55, 74.29, 236.36]
        })
    
    # Prepare data for time series visualization
    month_order = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO',
                   'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
    
    available_months = [m for m in month_order if m in kpi_df.columns]
    
    # Create time series format
    time_series_data = []
    
    for _, row in kpi_df.iterrows():
        metric = row['Métrica']
        for month in available_months:
            try:
                value = float(row[month]) if pd.notna(row[month]) else 0
            except:
                value = 0
            
            time_series_data.append({
                'Métrica': metric,
                'Mes': month,
                'Valor': value
            })
    
    return pd.DataFrame(time_series_data), kpi_df, available_months

if __name__ == '__main__':
    ts_df, kpi_df, months = get_kpi_annual_data()
    print("📊 KPI Summary loaded:")
    print(f"Métricas: {len(kpi_df)}")
    print(f"Meses: {months}")
    print("\nData Preview:")
    print(ts_df.head(10))
