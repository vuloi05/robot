# Ch 17: Sequential Decision Making and Dynamic Programming

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Part IV: Robot Decision Making
- **Trang sách:** 437–456 | **Trang PDF:** 439–458
- **Độ ưu tiên cho dự án:** `HỮU ÍCH`
- **Tóm tắt:** Quy hoạch động tất định và Markov Decision Processes (MDP) dưới bất định.

---

### [PDF p.439 | Book p.437]

17
Sequential Decision Making and Dynamic Programming
In Chapter 16, we introduced finite state machines as a structured and explicit
way to model the logical flow of a robot’s behavior, allowing us to hand-design
a set of rules that govern its actions in response to events. For well-defined tasks
with a limited number of states, a carefully crafted finite state machine is an effective and interpretable way to implement a robot’s decision-making logic. However, the very structure that makes finite state machines clear also imposes fundamental limitations, especially as the complexity and uncertainty of the robot’s
environment grow.
This chapter introduces a more general, optimization-based framework that
directly addresses these limitations. Rather than manually specifying decision
rules, we formulate decision-making as a mathematical optimization problem,
allowing optimal actions to be computed automatically for complex, multi-step
tasks, even under uncertainty. The central computational tool explored in this
chapter is dynamic programming, a powerful algorithmic paradigm for solving
sequential decision-making problems. Dynamic programming operates by decomposing complex, long-horizon problems into a sequence of simpler, nested
subproblems that can be solved efficiently. As we will see, it also provides the
theoretical foundation for modern learning-based approaches like reinforcement
learning (Chapter 18) and imitation learning (Chapter 19).
We begin in Section 17.1 by applying dynamic programming to deterministic
decision-making problems, where the robot’s actions have certain and predictable
outcomes. We then extend this framework in Section 17.2 to stochastic decisionmaking problems, specifically Markov decision processes (MDPs), which explicitly account for uncertainty in the environment. Finally, in Section 17.3, we discuss the limitations of classical dynamic programming methods, thereby motivating the learning-based approaches introduced in later chapters.

17.1

Deterministic Sequential Decision Making

We begin our study of dynamic programming by introducing a simple, yet extremely general, formulation of sequential decision making. Despite its apparent

---

### [PDF p.440 | Book p.438]

438

principles of robot autonomy

simplicity, this formulation captures a wide range of problems arising in robotics,
control, operations research, and artificial intelligence. We first consider the deterministic case, where the outcome of each action is fully predictable, before
addressing stochasticity in the next section.
In this formulation, time is modeled as a sequence of discrete stages at which
decisions are made. That is, we consider a discrete-time setting1 , where the evolution of the system is described by a difference equation of the form:
x t +1 = f t ( x t , u t ),

t = 0, . . . , T − 1,

(17.1)

where xt ∈ Rn denotes the system state at time step t, ut ∈ Rm is the control
applied at that step, and f t specifies how the state evolves. The integer T defines
a finite planning horizon.
At each time step, not all controls may be available. We therefore associate
with each state xt a set of admissible controls, denoted by U ( xt ), and impose the
constraint:
u t ∈ U ( x t ),

t = 0, . . . , T − 1.

(17.2)

No particular structure is assumed for U ( xt ). Depending on the application, it
may be a finite set of discrete actions, a continuous region of allowable inputs, or
a state-dependent subset encoding physical, logical, or resource limitations.
The objective of the decision making problem is specified through an additive
cost function defined over the planning horizon:
T −1

J ( x 0 , u 0 , . . . , u T −1 ) = g T ( x T ) + ∑ g t ( x t , u t ),

(17.3)

t =0

where gt represents the stage cost incurred at time t and gT is a terminal cost
applied to the final state. The additivity of the cost over time is a central structural
assumption: it is this property that enables the decomposition of the problem
into simpler subproblems, which lies at the heart of dynamic programming. No
assumptions are made regarding smoothness, convexity, or time invariance of the
cost functions.
The deterministic sequential decision making problem can be formally defined
as follows:
Definition 17.1.1 (Deterministic Sequential Decision Making Problem). Given
the discrete-time system (17.1), the control constraints (17.2), and the additive
cost function (17.3), the deterministic sequential decision making problem can be
stated as the following optimization problem:
J ∗ ( x0 ) = minimize

ut , t=0,...,T −1

subject to

T −1

g T ( x T ) + ∑ gt ( x t , u t ),
t =0

x t +1 = f t ( x t , u t ),
u t ∈ U ( x t ),

t = 0, . . . , T − 1,

t = 0, . . . , T − 1.

(17.4)

The continuous-time counterpart to dynamic programming is the HamiltonJacobi-Bellman (HJB) equation. While
the HJB equation is beyond the scope
of this chapter, we refer interested readers to Bertsekas [12] for a comprehensive
treatment of continuous-time decisionmaking.
1

---

### [PDF p.441 | Book p.439]

sequential decision making and dynamic programming

439

As we will see throughout the remainder of this chapter, the central goal of
dynamic programming is to compute a solution to Problem (17.4) in the form of
an optimal closed-loop control policy:
π ={π0 , . . . , π T −1 },
u∗t =πt∗ ( xt ),

t = 0, . . . , T − 1,

(17.5)

where the policy π denotes a sequence of functions πt mapping any state xt into
a control ut 2 .
In Chapter 3, we were able to derive closed-loop control laws primarily by exploiting strong structural assumptions, such as linear system dynamics, quadratic
cost functions, or special system properties like differential flatness. While these
assumptions yield elegant and computationally efficient solutions, they substantially limit the range of problems that can be addressed. Dynamic programming offers a fundamentally different approach. Rather than relying on restrictive structural properties, it exploits only the sequential nature of the decisionmaking process and the additive structure of the cost function, thereby providing a systematic framework for computing optimal closed-loop policies for a
much broader class of systems, including those with nonlinear dynamics and
non-quadratic costs.
In what follows, we will explore how dynamic programming can be employed
to solve the deterministic decision making problem defined above through the
so-called principle of optimality.

17.1.1

In the deterministic setting considered
here, the system evolution is fully predictable, and closed-loop and openloop optimal solutions therefore coincide. The true advantages of closed-loop
policies emerge mainly in the stochastic setting, which we address in the next
section.
2

The Principle of Optimality

The dynamic programming approach to sequential decision making rests on a
very simple, yet powerful, idea, known as the principle of optimality3 . Despite
its simplicity, this principle is the key that transforms an otherwise intractable
optimization problem into one that can be solved efficiently through recursive
decomposition.
At a high level, the principle of optimality expresses the following insight.
Suppose that a policy is optimal for a given decision making problem. Then, if we
consider any intermediate time and the state reached at that time while following
this policy, the remaining decisions prescribed by the policy must themselves be
optimal for the subproblem that starts from that state. In other words, any tail
segment of an optimal policy must itself be optimal for the corresponding tail
subproblem.
The intuitive justification for this principle is straightforward. If the remaining
decisions after some time were not optimal for the corresponding tail subproblem,
then we could replace them with a better alternative and thereby reduce the total
cost. This would contradict the assumption that the original policy was optimal.
Thus, optimal policies must be composed of optimal solutions to all of their tail
subproblems.
This idea is most easily visualized in shortest-path problems, as illustrated in

Often referred to as Bellman’s principle
of optimality.
3

---

### [PDF p.442 | Book p.440]

440

principles of robot autonomy

Section 17.1.1. If the optimal path from a starting point a to a destination e passes
through an intermediate point b, then the portion of the path from b to e must
itself be optimal among all paths that start at b. Otherwise, a shorter path from b
to e could be substituted, yielding a shorter overall path from a to e.

We now state the principle of optimality formally for deterministic decision
making problems.
Theorem 17.1.2 (Principle of Optimality (Deterministic Case)). Let {u0∗ , u1∗ , . . . , u∗T −1 }
be an optimal control sequence to the deterministic decision making problem defined by
Problem 17.4 with initial condition x0∗ , and let { x0∗ , x1∗ , . . . , x∗T } denote the corresponding
optimal state trajectory. Then, for any time t ∈ {0, . . . , T − 1}, the truncated control
sequence {u∗t , . . . , u∗T −1 } is optimal for the subproblem that starts from state x∗t at time t
and minimizes the tail cost:
T −1

Jtail ( xt , ut , . . . , u T −1 ) = gT ( x T ) + ∑ gi ( xi , ui ),
i =t

subject to the same system dynamics and control constraints, over the horizon t to T.
The principle of optimality suggests that an optimal policy can be constructed
by solving a sequence of smaller subproblems. One may first solve the tail subproblem involving only the final stage, then extend this solution to the tail subproblem involving the last two stages, and continue in this manner until an optimal policy for the entire horizon is obtained. The dynamic programming algorithm is based precisely on this idea: it proceeds backward in time, solving tail
subproblems of increasing length by reusing solutions to shorter tail subproblems.
Example 17.1.1 (Shortest-Path Problem). Consider the deterministic shortest-path
problem shown in Example 17.1.1, where the objective is to find an optimal path
from point b to point f . Suppose that the optimal costs from points c, d, and e to
f are already known.
A brute-force approach would require evaluating all possible paths from b to
f , including:

{b → c → f , b → c → d → f , b → c → d → e → f , b → d → c → f , b → d → f ,
b → d → e → f , b → e → d → c → f , b → e → d → f , b → e → f }.

Figure 17.1: Illustration of the
principle of optimality for a
shortest-path problem. If the
path a → b → e is optimal from
a to e, then the subpath b → e
must be optimal when starting
from b. Adapted from Kirk [70,
Ch. 3].

---

### [PDF p.443 | Book p.441]

sequential decision making and dynamic programming

441

Figure 17.2: By leveraging optimal tail costs, the number of
candidate paths that must be
evaluated when searching from
b to f is dramatically reduced.
Adapted from Kirk [70, Ch. 3].

By exploiting the principle of optimality, we know that any optimal path from b
to f must consist of an immediate step from b to one of its neighboring points (c,
d, or e), followed by an optimal path from that neighboring point to f . Thus, only
three candidate paths need to be evaluated:
b → c → f,

b → d → f,

b → e → f,

where the optimal path can be found by selecting the minimum-cost path among:

{ Jbc + Jc∗f , Jbd + Jd∗ f , Jbe + Je∗f }.
This simple example illustrates the central idea underlying dynamic programming, where optimal tail costs are reused to efficiently construct optimal solutions to larger problems. We now formalize this idea into a systematic algorithm
for solving sequential decision making problems.

17.1.2

The Dynamic Programming Algorithm

The principle of optimality provides a powerful structural property of optimal
solutions, but by itself it does not specify how such solutions should be computed.
Dynamic programming turns this structural insight into a concrete computational
procedure to find optimal control policies.
Rather than attempting to find an optimal control sequence over the entire
horizon at once, dynamic programming proceeds by solving a sequence of smaller
subproblems backward in time. This motivates the introduction of the so-called
cost-to-go function. For each time t ∈ {0, . . . , T } and each state xt , define the optimal cost-to-go Jt∗ ( xt ) as the minimum achievable cost when the system starts
from state xt at time t and evolves optimally until the terminal time T. By definition, the cost-to-go at time T coincides with the terminal cost:
JT∗ ( x T ) = gT ( x T ),

∀xT ∈ X ,

since no further decisions remain to be made after time T.
The principle of optimality implies that the optimal cost-to-go functions satisfy
a recursive relationship, where the cost-to-go at time t can be expressed in terms

---

### [PDF p.444 | Book p.442]

442

principles of robot autonomy

of the stage cost at time t and the cost-to-go at time t + 1:
Jt∗ ( xt ) = min

ut ∈U ( xt )

h

i
gt ( xt , ut ) + Jt∗+1 f t ( xt , ut ) ,

t = 0, . . . , T − 1.

(17.6)

This equation, often referred to as the Bellman equation, expresses the global
optimization problem in terms of a local minimization combined with the optimal
solution of a shorter-horizon problem.
In practice, the dynamic programming algorithm leverages the Bellman equation to compute the optimal cost-to-go functions via a backward-in-time recursion, as summarized in Algorithm 17.1. Starting from the known terminal cost
JT∗ , one computes JT∗ −1 , then JT∗ −2 , and so on, until J0∗ is obtained. At each stage
of this backward recursion, the optimal tail cost is computed for every state in
the state space. The result is a collection of functions { Jt∗ (·)}tT=0 that completely
characterize the optimal performance of the system from any state and time.
Algorithm 17.1: Dynamic Programming (Deterministic)
JT∗ ( x T ) = gT ( x T ), for all x T ∈ X
for t = T − 1 to 0 do h

i
Jt∗ ( xt ) = minut ∈U ( xt ) gt ( xt , ut ) + Jt∗+1 f t ( xt , ut ) ,

for all xt ∈ X

return J0∗ (·), . . . , JT∗ (·)
Once the cost-to-go functions have been computed, the optimal control at each
time step is obtained by minimizing the sum of the immediate cost and the optimal cost-to-go of the resulting next state:
h
i
u∗t = arg min gt ( x∗t , ut ) + Jt∗+1 f t ( x∗t , ut ) .
ut ∈U ( x∗t )

The system is then propagated to the next state x∗t+1 = f t ( x∗t , u∗t ), and the process
is repeated until the terminal time T is reached. Conceptually, the backward
pass computes the optimal cost-to-go functions of every tail subproblem, while
the forward pass uses these functions to compute the actions that realize these
optimal costs.
Although dynamic programming yields an exact solution to the deterministic
decision making problem, its direct application is often limited by computational
considerations. The backward recursion requires evaluating the Bellman equation
for every possible state at every time step, which may be infeasible when the
state space is continuous or very large. Discretization of the state space may
render the algorithm implementable, but even then the computational burden
can grow rapidly with the dimension of the state. These challenges motivate the
development of approximate methods that retain the conceptual framework of
dynamic programming while relaxing its computational demands.
Despite these practical limitations, dynamic programming occupies a central
role in sequential decision making. It provides the canonical solution method

---

### [PDF p.445 | Book p.443]

sequential decision making and dynamic programming

443

for finite-horizon problems, offers a precise interpretation of optimality through
cost-to-go functions, and serves as the conceptual foundation for a wide range of
learning-based control algorithms.
Example 17.1.2 (Grid Navigation). Consider the environment shown in Example 17.1.2, where the objective is to move from point a to point h while incurring
the minimum possible cost. The state x = { a, b, c, d, e, f , g, h} corresponds to the
agent’s current location on the grid, and the available control actions at each state
are encoded by the arrows indicating allowable directions of travel. For example,
at point c the agent may move either right or up, but not left or down. Each
directed edge is associated with a nonnegative traversal cost, as shown in the
figure.

Figure 17.3: A deterministic decision making problem where
the goal is to move from point
a to point h while incurring the
minimal amount of cost. The
path a → d → e → f →
g → h is the optimal path. We
solve this problem by dynamic
programming in Example 17.1.2.
Adapted from Kirk [70, Ch. 3].

We treat point h as a terminal state with zero terminal cost, so that:
JT∗ (h) = 0,
and we allow the agent to remain at h at zero cost once it is reached. The dynamic programming recursion is initialized at this terminal condition and proceeds backward in time, successively computing the optimal cost-to-go for states
that can reach h within an increasing number of steps.
At the first backward step, corresponding to one step from the terminal time,
only states that can transition directly to h are relevant. These are the points e
and g, together with h itself. The optimal costs-to-go are obtained by adding the
immediate transition cost to the terminal cost:
JT∗ −1 (h) = 0 + JT∗ (h) = 0,

u∗T −1 (h) = stay,

JT∗ −1 (e) = 8 + JT∗ (h) = 8,

u∗T −1 (e) = right,

JT∗ −1 ( g) = 2 + JT∗ (h) = 2,

u∗T −1 ( g) = up.

At the next step of the recursion, states such as d and f become relevant, since
they can reach h in two steps. Their optimal costs-to-go are computed by adding

---

### [PDF p.446 | Book p.444]

444

principles of robot autonomy

the immediate cost of moving to e or g and then using the previously computed
one-step tail costs:
JT∗ −2 (d) = 3 + JT∗ −1 (e) = 11,

u∗T −2 (d) = right,

JT∗ −2 ( f ) = 3 + JT∗ −1 ( g) = 5,

u∗T −2 ( f ) = right.

At this point, the cost-to-go values represent the optimal cost of reaching h in at
most two steps from each of the states {d, e, f , g}.
As the recursion continues, additional states enter the computation, and some
states acquire multiple feasible paths to the terminal state. For example, at the
next backward step, state e may either move directly to h or move downward to
f and then proceed optimally from there. The Bellman equation automatically
selects the cheaper of these alternatives:
JT∗ −3 (e) = min{8 + JT∗ −2 (h), 2 + JT∗ −2 ( f )} = 7,

u∗T −3 (e) = down.

Similarly, the other relevant states at this step are updated as follows:
JT∗ −3 ( g) = 2,

u∗T −3 ( g) = up,

JT∗ −3 (d) = 3 + JT∗ −2 (e) = 11,

u∗T −3 (d) = right,

JT∗ −3 ( f ) = 5,

u∗T −3 ( f ) = right,

JT∗ −3 ( a) = 8 + JT∗ −2 (d) = 19,

u∗T −3 ( a) = right,

JT∗ −3 (c) = min{5 + JT∗ −2 (d), 3 + JT∗ −2 ( f )} = 8,

u∗T −3 (c) = right.

At this stage, we see that the goal h is reachable from a in three time steps on
path a → d → e → h, and that we would incur a cost of 19.
Extending the horizon further allows the algorithm to discover lower-cost
paths that take advantage of additional intermediate states. In particular, the
recursion continues one more step to yield:
JT∗ −4 (e) = 7,

u∗T −4 (e) = down,

JT∗ −4 ( g) = 2,

u∗T −4 ( g) = up,

JT∗ −4 (d) = 3 + JT∗ −3 (e) = 10,

u∗T −4 (d) = right,

JT∗ −4 ( f ) = 5,

u∗T −4 ( f ) = right,

JT∗ −4 ( a) = 8 + JT∗ −3 (d) = 19,

u∗T −4 ( a) = right,

JT∗ −4 (c) = min{5 + JT∗ −3 (d), 3 + JT∗ −3 ( f )} = 8,

u∗T −4 (c) = right,

JT∗ −4 (b) = 9 + JT∗ −3 (c) = 17,

u∗T −4 (b) = right.

Finally, extending the horizon one last time allows the algorithm to find the optimal path from the initial state a to the goal state h, corresponding to the path

---

### [PDF p.447 | Book p.445]

sequential decision making and dynamic programming

a → d → e → f → g → h, with total cost 18:
JT∗ −5 (e) = 7,

u∗T −5 (e) = down,

JT∗ −5 ( g) = 2,

u∗T −5 ( g) = up,

JT∗ −5 (d) = 10,

u∗T −5 (d) = right,

JT∗ −5 ( f ) = 5,

u∗T −5 ( f ) = right,

JT∗ −5 ( a) = min{8 + JT∗ −4 (d), 5 + JT∗ −4 (b)} = 18,

u∗T −5 ( a) = right,

JT∗ −5 (c) = min{5 + JT∗ −4 (d), 3 + JT∗ −4 ( f )} = 8,

u∗T −5 (c) = right,

JT∗ −5 (b) = 9 + JT∗ −4 (c) = 17,

u∗T −5 (b) = right.

Several important features of dynamic programming are illustrated by this example. First, the algorithm does not search over complete paths from a to h. Instead,
it incrementally builds optimal solutions by reusing previously computed tail
costs. Second, the algorithm computes optimal costs and controls for all states,
not just the initial state of interest. As a result, once the cost-to-go functions have
been computed, optimal paths can be generated immediately from any starting
point and for any horizon length. For example, starting from point c with a horizon of three steps, the optimal path c → f → g → h and its associated cost of 8
can be read off directly, without any additional computation.

17.2

Decision Making Under Uncertainty: Markov Decision Processes

The deterministic decision making framework developed in Section 17.1 provides
a clean and powerful lens through which sequential decision making problems
can be understood and solved. In realistic robotic systems, however, the environment is never perfectly known, and uncertainty is an intrinsic feature of physical
interaction and perception. Sensor measurements are noisy, actuation is imperfect, and the environment may evolve in ways that cannot be modeled exactly or
anticipated in advance. As a result, the evolution of the system state cannot be
described deterministically, and decision quality must be evaluated in a statistical
sense.
The goal of this section is to extend the deterministic sequential decision making problem in Definition 17.1.1 to explicitly account for such uncertainty. We begin by deriving a stochastic formulation of the sequential decision making problem that incorporates uncertainty into both the system dynamics and the cost
structure, thereby introducing the framework of Markov decision processes (MDPs).
This framework is a cornerstone of modern decision making under uncertainty,
and will serve as a bridge to the learning-based methods developed in Chapter 18
and Chapter 19. We then adapt the principle of optimality and the dynamic programming algorithm to this stochastic setting.

445

---

### [PDF p.448 | Book p.446]

446

principles of robot autonomy

17.2.1

Problem Formulation

We begin by modifying the state transition model in (17.1) to include a stochastic
disturbance:
t = 0, . . . , T − 1,

x t +1 = f t ( x t , u t , wt ) ,

(17.7)

where wt denotes a stochastic disturbance at time t. The disturbance wt is assumed to be drawn from a known conditional probability distribution:
wt ∼ p t ( wt | x t , u t ) .

(17.8)

This assumption implies that the distribution of the next state depends only on
the current state and action, and not on the full history of the system. This conditional independence assumption is an instance of the Markov property4 , which
states that, given the present state and action, the future evolution of the system is independent of the past. Accordingly, the state xt can be interpreted as a
sufficient summary of all past information relevant for future decision making.
The admissible control constraints remain unchanged. At each time step, the
control must satisfy:
u t ∈ U ( x t ),

t = 0, . . . , T − 1,

Which we previously encountered in
Chapter 11 in the context of Bayesian filtering.
4

(17.9)

where U ( xt ) may encode physical limitations, logical constraints, or discrete action choices.
We also allow the instantaneous cost to depend explicitly on the disturbance:
gt : X × U × W → R,

t = 0, . . . , T − 1,

(17.10)

where W denotes the space of possible disturbance values.
Because the system evolution is now stochastic, performance can no longer be
evaluated along a single trajectory. Instead, we measure performance in expectation. Specifically, given a policy π = {π0 , . . . , π T −1 }, we define the associated
expected cost starting from an initial state x0 as:
"
Jπ ( x0 ) = Ew

T −1

#

g T ( x T ) + ∑ g t ( x t , π t ( x t ) , wt ) ,

(17.11)

t =0

where the expectation is taken with respect to the joint distribution of the disturbance sequence {w0 , . . . , wT −1 } induced by the policy π and the stochastic
dynamics (17.7). This formulation corresponds to a risk-neutral objective, where
policies are compared based on their average performance5 .
We can now formally state the stochastic sequential decision making problem.
Definition 17.2.1 (Stochastic Sequential Decision Making Problem). Given the
stochastic dynamics (17.7), the control constraints (17.9), and the expected cost
(17.11), the stochastic sequential decision making problem consists of computing
an optimal policy:
π ∗ = {π0∗ , . . . , π T∗ −1 },

While the expected cost formulation
is the most common in the literature, alternative risk measures—such as
worst-case performance or risk-sensitive
criteria—can also be considered, but are
beyond the scope of this chapter.
5

---

### [PDF p.449 | Book p.447]

sequential decision making and dynamic programming

447

that solves:
"
∗

J ( x0 ) = minimize
π

subject to

Ew

T −1

#

g T ( x T ) + ∑ g t ( x t , π t ( x t ) , wt ) ,
t =0

x t +1 = f t ( x t , u t , wt ) ,

t = 0, . . . , T − 1,

(17.12)

ut = πt ( xt ) ∈ U ( xt ), t = 0, . . . , T − 1.
This formulation is also known as a finite-horizon Markov decision process. It
mirrors the deterministic problem in structure, differing only in the introduction
of random disturbances and the use of expected cost as the performance criterion.
As we will see next, this similarity allows us to extend the principle of optimality
and dynamic programming methods to this stochastic setting6 .

17.2.2

Stochastic Decision Making with Dynamic Programming

As in the deterministic case, the key property that enables efficient solution methods for the stochastic sequential decision making problem is the principle of optimality. In this subsection, we first state the principle of optimality for the stochastic setting, and then show how it leads to a dynamic programming recursion for
computing optimal policies.
Principle of Optimality. In the stochastic setting, the core intuition behind the
principle of optimality—that optimal policies can be constructed by composing
optimal solutions to tail subproblems—remains valid. However, it must be formulated in terms of expected future cost. Because state transitions are random, it
is no longer meaningful to reason in terms of a single “optimal trajectory”. Instead, policies are evaluated by the expected cumulative cost they induce under
the stochastic elements in the system.
The crucial assumption that enables a recursive decomposition is the Markov
property. Specifically, as introduced in Chapter 11, the Markov property ensures
that the future evolution of the system depends only on the current state and
action, and not on the full history leading up to that state. Consequently, the
expected cost incurred from time t onward depends only on xt and the future
actions selected by the policy.
Under this assumption, if a policy is optimal from the initial condition, then
after reaching any intermediate state xt , the remaining portion of that policy must
still be optimal for the tail problem that starts at xt . If this were not the case, the
tail could be replaced by an alternative policy with strictly lower expected cost,
thereby reducing the overall expected cost and contradicting the optimality of the
original policy.
Formally, we can state the principle of optimality for the stochastic decision
making problem as follows:

This problem formulation lies at the
core of several disciplines, including
optimal control, operations research,
robotics, economics, and machine learning.
As a result, it is common to
encounter substantially different notation and terminology across communities, even when describing essentially
the same underlying problem. In this
chapter, we adopt notation that is standard in optimal control. In the next
chapter, we will reintroduce the same
problem using notation that is more
common in the machine learning and reinforcement learning literature. For a
broader discussion of the connections,
overlaps, and distinctions among these
perspectives, we refer the reader to Powell [109].
6

Theorem 17.2.2 (Principle of Optimality (Stochastic Case)). Let π ∗ = {π0∗ , π1∗ , . . . , π T∗ −1 }
be an optimal policy for the stochastic decision making problem defined in Problem 17.12.

---

### [PDF p.450 | Book p.448]

448

principles of robot autonomy

For any time t and any state xt that is reachable under π ∗ , the tail policy {πt∗ , . . . , π T∗ −1 }
is an optimal policy for the tail subproblem that starts at time t from state xt and minimizes the expected cost:
"
#
Jπ ( xt ) = Ew

T −1

g T ( x T ) + ∑ g i ( x i , π i ( x i ) , wi ) .
i =t

As in the deterministic case, this result implies that optimal policies can be
constructed by solving a sequence of nested tail subproblems, with dynamic programming providing a systematic procedure for carrying out this backward construction, as we describe next.
Dynamic Programming. The dynamic programming algorithm for the stochastic
case closely mirrors its deterministic counterpart. It proceeds backward in time,
starting from the terminal cost:
JT∗ ( x T ) = gT ( x T ),

∀xT ∈ X ,

and successively computing the optimal cost-to-go for earlier stages. At each
step, the algorithm evaluates, for every state, the expected cost associated with
each admissible control and selects the minimizing one. Similarly, the cost-to-go
can be expressed recursively, yielding the (stochastic) Bellman equation:


Jt∗ ( xt ) = min Ew gt ( xt , ut , wt ) + Jt∗+1 f t ( xt , ut , wt ) ,
ut ∈U ( xt )

t = 0, . . . , T − 1.

(17.13)
The resulting dynamic programming algorithm is summarized in Algorithm 17.2.
Algorithm 17.2: Dynamic Programming (Stochastic Case)
JT∗ ( x) = gT ( x), for all x ∈ X
for t = T − 1 to 0 do 

Jt∗ ( x) = min Ew gt ( x, u, w) + Jt∗+1 ( f t ( x, u, w)) , for all x ∈ X
u∈U ( x)
∗
return J0 (·), . . . , JT∗ (·)

Once the cost-to-go functions have been computed, an optimal policy is obtained by selecting:


πt∗ ( xt ) = arg min Ew gt ( xt , ut , wt ) + Jt∗+1 f t ( xt , ut , wt ) .

(17.14)

ut ∈U ( xt )

Example 17.2.1 (Inventory Control). Consider a simple inventory control problem
in which the state xt ∈ N denotes the available stock of an item at time t. At each
step, the decision maker chooses how many items to order, ut ∈ N, before facing
a random demand wt ∈ N.
The system dynamics are given by:
xt+1 = max{0, xt + ut − wt },

---

### [PDF p.451 | Book p.449]

sequential decision making and dynamic programming

which captures the fact that demand reduces inventory, restocking increases it,
and inventory cannot go below zero. We impose the constraint:
xt + ut ≤ 2,
so that the inventory capacity is limited to at most two units.
Demand is modeled as a discrete random variable with the following probability distribution:
p(wt = 0) = 0.1,

p(wt = 1) = 0.7,

p(wt = 2) = 0.2.

We consider a finite horizon of T = 3 steps and define the expected cost:
"
Ew

2

∑ ut + ( xt + u t − wt )

#

2

,

t =0

which penalizes both ordering costs and the squared deviation between inventory
and demand.
To solve this problem using dynamic programming, we first identify the state
and control spaces:

X = {0, 1, 2},

U ( xt ) = {0, 1, 2 − xt }.

Following Algorithm 17.2, we initialize the terminal cost-to-go function at time
t = 3 as:
J3∗ ( x3 ) = 0,

∀ x3 ∈ {0, 1, 2},

since no costs are incurred after the final stage. Working backward, we compute
the cost-to-go at time t = 2 by minimizing the expected one-step cost:
h
i
J2∗ (0) = minimize Ew u2 + (u2 − w2 )2 ,
u2 ∈{0,1,2}

= minimize u2 + 0.1u22 + 0.7(u2 − 1)2 + 0.2(u2 − 2)2 = 1.3,
u2 ∈{0,1,2}
h
i
∗
J2 (1) = minimize Ew u2 + (1 + u2 − w2 )2 ,
u2 ∈{0,1}

= minimize u2 + 0.1(1 + u2 )2 + 0.7(u2 )2 + 0.2(u2 − 1)2 = 0.3,
u2 ∈{0,1}
i
h
J2∗ (2) = Ew (2 − w2 )2 = 0.1(2)2 + 0.7(1)2 + 0.2(0)2 = 1.1.
Note that for x2 = 2, the only admissible action is u2 = 0 due to the inventory
capacity constraint, and hence the minimum is achieved at u2 = 0.
From these computations, we directly obtain the optimal actions at time t = 2:
π2∗ (0) = 1,
π2∗ (1) = 0,
π2∗ (2) = 0.

449

---

### [PDF p.452 | Book p.450]

450

principles of robot autonomy

Continuing this process, we compute the cost-to-go at time t = 1:
h
i
J1∗ (0) = minimize Ew u1 + (u1 − w1 )2 + J2∗ (max{0, u1 − w1 }) = 2.5,
u1 ∈{0,1,2}

h
i
J1∗ (1) = minimize Ew u1 + (1 + u1 − w1 )2 + J2∗ (max{0, 1 + u1 − w1 }) = 1.5,
u1 ∈{0,1}

h
i
J1∗ (2) = Ew (2 − w1 )2 + J2∗ (max{0, 2 − w1 }) = 1.68,
with optimal stage actions:
π1∗ (0) = 1,
π1∗ (1) = 0,
π1∗ (2) = 0.
Finally, in the last step:
h
i
J0∗ (0) = minimize Ew u0 + (u0 − w0 )2 + J1∗ (max{0, u0 − w0 }) = 3.7,
u0 ∈{0,1,2}

i
h
J0∗ (1) = minimize Ew u0 + (1 + u0 − w0 )2 + J1∗ (max{0, 1 + u0 − w0 }) = 2.7,
u0 ∈{0,1}

J0∗ (2) = Ew

h

i
(2 − w0 )2 + J1∗ (max{0, 2 − w0 }) = 2.818,

with:
π0∗ (0) = 1,
π0∗ (1) = 0,
π0∗ (2) = 0.
For this example, the optimal policy is time-invariant: order one unit when the
inventory is empty, and order nothing otherwise. This policy balances the risk of
unmet demand against the cost of carrying inventory, and it emerges naturally
from the dynamic programming recursion.

17.3

Limitations of Dynamic Programming

Dynamic programming is a powerful algorithmic framework that underlies a
wide range of methods for solving sequential decision-making problems. However, despite its generality and conceptual elegance, it suffers from several important practical limitations.
First, in its standard form, dynamic programming requires perfect knowledge
of the environment. This includes an accurate model of the system dynamics—
whether deterministic or stochastic—as well as a known cost or reward function.
In many real-world applications, particularly in robotics, this requirement can be
highly restrictive, as physical interactions involving friction, contact dynamics, or
complex nonlinear effects are often difficult to model accurately. Moreover, the
algorithms presented in this chapter assume that the full system state is known
and directly observable, which is often not the case in practice.

---

### [PDF p.453 | Book p.451]

sequential decision making and dynamic programming

A second major limitation of dynamic programming is the so-called curse of dimensionality. The computational and storage requirements of dynamic programming grow exponentially with the dimension of the state space. Concretely, if
the state is n-dimensional and each state variable can take on M discrete values,
then the Bellman equation must be evaluated Mn times at each stage of the algorithm. While this may be tractable for low-dimensional problems, it quickly
becomes infeasible as the dimensionality increases. This issue is especially relevant in robotics, where the state and action spaces can be very high-dimensional
due to the presence of multiple degrees of freedom, sensors, and actuators.
Together, these limitations motivate the development of alternative approaches
that relax some of the assumptions underlying classical dynamic programming.
In particular, they have led to the study of learning-based methods that trade
exact optimality for computational tractability.
In the next chapter, we first introduce reinforcement learning, which can be
viewed as a natural extension of the ideas developed here. At a high level, reinforcement learning may be viewed as a form of approximate dynamic programming,
as it retains the central concepts of value functions, Bellman recursions, and policy improvement, while addressing the key limitations of classical dynamic programming by allowing policies to be learned from interaction rather than computed from a perfectly known model over an explicitly enumerated state space.
For this reason, reinforcement learning provides the most direct next step after
the present chapter.
We then turn to imitation learning, which offers a broader and highly practical framework for robot learning from demonstrations. Rather than learning
solely through trial-and-error interaction with the environment, imitation learning leverages expert behavior to acquire control policies, and has become one of
the most widely used paradigms for training robotic systems in practice. Taken
together, reinforcement learning and imitation learning provide two complementary responses to the limitations of classical dynamic programming, and they will
be the focus of Chapter 18 and Chapter 19, respectively.

17.4

Summary

In this chapter, we introduced a general, optimization-based framework for sequential decision-making that allows us to compute optimal policies for complex
tasks, even under uncertainty. We began in Section 17.1 by framing deterministic
sequential decision-making as a discrete-time optimal control problem, introducing dynamic programming as the primary computational tool for solving such
problems. Grounded in the principle of optimality, dynamic programming allows long-horizon problems to be decomposed into a sequence of simpler, recursively defined subproblems. In Section 17.2, we extended this framework to the
stochastic setting, where uncertainty in system dynamics and outcomes must be
explicitly accounted for. This led to the formulation of Markov decision processes
and the use of dynamic programming to compute policies that optimize expected

451

---

### [PDF p.454 | Book p.452]

452

principles of robot autonomy

performance under known sources of randomness. Finally, in Section 17.3, we
discussed the practical limitations of dynamic programming, most notably the
curse of dimensionality and the reliance on accurate models of the environment.
These challenges motivate the development of learning-based approaches, which
are the focus of the next chapter.
To learn more. For a foundational and comprehensive treatment of dynamic programming and sequential decision-making, Dynamic Programming and Optimal
Control by Bertsekas [12] is an indispensable resource, providing rigorous derivations for both deterministic and stochastic problems. For an introduction to
Markov decision processes with a focus on their role in modern artificial intelligence and robotics, Reinforcement Learning: An Introduction by Sutton and Barto
[143] is the standard reference. A more in-depth mathematical treatment of MDPs
can be found in Markov Decision Processes: Discrete Stochastic Dynamic Programming
by Puterman [110].

17.5

Exercises

The starter code for the exercises provided below is available online through
GitHub. To get started, download the code by running in a terminal window:
git clone https://github.com/StanfordASL/pora-exercises.git

We denote Problems requiring hand-written solutions and coding in Python
with and , respectively.

Problem 1: Shortest Path Through A Grid
Consider the graph shown in Section 17.5, where it is only possible to move to the
right and the numbers associated with each edge represent a cost to traverse that
edge. The decision to be made at each node is whether to go “up” or “down”,
and we can assume the state transitions are deterministic.
For this exercise:
1. Use dynamic programming to find the shortest path from A to B.
2. Consider a generalized version of the shortest path problem in Section 17.5
where the grid has n segments along each side. Find the number of computations required by an exhaustive search algorithm (i.e., the number of routes
that such an algorithm would need to evaluate) and the number of computations required by a DP algorithm (i.e., the number of DP evaluations). For
example, for the n = 3 case shown in Section 17.5, an exhaustive search algorithm requires 20 computations, while the DP algorithm requires only 15.

---

### [PDF p.455 | Book p.453]

sequential decision making and dynamic programming

Figure 17.4: Simple grid for
shortest-path problem.

10
7
6

5
6

5
A

8

10

6

8

9

10

7

5

11

7

8

B

7

10
9

453

9
12
7

6

Problem 2: Machine Maintenance
Suppose we have a machine that is either running or is broken down. If it runs
throughout one week, it makes a gross profit of $100. If it fails during the week,
gross profit is zero. If it is running at the start of the week and we perform
preventive maintenance, the probability that it will fail during the week is 0.4.
If we do not perform maintenance, the probability of failure is 0.7. However,
preventative maintenance will cost $20. When the machine is broken down at
the start of the week, it may either be repaired at a cost of $40, in which case
it will fail during the week with a probability of 0.4, or it may be replaced at a
cost of $150 by a new machine that is guaranteed to run through its first week
of operation. Find the optimal repair, replacement, and maintenance policy that
maximizes total profit over four weeks, assuming a new machine at the start of
the first week (that is guaranteed to run during the first week of operation).

Problem 3: Markovian Drone
In this problem, we will model the task of flying a drone to its destination through
a storm as a Markov Decision Process (MDP), and solve for the optimal policy
using dynamic programming. The world is represented as an n × n grid, so the
state space is:

X := {( x1 , x2 ) ∈ R2 | x1 , x2 ∈ {0, 1, . . . , n − 1}}.
In these coordinates, (0, 0) represents the bottom left corner of the map and (n −
1, n − 1) represents the top right corner of the map. From any location x =
( x1 , x2 ) ∈ X , the drone has five possible controls it can apply:

U := {up, down, left, right, land}.

---

### [PDF p.456 | Book p.454]

454

principles of robot autonomy

The corresponding state changes for each control input are:
• up: ( x1 , x2 ) 7→ ( x1 , x2 + 1)
• down: ( x1 , x2 ) 7→ ( x1 , x2 − 1)
• left: ( x1 , x2 ) 7→ ( x1 − 1, x2 )
• right: ( x1 , x2 ) 7→ ( x1 + 1, x2 )
• land: ( x1 , x2 ) 7→ ( x1 , x2 )
Additionally, there is a storm centered at xeye ∈ X . The storm’s influence is
strongest at its
decays farther from the center according to the equation
center and
ω ( x ) = exp −

∥ x − xeye ∥22
2σ2

. Given its current state x and control input u, the

drone’s next state is determined as follows:
• The control to land is deterministic.
• With probability ω ( x ), the storm will cause the drone to move in a uniformly
random direction (for non-landing controls).
• With probability 1 − ω ( x ), the drone will move in the direction specified by
the control (for non-landing controls).
• If the resulting movement would cause the drone to leave X , then it will not
move at all. For example, if the drone is on the right boundary of the map,
then moving right will do nothing.
The quadrotor’s objective is to reach xgoal ∈ X as quickly as possible, so the
cost function is the indicator function gt ( xt ) = 1 − Ixgoal ( xt ). In other words, the
drone will receive a cost of 1 whenever it is not at xgoal ∈ X , and a cost of 0
at the goal. The drone has limited fuel capacity, so it must reach the goal in at
most T timesteps. If the drone is not at the goal at the end of the horizon, it will
crash and we will incur a cost of 100 to replace the drone, therefore gT ( x T ) =
100(1 − Ixgoal ( x T )).
In the notebook ch17/exercises/markovian _ drone.ipynb, complete the
following exercises:
1. Implement the functions of DroneMDP to compute the optimal cost-to-go values
via dynamic programming (Algorithm 17.2) and extract the optimal policy
using Equation (17.14).
2. Given T = 100, n = 20, σ = 10, xeye = (15, 15), and xgoal = (19, 9), compute
and plot a heatmap of the optimal cost-to-go for t = 0 over the grid X . Then,
using the code provided, simulate the MDP with the optimal policy for T =
100 time steps with the state initialized at x = (0, 19).

---

### [PDF p.457 | Book p.455]

sequential decision making and dynamic programming

References
[12]

D. Bertsekas. Dynamic Programming and Optimal Control. Athena Scientific,
2000.

[70]

D. E. Kirk. Optimal Control Theory: An Introduction. Dover Publications,
2004.

[109]

W. B. Powell. “AI, OR and control theory: A Rosetta Stone for stochastic
optimization”. In: Princeton University. 2012.

[110]

M. Puterman. Markov Decision Processes: Discrete Stochastic Dynamic Programming. Wiley, 2014.

[143]

R. Sutton and A. Barto. Reinforcement learning: An introduction. MIT Press,
2018.

455

---

### [PDF p.458 | Book p.456]

> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]
