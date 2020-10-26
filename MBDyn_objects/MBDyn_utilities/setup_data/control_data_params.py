
class MBDynControlDataParams:

    def __init__(self, custom_parameters=None, *args, **kwargs):
        """
        :param custom_parameters: string
        """
        self.set_parameters(custom_parameters, * args, ** kwargs)

    def set_parameters(self, custom_parameters=None, *args, **kwargs):
        self.custom_parameters = custom_parameters

    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- problem parameter -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        state = {}
        state["custom_parameters"] = self.custom_parameters
        return state

    def __setstate__(self, state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        self.custom_parameters = state["custom_parameters"]
        return None

    def write(self, name=None):
        """write control data parameters"""
        line_iv = ""

        if None != name:
            line_iv += '    title: "{}";\n'.format(name)

        if None != self.custom_parameters:
            line = self.custom_parameters
            line += "\n"
            line_iv += line

        return line_iv
