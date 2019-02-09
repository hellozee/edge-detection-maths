#!/usr/bin/python3 

from PIL import Image
import numpy
import math

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

def gauss_filter(matrix):
    gauss = (1.0/57) * numpy.array([
        [0, 1, 2, 1, 0],
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

def sobel_filter(matrix):
    xgradient = numpy.array([[-1, 0, 1], [-2, 0, 2],[-1, 0, 1]])
    ygradient = numpy.array([[-1, -2, -1], [0, 0, 0],[1, 2, 1]])

    height, width = matrix.shape
    resultant = numpy.empty((height,width),numpy.float64)
    
    for i in numpy.arange(1, height - 2):
        for j in numpy.arange(1, width - 2):
            xfactor = xgradient[0][0] * matrix[i-1][j-1] + xgradient[0][1] * matrix[i][j-1] + xgradient[0][2] * matrix[i+1][j-1] + \
                      xgradient[1][0] * matrix[i-1][j] + xgradient[1][1] * matrix[i][j] + xgradient[1][2] * matrix[i+1][j] + \
                      xgradient[2][0] * matrix[i-1][j+1] + xgradient[2][1] * matrix[i][j+1] + xgradient[2][2] * matrix[i+1][j+1]
            yfactor = ygradient[0][0] * matrix[i-1][j-1] + ygradient[0][1] * matrix[i][j-1] + ygradient[0][2] * matrix[i+1][j-1] + \
                      ygradient[1][0] * matrix[i-1][j] + ygradient[1][1] * matrix[i][j] + ygradient[1][2] * matrix[i+1][j] + \
                      ygradient[2][0] * matrix[i-1][j+1] + ygradient[2][1] * matrix[i][j+1] + ygradient[2][2] * matrix[i+1][j+1]
            val = math.sqrt(xfactor * xfactor + yfactor * yfactor)
            resultant[i,j] = val
    
    return resultant

def main():
    original_image = Image.open("samples/blocks_color.jpg")
    pixel_matrix = convert_to_grayscale(original_image)
    gauss_filter(pixel_matrix)
    pixel_matrix = sobel_filter(pixel_matrix)
    im = Image.fromarray(numpy.uint8(pixel_matrix * 255),'L')
    im.show()
    original_image.show()
    im.close()
    original_image.close()

if __name__ == '__main__':
    main()
