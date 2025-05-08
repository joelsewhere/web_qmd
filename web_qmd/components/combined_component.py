from fasthtml.common import Div
from .component import Component

class CombinedComponent(Component):
    
    children = []
    outer_tag_args = {}
    outer_tag_type = Div

    def __call__(self):
       
       called_children = self.call_children()
       return self.outer_tag(called_children)
    
    def call_children(self):

        called = []
        for child in self.children:
            called_child = child()
            called.append(called_child)
        
        return called
    
    def outer_tag(self, children=[]):

        return self.outer_tag_type(
            *children,
            **self.outer_tag_args
        )
    