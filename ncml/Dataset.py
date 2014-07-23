'''
Created on Jul 28, 2011

@author: ACrosby
'''
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element  
from xml.etree.ElementTree import ElementTree
import ncml


class NcmlDataset(object):
    '''
    classdocs
    '''
    def __init__(self, file):
        '''
        NcmlDataset Constructor
        NcmlDataset('path')
        or 
        NcmlDataset(xml.etree.ElementTree)
        '''
        
        self.dataset = file
        if type(file) == ElementTree:
            self.doctree = self.dataset
        else:
            self.doctree = parse(self.dataset)
        
    def addVariableAttribute(self, variable, key, value):
        '''
        addVariableAttribute('varName', 'attributeName', 'attributeValue')
        '''
        netcdfroot = self.doctree.getroot()
        Var = netcdfroot.find(("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}variable[@name='" + variable + "']"))
        NewElement = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}attribute", name=key, value=value)
        if Var is not None:
            exists = Var.find(("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}attribute[@name='" + key + "']"))
            if exists is not None:
                exists.attrib["name"] = key
                exists.attrib["value"] = value
            else:
                Var.append(NewElement)
        else:
            NewVarElement = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}variable", name=variable)
            NewVarElement.append(NewElement)
            netcdfroot.append(NewVarElement)
        

    def addDatasetAttribute(self, key, value):
        '''
        addDatasetAttribute('varName', 'attrName', 'attrValue')
        '''
        
        netcdfroot = self.doctree.getroot()
        exists = netcdfroot.find(("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}attribute[@name='" + key + "']"))
        if exists is not None:
            exists.attrib["name"] = key
            exists.attrib["value"] = value
        else:
            NewElement = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}attribute", 
            name=key, value=value)
            netcdfroot.append(NewElement)
        
        
        
    def writeNcmlBack(self, path=None):
        '''
        Write changes in doctree back to xml file
        writeNcmlBack()
        '''
        if path is not None:
            self.doctree.write(path)
        else:
            self.doctree.write(self.dataset)
        
    def removeDatasetAttribute(self, key):
        '''
        removeDatasetAttribute('Global_attrName')
        '''
        netcdfroot = self.doctree.getroot()
        NewElement = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}remove", 
        type='attribute',name=key)
        netcdfroot.append(NewElement)
        
    def removeDatasetVariable(self, key):
        '''
        removeDatasetVariable('VarName')
        '''
        netcdfroot = self.doctree.getroot()
        NewElement = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}remove", 
        type='variable',name=key)
        netcdfroot.append(NewElement)    
        
    def removeDatasetDimension(self, key):
        '''
        removeDatasetVariable('DimName')
        '''
        netcdfroot = self.doctree.getroot()
        NewElement = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}remove", 
        type='dimension',name=key)
        netcdfroot.append(NewElement) 
            
    def removeVariableAttribute(self, variable, key):
        '''
        removeVariableAttribute('varName', 'attrName')
        '''
        netcdfroot = self.doctree.getroot()
        Var = netcdfroot.find(("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}variable[@name='" + variable + "']"))
        NewElement = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}remove", 
        type='attribute',name=key)
        if Var is not None:
            Var.append(NewElement)
        else:
            NewVarElement = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}variable", name=variable)
            NewVarElement.append(NewElement)
            netcdfroot.append(NewVarElement)
    
    def addAggregation(self, agg):
        def createAggTags(type, dimName=None, ):
            NewAggregation = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}aggregation")
            NewAggregation.attrib["dimName"] = dimName
            NewAggregation.attrib["type"] = type
            return NewAggregation
        
        if type(agg) == ncml.Aggregation.Aggregation:
            netcdfroot = self.doctree.getroot()
            params = agg.checkParameters() 
            # Create the agg tags themselves here
            if agg.aggType == "joinNew":
                NewAggregation = createAggTags(agg.aggType, agg.dimName)
            elif agg.aggType == "joinExisting":
                NewAggregation = createAggTags(agg.aggType, agg.dimName)
            elif agg.aggType == "union":
                NewAggregation = createAggTags(agg.aggType)
            else: pass
            
            if params.datasetScan:
                NewElement = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}scan")
                NewElement.attrib["location"] = agg.location
                NewElement.attrib["subdirs"] = str(agg.recurse).lower()
                if agg.suffix is not None:
                    NewElement.attrib["suffix"] = agg.suffix
                NewAggregation.append(NewElement)
            else:
                for i in agg.files:
                    NewElement = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}netcdf")
                    NewElement.attrib["location"] = i
                    NewAggregation.append(NewElement)
                    
            # If new dim, create new variable here
            if params.newDim:
                NewVariable = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}variable")
                NewVariable.attrib["name"] = agg.dimName
                NewVariable.attrib["type"] = agg.dimType
                if agg.dimShape is not None:
                    NewVariable.attrib["shape"] = agg.dimShape
                if agg.newDimAttributes.values is not None:
                    NewValues = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}values")
                    NewVariable.append(NewValues)
                else:
                    pass
                if agg.newDimAttributes.axisType is not None:
                    NewType = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}attribute")
                    NewType.attrib["_CoordinateAxisType"] = agg.newDimAttributes.axisType
                    NewVariable.append(NewType)
                if agg.newDimAttributes.units is not None:
                    NewUnits = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}attribute")
                    NewUnits.attrib["units"] = agg.newDimAttributes.units
                    NewVariable.append(NewUnits)
                netcdfroot.append(NewVariable)
            netcdfroot.append(NewAggregation)
        else: pass # should add error
        
        
        
def createNcmlFrame(location=None):
    '''
    Returns an ncml.Dataset.NcmlDataset
    ElementTree = createNcmlFrame('path')
    '''
    netcdfroot = Element("{http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2}netcdf")
    if location is not None:    
        netcdfroot.attrib["location"] = location     
    else: pass
    Ncmldataset = NcmlDataset(ElementTree(netcdfroot))
        
    return Ncmldataset

        
