# Recaps
有六个SMFs
1.  default constructor 默认构造
2. 复制构造 
```c++
Widget(const Wideget& w)

场景是
Widget widgetOne;
Widget widgetTwo = widgetOne; 
// Copy constructor is called
```
3. 复制赋值
   
```c++
Widget& operator = (const Widget& w);
# copy assignment operator
场景是
Widget widgetOne; 
Widget widgetTwo; 

widgetOne = widgetTwo
```
3. 析构
讲了

还没讲
5. 移动构造
6. 移动赋值 
# Photo class
```c++
class Photo {
public:
	Photo(int width, int height);
	Photo(const Photo& other);
	Photo& operator=(const Photo& other);
	~Photo();

private:
	int width;
	int height;
	int* data;
};
```

```c++
// Constructor  构造
Photo::Photo(int width, int height)
: width(width)
, height(height)
, data(new int[width * height])
{}
```

```c++
//SMF 复制构造
Photo& Photo::operator=(const Photo& other) {
	// Check for self assignment
	if (this == &other) return *this;
	如果相等的化
	
	先删掉老的pixels
	delete[] data; // Clean up old pixels!
	
	复制新的pixels
	// Copy over new pixels!
	width = other.width;
	height = other.height;
	data = new int[width * height];
	// 这里的copy （source_start, source_end, source）
	std::copy(other.data, other.data + width * height, data);
	return *this;
}
```

```c++
Photo::~Photo()
{
delete[] data;
}
```
# takephoto问题

```c++
Photo takePhoto();
int main() {
	Photo selfie = takePhoto(); // (A)
	Photo retake(0, 0);
	retake = takePhoto(); // (B)
}
```
The return value of a function is temporary
编译器会把这个返回值 在赋值完之后就清理掉
the compiler is going to clean this object up before moving onto the next line
```c++
Photo selfie = takePhoto(); // Copy constructor
复制 构造
``` 

# Copy和Move的语意
```c++
Photo selfie = pic; 
这里是拷贝构造copy constructor
copy
// make copies of persistent objects (e.g. variables)
// that might get used in the future

Photo selfie = takePhoto();
这里是移动构造 move constructor
move
// move temporary objects (e.g return values)
// since we no longer need to use them
```

# 那么compiler怎么知道我们是 copy constructor还是move constructor呢
`是靠的= 右边到底是左值还是右值`
```c++
void foo(Photo pic) 
{ 
Photo beReal = pic;  
pic 是lvalue We can take its address!

Photo insta = takePhoto(); 
takePhoto（） 是rvalue We cannot take its address!
}
```

```c++
Which of the following right-hand assignments are rvalues? •
Hint: which ones have a definite address? rvalue lvalue rvalue lvalue rvalue rvalue
int a = 4;                               rvalue 
int& b = a;                              lvaue
vector<int> c = {1, 2, 3};               rvalue
int d = c[1];                            lvalue
int* e = &c[2];                          rvalue
size_t f = c.size();                     rvalue
```
An lvalue’s lifetime is until the end of scope 
左值的生命周期直到作用域的结尾
An rvalue’s lifetime is until the end of line
右值的声明周期到line的结尾

## lvalue的reference
```c++
void upload(Photo& pic); 
int main() {
 Photo selfie = takePhoto(); 
 upload(selfie); 
 }
```

## rvalue的reference 
```c++
void upload(Photo&& pic); 

int main() 
{ 
upload(takePhoto()); 
}
```
注意这里明显的区别是
是否能在upload里直接使用 一个右值
省去了一个创建selfie的过程
但是就需要lvalue/rvalue overloading


• lvalue references
	• Syntax: Type&
	• Persistent, must keep object in valid state after function terminates
• rvalue references
	• Syntax: Type&&
	• Temporary, we can steal (move) its resources
	• Object might end up in an invalid state, but that’s okay! It’s temporary!

```c++
- Move constructor 
Type::(Type&& other) 
- Move assignment operator 
Type& Type::operator=(Type&& other)
```

## copy constructor 和move constructor 的区别

### 这个是copy constructor
```c++
Photo::Photo(const Photo& other)
: width(other.width)
, height(other.height)
, data(new int[width * height])
{
	std::copy
	(
		other.data,
		other.data + width * height,
		data
	);

}
```

### 这个是move constructor
```c++
Photo::Photo(Photo&& other)
: width(other.width)
, height(other.height)
, data(other.data)
{
	other.data = nullptr;
}
```

## copy assignment 和 move assignment
### Copy assignment operator
```c++
Photo& Photo::operator=(const Photo& other) {
	if (this == &other) return *this;
	delete[] data;
	
	width = other.width;
	height = other.height;
	data = new int[width * height];
	
	std::copy(other.data, other.data + width *
	height, data);
	return *this;
}
```

### Move assignment 
```c++
Photo&
Photo::operator=(Photo&& other)
{
if (this == &other) return *this;
delete[] data

width = other.width
height = other.height
data = other.data

other.data = nullptr;

return *this;
}
```

在成员函数里：
Photo& Photo::operator=(...)
`this` 的类型是：`Photo* const this;`
也就是说：
- `this` 是一个 **指针**
- 指向 **当前被赋值的对象**
 `*this`
	就是：
	当前对象本身（一个左值）

#### 返回值是 T&
意味着:
1. 不返回新对象
2. 不返回拷贝
3. 返回被赋值的那个对象本身

#### other是左值引用/右值引用 
```c++
const Photo& other   // copy assignment
Photo&& other        // move assignment

左值是const 意味着不能动 copy
右值可以动 move
```

### 因为：： 作用域符 所以内部的width和height 都变成this ->width


# std::move 和 SMFs
```c++
void PhotoCollection::insert(const Photo& pic, int pos) {
	for (int i = size(); i > pos; i--)
		myPhotos[i] = myPhotos[i – 1]; // Shuffle elements down
	myPhotos[i] = pic;
}
```

第三行的 myphotos会把所有元素都放到新的位置
即使原来的值永远不会再使用


## Be wary of std::move
```c++
Photo takePhoto();

void foo(Photo whoAmI)

Photo selfie = std::move(whoAmI);
// 这里直接从 copy constructor变成 move constructor

whoAmI.get_pixel(21, 24); // ???
If we move, whoAmI ends up in an unknown state!
}
```

1. 直接把 一个左值cast成一个右值
2. 但是其实参数传参这里本身就发生拷贝了

# Rule zero
如果一个class并不管理内存 那么自带的default版本够用了

Example: Compiler generated SMFs of Post will call SMFs of Photo and std::string ```
```c++
struct Post { 
Photo photo; 
std::string caption; 
};
```
编译器生成的 SMF 会**逐个成员调用它们各自的 SMF**


# Rule of Three
如果一个 Class  类 管理外部的资源
我们必须定义 拷贝赋值和拷贝构造
copy assignment和copy construction
如果不写的话 
那么SMF 不会拷贝底层的资源的
```c++
struct Photo {
    int* data;
    int width, height;
};

如果什么都不写的话
Photo a;
Photo b = a;   // 默认 copy ctor
实际发生的是：
b.data = a.data;   // 浅拷贝

然后：
- 两个对象指向同一块内存
- 任意一个析构 → `delete[] data`
- 另一个直接 **悬空指针 / double free**

💥 **这是 C++ 新手墓地**
```

所以
## 所以 Rule of Three 说：

> **只要你需要下面三者之一，就必须同时定义它们**
> 
- Destructor
- Copy Constructor
- Copy Assignment
### 原因
这三者 **共同决定资源的“复制 + 销毁语义”**
- 析构：怎么释放？
- 拷贝构造：复制时是不是深拷贝？
- 拷贝赋值：已有对象被覆盖时怎么处理？
**缺一个，语义就不完整**


# Rule of Five（五法则）

## Rule of Three 的现代升级版
C++11 之后，多了 **move 语义**，于是：
> **如果你已经手写了资源管理，  
> 那你几乎一定也想要 move。**

所以变成：
- Destructor
- Copy Constructor
- Copy Assignment
- Move Constructor
- Move Assignment
