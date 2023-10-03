from dash import html, dcc
import dash


dash.register_page(__name__, path="/")
app = dash.get_app()

layout = html.Div(
    className="foreground w10 wrapper-horizontal",
    children=[
        html.Div(
            className="w5 center wrapper-horizontal",
            children=[
                html.A(
                    className="button",
                    href="/about",
                    children=[html.H3(children="About", className="link")],
                ),
                html.A(
                    href="/map",
                    children=[html.H3(children="Map", className="link")],
                ),
            ],
        )
    ],
)
