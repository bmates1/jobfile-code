import sys
sys.path.insert(0, './asml_ascii')
sys.path.insert(0, './semiwafer')

import asml_ascii
import resonatorDistribution
import semiwafer

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class cellDistribution(object):
    """ Distribution of chips across a wafer

    Allows placement and removal of resonator distributions
    at different locations on the wafer. Intended to interface
    with a placement GUI.

    Generates jobfiles for subsets of the distribution of chips
    
    Parameters:
    ===========
    wfr_diameter   : diameter of wafer (mm)
    edge_clearance : safe distance from perimeter of wafer (mm)
    x0,y0          : center of the [0,0] cell (mm)
    width,height   : cell dimensions (mm)

    bands          : dictionary of resonator distribution objects,
                     indexed by bandname
    cells          : dictionary of lists of cell coordinate tuples,
                     indexed by bandname

    """

    def __new__(cls, wfr_diameter=76.2, edge_clearance=2.0, x0=0.0, y0=0.0, width=0.0, height=0.0, filename=None):
        """ Instantiator for cell distribution

        If passed a filename, loads the pickled instance instead of creating a new instance.
        """
        if filename is not None:
            with open(filename,'rb') as f:
               inst = pickle.load(f)
            if not isinstance(inst, cls):
               raise TypeError('Unpickled object is not of type {}'.format(cls))
        else:
            inst = super(cellDistribution, cls).__new__(cls)

        return inst

    def __init__(self, wfr_diameter=76.2, edge_clearance=0.0, x0=0.0, y0=0.0, width=5.0, height=5.0, filename=None):
        """ Initialize data structures for cell distribution """
        if filename is None:
            self.wafer = semiwafer.semiWaferCells(size='3 inch',x0=x0,y0=y0,width=width,height=height,edge_clearance=edge_clearance)

            # self.wfr_diameter = wfr_diameter
            # self.edge_clearance = edge_clearance
            # self.x0 = x0
            # self.y0 = y0
            # self.width = width
            # self.height = height

            self.bands = {} # Initialize empty dictionary of resonator distribution objects
            self.cells = {} # Initialize empty dictionary of cell placement lists
    
    def save(self,filename):
        """ Save chipDistribution object to pickle file """
        with open(filename,'wb') as f:
            pickle.dump(self,f)
    
    @staticmethod
    def load(filename):
        """ Load chipDistribution object from pickle file """
        with open(filename,'rb') as f:
            return pickle.load(self,f)
    
    def importResonatorDistribution(self,filename):
        """ Import resonatorDistribution object to be placed in cells """
        rd = resonatorDistribution.resonatorDistribution(filename=filename)

        if rd.bandname in self.bands:
            raise ValueError('Band name already in use')
        else:
            self.bands[rd.bandname] = rd    # Add the new resonator distribution to the dictionary of bands
            self.cells[rd.bandname] = []    # Add empty list to dictionary of cell positions
    
    def placeResonatorDistribution(self,bandnames,cells):
        """ Attempt to place resonator distributions in each of a list of cells
        
        bandnames   : list of band names specifying already imported resonator distributions
        cells       : list of [cx,cy] pairs specifying cell positions e.g. [[0,0],[0,1],[1,1]]

        Note: will not duplicate a placement of a band in the same cell
        """
        for bandname in bandnames:
            if bandname not in self.bands:
                raise ValueError('Unknown resonator distribution')
            else:
                for [cx,cy] in cells:
                    if not self.wafer.cellValid(cx,cy):
                        raise ValueError('Cell not valid')
                    elif bandname not in self.getBandnames(cx,cy):
                        self.cells[bandname].append([cx,cy])    # Add (cx,cy) to list of cell locations for that bandname
    
    def removeResonatorDistribution(self,bandnames=None,cells=None):
        """ Remove resonator distribution from a cell

        If both band names and cells are specified, removes those bands from those
        cells. If the band names are specified and the cells are not, removes those
        bands from all cells. If the cells are specified and the band names are not,
        removes all bands from those cells. If neither are specified, fully clear
        the distribution.
        """
        if bandnames is None:
            self.removeResonatorDistribution(self.bands.keys(),cells)   # Clear all bands from specified cells
        elif cells is None:
            for bandname in bandnames:
                self.cells[bandname] = []                               # Clear all cells for specified bands
        else:
            for bandname in bandnames:
                for cell in cells:
                    if cell in self.cells[bandname]:
                        self.cells[bandname].remove[cell]               # Clear specified bands from specified cells

    def getBandnames(self,cx,cy):
        """ Find band names present in a given cell """
        bandnames = []

        for bandname in self.cells:
            if [cx,cy] in self.cells[bandname]:
                bandnames.append(bandname)

        return bandnames

    # def cellValid(self,cx,cy):
    #     """ Check if a cell fits within the edge clearance of the wafer """
    #     for n in [-0.5,0.5]:
    #         x = self.x0 + (cx+n)*self.width
    #         for m in [-0.5,0.5]:
    #             y = self.y0 + (cy+m)*self.height
    #             if np.sqrt(x**2 + y**2) > (self.wfr_diameter/2. - self.edge_clearance):
    #                 return False
    #     else:
    #         return True

    # def plotCellDistribution(self):
    #     """ Plot the cell distribution """

    #     wafer = semiwafer.semiWafer(size='3 inch')

    #     theta1 = np.arcsin(wafer.secondary_flat_length / wafer.diameter)
    #     theta2 = np.arcsin(wafer.primary_flat_length / wafer.diameter)

    #     r = wafer.diameter / 2.
    #     theta = np.concatenate((np.linspace(-(np.pi/2. - theta2),(np.pi/2. - theta1),100),np.linspace((np.pi/2. + theta1),(3*np.pi/2. - theta2),100),np.array([(3*np.pi/2. + theta2)])))

    #     fig,ax = plt.subplots(1)
    #     ax.plot(r*np.cos(theta),r*np.sin(theta),'k')
    #     plt.axis('equal')

    #     for cx in range(-int((r+self.x0)/self.width)-1,int((r-self.x0)/self.width)+1):
    #         for cy in range(-int((r+self.y0)/self.height)-1,int((r-self.y0)/self.height)+1):
    #             if self.cellValid(cx,cy):
    #                 ax.add_patch(patches.Rectangle((self.x0+self.width*(cx-0.5),self.y0+self.height*(cy-0.5)),self.width,self.height,linewidth=1,edgecolor='k',facecolor='none',fill=False))
    #                 bandstring = ''
    #                 for bandname in self.getBandnames(cx,cy):
    #                     bandstring = bandstring + bandname + ' / '
    #                 bandstring = bandstring[:-3]
    #                 ax.text(self.x0+self.width*cx, self.y0+self.height*cy,bandstring,horizontalalignment='center',verticalalignment='center')

    #     plt.show()


    def makeJobfileByCells(self,reticlesetreportfilename,cells):
        """ Generate ASCII jobfile for specified cells """

        jobfile = asmlAscii(filename='umuxbevtemplate.txt')

        for [cx,cy] in cells:
            for bandname in self.getBandnames(cx,cy):
                jobfile.merge(self.bands['bandname'].makeChipJobfile(reticlesetreportfilename,cx,cy))
        
        return jobfile
    
    def makeJobfileByBands(self,reticlesetreportfilename,bandnames):
        """ Generate ASCII jobfile for specified bands """

        jobfile = asmlAscii(filename='umuxbevtemplate.txt')

        for bandname in bandnames:
            for [cx,cy] in self.cells[bandname]:
                jobfile.merge(self.bands['bandname'].makeChipJobfile(reticlesetreportfilename,cx,cy))
        
        return jobfile