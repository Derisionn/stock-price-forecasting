import dateutil.relativedelta
import plotly.graph_objects as go 
import dateutil
import pandas as pd 
import datetime
import ta
import pandas_ta as pta


# def plotly_table(dataframe):
#     headerColor='grey'
#     rowEvenColor='blue'
#     rowOddColor='white'
    
    
#     fig=go.Figure(data=[go.Table(header=dict(
#         values=["<b><b>"]+["<b>"+str(i)[:10]+"<b>" for i in dataframe.columns],
#         line_color='#0078ff',fill_color='#0078ff',
#         align = 'center',font=dict(color='white',size=15),height=35,
#     ),
#     cells=dict(
#         values=[[]]
#     )
#                                  )])

def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = '#f8f8ff'
    rowOddColor = '#e1efff'

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b><b>"]+["<b>"+str(i)[:10] + "</b>" for i in dataframe.columns],
            line_color='#0078ff',
            fill_color='#0078ff',
            align='center',
            font=dict(color='white', size=15),
            height=35
        ),
        cells=dict(
            values=[["<b>" + str(i) + "<b>" for i in dataframe.index]] +
                   [dataframe[i] for i in dataframe.columns],
            align='left',
            line_color='white',
            font=dict(color='black', size=15),
            fill_color=[rowOddColor, rowEvenColor]
        )
    )])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig





import dateutil.relativedelta as rd

def filter_data(dataframe, num_period):
    last_date = dataframe.index[-1]

    if num_period == '1mo':
        date = last_date - rd.relativedelta(months=1)

    elif num_period == '5d':
        date = last_date - rd.relativedelta(days=5)

    elif num_period == '6mo':
        date = last_date - rd.relativedelta(months=6)

    elif num_period == '1y':
        date = last_date - rd.relativedelta(years=1)

    elif num_period == '5y':
        date = last_date - rd.relativedelta(years=5)

    elif num_period == 'ytd':
        date = pd.Timestamp(f"{last_date.year}-01-01")

    else:
        date = dataframe.index[0]

    # Reset index once and filter
    df = dataframe.reset_index()
    return df[df['Date'] > date]




    
    
    
def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Open'],
        mode='lines',
        name='Open',
        line=dict(width=2, color='#5ab7ff')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Close'],
        mode='lines',
        name='Close',
        line=dict(width=2, color='black')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['High'],
        mode='lines',
        name='High',
        line=dict(width=2, color='#0078ff')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Low'],
        mode='lines',
        name='Low',
        line=dict(width=2, color='red')
    ))
    fig.update_xaxes(
    tickformat='%b %Y',      # X-axis format: Jan 2025
    dtick="M1",              # Tick every month (optional)
    tickangle=45,             # Rotate labels if needed
    tickfont=dict(size=12, color='black')
    )

    fig.update_yaxes(
    dtick=50,                # Tick every 10 units on Y-axis
    tickprefix='$',          # Add dollar sign before Y-axis values
    tickfont=dict(size=12, color='black')
    )

    fig.update_xaxes(rangeslider_visible=True)

    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(
                family='Arial',
                size=12,
                color='blue'
            )
        )
    )

    return fig


def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['RSI'],
        name='RSI',
        marker_color='orange',
        line=dict(width=2, color='orange'),
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[70]*len(dataframe),
        name='Overbought',
        marker_color='red',
        line=dict(width=2, color='red', dash='dash'),
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[30]*len(dataframe),
        fill='tonexty',
        name='Oversold',
        marker_color='#79da84',
        line=dict(width=2, color='#79da84', dash='dash'),
    ))
    
    
    fig.update_xaxes(
        
    tickformat='%b %Y',      
    dtick="M1",              
    tickangle=45,            
    tickfont=dict(size=10, color='black')
    
    
    )

    fig.update_yaxes(
        
    dtick=20,                
    tickprefix='$',          
    tickfont=dict(size=10, color='black')
    
    
    )

    fig.update_layout(
    yaxis_range=[0, 100],
    height=200,
    plot_bgcolor='white',
    paper_bgcolor='#e1efff',
    margin=dict(l=0, r=20, t=20, b=0),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(
                family='Arial',
                size=12,
                color='blue'
            )
    )
)

    return fig




def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=dataframe['Date'],
        open=dataframe['Open'],
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close']
    ))
    
    fig.update_xaxes(
    tickformat='%b %Y',      # X-axis format: Jan 2025
    dtick="M1",              # Tick every month (optional)
    tickangle=45,             # Rotate labels if needed
    tickfont=dict(size=12, color='black')
    )

    fig.update_yaxes(
    dtick=50,                # Tick every 10 units on Y-axis
    tickprefix='$',          # Add dollar sign before Y-axis values
    tickfont=dict(size=12, color='black')
    )

    fig.update_layout(
    height=500,
    plot_bgcolor='white',
    paper_bgcolor='#e1efff',  # ✅ fixed color
    margin=dict(l=20, r=20, t=20, b=20),
    legend=dict(orientation="h",
                font=dict(
                family='Arial',
                size=12,
                color='blue'
            ))  # ✅ legend anchor can go here
    )

    return fig



def MACD(dataframe, num_period):
    # Calculate MACD using pandas_ta
    macd_full = pta.macd(dataframe['Close'])
    macd = macd_full.iloc[:, 0]         # MACD Line
    macd_signal = macd_full.iloc[:, 1]  # Signal Line
    macd_hist = macd_full.iloc[:, 2]    # Histogram

    # Assign to dataframe
    dataframe['MACD'] = macd
    dataframe['MACD Signal'] = macd_signal
    dataframe['MACD Hist'] = macd_hist

    # Filter last N periods
    dataframe = filter_data(dataframe, num_period)

    # Initialize figure
    fig = go.Figure()

    # MACD Line
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'],
        name='MACD',
        marker_color='orange',
        line=dict(width=2, color='orange')
    ))

    # Signal Line
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'],
        name='Signal',
        marker_color='red',
        line=dict(width=2, color='red', dash='dash')
    ))

    # Color-coded histogram bars
    c = ['red' if cl < 0 else 'green' for cl in dataframe['MACD Hist']]

    fig.add_trace(go.Bar(
        x=dataframe['Date'],
        y=dataframe['MACD Hist'],
        name='Histogram',
        marker_color=c,
        opacity=0.5
    ))
    
    
    fig.update_xaxes(
        
    tickformat='%b %Y',      
    dtick="M1",              
    tickangle=45,            
    tickfont=dict(size=10, color='black')
    
    
    )

    fig.update_yaxes(
        
    dtick=10,                
    tickprefix='$',          
    tickfont=dict(size=10, color='black')
    
    
    )

    # Layout settings
    fig.update_layout(
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        margin=dict(l=0, r=20, t=20, b=0),
        legend=dict(
        orientation='h',
        yanchor="top",
        
        xanchor="right",
        x=1,
        y=1,
        font=dict(
                family='Arial',
                size=12,
                color='blue'
            )
)
    )

    return fig


def Moving_average(dataframe, num_period):
    # Calculate 50-period Simple Moving Average
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], length=50)
    
    # Filter the last N periods
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    # Open
    # fig.add_trace(go.Scatter(
    #     x=dataframe['Date'], y=dataframe['Open'],
    #     mode='lines', name='Open',
    #     line=dict(width=2, color='#5ab7ff')
    # ))

    # High
    # fig.add_trace(go.Scatter(
    #     x=dataframe['Date'], y=dataframe['High'],
    #     mode='lines', name='High',
    #     line=dict(width=2, color='#0078ff')
    # ))

    # Close
    # fig.add_trace(go.Scatter(
    #     x=dataframe['Date'], y=dataframe['Close'],
    #     mode='lines', name='Close',
    #     line=dict(width=2, color='black')
    # ))

    # Low
    # fig.add_trace(go.Scatter(
    #     x=dataframe['Date'], y=dataframe['Low'],
    #     mode='lines', name='Low',
    #     line=dict(width=2, color='red')
    # ))

    # SMA 50
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['SMA_50'],
        mode='lines', name='SMA 50',
        line=dict(width=2, color='purple')
    ))
    
    
    fig.update_xaxes(
    tickformat='%b %Y',      # X-axis format: Jan 2025
    dtick="M1",              # Tick every month (optional)
    tickangle=45,             # Rotate labels if needed
    tickfont=dict(size=12, color='black')
    )
    

    fig.update_yaxes(
    dtick=100,                # Tick every 10 units on Y-axis
    tickprefix='$',          # Add dollar sign before Y-axis values
    tickfont=dict(size=12, color='black')
    )

    # Axis and layout styling
    
    fig.update_layout(
        height=200,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(
            orientation='h',
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                family='Arial',
                size=12,
                color='blue'
            )
            
        )
    )

    return fig


def Moving_average_forecast(forecast):
    fig = go.Figure()

    
    fig.add_trace(go.Scatter(
        x=forecast.index[:-30],
        y=forecast['Close'].iloc[:-30],
        mode='lines',
        name='Close Price',
        line=dict(width=2, color='black')
    ))

    
    fig.add_trace(go.Scatter(
        x=forecast.index[-31:],
        y=forecast['Close'].iloc[-31:],
        mode='lines',
        name='Future Close Price',
        line=dict(width=2, color='red')
    ))

   
    fig.update_xaxes(
        rangeslider_visible=True,
        title='Date',
        tickformat='%b %Y',    
        tickangle=0,
        showline=True,
        linecolor='black',
        tickfont=dict(size=12, color='black')
    )

    
    fig.update_yaxes(
        title='Close Price (USD)',
        tickprefix='$',
        dtick=10,              
        showline=True,
        linecolor='black',
        tickfont=dict(size=12, color='black')
    )

    
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(
            yanchor='top',
            xanchor='right',
            font=dict(
                family='Arial',
                size=12,
                color='blue' 
            )
        )
    )

    return fig