#include <algorithm>
#include <cmath>
#include <cstddef>
#include <vector>

float eff_sigma(std::vector<float> & v)
{
        size_t n = v.size();
        if (n < 2) return 0;
        std::sort(v.begin(), v.end());
        size_t s = floor(0.68269 * n);
        float d_min = v[s] - v[0];
        float a = 0, b = 0;
        size_t ai = 0, bi = 0;
        for (size_t i = s; i < n; ++i) {
                float d = v[i] - v[i - s];
                if (d < d_min) d_min = d;
        }
        return d_min / 2.;
}


float mean(std::vector<float> & v)
{
        size_t n = v.size();
        float m = 0;
        for (size_t i = 0; i < n; ++i) {
                m += v[i];
        }
        return m / (float)n;
}


float stddev(std::vector<float> & v)
{
        size_t n = v.size();
        float mm = 0;
        for (size_t i = 0; i < n; ++i) {
                mm += v[i] * v[i];
        }
        float m = mean(v);
        return sqrt(mm / (float)n - m * m);
}
