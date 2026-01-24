#include <utility>
#include <cmath>
using Zeros = std::pair<double, double>;
using Solution = std::pair<bool, Zeros>;

Solution solveQuadratic(double a, double b, double c)
{
    // 1. 处理退化情况
    if (a == 0.0) {
        return {false, {0.0, 0.0}};
    }

    // 2. 判别式（用 double）
    double discriminant = b * b - 4 * a * c;

    if (discriminant < 0.0) {
        return {
            false,
            {
                std::numeric_limits<double>::quiet_NaN(),
                std::numeric_limits<double>::quiet_NaN()
            }
        };
    }

    // 3. 正确公式
    double sqrt_disc = std::sqrt(discriminant);
    double denom = 2 * a;

    double x1 = (-b + sqrt_disc) / denom;
    double x2 = (-b - sqrt_disc) / denom;

    return {true, {x1, x2}};
}