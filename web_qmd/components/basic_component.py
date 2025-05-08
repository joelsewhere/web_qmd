from .component import Component


class BasicComponent(Component):

    def build_component(self):
        raise NotImplementedError
     
    def outer_div(self, component):
        return component
    
    def component_data(self):
        raise NotImplemented

    def __call__(self, *args):

        component = self.build_component()(*args)

        return self.outer_div(component)