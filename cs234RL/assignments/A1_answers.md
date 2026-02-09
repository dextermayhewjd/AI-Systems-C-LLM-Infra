# CS 234 Winter 2026 Assignment 1

## Effect of Effective Horizon [8pts]

一个agent 管理一个商店的存货， 用MDP表示。 这个库存水平指的是currently的 in stock的 items。  
在1-10之间， 在任意时刻，agent都有两个选择，可以选择sell或者buy（如果可能的话

先翻译一下规则：  

1. 如果stock > 0 agent就是卖出  
    reward+1， stock level -1  
    I如果s = 0 什么都不会发生.
2. s < 9 并且agent 买入  
    那么不收获reward 并且stock level 变成s+1

3. 店主喜欢在一天结束看到库存是满的  
    reward + 100

4. s = 10 是terminal state  
    如果遇到就会停止  

- r(s, sell, s − 1) = 1 for s > 0 and r(0, sell, 0) = 0  
- r(s, buy, s + 1) = 0 for s < 9 and r(9, buy, 10) = 100.  
The last condition indicates that transitioning from s = 9 to s = 10 (fully stocked) yields +100 reward.  

在开始一天的时候 库存水平被认为是总在s=3  
我们考虑agent的最佳policy 会如何更具我们调整 有限的Horizon H 而改变  

`考虑下面这个例子`  
H = 4, agent 可以卖3个steps（因为一开始的库存水平是s = 3）  
s从3 -> 2 ->1 -> 0  
受到reward +1,+1，+1.  
在第四轮inventory是空的因为s = 0,可以卖也可以买（不懂为什么可以卖）  
然后问题结束 terminate 因为时间expired了

`(a)`  
```bash
Starting from the initial state s = 3, 
is it possible to a choose a value of H that results in the optimal policy 
taking both buy and sell steps during its execution? 
Explain why or why not.
[2 pts]
```

我觉得考虑到上面的例子，因为一开始库存是3,快速拿到reward的方式是卖，  
所以 $0\lt H\le 3$的情况都只有快速卖。  
H = 4 的时候最佳策略并不需要买入，因为只要卖就像 第四步可以是买也可以是卖  
$5\lt H\le 6$ 的时候，必须要包含买入的action, 因为s=3 所以可以在卖出的情况下再买入卖出  
但是有一个转折，如果H = 7的情况 可以全部买入，立马触发S = 10之后reward = 100

这个reward标志着之后所有的最佳策略，应该是在此基础上，把买入触发S=10的操作延后，即在全部买入前，买入卖出，意味着每增加两个steps,例如H=9，就应该buy and sell 捆绑。  

```bash
(b) In the infinite-horizon discounted setting, is it possible to choose a fixed value of γ ∈ [0, 1)
such that the optimal policy starting from s = 3 never fully stocks the inventory? You do not
need to propose a specific value, but simply explain your reasoning either way. [2 pts]
```

考虑discount factor  
V(s) = 1 + ${\gamma}^2+{\gamma}^4 + ...  = \frac{1}{1 - {\gamma}^2}$

所以如果reward 要 小于这个值的话100才需要触发S=10 获得reward = 100  

```bash
Consider two versions of this inventory MDP. In the first version, the MDP is an infinite-horizon
MDP with discount factor γ. In the second version, the MDP is a finite-horizon MDP with
horizon H, no discount factor, and episodes that terminate after exactly H time steps even if
a terminal state has not been reached.
Does there ever exist a choice of γ such that the optimal policy for the infinite-horizon MDP
is the same as the optimal policy for the finite-horizon MDP with horizon H? If so, give a
concrete example of values of γ and H for which this holds. [2 pts]
```

一个是H= 1 和 $\gamma$ = 0 
这样子第一步天然等价  

否则就是问题2的value  = H

```bash
(d) Using the same setup as in part (c), does there always exist a discount factor γ such that the
optimal policy for the infinite-horizon MDP matches the optimal policy for the finite-horizon
MDP for any H? Briefly justify your answer in 1–2 sentences.[2 pts]
```

有限时域的最优策略通常是时间依赖的（同一库存 𝑠，因为“剩余步数”不同会做不同选择，比如临近截止会更倾向于直接买到 10 拿 100 或直接卖掉赚 1），而无限折扣 MDP 用固定𝛾 得到的最优策略通常是时间不变的 stationary 策略（只依赖 s）。因此对某些H，有限时域的最优策略无法被任何单一 γ 的无限折扣最优策略完全匹配。

## 2 Reward Hacking [5 pts]

(a)
因为并线会造成其他车辆减速，拉低很多车的速度，但是如果红色车一直停在匝道口，那么所有其他车的速度都能不下降，从而如果不设限那么可以增加很多车的速度。

(b)把“到达/进度”加入奖励：例如给红车沿路线的进度正奖励，并对长时间停滞加惩罚：  


## 3 Bellman Residuals and performance bounds [30 pts]

Definitions:  
  Recall that a value function is a |S|-dimensional vector where `|S| is the number of
states of the MDP`.  
  When we use the term V in these expressions as an “arbitrary value function”,  
we mean that `V is an arbitrary |S|-dimensional vector which need not be aligned with the definition of the MDP at all`. On the other hand, V π is a value function that is achieved by some policy π in the MDP.  
  For example, say the MDP has 2 states and only negative immediate rewards. V = [1, 1]
would be a valid choice for V even though t`his value function can never be achieved by any policy
π,` but we can never have a V π = [1, 1].  
  This distinction between V and V π is important for thisquestion and more broadly in reinforcement learning.