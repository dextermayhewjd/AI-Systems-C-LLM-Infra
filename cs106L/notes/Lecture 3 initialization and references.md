# initialization and references
## 初始化 initialization
### Direct initialization 直接初始化 = 或者（）

```c++
#include <iostream> 
int main() { 
	int numOne = 12.0; 
	int numTwo(12.0);  c++ 并不在意12是不是int
	
	std::cout << "numOne is: " << numOne << std::endl; 
	std::cout << "numTwo is: " << numTwo << std::endl; 
	
	return 0; 
}
```

### 问题很明显 不检查type
```c++
void checkCool() 
{ 
	if (temperature > 100.0) 
	{ 
		std::cout << "Emergency cooling activated!" << std::endl; 
	} else { 
		std::cout << "Temperature normal. No emergency cooling required."; 
	} 
} 
int main() 
{ 
int criticalTemperature(100.8); 
Reactor reactor(criticalTemperature); 

//等于使用 = 
Reactor reactor = criticalTemperature

reactor.checkCool(); return 0; 
}

```

## Uniform initialization 直接使用{}
```c++
#include <iostream> 
int main() { 
	int numOne {12.0};  c++ 这里会报错
	float numTwo(12.0);  
	
	std::cout << "numOne is: " << numOne << std::endl; 
	std::cout << "numTwo is: " << numTwo << std::endl; 
	
	return 0; 
}
```

1. uniform initialization 是安全的
2. 无处不在的 所有type 都能用
   vectors, maps, and custom classes, among other things

### Uniform initialization (Map)
```c++
#include <iostream>
#include <map>
int main() { 
	// Uniform initialization of a map 
	std::map<std::string,int> ages{
	 {"Alice" , 25},
	 {"Bob" , 30},
	 {"Charlie" , 35} 
	 }; 
 // Accessing map elements 
		std::cout << "Alice's age: " << ages["Alice"] << std::endl; 
		std::cout << "Bob's age: " << ages.at("Bob") << std::endl;
	 return 0; 
 }
```

```c++
#include 
#include 
int main() {
 // Uniform initialization of a vector 
 std::vector<int> numbers{1, 2, 3, 4, 5}; 
 // Accessing vector elements 
 for (int num : numbers) 
 { 
	 std::cout << num << " "; 
 } 
 std::cout << std::endl; 
 return 0; }
```

## 2️⃣ uniform initialization（统一初始化）——这是“设计理念”

**uniform initialization 不是语法名词**，而是 C++11 提出来的一个 **愿景**：
> “以后能不能都用 `{}` 初始化一切？”
目标是干掉这种混乱👇：
```c++
int a = 1; 
int b(1); 
int c = {1};
int d{1};
```

### 设计目标（理想）

- 一个初始化语法：`{}`
- 不再区分：
    - 聚合初始化
    - 构造函数初始化
    - 基本类型初始化
- 减少歧义和隐式转换

> **list initialization**  
> 👉 语言里真实存在的 `{}` 初始化规则
> **uniform initialization**  
> 👉 C++11 的“野心”，但最终只算半成功

### list initialization 的核心规则（非常重要）

#### ✅ 1. 禁止窄化转换（narrowing）
```c++
int a{3.14};    
// ❌ 编译错误 int b = 3.14;  // ✅（但危险）
```

#### ✅ 2. 优先匹配 `std::initializer_list`

```c++
std::vector<int> v1(10, 1); // 10 个 1 
std::vector<int> v2{10, 1}; // 两个元素：10 和 1
```

| 写法             | 属于什么                  | 特点                   |
| -------------- | --------------------- | -------------------- |
| `int x = 1;`   | copy initialization   | 允许隐式转换               |
| `int x(1);`    | direct initialization | 构造函数优先               |
| `int x{1};`    | list initialization   | 禁止窄化                 |
| `T t = {args}` | copy-list-init        | 会触发 initializer_list |
| `T t{args}`    | direct-list-init      | 更“直接”                |

> **`T x{};` 是 direct-list-initialization（更“直接”）**  
> **`T x = {};` 是 copy-list-initialization（多一道拷贝/匹配规则）**

在 **90% 情况下结果一样**，但在 **构造函数选择、explicit、initializer_list** 上会出现差异。

## structured Binding 像是python的拆包

```c++

std::tuple<std::string, std::string, std::string> getClassInfo() 
{ std::string className = "CS106L"; 
std::string buildingName = "Thornton 110"; 
std::string language = "C++"; 
return {className, buildingName, language}; 
}

int main() {
auto classInfo = getClassInfo();

std::string className    = std::get<0>(classInfo);
std::string buildingName = std::get<1>(classInfo);
std::string language     = std::get<2>(classInfo);

拆包python写法
auto [className, buildingName, language] = getClassInfo();

}
```

## References
```c++
int num = 5; 
int& ref = num; 
ref = 10; 
// Assigning a new value through the reference 
std::cout << num << std::endl; 
// Output: 10
```

- num is a variable of type int, that is assigned to have the value 5
- ref is a variable of type int&, that is an alias to num
- So when we assign 10 to ref, we also change the value of num, since ref is an alias for num

## pass by reference 传一个引用 alias 
```c++
#include <iostream>
#include <math.h>
// note the ampersand! 
void squareN(int& n) 
{ 
// calculates n to the power of 2 
n = std::pow(n, 2); 
} 

int main() 
{
 int num = 5; 
 squareN(num); 
 std::cout << num << std::endl; 
 return 0; 
}
```
Hey take in the actual piece of memory, don’t make a copy!
## Pass by Value 只是传一个copy

## classic reference-copy bug
```c++
#include <iostream>
#include <math.h>
#include <vector>
void shift(std::vector<std::pair<int, int>> &nums) 
{ 

We’re not modifying nums in this function
auto& 改下面才行
	for (auto [num1, num2] : nums) 
	{ 
		num1++; num2++; 
	} 
}
```
下面这样子也行
```c++
#include <iostream>
#include <math.h>
#include <vector>
void shift(std::vector<std::pair<int, int>> &nums) 
{ 
for (size_t i = 0; i < nums.size(); i++) 
	{ 
		nums[i].first++; nums[i].second++; 
	}
}
```

简单来说就是引用不会自动传递

# l-values and r-values 左值和右值
**左值 = 有“身份”的东西（有地址、能被引用）**  
**右值 = 只有“值”的东西（临时的、用完就没）**

### ✅ 左值（lvalue）

> **能被“指代”的对象**  
> 换句话说：**你能拿到它的地址**

特点：

- 有**稳定的内存地址**
- 可以被 `&` 取地址
- 可以多次使用、反复出现
- 可以出现在赋值号左边 **也可以右边**
例子：
```c++
int x = 10;
```
- `x` 是 **左值**
- 因为：
    ```c++
    &x;   // 合法
    ```
---

### ✅ 右值（rvalue）

> **只是一个“值”，没有身份**  
> **用完就没**

特点：
- 没有稳定地址
- 通常是临时对象 / 计算结果
- 不能被取地址
- 不能单独赋值
例子：
```c++
10 
x + 1 
std::string("hello")
```

## 右值引用（&&）

`int&& r = 10;   // ✅
说明什么？
> C++ 区分：
> - 左值引用 `T&`
> - 右值引用 `T&&`

```c++
#include <iostream>
#include <math.h>
// note the ampersand!
void squareN(int& n) 
{
	// calculates n to the power of 2
	n = std::pow(n, 2);
}
int main() 
{
	int num = 5;
	squareN(num);
	std::cout << num << std::endl;
	return 0;
}
```

int& n 是左值
1. num是paased by reference的
2. 不能传递右值的reference

# const 
A qualifier for objects that declares they cannot be modified
```c++
#include <iostream>
#include <vector>
int main()
{

std::vector<int> vec{ 1, 2, 3 }; /// a normal vector
const std::vector<int> const_vec{ 1, 2, 3 }; /// a const vector
std::vector<int>& ref_vec{ vec }; /// a reference to 'vec'
const std::vector<int>& const_ref{ vec }; /// a const reference

vec.push_back(3); /// this is ok!
const_vec.push_back(3); /// no, this is const!
ref_vec.push_back(3); /// this is ok, just a reference!
const_ref.push_back(3); /// this is const, compiler error!

return 0;
}
```

### You can’t declare a non-const reference to a const variable
不能声明 非const 的引用 的时候 使用const 变量 
```c++
#include <iostream>
#include <vector>
int main()
{
	/// a const vector
	const std::vector<int> const_vec{ 1, 2, 3 };
	std::vector<int>& bad_ref{ const_vec }; /// BAD 这个不可以
	const std::vector& good_ref{ const_vec }; /// Yay! 这个可以
	return 0;
}
```

## compile

```bash
g++ -std=c++23 main.cpp -o main

-o 代表要给executable一个特别的名字
This means that you’re going to give a specific name to your executable
main是这个名字

g++ -std=c++23 main.cpp
This is also valid, your executable will be something like a.out

./main 运行代码
```