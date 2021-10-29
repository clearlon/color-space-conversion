import numpy as np  
from rgb2xyz_matrix import convension_matrix


def rgb2yuv_709(Drgb,rgb_bit_depth=8, quantification=8):
    """
    input:RGB (Full range)
    output:uint8 YUV
    """
    h, w, _ = Drgb.shape
    #RGB去量化  输入为16bit PNG, 若为8bit,则 /1
    Er = ((Drgb[:,:,0] / 2 **(rgb_bit_depth - 8) - 16) / 219).flatten()
    Eg = ((Drgb[:,:,1] / 2 **(rgb_bit_depth - 8) - 16) / 219).flatten()
    Eb = ((Drgb[:,:,2] / 2 **(rgb_bit_depth - 8) - 16) / 219).flatten()
    Ergb = np.array([Er,Eg,Eb])
    #RGB2YUV
    yuv2rgb_709_matrix = np.matrix([[1., 0, 1.5747],
                                    [1., -0.1873, -0.4682],
                                    [1., 1.8556, 0]])
    rgb2yuv_709_matrix = yuv2rgb_709_matrix.I
    Eyuv = np.dot(rgb2yuv_709_matrix, Ergb)
    
    Ey = Eyuv[0,:].reshape(h,w)
    Eu = Eyuv[1,:].reshape(h,w)
    Ev = Eyuv[2,:].reshape(h,w)
    #RGB量化   量化为16bit
    Dy = np.round((219*Ey+16)*2**(quantification - 8)).clip(0,255)
    Du = np.round((219*Eu+16)*2**(quantification - 8)).clip(0,255)
    Dv = np.round((219*Ev+16)*2**(quantification - 8)).clip(0,255)
    Dyuv = np.array([Dy,Du,Dv]).astype(np.uint8)
    Dyuv = Dyuv.transpose(1,2,0)  #(c,h,w)->(h,w,c)
    return Dyuv

def rgb2yuv_601(Drgb,rgb_bit_depth=8, quantification=8):
    """
    input:Y,U,V
    output:uint8 Drgb
    """
    h, w, _ = Drgb.shape
    if np.max(Drgb) > 235:
        #RGB去量化  
        Er = (Drgb[:,:,0] / 255).flatten()
        Eg = (Drgb[:,:,1] / 255).flatten()
        Eb = (Drgb[:,:,2] / 255).flatten()
        Ergb = np.array([Er,Eg,Eb])
        #RGB2YUV
        rgb2yuv_601_matrix = np.matrix([[0.257, 0.504, 0.098],
                                        [-0.148, -0.291, 0.439],
                                        [0.439, -0.368, -0.071]])
    else:
        Er = ((Drgb[:,:,0] / 2 **(rgb_bit_depth - 8) - 16) / 219).flatten()
        Eg = ((Drgb[:,:,1] / 2 **(rgb_bit_depth - 8) - 16) / 219).flatten()
        Eb = ((Drgb[:,:,2] / 2 **(rgb_bit_depth - 8) - 16) / 219).flatten()
        Ergb = np.array([Er,Eg,Eb])
        #RGB2YUV
        rgb2yuv_601_matrix = np.matrix([[0.299, 0.587, 0.114],
                                        [-0.169, -0.331, 0.500],
                                        [0.500, -0.419, -0.081]])
    Eyuv = np.dot(rgb2yuv_601_matrix, Ergb)
    Ey = Eyuv[0,:].reshape(h,w)
    Eu = Eyuv[1,:].reshape(h,w)
    Ev = Eyuv[2,:].reshape(h,w)
    #RGB量化   
    Dy = np.round(255*Ey).clip(0,255)
    Du = np.round(255*Eu).clip(0,255)
    Dv = np.round(255*Ev).clip(0,255)
    Dyuv = np.array([Dy,Du,Dv]).astype(np.uint8)
    Dyuv = Dyuv.transpose(1,2,0)  #(c,h,w)->(h,w,c)
    return Dyuv

def rgb_E2L(Ergb, COLOR_SPACE='709'):
    Lrgb = Ergb.copy()
    Lrgb1 = Ergb.copy()
    Lrgb2 = Ergb.copy()
    if COLOR_SPACE in ['709','601']:
        Lrgb[Ergb < 0.081] = Lrgb2[Ergb < 0.081] / 4.5
        Lrgb[Ergb >= 0.081] = np.power((Lrgb1[Ergb >= 0.081] + 0.099) / 1.099, 1/0.45)
    if COLOR_SPACE in ['DisplayP3','DCIP3']:
        Lrgb[Ergb <= 0.04045] = Lrgb2[Ergb <= 0.04045] * 0.077
        Lrgb[Ergb > 0.04045] = np.power((Lrgb1[Ergb > 0.04045] * 0.9479 + 0.05214), 2.4)
    if COLOR_SPACE not in ['709','601','DisplayP3','DCIP3']:
        raise ValueError(f'unsupport the {COLOR_SPACE} color space')
    return Lrgb

def rgb_L2E(Lrgb, COLOR_SPACE='709'):
    Ergb = Lrgb.copy()
    Ergb1 = Lrgb.copy()
    Ergb2 = Lrgb.copy()
    if COLOR_SPACE in ['709','601']:
        Ergb[Lrgb < 0.018] = Ergb[Lrgb < 0.018] * 4.5
        Ergb[Lrgb >= 0.018] = np.power((Ergb1[Lrgb >= 0.018] * 1.099), 0.45) - 0.099
    if COLOR_SPACE in ['DisplayP3','DCIP3']:
        Ergb[Lrgb <= 0.0031308] = Ergb[Lrgb <= 0.0031308] / 0.77
        Ergb[Lrgb > 0.0031308] = (np.power((Ergb1[Lrgb > 0.0031308]), 1/2.4) - 0.05214) / 0.9479
    if COLOR_SPACE not in ['709','601','DisplayP3','DCIP3']:
        Ergb = np.power(Lrgb, 0.45)
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

def rgb_color_space_transfer(Drgb, input_color_space='709', output_color_space='DisplayP3', chad=False):
    '''
    input: Drgb (Full range)
    return: Drgb (0-255)
    '''
    h, w, _ = Drgb.shape
    # normalize
    Er = (Drgb[:,:,0] / 255).flatten()
    Eg = (Drgb[:,:,1] / 255).flatten()
    Eb = (Drgb[:,:,2] / 255).flatten()
    Ergb = np.array([Er,Eg,Eb])
    # EOTF
    Lrgb = rgb_E2L(Ergb, COLOR_SPACE=input_color_space)

    #color space transfer
    if input_color_space not in ['601','709','DCIP3','DisplayP3']:
        raise ValueError('input error')
    if input_color_space == '709':
        rgb2xyz = RGB2XYZ_709
    if input_color_space == '601':
        rgb2xyz = RGB2XYZ_601
    if input_color_space == 'DCIP3':
        rgb2xyz = RGB2XYZ_DCIP3
    if input_color_space == 'DisplayP3':
        rgb2xyz = RGB2XYZ_DsiplayP3

    if output_color_space == '709':
        xyz2rgb = RGB2XYZ_709
    if output_color_space == '601':
        xyz2rgb = RGB2XYZ_601
    if output_color_space == 'DCIP3':
        xyz2rgb = RGB2XYZ_DCIP3
    if output_color_space == 'DisplayP3':
        xyz2rgb = RGB2XYZ_DsiplayP3
    
    if chad:
        chad = np.matrix([[1.047882, 0.022919, -0.050201],
                            [0.029587, 0.990479, -0.017059],
                            [-0.009232, 0.015076, 0.751678]])
        print(chad.I)
        transfer_matrix = np.dot(xyz2rgb.I, chad, rgb2xyz)        
    else:           
        transfer_matrix = np.dot(xyz2rgb.I, rgb2xyz)
    Lrgb = np.dot(transfer_matrix, Lrgb)
    
    # OETF
    Lrgb = Lrgb.getA()
    Ergb = rgb_L2E(Lrgb, COLOR_SPACE=output_color_space)
    Er = Ergb[0,:].reshape(h,w)
    Eg = Ergb[1,:].reshape(h,w)
    Eb = Ergb[2,:].reshape(h,w)
    #RGB量化   
    Dr = np.round(255*Er).clip(0,255)
    Dg = np.round(255*Eg).clip(0,255)
    Db = np.round(255*Eb).clip(0,255)
    Drgb = np.array([Dr,Dg,Db]).astype(np.uint8)
    Drgb = Drgb.transpose(1,2,0)  #(c,h,w)->(h,w,c)
    return Drgb
    
