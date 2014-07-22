'''
Created on Jul 28, 2011

@author: ACrosby
'''
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element 

class NcmlCatalog(object):
    '''
    classdocs
    '''


    def __init__(self, file):
        '''
        Constructor
        '''
        self.dataset = file
        self.doctree = parse(self.dataset)
        self.services = self.doctree.getroot.findall(("{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}service"))
        # Within these datasets are other datasets than can be used with ncml.Dataset
        self.datasets = self.doctree.getroot.findall(("{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset"))
        
    def listDatasets(self):
        '''
        listDatasets
        '''  
        for i in self.datasets:
            catalog_cats = i.attrib["name"]   
        return catalog_cats
    
    def swapNcmlNetcdfDoctree(self, doctree, name):
        '''
        swapNcmlNetcdfDoctree
        '''
        pass
    
    def pullDatasets(self, doctree):
        '''
        pullDatasets
        '''
        pass
    
    def pullNetcdfs(self, doctree):
        '''
        pullNetcdfs
        '''
        pass
        
        