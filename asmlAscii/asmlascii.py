# -*- coding: utf-8 -*-

"""
@author: hiltong
Created Dec, 2013 by Gene Hilton
Edited Jan, 2019 by Ben Mates

Classes that provide the capability of reading ASCII jobfiles,
manipulating them in various ways, and writing them back to ASCII.
"""

from __future__ import print_function, absolute_import, division
# import shlex
from io import StringIO, BytesIO, IOBase
from collections import OrderedDict
import copy
import warnings
import six
import re
from asmljobsdef import ASMLJOBSECTIONS,ASMLELEMENTALIGN,ASMLELEMENTINDENT


if six.PY2:
    COMPATFILE = file
    COMPATSTRIO = BytesIO
elif six.PY3:
    COMPATFILE = IOBase
    COMPATSTRIO = StringIO
else:
    raise(IOError, 'Can\'t figure out python version')


class asmlElement(object):
    """ Class for parameters specified in an ASML jobfile

    Each element object corresponds to a line in the ASCII translation of the ASML jobfile
    or, equivalently, to a field or set of fields in the jobfile editor. Each object
    stores the following, with the default parameters defined in asmljobsdef.py:

    name            : name of element
    count           : number of data values defined by element
    element_type    : data type ['int','float','string','multiline']
    is_optional     : whether the element is optional in its section
    default         : default value on element creation
    validator       : list beginning with 'list' or 'range' which defines acceptable values
    value           : value of the element

    Class methods provide functionality to get and set values, to validate values, and to read
    and make an ASCII string representing the element.
    """
    def __init__(self,name=None,count=0,element_type=None,is_optional=True,default=None,validator=None,value=None):
        """ Initializes element parameters
        
        If no value is specified in the constructor call, uses the default value.
        """
        self.name = name
        self.count = count
        self.element_type = element_type
        self.is_optional = is_optional
        self.default = default
        self.validator = validator
        # Do we actually use or care about defined_in?
        # if defined_in is not None:
        #     self.defined_in = defined_in
        if value is None:
            self.value = self.default   # Use default if no value specified
        else:
            self.set(value)

    def set(self,value):
        """ Sets the element value """
        # Pack single value into list
        if not isinstance(value,list):
            value = [value]
        
        if self.validate(value):
            self.value = value
    
    def get(self):
        """ Gets the element values """
        if self.value is None: return None

        return self.value
    
    def validate(self,value):
        """ Validates a value against the element specifications

            1. checks for correct number of values
            2. checks for correct value type
            3. checks against range or list of acceptable values

        Note: Check #3 does not raise an exception, but returns True or False in case a
        user wants to test values in a loop.
        """

        # Should we check against string maxlength?

        if not isinstance(value,list):
            raise TypeError('{} element, received unknown {}'.format(self.name,type(value)))
        
        # Check number of values passed
        if len(value) != self.count:
            raise TypeError('{} element expects {:d} value(s)'.format(self.name,self.count))

        # Check type of values passed
        for v in value:
            if self.element_type == 'int':
                if not isinstance(v,int):
                    raise TypeError('{} element expects integer, received {}'.format(self.name,type(v)))
            elif self.element_type == 'float':
                if not isinstance(v,float):
                    raise TypeError('{} element expects float, received {}'.format(self.name,type(v)))
            if self.element_type == 'string' or self.element_type == 'multiline':
                if not isinstance(v,str):
                    raise TypeError('{} element expects string, received {}'.format(self.name,type(v)))
        
        # Validate against list or range
        for v in value:
            if self.validator is not None:
                if self.validator[0] == 'list':
                    if v not in self.validator[1:]:
                        # raise ValueError('{} element expects values from set {}, received {}'.format(self.name,self.validator[1:],v))
                        return False
                elif self.validator[0] == 'range':
                    if v < self.validator[1] or v > self.validator[2]:
                        # raise ValueError('{} element expects values between {} and {}, received {}'.format(self.name,self.validator[1],self.validator[2],v))
                        return False
        
        return True

    def makeAscii(self):
        """ Generates ASCII string representation of element """
        asciistring = '   ' + self.name + ' '*(ASMLELEMENTALIGN - ASMLELEMENTINDENT - len(self.name))
        for n in range(self.count):
            if self.element_type == 'int':
                asciistring += '{:d} '.format(self.value[n])
            elif self.element_type == 'float':
                asciistring += '{:.6f} '.format(self.value[n])
            elif self.element_type == 'string':
                asciistring += '"{}" '.format(self.value[n])
            elif self.element_type == 'multiline':
                if n > 0:
                    asciistring += ' '*(ASMLELEMENTALIGN)
                asciistring += '"{}"\n'.format(self.value[n])

        return asciistring[:-1] # Trim final whitespace character
    
    def readAscii(self,asciistring):
        """ Parses ASCII string representation of element

        Note that the section reader extracts the element name and only passes the string containing the values.
        """
        if self.element_type == 'int':
            value = list(map(int,re.findall(r'[-]?[0-9]+',asciistring)))
        elif self.element_type == 'float':
            value = list(map(float,re.findall(r'[-]?[0-9\.]+',asciistring)))
        elif self.element_type == 'string':
            value = list(map(str,re.findall(r'"([^"]*)"',asciistring)))
        elif self.element_type == 'multiline':
            value = list(map(str,re.findall(r'"([^"]*)"',asciistring)))

        self.set(value)



class asmlSection(object):
    """ Class for sections specified in an ASML jobfile

    Each object corresponds to a section block of lines in the ASCII translation
    of the ASML jobfile and to a logical organization of fields (e.g. a page) in
    the jobfile editor. Each object stores the following:

    section name     : name of section
    is_optional      : whiether the section is required in the jobfile
    multiple_allowed : whether multiple instances of the section are allowed in the jobfile
    id_element       : element which distinguishes instances of the same section

    as well as a dictionary of element objects containing the data for the jobfile.

    Class methods provide functionality to get and set element values, to read and
    make an ASCII string representing the element, and to compare sections.
    """
    def __init__(self,sectionname):
        """ Initializes section parameters and elements
        
        Looks up section specifications in asmljobsdef.py and fills parameters with
        their default values.
        """
        if sectionname not in ASMLJOBSECTIONS:
            raise ValueError('Section {} not found in ASMLJOBSECTIONS'.format(sectionname))

        self.sectionname = sectionname
        self.is_optional = ASMLJOBSECTIONS[sectionname]['is_optional']
        self.multiple_allowed = ASMLJOBSECTIONS[sectionname]['multiple_allowed']
        self.id_elements = ASMLJOBSECTIONS[sectionname]['id_elements']

        self.elements = OrderedDict()
        for elementname in ASMLJOBSECTIONS[sectionname]['elements']:
            elementdict = ASMLJOBSECTIONS[sectionname]['elements'][elementname]
            self.elements[elementname] = asmlElement(name=elementname,count=elementdict['count'],element_type=elementdict['element_type'],
                                        is_optional=elementdict['is_optional'],default=elementdict['default'],
                                        validator=elementdict['validator'])
    
    def set(self,elementname,value):
        """ Sets the value of an element """
        if elementname not in ASMLJOBSECTIONS[self.sectionname]['elements']:
            raise ValueError('Element {} not found in section {} in ASMLJOBSECTIONS'.format(elementname,self.sectionname))
        
        self.elements[elementname].set(value)
    
    def get(self,elementname):
        """ Gets the value of an element """
        if elementname not in ASMLJOBSECTIONS[self.sectionname]['elements']:
            raise ValueError('Element {} not found in section {} in ASMLJOBSECTIONS'.format(elementname,self.sectionname))
        
        return self.elements[elementname].get()
    
    def isSpecified(self):
        """ Checks if section is adequately specified """
        for elementname in ASMLJOBSECTIONS[self.sectionname]['elements']:
            if (not ASMLJOBSECTIONS[self.sectionname]['elements'][elementname]['is_optional']
                and self.elements[elementname].get() is None):
                return False

        return True
    
    @staticmethod
    def interfere(section1,section2):
        """ Checks if two section objects interfere

        Sections can interfere if:
            1. Only one section of that name is allowed, or
            2. Their id_elements match, e.g. if two reticle_data sections specify
               reticle data for the same image/layer.
        """
        if section1.sectionname == section2.sectionname:
            if not section1.multiple_allowed:
                return True     # Only one instance allowed
            
            for id_element in section1.id_elements:
                if section1.elements[id_element] != section2.elements[id_element]:
                    return False
            else:
                return True     # All ID elements identical
        else:
            return False        # Why would two different types of section interfere?

    def makeAscii(self):
        """ Generates ASCII string representation of section
        
        Within the bracketing section text, includes ASCII representation
        for all the elements specified either by the user or by the defaults.
        """
        asciistring = 'START_SECTION ' + self.sectionname + '\n'
        for elementname in self.elements:
            if self.elements[elementname].get() is not None:
                asciistring += self.elements[elementname].makeAscii() + '\n'
        asciistring += 'END_SECTION'

        return asciistring

    def readAscii(self,asciistring):
        """ Reads an ASCII string representation of a jobfile section

        Uses the definitions in asmljobsdef.py to define the section and steps through the
        specified elements in order, attempting to parse the lines of the section into the
        element objects.

        The ASCII string must include all non-optional elements and present the elements
        in the same order as specified in asmljobsdef.py.
        """
        sectionlines = asciistring.split('\n')
        self.elements = OrderedDict()

        # Steps through the elements of the section attempting to match them to lines
        # in the section body. Requires elements to be in fixed order.
        l = 0
        for elementname in ASMLJOBSECTIONS[self.sectionname]['elements']:
            elementdict = ASMLJOBSECTIONS[self.sectionname]['elements'][elementname]
            if l < len(sectionlines) and sectionlines[l][:ASMLELEMENTALIGN] == '   ' + elementname + ' '*(ASMLELEMENTALIGN - ASMLELEMENTINDENT - len(elementname)):
                newelement = asmlElement(name=elementname,count=elementdict['count'],element_type=elementdict['element_type'],
                                        is_optional=elementdict['is_optional'],default=elementdict['default'],
                                        validator=elementdict['validator'])
                newvalue = sectionlines[l][ASMLELEMENTALIGN:]
                l += 1
                if elementdict['element_type'] == 'multiline':
                    while l < len(sectionlines) and sectionlines[l][:ASMLELEMENTALIGN] == ' '*(ASMLELEMENTALIGN):
                        newvalue += '\n' + sectionlines[l][ASMLELEMENTALIGN:]
                        l += 1
                newelement.readAscii(newvalue)
                self.elements[elementname] = newelement     # Add element to section element dict
            elif not elementdict['is_optional']:
                raise ValueError('Required element {} not found'.format(elementname))
            
        if l != len(sectionlines):
            # Note that a section with duplicate elements will land here
            raise ValueError('Unread lines in section {}'.format(sectionname))
    
    def fixDelimBug(self):
        """ Fixes strings contaminated by JDAS bug

        The ASML program that converts binary<->ASCII (JDAS) seems to have a bug.
        For jobs with compound images it writes the first instance_id as "<Default>"
        instead of "Default". The fix_delim_bug option only applies to the fields
        where this bug seems to be a problem so that other strings may use the
        < and > characters if needed.
        """
        for elementname in self.elements:
            if 'fix_delim_bug' in ASMLJOBSECTIONS[self.sectionname]['elements'][elementname]:
                tempvals = self.get(elementname)
                for n in range(len(tempvals)):
                    if tempvals[n][0]=='<' and tempvals[n][-1]=='>':
                        tempvals[n] = tempvals[n][1:-1]                 # Strip the angle brackets from the string
            
                self.elements[elementname].set(tempvals)



class asmlAscii(object):
    """ Class for ASML jobfile

    Each object corresponds to an entire (possibly not fully specified) ASML
    jobfile, organized as a dictionary of lists of section objects, specified
    by section type.

    Class methods provide functionality to get, remove, and append sections,
    to merge jobfiles, to check for section interferences and jobfile completion,
    and to read and write ASCII strings and files.
    """
    def __init__(self):
        """ Initializes dictionary of empty section lists """
        self.sections = OrderedDict()
        for sectionname in ASMLJOBSECTIONS:
            self.sections[sectionname] = []
    
    def append(self,newsection,check_interference=False):
        """ Adds a new section object to the jobfile

        Can check for interference between the new section and
        existing sections and only add the new section if it does
        not interfere.

        Returns boolean for convenience of calling processes.
        """
        if check_interference:
            for section in self.sections[newsection.sectionname]:
                if asmlSection.interfere(section,newsection):
                    return False

        # If the interference test passes, append the new section            
        self.sections[newsection.sectionname].append(newsection)
        return True

    def get(self,sectionname,**id_element_values):
        """ Get sections from jobfile

        Identifies sections by name and optional specification of
        ID elements. If the specification matches several sections
        in the jobfile, returns a list of matching sections.
        """
        matchsections = []
        for section in self.sections[sectionname]:
            id_match = True
            for id_element_name in id_element_values:
                if id_element_name not in section.id_elements:
                    raise ValueError('{} not a valid id element for {} section'.format(id_element_name,sectionname))

                if section.get(id_element_name) != id_element_values[id_element_name]:
                    id_match = False    # Change match to False if any ID element disagrees
                    
            if id_match:
                matchsections.append(section)
        
        return matchsections

    def remove(self,sectionname,**id_element_values):
        """ Removes sections from jobfile

        Identifies sections by name and optional specification of
        ID elements. If the specification matches several sections
        in the jobfile, removes all of them.
        """
        for section in self.sections[sectionname]:
            id_match = True
            for id_element_name in id_element_values:
                if id_element_name not in section.id_elements:
                    raise ValueError('{} not a valid id element for {} section'.format(id_element_name,sectionname))

                if section.get(id_element_name) != id_element_values[id_element_name]:
                    id_match = False
            if id_match:
                self.sections.remove(section)
    
    @staticmethod
    def merge(job1,job2):
        """ Merges two jobfiles

        If there is any interference between sections of the jobfiles
        ignore conflicting sections from the second jobfile.
        """
        mergedjob = copy.deepcopy(job1)
        for sectionname in ASMLJOBSECTIONS:
            for section in job2.sections[sectionname]:
                mergedjob.append(section,check_interference=True)
        
        return mergedjob
    
    def isSpecified(self):
        """ Checks whether jobfile is adequately specified

        An adequately specified jobfile contains all non-optional sections,
        only one of each non-multiple-allowed sections, and has sections
        that are themselves adequately specified.
        """

        # There may be other things to check.
        # 
        # 1. Are layers in correct order?
        # 2. Does every layer have a PROCESS_DATA section?
        # 

        for sectionname in ASMLJOBSECTIONS:
            if (not ASMLJOBSECTIONS[sectionname]['is_optional']
                and len(self.sections[sectionname]) == 0):
                return False
            
            if (not ASMLJOBSECTIONS[sectionname]['multiple_allowed']
                and len(self.sections[sectionname]) > 1):
                # raising exception because this shouldn't be possible using class methods
                raise ValueError('Job can only have one {} section'.format(sectionname))
            
            for section in self.sections[sectionname]:
                if not section.isSpecified():
                    return False
        
        return True
        
    def makeAscii(self,fix_delim_bug=True):
        """ Generates ASCII string representation of jobfile """
        asciistring = ''
        for sectionname in self.sections:
            for section in self.sections[sectionname]:
                if fix_delim_bug:
                    section.fixDelimBug()
                asciistring += section.makeAscii() + '\n\n'
        
        return asciistring[:-2]     # strip off final newlines
    
    def readAscii(self,asciistring):
        """ Reads an ASCII string representation of a jobfile section """

        # Matches all section blocks in the string
        mm = re.findall(r'START_SECTION (\S*)\n(.*?)\nEND_SECTION',asciistring,re.DOTALL)
        for m in mm:
            sectionname = m[0]
            sectionbody = m[1]
            newsection = asmlSection(sectionname)
            newsection.readAscii(sectionbody)

            self.append(newsection)

    def readAsciiJobfile(self,filename):
        """ Loads and parses ASCII jobfile """
        with open(filename,'r') as f:
            asciistring = f.read()
        
        self.readAscii(asciistring)
    
    def writeAsciiJobfile(self,filename):
        """ Generates and saves ASCII jobfile """
        asciistring = self.makeAscii()

        with open(filename,'w') as f:
            f.write(asciistring)

    def printSummary(self):
        """ Print summary information on the jobfile

        Summary values could include:
            - number of images
            - number of instances
            - number of layers
            - number of image placements per layer
            - max. number of placements of each image
            - etc. 
        """
        print('Not yet implemented')
