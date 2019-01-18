import numpy as np
import resonatorModels
import readReticlesetReport
import pickle

import sys
sys.path.insert(0, './asml_ascii')
sys.path.insert(0, './semiwafer')
from asml_ascii import asmlAscii, asmlCells, asmlSection, asmlSectionList
import semiwafer

class resonator(object):
    """ Class that represents a single resonator
    
    Stores the target frequency, physical placement, slider shifts to meet the target
    frequency, and the model name and design parameters used to solve for the shifts.

    Parameters:
    ===========
    f0          : target frequency
    wx,wy       : position of wiggle
    sx,sy       : position of slider
    delta       : shift of slider
    modelname   : name of resonator model function in resonatormodels.py
    designparams: parameters to the model, e.g. Cc=4.47 fF, Lc=120.18 pH, etc.
    """    
    def setFrequency(self,f0):
        """ Sets the target resonance frequency """
        self.f0 = f0
    
    def setPlacement(self,wx,wy,sx,sy):
        """ Sets the placement of wiggles and sliders """
        self.wx = wx
        self.wy = wy
        self.sx = sx
        self.sy = sy
    
    def setModel(self,modelname,**designparams):
        """ Sets the resonator frequency model and its input parameters """
        self.modelname = modelname
        self.designparams = designparams
    
    def calculateShift(self):
        """ Uses model to calculate shifts of sliders relative to wiggles """
        if not hasattr(self,'f0'):
            raise ValueError('Target frequency must be defined.')
        if not hasattr(self,'modelname'):
            raise ValueError('Resonator model must be defined.')

        self.delta = resonatorModels.calcDelta(self.modelname,self.designparams,self.f0)
        self.sx = self.wx - self.delta


class resonatorDistribution(object):
    """
    Class that represents a distribution of wiggles and sliders across a chip

    Parameters:
    ===========
    nres        : number of resonators in the distribution
    bandname    : name of band
    wigglegds   : name of resonator base GDS file
    slidergds   : name of slider GDS file
    resonators  : list of resonator objects
    """
    def __new__(cls, nres=0, filename=None):
        """ Instantiator for resonator distribution

        If passed a filename, loads the pickled instance instead of creating a new instance.
        """
        if filename is not None:
            with open(filename,'rb') as f:
               inst = pickle.load(f)
            if not isinstance(inst, cls):
               raise TypeError('Unpickled object is not of type {}'.format(cls))
        else:
            # inst = super(resonatorDistribution, cls).__new__(cls,nres)
            inst = super(resonatorDistribution, cls).__new__(cls)

        return inst

    def __init__(self, nres=0, filename=None):
        """ Initializer for resonator distribution
        
        If passed a filename, do nothing, as the constructor will have loaded the object
        state from a pickle file. If not given a filename, initialize object for a given
        number of resonators.
        """
        if filename is None:
            if not isinstance(nres, int) or nres < 0:
                raise ValueError('Resonator count must be a positive integer')
            else:
                self.nres = nres
                self.resonators = []
                for n in range(self.nres):
                    self.resonators.append(resonator())
    
    def save(self,filename=None):
        """ Save values to pickle file """
        if filename is None:
            filename = self.bandname + '.pkl'
        with open(filename,'wb') as f:
            pickle.dump(self,f)

    @staticmethod
    def load(filename):
        """ Load resonator distribution from pickle file """
        with open(filename,'rb') as f:
            return pickle.load(f)
    
    def setImages(self,bandname,wigglegds,slidergds):
        """ Set images for usage in the jobfile

        This bandname is used in the construction of image names for the image
        definition, image distribution, and reticle data sections in the jobfile.

        GDS file names are used to map the image names to reticle locations
        according to a reticleset report file.
        """
        self.bandname = bandname
        self.wigglegds = wigglegds
        self.slidergds = slidergds

    def setResonatorCount(self,nres):
        """ Set the number of resonators in the distribution

        If the requested count is greater than the number currently in
        the distribution, add resonators to the end of the list.

        If the requested count is less than the number currently in the
        distribution, remove resonators from the end of the list.
        """
        if not isinstance(nres, int) or nres < 0:
            raise ValueError('Resonator count must be a positive integer')            
        
        if self.nres < nres:
            # Expand resonator list
            for n in range(self.nres,nres):
                self.resonators.append(resonator())
        elif self.nres > nres:
            # Shrink resonator list
            for n in range(self.nres - nres):
                self.resonators.pop()
        
        self.nres = nres

    def distributeFrequencies(self,f0s):
        """ Distributes the target resonance frequencies """
        if len(f0s) != self.nres:
            raise ValueError('Number of frequencies doesn\'t match number of resonators')
        
        for n in range(self.nres):
            self.resonators[n].setFrequency(f0s[n])
    
    def distributePositions(self,wx0,wy0,sx0,sy0,dx):
        """ Generates base positions for wiggles and sliders

        wx0,wy0 : center position for the first wiggle
        sx0,sy0 : base center position for the first slider
        dx      : lateral spacing between resonators

        Note: Assumes linear placement in the x-direction
        """
        for n in range(self.nres):
            wx = wx0 + n*dx
            wy = wy0
            sx = sx0 + n*dx
            sy = sy0
            self.resonators[n].setPlacement(wx,wy,sx,sy)

    def setModelForOne(self,n,modelname,**designparams):
        """ Sets the modelname and design parameters for a single resonator """
        self.resonators[n].setModel(modelname,**designparams)

    def setModelForAll(self,modelname,**designparams):
        """ Sets the modelname and design parameters for all resonators """
        for n in range(self.nres):
            self.resonators[n].setModel(modelname,**designparams)

    def calculateShifts(self):
        """ Uses model to calculate shifts of sliders relative to wiggles """
        for n in range(self.nres):
            self.resonators[n].calculateShift()
    
    def makeImageDistributionSectionList(self,cx,cy):
        """ Creates a list of image distribution sections """
        imdistseclist = asmlSectionList('image_distribution')
        for n in range(self.nres):
            wigglesec = asmlSection('image_distribution')
            wigglesec.set('image_id', 'WIGGLE-'+str.upper(self.bandname))
            wigglesec.set('instance_id', '{:03d}'.format(n+2))
            wigglesec.set('cell_selection', [str(cx), str(cy)])
            wigglesec.set('distribution_action', 'I')
            wigglesec.set('image_cell_shift', [self.resonators[n].wx, self.resonators[n].wy])
            imdistseclist.append(wigglesec)

            slidersec = asmlSection('image_distribution')
            slidersec.set('image_id', 'SLIDER-'+str.upper(self.bandname))
            slidersec.set('instance_id', '{:03d}'.format(n+2))
            slidersec.set('cell_selection', [str(cx), str(cy)])
            slidersec.set('distribution_action', 'I')
            slidersec.set('image_cell_shift', [self.resonators[n].sx, self.resonators[n].sy])
            imdistseclist.append(slidersec)
        
        return imdistseclist
    
    def makeInstanceDefinitionSectionList(self):
        """ Creates a list of instance definition sections """
        instseclist = asmlSectionList('instance_definition')
        for n in range(self.nres):
            instsec = asmlSection('instance_definition')
            instsec.set('instance_id', '{:03d}'.format(n+2)) # Instance ids start at 2 for some reason
            instseclist.append(instsec)

        return instseclist
    
    def makeImageDefinitionSectionList(self,reticlesetreportfilename):
        """ Creates a list of image definition sections """
        reticleimages = readReticlesetReport.readReticlesetReport(reticlesetreportfilename)

        imdefseclist = asmlSectionList('image_definition')

        image_id = 'WIGGLE-'+str.upper(self.bandname)
        for n in range(len(reticleimages)):
            retim = reticleimages[n]
            if (retim.gds_file == self.wigglegds) and (retim.xic_layer == 'BEV'):
                imdefsec = asmlSection('image_definition')
                imdefsec.set('image_id', image_id)
                imdefsec.set('reticle_id', retim.reticle_id)
                imdefsec.set('image_size', [retim.width,retim.height])
                imdefsec.set('mask_size', [retim.width,retim.height])
                imdefsec.set('image_shift', [retim.x_shift,retim.y_shift])
                imdefsec.set('mask_shift', [retim.x_shift,retim.y_shift])
                imdefseclist.append(imdefsec)
                break
        else:
            raise ValueError('Couldn\'t find resonator base image in reticle plates')

        image_id = 'SLIDER-'+str.upper(self.bandname)
        for n in range(len(reticleimages)):
            retim = reticleimages[n]
            if (retim.gds_file == self.slidergds) and (retim.xic_layer == 'BEV'):
                imdefsec = asmlSection('image_definition')
                imdefsec.set('image_id', image_id)
                imdefsec.set('reticle_id', retim.reticle_id)
                imdefsec.set('image_size', [retim.width,retim.height])
                imdefsec.set('mask_size', [retim.width,retim.height])
                imdefsec.set('image_shift', [retim.x_shift,retim.y_shift])
                imdefsec.set('mask_shift', [retim.x_shift,retim.y_shift])
                imdefseclist.append(imdefsec)
                break
        else:
            raise ValueError('Couldn\'t find slider image in reticle plates')

        return imdefseclist

    def makeReticleDataSectionList(self,reticlesetreportfilename):
        """ Creates a list of reticle data sections """
        reticleimages = readReticlesetReport.readReticlesetReport(reticlesetreportfilename)

        retdataseclist = asmlSectionList('reticle_data')

        image_id = 'WIGGLE-'+str.upper(self.bandname)
        for n in range(len(reticleimages)):
            retim = reticleimages[n]
            if (retim.gds_file == self.wigglegds) and (retim.xic_layer == 'BEV'):
                retdataseclist.append(retim.make_reticle_data_section(jobimage=image_id))
                break
        else:
            raise ValueError('Couldn\'t find resonator base image in reticle plates')

        image_id = 'SLIDER-'+str.upper(self.bandname)
        for n in range(len(reticleimages)):
            retim = reticleimages[n]
            if (retim.gds_file == self.slidergds) and (retim.xic_layer == 'BEV'):
                retdataseclist.append(retim.make_reticle_data_section(jobimage=image_id))
                break
        else:
            raise ValueError('Couldn\'t find resonator base image in reticle plates')

        return retdataseclist
    
    def makeChipJobfile(self,reticlesetreportfilename,cx,cy):
        """ Creates a single-chip jobfile from the resonator distribution """
        jobfile = asmlAscii(filename='umuxbevtemplate.txt')

        # # Need to rewrite asml_ascii to make a functional merge
        # jobfile.merge(self.makeImageDefinitionSectionList(reticlesetreportfilename))
        # jobfile.merge(self.makeImageDistributionSectionList(0,0))
        # jobfile.merge(self.makeInstanceDefinitionSectionList())
        # jobfile.merge(self.makeReticleDataSectionList(reticlesetreportfilename))

        imdefseclist = self.makeImageDefinitionSectionList(reticlesetreportfilename)
        for s in jobfile.sections:
            if s.name == 'image_definition':
                for t in imdefseclist.sections:
                    s.append(t)
                break

        imdistseclist = self.makeImageDistributionSectionList(0,0)
        for s in jobfile.sections:
            if s.name == 'image_distribution':
                for t in imdistseclist.sections:
                    s.append(t)
                break
        
        instdefseclist = self.makeInstanceDefinitionSectionList()
        for s in jobfile.sections:
            if s.name == 'instance_definition':
                for t in instdefseclist.sections:
                    s.append(t)
                break

        retdataseclist = self.makeReticleDataSectionList(reticlesetreportfilename)
        for s in jobfile.sections:
            if s.name == 'reticle_data':
                for t in retdataseclist.sections:
                    s.append(t)
                break

        return jobfile