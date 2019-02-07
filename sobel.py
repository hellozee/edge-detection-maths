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
            matrix[x][y] = gamma_correction(c_linear)
    return matrix

def gaussian_blur(matrix):
    pass

def create_image(matrix,pixels):
    height, width = matrix.shape
    calc = lambda i, j : int(matrix[i][j] * 255)
    make_tuple = lambda a : (a,a,a)
    for x in range(height):
        for y in range(width):
            pixels[x,y] = make_tuple(calc(x,y))

def main():
    im = Image.open("samples/blocks_color.jpg")
    original_image = Image.open("samples/blocks_color.jpg")
    pixel_matrix = convert_to_grayscale(im)
    gaussian_blur(pixel_matrix)
    create_image(pixel_matrix,im.load())
    im.show()
    original_image.show()
    im.close()
    original_image.close()

if __name__ == '__main__':
    main()
