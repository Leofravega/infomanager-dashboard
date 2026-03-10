"""
InfoManager - KPI Dashboard
Panel de inteligencia de negocios para seguimiento mensual de KPIs
"""
import dash
from dash import dcc, html, Input, Output, callback, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import base64
import io
import os

sys.path.insert(0, str(Path(__file__).parent))
from data_generator import get_kpi_annual_data

# Initialize the app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "InfoManager"
server = app.server  # For Gunicorn

# Upload folder
UPLOAD_FOLDER = Path(__file__).parent.parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)
EXCEL_FILE = UPLOAD_FOLDER / "data.xlsx"

# Admin credentials (cambiar en producción)
ADMIN_PASSWORD = "admin123"

# Load data
ts_df, kpi_df, available_months = get_kpi_annual_data()

if kpi_df is None or len(kpi_df) == 0:
    app.layout = html.Div([
        html.H1("⚠️ Error cargando datos"),
        html.P("No se pudo cargar el archivo Excel. Asegúrate de que 'Resumen mensual INFOMANAGER (1).xlsx' esté en la carpeta raíz.")
    ])
else:
    # Month order for proper sorting
    month_order = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO',
                   'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
    month_mapping = {m: i for i, m in enumerate(month_order)}
    
    # Sort available months properly
    available_months_sorted = sorted(available_months, key=lambda x: month_mapping.get(x, 999))
    
    # Key metrics to highlight
    key_metrics = ['Inversión total', 'Leads Ingresados', 'Reuniones', 'CPL', 'CPR']
    
    # Define app layout
    app.layout = html.Div([
        # Header
        html.Div([
            html.Div([
                html.Div([
                    html.Span("📊", style={'fontSize': '30px', 'marginRight': '12px', 'verticalAlign': 'middle'}),
                    html.Span("InfoManager", style={'fontSize': '26px', 'fontWeight': '700', 'letterSpacing': '-0.5px', 'verticalAlign': 'middle'})
                ], style={'margin': 0, 'marginBottom': '6px', 'color': 'white'}),
                html.P("Seguimiento Anual de KPIs · Marketing Intelligence", style={'margin': 0, 'color': '#93c5fd', 'fontSize': '13px', 'letterSpacing': '0.4px'})
            ], style={'flex': 1}),
            html.Div([
                html.P(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                       style={'textAlign': 'right', 'color': '#b0b0b0', 'margin': 0})
            ])
        ], style={
            'background': 'linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #2563eb 100%)',
            'color': 'white',
            'padding': '24px 36px',
            'marginBottom': '30px',
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'boxShadow': '0 4px 24px rgba(15,23,42,0.45)',
            'borderBottom': '3px solid #3b82f6'
        }),
        
        # Main content
        html.Div([
            # Tab navigation
            dcc.Tabs(id='main-tabs', value='tab-1', children=[
                # Tab 1: Resumen Anual
                dcc.Tab(label='📊 Resumen Anual', value='tab-1', children=[
                    html.Div([
                        # Table with all metrics
                        html.H2('Indicadores Clave Anuales', style={'color': '#0f172a', 'marginBottom': '20px', 'fontWeight': '700', 'fontSize': '20px'}),
                        
                        html.Div([
                            dcc.Loading(
                                id="loading-table",
                                type="default",
                                children=[
                                    html.Div(id='kpi-table-container')
                                ]
                            )
                        ], style={
                            'backgroundColor': 'white',
                            'padding': '22px',
                            'borderRadius': '10px',
                            'boxShadow': '0 1px 4px rgba(15,23,42,0.08)',
                            'border': '1px solid #e2e8f0',
                            'marginBottom': '30px'
                        }),
                        
                        # Summary stats
                        html.H2('Resumen General', style={'color': '#0f172a', 'marginBottom': '20px', 'fontWeight': '700', 'fontSize': '20px'}),
                        html.Div(id='summary-cards', style={
                            'display': 'grid',
                            'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
                            'gap': '15px'
                        })
                        
                    ], style={'padding': '20px'})
                ]),
                
                # Tab 2: Análisis de Métricas Principales
                dcc.Tab(label='📈 Métricas Principales', value='tab-2', children=[
                    html.Div([
                        html.H2('Evolución de KPIs a lo Largo del Año', style={'color': '#0f172a', 'marginBottom': '20px', 'fontWeight': '700', 'fontSize': '20px'}),
                        
                        # Selector de métrica
                        html.Div([
                            html.Label('Selecciona una métrica para ver su progresión:', 
                                      style={'fontWeight': '600', 'marginBottom': '10px', 'color': '#374151', 'fontSize': '14px'}),
                            dcc.Dropdown(
                                id='metric-selector',
                                options=[{'label': m, 'value': m} for m in kpi_df['Métrica'].tolist()],
                                value=key_metrics[0] if key_metrics[0] in kpi_df['Métrica'].tolist() else kpi_df['Métrica'].iloc[0],
                                style={'width': '100%'}
                            )
                        ], style={
                            'marginBottom': '30px',
                            'backgroundColor': 'white',
                            'padding': '15px',
                            'borderRadius': '8px',
                            'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
                        }),
                        
                        # Main chart
                        html.Div([
                            dcc.Loading(
                                id="loading-chart",
                                type="default",
                                children=[
                                    dcc.Graph(id='metric-trend-chart')
                                ]
                            )
                        ], style={
                            'backgroundColor': 'white',
                            'padding': '15px',
                            'borderRadius': '8px',
                            'boxShadow': '0 1px 3px rgba(0,0,0,0.1)',
                            'marginBottom': '30px'
                        }),
                        
                        # Statistics
                        html.Div(id='metric-stats', style={
                            'display': 'grid',
                            'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
                            'gap': '15px'
                        })
                        
                    ], style={'padding': '20px'})
                ]),
                
                # Tab 3: Comparativa Mensual
                dcc.Tab(label='📋 Vista Mensual', value='tab-3', children=[
                    html.Div([
                        html.H2('Comparativa por Mes', style={'color': '#0f172a', 'marginBottom': '20px', 'fontWeight': '700', 'fontSize': '20px'}),
                        
                        html.Div([
                            html.Label('Selecciona un mes para ver todos los KPIs:', 
                                      style={'fontWeight': '600', 'marginBottom': '10px', 'color': '#374151', 'fontSize': '14px'}),
                            dcc.Dropdown(
                                id='month-selector',
                                options=[{'label': m, 'value': m} for m in available_months_sorted],
                                value=available_months_sorted[-1] if available_months_sorted else 'ENERO',
                                style={'width': '100%'}
                            )
                        ], style={
                            'marginBottom': '30px',
                            'backgroundColor': 'white',
                            'padding': '15px',
                            'borderRadius': '8px',
                            'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
                        }),
                        
                        # Monthly metrics table
                        html.Div(id='monthly-table', style={
                            'backgroundColor': 'white',
                            'padding': '15px',
                            'borderRadius': '8px',
                            'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
                        })
                        
                    ], style={'padding': '20px'})
                ]),
                
                # Tab 4: Admin Panel
                dcc.Tab(label='🔐 Admin', value='tab-4', children=[
                    html.Div([
                        html.Div(id='admin-login-section', children=[
                            html.H2('Panel Administrativo', style={'color': '#0f172a', 'marginBottom': '20px', 'fontWeight': '700', 'fontSize': '20px'}),
                            html.Div([
                                html.P('Ingresa la contraseña para acceder:', style={'marginBottom': '10px'}),
                                dcc.Input(
                                    id='admin-password',
                                    type='password',
                                    placeholder='Contraseña',
                                    style={
                                        'width': '100%',
                                        'padding': '10px',
                                        'marginBottom': '10px',
                                        'border': '1px solid #ddd',
                                        'borderRadius': '4px',
                                        'fontSize': '14px'
                                    }
                                ),
                                html.Button(
                                    'Ingresar',
                                    id='admin-login-btn',
                                    n_clicks=0,
                                    style={
                                        'width': '100%',
                                        'padding': '10px',
                                        'backgroundColor': '#2563eb',
                                        'color': 'white',
                                        'border': 'none',
                                        'borderRadius': '6px',
                                        'cursor': 'pointer',
                                        'fontSize': '14px',
                                        'fontWeight': '600',
                                        'letterSpacing': '0.3px',
                                        'transition': 'background-color 0.2s'
                                    }
                                ),
                                html.Div(id='admin-login-message', style={'marginTop': '10px', 'color': 'red'})
                            ], style={
                                'maxWidth': '400px',
                                'backgroundColor': 'white',
                                'padding': '20px',
                                'borderRadius': '8px',
                                'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
                            })
                        ]),
                        dcc.Store(id='admin-auth', data={'authenticated': False})
                    ], style={'padding': '20px'})
                ])
            ], style={'fontSize': '15px'},
               colors={'border': '#e2e8f0', 'primary': '#2563eb', 'background': '#f8fafc'})
            
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 20px'})
        
    ], style={
        'fontFamily': "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        'backgroundColor': '#f1f5f9',
        'minHeight': '100vh',
        'paddingBottom': '40px'
    })
    
    # Callbacks
    @callback(
        Output('kpi-table-container', 'children'),
        Input('main-tabs', 'value')
    )
    def update_kpi_table(_):
        """Display KPI table with all metrics"""
        
        # Format the dataframe for display
        display_df = kpi_df.copy()
        
        # Reorder columns
        cols = ['Métrica'] + available_months_sorted
        display_df = display_df[cols]
        
        # Format numeric values
        for col in available_months_sorted:
            display_df[col] = display_df[col].apply(
                lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) and x > 1000 
                else f"{x:,.2f}" if isinstance(x, (int, float)) 
                else str(x)
            )
        
        # Create table
        table = html.Table([
            html.Thead(
                html.Tr([
                    html.Th(col, style={
                        'backgroundColor': '#1e3a8a',
                        'color': 'white',
                        'padding': '13px 14px',
                        'textAlign': 'left',
                        'fontWeight': '600',
                        'borderBottom': '3px solid #2563eb',
                        'fontSize': '12px',
                        'letterSpacing': '0.4px',
                        'textTransform': 'uppercase'
                    }) for col in display_df.columns
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(
                        row[col],
                        style={
                            'padding': '11px 14px',
                            'borderBottom': '1px solid #e2e8f0',
                            'backgroundColor': '#f8fafc' if i % 2 == 0 else 'white',
                            'fontWeight': '600' if col == 'Métrica' else 'normal',
                            'color': '#1e3a8a' if col == 'Métrica' else '#334155',
                            'fontSize': '13px'
                        }
                    )
                    for col in display_df.columns
                ], style={'height': '44px'})
                for i, (idx, row) in enumerate(display_df.iterrows())
            ])
        ], style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'fontSize': '13px'
        })
        
        return table
    
    @callback(
        Output('summary-cards', 'children'),
        Input('main-tabs', 'value')
    )
    def update_summary_cards(_):
        """Display key metric summary cards"""
        
        cards = []
        
        for metric in key_metrics:
            if metric in kpi_df['Métrica'].values:
                metric_row = kpi_df[kpi_df['Métrica'] == metric].iloc[0]
                
                # Get latest and first values
                latest_val = metric_row[available_months_sorted[-1]] if available_months_sorted else 0
                first_val = metric_row[available_months_sorted[0]] if available_months_sorted else 0
                
                # Calculate change
                if first_val != 0:
                    change_pct = ((latest_val - first_val) / first_val) * 100
                else:
                    change_pct = 0
                
                change_color = '#10b981' if change_pct >= 0 else '#ef4444'
                change_bg    = '#d1fae5' if change_pct >= 0 else '#fee2e2'
                change_symbol = '↗️' if change_pct >= 0 else '↘️'
                
                card = html.Div([
                    html.H4(metric, style={'margin': '0 0 10px 0', 'color': '#64748b', 'fontSize': '12px', 'textTransform': 'uppercase', 'letterSpacing': '0.5px', 'fontWeight': '600'}),
                    html.H2(f"{latest_val:,.0f}" if latest_val > 100 else f"{latest_val:,.2f}", 
                           style={'margin': '0 0 5px 0', 'color': '#0f172a', 'fontSize': '28px', 'fontWeight': '700'}),
                    html.P(f"{change_symbol} {change_pct:+.1f}% vs {available_months_sorted[0]}" if available_months_sorted else "",
                          style={'margin': '8px 0 0 0', 'color': change_color, 'fontSize': '12px', 'fontWeight': '600',
                                 'backgroundColor': change_bg, 'display': 'inline-block',
                                 'padding': '2px 8px', 'borderRadius': '12px'})
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px 22px',
                    'borderRadius': '10px',
                    'boxShadow': '0 1px 4px rgba(15,23,42,0.08)',
                    'borderTop': f'3px solid {change_color}',
                    'transition': 'box-shadow 0.2s'
                })
                cards.append(card)
        
        return cards
    
    @callback(
        Output('metric-trend-chart', 'figure'),
        Input('metric-selector', 'value')
    )
    def update_metric_chart(selected_metric):
        """Display trend chart for selected metric"""
        
        metric_data = ts_df[ts_df['Métrica'] == selected_metric].copy()
        
        # Sort by month
        metric_data['Mes_Num'] = metric_data['Mes'].map(month_mapping)
        metric_data = metric_data.sort_values('Mes_Num')
        
        # Create figure
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=metric_data['Mes'],
            y=metric_data['Valor'],
            mode='lines+markers',
            name=selected_metric,
            line=dict(color='#2563eb', width=3),
            marker=dict(size=8, color='#2563eb', line=dict(color='white', width=2)),
            fill='tozeroy',
            fillcolor='rgba(37, 99, 235, 0.1)',
            hovertemplate='<b>%{x}</b><br>Valor: %{y:,.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=f'<b>Evolución:</b> {selected_metric}', font=dict(size=16, color='#0f172a', family='Inter, Segoe UI')),
            xaxis_title='Mes',
            yaxis_title='Valor',
            template='plotly_white',
            height=420,
            hovermode='x unified',
            margin=dict(t=50, b=50, l=70, r=30),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(family='Inter, Segoe UI', color='#334155'),
            xaxis=dict(gridcolor='#f1f5f9', tickfont=dict(size=12)),
            yaxis=dict(gridcolor='#f1f5f9', tickfont=dict(size=12)),
            hoverlabel=dict(bgcolor='#1e3a8a', font=dict(color='white', size=13))
        )
        
        return fig
    
    @callback(
        Output('metric-stats', 'children'),
        Input('metric-selector', 'value')
    )
    def update_metric_stats(selected_metric):
        """Display statistics for selected metric"""
        
        metric_data = ts_df[ts_df['Métrica'] == selected_metric].copy()
        values = metric_data['Valor'].values
        
        if len(values) == 0:
            return []
        
        import numpy as np
        stats = [
            ('Promedio', np.mean(values)),
            ('Máximo', np.max(values)),
            ('Mínimo', np.min(values)),
            ('Últimas 3 meses', np.mean(values[-3:]) if len(values) >= 3 else np.mean(values))
        ]
        
        stat_cards = []
        colors = ['#2563eb', '#10b981', '#ef4444', '#f59e0b']
        
        for idx, (label, value) in enumerate(stats):
            stat_cards.append(
                html.Div([
                    html.P(label, style={'margin': '0', 'color': '#64748b', 'fontSize': '11px', 'fontWeight': '600',
                                         'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                    html.H3(f"{value:,.2f}", style={'margin': '8px 0 0 0', 'color': colors[idx], 'fontSize': '22px', 'fontWeight': '700'})
                ], style={
                    'backgroundColor': 'white',
                    'padding': '18px 20px',
                    'borderRadius': '10px',
                    'boxShadow': '0 1px 4px rgba(15,23,42,0.08)',
                    'borderTop': f'3px solid {colors[idx]}'
                })
            )
        
        return stat_cards
    
    @callback(
        Output('monthly-table', 'children'),
        Input('month-selector', 'value')
    )
    def update_monthly_table(selected_month):
        """Display all metrics for selected month"""
        
        if selected_month not in kpi_df.columns:
            return html.P("No hay datos para este mes")
        
        monthly_data = kpi_df[['Métrica', selected_month]].copy()
        monthly_data.columns = ['Métrica', 'Valor']
        
        # Sort by value
        try:
            monthly_data['Valor_Num'] = pd.to_numeric(monthly_data['Valor'], errors='coerce')
            monthly_data = monthly_data.sort_values('Valor_Num', ascending=False, na_position='last')
        except:
            pass
        
        # Format values
        monthly_data['Valor_Display'] = monthly_data['Valor'].apply(
            lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) and x > 100 
            else f"{x:,.4f}" if isinstance(x, (int, float)) 
            else str(x)
        )
        
        # Create table
        table = html.Table([
            html.Thead(
                html.Tr([
                    html.Th('Métrica', style={
                        'backgroundColor': '#1e3a8a',
                        'color': 'white',
                        'padding': '13px 14px',
                        'textAlign': 'left',
                        'fontWeight': '600',
                        'borderBottom': '3px solid #2563eb',
                        'fontSize': '12px',
                        'letterSpacing': '0.4px',
                        'textTransform': 'uppercase'
                    }),
                    html.Th(f'{selected_month}', style={
                        'backgroundColor': '#1e3a8a',
                        'color': 'white',
                        'padding': '13px 14px',
                        'textAlign': 'right',
                        'fontWeight': '600',
                        'borderBottom': '3px solid #2563eb',
                        'fontSize': '12px',
                        'letterSpacing': '0.4px',
                        'textTransform': 'uppercase'
                    })
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(row['Métrica'], style={
                        'padding': '12px',
                        'borderBottom': '1px solid #e0e0e0',
                        'backgroundColor': '#fafafa' if i % 2 == 0 else 'white',
                        'fontWeight': 'bold'
                    }),
                    html.Td(row['Valor_Display'], style={
                        'padding': '12px',
                        'borderBottom': '1px solid #e0e0e0',
                        'backgroundColor': '#fafafa' if i % 2 == 0 else 'white',
                        'textAlign': 'right'
                    })
                ])
                for i, (idx, row) in enumerate(monthly_data.iterrows())
            ])
        ], style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'fontSize': '13px'
        })
        
        return table
    
    # Admin callbacks
    @callback(
        [Output('admin-login-section', 'children'),
         Output('admin-auth', 'data')],
        Input('admin-login-btn', 'n_clicks'),
        State('admin-password', 'value'),
        State('admin-auth', 'data'),
        prevent_initial_call=True
    )
    def verify_admin_password(n_clicks, password, auth_data):
        """Verify admin password and show upload panel"""
        
        if not password:
            return html.Div([
                html.P('Por favor ingresa la contraseña', style={'color': 'red'})
            ]), auth_data
        
        if password == ADMIN_PASSWORD:
            # Show upload panel
            admin_panel = html.Div([
                html.H2('Panel Administrativo', style={'color': '#0f172a', 'marginBottom': '20px', 'fontWeight': '700', 'fontSize': '20px'}),
                html.Div([
                    html.H3('Cargar Nuevo Archivo Excel', style={'color': '#1e3a8a', 'marginBottom': '15px', 'fontWeight': '600'}),
                    dcc.Upload(
                        id='upload-excel',
                        children=html.Div([
                            '📁 Arrastra y suelta o ',
                            html.A('selecciona un archivo Excel')
                        ]),
                        style={
                            'width': '100%',
                            'height': '110px',
                            'lineHeight': '110px',
                            'borderWidth': '2px',
                            'borderStyle': 'dashed',
                            'borderColor': '#cbd5e1',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'cursor': 'pointer',
                            'backgroundColor': '#f8fafc',
                            'color': '#64748b',
                            'fontSize': '14px',
                            'marginBottom': '20px',
                            'transition': 'border-color 0.2s, background-color 0.2s'
                        },
                        multiple=False,
                        accept='.xlsx,.xls'
                    ),
                    html.Div(id='upload-message', style={
                        'padding': '15px',
                        'borderRadius': '8px',
                        'marginTop': '15px'
                    }),
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 1px 3px rgba(0,0,0,0.1)',
                    'maxWidth': '600px'
                })
            ])
            
            return admin_panel, {'authenticated': True}
        else:
            return html.Div([
                html.P('Contraseña incorrecta', style={'color': 'red', 'fontSize': '14px'})
            ]), auth_data
    
    @callback(
        Output('upload-message', 'children'),
        Input('upload-excel', 'contents'),
        State('upload-excel', 'filename'),
        prevent_initial_call=True
    )
    def handle_file_upload(contents, filename):
        """Handle Excel file upload and reload data"""
        
        if not contents:
            return ""
        
        try:
            # Decode the uploaded file
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            
            # Save the file
            with open(EXCEL_FILE, 'wb') as f:
                f.write(decoded)
            
            # Try to load the new data
            from importlib import reload
            import src.data_generator as dg
            reload(dg)
            
            global ts_df, kpi_df, available_months
            ts_df, kpi_df, available_months = dg.get_kpi_annual_data()
            
            message = html.Div([
                html.P('✅ Archivo cargado exitosamente', style={'color': '#2e7d32', 'fontWeight': 'bold'}),
                html.P(f'📊 Métricas: {len(kpi_df)}, Meses: {len(available_months)}', style={'color': '#666'}),
                html.P('El reporte se ha actualizado automáticamente.', style={'color': '#666', 'fontSize': '12px'})
            ], style={'backgroundColor': '#c8e6c9', 'padding': '15px', 'borderRadius': '4px'})
            
            return message
            
        except Exception as e:
            return html.Div([
                html.P('❌ Error al cargar el archivo', style={'color': '#c62828', 'fontWeight': 'bold'}),
                html.P(str(e), style={'color': '#666', 'fontSize': '12px'})
            ], style={'backgroundColor': '#ffcdd2', 'padding': '15px', 'borderRadius': '4px'})

if __name__ == '__main__':
    print("🚀 Iniciando InfoManager...")
    port = int(os.environ.get('PORT', 8050))
    print(f"📍 Accede a http://localhost:{port}")
    if kpi_df is not None:
        print(f"📊 Datos cargados: {len(kpi_df)} métricas, {len(available_months)} meses")
    app.run_server(debug=True, port=port, host='0.0.0.0')
