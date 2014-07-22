'''
Created on Jul 29, 2011

@author: ACrosby
'''

class Aggregation(object):
    '''
    Aggregation class docs
    '''
    def __init__(self):
        '''
        Constructor
        TODO: no support for ncoords or coordValue args yet
        '''
        self.aggType = None #union or joinExisting or joinNew
        self.location = None #folder to scan
        self.files = None #list of inv files
        self.recurse = None #for dataset scans
        self.suffix = None #for dataset scans
        self.dimName = None #for joinExisting/joinNew
        self.dimType = None #joinNew
        self.dimShape = None #joinNew
        self.newDimAttributes = self.DimAttributes()
        self.timeUnitsChange = None #if the units of the joinExisting var change along datasets
        self.parameters = self.Parameter()
        
    def joinExistingAggType(self, dimension, scanlocation=None):
        '''
        joinExistingAggType(nameofdimvariable)
        '''
        self.aggType = "joinExisting"
        self.dimName = dimension
        if scanlocation is not None:
            self.setDatasetScan(scanlocation)
            
    def joinNewAggType(self, dimension, shape=None, type="float", scanlocation=None):
        '''
        '''
        if scanlocation is not None:
            self.setDatasetScan(scanlocation)
        if shape is None:  
            self.newDim(dimension, None, type)
        else: 
            self.newDim(dimension, shape, type)    
        
    
    def unionAggType(self, scanlocation=None):
        '''
        unionAggType()
        '''
        self.aggType = "union"
        if scanlocation is not None:
            self.setDatasetScan(scanlocation)
            
        
    def addDataset(self, file):
        '''
        '''
        self.files.append(file)
        
    def setDatasetScan(self, path, recurse=True, suffix=None):
        '''
        '''
        self.recurse = recurse #hopefully True or False
        self.location = path
        self.parameters.datasetScan = True
        self.suffix = suffix
        
    def newDim(self, dimName, shape, type="float"):
        '''
        '''
        self.dimName = dimName
        self.dimShape = shape
        self.dimType = type
        self.parameters.newDim = True
        
    class DimAttributes():
        '''
        DimAttributes class doc
        '''
        def __init__(self):
            self.valuesIncrementStart = None
            self.valuesIncrementStep = None
            self.values = None
            self.axisType = None
            self.units = None
            
    class Parameter():
        newDim = False
        datasetScan = False
        aggType = None
        pass
    
    def checkParameters(self):
        self.parameters.aggType = self.aggType
        return self.parameters
    