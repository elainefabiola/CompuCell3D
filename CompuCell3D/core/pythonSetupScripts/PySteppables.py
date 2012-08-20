"This module contains definitions of basic classes that are used to construct Python based Steppables"


#steppables

class SimObjectPy:
    def __init__(self):pass
    def init(self,_simulator):
        self.simulator=_simulator
    def extraInit(self,_simulator):
        self.simulator=_simulator

class SteppablePy(SimObjectPy):
    def __init__(self,_frequency=1):
        self.frequency=_frequency
        self.runBeforeMCS=0
    #def __name__(self):
        #self.name="Steppable"
    def setFrequency(self,_freq):
        self.frequency=_freq
    def start(self):pass
    def step(self,_mcs):pass
    def finish(self):pass


class SteppableBasePy(SteppablePy):    
    def __init__(self,_simulator,_frequency=1):
        SteppablePy.__init__(self,_frequency)
        self.simulator=_simulator
        self.potts=_simulator.getPotts()
        self.cellField=self.potts.getCellFieldG()
        self.dim=self.cellField.getDim()
        self.inventory=self.simulator.getPotts().getCellInventory()
        self.clusterInventory=self.inventory.getClusterInventory()
        self.cellList=CellList(self.inventory)
        self.cellListByType=CellListByType(self.inventory)
        self.clusterList=ClusterList(self.inventory)        
        import CompuCellSetup
        self.typeIdTypeNameDict = CompuCellSetup.ExtractTypeNamesAndIds()    
        for typeId in self.typeIdTypeNameDict:
            setattr(self,self.typeIdTypeNameDict[typeId].upper(),typeId)
        
        
        #VolumeTrackerPlugin
        self.volumeTrackerPlugin=None
        if self.simulator.pluginManager.isLoaded("VolumeTracker"):
            import CompuCell
            self.volumeTrackerPlugin=CompuCell.getVolumeTrackerPlugin()
        
        #NeighborTrackerPlugin
        self.neighborTrackerPlugin=None
        if self.simulator.pluginManager.isLoaded("NeighborTracker"):
            import CompuCell
            self.neighborTrackerPlugin=CompuCell.getNeighborTrackerPlugin()

        #FocalPointPlasticity
        self.focalPointPlasticityPlugin=None
        if self.simulator.pluginManager.isLoaded("FocalPointPlasticity"):
            import CompuCell
            self.focalPointPlasticityPlugin=CompuCell.getFocalPointPlasticityPlugin()
            
        #Chemotaxis    
        self.chemotaxisPlugin=None        
        if self.simulator.pluginManager.isLoaded("Chemotaxis"):
            import CompuCell            
            self.chemotaxisPlugin=CompuCell.getChemotaxisPlugin()

        #BoundaryPixelTrackerPlugin
        self.boundaryPixelTrackerPlugin=None        
        if self.simulator.pluginManager.isLoaded("BoundaryPixelTracker"):
            import CompuCell            
            self.boundaryPixelTrackerPlugin=CompuCell.getBoundaryPixelTrackerPlugin()

        #PixelTrackerPlugin
        self.pixelTrackerPlugin=None        
        if self.simulator.pluginManager.isLoaded("PixelTracker"):
            import CompuCell            
            self.pixelTrackerPlugin=CompuCell.getPixelTrackerPlugin()
            
        #ElasticityTrackerPlugin    
        self.elasticityTrackerPlugin=None        
        if self.simulator.pluginManager.isLoaded("ElasticityTracker"):
            import CompuCell            
            self.elasticityTrackerPlugin=CompuCell.getElasticityTrackerPlugin()

        #PlasticityTrackerPlugin    
        self.plasticityTrackerPlugin=None        
        if self.simulator.pluginManager.isLoaded("PlasticityTracker"):
            import CompuCell            
            self.plasticityTrackerPlugin=CompuCell.getPlasticityTrackerPlugin()
            
        #ConnectivityLocalFlexPlugin    
        self.connectivityLocalFlexPlugin=None        
        if self.simulator.pluginManager.isLoaded("ConnectivityLocalFlex"):
            import CompuCell            
            self.connectivityLocalFlexPlugin=CompuCell.getConnectivityLocalFlexPlugin()

        #ConnectivityLocalFlexPlugin    
        self.connectivityGlobalPlugin=None        
        if self.simulator.pluginManager.isLoaded("ConnectivityGlobal"):
            import CompuCell            
            self.connectivityGlobalPlugin=CompuCell.getConnectivityGlobalPlugin()            
            
        # #LengthConstraintLocalFlexPlugin    
        # self.lengthConstraintLocalFlexPlugin=None        
        # if self.simulator.pluginManager.isLoaded("LengthConstraintLocalFlex"):
            # import CompuCell            
            # self.lengthConstraintLocalFlexPlugin=CompuCell.getLengthConstraintLocalFlexPlugin()

        #LengthConstraintPlugin    
        self.lengthConstraintPlugin=None        
        if self.simulator.pluginManager.isLoaded("LengthConstraint"):
            import CompuCell            
            self.lengthConstraintPlugin=CompuCell.getLengthConstraintPlugin()
            self.lengthConstraintLocalFlexPlugin=self.lengthConstraintPlugin # kept for compatibility reasons

            
        #ContactLocalFlexPlugin 
        self.contactLocalFlexPlugin=None
        if self.simulator.pluginManager.isLoaded("ContactLocalFlex"):
            import CompuCell            
            self.contactLocalFlexPlugin=CompuCell.getContactLocalFlexPlugin()
            
        #ContactLocalProductPlugin 
        self.contactLocalProductPlugin=None
        if self.simulator.pluginManager.isLoaded("ContactLocalProduct"):
            import CompuCell            
            self.contactLocalProductPlugin=CompuCell.getContactLocalProductPlugin()
            
        #ContactMultiCadPlugin 
        self.contactMultiCadPlugin=None
        if self.simulator.pluginManager.isLoaded("ContactMultiCad"):
            import CompuCell            
            self.contactMultiCadPlugin=CompuCell.getContactMultiCadPlugin()

        #ContactOrientationPlugin 
        self.contactOrientationPlugin=None
        if self.simulator.pluginManager.isLoaded("ContactOrientation"):
            import CompuCell            
            self.contactOrientationPlugin=CompuCell.getContactOrientationPlugin()
            
        #AdhesionFlexPlugin 
        self.adhesionFlexPlugin=None
        if self.simulator.pluginManager.isLoaded("AdhesionFlex"):
            import CompuCell            
            self.adhesionFlexPlugin=CompuCell.getAdhesionFlexPlugin()

        #CellOrientationPlugin 
        self.cellOrientationPlugin=None
        if self.simulator.pluginManager.isLoaded("CellOrientation"):
            import CompuCell            
            self.cellOrientationPlugin=CompuCell.getCellOrientationPlugin()

        #PolarizationVectorPlugin 
        self.polarizationVectorPlugin=None
        if self.simulator.pluginManager.isLoaded("PolarizationVector"):
            import CompuCell            
            self.polarizationVectorPlugin=CompuCell.getPolarizationVectorPlugin()
            
        #MomentOfInertiaPlugin 
        self.momentOfInertiaPlugin=None
        if self.simulator.pluginManager.isLoaded("MomentOfInertia"):
            import CompuCell            
            self.momentOfInertiaPlugin=CompuCell.getMomentOfInertiaPlugin()

        #SecretionPlugin 
        self.secretionPlugin=None
        if self.simulator.pluginManager.isLoaded("Secretion"):
            import CompuCell            
            self.secretionPlugin=CompuCell.getSecretionPlugin()

        #ClusterSurfacePlugin 
        self.clusterSurfacePlugin=None
        if self.simulator.pluginManager.isLoaded("ClusterSurface"):
            import CompuCell            
            self.clusterSurfacePlugin=CompuCell.getClusterSurfacePlugin()

        #ClusterSurfaceTrackerPlugin 
        self.clusterSurfaceTrackerPlugin=None
        if self.simulator.pluginManager.isLoaded("ClusterSurfaceTracker"):
            import CompuCell            
            self.clusterSurfaceTrackerPlugin=CompuCell.getClusterSurfaceTrackerPlugin()

        #polarization23Plugin 
        self.polarization23Plugin=None
        if self.simulator.pluginManager.isLoaded("Polarization23"):
            import CompuCell            
            self.polarization23Plugin=CompuCell.getPolarization23Plugin()

        #cellTypeMonitorPlugin 
        self.cellTypeMonitorPlugin=None
        if self.simulator.pluginManager.isLoaded("CellTypeMonitor"):
            import CompuCell            
            self.cellTypeMonitorPlugin=CompuCell.getCellTypeMonitorPlugin()
            
        #boundaryMonitorPlugin 
        self.boundaryMonitorPlugin=None
        if self.simulator.pluginManager.isLoaded("BoundaryMonitor"):
            import CompuCell            
            self.boundaryMonitorPlugin=CompuCell.getBoundaryMonitorPlugin()

            
            
            
    def getClusterCells(self,_clusterId):
        return ClusterCellList(self.inventory.getClusterInventory().getClusterCells(_clusterId))   
        #may work on some systems
        # return self.inventory.getClusterInventory().getClusterCells(_clusterId)       
        
    def reassignClusterId(self,_cell,_clusterId):
        oldClusterId=_cell.clusterId
        newClusterId=_clusterId            
        self.inventory.reassignClusterId(_cell,newClusterId)
        if self.clusterSurfaceTrackerPlugin:
            self.clusterSurfaceTrackerPlugin.updateClusterSurface(oldClusterId)
            self.clusterSurfaceTrackerPlugin.updateClusterSurface(newClusterId)        
    
    
        
        
        
    def getCellNeighbors(self,_cell):
        if self.neighborTrackerPlugin:
            return CellNeighborListAuto(self.neighborTrackerPlugin,_cell)
        
        return None
            
    def getFocalPointPlasticityDataList(self,_cell):
        if self.focalPointPlasticityPlugin:
            return FocalPointPlasticityDataList(self.focalPointPlasticityPlugin,_cell)
            
        return None    

    def getInternalFocalPointPlasticityDataList(self,_cell):
        if self.focalPointPlasticityPlugin:
            return InternalFocalPointPlasticityDataList(self.focalPointPlasticityPlugin,_cell)            
            
        return None    
        
    def getCellBoundaryPixelList(self,_cell):
        if self.boundaryPixelTrackerPlugin:
            return CellBoundaryPixelList(self.boundaryPixelTrackerPlugin,_cell)
            
        return None    
        
    def getCellPixelList(self,_cell):
        if self.pixelTrackerPlugin:
            return CellPixelList(self.pixelTrackerPlugin,_cell)

        return None    
        
    def getElasticityDataList(self,_cell):
        if self.elasticityTrackerPlugin:
            return ElasticityDataList(self.elasticityTrackerPlugin,_cell)

    def getPlasticityDataList(self,_cell):
        if self.plasticityTrackerPlugin:
            return PlasticityDataList(self.plasticityTrackerPlugin,_cell)
            
        return None    
        
    def getFieldSecretor(self,_fieldName):
    
        if self.secretionPlugin:
            return self.secretionPlugin.getFieldSecretor(_fieldName)
            
        return None    
    '''    
        We have to call volumeTracker. setp function manually when tryuign to delete cell. This function is called only from potts loop whil Python steppables are run outside this loop.
    '''     
    def cleanDeadCells(self):
        if self.volumeTrackerPlugin:
            self.volumeTrackerPlugin.step()        
            
    def  deleteCell(self,cell):
        import CompuCell
        pixelsToDelete=[] #used to hold pixels to delete        
        pixelList=self.getCellPixelList(cell)
        pt=CompuCell.Point3D()
        
        for pixelTrackerData in pixelList:
            pixelsToDelete.append(CompuCell.Point3D(pixelTrackerData.pixel))            
            self.mediumCell=CompuCell.getMediumCell()                                    
        for pixel in pixelsToDelete:            
            self.cellField.set(pixel,self.mediumCell)   
        # We have to call volumeTracker. setp function manually when tryuign to delete cell. This function is called only from potts loop whil Python steppables are run outside this loop.    
        self.cleanDeadCells()   
    
    def createNewCell (self,type,pt,xSize,ySize,zSize=1):
        import CompuCell
        if not self.checkIfInTheLattice(pt):
            return
        cell=self.potts.createCellG(pt)    
        cell.type=type
        
        ptCell=CompuCell.Point3D()
        
        for x in range(pt.x,pt.x+xSize,1):
            for y in range(pt.y,pt.y+ySize,1):        
                for z in range(pt.z,pt.z+zSize,1):
                    ptCell.x=x
                    ptCell.y=y
                    ptCell.z=z                    
                    if self.checkIfInTheLattice(ptCell):
                        self.cellField.set(ptCell,cell)        
                        
    def moveCell(self, cell, shiftVector):
        import  CompuCell  
        #we have to make two list of pixels :
        pixelsToDelete=[] #used to hold pixels to delete
        pixelsToMove=[] #used to hold pixels to move
        
        # If we try to reassign pixels in the loop where we iterate over pixel data we will corrupt the container so in the loop below all we will do is to populate the two list mentioned above
        pixelList=self.getCellPixelList(cell)
        pt=CompuCell.Point3D()
        
        for pixelTrackerData in pixelList:
            pt.x = pixelTrackerData.pixel.x + shiftVector.x
            pt.y = pixelTrackerData.pixel.y + shiftVector.y
            pt.z = pixelTrackerData.pixel.z + shiftVector.z
            # here we are making a copy of the cell                 
            pixelsToDelete.append(CompuCell.Point3D(pixelTrackerData.pixel))
            
            if self.checkIfInTheLattice(pt):
                pixelsToMove.append(CompuCell.Point3D(pt))
                # self.cellField.set(pt,cell)
         
        # Now we will move cell
        for pixel in pixelsToMove:
            self.cellField.set(pixel,cell)
         
        # Now we will delete old pixels    
        pixelList=self.getCellPixelList(cell)
        pt=CompuCell.Point3D()
        
        self.mediumCell=CompuCell.getMediumCell()                
        for pixel in pixelsToDelete:
            self.cellField.set(pixel,self.mediumCell)   
                    
    def checkIfInTheLattice(self,_pt):
        if _pt.x>=0 and _pt.x<self.dim.x and  _pt.y>=0 and _pt.y<self.dim.y and _pt.z>=0 and _pt.z<self.dim.z:            
            return True
        return False
        
        
class RunBeforeMCSSteppableBasePy(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)   
        self.runBeforeMCS=1    
        
class SecretionBasePy(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)   
        self.runBeforeMCS=1    

        
class SteppableRegistry(SteppablePy):
    def __init__(self):
        self.steppableList=[]
        self.runBeforeMCSSteppableList=[]

    def registerSteppable(self,_steppable):
        try:
            if _steppable.runBeforeMCS:
                self.runBeforeMCSSteppableList.append(_steppable)
            else:
                self.steppableList.append(_steppable)
            return    
        except AttributeError:
            self.steppableList.append(_steppable)

    def init(self,_simulator):
        for steppable in self.runBeforeMCSSteppableList:
            steppable.init(_simulator)            


        for steppable in self.steppableList:
            steppable.init(_simulator)
            

    def extraInit(self,_simulator):
        for steppable in self.runBeforeMCSSteppableList:
            steppable.extraInit(_simulator)

        for steppable in self.steppableList:
            steppable.extraInit(_simulator)
            
            
    def start(self):
        for steppable in self.runBeforeMCSSteppableList:
            steppable.start()

        for steppable in self.steppableList:
            steppable.start()

    def step(self,_mcs):
        for steppable in self.steppableList:
            if not _mcs % steppable.frequency: #this executes given steppable every "frequency" Monte Carlo Steps                
                steppable.step(_mcs)

    def stepRunBeforeMCSSteppables(self,_mcs):
        for steppable in self.runBeforeMCSSteppableList:
            if not _mcs % steppable.frequency: #this executes given steppable every "frequency" Monte Carlo Steps
                steppable.step(_mcs)
        
    def finish(self):
        for steppable in self.runBeforeMCSSteppableList:
            steppable.finish()
    
        for steppable in self.steppableList:
            steppable.finish()

#IMPORTANT: It is best to always provide hand-written iterators for STL containers even though swig generates them for you. 
# with multiple swig modules  those autogenerated iterators will work on one platform and crash on another ones so best solution is to write iterators yourself
            
#this is used to iterate more easily over cells

class CellList:
    def __init__(self,_inventory):
        self.inventory = _inventory
    def __iter__(self):
        return CellListIterator(self)
    def __len__(self):
        return self.inventory.getSize()

class CellListIterator:
    def __init__(self, _cellList):
        import CompuCell
        self.inventory = _cellList.inventory
        self.invItr=CompuCell.STLPyIteratorCINV()
        self.invItr.initialize(self.inventory.getContainer())
        self.invItr.setToBegin()
    def next(self):
        if not self.invItr.isEnd():
            self.cell = self.invItr.getCurrentRef()
            self.invItr.next()
            return self.cell
        else:
            raise StopIteration
    def __iter__(self):
            return self

            
# iterating ofver inventory of cells of a given type
class CellListByType:
    def __init__(self,_inventory,*args):            
        import CompuCell
        self.inventory = _inventory
        
        self.types=CompuCell.vectorint()
        
        self.inventoryByType=CompuCell.mapLongCellGPtr()
        
        self.initTypeVec(args)
        self.inventory.initCellInventoryByMultiType(self.inventoryByType , self.types)  
        
        
        
    def __iter__(self):
        return CellListByTypeIterator(self)

    def __call__(self,*args):
        self.initTypeVec(args)
        self.inventory.initCellInventoryByMultiType(self.inventoryByType , self.types)

        return self       

        
        
    def __len__(self):
        return self.inventoryByType.size()
        
    def initTypeVec(self,_typeList):
        
        self.types.clear()        
        if len(_typeList)<=0:
            self.types.push_back(1) # type 1 
        else:    
            for type in _typeList:
                self.types.push_back(type)
    
    def initializeWithType(self,_type):
        self.types.clear()
        self.types.push_back(_type)
        self.inventory.initCellInventoryByMultiType(self.inventoryByType , self.types)
        
    def refresh(self):
        self.inventory.initCellInventoryByMultiType(self.inventoryByType , self.types)        
        


        
        
class CellListByTypeIterator:
    def __init__(self,  _cellListByType):
        import CompuCell
        self.inventoryByType = _cellListByType.inventoryByType        
        
        self.invItr=CompuCell.mapLongCellGPtrPyItr()
        self.invItr.initialize(self.inventoryByType)        
        self.invItr.setToBegin()
        
    def next(self):
        if not self.invItr.isEnd():
            self.cell=self.invItr.getCurrentRef()
            # print 'self.idCellPair=',self.idCellPair
            # print 'dir(self.idCellPair)=',dir(self.idCellPair)
            self.invItr.next()
            return self.cell
#       
        else:
            raise StopIteration
    
    def __iter__(self):
            return self 
            
            
#this is used to iterate more easily over clusters 

class ClusterList:
    def __init__(self,_inventory):
        self.inventory = _inventory.getClusterInventory().getContainer()
    def __iter__(self):
        return ClusterListIterator(self)
    def __len__(self):
        return self.inventory.size()        

class ClusterListIterator:
    def __init__(self, _cellList):
        import CompuCell
        self.inventory = _cellList.inventory
        
        self.invItr=CompuCell.compartmentinventoryPtrPyItr()
        self.invItr.initialize(self.inventory)        
        self.invItr.setToBegin()
        
        
    def next(self):
    
        if not self.invItr.isEnd():
            self.compartmentList=self.invItr.getCurrentRef()
            # print 'self.idCellPair=',self.idCellPair
            # print 'dir(self.idCellPair)=',dir(self.idCellPair)
            self.invItr.next()
            return self.compartmentList
#       
        else:
            raise StopIteration
    

#this is used to iterate more easily over list of compartments , notice regular map iteration will work too but this is more abstracted out and will work with other containers too

class CompartmentList:
    def __init__(self,_inventory):            
        import CompuCell
        self.inventory = _inventory
        
                
    def __iter__(self):
        return CompartmentListIterator(self)
                
    def __len__(self):
        return self.inventoryByType.size()
        
class CompartmentListIterator:
    def __init__(self,  _cellList):
        import CompuCell
        self.inventory = _cellList.inventory        
        
        self.invItr=CompuCell.mapLongCellGPtrPyItr()
        self.invItr.initialize(self.inventory)        
        self.invItr.setToBegin()
        
    def next(self):
        if not self.invItr.isEnd():
            self.cell=self.invItr.getCurrentRef()
            # print 'self.idCellPair=',self.idCellPair
            # print 'dir(self.idCellPair)=',dir(self.idCellPair)
            self.invItr.next()
            return self.cell
#       
        else:
            raise StopIteration
    
    def __iter__(self):
            return self 



# this is wrapper for std::vector<CellG*>            
class ClusterCellList:
    def __init__(self,_inventory):        
        self.inventory = _inventory
    def __iter__(self):
        return ClusterCellListIterator(self)
        
    def __len__(self):
        return self.inventory.size()        

class ClusterCellListIterator:
    def __init__(self, _cellList):
        import CompuCell
        self.inventory = _cellList.inventory        
        # print "dir(self.inventory)=",dir(self.inventory)        
        self.currentIdx=0
        self.cell=None
        # self.invItr.initialize(self.inventory.getContainer())
        # self.invItr.setToBegin()
    def next(self):
        # if self.invItr !=  self.inventory.end():
        if self.currentIdx<self.inventory.size():
            # print "self.invItr=",dir(self.invItr)
            # print "self.invItr.next()=",self.invItr.next()
            # self.compartmentList = self.invItr.next()
            
            
            
            self.cell=self.inventory[self.currentIdx]
            self.currentIdx+=1
            return self.cell
        else:
            raise StopIteration
    def __iter__(self):
            return self 
            
class CellNeighborList:
    def __init__(self,_neighborTrackerAccessor,_cell):
        self.neighborTrackerAccessor = _neighborTrackerAccessor
        self.cell=_cell
    def __iter__(self):
        return CellNeighborIterator(self)


class CellNeighborIterator:
    def __init__(self, _cellNeighborList):
        import CompuCell
        self.neighborTrackerAccessor = _cellNeighborList.neighborTrackerAccessor
        self.cell=_cellNeighborList.cell
        self.nsdItr=CompuCell.nsdSetPyItr()
        self.nTracker=self.neighborTrackerAccessor.get(self.cell.extraAttribPtr)
        self.nsdItr.initialize(self.nTracker.cellNeighbors)
        self.nsdItr.setToBegin()

    def next(self):
        if not self.nsdItr.isEnd():
            self.neighborCell = self.nsdItr.getCurrentRef().neighborAddress
            self.nsdItr.next()
            return self.neighborCell
        else:
            raise StopIteration
    def __iter__(self):
            return self


class CellNeighborListAuto:
    def __init__(self,_neighborPlugin,_cell):
        self.neighborPlugin=_neighborPlugin
        self.neighborTrackerAccessor=self.neighborPlugin.getNeighborTrackerAccessorPtr()
        self.cell=_cell
    def __iter__(self):
        return CellNeighborIteratorAuto(self)



class CellNeighborIteratorAuto:
    def __init__(self, _cellNeighborList):
        import CompuCell
        self.neighborTrackerAccessor = _cellNeighborList.neighborTrackerAccessor
        self.cell=_cellNeighborList.cell
        self.nsdItr=CompuCell.nsdSetPyItr()
        self.nTracker=self.neighborTrackerAccessor.get(self.cell.extraAttribPtr)
        self.nsdItr.initialize(self.nTracker.cellNeighbors)
        self.nsdItr.setToBegin()


    def next(self):
        if not self.nsdItr.isEnd():
            self.neighborCell = self.nsdItr.getCurrentRef().neighborAddress
            self.currentNsdItr = self.nsdItr.current
            self.currentNeighborSurfaceData=self.nsdItr.getCurrentRef()
            self.nsdItr.next()
            return self.currentNeighborSurfaceData
        else:
            raise StopIteration

    def __iter__(self):
            return self


class CellBoundaryPixelList:

    def __init__(self,_boundaryPixelTrackerPlugin,_cell):
        self.boundaryPixelTrackerPlugin=_boundaryPixelTrackerPlugin
        self.boundaryPixelTrackerAccessor=self.boundaryPixelTrackerPlugin.getBoundaryPixelTrackerAccessorPtr()
        self.cell=_cell

    def __iter__(self):
        return CellBoundaryPixelIterator(self)

    def numberOfPixels(self):
        return self.boundaryPixelTrackerAccessor.get(self.cell.extraAttribPtr).pixelSet.size()



class CellBoundaryPixelIterator:
    def __init__(self, _cellPixelList):
        import CompuCell
        self.boundaryPixelTrackerAccessor = _cellPixelList.boundaryPixelTrackerAccessor
        self.boundaryPixelTrackerPlugin=_cellPixelList.boundaryPixelTrackerPlugin
        self.cell=_cellPixelList.cell
        self.boundaryPixelItr=CompuCell.boundaryPixelSetPyItr()
        self.boundaryPixelTracker=self.boundaryPixelTrackerAccessor.get(self.cell.extraAttribPtr)
        self.boundaryPixelItr.initialize(self.boundaryPixelTracker.pixelSet)
        self.boundaryPixelItr.setToBegin()


    def next(self):
        if not self.boundaryPixelItr.isEnd():
#             self.neighborCell = self.nsdItr.getCurrentRef().neighborAddress
#             self.currentNsdItr = self.nsdItr.current
            self.currentBoundaryPixelTrackerData=self.boundaryPixelItr.getCurrentRef()
            self.boundaryPixelItr.next()
            return self.boundaryPixelTrackerPlugin.getBoundaryPixelTrackerData(self.currentBoundaryPixelTrackerData)
#             return self.currentPixelTrackerData
        else:
            raise StopIteration

    def __iter__(self):
            return self


class CellPixelList:

    def __init__(self,_pixelTrackerPlugin,_cell):
        self.pixelTrackerPlugin=_pixelTrackerPlugin
        self.pixelTrackerAccessor=self.pixelTrackerPlugin.getPixelTrackerAccessorPtr()
        self.cell=_cell

    def __iter__(self):
        return CellPixelIterator(self)

    def numberOfPixels(self):
        return self.pixelTrackerAccessor.get(self.cell.extraAttribPtr).pixelSet.size()



class CellPixelIterator:
    def __init__(self, _cellPixelList):
        import CompuCell
        self.pixelTrackerAccessor = _cellPixelList.pixelTrackerAccessor
        self.pixelTrackerPlugin=_cellPixelList.pixelTrackerPlugin
        self.cell=_cellPixelList.cell
        self.pixelItr=CompuCell.pixelSetPyItr()
        self.pixelTracker=self.pixelTrackerAccessor.get(self.cell.extraAttribPtr)
        self.pixelItr.initialize(self.pixelTracker.pixelSet)
        self.pixelItr.setToBegin()


    def next(self):
        if not self.pixelItr.isEnd():
#             self.neighborCell = self.nsdItr.getCurrentRef().neighborAddress
#             self.currentNsdItr = self.nsdItr.current
            self.currentPixelTrackerData=self.pixelItr.getCurrentRef()
            self.pixelItr.next()
                
            return self.pixelTrackerPlugin.getPixelTrackerData(self.currentPixelTrackerData)
            # return self.currentPixelTrackerData
        else:
            raise StopIteration

    def __iter__(self):
            return self
            

class ElasticityDataList:
    def __init__(self,_elasticityTrackerPlugin,_cell):
        self.elasticityTrackerPlugin=_elasticityTrackerPlugin
        self.elasticityTrackerAccessor=self.elasticityTrackerPlugin.getElasticityTrackerAccessorPtr()
        self.cell=_cell
    def __iter__(self):
        return ElasticityDataIterator(self)


class ElasticityDataIterator:
    def __init__(self, _elasticityDataList):
        import CompuCell
        self.elasticityTrackerAccessor = _elasticityDataList.elasticityTrackerAccessor
        self.cell=_elasticityDataList.cell
        self.elasticityTrackerPlugin=_elasticityDataList.elasticityTrackerPlugin
        self.elasticityTracker=self.elasticityTrackerAccessor.get(self.cell.extraAttribPtr)
        self.elasticityDataSetItr=CompuCell.elasticitySetPyItr()
        self.elasticityDataSetItr.initialize(self.elasticityTracker.elasticityNeighbors)
        self.elasticityDataSetItr.setToBegin()

    def next(self):
        if not self.elasticityDataSetItr.isEnd():
            self.currentElasticityDataSetItr = self.elasticityDataSetItr.current
            self.elasticityData=self.elasticityDataSetItr.getCurrentRef()
            self.elasticityDataSetItr.next()
            return self.elasticityTrackerPlugin.getElasticityTrackerData(self.elasticityData)
#             return self.elasticityData
        else:
            raise StopIteration

    def __iter__(self):
            return self


class PlasticityDataList:
    def __init__(self,_plasticityTrackerPlugin,_cell):
        self.plasticityTrackerPlugin=_plasticityTrackerPlugin
        self.plasticityTrackerAccessor=self.plasticityTrackerPlugin.getPlasticityTrackerAccessorPtr()
        self.cell=_cell
    def __iter__(self):
        return PlasticityDataIterator(self)


class PlasticityDataIterator:
    def __init__(self, _plasticityDataList):
        import CompuCell
        self.plasticityTrackerAccessor = _plasticityDataList.plasticityTrackerAccessor
        self.cell=_plasticityDataList.cell
        self.plasticityTrackerPlugin=_plasticityDataList.plasticityTrackerPlugin
        self.plasticityTracker=self.plasticityTrackerAccessor.get(self.cell.extraAttribPtr)
        self.plasticityDataSetItr=CompuCell.plasticitySetPyItr()
        self.plasticityDataSetItr.initialize(self.plasticityTracker.plasticityNeighbors)
        self.plasticityDataSetItr.setToBegin()

    def next(self):
        if not self.plasticityDataSetItr.isEnd():
            self.currentPlasticityDataSetItr = self.plasticityDataSetItr.current
            self.plasticityData=self.plasticityDataSetItr.getCurrentRef()
            self.plasticityDataSetItr.next()
            return self.plasticityTrackerPlugin.getPlasticityTrackerData(self.plasticityData)
#             return self.plasticityData
        else:
            raise StopIteration

    def __iter__(self):
            return self

            
class FocalPointPlasticityDataList:
    def __init__(self,_focalPointPlasticityPlugin,_cell):
        self.focalPointPlasticityPlugin=_focalPointPlasticityPlugin
        self.focalPointPlasticityTrackerAccessor=self.focalPointPlasticityPlugin.getFocalPointPlasticityTrackerAccessorPtr()
        self.cell=_cell
    def __iter__(self):
        return FocalPointPlasticityDataIterator(self)


class FocalPointPlasticityDataIterator:
    def __init__(self, _focalPointPlasticityDataList):
        import CompuCell
        self.focalPointPlasticityTrackerAccessor = _focalPointPlasticityDataList.focalPointPlasticityTrackerAccessor
        self.cell=_focalPointPlasticityDataList.cell
        self.focalPointPlasticityPlugin=_focalPointPlasticityDataList.focalPointPlasticityPlugin
        self.focalPointPlasticityTracker=self.focalPointPlasticityTrackerAccessor.get(self.cell.extraAttribPtr)
        self.focalPointPlasticityDataSetItr=CompuCell.focalPointPlasticitySetPyItr()
        self.focalPointPlasticityDataSetItr.initialize(self.focalPointPlasticityTracker.focalPointPlasticityNeighbors)
        self.focalPointPlasticityDataSetItr.setToBegin()

    def next(self):
        if not self.focalPointPlasticityDataSetItr.isEnd():
            self.currentFocalPointPlasticityDataSetItr = self.focalPointPlasticityDataSetItr.current
            self.focalPointPlasticityData=self.focalPointPlasticityDataSetItr.getCurrentRef()
            self.focalPointPlasticityDataSetItr.next()
            return self.focalPointPlasticityPlugin.getFocalPointPlasticityTrackerData(self.focalPointPlasticityData)
#             return self.plasticityData
        else:
            raise StopIteration

    def __iter__(self):
            return self            

class InternalFocalPointPlasticityDataList:
    def __init__(self,_focalPointPlasticityPlugin,_cell):
        self.focalPointPlasticityPlugin=_focalPointPlasticityPlugin
        self.focalPointPlasticityTrackerAccessor=self.focalPointPlasticityPlugin.getFocalPointPlasticityTrackerAccessorPtr()
        self.cell=_cell
    def __iter__(self):
        return InternalFocalPointPlasticityDataIterator(self)


class InternalFocalPointPlasticityDataIterator:
    def __init__(self, _focalPointPlasticityDataList):
        import CompuCell
        self.focalPointPlasticityTrackerAccessor = _focalPointPlasticityDataList.focalPointPlasticityTrackerAccessor
        self.cell=_focalPointPlasticityDataList.cell
        self.focalPointPlasticityPlugin=_focalPointPlasticityDataList.focalPointPlasticityPlugin
        self.focalPointPlasticityTracker=self.focalPointPlasticityTrackerAccessor.get(self.cell.extraAttribPtr)
        self.focalPointPlasticityDataSetItr=CompuCell.focalPointPlasticitySetPyItr()
        self.focalPointPlasticityDataSetItr.initialize(self.focalPointPlasticityTracker.internalFocalPointPlasticityNeighbors)
        self.focalPointPlasticityDataSetItr.setToBegin()

    def next(self):
        if not self.focalPointPlasticityDataSetItr.isEnd():
            self.currentFocalPointPlasticityDataSetItr = self.focalPointPlasticityDataSetItr.current
            self.focalPointPlasticityData=self.focalPointPlasticityDataSetItr.getCurrentRef()
            self.focalPointPlasticityDataSetItr.next()
            return self.focalPointPlasticityPlugin.getFocalPointPlasticityTrackerData(self.focalPointPlasticityData)
#             return self.plasticityData
        else:
            raise StopIteration

    def __iter__(self):
            return self              
            

# forEachCellInInventory function takes as arguments inventory of cells and a function that will operate on a single cell
# It will run singleCellOperation on each cell from cell inventory
def forEachCellInInventory(inventory,singleCellOperation):
    import CompuCell
    invItr=CompuCell.STLPyIteratorCINV()
    invItr.initialize(inventory.getContainer())
    invItr.setToBegin()
    cell=invItr.getCurrentRef()
    while (not invItr.isEnd()):
        cell=invItr.getCurrentRef()
        singleCellOperation(cell)
        invItr.next()