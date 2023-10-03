from dash import Dash, html, Input, Output
import dash

# import dash_daq as daq
# import asyncio
# from threading import Thread
# from transcribing import audio_fetch_and_transcribe

external_stylesheets = [
    # Plane icons, etc.
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/font-awesome.min.css",
]

# Website settings
app = Dash(
    __name__, title="ATC Map", external_stylesheets=external_stylesheets, use_pages=True
)

# map_types = ["Interactive Map", "Aeronautical Chart Map"]


# def create_toggle_label(map):
#     return f"Click to view {map_types[map]}"


# header = html.Header(
#     className="foreground w10 wrapper-horizontal",
#     children=[
#         html.Div(
#             className="w5 center left wrapper-horizontal",
#             children=[
#                 html.A(
#                     href="/", children=[html.H2(children="ATC Map", className="link")]
#                 ),
#                 html.A(href="/about", children="About", className="link"),
#             ],
#         ),
#         html.Div(
#             className="w5 center right",
#             children=[
#                 # Toggle map button
#                 daq.ToggleSwitch(
#                     id="map-switch",
#                     label=create_toggle_label(0),
#                     value=False,
#                     size=45,
#                     color="#2c62c6",
#                     labelPosition="bottom",
#                     className="link",
#                 )
#             ],
#         ),
#     ],
# )

# Render the layout of the website
app.layout = html.Div(children=[dash.page_container])


# Change the toggle text label on click
# @app.callback([Output("map-switch", "label")], [Input("map-switch", "value")])
# def toggle_switch(value):
#     other_map = 0 if value else 1
#     return (create_toggle_label(other_map),)


# def audio_fetching_thread():
#     asyncio.run(audio_fetch_and_transcribe())


if __name__ == "__main__":
    # Start audio fetching
    # audio_fetching = Thread(target=audio_fetching_thread)
    # audio_fetching.start()

    app.run_server(
        debug=True  # Must run debug False to prevent extra audio fetching thread from being created
    )
    # audio_fetching.join()
