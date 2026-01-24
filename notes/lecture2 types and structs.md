# Notes

## compile and run

- The compiler translates the ENTIRE program,
packages it into an executable file, and then executes it
编译器翻译完整个程序然后生成一个文件然后执行

## types

```c
• int 106 
• double 71.4 
• string “Welcome to CS106L!” 
• bool true false 
• size_t 12
```

## dynamic typing vs static typing

```python
Python (Dynamic Typing)
a = 3 
b = "test" 
def foo(c): 
 d = 106 
 d = "hello world!"
```

```c++
int a = 3; 
string b = "test"; 
void foo(string c) 
{ 
 int d = 106; 
 d = "hello world!"; 
}
```

## Function Overloading

```c++
double axolotl(int x) 
{ // (1) 
 return (double) x + 3;
 // typecast: int → double 
 } 
}
double axolotl(double x) 
{ // (2) 
 return x * 3; 
}
```

## Structs

```c++
struct StanfordID 
{ 
string name; // These are called fields 
string sunet; // Each has a name and type 
int idNumber; 
}; 

StanfordID id; // Initialize struct 
id.name = "THE Stanford Tree"; // Access field with ‘.’ 
id.sunet = "theTREE"; 
id.idNumber = 0000002;
```

## uniform initialization

```c++
StanfordID id; 
id.name = "THE Stanford Tree"; 
id.sunet = "theTREE"; 
id.idNumber = 0000002;
```

## list initialization

```c++
StanfordID issueNewID() 
{ 
// Order depends on field order in struct. ‘=‘ is optional
 StanfordID id = { "THE Stanford Tree", "theTREE", 0000002 }; 
 return id; 
}
```

## std::pair

```c++
struct Order 
{ 
std::string item; 
int quantity; 
}; 

Order dozen = { "Eggs", 12 };

变成

std::pair <std::string,int> dozen { "Eggs", 12 }; 
std::string item = dozen.first; // "Eggs" 
int quantity = dozen.second;
```

# std::pair is a template

```c++
template <typename T1, typename T2>
struct pair { 
T1 first; 
T2 second; 
}; 
std::pair<std::string, int>
```

## std The C++ Standard Library

- Built-in types, functions, and more provided by C++
- You need to
- #include the relevant file
- • #include → std::string
- • #include → std::pair
- • #include → std::cout, std::endl
- • We prefix standard library names with std::
- • If we write using namespace std; we don’t have to, but this is considered bad style as it can introduce ambiguity
- • (What would happen if we defined our own string?)

## Quadratic

问题背景是使用c++ 知识解决 一元二次方程

1. std：：pair
2. using
3. auto

## using keyword

```c++
原来 
std::pair<bool,std::pair<double,double>> solveQuadratic(double a, double b, double c)
```

keyword 作为alias

```c++
using Zeros = std::pair<double, double>;
using Solution = std::pair<bool, Zeros>;
Solution solveQuadratic(double a ,double b, double c)
```

## auto

auto 会让compiler infer
但是还是static type

## cmath 数学库

常见函数一览（工程里高频）

```c++
#include <cmath>

double a = std::sqrt(9.0);        // 3
double b = std::pow(2.0, 10.0);   // 1024
double c = std::log(10.0);        // ln
double d = std::log10(100.0);     // 2
double e = std::exp(1.0);         // e
double f = std::abs(-3.14);       // 3.14
double g = std::floor(3.7);       // 3
double h = std::ceil(3.1);        // 4
double i = std::round(3.5);       // 4

```

三角函数（弧度制⚠️

```c++
#include <cmath>

double rad = M_PI / 2;   // ⚠️ 这个宏不推荐（下面解释）
double s = std::sin(rad);
double c = std::cos(rad);
double t = std::tan(rad);

```

## 返回可以直接使用 { } list initialization 

```c++
#include <utility>
#include <cmath>
using Zeros = std::pair<double, double>;
using Solution = std::pair<bool, Zeros>;
Solution solveQuadratic(double a, double b, double c)
{
// 1.处理退化情况
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
```
