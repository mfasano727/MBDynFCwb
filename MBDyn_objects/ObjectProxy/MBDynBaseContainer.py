class BaseContainer:
    BaseType  = "MBDyn::BaseContainer"  # is actually lost on save

    def __init__(self, obj, Type=""):
        """
        Default constructor
        """
        obj.Proxy = self
        self.Object = obj
        self.Type = Type

    def onDocumentRestored(self, obj):
        obj.Proxy = self
        self.Object = obj

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state
        return None
