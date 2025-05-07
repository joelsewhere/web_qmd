from . import paths
from fasthtml.common import Body, Img, Div, Nav
from config import paths
from pilot.html.components.combined import CombinedComponent


class Menus(CombinedComponent):

    children = [
        Div(topic.stem.lower())
        for topic in paths.creation_groups
    ]

    outer_tag_args = {"cls": "menus"}


class NavBar(CombinedComponent):

    children = [
        Img(src='/' + paths.logo.as_posix(), cls="logo"),
        Menus(),
        Div("X", cls="toggler"),
    ]
    outer_tag_args = {
        'cls': 'navbar'
    }

    outer_tag_type = Nav


headers = [
    NavBar(),

    ]

footers = [
    
]



        