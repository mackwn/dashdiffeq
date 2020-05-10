import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/about")),
        dbc.DropdownMenu(
            children=[
                #dbc.DropdownMenuItem("Apps", header=True),
                dbc.DropdownMenuItem("2D Elliptical", href="/apps/app2del"),
                dbc.DropdownMenuItem("1D Parabolic", href="/apps/app1dpar"),
            ],
            nav=True,
            in_navbar=True,
            label="Apps",
        ),
    ],
    brand="SM Github",
    brand_href="https://github.com/mackwn/dashdiffeq",
    color="primary",
    dark=True,
)
