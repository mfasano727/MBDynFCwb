
class MBDynInitialValue:

    def __init__(self, initial_time=None, final_time=None, time_step=None, max_iterations=None, tolerance=None,
                 derivatives_tolerance=None, method=None, output=None, custom_parameters=None, *args, **kwargs):
        """
        :param initial_time: float
        :param final_time: flaot
        :param time_step: flaot
        :param max_iterations:  int
        :param tolerance: float
        :param derivatives_tolerance: float
        :param method: dict: {"Name":"","Params":[]}
        :param output: list of string.
        :param custom_parameters: string
        """
        print("here", args)
        print("here", kwargs)
        self.type = "initial value"
        self.set_parameters(initial_time, final_time, time_step, max_iterations, tolerance,
                               derivatives_tolerance, method, output, custom_parameters, *args, **kwargs)

    def set_parameters(self, initial_time=None, final_time=None, time_step=None, max_iterations=None, tolerance=None,
                          derivatives_tolerance=None, method=None, output=None, custom_parameters=None, *args, **kwargs):
        self.initial_time = initial_time
        self.final_time = final_time
        self.time_step = time_step
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.derivatives_tolerance = derivatives_tolerance
        self.method = method
        self.output = output
        self.custom_parameters = custom_parameters

    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- problem parameter -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        state = {}
        state["type"] = self.type
        state["initial_time"] = self.initial_time
        state["final_time"] = self.final_time
        state["time_step"] = self.time_step
        state["max_iterations"] = self.max_iterations
        state["tolerance"] = self.tolerance
        state["derivatives_tolerance"] = self.derivatives_tolerance
        state["method"] = self.method
        state["output"] = self.output
        state["custom_parameters"] = self.custom_parameters
        return state

    def __setstate__(self, state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        self.type = state["type"]
        self.initial_time = state["initial_time"]
        self.final_time = state["final_time"]
        self.time_step = state["time_step"]
        self.max_iterations = state["max_iterations"]
        self.tolerance = state["tolerance"]
        self.derivatives_tolerance = state["derivatives_tolerance"]
        self.method = state["method"]
        self.output = state["output"]
        self.custom_parameters = state["custom_parameters"]
        return None

    def write(self):
        """write problem data"""

        line_iv = "begin: {};\n".format(self.type)

        if None != self.initial_time:
            line = "    initial time: {};\n".format(self.initial_time)
            line_iv += line
        if None != self.final_time:
            line = "    final time: {};\n".format(self.final_time)
            line_iv += line
        if None != self.time_step:
            line = "    time step: {};\n".format(self.time_step)
            line_iv += line
        if None != self.tolerance:
            line = "    tolerance: {};\n".format(self.tolerance)
            line_iv += line
        if None != self.max_iterations:
            line = "    max iterations: {};\n".format(self.max_iterations)
            line_iv += line
        if None != self.derivatives_tolerance:
            line = "    derivatives tolerance: {};\n".format(self.derivatives_tolerance)
            line_iv += line
        if None != self.method:
            line = "    method: {}".format(self.method["name"])
            for param in self.method["params"]:
                line += ", {}".format(param)
            line += ";\n"
            line_iv += line
        if None != self.output:
            line = "    output: {}".format(self.output[0])
            for output in self.output[1::]:
                line += ", {}".format(output)
            line += ";\n"
            line_iv += line
        if None != self.custom_parameters:
            line = self.custom_parameters
            line += "\n"
            line_iv += line

        line_iv += "end: {};\n\n".format(self.type)
        return line_iv
