from PIL import Image
import sys
import numpy as np
import glob
import os


def read_img(file_path):
    origin = Image.open(file_path)
    width, height = origin.size
    return origin, width, height
def gammabrighten(origin, width, height):
    brighten_img = Image.new('RGB', (width, height), 'white')
    print("gammabrighten")
    print('width, height:', width, height)
    for nX in range(0, width):
        for nY in range(0,height):
#             print(nX, nY)
            nV = np.array(origin.getpixel((nX, nY)))
            after = (((nV/255)**0.5) * 255).astype(int)
            brighten_img.putpixel((nX, nY), tuple(after))
    return brighten_img
def removenoise(brighten_img, width, height):
    rem_img = Image.new('RGB', (width, height), 'white')
    print("removenoise")
    for nX in range(1, width-1):
        for nY in range(1, height -1):
#             print(nX, nY)
            local_region = np.zeros((9, 3), dtype=np.int)
            count = 0
            for nX_O in range(-1, 2):
                for nY_O in range(-1, 2):
                    local_region[count][0] = brighten_img.getpixel((nX+nX_O, nY+nY_O))[0]
                    local_region[count][1] = brighten_img.getpixel((nX+nX_O, nY+nY_O))[1]
                    local_region[count][2] = brighten_img.getpixel((nX+nX_O, nY+nY_O))[2]
                    count += 1
            median = np.median(local_region, axis=0).astype(int)
            final_color = []
            for i in range(3):
                final_color.append(median[i])
            rem_img.putpixel((nX, nY), tuple(final_color))
    return rem_img
def sharpen(brighten_img, width, height, output):
    final_img = Image.new('RGB', (width, height), 'white')
    print('width, height:', width, height)
    print("sharpen")
    for nX in range(1, width-1):
        for nY in range(1, height - 1):
#             print(nX, nY)
            nsum = np.zeros((3,), dtype=np.int)
            for nX_O in range(-1, 2):
                for nY_O in range(-1, 2):
                    nR = brighten_img.getpixel((nX+nX_O, nY+nY_O))[0]
                    nG = brighten_img.getpixel((nX+nX_O, nY+nY_O))[1]
                    nB = brighten_img.getpixel((nX+nX_O, nY+nY_O))[2]
                    nsum[0] += ((-1)*nR)
                    nsum[1] += ((-1)*nG)
                    nsum[2] += ((-1)*nB)
                    if nX_O == 0 and nY_O == 0:
                        nsum[0] += (10*nR)
                        nsum[1] += (10*nG)
                        nsum[2] += (10*nB)
            final_color = []
            for i in range(3):
                final_color.append(nsum[i])
            final_img.putpixel((nX, nY), tuple(final_color))
    final_img.save(output)
    
if __name__ == '__main__':
    #Variables
    input_image_path =  './water_in'
    output_path = './water_out'
    input_path = glob.glob(os.path.join(input_image_path, '*.jpg'))
    
    for filename in input_path:
        input_filename = filename
        print(input_filename)
        output_filename = os.path.basename(filename)
        origin, width, height = read_img(input_filename)
        print(origin,width,height)
        #gammabrighten(origin, width,height)
        brighten_img = gammabrighten(origin, width, height)
        remove_1 = removenoise(brighten_img, width, height)
        remove_2 = removenoise(remove_1, width, height)
        remove_3 = removenoise(remove_2, width, height)
        output= os.path.join(output_path , output_filename)
        sharpen(remove_3, width, height,output)
