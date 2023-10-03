import dash
from dash import html

dash.register_page(__name__, path="/about")

layout = html.Div(
    children=[
        html.Div(
            className="wrapper-vertical w10 center",
            children=[
                html.Div(
                    className="wrapper-horizontal w9 p3 center alt-left",
                    children=[
                        html.Div(
                            className="w5",
                            children=[
                                html.Div(
                                    className="foreground card",
                                    children=[
                                        html.Div(
                                            className="p3 margin-below",
                                            children=[
                                                html.H3(children="About"),
                                                html.P(
                                                    children=[
                                                        "This project was created in a group as a Senior Design Project at Embry-Riddle Aeronautical University. It was sponsored by Dr. Jianhua Liu.",
                                                        html.Br(),
                                                        html.Br(),
                                                        "Flight training can be difficult when it comes to flight planning, aeronautical sectional map reading, and understanding Air Traffic Control (ATC) communications.",
                                                        html.Br(),
                                                        html.Br(),
                                                        "The software is a web-based ASR map that displays an interactive map with the ability to toggle to an aeronautical sectional chart. The real-time flight tracker is displayed over both maps with icons representing the individual planes. Each plane can be clicked to display information about the flight. Using the LiveATC website, real-time ATC communications are run through a speech recognizer using Nvidia NeMo. The transcribed text from NeMo will then be displayed on the website alongside the plane information.",
                                                    ]
                                                ),
                                            ],
                                        )
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="w5",
                            children=[
                                html.Div(
                                    className="foreground card",
                                    children=[
                                        html.Div(
                                            className="p3 margin-below",
                                            children=[
                                                html.H3(children="Links"),
                                                html.Ul(
                                                    children=[
                                                        html.Li(
                                                            children=[
                                                                html.A(
                                                                    href="https://github.com/Burnetb8/Senior-Capstone",
                                                                    target="_blank",
                                                                    children="GitHub Repository",
                                                                ),
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children=[
                                                                html.A(
                                                                    href="https://trello.com/b/zKXAUiNI/scrum-board-spring",
                                                                    target="_blank",
                                                                    children="Trello Board",
                                                                )
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ],
                                        )
                                    ],
                                )
                            ],
                        ),
                    ],
                )
            ],
        )
    ]
)
