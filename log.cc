#include<iostream>
#include<vector>
#include<cmath>
#include<png++/png.hpp>
#include <eigen3/Eigen/Core>

typedef std::vector<int> vec;
typedef std::vector<vec> mat;

constexpr double pi() { return std::atan(1)*4; }

// Shamelessly copying the Krita one, thanks Dmitry
Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic>
createLoGMatrix(double radius, double coeff)
{
    int kernelSize = 4 * std::ceil(radius) + 1;
    Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic> matrix(kernelSize, kernelSize);

    const double sigma = radius/* / sqrt(2)*/;
    const double multiplicand = -1.0 / (M_PI * std::pow(sigma,4.0));
    const double exponentMultiplicand = 1 / (2 * std::pow(sigma,2.0));
    const int center = kernelSize / 2;

    for (int y = 0; y < kernelSize; y++) {
        const double yDistance = center - y;
        for (int x = 0; x < kernelSize; x++) {
            const double xDistance = center - x;
            const double distance = std::pow(xDistance,2.0) + std::pow(yDistance,2.0);
            const double normalizedDistance = exponentMultiplicand * distance;

            matrix(x, y) = multiplicand *
                (1.0 - normalizedDistance) *
                exp(-normalizedDistance);
        }
    }

    double lateral = matrix.sum() - matrix(center, center);
    matrix(center, center) = -lateral;

    double positiveSum = 0;
    double sideSum = 0;
    double quarterSum = 0;

    for (int y = 0; y < kernelSize; y++) {
        for (int x = 0; x < kernelSize; x++) {
            const double value = matrix(x, y);
            if (value > 0) {
                positiveSum += value;
            }
            if (x > center) {
                sideSum += value;
            }
            if (x > center && y > center) {
                quarterSum += value;
            }
        }
    }

    const double scale = coeff * 2.0 / positiveSum;
    matrix *= scale;
    positiveSum *= scale;
    sideSum *= scale;
    quarterSum *= scale;

    return matrix;
}

double gamma_correction(double c_linear){
    double c_srgb = 12.92 * c_linear;
    if (c_linear > 0.0031308){
        c_srgb = 1.055 * std::pow(c_linear, 1/2.4);
    }
    return c_srgb;
}

mat convert_to_grayscale(const png::image<png::rgb_pixel> &image){
    auto height = image.get_height();
    auto width = image.get_width();
    mat result(height, vec(width, 0));
    for(png::uint_32 i=0;i<height;i++){
        for(png::uint_32 j=0;j<width;j++){
            auto pixel = image.get_pixel(i,j);
            auto r = static_cast<double>(pixel.red);
            auto g = static_cast<double>(pixel.green);
            auto b = static_cast<double>(pixel.blue);
            double c_linear = 0.2126 * (r/255) + 0.7152 * (g/255) + 0.0722 * (b/255);
            result[j][i] = static_cast<unsigned char>(255*gamma_correction(c_linear));
        }
    }
    return result;
}

void save_image(const std::string &fname, const mat &matrix){
    png::image<png::gray_pixel>image(matrix.size(),matrix[0].size());
    for(size_t i=0;i<matrix.size();i++){
        for(size_t j=0;j<matrix[0].size();j++){
            image[i][j] = static_cast<unsigned char>(matrix[i][j]);
        }
    }
    image.write(fname);
}

int main(){

    png::image<png::rgb_pixel> image("./samples/blocks_color.png");
    auto pixels = convert_to_grayscale(image);
    save_image("test.png",pixels); 
    std::cout << createLoGMatrix(1.4,103) << std::endl;
    return 0;
}
