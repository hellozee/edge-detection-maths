from PIL import Image

def gamma_correction(c_linear):
    c_srgb = 12.92 * c_linear 
    if c_linear > 0.0031308:
        c_srgb = 1.055 * (c_linear ** (1/2.4))
    return c_srgb

def convert_to_grayscale(image):
    width, height = image.size
    pixels = im.load()
    for x in range(width):
        for y in range(height):
            r,g,b = pixels[x,y]
            c_linear = 0.2126 * (r/255) + 0.7152 * (g/255) + 0.0722 * (b/255)
            c_srgb = gamma_correction(c_linear)
            val = int(c_srgb * 255)
            pixels[x,y] = (val,val,val)


im = Image.open("samples/blocks_color.jpg")
original_image = Image.open("samples/blocks_color.jpg")
convert_to_grayscale(im)
im.show()
original_image.show()
