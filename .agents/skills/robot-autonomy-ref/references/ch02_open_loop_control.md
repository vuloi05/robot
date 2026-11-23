# Ch 2: Open-Loop Control & Trajectory Optimization

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Part I: Motion Planning & Control
- **Trang sách:** 55–88 | **Trang PDF:** 57–90
- **Độ ưu tiên cho dự án:** `THAM KHẢO`
- **Tóm tắt:** Bài toán điều khiển tối ưu, phương pháp trực tiếp/gián tiếp và hệ phẳng vi phân (differential flatness).

---

### [PDF p.57 | Book p.55]

2
Open-Loop Control & Trajectory Optimization
In Chapter 1, we introduced the state space model as a mathematical formulation
for representing a robot’s dynamics. These models, typically expressed as systems of differential equations, provide a foundational framework that describes
how the state of a robot evolves over time in response to control inputs. In particular, we saw how a state space model can be derived from the robot’s kinematics
and dynamics, providing a compact yet expressive description of its physical motion. In this chapter, we turn to a fundamental question: given a state space model
of the robot, how can we determine the control inputs that will drive it to execute a desired
behavior?
As we will see throughout Chapters 2-4, robots must transform high-level goals
into precise physical actions. This process is often described hierarchically, spanning decision-making, motion planning, trajectory optimization, and control (Chapter 2). Each layer plays a distinct role, yet they remain deeply interconnected.
At the higher level of this hierarchy, decision-making governs what tasks the
robot should perform to fulfill its objectives. It involves reasoning over goals, resources, and constraints, often under uncertainty. In a self-driving car, for example, this may correspond to deciding when to overtake, yield, or reroute. Because
it involves strategic considerations rather than immediate actuation, decisionmaking typically unfolds on the order of seconds to minutes. Ultimately, decisionmaking defines the high-level objectives that guide subsequent layers of the hierarchy.
Once a high-level decision has been made, motion planning determines how
to realize it in the robot’s physical environment. This is typically expressed in
terms of the robot’s configuration space and involves finding a collision-free path
that respects geometric and kinematic constraints. For instance, motion planning
may compute a path for a mobile robot to navigate a cluttered warehouse without
collisions. The timescale of motion planning is often on the order of hundreds of
milliseconds to seconds.
Building on this path, trajectory optimization refines it into a time-parameterized
trajectory that is dynamically feasible and optimized for performance criteria.
This entails solving continuous optimization problems that incorporate dynamics, actuator limits, and objectives such as energy efficiency, comfort, or safety

---

### [PDF p.58 | Book p.56]

56

principles of robot autonomy

Figure 2.1: A hierarchical view
of the relationship between
decision-making, motion planning, trajectory optimization,
and control.

margins. The result is a trajectory specifying both the robot’s states and the control inputs needed to realize them over time, ensuring compatibility with the
robot’s actuation capabilities and dynamic constraints. Trajectory optimization
typically operates on shorter timescales, from tens to hundreds of milliseconds.
Finally, low-level control ensures that the robot faithfully executes the desired
trajectory in the physical world, by converting the trajectory into actuation commands. Controllers must operate at high frequency, applying feedback to correct
deviations caused by disturbances, modeling errors, or sensor noise. Whether
adjusting wheel torques, joint forces, or thrust vectors, control is what closes the
loop between higher-level plans and physical reality.
Together, these layers form the backbone of an autonomous system: decisionmaking provides strategic guidance, motion planning translates that guidance
into feasible paths, trajectory optimization refines those paths into feasible and
optimal trajectories, and control ensures that the robot can follow those trajectories in the real world. In practice, the boundaries between these layers are
often blurred. Trajectory optimization, for instance, may be tightly integrated
with planning or even embedded within control loops, while high-level decisions
may be informed by the lower-level processes. For the purposes of this book, we
will adopt the hierarchical perspective outlined above, while acknowledging that
real-world systems frequently combine or intertwine these processes.
In this chapter, we focus on trajectory optimization as a fundamental tool for
computing trajectories that are both feasible and optimal. While control and
motion planning will be revisited in Chapter 3 and Chapter 4, respectively, our
emphasis in this chapter is on the formulation and solution of the trajectory optimization problem. We begin in Section 2.1 by introducing the trajectory optimization problem and casting it as a continuous optimization problem. Building
on this foundation, Sections 2.2 and 2.3 present two major classes of solution
strategies—indirect methods, which derive optimality conditions for the contin-

---

### [PDF p.59 | Book p.57]

open-loop control & trajectory optimization

uous problem using tools from the calculus of variations, and direct methods,
which discretize and numerically solve the problem as a finite-dimensional nonlinear program. Finally, in Section 2.4, we explore specialized techniques tailored
to certain problem structures, known as differentially flat systems.

2.1

The Optimal Control Problem

Optimal control theory aims to determine control inputs that drive a dynamical
system to satisfy its physical constraints while optimizing a performance criterion. At a high level, formulating an optimal control problem requires three key
components:
• A mathematical model of the system, typically expressed in state space form.
• A description of the physical constraints the system must satisfy.
• A specification of the performance criterion to be optimized.
Mathematical model. As discussed extensively in Chapter 1, the purpose of a
mathematical model is to describe how the system’s state evolves over time in
response to control inputs. Using the notation from Chapter 1, the system dynamics can be expressed as a set of ordinary differential equations:
ẋ(t) = f ( x(t), u(t)) ,

(2.1)

where x(t) ∈ Rn is the state of the system at time t, u(t) ∈ Rm is the control
input, and f : Rn × Rm → Rn defines the state evolution over time. Throughout
this book, we will often refer to x(t) and u(t) as the state and control sequences,
respectively, or equivalently as the state and control trajectories.
Physical constraints. Once we define the system dynamics, the next step is to
specify the physical constraints that the system must satisfy. These constraints
can take several forms, including:
• Initial conditions, which specify the state at the initial time t0 as x(t0 ) = x0 .
• Final conditions, which specify the state at the final time t f as x(t f ) = x f or
x(t f ) ∈ X f , where X f denotes a set of allowable terminal states.
• State constraints, which require that the state remains within an allowable set
X for all times t ∈ [t0 , t f ], that is, x(t) ∈ X .
• Control constraints, which enforce that the control input remains within an allowable set U for all times t ∈ [t0 , t f ], that is, u(t) ∈ U .
Depending on whether the constraints are satisfied or not, we can define the
concept of admissibility for a control history and state trajectory.

57

---

### [PDF p.60 | Book p.58]

58

principles of robot autonomy

Definition 2.1.1 (Admissible State and Control Sequences). A state trajectory x(t)
and a control sequence u(t) are admissible if they satisfy the state and control
constraints at all times, that is:
x(t) ∈ X

and

u(t) ∈ U ,

∀ t ∈ [ t0 , t f ].

Admissibility is a key concept in optimal control, as it restricts the set of realizable trajectories1 .
Performance criterion. The final component of an optimal control problem is the
performance criterion to be optimized. An optimal control is defined as one that
minimizes (or maximizes) this performance criterion. In some cases, the performance criterion may be implicitly defined by the problem statement (e.g., minimizing the time to reach a goal state), whereas in other cases, it must be explicitly
designed (e.g., driving a car in a way that is comfortable for the passengers).
Throughout this book, we will focus on performance criteria that can be expressed as a cost functional2 of the form:
J ( x ( t ), u ( t ), t ) = h ( x ( t f ), t f ) +

Z t

f

t0

g( x(t), u(t), t) dt,

(2.2)

where h : Rn × R → R is the terminal cost and g : Rn × Rm × R → R is the
running cost. The terminal cost h is evaluated at the final time t f and typically
represents a cost associated with the state of the system at that time, such as a
penalty for being far from a desired goal state. The running cost g is integrated
over the time interval [t0 , t f ] and represents the instantaneous cost incurred by
the system at each time step, for example, the cost of energy consumption, or any
other cost associated with the system’s operation. Depending on the problem,
the final time t f may be finite and fixed, finite and free, or infinite3 .

2.1.1

Problem Formulation

As a result, an optimal control problem can be formulated as follows:
Determine an admissible control sequence u∗ (t) such that the system dynamics:
ẋ(t) = f ( x(t), u(t), t),
generate a corresponding admissible state trajectory x∗ (t) that minimizes
the performance criterion:
J ( x ( t ), u ( t ), t ) = h ( x ( t f ), t f ) +

Z t
t0

f

g( x(t), u(t), t) dt,

where u∗ (t) and x∗ (t) are referred to as the optimal control sequence and
optimal state trajectory, respectively.

In practice, this allows numerical methods to focus exclusively on admissible
state and control sequences, rather than
considering all possible solutions.
1

A functional maps functions to real
numbers; intuitively, we might say that a
functional is a “function over functions".
Here, the cost functional maps a state
trajectory and control sequence to a real
number representing the overall cost.
2

In the case of an infinite final time, the
terminal cost h is typically ignored and
set to zero.
3

---

### [PDF p.61 | Book p.59]

open-loop control & trajectory optimization

This problem can be formally posed as the following optimization problem:
minimize

J ( x ( t ), u ( t ), t ),

subject to

ẋ(t) = f ( x(t), u(t), t),

u(t)

(2.3)

x ( t0 ) = x0 ,

x(t f ) = x f ,

u(t) ∈ U ,

x(t) ∈ X ,

t0 < t < t f .

This general formulation serves as the starting point for the optimal control methods developed in the remainder of this book. There are also several important
attributes related to the solution of this problem that are worth highlighting:
1. Existence: A solution to an optimal control problem is not guaranteed to exist;
there may be no control history that is both admissible and optimal.
2. Uniqueness: Even when a solution exists, it may not be unique. Multiple admissible control inputs can yield the same performance. While this can pose
challenges for numerical algorithms, it also provides flexibility in selecting
among equally good solutions depending on the application.
3. Optimality: The objective of optimal control is to find a control sequence that
outperforms all other admissible candidates. Thus, optimal control is interested in global optimality, as opposed to local optimality.
Example 2.1.1 (Autonomous Racing Optimal Control). Consider an autonomous
racing scenario in which the goal is to complete a lap of a known course in the
shortest possible time. We can formulate this as a finite-horizon optimal control
problem, where the objective is to minimize the final time t f required to reach
a designated goal position ( xgoal , ygoal ), subject to the constraint that the vehicle
must remain on the track at all times. Let X denote the set of admissible states
that correspond to positions on the course.
Suppose the vehicle is modeled using the simple kinematic car model from Equation (1.29), with state x = [ x, y, θ ]⊤ representing position and heading, and control inputs u = [v, ϕ]⊤ representing forward speed and steering angle, respectively. The resulting optimal control problem is:
minimize

tf ,

subject to

ẋ = v cos θ,

ẏ = v sin θ,

x ∈ Xcourse ,

u ∈ U,

x ( t0 ) = x0 ,

( x (t f ), y(t f )) = ( xgoal , ygoal ).

v ( t ), ϕ ( t )

θ̇ =

v
tan ϕ,
L

In this formulation, the cost depends only on the final time and not directly on
the state or control at intermediate points. As a result, the time-optimal solution
( x(t), u(t)) will lie on the boundaries of the admissible control and state sets.
In practice, this means the vehicle will operate at full throttle and steer at the
physical limits to cut the lap time, a strategy that achieves optimality mathematically—but may not make for a smooth or comfortable ride.

59

---

### [PDF p.62 | Book p.60]

60

principles of robot autonomy

Throughout this book, we will see that the solution to the optimal control
problem can take different forms, depending on whether and how it incorporates
feedback from the current state of the system. At the most fundamental level, we
distinguish between open-loop and closed-loop control. While closed-loop control
will be the focus of Chapter 3, this chapter addresses open-loop control.

Open-loop control. If the optimal control is computed purely as a function of time
for a given initial state,
u∗ (t) = ℓ( x(t0 ), t),

(2.4)

it is said to be in open-loop form. In the context of trajectory optimization, restricting the focus to open-loop strategies is natural, as they balance computational
efficiency—computing open-loop sequences is faster than computing closed-loop
policies—with effectiveness, since robustness can be endowed through closedloop tracking or by re-optimizing the trajectory in a receding-horizon fashion, as
in Model Predictive Control4 .
Having introduced the optimal control problem, we now turn to methods for
computing optimal open-loop solutions. Fundamentally, Problem (2.3) is an
infinite-dimensional optimization problem, where the optimization variables are
functions of time. In practice, solution methods must rely on discretization
strategies, thereby approximating the infinite-dimensional problem with a finitedimensional one. Different discretization approaches give rise to distinct families
of methods.
Broadly speaking, two main classes of methods exist: indirect methods and
direct methods. Indirect methods follow an “optimize-then-discretize” paradigm:
they first derive necessary conditions for optimality—typically in the form of
boundary-value problems involving adjoint variables—and then apply numerical
techniques to solve these conditions. In contrast, direct methods take a “discretizethen-optimize” approach: the state and control sequences are parameterized using finite-dimensional representations, and the resulting finite-dimensional optimization problem is solved numerically.
Beyond these two general classes, some systems admit further structural simplifications. In particular, differentially flat systems allow trajectories to be described in terms of a small set of variables that fully capture the system’s evolution5 . This property enables efficient trajectory generation and optimization,
making these systems especially relevant in mobile robotics and aerospace applications.
The remainder of this chapter examines these three classes of methods in detail: indirect methods in Section 2.2, direct methods in Section 2.3, and trajectory
optimization for differentially flat systems in Section 2.4.

4

Discussed further in Chapter 3.

These variables are commonly known
as flat outputs.
5

---

### [PDF p.63 | Book p.61]

open-loop control & trajectory optimization

2.2

Indirect Methods

Indirect methods provide a principled framework for solving optimal control
problems by drawing on ideas from calculus of variations (CoV)6 . For a comprehensive treatment of the calculus of variations and its applications in optimal
control theory, we refer the reader to Kirk [70]. At their core, indirect methods
rely on the derivation of necessary optimality conditions (NOCs) that any solution must satisfy and then leverage numerical techniques to compute solutions
consistent with these conditions. In this way, the NOCs serve as the bridge between the continuous-time formulation of an optimal control problem and its
numerical resolution.
Before turning to the derivation of such conditions for infinite-dimensional optimization problems, let us first review key concepts from finite-dimensional optimization, which will serve as a foundation for the discussion ahead.

2.2.1

61

Calculus of variations extends the principles of classical calculus from functions to functionals. The central idea
is to study how small perturbations—
called variations—of a candidate function
influence the value of the functional. By
analyzing the first- and higher-order effects of these variations, one can derive
necessary conditions for optimality.
6

NOCs for Unconstrained Nonlinear Optimization Problems

Consider the following finite-dimensional optimization problem:
minimize
n
x ∈R

f ( x ),

(2.5)

where f : Rn → R is assumed continuously differentiable, i.e., f ∈ C1 . We wish
to identify the NOCs that any minimizer—local or global—must satisfy.
The key intuition is that at a local minimizer, no infinitesimal perturbation
of the decision variable should decrease the objective. Formally, this requires
analyzing how f changes under small variations around a candidate minimizer
x∗ .
First-order necessary condition. Let x∗ ∈ Rn be a local minimizer. If f ∈ C1 , we
can use gradients and Taylor series expansions to characterize the behavior of f
near x∗ . For a small perturbation ∆x, the cost variation is, up to first order:
f ( x∗ + ∆x ) − f ( x∗ ) ≈ ∇ f ( x∗ )⊤ ∆x.
If x∗ is a local minimizer, then for sufficiently small ∆x, the first-order term must
be non-negative7 :
n
∂ f ( x∗ )
∆xi ≥ 0.
∇ f ( x∗ )⊤ ∆x = ∑
∂xi
i =1
In particular, by taking ∆x to be positive and negative multiples of the coordinate
unit vectors, that is, vectors having all components equal to zero except for one
component equal to one, we obtain simultaneously:
∂ f ( x∗ )
≥0
∂xi

and

∂ f ( x∗ )
≤ 0,
∂xi

i = 1, . . . , n,

which forces the condition:
∂ f ( x∗ )
= 0,
∂xi

i = 1, . . . , n,

This is because, if we were to decrease
the cost by perturbing x∗ by ∆x, then x∗
would not be a local minimizer.
7

---

### [PDF p.64 | Book p.62]

62

principles of robot autonomy

or, more compactly:

∇ f ( x∗ ) = 0.
Thus, any local minimizer x∗ must be a stationary point of f .
Second-order necessary condition. Assuming f ∈ C2 , consider again the Taylor
expansion of f around a local minimizer x∗ , this time up to second order:
1
f ( x∗ + ∆x ) − f ( x∗ ) ≈ ∇ f ( x∗ )⊤ ∆x + ∆x ⊤ ∇2 f ( x∗ )∆x.
2
For x∗ to be a local minimizer, the second-order variation must be nonnegative
for all sufficiently small ∆x, that is:
1
∇ f ( x∗ )⊤ ∆x + ∆x ⊤ ∇2 f ( x∗ )∆x ≥ 0.
2
Using the first-order condition ∇ f ( x∗ ) = 0, the linear term vanishes, leaving:
∆x ⊤ ∇2 f ( x∗ )∆x ≥ 0.
Thus, the Hessian ∇2 f ( x∗ ) must be positive semidefinite at any local minimizer.
Theorem 2.2.1 (Necessary Conditions for Unconstrained Local Minimizers). Let
x∗ be a local minimizer of f : Rn → R. If f ∈ C1 in an open set containing x∗ , then:

∇ f ( x∗ ) = 0 (first-order NOC).

(2.6)

If, in addition, f ∈ C2 , then:

∇2 f ( x∗ ) ⪰ 0 (second-order NOC).

2.2.2

(2.7)

NOCs for Constrained Nonlinear Optimization Problems

Having introduced the NOCs for unconstrained problems, this section extends
the discussion to optimization problems subject to constraints. The definition
of optimality conditions in the constrained setting requires the introduction of
auxiliary variables, known as Lagrange multipliers. These variables are associated
with the constraints and facilitate the characterization of optimal solutions while
providing insights into the sensitivity of the optimal cost with respect to perturbations in the constraints. In this section, we limit our discussion on the theory of
Lagrange multipliers to the case of equality constrained optimization. For a comprehensive treatment of optimality conditions in finite-dimensional optimization,
the reader is referred to Bertsekas [13].
Consider the following constrained optimization problem:
minimize
n

f ( x ),

subject to

hi ( x) = 0,

x ∈R

(2.8)
i = 1, . . . , m,

where f : Rn → R and hi : Rn → R are continuously differentiable.

---

### [PDF p.65 | Book p.63]

open-loop control & trajectory optimization

63

For compactness, define the constraint function h : Rn → Rm as:
h( x) = (h1 ( x), . . . , hm ( x))⊤ ,

(2.9)

so that the constraints can be written simply as h( x) = 0.
The Lagrange multiplier theorem for equality-constrained optimization states
that, if x∗ is a local minimizer, then there exist scalars λ1∗ , . . . , λ∗m , called Lagrange
multipliers, such that:
m

∇ f ( x∗ ) + ∑ λi∗ ∇hi ( x∗ ) = 0.

(2.10)

i =1

To interpret this condition, observe that the cost gradient ∇ f ( x∗ ) must be orthogonal to the subspace of first-order feasible variations:
V ( x∗ ) := {∆x | ∇ hi ( x∗ )⊤ ∆x = 0,

i = 1, . . . , m}.

This subspace consists of all variations ∆x that preserve feasibility to first order 8 .
Thus, condition (2.10) ensures that the first-order cost variation ∇ f ( x∗ )⊤ ∆x = 0
for all ∆x ∈ V ( x∗ ). This statement is analogous to the ∇ f ( x∗ ) = 0 condition of
unconstrained optimization.
Formally, the necessary conditions for equality constrained optimality are summarized as follows:
Theorem 2.2.2 (Lagrange Multiplier Theorem — Necessary Conditions for Equality Constrained Local Minimizers). Let x∗ be a local minimizer of f : Rn → R subject
to the equality constraints hi ( x) = 0, i = 1, . . . , m, and assume the constraint gradients ∇ h1 ( x∗ ), . . . , ∇ hm ( x∗ ) are linearly independent. Then there exists a unique vector
[λ1∗ , . . . , λ∗m ]⊤ , called the Lagrange multiplier vector, such that:
m

∇ f ( x∗ ) + ∑ λi∗ ∇hi ( x∗ ) = 0.

(2.11)

i =1

It is often convenient to express these conditions using the Lagrangian function
L : Rn+m → R defined as:
m

L( x, λ) := f ( x) + ∑ λi hi ( x).

(2.12)

i =1

The first-order NOCs for a local minimum x∗ then take the compact form:

∇ x L( x∗ , λ∗ ) = 0,
∇λ L( x∗ , λ∗ ) = 0,

(2.13)

where ∇ x L and ∇λ L denote the gradients with respect to x and λ, respectively,
and where the system in (2.13) consists of n + m equations in n + m unknowns—
namely, the n components of x∗ and the m components of λ∗ .
In practice, optimality conditions serve as a powerful tool to filter candidate
solutions for global or local minima and often form the foundation of numerical
optimization algorithms. For instance, in the unconstrained case of Problem (2.5),

That is, variations for which x = x∗ +
∆x satisfies h( x) = 0 to first order.

8

---

### [PDF p.66 | Book p.64]

64

principles of robot autonomy

one might (i) find all stationary points by solving ∇ f ( x) = 0, and (ii) apply
the second-order test by checking ∇2 f ( x) ⪰ 0 at each candidate. This same
philosophy extends naturally to infinite-dimensional optimal control problems,
where any candidate solution must satisfy the corresponding NOCs. However,
as we move to infinite-dimensional problems, the nature of the NOCs changes
significantly: rather than yielding algebraic equations as in the finite-dimensional
case, the NOCs for optimal control take the form of differential equations.

2.2.3

Pontryagin’s Minimum Principle

Extending the concept of necessary optimality conditions to infinite-dimensional
problems leads to Pontryagin’s Minimum Principle (PMP), a cornerstone of optimal control theory. Specifically, the PMP generalizes the finite-dimensional NOCs
to the infinite-dimensional setting.
Consider the problem of finding an admissible control u∗ (t) ∈ U that drives
the system:
ẋ(t) = f ( x(t), u(t), t),
(2.14)
along a trajectory that minimizes the cost functional:
J ( x ( t ), u ( t ), t ) = h ( x ( t f ), t f ) +

Z t
t0

f

g( x(t), u(t), t) dt.

To derive the NOCs, we define the Hamiltonian, the analog of the Lagrangian
in finite-dimensional optimization:
H ( x(t), u(t), p(t), t) := g( x(t), u(t), t) + p(t)⊤ f ( x(t), u(t), t),

(2.15)

where p(t) ∈ Rn is the costate9 vector.
Similarly to the finite-dimensional case, where necessary conditions for optimality are derived by considering the cost increment ∆ f = f ( x + ∆x) − f ( x) in
response to a perturbation ∆x, here we analyze the increment ∆J under variations
around a candidate function.
Theorem 2.2.3 (Pontryagin’s Minimum Principle; for a comprehensive treatment,
we refer the reader to Chapter 5 in Kirk [70]). Let u∗ (t) be an optimal control with
associated state trajectory x(t) for the system in (2.14) over [t0 , t f ]. Then there exists a
costate vector p∗ (t) such that, for all t ∈ [t0 , t f ], the following conditions hold:
∂H ∗
( x ( t ), u ∗ ( t ), p ∗ ( t ), t ),
∂p
∂H ∗
ṗ∗ (t) = −
( x ( t ), u ∗ ( t ), p ∗ ( t ), t ),
∂x
u∗ (t) = arg min H ( x∗ (t), u, p∗ (t), t),
ẋ∗ (t) =

(2.16)

u∈U

along with the boundary conditions:
 
⊤

∂h ∗
∗
x (t f ), t f − p (t f ) δx f
∂x


∂h  ∗
∗
∗
∗
+ H ( x ( t f ), u ( t f ), p ( t f ), t f ) +
x ( t f ), t f
δt f = 0,
∂t

(2.17)

The term costate highlights that there
is one costate associated with each state
variable, analogous to Lagrange multipliers in finite-dimensional optimization.
9

---

### [PDF p.67 | Book p.65]

open-loop control & trajectory optimization

where δx f and δt f denote the variations of the final state and time, respectively 10 .
Equations (2.16) constitute the necessary conditions for optimality. They form
a system of 2n first-order differential equations—n for the state and n for the
costate—together with m algebraic equations defining the control input. Solving
these equations produces 2n constants of integration. Half of these constants are
determined by the initial conditions x∗ (t0 ) = x0 . The remaining n (or n + 1, if the
final time is free) are specified by the boundary conditions in Equation (2.17). This
results in a two-point boundary value problem, which may be solved analytically
in special cases, or numerically using methods such as shooting or collocation11 .
In practice, once the initial state is fixed, the boundary conditions are obtained
by substituting the appropriate assumptions into Equation (2.17). Common cases
include:
Fixed final time and fixed final state. If both t f and x(t f ) are fixed, then δt f = 0
and δx f = 0, leaving the sole boundary condition:
x∗ (t f ) = x f .
Fixed final time and free final state. If t f is fixed but x(t f ) is free, then δt f = 0
while δx f is arbitrary. Hence, the boundary condition is:

∂h  ∗
x (t f ), t f − p∗ (t f ) = 0.
∂x
Free final time and fixed final state. If x(t f ) is fixed but t f is free, then δx f = 0
while δt f is arbitrary. Thus, the boundary condition is:
H ( x ∗ ( t f ), u ∗ ( t f ), p ∗ ( t f ), t f ) +

∂h ∗
( x (t f ), t f ) = 0.
∂t

Free final time and free final state. If both x(t f ) and t f are free, then δx f and δt f
are arbitrary, and both coefficients in Equation (2.17) must be set to zero. That is:
∂h ∗
( x (t f ), t f ) − p∗ (t f ) = 0,
∂x

(n equations)

H ( x ∗ ( t f ), u ∗ ( t f ), p ∗ ( t f ), t f ) +

∂h ∗
( x (t f ), t f ) = 0,
∂t

(1 equation).

While these four cases cover many problems of practical interest, more general
boundary conditions can be found in Kirk [70].

2.2.4

Solving a Two-Point Boundary Value Problem

Finding solutions that satisfy the necessary optimality conditions in Equation (2.16)
is a nontrivial task, as these must simultaneously satisfy a system of 2n differential equations together with boundary conditions imposed at both t0 and t f . This
type of problem, where conditions are specified at two distinct points in time, is
known as a two-point boundary value problem (TPBVP).

65

As we will discuss in the remainder
of this section, the boundary conditions
in Equation (2.17) depend on whether
the final state and time are fixed (i.e.,
δx f = 0 or δt f = 0) or free (i.e., δx f or
δt f are arbitrary).
10

J. Hertling.
“Numerical Methods
for Two-Point Boundary Value Problems
(Herbert B. Keller)”. In: SIAM Review
12.2 (1970), pp. 313–315
11

---

### [PDF p.68 | Book p.66]

66

principles of robot autonomy

Over the years, a number of numerical procedures have been developed for
solving TPBVPs. Two broad classes of approaches are commonly used:
• Shooting methods, which reformulate the TPBVP as an initial value problem
by guessing the unknown boundary conditions (e.g., the initial costate), simulating the system forward, and then iteratively adjusting the guess until the
terminal boundary conditions are satisfied. Although conceptually straightforward, shooting methods may suffer from numerical instability, especially for
long time horizons.
• Collocation methods, whereby the solution is approximated by a parametric
function with unknown parameters at a set of discrete points (called collocation points). These methods turn the TPBVP into a large system of nonlinear
algebraic equations that can be solved using computational techniques. Collocation methods are robust and widely used in practice because they avoid the
instability issues of shooting methods.
Modern scientific computing environments provide high-level implementations
of these ideas. For example, the scikits.bvp_solver package in Python or the
function bvp4c in MATLAB implement numerical algorithms for solving TPBVPs
with relatively little effort from the user.
Most solvers assume that the system of necessary conditions in Equation (2.16),
along with its boundary conditions, can be expressed in the standard form:
ż = g(z, t),

l (z(t0 ), z(t f )) = 0,

(2.18)

where z(t) collects the unknown functions (such as states and costates), g encodes
their dynamics, and l encodes the two-point boundary constraints.
To illustrate how TPBVPs can be solved in practice, consider the toy dynamics:
#
# "
"
z2 ( t )
ż1 (t)
,
=
ż(t) =
− z1 ( t )
ż2 (t)
with boundary conditions z1 (t0 ) = 0 and z1 (t f ) = −2. The boundary conditions
can equivalently be expressed in standard form as:
"
#
z1 ( t0 )
l (z(t0 ), z(t f )) =
= 0.
z1 ( t f ) + 2
In Python, the system dynamics g(z, t) and boundary conditions l (z(t0 ), z(t f ))
can be passed directly to solve_bvp as shown in Algorithm 5.
Many optimal control problems can, in fact, be cast into the standard TPBVP
form in Equation (2.18) and solved directly with off-the-shelf BVP solvers such
as solve _ bvp, sometimes after simple reformulations. Common cases include
problems with conditions at special points, such as free-end problems, switching
points, interface points, or discontinuities. Example 2.2.1 illustrates these ideas in
the context of a free-final-time problem.

---

### [PDF p.69 | Book p.67]

open-loop control & trajectory optimization

Solving a TPBVP with solve_bvp
from scipy.integrate import solve_bvp
import numpy as np
# Dynamics: |$\dot{z} = g(z,t)$|
def g(t, z):
return np.vstack((z[1], -z[0]))
# Boundary conditions: |$l(z(t_0), z(t_f))=0$|
def l(z0, zf):
return np.array([z0[0], zf[0] + 2])
# Time mesh and initial guess for |$z(t)$|
t_mesh = np.linspace(0, 4, 5)
z_guess = np.zeros((2, t_mesh.size))
# Solve TPBVP
sol = solve_bvp(g, l, t_mesh, z_guess)
z_sol = sol.sol(np.linspace(0, 4, 100))

Algorithm 5: Example usage of solve_bvp for a TPBVP in standard form. The
code for this example is available in the repository github.com/StanfordASL/por
a-exercises in the notebook ch02/tpbvp.ipynb.
Example 2.2.1 (Free Final Time Optimal Control Problem; see Example 6.1 in
How [54]). Consider the double integrator system:
ẍ = u,
where x ∈ R is the state and u ∈ R is the control input. The control objective is
to find a trajectory that minimizes the cost:
J ( x, u) =

1 2
αt +
2 f

Z t
0

f

1 2
βu (t)dt,
2

and satisfies the boundary conditions:
x (0) = 10,

ẋ (0) = 0,

x (t f ) = 0,

ẋ (t f ) = 0.

This is a free final time problem with fixed boundary conditions on the state.
The cost penalizes both the duration of the maneuver (through the αt2f term) and
the control effort (through the integral of u2 ), with the trade-off governed by the
weights α and β.
We can equivalently express the double integrator dynamics as a first-order
system of differential equations by setting x1 = x and x2 = ẋ:
ẋ1 = x2 ,

ẋ2 = u,

67

---

### [PDF p.70 | Book p.68]

68

principles of robot autonomy

so that the state vector is x = [ x1 , x2 ]⊤ and the boundary conditions become:
x1 (0) = 10,

x2 (0) = 0,

x1 (t f ) = 0,

x2 (t f ) = 0.

The Hamiltonian is given by:
H=

1 2
βu + p1 x2 + p2 u,
2

where p1 and p2 are the costate variables. Next, we construct the NOCs from
Equation (2.16) by taking the partial derivatives of H with respect to p, x, and u:
ẋ1∗ = x2∗ ,
ẋ2∗ = u∗ ,
ṗ1∗ = 0,
ṗ2∗ = − p1∗ ,
0 = βu∗ + p2∗ .
Thus, from the last condition, the optimal control satisfies:
1
u∗ = − p2∗ .
β
Since this is a free-final-time problem with fixed terminal state, the boundary
conditions for the NOCs are given by:
x1∗ (0) = 10,
x2∗ (0) = 0,
x1∗ (t f ) = 0,
x2∗ (t f ) = 0,
1 ∗
βu (t f )2 + p1∗ (t f ) x2∗ (t f ) + p2∗ (t f )u∗ (t f ) + αt f = 0.
2
However, the necessary conditions obtained above do not immediately match the
“standard” form required by numerical TPBVP solvers in Equation (2.18), which
assumes fixed final time. To cast the problem into standard form, one can apply
the time-scaling strategy. First, the time horizon is rescaled to the fixed interval
[0, 1] by using the scaled time variable τ = t/t f . Next, the derivatives must be
adjusted according to the new time variable. By the chain rule, differentiation
∂(τt )

∂ :
= ∂t∂ ∂τ f = ∂t∂ t f . Finally,
with respect to τ introduces a scaling factor, that is, ∂τ
the final time t f is replaced by an auxiliary state variable r with trivial dynamics
ṙ = 0. This results in a TPBVP with fixed final time, namely equal to 1, and an
additional state variable r that encodes the original final time t f .
For this example, the time-scaled cost becomes:

J ( x, u, r ) =

1 2
αr +
2

Z 1
0

1
βru2 (τ )dτ,
2

---

### [PDF p.71 | Book p.69]

open-loop control & trajectory optimization

with corresponding Hamiltonian:
H=

1
βru2 + p1 rx2 + p2 ru.
2

As a result, the necessary conditions for optimality become:
ẋ1∗ = r ∗ x2∗ ,
ẋ2∗ = r ∗ u∗ ,
ṗ1∗ = 0,
ṗ2∗ = −r ∗ p1∗ ,
ṙ ∗ = 0,
0 = βr ∗ u∗ + r ∗ p2∗ ,
with boundary conditions:
x1∗ (0) = 10,
x2∗ (0) = 0,
x1∗ (1) = 0,
x2∗ (1) = 0,
1
αr ∗ + βr ∗ u∗ (1)2 + r ∗ p1∗ (1) x2∗ (1) + r ∗ p2∗ (1)u∗ (1) = 0.
2
After this reformulation, the problem adheres to the standard form and can be
solved numerically.
For a systematic treatment of how nonstandard boundary value problems can
be reformulated into standard form suitable for general-purpose solvers, see
Ascher and Russell [7]. For a practical implementation of TPBVP solvers for
free-final time optimal control problems, we refer the reader to the notebook
ch02/free_final_time_optimal_control.ipynb in the repository
github.com/StanfordASL/pora-exercises.

2.3

Direct Methods

So far, we introduced indirect methods, which involve deriving the necessary
optimality conditions of the continuous-time optimal control problem and then
discretizing them to numerically solve the resulting two-point boundary value
problem. While indirect methods provide deep theoretical insights, they can be
challenging to apply in practice due to the difficulty of solving boundary value
problems, particularly for complex nonlinear dynamics or large-scale systems.
Direct methods take the opposite approach. Rather than deriving the optimality conditions analytically, the problem is discretized first. This reduces the
continuous-time optimal control problem to a finite-dimensional nonlinear optimization problem, which can then be solved using general-purpose numerical
optimization algorithms.

69

---

### [PDF p.72 | Book p.70]

70

principles of robot autonomy

The process of converting the continuous-time optimal control problem into
a discretized form amenable to numerical optimization is known as transcription.
While there exist many different transcription methods, a simple and widely used
approach is the forward Euler discretization. This method selects a discretization
0 = t0 < t1 < . . . < t N = t f of the time interval [0, t f ] and approximates the state
and control sequences assuming a zero-order hold on both the states and control
inputs, meaning that both the state and the control input are constant over each
time interval [ti , ti+1 ). The system dynamics are then integrated forward using
Euler integration:
x i +1 ≈ x i + h i f ( x i , u i ),

h i = t i +1 − t i .

(2.19)

Direct methods are typically grouped into two main families:
• State and control parameterization methods (also known as direct collocation methods): here, both the control inputs and the state trajectories are discretized,
and the dynamics are introduced explicitly as algebraic constraints linking the
state and control variables at each discretization point (e.g., trapezoidal and
Hermite-Simpson collocation, Gauss-Lobatto methods, etc.).
• Control parameterization methods (also known as direct shooting methods): in this
approach, only the control inputs are discretized, and the state trajectories are
obtained by numerically integrating the system dynamics forward in time. As
a result, the optimization variables are solely the discretized controls, while
the states are implicitly defined by the integration of the dynamics (e.g., using
single or multiple shooting techniques).
In what follows, we illustrate the fundamental concepts of both families of
methods through a concrete example.
Example 2.3.1 (Zermelo’s Problem - Continuous-time problem). Consider the
problem of steering a boat from a point (0, 0) to a point ( M, ℓ) in a river with
a current. The boat can be controlled by adjusting its direction and its speed is
constant. The dynamics of the boat are described by the following differential
equations:
ẋ (t) = v cos(u(t)) + flow(y(t)),
ẏ(t) = v sin(u(t)),

t ∈ [0, t f ],

t ∈ [0, t f ],

where ( x (t), y(t)) is the position of the boat with x defining the coordinate along
the river and y the coordinate across the river, u(t) is the control input (the direction of the boat), and v is the constant speed of the boat. For simplicity, assume
that the river flow is described by an arbitrary function acting in the x-direction,
with its intensity depending on the position y(t), namely flow(y(t)).
The objective is to minimize the control effort over time, which can be formu-

---

### [PDF p.73 | Book p.71]

open-loop control & trajectory optimization

lated as an optimal control problem:
Z t

minimize
u(t)

f

0

u(t)2 dt,

ẋ (t) = v cos(u(t)) + flow(y(t)),

subject to

ẏ(t) = v sin(u(t)),

t ∈ [0, t f ],

t ∈ [0, t f ],

( x (0), y(0)) = (0, 0),


x (t f ), y(t f ) = ( M, ℓ),
|u(t)| ≤ umax ,

2.3.1

t ∈ [0, t f ].

Direct Collocation Methods

Consider the Problem introduced in Example 2.3.1. Applying a state and control parametrization, that is a collocation method, leads to the following finitedimensional nonlinear program, equivalently described in Algorithm 6:
N −1

minimize
( x,y,u)

subject to

∑ hi u2i ,

i =0

xi+1 = xi + hi (v cos(ui ) + flow(yi )) ,
yi+1 = yi + hi v sin(ui ),

i = 0, . . . , N − 1,

i = 0, . . . , N − 1,

( x0 , y0 ) = (0, 0),
( x N , y N ) = ( M, ℓ),
|ui | ≤ umax ,

i = 0, . . . , N − 1.

In this formulation, both the state and control trajectories are discretized and
treated as decision variables. The system dynamics are not enforced through
numerical integration, but rather as algebraic equality constraints linking consecutive discretization points.

2.3.2

Direct Shooting Methods

Many of the concepts introduced for state and control parametrization carry over
to control parametrization methods, with a key distinction in how the dynamics are handled. In control parametrization (shooting) methods, the optimization
variables consist only of the control inputs at each discretization point. The state
trajectory is not explicitly optimized but is instead computed recursively by forward simulation of the system dynamics. In other words, a candidate sequence
of controls uniquely determines the corresponding states, which are then used to
evaluate the cost and any state constraints.
Concretely, let us revisit Zermelo’s problem from Example 2.3.1, this time
using a shooting method transcription. In this formulation, the control inputs
{ui }iN=−0 1 are treated as the optimization variables, while the states {( xi , yi )}iN=−0 1
are computed recursively from the dynamics.

71

---

### [PDF p.74 | Book p.72]

72

principles of robot autonomy

Collocation Formulation of Zermelo’s Problem
# Decision variables: |$(x_i, y_i, u_i), \; i=0,\dots,N$|
get_x = lambda z: z[:N + 1]
get_y = lambda z: z[N + 1:-N]
get_u = lambda z: z[-N:]
get_z = lambda x, y, u: np.concatenate([x, y, u])
# Cost: |$\sum_{i=0}^{N-1} h_i u_i^2$|
cost = lambda z: np.sum(h * np.square(get_u(z)))
def constraints(z):
x, y, u = get_x(z), get_y(z), get_u(z)
constraints = []
for i in range(N):
# |$x_{i+1} = x_i + h_i \left(v \cos(u_i) + \text{flow}(y_i)\right)$|
constraints.append(x[i+1] - x[i] - h*(v*np.cos(u[i])
+ flow(y[i])))
_
_
# |$y {i+1} = y i + h_i v \sin(u_i)$|
constraints.append(y[i+1] - y[i] - h*v*np.sin(u[i]))
# Boundary conditions: |$(x_0, y_0) = (0,0), \; (x_N, y_N) = (M, \ell)$|
constraints.extend([x[0], y[0], x[N] - M, y[N] - l])
return np.array(constraints)
# State bounds
x_lower = np.zeros(N + 1)
x_upper = M * np.ones(N + 1)
y_lower = np.zeros(N + 1)
y_upper = l * np.ones(N + 1)
# Control bounds: |$|u_i| \leq u_{\text{max}}$|;
u_lower = -u_max * np.ones(N) # control constraint
u_upper = u_max * np.ones(N)

# control constraint

bounds = Bounds(
get_z(x_lower, y_lower, u_lower),
get_z(x_upper, y_upper, u_upper))
# Solve the NLP
result = minimize(cost, z0, bounds=bounds,
constraints={'type': 'eq', 'fun': constraints})

Algorithm 6: Direct collocation approach to Zermelo’s problem using forward
Euler discretization. The code for this example is available in the repository
github.com/StanfordASL/pora-exercises in the notebook ch02/zermelos_prob
lem.ipynb.

---

### [PDF p.75 | Book p.73]

open-loop control & trajectory optimization

73

The resulting finite-dimensional optimization problem is:
N −1

minimize
u

subject to

∑ hi u2i ,

i =0

( x N , y N ) = ( M, ℓ),
|ui | ≤ umax ,

i = 0, . . . , N − 1,

where, recursively,
xi+1 = xi + hi (v cos(ui ) + flow(yi )) ,
yi+1 = yi + hi v sin(ui ),

i = 0, . . . , N − 1,

i = 0, . . . , N − 1.

Here, the dynamics are no longer constraints in the optimization problem, but
rather equations that implicitly determine the state evolution given a candidate
control sequence. Algorithm 7 provides a Python implementation of this shooting
method approach to Zermelo’s problem.
Both approaches come with their own advantages and limitations. Control parameterization methods generally result in smaller optimization problems, making the method computationally attractive. The dynamics are enforced exactly
through integration (up to the accuracy of the chosen numerical integrator),
which is especially useful when the dynamics are complex or only accessible
via a black-box simulator. However, state constraints may be difficult to enforce,
as the states are not explicit optimization variables but rather implicitly defined
through the integration of the dynamics. This can lead to numerical instability or
infeasibility when state constraints are critical. Moreover, errors from numerical
integration may accumulate, potentially reducing the accuracy of the solution.
On the other hand, state and control parametrization methods treat both states
and controls as optimization variables. This allows state constraints to be imposed directly, improving numerical stability and robustness, often leading to
better-conditioned optimization problems when constraints play a central role.
However, the resulting optimization problem generally grows significantly in
size, since all states and controls at every discretization point are treated as decision variables. This higher dimensionality increases computational cost and can
make the solver more sensitive to initial guesses.
In practice, both methods are widely used, and the choice between them often depends on the problem structure, the availability of simulators or system
models, and the importance of accurately handling state constraints.

2.4

Differentially Flat Systems

Computing open-loop control sequences by directly solving optimal control problems can often be computationally intensive. In many applications, it is useful
to trade off strict optimality12 for computational tractability by seeking “good”
trajectories that are simpler to compute, even if slightly sub-optimal.
For a special class of systems known as differentially flat systems, generating
such feasible trajectories is considerably simpler. A system is differentially flat if

That is, the theoretical best performance according to a given cost functional.
12

---

### [PDF p.76 | Book p.74]

74

principles of robot autonomy

Shooting Formulation for Zermelo’s Problem
# Decision variables: |$(u_i), \; i=0,\dots,N-1$|; Cost: |$\sum_{i=0}^{N-1} h_i u_i^2$|
cost = lambda u: np.sum(h * np.square(u))
# States computed recursively from |$x_0=0, y_0=0$|
dynamics = lambda x, y, u: (
x + h * (v * np.cos(u) + flow(y)),
y + h * v * np.sin(u)
)
def inequality_constraints(u):
x, y = 0, 0 # initial condition (x(0), y(0)) = (0, 0)
constraints = []
for ui in u:
x, y = dynamics(x, y, ui)
# |$(x_i, y_i) >= (0,0)$| (box constraint with below)
constraints.extend([x, y])
# |$(x_i, y_i) <= [M, \ell]$|
constraints.extend([M - x, l - y])
# |$(x_N, y_N) >= [M, \ell]$| (enforcing equality with the above)
constraints.extend([x - M, y - l])
return constraints
bounds = Bounds(-u_max * np.ones(N),
u_max * np.ones(N)) # |$\lvert u_i\rvert \le u_{\text{max}}$|
# Solve NLP
result = minimize(cost, u0, bounds=bounds,
constraints={'type': 'ineq',
'fun': inequality_constraints})

Algorithm 7: Direct shooting approach to Zermelo’s problem using forward Euler
discretization. The code for this example is available in the repository github.com
/StanfordASL/pora-exercises in the notebook ch02/zermelos_problem.ipynb.

there exists a set of outputs, called flat outputs, such that all system states and inputs can be expressed as algebraic functions of these outputs and a finite number
of their derivatives. This property allows trajectory generation to be performed in
the space of the flat outputs, eliminating the need to solve differential equations
as part of the optimization process and greatly reducing computational complexity.
Differentially flat models arise in several common robotics applications, in-

---

### [PDF p.77 | Book p.75]

open-loop control & trajectory optimization

75

cluding simple car models, quadrotors, and many other wheeled or aerial vehicles. Their relative simplicity and expressiveness make them particularly attractive for trajectory planning and open-loop control synthesis.
Example 2.4.1 (Differentially Flat Autonomous Vehicle Control). Recall the motion planning task from Example 2.1.1 where the objective was to compute an
open-loop control sequence to drive a vehicle through a course to a goal position
in minimum time. If we relax the requirement of optimality and instead aim
simply to find a feasible trajectory that follows the course, we can exploit the differential flatness of the kinematic car model. Specifically, consider the kinematic
car model from Equation (1.29):
ẋ = v cos θ,
ẏ = v sin θ,
v
θ̇ = tan ϕ,
L
where ( x, y) is the vehicle position, θ is the heading, v is the speed, ϕ is the
steering angle, and L is the wheelbase.
This system is differentially flat with flat outputs ( x (t), y(t)). Therefore, it is
sufficient to specify any differentiable trajectory for x (t) and y(t) that respects
the course constraints. From these trajectories, the remaining state and control
variables—which are the quantities needed for practical implementation—can be
computed analytically. The heading is obtained from the velocity direction as:
 
ẏ
θ = tan−1
.
ẋ
and the speed along the trajectory can be computed using either component of
the velocity:
ẋ
ẏ
v=
, or v =
.
cos θ
sin θ
Finally, the steering angle is determined from the heading dynamics:
 
−1 L θ̇
ϕ = tan
.
v
In this way, a feasible trajectory for the vehicle can be generated entirely by specifying smooth flat output trajectories, from which all states and, importantly, the
control inputs can be derived directly.
We formalize this concept through the notion of differential flatness13 .
Definition 2.4.1 (Differential Flatness). A nonlinear system with state x ∈ Rn and
control u ∈ Rm :
ẋ(t) = f ( x(t), u(t)),
(2.20)
is differentially flat if there exists a function α such that:
z = α( x, u, u̇, . . . , u(a) ),

Murray [101] is a good resource for a
comprehensive treatment on differential
flatness.
13

(2.21)

---

### [PDF p.78 | Book p.76]

76

principles of robot autonomy

where u(i) denotes the i-th time derivative of u, and such that the system trajectories can be expressed as functions of the flat output z ∈ Rm and a finite number
of its derivatives:
x = β(z, ż, . . . , z(b) )
u = γ(z, ż, . . . , z(c) ).

(2.22)

In other words, a system is said to be differentially flat if there exists a set of
outputs z (with the same dimension as the input vector u) that completely determine both the states and the inputs, without requiring integration of the system
dynamics. For trajectory optimization, this property is particularly advantageous:
since the evolution of a flat system is fully characterized by its flat outputs, trajectories can be computed directly in the output space and then mapped to the
corresponding inputs, thereby avoiding expensive integration of the dynamics.
In the following sections, we explore different techniques to exploit differential
flatness for open-loop trajectory design, including how to parameterize trajectories in the flat output space, handle initial and terminal state constraints, and
enforce control constraints.

2.4.1

Trajectory Parameterization

Our primary limitation when planning a trajectory in the flat output space is that
it must be differentiable. A common approach is to parameterize each component
of the flat output z using N smooth basis functions:
N

z j (t) = ∑ αi ψi (t),
[ j]

(2.23)

i =1

[ j]

where z j is the j-th element of z, αi ∈ R are parameters that define the trajectory,
and ψi (t) are smooth basis functions.
Polynomial basis functions are a natural choice, e.g., ψ1 (t) = 1, ψ2 (t) = t,
ψ3 (t) = t2 , etc. A key advantage of this parameterization is that z j (t) is linear in
[ j]

the variables αi , which facilitates translating constraints on z and its derivatives
[ j]

directly into constraints on the coefficients αi .

2.4.2

Equality Constraints

A key component of any open-loop motion planning problem is the enforcement
of boundary conditions. Typically, this means ensuring that the system begins at
a prescribed initial state x(0) = x0 and often that it reaches a desired terminal
state, x(t f ) = x f , at some final time t f . When planning in the flat output space,
these state conditions must be expressed as constraints on the flat output z(t) and
its derivatives. Recalling the mapping in Equation (2.22), this leads to:
x0 = β(z(0), ż(0), . . . , z(q) (0)),
x f = β(z(t f ), ż(t f ), . . . , z(q) (t f )).

(2.24)

---

### [PDF p.79 | Book p.77]

open-loop control & trajectory optimization

(q)

In practice, this means that boundary conditions on z j (0), ż j (0), . . . , z j (0) and
(q)

z j (t f ), ż j (t f ), . . . , z j (t f ) must be enforced. When using a smooth basis function
parameterization of the form in Equation (2.23), these conditions translate directly
[ j]

into algebraic constraints on the coefficients αi . By differentiating Equation (2.23)
q times, we obtain:
N

ż j (t) = ∑ αi ψ̇i (t),
[ j]

i =1

..
.

(2.25)
N

z j (t) = ∑ αi ψi (t).
(q)

[ j] (q)

i =1

which allows us to express the boundary conditions as a system of linear equations:




z j (0)
ψ1 (0)
ψ2 (0)
. . . ψ N (0)
 ż (0) 
 ˙

ψ˙2 (0)
. . . ψ˙N (0) 
 j

 ψ1 (0)


  
..
..
..
..


 [ j]

α
.




.
.
.


  1[ j]   (q)
 ψ ( q ) (0) ψ ( q ) (0) . . . ψ ( q ) (0)   α   z (0) 

 1
 2   j
2
N
(2.26)
.
  = 

 ψ1 (t f )
ψ2 (t f ) . . . ψN (t f )   ...   z j (t f ) 


  
 ż j (t f ) 
 ψ˙1 (t f )
ψ˙2 (t f ) . . . ψ˙N (t f ) 



 α[ j]



 N
..
.
.
.




..
..
..
.




(q)
(q)
(q)
(q)
z j (t f )
ψ1 (t f ) ψ2 (t f ) . . . ψN (t f )
Assuming the matrix formed by the basis functions has a sufficient number of
columns and that it is full column rank, we can solve for (possibly non-unique)
[ j]

αi that solve the trajectory generation problem.
More generally, any equality constraint on the flat outputs or their derivatives—beyond just initial and terminal states—can be written in this linear form.
For instance, waypoints can be added as additional equality constraints. However, if too many constraints are imposed, the system may become overdetermined, leaving no feasible solution. In such cases, one must increase the richness
of the basis functions, for example by using higher-order polynomials or additional functions, which improves flexibility but also increases computational
complexity.

2.4.3

Inequality Constraints via Time Scaling

Having addressed equality constraints in Section 2.4.2, we now turn to inequality
constraints. These commonly arise in motion planning and control to enforce
actuator limits or safety bounds on the state. For example, the simple car model
from Example 2.4.1 may have a speed constraint of the form:

|v(t)| ≤ vmax .

77

---

### [PDF p.80 | Book p.78]

78

principles of robot autonomy

A useful technique for handling such constraints in the flat-output space is
time scaling. The idea is to first plan a trajectory that satisfies the equality constraints (e.g., by solving Equation (2.26)), and then adjust its temporal evolution—speeding up or slowing down along the path—to enforce the inequality
constraints.
Formally, let x(t) be a trajectory satisfying the equality constraints. We can
separate the geometric path14 from its timing by introducing a path parameter
s ( t ):

The geometric path of a trajectory is
the sequence of states x of the trajectory,
but not associated with a particular time
14

x(t) = x(s(t)),
with s(0) = s0 , s(t f ) = s f , and ṡ(t) > 015 . The geometric path x(s) captures the
sequence of states, while the choice of s(t) determines how quickly the system
traverses that path. Varying s(t) is referred to as time scaling.
Example 2.4.2 (Time Scaling for a Simple System). Consider a scalar system with
state x ∈ R and a straight-line path connecting an initial and terminal state, x0
and x f :
x ( s ) = x0 + s ( x f − x0 ),

s ∈ [0, 1].

Choosing a cubic polynomial for s(t),
s(t) =

3 2
2
t − 3 t3 ,
2
T
T

t ∈ [0, T ],

which satisfies s(0) = 0, s( T ) = 1, and ṡ(t) > 0, yields the temporal trajectory:

x ( t ) = x0 +


3 2
2 3
t
−
t
( x f − x0 ).
T2
T3

Here, T controls the duration of the trajectory. If we impose a velocity bound:

| ẋ | ≤ ẋmax ,
then:

t
t2
−
( x f − x0 ),
T2
T3


1
2t
ẍ = 6
( x f − x0 ),
−
T2
T3


ẋ = 6

with the maximum velocity attained at t = T2 . We can then convert this into a
constraint on T to ensure the inequality constraint is satisfied:
T≥

3( x f − x0 )
.
2ẋmax

Example 2.4.2 illustrates the key idea: inequality constraints can often be transformed into conditions on the timing law s(t), without altering the geometric path
itself.

The condition ṡ(t) > 0 ensures invertibility, so each t corresponds to a unique
s.
15

---

### [PDF p.81 | Book p.79]

open-loop control & trajectory optimization

79

For general state-space systems, time scaling is often more complex. Given a
feasible trajectory ( x(t), u(t)) of the system dynamics in Equation (2.20), we can
rewrite it as a geometric path ( x(s), u(s)) using a path parameter s(t):
dx(s) ds(t)
= f ( x(s), u(s)).
ds
dt

(2.27)

For time scaling, we replace s(t) with a new path parameter s̃(t) over a possibly
different interval t ∈ [0, t̃ f ], with s̃(0) = s0 and s̃(t̃ f ) = s f 16 . The new scaling
must still satisfy the dynamics:
dx(s̃) ds̃(t)
= f ( x(s̃), u(s̃)).
ds̃
dt

The geometric path is still defined on
the interval [s0 , s f ], which must remain
the same for any new time scaling law.
16

(2.28)
dx(s̃)

Since the geometric path is fixed—as it was previously defined—the terms ds̃
and x(s̃) are also fixed. Therefore, time scaling with a new path parameter s̃(t),
is only admissible if an appropriate ũ(s̃) can be found. Fortunately, for many
systems—including those commonly studied in motion planning—this is possible
with the right choice of s̃(t).
Example 2.4.3 (Time Scaling for the Simple Car Model). Consider again the simple car model from Equation (1.29):
ẋ = v cos θ,
ẏ = v sin θ,
v
θ̇ = tan ϕ,
L
and suppose we have identified a candidate trajectory xc (t) with control uc (t)
by leveraging the differential flatness of the model through Equation (2.26) and
mapping the flat outputs zc (t) into the state and control space.
For this model, a natural choice for the path parameter s is the arc-length,
defined as:
s(t) =

Z t
0

v(τ )dτ.

such that ṡ(t) = v(t) > 0. With this choice, the geometric path xc (s) is defined
over s ∈ [0, Lpath ], where Lpath is the total length of the path. Rewriting the
dynamics in terms of an arbitrary time scaling s̃(t) gives:
dxc (s̃) ˙
s̃ = v(s̃) cos θc (s̃),
ds̃
dyc (s̃) ˙
s̃ = v(s̃) sin θc (s̃),
ds̃
dθc (s̃) ˙
v(s̃)
s̃ =
tan ϕ(s̃),
ds̃
L
which must hold for any admissible time scaling s̃(t)17 .

The trivial choice s̃(t) = s(t) reproduces the original candidate trajectory
with control inputs uc (t).
17

---

### [PDF p.82 | Book p.80]

80

principles of robot autonomy

By adopting the arc-length parameterization, we have s̃˙ = v(s̃), so these equations reduce to:
dxc (s̃)
= cos θc (s̃),
ds̃
dyc (s̃)
= sin θc (s̃),
ds̃
1
dθc (s̃)
= tan ϕ(s̃).
ds̃
L
The first two equations are automatically satisfied for any choice of s̃ ∈ [s0 , s f ],
since the original candidate trajectory satisfies the dynamics. On the other hand,
the third equation is satisfied provided we reuse the same steering input, ϕ(s̃) =
ϕc (s̃). Therefore, the dynamics remain consistent for any choice of time scaling
s̃(t): the geometric path is preserved, while the temporal evolution along that
path is left free. This observation is powerful as we may freely adjust the speed
input v(t), subject only to s̃˙ (t) > 0, without altering the geometry of the trajectory.
In practice, this allows us to easily enforce inequality constraints on the speed
|v(t)| ≤ vmax .
Example 2.4.3 shows a relatively straightforward application of time scaling
to a model derived from kinematic constraints. This idea extends naturally to a
wide class of kinematic models of the form:
ẋ(t) = G ( x(t))u(t).

(2.29)

Applying the chain rule, we obtain:
dx(s)
ṡ = G ( x(s(t)))u(t),
ds
which can be rewritten as:
dx(s)
= G ( x(s))u g (s),
ds

(2.30)

u(t)

where u g (s) = ṡ(t) is the geometric control18 . Equation (2.30) shows that the geometric path x(s) is fully determined by the geometric control u g (s), independent
of the time parametrization. Therefore, once the geometric control and geometric path are defined, we can temporally scale the trajectory x(t) using the path
parameter s(t) without changing the geometric path. The corresponding control
inputs are recovered via u(t) = ṡ(t)u g (s).
In summary, for models of the form (2.29), we can perform time scaling by:
1. Selecting a path parameter s (e.g., arc-length), computing s(t) for the original
trajectory x(t), and determining the interval [s0 , s f ].
2. Re-parameterizing the control u(t) in terms of s.
3. Computing the geometric control u g (s) = u(s(t))/ṡ(t) for s ∈ [s0 , s f ].

Since s(t) must be strictly increasing,
we require ṡ(t) > 0.
18

---

### [PDF p.83 | Book p.81]

open-loop control & trajectory optimization

4. Defining a new path parameter function s̃(t) over the interval [0, t̃ f ] with s̃˙ (t) >
0, s̃(0) = s0 , and s̃(t̃ f ) = s f .
5. Computing the new control inputs as ũ(t) = u g (s̃(t))s̃˙ (t) for all t ∈ [0, t̃ f ].
Example 2.4.4 (Time Scaling for the Unicycle Model). Consider the kinematic
unicycle model:
ẋ = v cos θ,
(2.31)

ẏ = v sin θ,
θ̇ = ω,

where ( x, y) denote the position, θ the heading, v the forward velocity, and ω the
rotation rate. We define the state as x = [ x, y, θ ]⊤ and the control as u = [v, ω ]⊤ .
A natural path parameter for this system is again the arc-length:
s(t) =

Z t
0

v(τ )dτ,

such that ṡ(t) = v(t) > 0. If the trajectory is defined over t ∈ [0, T ] with total
length Lpath , then s(0) = 0 and s( T ) = Lpath . The corresponding geometric
controls are:
v(s)
= 1,
ṡ(t)
ω (s)
ω (s)
ω g (s) =
=
,
ṡ(t)
v(s)
v g (s) =

where the fact that v g (s) = 1 follows directly from ṡ(t) = v(s(t)). Introducing a
new timing law s̃(t) generates a new velocity profile ṽ(s̃) = s̃˙ (t) along the path,
which can use to solve for the new ω̃ inputs by:
ω̃ (s̃) = ω g (s̃)s̃˙ (t) =

ω (s̃)
ṽ(s̃).
v(s̃)

In practice, it is often simpler to directly prescribe a velocity profile ṽ(s̃) along the
ω (s̃)
path and compute the corresponding angular velocity ω̃ (s̃) = v(s̃) ṽ(s̃). Finally,
to determine the new controls as functions of time, we note that:
τ (s) =

Z s

1
ds′ ,
′
0 ṽ ( s )

defines a function τ (s) that maps each point s ∈ [0, Lpath ] to a new time.
Example 2.4.5 (Planar Quadrotor Control). In this example we consider the control of a planar quadrotor system. The quadrotor is modeled with six state variables: horizontal position x, vertical position y, orientation angle ϕ, and their
respective velocities. The control inputs are the thrusts T1 and T2 from the two
rotors. The objective is to minimize the energy consumption, represented by the
integral of the squared thrusts over time:
minimize

Z t
0

f

T1 (t)2 + T2 (t)2 dt.

81

---

### [PDF p.84 | Book p.82]

82

principles of robot autonomy

The system dynamics are given by the following differential equations:
  

vx
ẋ
   − (T1 +T2 ) sin ϕ 
v̇ x  

m
  

 ẏ  

vy
 =

 v̇   (T1 +T2 ) cos ϕ − g ,
 y  m

  

ω
 ϕ̇  

( T2 − T1 )ℓ
ω̇
Izz

where m is the mass, g is the gravitational acceleration, ℓ is the distance from the
center of mass to each rotor, and Izz is the moment of inertia about the z-axis.
This system is differentially flat, with flat outputs ( x, y). For a practical implementation of differential flatness for trajectory generation applied to this system,
refer to the notebook ch02/differentially_flat_planar_quadrotor.ipynb in
the repository github.com/StanfordASL/pora-exercises.

2.5

Summary

In this chapter, we explored how trajectory optimization provides a fundamental
framework for computing open-loop motions and establishing a foundation for
autonomous decision-making in robotic systems.
We began by formalizing the optimal control problem—a mathematical formalization for the task of driving a system’s state evolution through admissible
control inputs while optimizing a performance criterion. This formulation involves three key components: the system’s mathematical model, the physical
constraints, and the performance criteria.
We then introduced two major families of methods for solving optimal control problems and compute optimal open-loop control sequences: direct methods and indirect methods. Indirect methods adopt an “optimize-then-discretize”
approach, deriving analytical necessary conditions for optimality and solving
the resulting two-point boundary value problem numerically. In contrast, direct
methods follow a “discretize-then-optimize” strategy, transcribing the continuous problem into a finite-dimensional nonlinear program that can be solved with
standard optimization solvers.
Lastly, we discussed differentially flat systems, a special class of systems for
which trajectory generation is significantly simplified. For these systems, planning can be performed in a lower-dimensional “flat output" space using techniques like polynomial parameterization. We showed how initial, terminal, and
waypoint constraints can be translated into linear algebraic equations, and how
inequality constraints on state and control can be managed through time scaling.
To learn more. For comprehensive treatments of optimal control, we point the
reader to several excellent references, including Murray [101], Kirk [70], Rao
[117], and Kelly [67]. Kirk [70] offers a foundational perspective on indirect methods, including detailed derivations of the calculus of variations and Pontryagin’s

---

### [PDF p.85 | Book p.83]

open-loop control & trajectory optimization

Minimum Principle. For a thorough exploration of direct methods and modern optimization-based approaches, Rao [117] and Kelly [67] provide in-depth
coverage of transcription techniques, such as collocation and shooting, and their
formulation as nonlinear programming problems. Finally, Murray [101] gives an
extensive overview of differential flatness, illustrating how this property can be
exploited for efficient trajectory generation.

2.6

Exercises

The starter code for the exercises provided below is available online through
GitHub. To get started, download the code by running in a terminal window:
git clone https://github.com/StanfordASL/pora-exercises.git

We denote Problems requiring hand-written solutions and coding in Python
with and , respectively.

Problem 1: Extremal Curves
[This exercise is inspired by Kirk [70], Chapter 4, Problem 4.9]
Given the functional:

Z 1
1
J (x) =
ẋ (t)2 + 5x (t) ẋ (t) + x (t)2 + 5x (t) dt,
2
0
find an extremal curve x ∗ : [0, 1] → R that satisfies x ∗ (0) = 1 and x ∗ (1) = 3.

Problem 2: Minimum Control Effort
Consider the dynamics:
ẋ (t) = −2x (t) + u(t),
with the initial constraint x (0) = 2, terminal constraint x (1) = 0, and cost functional:
J (u) =

Z 1
0

u(t)2 dt.

Write down the Hamiltonian and use the necessary optimality conditions to derive an optimal control u∗ (t) and corresponding state trajectory x ∗ (t).

Problem 3: Zermelo’s Ship
Zermelo’s ship must travel through a region of strong currents. The position of
the ship is denoted by ( x (t), y(t)) ∈ R2 . The ship travels at a constant speed
v > 0, yet its heading θ (t) can be controlled. The current moves in the positive

83

---

### [PDF p.86 | Book p.84]

84

principles of robot autonomy

x-direction with speed w(y(t)). The equations of motion for the ship are:
ẋ (t) = v cos θ (t) + w(y(t)),
ẏ(t) = v sin θ (t).
We want to control the heading θ (t) such that the ship travels from a given initial
position ( x (t0 ), y(t0 )) = ( x0 , y0 ) to the origin (0, 0) in minimum time.
1. Suppose w(y(t)) = vh y(t), where h > 0 is a known constant. Show that an
optimal control law θ ∗ (t) must satisfy a linear tangent law of the form:
v
tan θ ∗ (t) = α − t,
h
for some constant α ∈ R.
2. Suppose w(y(t)) ≡ β for some constant β > 0. Derive an expression for the
optimal transfer time t1∗ − t0 .

Problem 4: Singular Arc for Dubins’ Car
The kinematics of Dubins’ car are described by:
ẋ = v cos θ,
ẏ = v sin θ,
θ̇ = u,
where ( x, y) ∈ R2 is the car’s position, θ ∈ R is the car’s heading, v > 0 is the
car’s constant known speed, and u is the controlled turn rate. The turn rate is
bounded, meaning u ∈ [−ω̄, ω̄ ], where ω̄ > 0 is a known constant.
The car starts at ( x, y) = (0, 0) with a heading of θ = 0 at t = 0. We want the
car to drive to ( x, y) = (0, c) in the least amount of time possible, where c > 0 is
a given constant.
1. Use Pontryagin’s maximum principle to express the optimal control input
u∗ (t) as a function of the optimal co-state p∗ (t) := ( p∗x (t), p∗y (t), p∗θ (t)) ∈ R3 .
Hint: You should discover that the maximum condition for u∗ (t) is not informative whenever p∗θ (t) ≡ p̄θ for a particular fixed value p̄θ ∈ R. When such
a lack of information persists over a non-trivial time interval, i.e., any time interval [t1 , t2 ] with t2 > t1 ≥ 0, this is known as a singular arc. To compute u∗ (t)
in this case, use the fact that p∗θ (t) ≡ p̄θ is constant in time along this singular
arc.
2. Use boundary conditions to argue why p∗ (t) might end in a singular arc.
Suppose we know p∗ (t) begins on a non-singular arc, then switches once to
and ends on a singular arc. For this particular case, argue why u∗ (0) = ω̄ and
describe the optimal state trajectory ( x ∗ (t), y∗ (t), θ ∗ (t)) and control trajectory
u∗ (t) in words without explicitly deriving them.

---

### [PDF p.87 | Book p.85]

open-loop control & trajectory optimization

Problem 5: Single Shooting for a Unicycle
Consider the kinematic model of a unicycle:
ẋ = v cos(θ ),
ẏ = v sin(θ ),
θ̇ = ω,
where ( x, y) is the planar position of the vehicle, θ is its heading angle, v is its
forward velocity, and ω is its angular velocity. Overall, the state and control input
for this system are x := ( x, y, θ ) ∈ R3 and u := (v, ω ) ∈ R2 , respectively. We have
overloaded x to denote both horizontal position x ∈ R and the full state vector
x ∈ R3 .
Our task is to drive the vehicle from the starting configuration x (0) = (0, 0, π/2)
to the target configuration x ( T ) = (5, 5, π/2) in minimum time with as little control effort as possible. To this end, we consider the objective:
J ( x, u) =

Z T
0


α + v(t)2 + ω (t)2 dt,

where α > 0 is a chosen constant weighting factor and T is the free final time.
1. Derive the Hamiltonian and necessary optimality conditions, specifically
(a) the ODE for the state and co-state,
(b) the optimal control as a function of the state and co-state, and
(c) the boundary conditions, including the additional condition for free final
time T.
Hint: Since the control set is unbounded, use the weak maximum condition.
In practice, you might use a boundary value problem (BVP) solver from an
existing computing library, such as scipy.integrate.solve _ bvp, but in this
problem we will use a bit of nonlinear optimization theory and JAX to write our
own!
2. In the file ch02/exercises/unicycle_optimal_control.ipynb, complete the
implementations of unicycle_dynamics, hamiltonian, optimal_control, and
noc_ode. Use α = 0.25.
In the single shooting method, we need to initialize estimates of the initial costate p(0) and final time T. We then integrate the state and co-state dynamics
forward in time from t = 0 to t = T, at which point we check whether the
terminal boundary conditions are satisfied.
3. Use the ODE integration from noc_trajectories to complete
boundary_residual, which should compute a measure of how far off each of
your terminal boundary conditions is from satisfaction, given guesses for the
initial co-state p(0) and final time T.

85

---

### [PDF p.88 | Book p.86]

86

principles of robot autonomy

4. Finally, in newton _ step and single _ shooting, implement the NewtonRaphson root-finding method for boundary_residual. Now, if you provide
an appropriate guess for the initial costate and final time, you can solve the
problem in unicycle_optimal_control.ipynb and see a plot of the optimal
solution. You may find that whether or not your BVP solver converges to a
solution is highly dependent on the quality of your initial guess—indeed, initialization is a major challenge when applying indirect methods for optimal
control!
Hint: For finding roots of a function f : Rn → Rn , each iteration of the
Newton-Raphson method entails improving a current best guess x (k) at iteration k using the update rule:
x ( k +1) = x ( k ) −

∂ f ( k ) −1
( x ) f ( x ( k ) ).
∂x

---

### [PDF p.89 | Book p.87]

open-loop control & trajectory optimization

References
[7]

U. M. Ascher and R. D. Russell. “Reformulation of boundary value problems into “standard” form”. In: SIAM Review 23.2 (1981), pp. 238–254.

[13]

D. Bertsekas. Nonlinear Programming. Athena Scientific, 2016.

[51]

J. Hertling. “Numerical Methods for Two-Point Boundary Value Problems
(Herbert B. Keller)”. In: SIAM Review 12.2 (1970), pp. 313–315.

[54]

J. P. How. Lecture Notes for Principles of Optimal Control. 2008.

[67]

M. Kelly. “An Introduction to Trajectory Optimization: How to Do Your
Own Direct Collocation”. In: SIAM Review 59.4 (2017), pp. 849–904.

[70]

D. E. Kirk. Optimal Control Theory: An Introduction. Dover Publications,
2004.

[101]

R. M. Murray. Optimization-Based Control. California Institute of Technology, 2009.

[117]

A. Rao. “A Survey of Numerical Methods for Optimal Control”. In: Advances in the Astronautical Sciences 135 (2010).

87

---

### [PDF p.90 | Book p.88]

> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]
