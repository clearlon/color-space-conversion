import numpy as np


class TransCharacteristics:
    """
    Transfer Characteristics for OOTF, OETF, EOTF.
    input: Ergb [0-1]
    output: Lrgb[0-1]
    """

    def __init__(self):
        super(TransCharacteristics, self).__init__()
        self.Lw = 1000
        self.Lb = 0.0005
        # HLG constant
        self.a = 0.17883277
        self.b = 1 - 4 * self.a
        self.c = 0.5 - self.a * np.log(4 * self.a)

        self.alpha = 1 # 1.0 cd/m^2 may be is equal to Lw?
        self.gamma = 1.2 + 0.42 * np.log10(self.Lw / 1000)
        self.beta = np.power(3 * (np.power(self.Lb / self.Lw, 1/self.gamma)), 1/2)

        # PQ constant
        self.m1 = 0.1593017578125
        self.m2 = 78.84375
        self.c1, self.c2, self.c3 = 0.8359375, 18.8515625, 18.6875

    def OOTF(self, x, mode='HLG'):
        if np.max(x) > 1 or np.min(x) < 0:
            raise ValueError('input range is not in [0,1')
        
        if mode == 'PQ':
            E = np.where(x > 0.0003024, 1.099 * np.power(59.5208 * x, 0.45) - 0.099, 267.84 * x)
            return 100 * np.power(E, 2.4)
        
        if mode == 'HLG':
            if x.shape == 3 and x.shape[2] == 3:
                Y = 0.2627 * x[:,:,0] + 0.6780 * x[:,:,1] + 0.0593 * x[:,:,2]
            else:
                Y = 0.2627 * x + 0.6780 * x + 0.0593 * x
            return self.alpha * np.power(Y, self.gamma - 1) * x


    def OOTFinverse(self, x, mode='HLG'):
        '''
        input: if use PQ mode, the input range need to be between [0, 10000].
        output: 
        '''
        if mode == 'PQ':
            E = np.power(F_display / 100, 1/2.4)
            return np.where(E > 0.080994816, np.power((E + 0.099) / 1.099, 1 / 0.45) / 59.5208, E / 267.84)

        if mode == 'HLG':
            pass


    def OETF(self, x, mode='HLG'):
        '''
        input: Lrgb [0-1](normalized linear RGB image)
        output: Ergb [0-1](normalized non-linear RGB image)
        mode options: '709','601','DisplayP3','HLG','PQ'
        '''
        Ergb = x.copy()
        if mode == 'HLG':
            Ergb[x <= 1/12] = np.sqrt(x[x <= 1/12] * 3)
            Ergb[x > 1/12] = self.a * np.log(x[x > 1/12] * 12 - self.b) + self.c
            # Ergb = np.where(x > 1/12, a * np.log(x * 12 - b) + c, np.sqrt(x * 3))

        if mode == 'PQ':
            Ergb = np.power((self.c1 + self.c2 * np.power(x, self.m1)) / (1 + self.c3 * np.power(x, self.m1)), self.m2)

        if mode in ['709','601']:
            Ergb[x < 0.018] = x[x < 0.018] * 4.5
            Ergb[x >= 0.018] = 1.099 * np.power(x[x >= 0.018], 0.45) - 0.099

        if mode in ['DisplayP3']:
            Ergb[x <= 0.0031308] = x[x <= 0.0031308] / 0.77
            Ergb[x > 0.0031308] = (np.power((x[x > 0.0031308]), 1/2.4) - 0.05214) / 0.9479

        if mode not in ['709','601','DisplayP3','HLG','PQ']:
            Ergb = np.power(x, 0.45)
            raise Warning('input mode is not support, default gamma coefficient is 0.45')

        return Ergb

    def EOTF(self, x, mode='HLG'):
        '''
        input: Ergb [0-1](normalized non-linear RGB image)
        output: Lrgb [0-1](normalized linear RGB image)
        '''
        Lrgb = x.copy()

        if mode == 'HLG':
            Lrgb[x <= 1/2] = np.power(x[x <= 1/2], 2) / 3
            Lrgb[x > 1/2] = (np.power(np.e, (x[x > 1/2] - self.c) / self.a) + self.b) / 12
            # Lrgb = np.where(x > 1/2, (np.power(np.e, (x - c) / a) + b) / 12, np.power(x, 2) / 3)
            
        if mode == 'PQ':
            Lrgb = np.power(np.maximum(np.power(x, 1/self.m2) - self.c1, 0) / (self.c2 - self.c3 * np.power(x, 1/self.m2)), 1/self.m1)

        if mode in ['709','601']:
            Lrgb[x < 0.081] = x[x < 0.081] / 4.5
            Lrgb[x >= 0.081] = np.power((x[x >= 0.081] + 0.099) / 1.099, 1/0.45)

        if mode in ['DisplayP3','DCIP3']:
            Lrgb[x <= 0.04045] = x[x <= 0.04045] * 0.077
            Lrgb[x > 0.04045] = np.power((x[x > 0.04045] * 0.9479 + 0.05214), 2.4)

        if mode not in ['709','601','DisplayP3','DCIP3','HLG','PQ']:
            raise ValueError(f'unsupport the {mode} color space')

        return Lrgb



