### MDP Value Iteration and Policy Iteration

import numpy as np
from riverswim import RiverSwim

np.set_printoptions(precision=3)

def bellman_backup(state, action, R, T, gamma, V):
    """
    Perform a single Bellman backup.

    Parameters
    ----------
    state: int
    action: int
    R: np.array (num_states, num_actions)
    T: np.array (num_states, num_actions, num_states)
    gamma: float
    V: np.array (num_states)

    Returns
    -------
    backup_val: float
    """
    backup_val = 0.
    ############################
    # YOUR IMPLEMENTATION HERE #
    part2_sum = 0
    num_states = V.shape[0]
    for i in range(num_states):
        part2_sum += T[state, action, i] * V[i] 
    backup_val = R[state,action] + gamma * part2_sum
    ############################
    return backup_val

def policy_evaluation(policy, R, T, gamma, tol=1e-3):
    """
    Compute the value function induced by a given policy for the input MDP
    Parameters
    ----------
    policy: np.array (num_states)
    R: np.array (num_states, num_actions)
    T: np.array (num_states, num_actions, num_states)
    gamma: float
    tol: float

    Returns
    -------
    value_function: np.array (num_states)
    """
    num_states, num_actions = R.shape
    # 初始化 V_0(s) = 0
    value_function = np.zeros(num_states)

    ############################
    # YOUR IMPLEMENTATION HERE #
    # difference = 1 # initial number
    # while(difference > tol):
    #     value_function_minus1 = value_function.copy()
    #     for state in range(num_states):
    #         # 先拷贝一下直接更新 原value function
            
    #         # 选取动作向左边还是向右
    #         # action
    #         action = policy[state]
    #         current_reward = R[state,action]
            
    #         future_reward_sum = 0
    #         for state_new in range(num_states):
    #             future_reward_sum += gamma * T[state,action,state_new] * value_function_minus1[state_new]
            
    #         value_function[state] = current_reward + future_reward_sum 
    #     difference = np.max(np.abs(value_function - value_function_minus1))
    ############################
    difference = 1
    while(difference > tol):
        value_function_minus1 = value_function.copy()
        for state in range(num_states):
            action = policy[state]
            value_function[state] = bellman_backup(state=state,
                                                    action=action,
                                                    R=R,
                                                    T=T,
                                                    gamma=gamma,
                                                    V=value_function_minus1
                                                    )
        difference = np.max(np.abs(value_function - value_function_minus1))
    ############################                
    
    ######
    return value_function


def policy_improvement(policy, R, T, V_policy, gamma):
    """
    Given the value function induced by a given policy, perform policy improvement
    Parameters
    ----------
    policy: np.array (num_states)
    R: np.array (num_states, num_actions)
    T: np.array (num_states, num_actions, num_states)
    V_policy: np.array (num_states)
    gamma: float

    Returns
    -------
    new_policy: np.array (num_states)
    """
    num_states, num_actions = R.shape
    new_policy = np.zeros(num_states, dtype=int)

    ############################
    # YOUR IMPLEMENTATION HERE #
    for state in range(num_states):
        q_vals = np.zeros(num_actions)
        for action in range(num_actions):
            q_vals[action] = bellman_backup(
                                            state=state,
                                            action=action,
                                            R=R,
                                            T=T,
                                            gamma=gamma,
                                            V=V_policy
                                            )
        new_policy[state] = int(np.argmax(q_vals)) # 贪心选最大Q
    ############################
    return new_policy


def policy_iteration(R, T, gamma, tol=1e-3):
    """Runs policy iteration.

    You should call the policy_evaluation() and policy_improvement() methods to
    implement this method.
    Parameters
    ----------
    R: np.array (num_states, num_actions)
    T: np.array (num_states, num_actions, num_states)
    gamma: float
    tol: float

    Returns
    -------
    V_policy: np.array (num_states)
    policy: np.array (num_states)
    """
    num_states, num_actions = R.shape
    V_policy = np.zeros(num_states)
    policy = np.zeros(num_states, dtype=int)
    ############################
    # YOUR IMPLEMENTATION HERE #

    ############################
    return V_policy, policy


def value_iteration(R, T, gamma, tol=1e-3):
    """Runs value iteration.
    Parameters
    ----------
    R: np.array (num_states, num_actions)
    T: np.array (num_states, num_actions, num_states)
    gamma: float
    tol: float

    Returns
    -------
    value_function: np.array (num_states)
    policy: np.array (num_states)
    """
    num_states, num_actions = R.shape
    value_function = np.zeros(num_states)
    policy = np.zeros(num_states, dtype=int)
    ############################
    # YOUR IMPLEMENTATION HERE #

    ############################
    return value_function, policy


# Edit below to run policy and value iteration on different configurations
# You may change the parameters in the functions below
if __name__ == "__main__":
    SEED = 1234

    RIVER_CURRENT = 'WEAK'
    assert RIVER_CURRENT in ['WEAK', 'MEDIUM', 'STRONG']
    env = RiverSwim(RIVER_CURRENT, SEED)

    R, T = env.get_model()
    discount_factor = 0.99

    print("\n" + "-" * 25 + "\nBeginning Policy Iteration\n" + "-" * 25)

    V_pi, policy_pi = policy_iteration(R, T, gamma=discount_factor, tol=1e-3)
    print(V_pi)
    print([['L', 'R'][a] for a in policy_pi])

    print("\n" + "-" * 25 + "\nBeginning Value Iteration\n" + "-" * 25)

    V_vi, policy_vi = value_iteration(R, T, gamma=discount_factor, tol=1e-3)
    print(V_vi)
    print([['L', 'R'][a] for a in policy_vi])
