# -*- coding: utf-8 -*-

"""
@author: hiltong
Created Dec, 2013 by Gene Hilton
Edited Jan, 2019 by Ben Mates

Specification for ASML jobfiles
"""

from collections import OrderedDict

ASMLELEMENTINDENT = 3       # Indentation of element lines in ASCII jobfile
ASMLELEMENTALIGN = 49       # Alignment position of element values in ASCII jobfile

# # Discovered limitations on ASML jobfiles
# ASMLMAXIMAGECOUNT = 50
# ASMLMAXLAYERCOUNT = 60
# ASMLMAXRETICLEDATACOUNT = 80 # this one is not really clear
# more...

"""
Section fields:
    is_optional         : Section is not required for a valid jobfile
    multiple_allowed    : Multiple instances of the section are allowed in the jobfile
    id_element          : List of elements that uniquely identify the section instance
    elements            : Parameters specified in the jobfile section

Element fields:
    count               : Number of variables to specify for element
    element_type        : Field type [int, float, string, multiline]
    is_optional         : Element is not required in the section
    default             : Default value for element
    validator           : Specification of valid range or list
    defined_in          : Other section where list of valid values is defined
"""
ASMLJOBSECTIONS = OrderedDict([
    ('GENERAL',{
        'is_optional':False,
        'multiple_allowed':False,
        'id_elements':[],
        'elements':OrderedDict([
            ('COMMENT',{'count':3,'element_type':'multiline','is_optional':True,
                'default':None,'validator':None }),
            ('MACHINE_TYPE',{'count':1,'element_type':'string','is_optional':True,
                'default':['PAS5500/100',],'validator':['list', 'PAS5500/80', 'PAS5500/100', 'PAS5500/275'] }),
            ('RETICLE_SIZE',{'count':1,'element_type':'int','is_optional':True,
                'default':[6,],'validator':['list', 5, 6] }),
            ('WFR_DIAMETER',{'count':1,'element_type':'float','is_optional':True,
                'default':[150.0,],'validator':['list', 76.2, 100.0, 125.0, 150.0, 200.0] }),    # Why not default to 76.2?
            ('WFR_NOTCH',{'count':1,'element_type':'string','is_optional':True,
                'default':['N',],'validator':['list', 'Y', 'N'] }),
            ('CELL_SIZE',{'count':2,'element_type':'float','is_optional':False,
                'default':[10.0,10.0],'validator':None }),
            ('ROUND_EDGE_CLEARANCE',{'count':1,'element_type':'float','is_optional':True,
                'default':[2.0,],'validator':['range', 0.0, 20.0] }),
            ('FLAT_EDGE_CLEARANCE',{'count':1,'element_type':'float','is_optional':True,
                'default':[2.0,],'validator':['range', 0.0, 20.0] }),
            ('EDGE_EXCLUSION',{'count':1,'element_type':'float','is_optional':True,
                'default':[3.0,],'validator':['range', 0.0, 5.0] }),
            ('COVER_MODE',{'count':1,'element_type':'string','is_optional':True,
                'default':['I'],'validator':['list', 'W', 'I'] }),
            ('NUMBER_DIES',{'count':2,'element_type':'int','is_optional':True,
                'default':[1,1],'validator':None }),
            ('MIN_NUMBER_DIES',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('PLACEMENT_MODE',{'count':1,'element_type':'string','is_optional':True,
                'default':['O',],'validator':['list', 'O', 'C'] }),
            ('MATRIX_SHIFT',{'count':2,'element_type':'float','is_optional':True,
                'default':[0.0,0.0],'validator':None }),
            ('PREALIGN_METHOD',{'count':1,'element_type':'string','is_optional':True,
                'default':['STANDARD',],'validator':None }),
            ('WAFER_ROTATION',{'count':1,'element_type':'float','is_optional':True,
                'default':[0.0,],'validator':['range', -360.0, 360.0] }),
            ('COMBINE_ZERO_FIRST',{'count':1,'element_type':'string','is_optional':True,
                'default':['N',],'validator':['list', 'Y', 'N'] }),
            ('MARK_CLEAR_OUT',{'count':1,'element_type':'string','is_optional':True,
                'default':['N',],'validator':['list', 'Y', 'N'] }),
            ('MATCHING_SET_ID',{'count':1,'element_type':'string','is_optional':True,
                'default':['DEFAULT',],'validator':None })
        ])
    }),
    ('ALIGNMENT_MARK',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['MARK_ID'],
        'elements':OrderedDict([
            ('MARK_ID',{'count':1,'element_type':'string','is_optional':False,
                'default':None,'validator':None }),
            ('IMAGE_ID',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('MARK_EDGE_CLEARANCE',{'count':1,'element_type':'string','is_optional':True,
                'default':['L',],'validator':['list', 'L', 'S'] }),
            ('WAFER_SIDE',{'count':1,'element_type':'string','is_optional':True,
                'default':['A',],'validator':['list', 'A', 'B'] }),
            ('MARK_LOCATION',{'count':2,'element_type':'float','is_optional':False,
                'default':None,'validator':None })
        ])
    }),
    ('WFR_ALIGN_STRATEGY',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['STRATEGY_ID'],
        'elements':OrderedDict([
            ('STRATEGY_ID',{'count':1,'element_type':'string','is_optional':False,
                'default':None,'validator':None }),
            ('WAFER_ALIGNMENT_METHOD',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':['list', 'O', 'T', 'N'] }),
            ('NR_OF_MARKS_TO_USE',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':['range', 2, 200] }),
            ('NR_OF_X_MARKS_TO_USE',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':['range', 2, 200] }),
            ('NR_OF_Y_MARKS_TO_USE',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':['range', 2, 200] }),
            ('MIN_MARK_DISTANCE_COARSE',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':['range', 0.1, 200.0] }),
            ('MIN_MARK_DISTANCE',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':['range', 0, 100] }),
            ('MAX_80_88_MARK_SHIFT',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':['range', 0.0, 0.5] }),
            ('MAX_MARK_RESIDUE',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':['range', 0.0, 4000.0] }),
            ('SPM_MARK_SCAN',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':['list', 'S', 'F'] }),
            ('CORR_WAFER_GRID',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('ERR_DETECTION_88_8',{'count':1,'element_type':'string','is_optional':True,
                'default':'M','validator':['list', 'M', 'E', 'D'] }),
            ('GRID_OPTIMISATION_ALGORITHM',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':['list', 'N', 'F'] }),
            ('FLYER_REMOVAL_THRESHOLD',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':['range', 0.0, 10.0] }),
            ('ALIGNMENT_MONITORING',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':['list', 'N', 'O', 'A', 'D'] })
        ])
    }),
    ('MARK_ALIGNMENT',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['MARK_ID'],
        'elements':OrderedDict([
            ('STRATEGY_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'WFR_ALIGN_STRATEGY',
                'default':None,'validator':None }),
            ('MARK_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'ALIGNMENT_MARK',
                'default':None,'validator':None }),
            ('GLBL_MARK_USAGE',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':['list', 'E', 'A', 'C', 'F', 'N'] }),
            ('MARK_PREFERENCE',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':['list', 'P', 'B'] })
        ])
    }),
    ('IMAGE_DEFINITION',{
        'is_optional':False,
        'multiple_allowed':True,
        'id_elements':['IMAGE_ID'],
        'elements':OrderedDict([
            ('IMAGE_ID',{'count':1,'element_type':'string','is_optional':False,
                'default':['NONAME',],'validator':None }),
            ('RETICLE_ID',{'count':1,'element_type':'string','is_optional':True,
                'default':['NONAME',],'validator':None }),
            ('IMAGE_SIZE',{'count':2,'element_type':'float','is_optional':False,
                'default':None,'validator':None }),
            ('IMAGE_SHIFT',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('MASK_SIZE',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('MASK_SHIFT',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('BASE_IMAGE_ID',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('VARIANT_ID',{'count':1,'element_type':'string','is_optional':True,
                'default':["",],'validator':None })
        ])
    }),
    ('INSTANCE_DEFINITION',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['INSTANCE_ID'],
        'elements':OrderedDict([
            ('INSTANCE_ID',{'count':1,'element_type':'string','is_optional':False,
                'default':None,'validator':None,'fix_delim_bug':True })
        ])
    }),
    ('IMAGE_DISTRIBUTION',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['IMAGE_ID','INSTANCE_ID','CELL_SELECTION'],
        'elements':OrderedDict([
            ('IMAGE_ID',{'count':1,'element_type':'string','is_optional':False,
                'default':None,'validator':None }),
            ('INSTANCE_ID',{'count':1,'element_type':'string','is_optional':False,  # Was optional
                'default':'<Default>','validator':None, 'fix_delim_bug':True }),
            ('CELL_SELECTION',{'count':2,'element_type':'string','is_optional':False,
                'default':None,'validator':None }),
            ('DISTRIBUTION_ACTION',{'count':1,'element_type':'string','is_optional':False,
                'default':['I',],'validator':['list', 'I', 'S', 'D'] }),
            ('OPTIMIZE_ROUTE',{'count':1,'element_type':'string','is_optional':True,
                'default':['N',],'validator':None }),                                            # Check validator
            ('IMAGE_CELL_SHIFT',{'count':2,'element_type':'float','is_optional':False,
                'default':[0.0, 0.0],'validator':None })
        ])
    }),
    ('LAYER_DEFINITION',{
        'is_optional':False,
        'multiple_allowed':True,
        'id_elements':['LAYER_NO'],  # This was LAYER_ID, but I don't like an optional id_element
        'elements':OrderedDict([
            ('LAYER_NO',{'count':1,'element_type':'int','is_optional':False,
                'default':None,'validator':None }),
            ('LAYER_ID',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('WAFER_SIDE',{'count':1,'element_type':'string','is_optional':True,
                'default':['A',],'validator':['list', 'A', 'B'] })
        ])
    }),
    ('MARKS_SELECTION',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['LAYER_ID','MARK_ID'],
        'elements':OrderedDict([
            ('LAYER_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'LAYER_DEFINITION',
                'default':None,'validator':None }),
            ('MARK_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'ALIGNMENT_MARK',
                'default':None,'validator':None }),
            ('GLBL_MARK_USAGE',{'count':1,'element_type':'string','is_optional':True,   # What values can this take?
                'default':None,'validator':None })
        ])
    }),
    ('STRATEGY_SELECTION',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['LAYER_ID'],
        'elements':OrderedDict([
            ('LAYER_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'LAYER_DEFINITION',
                'default':None,'validator':None }),
            ('STRATEGY_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'WFR_ALIGN_STRATEGY',
                'default':None,'validator':None }),
            ('STRATEGY_USAGE',{'count':1,'element_type':'string','is_optional':False,
                'default':None,'validator':['list', 'A', 'E'] })
        ])
    }),
    ('PROCESS_DATA',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['LAYER_ID'],
        'elements':OrderedDict([
            ('LAYER_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'LAYER_DEFINITION',
                'default':None,'validator':None }),
            ('LENS_REDUCTION',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('CALIBRATION',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('OPTICAL_PREALIGNMENT',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('OPT_PREALIGN_MARKS',{'count':2,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('GLBL_WFR_ALIGNMENT',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('COO_REDUCTION',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('MIN_NUMBER_PULSES_IN_SLIT',{'count':1,'element_type':'string','is_optional':True, # Should this be a string?
                'default':None,'validator':None }),
            ('MIN_NUMBER_PULSES',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('SKIP_COARSE_WAFER_ALIGN',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('REDUCE_RETICLE_ALIGN',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('REDUCE_RA_DRIFT',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('REDUCE_RA_INTERVAL',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('RET_COOL_CORR',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('RET_COOL_TIME',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('RET_COOL_START_ON_LOAD',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('RET_COOL_USAGE',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('GLBL_RTCL_ALIGNMENT',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('GLBL_OVERLAY_ENHANCEMENT',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('GLBL_SYM_ALIGNMENT',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('LAYER_SHIFT',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_WAFER_GRID',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('NR_OF_MARKS_TO_USE',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('MIN_MARK_DISTANCE_COARSE',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('MIN_MARK_DISTANCE',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('MAX_80_88_SHIFT',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('MAX_MARK_RESIDUE',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('SPM_MARK_SCAN',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('ERR_DETECTION_88_8',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_INTER_FLD_EXPANSION',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_INTER_FLD_NONORTHO',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_INTER_FLD_ROTATION',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_INTER_FLD_TRANSLATION',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_INTRA_FLD_MAGNIFICATION',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_INTRA_FLD_ROTATION',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_INTRA_FLD_TRANSLATION',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_INTRA_FLD_ASYM_ROTATION',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_INTRA_FLD_ASYM_MAGN',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_PREALIGN_ROTATION',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_PREALIGN_TRANSLATION',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('CORR_80_88_MARK_SHIFT',{'count':4,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            # corr_rowbar_cpe_file
            ('CORR_LENS_HEATING',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('NUMERICAL_APERTURE',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('SIGMA_INNER',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('SIGMA_OUTER',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            # blade_id
            # quadrupole_id
            ('RTCL_CHECK_SURFACES',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('RTCL_CHECK_LIMITS_UPPER',{'count':3,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('RTCL_CHECK_LIMITS_LOWER',{'count':3,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('ALIGNMENT_METHOD',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('REALIGNMENT_METHOD',{'count':1,'element_type':'string','is_optional':False,
                'default':None,'validator':None }),
            # realignment_interval
            ('IMAGE_ORDER_OPTIMISATION',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('RETICLE_ALIGNMENT',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('USE_DEFAULT_RETICLE_ALIGNMENT_METHOD',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('CRITICAL_PERCENTAGE',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('SHARE_LEVEL_INFO',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('FOCUS_EDGE_CLEARANCE',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('INLINE_Q_ABOVE_P_CALIBRATION',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('SHIFTED_MEASUREMENT_SCANS',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('FOCUS_MONITORING',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            # [-FOCUS_ERR_MAX-]
            # [-FOCUS_USE_Z_DIES-]
            # [-FOCUS_MINIMAL_DIE_AREA-]
            # [-FOCUS_EDGE_EXCLUSION-]
            # [-FOCUS_FIT_ORDER-]
            # [-FOCUS_STATISTICS-]
            # [-FOCUS_STATISTICS_LIMIT-]
            # [-FOCUS_Z_LIMIT-]
            # [-FOCUS_RX_LIMIT-]
            # [-FOCUS_RY_LIMIT-]
            # next one not in secs manual
            ('FOCUS_MONITORING_SCANNER',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('DYN_PERF_MONITORING',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            # [-DYN_PERF_ERR_MAX-]
            # [-DYN_PERF_MA_X_ERROR_LIMIT-]
            # [-DYN_PERF_MA_Y_ERROR_LIMIT-]
            # [-DYN_PERF_MA_Z_ERROR_LIMIT-]
            # [-DYN_PERF_MA_RZ_ERROR_LIMIT-]
            # [-DYN_PERF_MSD_X_ERROR_LIMIT-]
            # [-DYN_PERF_MSD_Y_ERROR_LIMIT-]
            # [-DYN_PERF_MSD_Z_ERROR_LIMIT-]
            # [-DYN_PERF_MSD_RZ_ERROR_LIMIT-]
            # [-USE_DEFAULT_RTCL_ALIGN_METHOD-] this or the next one manual says RTCL, jobs say reticle?????
            # [-FOCUS_MONITORING_USE_GENERIC_WEA-]
            # [-FOCUS_MONITORING_ON_EDGE-]
            # [-FOCUS_RX_ON_EDGE_LIMIT-]
            # [-FOCUS_RY_ON_EDGE_LIMIT-]
            # [-FOCUS_Z_ON_EDGE_LIMIT-]
            # [-FOCUS_STATISTICS_ON_EDGE-]
            # [-FOCUS_STATISTICS_ON_EDGE_LMT-]
            # [-FOCUS_MONITORING_SCANNER-]
            # [-FOCUS_ERR_MAX_SCANNER-]
            # [-FOCUS_EDGE_EXCLUSION_SCANNER-]
            # [-FOCUS_RX_LIMIT_SCANNER-]
            # [-FOCUS_RY_LIMIT_SCANNER-]
            # [-FOCUS_Z_LIMIT_SCANNER-]
            # [-FOCUS_STATISTICS_SCANNER-]
            # [-FOCUS_STATISTICS_LIMIT_SCANNER-]
            # [-FORCE_MEANDER-] or the next one??????
            ('FORCE_MEANDER_ENABLED',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None })
        ])
    }),
    ('RETICLE_DATA',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['LAYER_ID','IMAGE_ID'],
        'elements':OrderedDict([
            ('LAYER_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'LAYER_DEFINITION',
                'default':None,'validator':None }),
            ('IMAGE_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'IMAGE_DEFINITION',
                'default':None,'validator':None }),
            ('IMAGE_USAGE',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':['list', 'Y', 'N'] }),
            ('RETICLE_ID',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('IMAGE_SIZE',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('IMAGE_SHIFT',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('MASK_SIZE',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('MASK_SHIFT',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('ENERGY_ACTUAL',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('FOCUS_ACTUAL',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('FOCUS_TILT',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('NUMERICAL_APERTURE',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('SIGMA_INNER',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('SIGMA_OUTER',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            # quadrupole id
            ('IMAGE_EXPOSURE_ORDER',{'count':1,'element_type':'int','is_optional':True,
                'default':None,'validator':None }),
            ('LITHOGRAPHY_PROCESS',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('IMAGE_INTRA_FLD_COR_TRANS',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('IMAGE_INTRA_FLD_COR_ROT',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('IMAGE_INTRA_FLD_COR_ASYM_ROT',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('IMAGE_INTRA_FLD_COR_MAG',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('IMAGE_INTRA_FLD_COR_ASYM_MAG',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('LEVEL_METHOD_Z',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('LEVEL_METHOD_RX',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('LEVEL_METHOD_RY',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('EXTRAPOLATION_DISTANCE',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('SCAN_DIRECTION',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            # measurement_scans
            ('DIE_SIZE_DEPENDENCY',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('ENABLE_EFESE',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            # [-MINIMUM_DIE_SIZE-]
            # [-SLIT_TILT_CORRECTION-]
            ('CD_FEC_MODE',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            ('CD_FEC_OFFSET',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('DOSE_CORRECTION',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            # [-DOSE_CORRECTION_RECIPE_ID-]
            ('DOSE_CRITICAL_IMAGE',{'count':1,'element_type':'string','is_optional':True,
                'default':None,'validator':None }),
            # [-FOCUS_RANGE-]
            # are the names right below?
            ('GLOBAL_LEVEL_POINT_1',{'count':2,'element_type':'float','is_optional':False,
                'default':None,'validator':None }),
            ('GLOBAL_LEVEL_POINT_2',{'count':2,'element_type':'float','is_optional':False,
                'default':None,'validator':None }),
            ('GLOBAL_LEVEL_POINT_3',{'count':2,'element_type':'float','is_optional':False,
                'default':None,'validator':None })
        ])
    }),
    ('EXPOSURE_DATA',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['LAYER_ID','IMAGE_ID','CELL_SELECTION'],
        'elements':OrderedDict([
            ('LAYER_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'LAYER_DEFINITION',
                'default':None,'validator':None }),
            ('IMAGE_ID',{'count':1,'element_type':'string','is_optional':False,'defined_in':'IMAGE_DEFINITION',
                'default':None,'validator':None }),
            ('CELL_SELECTION',{'count':2,'element_type':'string','is_optional':False,
                'default':None,'validator':None }),
            ('ENERGY_OFFSET',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('ENERGY_REL_OFFSET',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('FOCUS_OFFSET',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('FOCUS_TILE_OFFSET',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('TRANSLATION_OFFSET',{'count':2,'element_type':'float','is_optional':True,
                'default':None,'validator':None })
        ])
    }),
    ('LEVEL_SENSOR_AREA',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['LAYER_ID','IMAGE_ID','CELL_SELECTION'],
        'elements':OrderedDict([
            ('LAYER_ID',{'count':1,'element_type':'string','is_optional':False,
                'default':None,'validator':None }),
            ('IMAGE_ID',{'count':1,'element_type':'string','is_optional':False,
                'default':None,'validator':None }),
            ('CELL_SELECTION',{'count':2,'element_type':'string','is_optional':False,
                'default':None,'validator':None }),
            ('AREA',{'count':4,'element_type':'float','is_optional':False,
                'default':None,'validator':None }),
            ('USABLE_AREA',{'count':1,'element_type':'string','is_optional':False,
                'default':None,'validator':None })
        ])
    }),
    ('FOCUS_MONITORING_WEA',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['LAYER_ID'],
        'elements':OrderedDict([
            ('LAYER_ID',{'count':1,'element_type':'string','is_optional':False,    # Both True and False in Gene's
                'default':None,'validator':None }),
            ('FOCUS_MONITORING_WEA_LL_X',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('FOCUS_MONITORING_WEA_LL_Y',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('FOCUS_MONITORING_WEA_UR_X',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None }),
            ('FOCUS_MONITORING_WEA_UR_Y',{'count':1,'element_type':'float','is_optional':True,
                'default':None,'validator':None })
        ])
    }),
    ('MEASUREMENT_POINT',{
        'is_optional':True,
        'multiple_allowed':True,
        'id_elements':['MEASUREMENT_POINT_ID','MEASUREMENT_POS'],
        'elements':OrderedDict([
            ('MEASUREMENT_POINT_ID',{'count':1,'element_type':'string','is_optional':False,
                'default':None,'validator':None }),
            ('MEASUREMENT_POS',{'count':2,'element_type':'float','is_optional':False,
                'default':None,'validator':None })
        ])
    })
])