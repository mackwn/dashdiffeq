import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def render_slider(label,vmin,vmax,symbol,units): 

    output = dbc.Row([
            dbc.Col(
                dbc.Badge([
                    '{symbol}: '.format(symbol=symbol),
                    html.Span(id='{label}-slider-output-container'.format(label=label)),
                    ' {units}'.format(units=units)
                ],color='primary',className='slider-labels'),
                width = 3
            ),
            dbc.Col(
                dcc.Slider(
                    id='{label}-slider'.format(label=label),
                    min = vmin,
                    max = vmax,
                    value = (vmin+vmax)/2,
                    step = (vmax-vmin)/10,
                    className = 'input-slider'
                ),
                width = 9
            )
        ])
    return output