import numpy as np
import plotly.express as px
import yfinance as yf
import datetime
#lista de acciones a importar de las empresas que se dedican a consumo masivo y produccion industrial
stocks=['NESN.SW','PG','KA','GE','ETR','CAT']

#rango de fechas a importat
end_date=datetime.datetime.now()
start_date=end_date-datetime.timedelta(days=3*365) #5 anios

#crear un dataframe vacio para almacenar los datos
historical_data=yf.download(stocks,start=start_date,end=end_date)['Adj Close']

#calcular retornos diarios
returns_data=historical_data.pct_change().dropna()
#usamos rpecios ajustados

#guardar en csv
historical_data.to_csv('stock_prices.csv')
returns_data.to_csv('stock_returns.csv')

print(historical_data.head())
print(returns_data.head())
import pandas as pd
import datetime
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
# Iniciar la app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Prices and Returns Dashboard"),
    
    # Dropdown para seleccionar la acción
    html.Label("Select Stock"),
    dcc.Dropdown(id='stock-dropdown', options=[{'label': stock, 'value': stock} for stock in stocks], value=stocks[0], multi=True),
    
    # Dropdown para seleccionar precios o retornos
    html.Label("Select Data Type"),
    dcc.Dropdown(id='data-type-dropdown', options=[
        {'label': 'Closing Prices', 'value': 'price'},
        {'label': 'Returns', 'value': 'return'}
    ], value='price'),
    
    # Slicer para el rango de fechas
    dcc.DatePickerRange(
        id='date-range',
        start_date=start_date,
        end_date=end_date,
        display_format='YYYY-MM-DD'
    ),
    
    # Gráfico
    dcc.Graph(id='stock-graph')
])
# Callback para actualizar el gráfico
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('data-type-dropdown', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_graph(selected_stocks, data_type, start_date, end_date):
    # Filtrar los datos por el rango de fechas
    filtered_data = historical_data.loc[start_date:end_date, selected_stocks]
    if data_type == 'return':
        filtered_data = returns_data.loc[start_date:end_date, selected_stocks]
    
    # Crear la figura
    fig = px.line(filtered_data, x=filtered_data.index, y=filtered_data.columns)
    fig.update_layout(title="Stock Prices and Returns", xaxis_title="Date", yaxis_title="Value")
    
    return fig

if __name__ == '__main__':
    app.run_server(port=1590,debug=True)
  import pyfolio as pf
import warnings
warnings.filterwarnings('ignore')
performanceCAT=pf.timeseries.perf_stats(returns_data['CAT'])
print(performanceCAT)
performanceETR=pf.timeseries.perf_stats(returns_data['ETR'])
print(performanceETR)
performanceGE=pf.timeseries.perf_stats(returns_data['GE'])
print(performanceGE)
performanceNESN=pf.timeseries.perf_stats(returns_data['NESN.SW'])
print(performanceNESN)
performancePG=pf.timeseries.perf_stats(returns_data['PG'])
print(performancePG)
performanceKA=pf.timeseries.perf_stats(returns_data['KA'])
print(performanceKA)
historical_data.to_csv("stock_prices,csv", index = False)
file_path= "stock_prices,csv"
data = pd.read_csv(file_path)
returns = data.pct_change()
returns
meanDailyReturns = returns.mean()
meanDailyReturns
#Definir pesos del portafolio
pesos = np.array([0.17,0.17,0.17,0.17,0.16,0.16])
#Retorno del Portafolio
portReturns=np.sum(meanDailyReturns*pesos)
portReturns 
returns["Portafolio"] = returns.dot(pesos)
returns
daily_cum_ret = (1+returns).cumprod()
print(daily_cum_ret.tail())
fig = px.line(daily_cum_ret, x=daily_cum_ret.index,y=['NESN.SW','PG','KA','GE','ETR','CAT'],
             line_shape="linear")
fig.show()
fig = px.line(daily_cum_ret, x=daily_cum_ret.index, y="Portafolio", line_shape="linear")
fig.show() 
total_return = (data["NESN.SW"].iloc[-1] - data["NESN.SW"].iloc[0]) / data["NESN.SW"].iloc[0]
total_return

# Retorno Anualizado NESN.SW
annualized_return = ((1 + total_return) ** (12 / 60)) - 1
print(annualized_return)
total_return = (data["PG"].iloc[-1]-data["PG"].iloc[0])/data["PG"].iloc[0]
total_return
#Retorno Anualizado PG
annualized_return = ((1+total_return)**(12/60))-1
annualized_return 
#Retorno total
total_return = (data["GE"].iloc[-1]-data["GE"].iloc[0])/data["GE"].iloc[0]
total_return
#Retorno Anualizado GE
annualized_return = ((1+total_return)**(12/60))-1
annualized_return 
#Retorno total
total_return = (data["ETR"].iloc[-1]-data["ETR"].iloc[0])/data["ETR"].iloc[0]
total_return
#Retorno Anualizado ETR
annualized_return = ((1+total_return)**(12/60))-1
annualized_return 
#Retorno total
total_return = (data["CAT"].iloc[-1]-data["CAT"].iloc[0])/data["CAT"].iloc[0]
total_return
#Retorno Anualizado CAT
annualized_return = ((1+total_return)**(12/60))-1
annualized_return 
import pyfolio as pf
import warnings
warnings.filterwarnings("ignore")
import pyfolio as pf
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.efficient_frontier import EfficientFrontier
import matplotlib.pyplot as pl
mu = expected_returns.mean_historical_return(historical_data)
print(mu)
sigma = risk_models.sample_cov(historical_data)
print(sigma)
ef = EfficientFrontier(mu,sigma)
ef
maxsharpe = ef.max_sharpe()
weights_maxsharpe = ef.clean_weights()
print(maxsharpe, weights_maxsharpe) #Portafolio con Max Sharpe
ef = EfficientFrontier(mu,sigma)
minvol = ef.min_volatility()
weights_minvol = ef.clean_weights()
print(weights_minvol) #Portafolio con Varianza Mín
#7
pesos2 = np.array([0.0985,0.2707,0.6309,0.0,0.0,0.0])
pesos2
portReturns2=np.sum(meanDailyReturns*pesos2)
portReturns2
pesos3 = np.array([0.11023,0.08255,0.05156,0.00885,0.43461,0.3122])
pesos3
portReturns3=np.sum(meanDailyReturns*pesos3)
portReturns3
meanDailyReturns2 = meanDailyReturns.drop(columns='Portafolio')
meanDailyReturns2
returns2 = returns.drop(columns=['Portafolio'])
returns2
returns2["Portafolio"] = returns2.dot(pesos2)
print(returns2)
performance2 = pf.timeseries.perf_stats(returns2["Portafolio"])
print(performance2)
#MAX SHARPE
fig = px.histogram(returns2, x="Portafolio")
fig.show()
meanDailyReturns3 = meanDailyReturns.drop(columns='Portafolio')
meanDailyReturns3
returns3 = returns.drop(columns=['Portafolio'])
returns3
returns3["Portafolio"] = returns3.dot(pesos3)
print(returns3)
performance3 = pf.timeseries.perf_stats(returns3["Portafolio"])
print(performance3)
#MIN VOLATILITY
fig = px.histogram(returns3, x="Portafolio")
fig.show()
