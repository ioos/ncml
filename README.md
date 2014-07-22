ncml
====

Python tools for manipulating NCML (NetCDF Markup) files

These tools allow you to modify NcML by:
* adding or removing global attributes
* adding or removing variable attributes
* removing variables and dimensions

Example: 

```
      import ncml
      nc = ncml.Dataset.NcmlDataset('original.ncml')            # create an Ncmldataset object from a local NcML file
   
      nc.removeDimension('time2')                            # remove dimension
      nc.removeVariable('time2')                             # remove variable
      nc.addDatasetAttribute('Conventions','CF-1.6')         # add global attribute
      nc.addVariableAttribute('Temperature','units','degC')   # add variable attribute
      nc.removeVariableAttribute('Salinity','units')          # remove variable attribute
      
      nc.writeNcmlBack('modified.ncml')
```
