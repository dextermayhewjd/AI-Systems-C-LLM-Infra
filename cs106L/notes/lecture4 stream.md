## 定义 
- a general input/output(IO) abstraction for C++
- Abstraction = hide unnecessary details and expose what is only relevant
- Abstractions provide a consistent interface, and in the case of streams the interface is for reading and writing data!

```c++
std::cout << “Hello, World” << std::endl;
```

- Stream = 一个“会记住当前位置的字符通道”，  
用统一的 `<<` / `>>` 接口，把“外部世界的文本” ↔ “程序里的类型” 连起来。

- 看到的一切（`cin / cout / ifstream / ofstream / stringstream`）  
**只是“这个通道接在了哪里”不同**。

1. **I/O 本质是“字符流”**
2. **`>>` / `<<` 是“类型转换 + 移动读写指针”**
3. **所有流共享一套抽象（不管是键盘、文件、string）**

## 核心模型（你一定要有的脑内画面）

### Stream =「字符队列 + 读写指针 + 状态位」

```c++
[B][j][a][r][n][e][ ][S][t][r][o][u][s][t][r][u][p][\n]
 ↑
 current position
```

流里永远是 **字符**，不是 `int / double / string`  
👉 **类型是你“读的时候”才发生的事**

--- 

## `>>` 到底干了什么（这是全课的灵魂）

```c++
double pi;
std::cin >> pi;
```

实际发生的是：

1. 从 stream 当前指针开始
2. 读字符，**跳过前导空白**
3. 一直读到 **不合法字符 / 空白**
4. 把 `"3.14"` **解析成 double**
5. 指针停在 `\n` 后面
6. 如果解析失败 → `failbit = true`

👉 所以 slide 里才会问：
> “我们把 string 存进 double 了？？？”
**是的，但那是 stream 帮你 parse 的**

```bash
Input streams (I) ● a way to read data from a source 
	
	○ Are inherited from std::istream 
	○ ex. reading in something from the console (std::cin) 
	○ primary operator: >> (called the extraction operator)
Output streams (O) ● a way to write data to a destination  
	
	○ Are inherited from std::ostream 
	○ ex. writing out something to the console (std::cout) 
	○ primary operator: << (called the insertion operator)
```


## std :: stringstream 
```c++
void foo() {

/// partial Bjarne Quote
std::string initial_quote = “Bjarne Stroustrup C makes it easy to shoot
yourself in the foot\n”;

/// create a stringstream 
std::stringstream ss(initial_quote);

/// data destinations 
std::string first; 
std::string last; 
std::string language, extracted_quote;

ss >> first >> last >> language; 
std::cout << first << “ ” << last << “ said this: ”<< language << “ “ << extracted_quote << std::endl;
}
```

这里会碰到的问题是读到下一个whitespace就停了 读到makes就停下来了 不会读到 句末
（每次读 `掉` 一个空格）

## getline（）

```c++
istream& getline(istream& is, string& str, char delim) 

● getline() reads an input stream, 
is, up until the delim char and stores it in some buffer, str.

 ● The delim char is by default ‘\n’. 
 
 ● getline() consumes the delim character! ○ PAY ATTENTION TO THIS :)
```
读一个inputstream

delim默认是换行符
会吞掉一个换行符

- 从当前位置开始
- 一直读到 `\n`
- **把 `\n` 吃掉**
- 存剩下的内容
# cout 和cin
## output streams
- a way to write data to a destination/external source 
	- ex. writing out something to the console (std::cout) 
	- use the << operator to send to the output stream
ouputstream 是把数据写到一个目的地或者外部源的

## flush
```c++
std::cout << "6.28";
```
`std::cout` 是有 buffer 的
并不一定立刻显示
知道非常明确的flush了

### 什么时候会flush

- `std::endl`（换行 + flush）❌ 慢
- `std::flush`
- 程序结束
- buffer 满
- When tied streams interact (ie. cout has to flush before you take input via cin)
  例如cout必须flush 在你使用cin前

所以只是换行 推荐使用
```c++
'\n'！不要 
std::endl！

```

```c++
double tao = 6.28; 
std::cout << tao; 

1. std::cout << std::flush
2. std::cout << std::endl;
都会flush
```


```c++
int main()
{
for (int i=1; i <= 5; ++i) 
	{
		std::cout << i << std::endl;
	}
return 0;
}

<<
“1” 
“2” 
“3” 
“4” 
“5”
int main()
{
for (int i=1; i <= 5; ++i) 
	{
		std::cout << i ;
	}
return 0;
}
<<
“12345”
```

## ## 工程里的标准做法（你以后可以直接照抄）

### ✅ 推荐
`std::cout << "value = " << x << '\n';`
### ❌ 不推荐（除非你知道自己在干嘛）
`std::cout << "value = " << x << std::endl;`
### ✅ 真正需要 flush 时（明确写出来）
`std::cout << "waiting..." << std::flush;`
这比 `endl` **语义清楚 + 可控**


```c++
没明白
int main()
{
std::ios::sync_with_stdio(false)
	for (int i=1; i <= 5; ++i) 
	{
		std::cout << i << ‘\n’;
	}
return 0;
}
```




## cerr and clog
 `cerr`: used to output errors (unbuffered) 
		 - sends errors out IMMEDIATELY 
 `clog`: used for non-critical event logging (buffered)

# Output File Streams

## 一、Output File Streams（`std::ofstream`）在干嘛


```c++
int main() {
/// associating file on construction
std::ofstream ofs(“hello.txt”);
if (ofs.is_open()) 
{
	ofs << “Hello CS106L!” << ‘\n’;
}
ofs.close();
ofs << “this will not get written”;
ofs.open(“hello.txt”);
ofs << “this will though! It’s open again”;

return 0;
```

 1️⃣ `std::ofstream` 
一句话：
> **`std::ofstream` = 一个“把字符流写进文件”的 `ostream`**
所以它具备所有 `ostream` 的能力：
```c++
ofs << "hello" << 123 << '\n';
```
**和 `std::cout` 一模一样**，目的地从“终端”变“文件”。

 2️⃣ 构造时
`std::ofstream ofs("hello.txt");`

1. 创建一个 `ofstream` 对象
2. 尝试打开文件 `"hello.txt"`
3. **默认模式：**
    - 如果文件不存在 → 创建
    - 如果文件存在 → **清空（truncate）**

3️⃣`is_open()`
```c++
if (ofs.is_open()) {
    ofs << "Hello\n";
}
```
在检查文件是否打开并且尝试写入
4️⃣ `close()`
这一步
- flush buffer
- 关闭文件描述符
- **流对象还在，但已经“断线”**

 6️⃣ 重新 `open()` 合法
`ofs.open("hello.txt");`
此时：
- 文件重新打开
- 默认还是 **truncate 模式**
- 之前内容可能被清空
7️⃣ `std::ios::app` 是什么？

```c++
ofs.open("hello.txt", std::ios::app);
```
这是一个 **open mode flag**，意思是：
> **append（追加）模式**

|模式|行为|
|---|---|
|默认|清空文件|
|`std::ios::app`|从文件末尾写|
|`std::ios::trunc`|强制清空|
|`std::ios::binary`|二进制模式|
## inputstream
```c++
int inputFileStreamExample() {
std::ifstream ifs(“input.txt”);
	if (ifs.is_open()) {
		std::string line;
		std::getline(ifs, line);
		std::cout << “Read from the file: “ << line << ‘\n’;
	}
	if (ifs.is_open()) {
		std::string lineTwo;
		std::getline(ifs, lineTwo);
		std::cout << “Read from the file: “ << lineTwo << ‘\n’;
	}
return 0;
}
```

## std: : cin
● std::cin is buffered 
● Think of it as a place where a user can store some data and then read from it 
● std::cin buffer stops at a whitespace 
● Whitespace in C++ includes: 
	○ “ ” – a literal space 
	○ \n character 
	○ \t character

# 四、`std::cin` 那一大段“灾难现场”到底在教什么
核心只有 **3 条规则**，但 slide 拆成了 30 页 😅

---

## 规则 1：`>>` 读到 whitespace 停
`std::cin >> name;`
- 读到空格 / `\n` / `\t` 停
- `"Rachel Fernandez"` → 只得到 `"Rachel"`
---
## 规则 2：`>>` 不吃掉 `\n`
`std::cin >> pi;`
输入：
`3.14\n`
buffer 里剩下：
`\n`

---

## 规则 3：`getline` 会立刻读并吃掉 `\n`

`std::getline(std::cin, name);`
如果 buffer 里一开始就是 `\n`：
👉 直接读到 **空字符串**

---

## 所有“cin fails”的根因只有一句话
> **你在同一个 stream 里混用了两种解析规则**

---

## slide 最后的结论是对的，而且是工程级结论：
> ❗**不要混用 `>>` 和 `getline`**
```c++
cin 3 . 1 4 \n R a c h e l F e r n a n d e z \n 6 . 2 \n
void cinGetline() {
 double pi;
 double tao;
 std::string name;

 std::cin >> pi;              // ❌ token 解析，留下 '\n'
 std::getline(std::cin, name); // ❌ 读掉 '\n'，得到空串
 std::getline(std::cin, name); // ❌ 侥幸读到真正名字
 std::cin >> tao;             // ❌ 又回到 token 解析

 std::cout << ...
}

```
### 正确姿势只有两个：
#### ✅ 全 `>>`
`std::cin >> a >> b >> c;`

#### ✅ 全 `getline` + `stringstream`

```c++
std::string line;
std::getline(std::cin, line);

std::stringstream ss(line);
int n;
double x;
ss >> n >> x;
```