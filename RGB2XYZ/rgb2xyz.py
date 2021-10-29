import numpy as np  

# NTSC / reference white point C
RGB2XYZ_601 = np.matrix([[0.6068909, 0.1735011, 0.2003480],
                            [0.2989164, 0.5865990, 0.1144845],
                            [0.0000000, 0.0660957, 1.1162243]])

# PAL/SECAM / reference white point D65
RGB2XYZ_PAL = np.matrix([[0.4306190, 0.3415419, 0.1783091],
                            [0.2220379, 0.7066384, 0.0713236],
                            [0.0201853, 0.1295504, 0.9390944]])

# reference white point ~6300K
RGB2XYZ_DCIP3 = np.matrix([[0.4866, 0.2657, 0.1982],
                                [0.2290, 0.6917, 0.0793],
                                [0, 0.0451, 1.0439]])

# sRGB / reference white point D50
RGB2XYZ_sRGB_D50 = np.matrix([[0.4360747, 0.3850649, 0.1430804],
                            [0.2225045, 0.7168786, 0.0606169],
                            [0.0139322, 0.0971045, 0.7141733]])

# Apple Display P3 / D65
RGB2XYZ_DisplayP3 = np.matrix([[0.51512, 0.29198, 0.1571],
                                [0.2412, 0.69225, 0.06657],
                                [-0.00105, 0.04189, 0.78407]])

# sRGB or Rec.709 / reference white point D65
RGB2XYZ_709 = np.matrix([[0.4124564, 0.3575761, 0.1804375],
                        [0.2126729, 0.7151522, 0.0721750],
                        [0.0193339, 0.1191920, 0.9503041]])

# AdobeRGB D65
RGB2XYZ_AdobeRGB_D65 = np.matrix([[0.5767309, 0.1855540, 0.1881852],
                                [0.2973769, 0.6273491, 0.0752741],
                                [0.0270343, 0.0706872, 0.9911085]])

def convension_matrix():
    matrix = {'AdobeRGB_D65': RGB2XYZ_AdobeRGB_D65, 'DisplayP3': RGB2XYZ_DisplayP3, 'sRGB_D65': RGB2XYZ_709, \
                '709': RGB2XYZ_709, 'sRGB_D50': RGB2XYZ_sRGB_D50, 'DCIP3': RGB2XYZ_DCIP3, 'PAL': RGB2XYZ_PAL,\
                'NTSC': RGB2XYZ_601, '601_C': RGB2XYZ_601}
    return matrix
