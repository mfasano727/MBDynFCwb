from MBDyn_objects.MBDynBaseContainer import BaseContainer

class WorkbenchContainer(BaseContainer):

    def __init__(self, obj):
        """
        Default constructor
        """
        super(WorkbenchContainer,self).__init__(obj, "MBDyn::WorkbenchContainer")
        self.activeSimulation = None
        self.activeResult = None

    #def onDocumentRestored(self, obj):
    #    super(WorkbenchContainer,self).onDocumentRestored(obj)
    #    self.activeSimulation = None
    #    self.activeResult = None

    def setActiveSimulation(self, simObj):
        """ simObj is the simulation object not the proxy"""
        #previousActive = self.activeSimulation 
        #self.activeSimulation = simObj
        previousActive = self.activeSimulation
        self.activeSimulation = simObj
        if previousActive:
            previousActive.ViewObject.signalChangeIcon()

    def setActiveResult(self, resObj):
        """ resObj is the simulation object not the proxy"""
        previousActive = self.activeResult
        self.activeSimulation = resObj
        if previousActive:
            previousActive.ViewObject.signalChangeIcon()

    def getActiveSimulation(self):
        return self.activeSimulation

    def getActiveResult(self):
        return self.activeResult

    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.
                active simulation and result are lost on save/restore'''
        super(WorkbenchContainer,self).__setstate__(state)
        self.activeSimulation = None
        self.activeResult = None
        return None
