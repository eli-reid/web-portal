from ..adapters import SQLDBAdapter

class MeetingMixin(SQLDBAdapter):
    """description of class"""

    def __init__(self, *args, **kwargs):
        #populate table values
        for key, value in kwargs.items():
            self.__dict__[key] = value
        return super().__init__( *args, **kwargs)


    def exists(self):
        return self.get_first(date=self.date, title=self.title) is not None 
    
    
