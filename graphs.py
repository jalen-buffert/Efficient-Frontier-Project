import plotly.express as px
import plotly.graph_objects as go
from portfolio import optimal_port



def efficient_frontier_visual(random_ports, returns, show = True):
    r_ports =  random_ports
    efficient_frontier = optimal_port(returns)


    frontier = px.scatter(r_ports, x='Volatility',y='Returns', width=800, height=600,
                          title='Efficient Frontier',opacity=0.35, template='plotly_dark',color='Sharpe',
                          hover_data=['Returns','Volatility','Sharpe'])

    frontier.add_trace(go.Scatter(x=efficient_frontier['Volatility'],
                                  y=efficient_frontier['Returns'],
                                  mode='lines',
                                  line=dict(color='red',width=3),
                                  name='Efficient Frontier'))

    frontier.update_layout(xaxis_title='Annual Volatility', yaxis_title='Annual Return', legend=dict(
        orientation='h',
        yanchor='top',
        y=1.1,
        xanchor='center',
        x=0.5))

    if show:
        frontier.show()
    return frontier


