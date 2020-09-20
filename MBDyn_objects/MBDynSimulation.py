from MBDyn_objects.MBDynBaseContainer import BaseContainer
from ToBeOrganized.MBDyn_problems.initial_value import MBDynInitialValue
from ToBeOrganized.control_data_params import MBDynControlDataParams



class Simulation(BaseContainer):
    def __init__(self, obj, sim_parameter):
        """
        Default constructor
        """
        super(Simulation,self).__init__(obj, "MBDyn::Simulation")

        problem = MBDynInitialValue(**sim_parameter["problem_data"])
        control_data = MBDynControlDataParams(**sim_parameter["control_data"])

        obj.addProperty("App::PropertyPythonObject","Problem").Problem = problem
        obj.addProperty("App::PropertyPythonObject","ControlData").ControlData = control_data

        obj.Label = sim_parameter["general"]["name"]

        obj.addProperty("App::PropertyString", "WorkingDirectory", "Base","Working directory for the simulation run")
        obj.WorkingDirectory = sim_parameter["general"]["working_dir"]

    def write_problem(self):
        return self.Object.Problem.write()

    def write_control_data_param(self):
        return self.Object.ControlData.write(self.Object.Label)

    def set_parameters(self, sim_parameter):
        self.Object.Label = sim_parameter["general"]["name"]
        self.Object.WorkingDirectory = sim_parameter["general"]["working_dir"]
        self.Object.Problem.set_parameters(**sim_parameter["problem_data"])
        self.Object.ControlData.set_parameters(**sim_parameter["control_data"])
        self.Object.Document.recompute()

