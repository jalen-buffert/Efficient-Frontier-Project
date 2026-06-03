import plotly.express as px
import plotly.graph_objects as go
from portfolio import optimal_port



def efficient_frontier_visual(random_ports, returns, show = True, sample_size = 2000):
    r_ports =  random_ports.copy()
    if len(r_ports) > sample_size:
        r_ports = r_ports.sample(sample_size, random_state=42)
        
    efficient_frontier = optimal_port(returns)
    
    frontier = px.scatter(r_ports,
                          x='Volatility',
                          y='Returns',
                          width=900,
                          height=650,
                          title='Efficient Frontier Portfolio Optimization',
                          opacity=0.65,
                          template='plotly_dark',
                          color='Sharpe',
                          hover_data=['Returns','Volatility','Sharpe'],
                          color_continuous_scale='Viridis'
                          )
    
    frontier.update_traces(marker=dict(size=4), selector=dict(mode='markers'))

    frontier.add_trace(go.Scatter(x=efficient_frontier['Volatility'],
                                  y=efficient_frontier['Returns'],
                                  mode='lines',
                                  line=dict(color='white',width=4),
                                  name='Efficient Frontier'))

    frontier.update_layout(xaxis_title='Annualized Volatility',
                           yaxis_title='Annualized Return',
                           font=dict(size=14),
                           title=dict(x=0.5,xanchor='center',font=dict(size=22)),
                           legend=dict(orientation='h', yanchor='bottom',y=1.02,
                                       xanchor='center',x=0.5),
                           margin=dict(l=70,r=70,t=90,b=70)
                           )
    frontier.write_image("efficient_frontier_example.png", scale = 3)

    if show:
        frontier.show()
    return frontier


