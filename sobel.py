#!/usr/bin/python3 

from PIL import Image
import numpy

def gamma_correction(c_linear):
    c_srgb = 12.92 * c_linear 
    if c_linear > 0.0031308:
        c_srgb = 1.055 * (c_linear ** (1/2.4))
    return c_srgb

def convert_to_grayscale(image):
    width, height = image.size
    pixels = image.load()
    matrix = numpy.empty((height,width),numpy.float64)
    for x in range(height):
        for y in range(width):
            r,g,b = pixels[x,y]
            c_linear = 0.2126 * (r/255) + 0.7152 * (g/255) + 0.0722 * (b/255)
            matrix[y,x] = gamma_correction(c_linear)
    return matrix

def gaussian_blur(matrix):
    gauss = (1.0/57) * numpy.array(
        [[0, 1, 2, 1, 0],
        [1, 3, 5, 3, 1],
        [2, 5, 9, 5, 2],
        [1, 3, 5, 3, 1],
        [0, 1, 2, 1, 0]])
    height, width = matrix.shape
    
    for i in numpy.arange(2, height - 2):
        for j in numpy.arange(2, width - 2):
            total = 0
            for k in numpy.arange(-2,3):
                for l in numpy.arange(-2,3):
                    val = matrix[i+k][j+l]
                    pos = gauss[2+k, 2+l]
                    total += (pos * val)
            matrix[i][j] = total
def main():
    original_image = Image.open("samples/blocks_color.jpg")
    pixel_matrix = convert_to_grayscale(original_image)
    gaussian_blur(pixel_matrix)
    im = Image.fromarray(numpy.uint8(pixel_matrix * 255),'L')
    im.show()
    original_image.show()
    im.close()
    original_image.close()

if __name__ == '__main__':
    main()
