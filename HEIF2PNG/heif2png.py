# 作者 远程开发者  QQ:296863766 CSDN: https://blog.csdn.net/fittec
import subprocess
import os
import io
import binascii
import whatimage
import pyheif
import traceback
from PIL import Image,ExifTags
import exifread
import numpy as np  
import cv2
import argparse
from color_space_transfer import rgb_6012DisplayP3,rgb_DisplayP32601,rgb_6012709,rgb_color_space_transfer


def decodeImage(bytesIo,save_path,name):
    try:
        fmt = whatimage.identify_image(bytesIo)
        print(fmt)
        if fmt in ['heic']:
            i = pyheif.read_heif(bytesIo)
            pi = Image.frombytes(mode=i.mode, size=i.size, data=i.data, decoder_name='raw')
            # pi.save(save_path+'/png/' + name.split('.')[0]+'.png', format="PNG")
            matrix=np.asarray(pi)
            output = rgb_6012DisplayP3(matrix)
            # output = yuv2rgb_709(matrix[:,:,0],matrix[:,:,:1],matrix[:,:,2])
            cv2.imwrite(save_path+'/png/' + name.split('.')[0]+'601adjust.png', cv2.cvtColor(output, cv2.COLOR_RGB2BGR))
            print("文件转换成功并保存到：" + save_path+'/png/')
    except:
            traceback.print_exc()

# 读取图片文件
# filename为要打开的文件路径
def readImage(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return data
    
# 遍历path指定文件夹下的所有HEIC文件并转换为PNG文件   
def convertImages(path,save_path):
    filenames=os.listdir(path)
    os.makedirs(save_path+'/png', exist_ok=True)
    for name in filenames:
        filename = path +"/"+ name         # 完成路径
        print('当前转换文件：'+filename) 
        data = readImage(filename)         # 读取图像文件
        decodeImage(data,save_path,name)   # 转换

# 开始转换
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='heif_img/IMG_3056.HEIC', help='Path to gt (Ground-Truth)')
    parser.add_argument('--png_path', type=str, default='png/IMG_3056_2.png', help='Path to restored images')
    parser.add_argument('--save_path', type=str, default='/data/disk2/longshaoyi/project/heif/png', help='Path to bicubic images')
    parser.add_argument('--input_color_space', type=str, default='DisplayP3')
    parser.add_argument('--output_color_space', type=str, default='DisplayP3')
    parser.add_argument('--describe', type=str, default='')
    args = parser.parse_args()

    image_name, ext = os.path.basename(args.input_path).split('.')
    # convertImages("heif_img", "/data/disk2/longshaoyi/project/heif")
    
    if ext in ['HEIC','HEIF','heic','heif']:
        # convert heif to png
        i = pyheif.read_heif(args.input_path)
        metadata = i.metadata
        icc_profile = i.color_profile['data']
        heif = open(args.input_path, 'rb')
        exif = exifread.process_file(heif)
        # tmp = ExifTags.TAGS
        pi = Image.frombytes(mode=i.mode, size=i.size, data=i.data, decoder_name='raw')
        pi.save(f'{args.save_path}/{image_name}_test4.png', icc_profile=icc_profile)
    else:
        raise ValueError('input image is not HEIF or HEIC file')
    # cv2.imwrite(f'{args.save_path}/{image_name}_{args.input_color_space}2{args.output_color_space}{args.describe}.png', cv2.cvtColor(output, cv2.COLOR_RGB2BGR))
    print("文件转换成功并保存到：" + args.save_path +'/png/')

if __name__=='__main__':
    main()
