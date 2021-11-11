import numpy as np  
from rgb2xyz_matrix import convension_matrix


def rgb_E2L(Ergb, COLOR_SPACE='709'):
    Lrgb = Ergb.copy()
    Lrgb1 = Ergb.copy()
    Lrgb2 = Ergb.copy()
    if COLOR_SPACE == 'hlg':
        a = 0.17883277
        b = 1 - 4 * a
        c = 0.5 - a * np.log(4 * a)
        Lrgb[Ergb <= 1/2] = np.power(Lrgb2[Ergb <= 1/2], 2) / 3
        Lrgb[Ergb > 1/2] = (np.power(np.e, (Lrgb1[Ergb > 1/2] - c) / a) + b) / 12
        
    if COLOR_SPACE in ['709','601']:
        Lrgb[Ergb < 0.081] = Lrgb2[Ergb < 0.081] / 4.5
        Lrgb[Ergb >= 0.081] = np.power((Lrgb1[Ergb >= 0.081] + 0.099) / 1.099, 1/0.45)
        
    if COLOR_SPACE in ['DisplayP3','DCIP3']:
        Lrgb[Ergb <= 0.04045] = Lrgb2[Ergb <= 0.04045] * 0.077
        Lrgb[Ergb > 0.04045] = np.power((Lrgb1[Ergb > 0.04045] * 0.9479 + 0.05214), 2.4)
        
    if COLOR_SPACE not in ['709','601','DisplayP3','DCIP3','hlg']:
        raise ValueError(f'unsupport the {COLOR_SPACE} color space')
        
    return Lrgb

def rgb_L2E(Lrgb, COLOR_SPACE='709'):
    Ergb = Lrgb.copy()
    Ergb1 = Lrgb.copy()
    Ergb2 = Lrgb.copy()
    if COLOR_SPACE == 'hlg:
        a = 0.17883277
        b = 1 - 4 * a
        c = 0.5 - a * np.log(4 * a)
        Ergb[Lrgb <= 1/12] = np.sqrt(Ergb2[Lrgb <= 1/12] * 3)
        Ergb[Lrgb > 1/12] = a * np.log(Ergb1[Lrgb > 1/12] * 12 - b) + c
    
    if COLOR_SPACE in ['709','601']:
        Ergb[Lrgb < 0.018] = Ergb[Lrgb < 0.018] * 4.5
        Ergb[Lrgb >= 0.018] = 1.099 * np.power(Ergb1[Lrgb >= 0.018], 0.45) - 0.099
        
    if COLOR_SPACE in ['DisplayP3','DCIP3']:
        Ergb[Lrgb <= 0.0031308] = Ergb[Lrgb <= 0.0031308] / 0.77
        Ergb[Lrgb > 0.0031308] = (np.power((Ergb1[Lrgb > 0.0031308]), 1/2.4) - 0.05214) / 0.9479
        
    if COLOR_SPACE not in ['709','601','DisplayP3','DCIP3','hlg']:
        Ergb = np.power(Lrgb, 0.45)
        raise Warning('input color space is not support, gamma is 0.45')
        
    return Ergb

def rgb2xyz(Drgb, COLOR_SPACE='709'):
    '''
    input: Drgb (Full range)
    return: xyz
    '''
    # get conversion matrix
    matrix = convension_matrix()
    if COLOR_SPACE not in matrix.keys():
        raise ValueError(f'input COLOR_SPACE is unsupport \nplease selected in {keys}')
    rgb2xyz_matrix = matrix[COLOR_SPACE]

    h, w, _ = Drgb.shape
    # 归一化
    Er = (Drgb[:,:,0] / 255).flatten()
    Eg = (Drgb[:,:,1] / 255).flatten()
    Eb = (Drgb[:,:,2] / 255).flatten()
    Ergb = np.array([Er,Eg,Eb])
    # 线性化
    if COLOR_SPACE == 'Display P3':
        Lrgb = rgb_E2L(Ergb, COLOR_SPACE='DisplayP3')

    if COLOR_SPACE == '601':
        Lrgb = rgb_E2L(Ergb, COLOR_SPACE='601')

    if COLOR_SPACE == '709':
        Lrgb = rgb_E2L(Ergb, COLOR_SPACE='709')

    if COLOR_SPACE == 'DCIP3':
        Lrgb = rgb_E2L(Ergb, COLOR_SPACE='Display P3')                   

    return np.dot(rgb2xyz_matrix, Lrgb)

    
