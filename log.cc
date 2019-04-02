#include<iostream>
#include<vector>
#include<cmath>

typedef std::vector<int> vec;
typedef std::vector<vec> mat;

constexpr double pi() { return std::atan(1)*4; }

double log(int x, int y, double sigma){
    double f1 = (-1)/(pi() * std::pow(sigma, 4.0));
    double f2 = (-1) * (x*x + y*y)/(2 * std::pow(sigma, 2.0));
    double f3 = std::exp(f2);
    return f1 * (1 + f2) * f3;
}

int main(){
    int size = 9;
    double sigma = 1.4;
    mat log_matrix(size, vec(size,0));
    for(int i=1;i<=size;i++){
        for(int j=1;j<=size;j++){
            int x = j - (size+1)/2;
            int y = i - (size+1)/2;
            log_matrix[i-1][j-1] = 255 * log(x,y,sigma);
        }
    }

    for(int i=0;i<size;i++){
        for(int j=0;j<size;j++){
            std::cout << log_matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
