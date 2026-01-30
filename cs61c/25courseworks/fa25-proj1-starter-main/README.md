# 61C Project 1: Snek (C) - Creating the Default Game State

# 61C Project 1: Snek (Snake Game in C)

本项目是UC Berkeley 61C课程的首个C语言实战项目，核心目标是实现一个可玩的贪吃蛇游戏，通过该项目练习C语言基础、内存管理、结构体使用、文件操作及程序调试等核心能力。

## 项目基础信息

- **截止时间**：Thursday, September 12, 11:59:59 PM PT

- **贪吃蛇演示**：若不熟悉游戏规则，可参考课程提供的演示链接体验

- **核心要求**：提交工单前必须展示调试尝试，未尝试/不理解调试将要求完成Lab2后重新提交

## 前置准备

### 必做项

1. 完成Lab 0的环境搭建

2. 完成Lab 1-2（项目核心前置实验）

### 推荐学习内容

1. 课程讲座：Lectures 2-3、Lecture 4的内存管理/布局章节

2. 课程讨论：Discussions 1 and 2

## 环境搭建

### 组队规则

- 支持**单人完成**或**双人搭档**，必须在**hive机器**上开发（禁止本地开发，Lab0有hive机器搭建教程）

- ⚠️ 重要：Gradar上创建小组后**无法修改搭档**（添加/移除/替换），确认搭档后再操作；需同时在Gradar和Gradescope提交中添加搭档

- 特殊情况（搭档退课/无响应）需私下联系课程团队申请调整

### 仓库操作（hive机器上执行）

1. 登录Gradar，注册Project 1小组并创建GitHub仓库（双人搭档由一方创建并邀请另一方，另一方仅接受邀请，不重复创建）

2. 克隆仓库到本地（替换占位符为实际仓库名）

    ```Bash
    
    git clone git@github.com:61c-student/fa24-proj1-USERNAME.git 61c-proj1
    ```

3. 进入仓库目录

    ```Bash
    
    cd 61c-proj1
    ```

4. 添加课程starter仓库为远程源

    ```Bash
    
    git remote add starter https://github.com/61c-teach/fa24-proj1-starter.git
    ```

5. 拉取starter代码（项目基础框架）

    ```Bash
    
    git pull starter main
    ```

### 可修改文件

⚠️ 仅允许修改以下3个文件，其余文件禁止改动：

- `state.c`（核心逻辑实现）

- `snake.c`（主程序补全）

- `custom_tests.c`（自定义测试用例）

## 核心概念概述

### 1. 贪吃蛇游戏网格定义

```
##############
#            #
#    dv      #
#     v   #  #
#     v   #  #
#   s >>D #  #
#   v     #  #
# *A<  *  #  #
#            #
##############
```
游戏以字符网格为基础，包含墙壁、果实、贪吃蛇（尾/身/头），各字符含义及规则如下：

|字符|含义|方向关联（贪吃蛇）|
|---|---|---|
|`#`|墙壁|-|
|空格|空位置|-|
|`*`|果实|-|
|`wasd`|贪吃蛇尾巴|w(上)/a(左)/s(下)/d(右)|
|`^<v>`|贪吃蛇身体|^(上)/<(左)/v(下)>(右)|
|`WASD`|存活的贪吃蛇头部|W(上)/A(左)/S(下)/D(右)|
|`x`|死亡的贪吃蛇头部|-|
### 2. 贪吃蛇移动核心规则

每个时间步，所有贪吃蛇按以下规则移动：

1. 蛇向**头部指向的方向**移动一格

2. 头部撞到**墙壁**或**任意蛇的身体** → 蛇死亡，头部替换为`x`，停止后续所有移动

3. 头部吃到果实（`*`）→ 蛇长度+1（仅更新头部，不更新尾部），同时生成新果实到网格随机空位置

In the example above, after one time step, the board will look like this:
```
##############
#         *  #
#     s      #
#     v   #  #
#     v   #  #
#   s >>>D#  #
#   v     #  #
# A<<  *  #  #
#            #
##############
```
After one more time step, the board will look like this:


```
##############
#         *  #
#     s      #
#     v   #  #
#     v   #  #
#     >>>x#  #
#   s     #  #
#A<<<  *  #  #
#            #
##############
```
Snakes are guaranteed to be at least three units long.

### 3. 贪吃蛇编号规则

```
#############
#  s  d>>D  #
#  v   A<a  #
#  S    W   #
#       ^   #
#       w   #
#############
```
Snake 0 is the snake with tail s, snake 1 has tail d, snake 2 has tail a, and snake 3 has tail w.

1. 按**尾巴的出现位置**编号，顺序为**从上到下、从左到右**

2. 初始编号确定后，游戏全程编号不改变

3. 所有蛇初始长度至少为3格

### 4. 游戏棋盘特性
```
##############
#            #######
#####             ##
#   #             ##
#####             ######
#                 ##   #
#                 ######
#                 ##
#                  #
#      #####       #
########   #########
```


- 棋盘**不一定是矩形**，每行字符数可不同，但每行**首尾必须是墙壁（#）**

- 棋盘为**封闭空间**，蛇无法向任意方向无限移动

### 5. 核心数据结构（定义在`state.h`）

⚠️ 禁止修改结构体定义，仅可使用其字段完成开发

#### `game_state_t`（游戏状态结构体）

存储整个游戏的核心状态，包含棋盘和所有蛇的信息：  
 snake game is stored in memory in a `game_state_t` struct, which is defined in `state.h`. The struct contains the following fields:
```C

typedef struct {
    unsigned int num_rows;  // 棋盘行数
    char** board;           // 棋盘：二维字符数组，每行以换行符结尾且为有效字符串
    unsigned int num_snakes;// 棋盘上的蛇的数量
    snake_t* snakes;        // 蛇的数组：存储所有蛇的信息
} game_state_t;
```

#### `snake_t`（单条蛇的结构体）

存储单条蛇的位置和存活状态：  
Also defined in `state.h`, each `snake_t` struct contains the following fields:

```C

typedef struct {
    unsigned int tail_row;  // 尾巴行号（零索引）
    unsigned int tail_col;  // 尾巴列号（零索引）
    unsigned int head_row;  // 头部行号（零索引）
    unsigned int head_col;  // 头部列号（零索引）
    bool live;              // 存活状态：true=存活，false=死亡
} snake_t;
```

Please don't modify the provided struct definitions. You should only need to modify `state.c` `snake.c`, and `custom_tests.c` in this project.

## 编译、测试与调试

### 核心原则

⚠️ 项目提供Makefile，**禁止直接调用gcc**编译，所有编译/测试均通过make命令执行

### 两个核心可执行文件

|可执行文件|用途|编译命令|运行命令|
|---|---|---|---|
|`unit-tests`|单元测试（Task1-6）|`make unit-tests`|`./unit-tests`|
|`snake`|完整游戏（Task7集成测试）|`make snake`|`./snake [参数]`|
### 通用调试工具/命令

1. **Valgrind**：检测内存泄漏/越界读写，命令示例：`valgrind ./unit-tests`、`valgrind ./snake [参数]`

2. **CGDB**：断点调试，核心命令：

    - 设置断点：`b 文件名:行号`（如`b state.c:50`）

    - 启动程序：`r`

    - 查看调用栈（段错误时）：`bt`/`backtrace`

    - 打印棋盘：`p print_board(state, stdout)`（调试时实时查看棋盘状态）

3. **printf调试**：代码中添加printf打印变量，重新编译后运行查看输出

4. **自定义测试**：在`custom_tests.c`中编写测试用例，编译命令`make custom-tests`，运行`./custom-tests`

### 测试注意事项

- 课程提供的单元测试**非全覆盖**，通过单元测试不代表实现完全正确，需自行编写自定义测试

- 单元测试失败时，可查看`unit-test-out.snk`文件对比棋盘输出差异

### 常见错误排查

- **Segmentation fault (core dumped)**：程序崩溃，通过CGDB的`bt`命令定位崩溃行号

- **内存泄漏**：通过Valgrind命令检测，确保所有堆内存均被释放

## 核心任务分解（Task1-Task8）

所有任务的核心实现文件为`state.c`（除Task7为`snake.c`、Task8为反馈表），每个任务均提供单元测试/专用测试命令，按步骤完成即可。

### Task 1：实现`create_default_state`（创建默认游戏状态）

#### 功能要求

在`state.c`中实现，**硬编码**创建指定的默认游戏棋盘，返回`game_state_t*`指针（堆内存）。

默认棋盘规格：

- 18行20列，果实位于(2,9)，蛇尾巴(2,2)，蛇头部(2,4)

- 棋盘样式参考课程文档中的默认布局（首尾墙壁，中间仅一条蛇+一个果实）

#### 函数定义

```C

game_state_t *create_default_state(void);
```

#### 关键提示

1. 游戏状态需存储在**堆内存（heap）**（栈内存会随函数返回释放，栈/静态/代码区均不可用）

2. 可用`strcpy`复制每行棋盘字符

3. 需正确初始化`game_state_t`所有字段（num_rows/board/num_snakes/snakes）

#### 测试方法

```Bash

make unit-tests && ./unit-tests  # 运行单元测试
```

### Task 2：实现`free_state`（释放游戏状态内存）

#### 功能要求

在`state.c`中实现，**递归释放**`game_state_t`的所有堆内存，包括：

1. 棋盘二维数组（`board`的每一行 + `board`本身）

2. 蛇数组（`snakes`）

3. `game_state_t`结构体本身

#### 函数定义

```C

void free_state(game_state_t* state);
```

#### 测试方法（内存泄漏检测）

```Bash

make valgrind-test-free-state  # 无内存泄漏则测试通过
```

### Task 3：实现`print_board`（打印游戏棋盘）

#### 功能要求

在`state.c`中实现，将棋盘内容打印到指定的文件指针（支持stdout/文件等）。

#### 函数定义

```C

void print_board(game_state_t* state, FILE* fp);
```

#### 关键提示

使用`fprintf`实现向任意文件指针的打印（替代printf，支持多输出目标）

#### 测试方法

```Bash

make unit-tests && ./unit-tests
# 输出错误时查看对比文件：unit-test-out.snk
```

### Task 4：实现`update_state`（更新游戏状态，核心移动逻辑）

该任务为项目核心，分5个子任务，先实现辅助函数，再基于辅助函数完成主逻辑，**辅助函数不单独评分，仅检查update_state正确性**。

#### Task 4.1：实现基础辅助函数（无单元测试，需自行在`custom_tests.c`编写测试）

所有函数接收单个字符，返回蛇的相关属性，**仅处理指定蛇字符，其他字符返回值未定义**：

```C

// 判断是否为蛇尾巴（wasd）
bool is_tail(char c);
// 判断是否为蛇头部（WASDx）
bool is_head(char c);
// 判断是否为蛇的任意部分（wasd^<v>WASDx）
bool is_snake(char c);
// 蛇身体→尾巴转换（^→w, <→a, v→s, >→d）
char body_to_tail(char c);
// 蛇头部→身体转换（W→^, A→<, S→v, D→>）
char head_to_body(char c);
// 根据字符获取下一行号（v/s/S→+1，^/w/W→-1，其他不变）
unsigned int get_next_row(unsigned int cur_row, char c);
// 根据字符获取下一列号（>/d/D→+1，</a/A→-1，其他不变）
unsigned int get_next_col(unsigned int cur_col, char c);
```

#### Task 4.2：实现`next_square`（获取蛇下一个移动位置的字符）

##### 功能要求

返回指定蛇的头部即将移动到的网格位置的字符，**不修改任何游戏状态**。

##### 函数定义

```C

char next_square(game_state_t* state, int snum);
```

##### 关键提示

1. 使用Task4.1的辅助函数

2. 可使用课程提供的`get_board_at`/`set_board_at`辅助函数操作棋盘

##### 测试方法

```Bash

make unit-tests && ./unit-tests
```

#### Task 4.3：实现`update_head`（更新蛇的头部）

##### 功能要求

按头部方向移动蛇头，**同时更新棋盘和snake_t结构体**，忽略墙壁/果实/蛇身（仅单纯移动）。

##### 函数定义

```C

void update_head(game_state_t* state, int snum);
```

##### 核心操作

1. 棋盘：在新位置添加头部字符（WASD），原头部位置转换为身体字符（^<v>）

2. 结构体：更新`snake_t`的`head_row`/`head_col`

##### 测试方法

```Bash

make unit-tests && ./unit-tests
```

#### Task 4.4：实现`update_tail`（更新蛇的尾部）

##### 功能要求

按蛇的移动方向更新蛇尾，**同时更新棋盘和snake_t结构体**。

##### 函数定义

```C

void update_tail(game_state_t* state, int snum);
```

##### 核心操作

1. 棋盘：清空原尾巴位置（设为空格），原尾巴下一个身体位置转换为尾巴字符（wasd）

2. 结构体：更新`snake_t`的`tail_row`/`tail_col`

##### 测试方法

```Bash

make unit-tests && ./unit-tests
```

#### Task 4.5：实现`update_state`（主移动逻辑，整合所有辅助函数）

##### 功能要求

按贪吃蛇移动规则，更新所有蛇的状态，处理**死亡**/**吃果实生长**/**生成新果实**逻辑。

##### 函数定义

```C

void update_state(game_state_t* state, int (*add_food)(game_state_t* state));
```

##### 关键参数说明

- `add_food`：**函数指针**，指向生成新果实的函数，调用方式：`add_food(state)`，成功生成返回非0值，无需实现该函数，直接调用即可。

##### 核心规则实现

1. 遍历所有蛇，仅处理**存活**的蛇

2. 调用`next_square`获取下一个位置字符，分情况处理：

    - 下一个位置是`#`/蛇身 → 蛇死亡：将棋盘头部改为`x`，结构体`live`设为`false`

    - 下一个位置是`*`（果实）→ 吃果实：仅调用`update_head`（生长，不更新尾部），并调用`add_food`生成新果实

    - 下一个位置是空格 → 正常移动：依次调用`update_head`和`update_tail`

##### 测试方法

```Bash

make unit-tests && ./unit-tests
```

### Task 5：实现`load_board`（从文件流加载棋盘）

支持从**任意文件流**（包括stdin）读取棋盘，支持**非矩形棋盘**，**内存高效**（不额外分配多余内存），分2个子任务完成。

#### 核心要求

1. 必须使用`fgets`读取行（禁止使用fseek/rewind等不支持stdin的函数）

2. 每行按需分配内存，例如3字符的行仅分配3+1（结束符）字节

3. 暂将`num_snakes`设为0，`snakes`设为NULL（Task6初始化）

4. 可用`strchr`处理行尾字符，`realloc`实现动态数组扩容（棋盘行数组）

#### Task 5.1：实现`read_line`（从文件流读取一行到堆内存）

##### 函数定义

```C

char *read_line(FILE* file);
```

##### 功能要求

- 读取一行字符，存储到堆内存，返回字符串指针

- fgets出错/到达EOF时返回NULL

- 无需处理行尾换行符，保留原始格式

#### Task 5.2：实现`load_board`（整合read_line，加载棋盘到game_state_t）

##### 函数定义

```C

game_state_t *load_board(FILE* file);
```

##### 核心操作

1. 循环调用`read_line`读取每行，动态扩容棋盘行数组（`board`）

2. 初始化`game_state_t`的`num_rows`/`board`字段

3. `num_snakes=0`，`snakes=NULL`

##### 测试方法

```Bash

make unit-tests && ./unit-tests
```

### Task 6：实现`initialize_snakes`（初始化蛇数组）

基于加载的棋盘，找到所有蛇的尾巴和头部，初始化`game_state_t`的`num_snakes`和`snakes`数组，分2个子任务完成。

#### Task 6.1：实现`find_head`（根据尾巴找头部，填充snake_t）

##### 功能要求

给定已填充`tail_row`/`tail_col`的`snake_t`，遍历棋盘**追踪蛇的身体**，找到头部位置并填充`head_row`/`head_col`。

##### 函数定义

```C

void find_head(game_state_t* state, int snum);
```

#### Task 6.2：实现`initialize_snakes`（创建并初始化蛇数组）

##### 功能要求

遍历棋盘找到所有蛇的尾巴（wasd），按**从上到下、从左到右**编号，创建蛇数组并初始化所有字段。

##### 函数定义

```C

game_state_t* initialize_snakes(game_state_t* state);
```

##### 核心操作

1. 遍历棋盘，统计尾巴数量（即`num_snakes`）

2. 为`snakes`数组分配堆内存（大小为`num_snakes * sizeof(snake_t)`）

3. 对每个蛇，先填充`tail_row`/`tail_col`，调用`find_head`填充头部位置

4. 所有蛇初始状态`live=true`

5. 原地修改传入的`state`并返回

##### 测试方法

```Bash

make unit-tests && ./unit-tests
```

### Task 7：补全`snake.c`的main函数（完整游戏集成）

#### 功能要求

整合Task1-Task6的所有函数，补全`snake.c`的主程序，实现**从文件/stdin加载棋盘**→**更新一次游戏状态**→**输出到文件/stdout**的逻辑，程序每次运行仅更新**一个时间步**。

#### 核心测试命令

##### 运行所有集成测试

```Bash

make run-integration-tests  # 内部会自动编译make snake
```

##### 单独调试某个测试用例（替换TESTNAME为实际测试名，如01-simple）

```Bash

# CGDB调试
cgdb --args ./snake -i tests/TESTNAME-in.snk -o tests/TESTNAME-out.snk
# Valgrind检测内存/越界
valgrind ./snake -i tests/TESTNAME-in.snk -o tests/TESTNAME-out.snk
# 对比输出与参考结果
diff tests/TESTNAME-ref.snk tests/TESTNAME-out.snk
```

##### 从stdin加载棋盘测试（自动 grader 会检测该功能）

```Bash

# 加载并输出
./snake --stdin -o tests/TESTNAME-out.snk < tests/TESTNAME-in.snk
# 对比结果
diff tests/TESTNAME-ref.snk tests/TESTNAME-out.snk
# CGDB/Valgrind调试该模式
cgdb ./snake && set args --stdin -o tests/TESTNAME-out.snk < tests/TESTNAME-in.snk
valgrind ./snake --stdin -o tests/TESTNAME-out.snk < tests/TESTNAME-in.snk
```

##### 测试文件不存在的错误处理（应返回错误码-1）

```Bash

make run-nonexistent-input-file-test
```

#### 测试用例列表

tests文件夹下的所有测试用例，覆盖简单移动、方向、吃果实、撞墙、多蛇等所有场景：

01-simple、02-direction、03-tail、04-food、05-wall、06-small、07-medium、08-multisnake、09-everything、10-filled、11-manyclose、12-corner、13-sus、14-orochi、15-hydra、16-huge、17-wide、18-tall、19-101-127、20-long-line、21-bigL

### Task 8：填写搭档/项目反馈表

项目为新课程实验，课程团队收集反馈用于优化，**反馈不影响成绩**，可诚实提出建议：

- 双人搭档：评价合作体验

- 单人完成：仅评价项目本身

- 反馈表链接：课程提供的专属链接

## 提交与评分

### 提交方式

将代码提交到Gradescope的**Project 1**作业入口，需注意：

1. 仅提交修改后的`state.c`、`snake.c`、`custom_tests.c`

2. 双人搭档需在提交中添加对方账号（Gradar已添加的前提下）

3. 可**无限次提交**，Gradescope显示的最后一次分数为最终成绩

### 评分标准

1. 单元测试（Task1-Task6）：占比主要部分，通过即得分

2. 集成测试（Task7）：覆盖完整游戏逻辑，需通过所有测试用例

3. 内存管理：无内存泄漏、无越界读写（Valgrind检测）

4. 代码规范：仅修改指定文件，不改动结构体/其他源文件

## 趣味玩法：运行交互式贪吃蛇

完成所有任务后，可运行自己实现的交互式贪吃蛇游戏，体验成果：

### 编译并运行

```Bash

make interactive-snake && ./interactive-snake
```

### 游戏控制

1. 方向键：`wasd` 控制蛇的移动方向（与游戏中蛇的字符定义一致）

2. 调速方式：

    - 启动时调速：`./interactive-snake -d 0.5`（0.5为时间步间隔，单位秒，值越小越快）

    - 游戏中调速：按`]`加快，按`[`减慢
> （注：文档部分内容可能由 AI 生成）