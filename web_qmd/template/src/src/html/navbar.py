from fasthtml.common import *
from pilot.html.components.combined.combined_component import CombinedComponent

def navbar(paths):

    class Menus(CombinedComponent):

        children = [
            Div(topic.stem.lower())
            for topic in paths.content_groups
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

    return NavBar()
