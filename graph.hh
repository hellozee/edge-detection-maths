#ifndef GRAPH_HH
#define GRAPH_HH

#include <cmath>

struct point{
    int x,y;
};

double heuristic_function(const point &p0, const point &pi, const point &pm){
    double num = std::abs((pm.y-p0.y)*pi.x - (pm.x-p0.x)*pi.y + pm.x*p0.y + p0.x * pm.y);
    double denom = std::sqrt(std::pow(pm.y - p0.y,2.0)+std::pow(pm.x-p0.x,2.0)); 
    double di = num/denom;

    double dm = std::sqrt(std::pow(pm.y-pi.y,2.0) + std::pow(pm.x-pi.x,2.0));
    return 0.5*di + 0.5*dm;
}

#endif
