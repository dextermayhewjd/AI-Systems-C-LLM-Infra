Special Member Functions
-  An overview
○ Copy and copy assignment
○ delete 
○ Move and move assignment

# Overview
```c++
These functions are generated only when 
they're called (and before any are explicitly defined by you): 

Default constructor: T() 
Destructor: ~T() 
Copy constructor: T(const T&) 
Copy assignment-operator: T& operator=(const T&) 
Move constructor: T(T&&) 
`Move assignment-operator`: T& operator=(T&&)
```
```c++
class Widget
{
	public:
		Widget();
		# default constructor
		创造一个新的对象但是不需要任何参数
		
		Widget(const Wideget& w);
		# copy constructor
		创造一个新的对象obejct 每个成员都copy 
		
		Widget& operator = (const Widget& w);
		# copy assignment operator
		assgin 一个已经存在的obejct给另一个
		
		~Widget();
		# destructor
		# Called when the object goes out of scope
		
		Widget(Widget&& rhs);
		Widget& operator = (Widget&& rhs);
		不是这一次的重点 
}
```

### copy constructor invoked
```c++
Widget widgetOne;
Widget widgetTwo = widgetOne; // Copy constructor is called
```
还没有默认初始化, 默认构造过的`widgetTwo`

## copy assignment operator invoked
```c++
Widget widgetOne; 
Widget widgetTwo; 

widgetOne = widgetTwo
```
注意这里两个object 都已经constructed 构造过了 在使用= 之前

# 我们不用写任何一个这个函数 他们都有默认版本




Special Member Functions
○ An overview
-   Copy and copy assignment
○ delete 
○ Move and move assignment

当我们使用
```c++
template <typename T> 
Vector<T>::Vector() 
{
_size = 0; 
_capacity = 4; 
_data = new T[_capacity]; 
}
```
这里其实有两步骤
### 第一步
`_size, _capacity, and _data`
可能被默认初始化了
## 第二步
然后给变量赋值
assignment to the variables 

采取的办法是
# Member initialization Lists
```c++
template <typename T>
Vector<T>::Vector(): _size(0), _capacity(4),_data(new T[_capacity]){}
```

## 但如果变量是一个没有办法被赋值的type呢
那么就只能initializer list了 

# 为什么要override SMF
## 比如member-wise copying

### 考虑一下pointer
如果变量是一个指针
那么memberwise copy 会指向同一个分配的数据
！！ 不是fresh copy

```c++
template<typename T> 
Vector<T>::Vector<T>(const Vector::Vector& other) :
 _size(other._size), _capacity(other._capacity), _data(other._data) { }
```
最后other._ data  会指向相同的underlying array

## deep copy 手动写一份copy
```c++
Vector<T>::Vector(const Vector<T>& other)
	:_size(toher._size),_capacity(other._capacity),_data(new T[other._capacity])
	{
		for(size)t i = 0;i<_size;i++)
		{
			_data[i] = other._data[i];
		}
	}
```


Special Member Functions
○  An overview
○Copy and copy assignment
-  delete 
○ Move and move assignment

# 如何避免拷贝

我们可以把SMFs 设置成delete 来移除他们的功能
```c++
class PasswordManger{
	public:
	PasswordManager();
	~PasswordManager();
	PasswordManager(const PasswordManager$ pm);
// other methods
	PasswordManager(const PasswordManager& rhs) = delete;
	PasswordManager$ operator = (const PasswordManager& rhs) = delete;
}
```

### 规则
1. 如果默认的 SMFs 够用 
   不要定义你自己的
2. 如果你不需要 构造 析构 或者 copy assignment
   那就别用
   但如果你的class以来 哪些SMFs那就不要去重新 reimplement

```c++
class a_string_with_an_id() 
{ 
public: 
	/// getter and setter methods for our private variables 
private: 
	int id; 
	std::string str; }
```
3. 如果你需要custom的析构
   那么你大概也需要copy constructor 和一个copy assignment operator


recap
1. Default Constructor 默认构造
	1. 没有参数地创造对象
		1. 没有成员变量被实例化
2. Copy Constructor 复制构造
	1. 被创造的对象 作为一个已经存在的对象的复制（member variable-wise）
3. Copy Assignment Operator 复制赋值 操作
	1. 现有的对象被另一个对象的复制取代
4. Destructor 析构
	1. 对象被毁灭 当它离开他的作用域

 ```c++
 vector<int> func(vector<int> vec0) {
vector<int> vec1; // // 默认初始化 → 默认构造
vector<int> vec2(3); // 直接初始化 → size 构造 
vector<int> vec3{3}; // 列表初始化 → initializer_list
vector<int> vec4();  // ⚠️ 函数声明（不是对象）
vector<int> vec5(vec2); // 拷贝初始化 → 拷贝构造
vector<int> vec6{};     //  列表初始化 → 空 initializer_list
vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
// 列表初始化 → initializer_list

vector<int> vec8 = vec2; // 拷贝初始化 → 拷贝构造
vec8 = vec2;   // 赋值 → 拷贝赋值运算符
return vec8;
}
 ```