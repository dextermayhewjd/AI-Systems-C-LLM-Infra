## 太多containers了
The C++ Standard Template Library (STL)
The many containers of C++ 
```c++
std::vector 
std::set 
std::stack 
std::queue 
std::map 
std::unordered_map 
std::unordered_set 
std::priority_queue 
std::deque 
std::array
```

## Vector
store a list of elements
```c++
std::vector vec { 1, 2, 3, 4 }; 
vec.push_back(5); 
vec.push_back(6); 
vec[1] = 20; 
for (size_t i = 0; i < vec.size(); i++) 
{ 
	std::cout << vec[i] << " "; 
}
```

|你想做什么|推荐写法|说明|
|---|---|---|
|创建空 vector|`std::vector<int> v;`|最常见|
|创建长度为 n、元素为 0 的 vector|`std::vector<int> v(n);`|对 `int` 会值初始化为 0|
|创建长度为 n、元素为 k 的 vector|`std::vector<int> v(n, k);`|显式指定初值|
|在末尾添加元素 k|`v.push_back(k);`|最标准|
|清空 vector|`v.clear();`|size → 0，capacity 不一定释放|
|判断是否为空|`if (v.empty())`|**不要用 `v.size() == 0`**|
|访问第 i 个元素（不检查边界）|`v[i]`|**最快，但不安全**|
|访问第 i 个元素（检查边界）|`v.at(i)`|越界会抛异常|
|修改第 i 个元素|`v[i] = k;`|默认写法|
|修改第 i 个元素（安全）|`v.at(i) = k;`|调试期友好|

## 尽可能使用range-based 
```c++
for (size_t i = 0; i < vec.size(); i++) 
{
 std::cout << vec[i] << " "; 
}
用下面的
for (auto elem : vec) 
{ 
	std::cout << elem << " "; 
}
```

所有容器都适用 不只是vector
Applies for all iterable containers, not just std::vector

## 尽可能使用const auto& 来避免昂贵的拷贝
```c++
std::vector<MassiveType> vec { ... };

for (auto elem : vec)
用下面的
for (const auto& elem : v)
```

vector 没有从头加新的push_front 只有 push_back

# std::deque
```c++
 # include<deque>
```
A deque (“deck”) is a double-ended queue 
Allows efficient insertion/removal at either end
允许高效移除首尾
```c++
void receivePrice(deque<double>& prices, double price)
{
	prices.push_front(price); // Super fast
	if (prices.size() > 10000)
		prices.pop_back(); // Remove last price
		// so we don't exceed 10k
}
```

# Associative Containers

## std::map 
```c++
#inclue <map>

std::map<std::string, int>
```
Equivalent of a Python dictionary 
Sometimes called an associative array
```c++
std::map<std::string, int> map {
	{ "Chris", 2 },
	{ "CS106L", 42 },
	{ "Keith", 14 },
	{ "Nick", 51 },
	{ "Sean", 35 },
};
int sean = map["Sean"]; // 35
map["Chris"] = 31
```

| 你想做什么              | 推荐写法                     | 说明                 |
| ------------------ | ------------------------ | ------------------ |
| 创建空 map            | `std::map<char, int> m;` | 有序 map（红黑树）        |
| 插入键 k、值 v          | `m[k] = v;`              | **最常用**，不存在会自动插入   |
| 插入键值对（不覆盖已有）       | `m.insert({k, v});`      | 若 k 已存在，不会覆盖       |
| 删除键 k              | `m.erase(k);`            | 若不存在，什么也不发生        |
| 判断 key 是否存在（C++20） | `if (m.contains(k))`     | **首选，语义最清晰**       |
| 判断 key 是否存在（C++17） | `if (m.count(k))`        | 返回 0 或 1           |
| 判断 map 是否为空        | `if (m.empty())`         | 标准写法               |
| 读取或写入 `m[k]`       | `int v = m[k];`          | ⚠️ 不存在会**自动插入默认值** |
| 覆盖 key 对应的值        | `m[k] = v;`              | 若不存在 → 插入          |
### std::map<K,V> 存了一堆std:: pair <const K,V>

```c++
std::map<std::string, int> map; 
for (auto kv : map) 
{ // kv is a std::pair 
	std::string key = kv.first;
	 int value = kv.second; 
 }

 std::map<std::string, int> map; 
for (const auto& [key, value] : map) 
{ 
	// key has type const std::string& 
	// value has type const int& 
 }
```
map 是如何实现的呢
binary search tree 也是红黑树
所以 std::map requires K to have an operator<

# std::set 
```c++
#include<set>
```

|你想做什么|`std::set<char>`|
|---|---|
|创建空 set|`std::set<char> s;`|
|向 set 中添加元素 k|`s.insert(k);`|
|从 set 中删除元素 k|`s.erase(k);`|
|判断 k 是否在 set 中（C++20）|`if (s.contains(k))`|
|判断 k 是否在 set 中（C++17）|`if (s.count(k))`|
|判断 set 是否为空|`if (s.empty())`|
But wait... map and set have an alter ego 🥷 

## std::unordered_map  and  std::unordered_set
```c++
#include <unordered_map>
#include <unordered_set>
```
unordered_map 靠bucket存
unordered_map 内部维护：
- 一组 bucket（比如 5 个）
- 每个 bucket 里放 **若干 (key, value) 对**

- **对 key 做 hash**
    `hash("CS106L") → 80489869`    
- **算 bucket 编号**
    `80489869 mod 5 = 4`
- **去第 4 号 bucket**
    - 遍历这个 bucket 里的所有 pair
    - 用 `==` 比较 key
    - 找到就返回 value
    - 找不到就插入（operator[]）
unordered_map =  
**hash → bucket → linear search（小范围）**

hash collision
两个 key 落到同一个 bucket  
👉 这就叫 **hash collision**

key 必须 “hashable”

```c++
std::unordered_map<int, int> ok;          // ✅
std::unordered_map<std::string, int> ok;  // ✅
std::unordered_map<std::ifstream, int> ❌ // 没 hash
```

### 7️⃣ Load factor = 平均每个 bucket 放几个元素

`load_factor = 元素个数 / bucket 数`

### 为什么 load factor 重要？
- load factor 越大
- 每个 bucket 越挤
- 查找越慢（退化成 O(N)）
所以 unordered_map 会：
> **当 load factor 超过阈值 → 自动 rehash**
也就是：
- bucket 数翻倍
- 所有元素重新分配
# 性能对照表

|Data Structure|i-th element|Search|Insertion|Erase|
|---|---|---|---|---|
|`std::vector`|**Very Fast**|Slow|Slow|Slow|
|`std::deque`|**Fast**|Slow|**Fast (front/back)**Slow (others)|**Fast (front/back)**Slow (others)|
|`std::set`|Slow|**Fast**|**Fast**|**Fast**|
|`std::map`|Slow|**Fast**|**Fast**|**Fast**|
|`std::unordered_set`|N/A|**Very Fast**|**Very Fast**|**Very Fast**|
|`std::unordered_map`|N/A|**Very Fast**|**Very Fast**|**Very Fast**|
