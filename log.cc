#include <image.hh>
#include <graph.hh>

int main(){
    png::image<png::rgb_pixel> image("./samples/samplei.png");
    auto pixels = convert_to_grayscale(image);
    auto pixels_log = apply_log(pixels,createLoGMatrix(2,-1));
    save_image("./result/log_applied.png",pixels_log); 
    auto pixels_sobel = apply_sobel(pixels);
    save_image("./result/sobel_applied.png", pixels_sobel);
    return 0;
}
