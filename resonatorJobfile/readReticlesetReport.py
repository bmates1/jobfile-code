import sys
sys.path.insert(0, './asml_ascii')

from asml_ascii import asmlAscii, asmlCells, asmlSection, asmlSectionList
import re

UMUXEXPOSURES = {'CE':150.0,
                 'AL':150.0,
                 'BES':190.0,
                 'R1':180.0,
                 'I1':190.0,
                 'W1':190.0,
                 'I1X':190.0,
                 'BEV':190.0}

class ReticleImage():
    """
    Class that holds relevant parameters for each image on a reticle plate, as specified
    in the Reticleset report file.
    """
    def __init__(self, reticle_id, gds_file, xic_layer, x_shift, y_shift, width, height):
        """
        Parameters
        ==========
        reticle_id : string
            Name of reticle plate the image is on, e.g. TESTRET-00
        gds_file : string
            Name of GDS file from which Reticleset generated the image. Can be used
            as one way to identify design splits.
        xic_layer : string
            Name of Xic layer associated with the image. Can be used to auto-map
            reticle images to jobfile layers. Can also identify design splits.
        x_shift, y_shift : float
            Location of the center of the image on the reticle plate (in mm).
        width, height : float
            Size of the image on the reticle plate (in mm).
        """
        self.reticle_id = reticle_id
        self.gds_file = gds_file
        self.xic_layer = xic_layer
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.width = width
        self.height = height


    def make_reticle_data_section(self, joblayer=None, jobimage=None, exposure=0.0):
        """
        Creates an AsmlAscii reticle_data section that can be added to the
        jobfile.
        """
        if joblayer is not None:
            layer = joblayer
        else:
            layer = self.xic_layer
        
        if jobimage is not None:
            image = jobimage
        else:
            image = self.gds_file[:-4]
        
        if exposure == 0.0:
            exposure = UMUXEXPOSURES[layer]

        section = asmlSection('reticle_data')
        section.set('image_id', image)
        section.set('layer_id', layer)
        section.set('reticle_id', self.reticle_id)
        section.set('image_size', [self.width, self.height])
        section.set('mask_size', [self.width, self.height])
        section.set('image_shift', [self.x_shift, self.y_shift])
        section.set('mask_shift', [self.x_shift, self.y_shift])
        section.set('energy_actual', float(exposure))
        section.set('image_usage','Y')

        return section



def readReticlesetReport(filename):
    """
    Parses a Reticleset report file to extract relevant parameters
    with string operations and regular expressions.
    Caution: depends on Reticleset report formatting
    """
    with open(filename,'r') as f:
        reportstring = f.read()

    # Split report into sections by reticle
    reportstring = '\n' + reportstring
    reticlestrings = reportstring.split('\nReticle ')
    # TODO: check that the regular expression parsing succeeds

    reticleimages = []
    # For each reticle plate section
    for r in range(1,len(reticlestrings)):  # First string from the split is empty

        # Grab reticle name
        reticle_id = re.match(r'([\w-]*)  ', reticlestrings[r]).group(1)

        # Split into sections by reticle image
        imagestrings = reticlestrings[r].split('\n\n')

        # For each image on the reticle plate
        for imagestring in imagestrings:

            # Search for: gds filename, xic layer, x shift, y shift, width, and height
            gds_file = re.search(r'GDS File: (\S*\.gds)', imagestring).group(1)
            xic_layer = re.search(r'Layer Name:(\w*)', imagestring).group(1)
            m = re.search(r'Center coordinates: x=([-\d.]+) y=([-\d.]+)', imagestring)
            x_shift = float(m.group(1))
            y_shift = float(m.group(2))
            m = re.search(r'Image Size: width=([\d.]+) height=([\d.]+)', imagestring)
            width = float(m.group(1))
            height = float(m.group(2))

            # Create ReticleImage object and add it to the list
            reticleimages.append(ReticleImage(reticle_id, gds_file, xic_layer, x_shift, y_shift, width, height))

    return reticleimages