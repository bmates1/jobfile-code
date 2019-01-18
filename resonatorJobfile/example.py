import resonatorDistribution
import numpy as np
import sys
sys.path.insert(0, './asml_ascii')
from asml_ascii import asmlAscii, asmlCells, asmlSection, asmlSectionList

rd = resonatorDistribution.resonatorDistribution(nres=4)
rd.setImages('BAND04','band04.gds','slider3.gds')

rd.distributeFrequencies(np.arange(4300,4304,1.0)*1e6)
rd.distributePositions(0.0,0.0,0.0,1100.0,500.0)
rd.setModelForAll('wigglemodel1',e=0.0,w=21,s=3,Z1=50.0,Cc=4.778e-15,Lc=120e-12)

rd.resonators[3].__dict__
rd.calculateShifts()
rd.resonators[3].__dict__

aa = asmlAscii()
asl = rd.makeImageDefinitionSectionList('retsetrep.txt')
aa.append(asl)
asl = rd.makeImageDistributionSectionList(cx=0,cy=0)
aa.append(asl)
asl = rd.makeInstanceDefinitionSectionList()
aa.append(asl)
asl = rd.makeReticleDataSectionList('retsetrep.txt')
aa.append(asl)
with open('tmp.txt','w') as f:
    aa.writer(f)

jobfile = rd.makeChipJobfile(reticlesetreportfilename='retsetrep.txt',cx=0,cy=0)
with open('tmp2.txt','w') as f:
    jobfile.writer(f)