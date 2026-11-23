# Ch 3: Closed-Loop Control & Trajectory Tracking

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Part I: Motion Planning & Control
- **Trang sách:** 89–126 | **Trang PDF:** 91–128
- **Độ ưu tiên cho dự án:** `CỐT LÕI`
- **Tóm tắt:** Điều khiển phản hồi kinh điển (PID), LQR, điều khiển phi tuyến và MPC bám quỹ đạo.

---

### [PDF p.91 | Book p.89]

3
Closed-Loop Control & Trajectory Tracking
In Chapter 2, we introduced trajectory optimization as a foundational tool for
open-loop optimal control, where the objective is to compute a time-parameterized
control sequence that minimizes a given cost function subject to system dynamics
and constraints. Within a robot’s autonomy stack, open-loop control is often
a key component, generating control sequences for tasks such as manipulation,
locomotion, and navigation. However, because open-loop strategies depend only
on time and not on the current system state, they are inherently vulnerable to
disturbances, modeling errors, and other execution-time uncertainties.
In this chapter, we turn our attention to closed-loop optimal control. While the
core elements of the problem remain the same—namely, the system dynamics,
state and input constraints, and a performance criterion—the object of optimization is fundamentally different. Specifically, rather than seeking an open-loop
sequence u(t), closed-loop control aims to determine an optimal control law of
the form u(t) = π ( x(t), t), which explicitly depends on the current state in addition to the current time. Such closed-loop control laws are often referred to as
feedback controllers or control policies.
Obtaining solutions to an optimal control problem in the form of a closed-loop
policy is particularly powerful, as it provides a rule prescribing optimal behavior from any state the system might encounter. Under idealized assumptions—
that is, exact system models, perfect knowledge of the state, and absence of
disturbances—the optimal open-loop sequence and the optimal closed-loop policy would produce identical behavior. In practice, however, such conditions are
rarely met, with real systems inevitably facing model uncertainties, external disturbances, and measurement noise. In these settings, closed-loop policies offer
a distinct advantage, as they continuously adapt the control input to the actual
system state, thereby providing levels of robustness that are difficult to achieve
through open-loop strategies (Chapter 3).
Formally, we define a closed-loop control law as follows:
Definition 3.0.1 (Closed-loop control law). A closed-loop control law is a function
π : Rn × R → Rm that maps the current state1 x(t) ∈ Rn and time t ∈ R to a

When the full system state is not directly measurable, closed-loop control
laws can be defined based on the current
measured system outputs, i.e., u(t) =
π (y(t), t), where y(t) denotes the measured system output at time t. In this
case, the closed-loop policy is referred to
as an output feedback policy.
1

---

### [PDF p.92 | Book p.90]

90

principles of robot autonomy

control input u(t) ∈ Rm :
u ( t ) = π ( x ( t ), t ).

(3.1)

Despite their theoretical appeal and practical advantages, the main drawback
of closed-loop control approaches is computational, as solving for an optimal
closed-loop policy is generally more expensive than computing an open-loop input sequence. In practice, a useful compromise is achieved by following a twostep design, which aims to combine the strengths of both open- and closed-loop
paradigms. In this scheme, one first computes a nominal reference trajectory by
solving an open-loop optimal control problem, using tools such as those introduced in Chapter 2. Then, a closed-loop controller is designed to track this reference trajectory during execution. Conceptually, the resulting controller blends a
feedforward term—the nominal trajectory—with a feedback term that reacts to deviations from it. As we will discuss in more depth throughout this chapter, these
ideas are at the core of what is commonly referred to as trajectory tracking control.
Formally, the two-step design can be expressed as:
u(t) = ū(t) + π ( x(t), x̄(t), t),

(3.2)

where ū(t) and x̄(t) denote the nominal input and state trajectories, and π is a
trajectory-tracking control law ensuring that the actual trajectory remains close to
the planned one despite model mismatch or disturbances.
Building on these concepts, this chapter explores key strategies for closed-loop
optimal control and their application to trajectory tracking. We begin in Section 3.1 with the classical paradigm of feedback control, illustrated through the
widely used proportional–integral–derivative (PID) controllers and their application
to tracking, with a focus on differentially flat systems. Next, in Section 3.2, we

Figure 3.1: Comparison between
open-loop and closed-loop control in a 2D gridworld navigation task. Without disturbances
(left figure), we can see both
open and closed-loop policies
lead to same path, ending at the
goal (star). With a wind disturbance (right figure), the fixed
series of actions from the openloop control sequence fails to
take the robot to the goal after it
is pushed upward by the wind.
In contrast, the closed-loop policy specifies an action for each
state, allowing the system to react to the disturbance and successfully reach the goal by adjusting its behavior based on the
current state.

---

### [PDF p.93 | Book p.91]

closed-loop control & trajectory tracking

turn to linear optimal control, focusing on the linear quadratic regulator (LQR), its
key extensions, and its application to tracking control. We then discuss nonlinear
optimal control problems in Section 3.3, first introducing techniques that compute
optimal solutions in closed-loop form—such as the Hamilton-Jacobi-Bellman (HJB)
equation and Dynamic Programming (DP)—and then showing how, for tracking
purposes, linear methods can be extended to nonlinear systems through linearization. Building on this, we present how LQR ideas generalize to nonlinear optimal control through algorithms such as iterative LQR (iLQR) and differential dynamic programming (DDP), that simultaneously generate an open-loop trajectory
and closed-loop tracking controller in two-step design form. Finally, in Section 3.4, we introduce model predictive control (MPC), a powerful framework that
brings together ideas of open-loop and closed-loop optimal control through the
framework of receding horizon optimization, and discuss how it can be applied
to tracking.

3.1

Classical Feedback Control

The central goal of classical feedback control is to regulate a system’s output
so that it tracks a desired reference signal. For example, in the context of an
autonomous vehicle, one might want to control the vehicle’s speed to match a
target velocity or maintain a specific distance from another vehicle.
The classical paradigm of feedback control is built on a simple yet powerful principle: continuously measure the system output, compare it against the
desired reference, and compute corrective actions based on the resulting discrepancy, known as the error signal. These corrective inputs are then applied to the
system, ensuring the output continually adjusts toward the desired behavior. For
example, accelerate if the vehicle is below the target speed, or decelerate it if it is
above.
Classical feedback controllers are generally designed to satisfy a set of fundamental desiderata:
• Stability: the controller should ensure that the system remains stable. While
there are several formal notions of stability, the essential requirement is that,
loosely speaking, the system “is bounded in its behavior”.
• Tracking: the controller should minimize the error between the system output and the desired reference, ensuring the system follows the commanded
trajectory as closely as possible.
• Disturbance rejection: the controller should attenuate the effects of external disturbances and measurement noise, keeping the system performance relatively
unaffected by unexpected inputs.
• Robustness: the controller should perform well despite uncertainties in the system model or parameters, ensuring reliable operation under varying conditions.

91

---

### [PDF p.94 | Book p.92]

92

principles of robot autonomy

k p e(t)

r (t)

+

e(t)

ki

Rt

+

0 e ( τ ) dτ

u(t)

System Dynamics

y(t)

−
de(t)

k d dt

This feedback principle underlies many widely used strategies in control engineering. Among the simplest and most widely adopted strategies arising from
this principle is the proportional–integral–derivative (PID) controller2 . Despite its
conceptual simplicity, PID has endured the test of time and remains a dominant
tool in control engineering, from regulating temperature in industrial furnaces to
stabilizing the flight of drones.

3.1.1

Structure of PID Control

Figure 3.2: Block diagram for
a PID controller in a feedback
loop. The error signal e(t) is
computed as the difference between the reference r (t) and the
output y(t). The control input
u(t) is generated by combining
the proportional, integral, and
derivative terms of the error.

PID control is most naturally formulated for single-input, single-output
(SISO) linear systems, where the error
signal is scalar. Extensions to multiinput multi-output or nonlinear systems are possible, but they often rely
on heuristic tuning and provide weaker
guarantees.
2

A PID controller computes the control input as a weighted combination of three
terms derived from the tracking error e(t) = r (t) − y(t), where r (t) denotes the
desired reference and y(t) the measured output:
u(t) = k p e(t) + k i

Z t
0

e(τ )dτ + k d

d
e ( t ).
dt

(3.3)

The three terms serve complementary purposes:
• Proportional (P): reacts immediately to deviations, producing corrective action
proportional to the current error.
• Integral (I): accumulates past error, driving steady-state error to zero.
• Derivative (D): predicts future trends by responding to the rate of change,
improving transient behavior and damping oscillations.
By adjusting the gains (k p , k i , k d ), we can shape how aggressively the controller
responds to disturbances, how quickly it eliminates offsets, and how smoothly it
approaches the reference trajectory3 . The structure of a PID controller is depicted
in the block diagram in Section 3.1.1. PID control is ubiquitous in industry precisely because of this simplicity: the controller can be deployed with only limited
implementation effort and modest computational resources, which makes it attractive for embedded systems.

Although tuning PID controllers is
not trivial, heuristic rules such as the
Ziegler–Nichols method provide systematic starting points for gain selection,
but they often require further refinement
in practice.
3

---

### [PDF p.95 | Book p.93]

closed-loop control & trajectory tracking

93

Example 3.1.1 (PD control of a double-integrator system). To illustrate the mechanics of PID-type control, consider a double-integrator system with dynamics:
"

#
" #
1
0
x(t) +
u ( t ),
0
1

0
ẋ(t) =
0

where x = [ x1 , x2 ]⊤ . Suppose the control objective is to regulate x1 to the origin.
A proportional–derivative controller of the form:
u(t) = −k p e(t) − k d

de(t)
,
dt

e ( t ) = x1 ( t ),

yields closed-loop dynamics:
"

0
ẋ(t) =
−k p

#
1
x ( t ),
−k d

where we have used the fact that ė = ẋ1 = x2 . The eigenvalues of this system are:
1
k
λ=− d±
2
2

q

k2d − 4k p ,

and, as a result, stability requires selecting k p and k d such that the real parts of
these eigenvalues are negative; that is, k p > 0 and k d > 04 . By appropriately
tuning k p and k d , we can trade off speed of convergence against overshoot, oscillations, and sensitivity to measurement noise. For example, one might set the
proportional gain k p to a very large value in order to drive rapid convergence
to the origin. In practice, however, excessively large gains tend to amplify measurement noise and can cause the controller to behave poorly. For example, with
large proportional gain k p , the controller may introduce oscillations, while a large
derivative gain k d increases damping but may also slow the system’s response.
Beyond PID and PD control, classical control theory provides a rich suite of
tools for analysis and design. These methods are often developed in the frequency
domain5 , where tools such as Bode plots and the Nyquist stability criterion offer
powerful ways to assess and shape system behavior. For an in-depth treatment
of these topics, we refer the reader to Aström and Murray [9].

3.1.2

Application of PID Control to Tracking Problems

Although PID controllers are most commonly associated with regulation tasks,
as discussed in Example 3.1.1, the same structure introduced in Section 3.1.1
can also be employed for trajectory tracking, where the objective is to follow a
time-varying nominal trajectory. In this setting, the reference signal r (t) evolves
over time, and the controller seeks to minimize the instantaneous tracking error
e(t) = r (t) − y(t) throughout the motion. While this direct application of the
PID framework can perform reasonably well for simple scenarios, such as slowly

Note that a proportional controller
alone, with k d = 0, will not make the
system stable since at best the eigenvalues would be purely complex, and thus
the system response would be an undamped oscillation.
4

Frequency-domain analysis uses the
Laplace transform to represent system dynamics as algebraic relations—
referred to as transfer functions—rather
than differential equations.
5

---

### [PDF p.96 | Book p.94]

94

principles of robot autonomy

varying or smooth trajectories, it remains largely heuristic, requiring ad hoc design and tuning of the gains for each specific task and system. As a result, PIDbased tracking tends to be fragile and poorly generalizable, with performance
degrading even under minor variations to the problem setup. There is, however,
an important class of systems where PID-type control can be systematically and
effectively applied to tracking: differentially flat systems.
As introduced in Section 2.4, differential flatness provides a powerful framework for computing open-loop control sequences. Recall that a system with state
x ∈ Rn and input u ∈ Rm :
ẋ = f ( x, u),
is said to be differentially flat if there exists a function α such that:
z = α( x, u, u̇, . . . , u(a) ),
where u(i) denotes the i-th derivative of u, and such that both the system states
and inputs can be expressed as algebraic functions of the flat outputs z ∈ Rm and
a finite number of their derivatives:
x = β(z, ż, . . . , z(b) ),

u = γ(z, ż, . . . , z(c) ).

This structural property implies that the full system trajectory is fully determined
once the flat outputs z(t) are known. In practice, we can therefore design a trajectory directly in the flat-output space—using, for example, spline interpolation or
polynomial parameterizations—and reconstruct the corresponding state and control trajectories algebraically, without the need to integrate the system dynamics.
While in Chapter 2 we focused on leveraging differential flatness for openloop trajectory generation, it is important to highlight how these systems also
lend themselves naturally to trajectory tracking. In particular, differential flatness
enables the trajectory tracking problem for a nonlinear system to be reduced to a
linear tracking problem in the flat-output space, where classic control methods—
such as PID—can be applied.
Differentially flat systems possess a particularly useful feature, as they can be
feedback linearized to yield a linear system in the flat-output space. Specifically,
given a differentially flat system with flat output z = (z1 , . . . , zm ) there exist a
vector of integers r = (r1 , r2 , . . . , rm ) such that:
(r )

(r )

x = β(z1 , ż1 , . . . , z1 1 , . . . , zm , żm , . . . , zm m ),
(r +1)

u = γ(z1 , ż1 , . . . , z1 1

(r +1)

, . . . , zm , żm , . . . , zm m

(3.4)

),

and such that the system dynamics can be equivalently expressed as a linear
system of the form:
(r +1)

zi 1

= w1 ,

(r +1)
z2 2
= w2 ,

..
.
(r +1)

zm m

= wm ,

(3.5)

---

### [PDF p.97 | Book p.95]

closed-loop control & trajectory tracking

where w = (w1 , . . . , wm ) is a virtual control input that can be algebraically related to the original system inputs u6 . The linear system in Equation (3.5) can
effectively be controlled using standard linear control techniques, such as PID
control.
In particular, given a reference flat output trajectory zd = (zd,1 , . . . , zd,m )—
computed, for example, by any open-loop method—and its corresponding virtual
input trajectory wd = (wd,1 , . . . , wd,m ), we can define the component-wise tracking
error:
ei := zi − zd,i , i = 1, . . . , m,
which implies the following error dynamics:
(r +1)

ei i

= wi − wd,i .

To ensure convergence of the tracking error to zero, we can choose the following
control law:
ri

wi = wd,i − ∑ k i,j ei ,
( j)

j =0

which, applied to the system in Equation (3.5), yields the following closed-loop
dynamics:
(r +1)

zi i
(r +1)

Since wd,i = zd,ii
the form:

ri

= wd,i − ∑ k i,j ei .
( j)

j =0

by construction, the resulting tracking error dynamics take
(r +1)

ei i

ri

+ ∑ k i,j ei = 0,
( j)

j =0

where the gains k i,j > 0 are selected to enforce stability.
This procedure effectively reduces the nonlinear trajectory tracking problem
to a set of decoupled linear tracking problems, one for each flat output, which
can be solved using standard linear control techniques. Below, we illustrate this
procedure with a concrete example.
Example 3.1.2 (PD control for a dynamically extended unicycle). Consider the
dynamically extended unicycle model introduced in Example 1.3.1:
ẋ = v cos θ,
ẏ = v sin θ,
v̇ = a,
θ̇ = ω,
with state x = [ x, y, v, θ ]⊤ and control input u = [ a, ω ]⊤ . This system is differentially flat with flat outputs ( x, y) and its dynamics can be expressed as:
" # "
#" #
" #
ẍ
w1
a
cos θ −v sin θ
:=
=
,
(3.6)
sin θ v cos θ
ÿ
ω
w2
|
{z
} |{z}
J (θ,v)

u

95

For a detailed treatment of feedback
linearization for differentially flat systems, we refer the reader to Levine [80]
and Murray [101].
6

---

### [PDF p.98 | Book p.96]

96

principles of robot autonomy

where w = [w1 , w2 ]⊤ is a virtual control input representing the flat-output accelerations, effectively transforming the system into a system of the form in Equation (3.5).
As a result, given a reference trajectory ( xd , yd ), we can design a feedback law
for w that ensures tracking of the desired trajectory. Specifically, we can select
the following PD-type virtual control:
w1 = ẍd + k px ( xd − x ) + k dx ( ẋd − ẋ ),
w2 = ÿd + k py (yd − y) + k dy (ẏd − ẏ),

(3.7)

with positive control gains k px , k dx , k py , k dy > 0. Under this law, the Cartesian
tracking error obeys a second-order linear differential equation:
ëx + k dx ėx + k px ex = 0,

ëy + k dy ėy + k py ey = 0,

ensuring that the tracking error (e x , ey ) = ( xd − x, yd − y) converges exponentially
to zero.
Finally, assuming the Jacobian matrix J (θ, v) is invertible, the corresponding
control inputs ( a, ω ) can be obtained algebraically by:
" #
" #
a
w1
−1
= J (θ, v)
.
ω
w2
Thus, a conceptually simple PD control law in the flat-output space translates
into a nonlinear state feedback law for the original system.

3.2

Optimal Closed-loop Control for Linear Systems

Despite their widespread use and practical appeal, classical feedback controllers
lack systematic methods to mathematically quantify and optimize performance.
As introduced in Chapter 2, modern control theory addresses these issues by
formulating controller design as an explicit optimization problem.
In this section, we focus on the linear–quadratic setting7 , which represents one
of the most elegant and widely applicable frameworks for closed-loop optimal
control. Specifically, we focus on the linear quadratic regulator problem by first
presenting its infinite-horizon, continuous-time formulation. Then, we discuss
several important extensions of this framework—such as finite-horizon, discretetime, and time-varying formulations—and illustrate how it can be applied to
linear tracking problems.

3.2.1

That is, where the system dynamics are
linear and the cost function is quadratic.
7

The Linear Quadratic Regulator

The linear quadratic regulator (LQR) provides a principled solution to the regulation problem, where the primary objective is to drive the state of a linear system
to the origin while optimally balancing state deviations against control effort8 .
Formally, consider the linear time-invariant (LTI) system:
ẋ(t) = Ax(t) + Bu(t),

(3.8)

While this may seem like a restrictive
setting at first, we will see in the remainder of this chapter that this formulation extends naturally to a wide range
of practically relevant problems.
8

---

### [PDF p.99 | Book p.97]

closed-loop control & trajectory tracking

97

where A ∈ Rn×n and B ∈ Rn×m are constant matrices. The objective is to determine a control policy u(t) that minimizes the quadratic cost functional:
J (u) =

Z ∞
0

x(t)⊤ Qx(t) + u(t)⊤ Ru(t)dt,

(3.9)

where Q ∈ Rn×n is a symmetric positive semidefinite matrix that penalizes deviations of the state from the origin and R ∈ Rm×m is a symmetric positive definite
matrix that penalizes control effort. Thus, in its infinite-horizon form, the LQR
problem is formalized as the following optimal control problem:
minimize
u

subject to

Z ∞
0

x(t)⊤ Qx(t) + u(t)⊤ Ru(t)dt,

(3.10)

ẋ(t) = Ax(t) + Bu(t).

Assuming that the pair ( A, B) is stabilizable and ( Q, A) is detectable9 , the LQR
problem admits a unique optimal solution in the form of a stationary linear statefeedback controller:
u(t) = −Kx(t),
(3.11)
where the optimal gain matrix K ∈ Rm×n is given by:
K = R−1 B⊤ P.

These assumptions guarantee the existence of a unique stabilizing solution to
the infinite-horizon LQR problem. For
formal definitions and proofs, we refer
the reader to Murray [101] and Bertsekas
[12].
9

(3.12)

Here, P ∈ Rn×n is the unique positive semidefinite solution to the continuous-time
algebraic Riccati equation:
A⊤ P + PA − PBR−1 B⊤ P + Q = 0.

(3.13)

The Riccati equation can be derived either through the calculus of variations—
via the Pontryagin Maximum Principle introduced in Chapter 2—or through dynamic programming, using the Hamilton–Jacobi–Bellman equation10 . Substituting the optimal closed-loop policy from Equation (3.11) into the system dynamics
from Equation (3.8) yields the closed-loop system:
ẋ(t) = ( A − BK ) x(t),

Both derivations lead to the Riccati
equation and the same optimal linear
feedback law. We refer the reader to
Bertsekas [12] for an in-depth treatment
of both approaches.
10

(3.14)

which is guaranteed to be asymptotically stable, i.e., the eigenvalues of the matrix
A − BK have strictly negative real parts. Thus, the LQR problem provides a
direct recipe for the regulation problem: solve the Riccati equation11 , compute
the optimal gain matrix K, and apply the feedback law u(t) = −Kx(t).
As a concrete example, Algorithm 8 demonstrates how to compute the optimal infinite-horizon LQR controller for a simple double integrator system with
dynamics ẍ = u.
Designing the cost matrices. A central question in LQR design is how to select the
cost matrices Q and R, as these determine the trade-off between state regulation
and control effort, thereby shaping the overall closed-loop performance. For a
valid solution to exist, the matrices must satisfy Q = Q⊤ ⪰ 0 and R = R⊤ ≻ 0.

In practice, solutions to the algebraic
Riccati equation are obtained numerically using standardized software packages. Popular implementations include
11

scipy.linalg.solve _ continuous _ are
in Python or icare in MATLAB.

---

### [PDF p.100 | Book p.98]

98

principles of robot autonomy

Double Integrator Infinite-horizon LQR
import numpy as np
from scipy.linalg import solve_continuous_are
# System dynamics matrices for simple double integrator |$\ddot{x}$| = u
A = np.array([[0, 1], [0, 0]])
B = np.array([[0], [1]])
# Define cost function matrices
Q = np.array([[1, 0], [0, 1]])
R = np.array([[1]])
# Solve the continuous algebraic Riccati equation
P = solve_continuous_are(A, B, Q, R)
# Compute optimal feedback gain matrix
K = -np.linalg.inv(R) |$@$| B.T |$@$| P
# Verify eigenvalues are negative (closed-loop system is stable)
eig_val, eig_vec = np.linalg.eig(A + B |$@$| K)
print(eig_val)

Algorithm 8: Computing the optimal infinite-horizon LQR controller for a simple
double integrator with dynamics ẍ = u in Python. The code for this example
is available in the repository github.com/StanfordASL/pora-exercises in the
notebook ch03/lqr.ipynb.
To simplify the discussion, we further assume Q = Q⊤ ≻ 0. Together with
the stabilizability and detectability assumptions stated above, this guarantees the
existence of a unique stabilizing solution to the algebraic Riccati equation. In
practice, the specific choice of Q and R depends on the designer’s understanding
of the system dynamics and performance objectives. A particularly simple and
commonly adopted approach is to use diagonal weight matrices, where each
diagonal element directly penalizes a corresponding state or control variable:


q1

0
Q=
 ..
.
0

0
q2
..
.
0

···
···
..
.
···


0

0
.. 
,
.
qn



r1

0
R=
 ..
.
0

0
r2
..
.
0

···
···
..
.
···


0

0
.. 
,
. 
rm

where qi > 0 and r j > 0 for all i = 1, . . . , n and j = 1, . . . , m. With this choice,
each diagonal entry directly specifies how strongly the corresponding (squared)
state or input contributes to the overall cost. In general, states (or equivalently,

---

### [PDF p.101 | Book p.99]

closed-loop control & trajectory tracking

control inputs) that are particularly important to regulate are assigned larger
weights, ensuring that deviations in those directions are penalized more heavily.
Conversely, less critical states or inputs are assigned smaller weights, reflecting
their reduced influence on the system’s overall performance.
Finite-horizon formulation. The LQR formulation can be naturally extended to
the finite-horizon setting, where performance is evaluated only over a fixed time
interval [0, t f ]. In this case, the optimal control problem can be formulated as:
⊤

Z t

f

x(t)⊤ Qx(t) + u(t)⊤ Ru(t)dt,

minimize

x(t f ) Q f x(t f ) +

subject to

ẋ(t) = Ax(t) + Bu(t),

u

0

(3.15)

where Q f ∈ Rn×n and Q ∈ Rn×n are symmetric positive semidefinite matrices,
and R ∈ Rm×m is symmetric positive definite. The matrix Q f specifies the terminal cost, penalizing deviations of the state from the origin at the final time
tf .
As in the infinite-horizon case, the optimal control law retains the linear form
u(t) = −K (t) x(t), but the gain matrix becomes time-varying. Specifically, the
optimal gain matrix K (t) is given by:
K ∗ ( t ) = R −1 B ⊤ P ( t ),

(3.16)

where P(t) is the positive semidefinite matrix that solves the continuous-time differential Riccati equation:
Ṗ(t) = − A⊤ P(t) − P(t) A + P(t) BR−1 B⊤ P(t) − Q,
with terminal condition P(t f ) = Q f .
As the horizon length t f tends to infinity, and under the standard assumptions introduced for the infinite-horizon case—namely, that ( A, B) is stabilizable,
( Q, A) is detectable, Q = Q⊤ ⪰ 0, and R = R⊤ ≻ 0—the solution P(t) of the
differential Riccati equation converges to the steady-state solution P of the algebraic Riccati equation from Equation (3.13). Correspondingly, the time-varying
gain matrix K (t) converges to the constant gain matrix K from Equation (3.12). In
practice, for sufficiently long horizons, it is common to use the infinite-horizon
gain directly, thereby avoiding the need to compute or store the entire gain schedule K (t).
Discrete-time LQR. Up to this point, we have focused on continuous-time formulations. However, both the finite-horizon and infinite-horizon problems can be
posed just as naturally in discrete time, where the system evolves according to
the difference equation:
xt+1 = Axt + But ,
(3.17)
and where, as discussed in Chapter 2, the time horizon t f is discretized into
N ∈ N intervals t = 0, 1, . . . , N − 1 of length ∆t = t f /N. In this setting, the

99

---

### [PDF p.102 | Book p.100]

100

principles of robot autonomy

structure of the optimal solution mirrors the continuous-time case, where the
optimal state-feedback law is again linear in the state, ut = −Kt xt , with gains
obtained by solving a Riccati equation—now in its discrete form.
Specifically, the finite-horizon problem in discrete time is formulated as:
N −1

minimize
u

⊤
⊤
x⊤
N Q f x N + ∑ xt Qxt + ut Rut ,

(3.18)

t =0

subject to

xt+1 = Axt + But ,

t = 0, . . . , N − 1,

⊤
⊤
where Q f = Q⊤
f ⪰ 0, Q = Q ⪰ 0, and R = R ≻ 0. The optimal solution is
obtained through a backward Riccati recursion, which proceeds from the terminal
condition PN = Q f and iterates backward in time for t = N − 1, N − 2, . . . , 0
according to:

Pt = Q + A⊤ Pt+1 A − A⊤ Pt+1 B R + B⊤ Pt+1 B

 −1

B⊤ Pt+1 A,

(3.19)

with the corresponding feedback gain:
Kt = R + B⊤ Pt+1 B

 −1

B⊤ Pt+1 A.

(3.20)

This recursion can be viewed as the discrete-time analogue of integrating the
continuous-time differential Riccati equation backward from t f to 0. At each step,
Pt is updated one stage earlier, effectively propagating future cost information
back through time to determine the optimal closed-loop policy.
In the infinite-horizon setting, the problem is formulated as:
∞

minimize
u

subject to

∑ x⊤t Qxt + u⊤t Rut ,

t =0

(3.21)

xt+1 = Axt + But ,

where Q = Q⊤ ⪰ 0 and R = R⊤ ≻ 0. Analogous to the continuous-time case, and
under the standard stabilizability and detectability conditions, the backward Riccati recursion converges—as the horizon length t f tends to infinity—to a steadystate matrix P, which satisfies the discrete-time algebraic Riccati equation:
P = Q + A⊤ PA − A⊤ PB( R + B⊤ PB)−1 B⊤ PA.

(3.22)

The corresponding optimal feedback gain is then time-invariant and given by:
K = ( R + B⊤ PB)−1 B⊤ PA.

(3.23)

Thus, while the overall structure of the LQR solution carries over seamlessly to
discrete time, the computational machinery changes, where instead of solving a
continuous-time differential or algebraic Riccati equation, one either propagates
a backward recursion over a finite horizon (finite case) or solves a fixed-point
equation (infinite case). This recursive viewpoint is also closely aligned with the
principles of dynamic programming, which is a foundational concept in optimal

---

### [PDF p.103 | Book p.101]

closed-loop control & trajectory tracking

control and reinforcement learning and will be discussed in more detail in Chapter 17.
Below, we summarize key extensions of the LQR problem using its discretetime formulation.
Time-varying LQR with cross-quadratic costs. We now consider the finite-horizon,
discrete-time LQR problem with both time-varying dynamics and cross-quadratic
cost terms:

N −1 
1 ⊤
1 ⊤
1
⊤
minimize
xN Q f xN + ∑
xt Qt xt + u⊤
R
u
+
x
S
u
t t
t t t ,
u
2
2
2 t
(3.24)
t =0
subject to

xt+1 = At xt + Bt ut ,

t = 0, . . . , N − 1,

⊤
⊤
where Q f = Q⊤
f ⪰ 0, and where Qt = Qt ⪰ 0, Rt = Rt ≻ 0, and St are
time-varying cost matrices. The system matrices At and Bt are also explicitly
time-dependent, capturing nonstationary dynamics. This formulation extends
the standard LQR problem by incorporating the cross-term matrices St , which
penalize state–control interactions. Such terms naturally arise when the cost of
applying a control action depends on the current system state. For example, in a
vehicle control scenario, the cost of applying a braking force may vary with the
vehicle’s speed.
The optimal solution retains the linear feedback form ut = −Kt xt , with:

Kt = ( Rt + Bt⊤ Pt+1 Bt )−1 ( Bt⊤ Pt+1 At + St⊤ ),

(3.25)

and where the matrices Pt are obtained from the backward Riccati recursion:
⊤
⊤
−1 ⊤
⊤
Pt = Qt + A⊤
t Pt+1 At − ( At Pt+1 Bt + St )( Rt + Bt Pt+1 Bt ) ( Bt Pt+1 At + St ),
(3.26)
with terminal condition Pt f = Q f .

LQR with affine dynamics and quadratic and linear costs. We now consider a more
general discrete-time LQR formulation that incorporates affine dynamics together
with quadratic, linear, and constant terms in the cost. Let Q f = Q⊤
f ⪰ 0, Qt =
⊤
Q⊤
t ⪰ 0, and Rt = Rt ≻ 0. The cost function is given by:
N −1

J ( u ) = h ( x N ) + ∑ g ( x t , u t ),
t =0

1
h( x N ) = x⊤
Q x N + q⊤
f xN + α f ,
2 N f
1
1 ⊤
⊤
g( xt , ut ) = x⊤
t Q t x t + u t R t u t + x t St u t +
2
2
⊤
t = 0, . . . , N − 1,
+ q⊤
t xt + rt ut + αt ,

(3.27)

subject to the affine dynamics:
xt+1 = At xt + Bt ut + ct .

(3.28)

101

---

### [PDF p.104 | Book p.102]

102

principles of robot autonomy

The optimal control policy can be derived using dynamic programming, yielding
a time-varying affine closed-loop control law12 . To streamline notation, let us
define the following intermediate quantities:
1 ⊤
ηt := αt + β t+1 + p⊤
t+1 ct + ct Pt+1 ct ,
2
h x,t := qt + A⊤
p
+
P
c
(
t +1
t +1 t ) ,
t
hu,t := rt + Bt⊤ ( pt+1 + Pt+1 ct ) ,
Hxx,t := Qt + A⊤
t Pt+1 At ,
⊤
Hxu,t := St + At Pt+1 Bt ,
Huu,t := Rt + Bt⊤ Pt+1 Bt .

(3.29)

The optimal law remains affine in the state:
u t = − Kt x t − k t ,

(3.30)

with parameters given recursively by:
PN = Q f ,
pN = q f ,
βN = α f ,
−1
⊤
Kt∗ := Huu,t
Hxu,t
,
−1
k t := Huu,t
hu,t ,

(3.31)

Pt := Hxx,t − Hxu,t Kt∗ ,
pt := h x,t − Hxu,t k t ,
1
kt .
β t := ηt − h⊤
2 u,t
This affine–quadratic formulation generalizes the classical LQR by accommodating affine dynamics and nonhomogenous cost terms. As we will see in the remainder of this chapter, this formulation plays a central role in extending LQR
techniques to nonlinear systems, where such affine and cross-linear structures
naturally arise through linearization and quadratic approximation of the dynamics and cost functions.
In summary, the LQR framework represents a powerful tool for closed-loop
optimal control of linear systems with quadratic costs. As we will see next, the
principles underlying LQR can be extended to tackle more complex scenarios,
including trajectory tracking and nonlinear dynamics.

3.2.2

Linear Tracking Problems

As discussed in the previous section, the LQR framework provides a principled
solution to the regulation problem, in which the goal is to drive the system state to
the origin. In many practical settings, however, tasks may extend well beyond regulation. Robotic manipulators must follow preplanned motions, autonomous vehicles must pass through waypoints, and industrial systems often operate around

In this section, we cite the result without proof and refer the reader to Bertsekas [12] for a detailed derivation of the
optimal solution for various LQR extensions.
12

---

### [PDF p.105 | Book p.103]

closed-loop control & trajectory tracking

103

time-varying setpoints. In such scenarios, the control objective is one of trajectory tracking rather than regulation. Thus, restricting control design to regulation
about the origin is often insufficient for many real-world applications.
The tracking problem can be naturally formulated within the two-step design
paradigm introduced earlier in Equation (3.2). In the first step, an open-loop optimal control problem is solved to obtain a nominal state–control trajectory:

( x̄(t), ū(t)) ,

t ∈ [0, t f ],

that satisfies the system dynamics and optimizes a chosen performance criterion13 . In the second step, a closed-loop controller is designed to ensure that the
actual system trajectory remains close to this nominal trajectory, compensating
for disturbances, modeling errors, and measurement noise.
Formally, consider the linear system given by:
ẋ(t) = Ax(t) + Bu(t),

(3.32)

and let ( x̄(t), ū(t)) denote a nominal trajectory we wish to track, which satisfies
the same dynamics, that is:
x̄˙ (t) = A x̄(t) + Bū(t).

(3.33)

We define the deviation (or error) variables as:
δx(t) = x(t) − x̄(t),

δu(t) = u(t) − ū(t),

(3.34)

which represent the difference between the actual state and control inputs and
their nominal counterparts. By using the definition of δx(t) in Equation (3.34)
and substituting the dynamics from Equations (3.32) and (3.33), we can derive
the dynamics of the deviation variables:
δ ẋ(t) = ẋ(t) − x̄˙ (t)

= [ Ax(t) + Bu(t)] − [ A x̄(t) + Bū(t)]
= A( x(t) − x̄(t)) + B(u(t) − ū(t))
= Aδx(t) + Bδu(t),
which have the same linear structure as the original system, only now expressed
in terms of the deviation variables. This observation is central, as it allows the
direct application of LQR techniques to the tracking problem.
LQR formulation for tracking. Tracking performance can be naturally expressed
through a quadratic cost on the deviation variables:
J (δu(t)) = δx(t f )⊤ Q f δx(t f ) +

Z t
0

f

δx(t)⊤ Qδx(t) + δu(t)⊤ Rδu(t) dt,

(3.35)

where Q ⪰ 0, R ≻ 0, and Q f ⪰ 0 are weighting matrices that penalize deviations
of the state and control from their nominal values. The tracking problem can thus

These nominal trajectories are typically computed using trajectory optimization methods, as discussed in Chapter 2.
13

---

### [PDF p.106 | Book p.104]

104

principles of robot autonomy

be expressed as the finite-horizon optimal control problem:
minimize
δu

subject to

δx(t f )⊤ Q f δx(t f ) +

Z t
0

f

δx(t)⊤ Qδx(t) + δu(t)⊤ Rδu(t) dt,

(3.36)

δ ẋ(t) = Aδx(t) + Bδu(t),

which is precisely the finite-horizon LQR problem introduced in Section 3.2.1,
but now formulated in terms of the deviation variables. Therefore, all the results
derived for finite-horizon LQR apply directly to this tracking formulation, and
the optimal control law takes the form:
δu(t) = −K (t)δx(t),

(3.37)

where K (t) is the time-varying optimal feedback gain obtained by solving the
differential Riccati equation from Equation (3.16).
Finally, substituting the definitions of the deviation variables from Equation (3.34)
yields the optimal control law in terms of the original state and control variables:

u(t) = ū(t) − K (t) x(t) − x̄(t) .
(3.38)
This expression is a clear instantiation of the two-step design paradigm, where
the control input consists of a feedforward term ū(t), derived from the nominal
trajectory, and a feedback term −K (t)( x(t) − x̄(t)) that actively compensates for
any deviations of the actual state from the nominal trajectory.

3.3

Optimal Closed-loop Control for Nonlinear Systems

The previous section focused on linear systems, for which the LQR framework
provides elegant closed-form solutions. However, many real-world systems are
inherently nonlinear, making the extension of optimal closed-loop control to nonlinear dynamics crucial for numerous practical applications.
In this section, we first briefly contextualize dynamic programming and the
HJB equation—two foundational methods for deriving globally optimal closedloop control laws in Section 3.3.1, referring the reader to Chapter 18 and Bertsekas
[12] for a more in-depth discussion. We then turn our attention to approaches
that aim to leverage the structure and insights from linear optimal control to solve
nonlinear optimal control problems. For trajectory-tracking, we begin by showing
how the notion of linearization enables the application of LQR tracking techniques
to nonlinear systems in Section 3.3.2. Finally, we extend ideas from linearization
and LQR to develop algorithms that simultaneously generate an open-loop trajectory and closed-loop tracking controller in two-step design form. Specifically, we
present iLQR and DDP in Section 3.3.3.

3.3.1

Dynamic Programming and the Hamilton–Jacobi–Bellman Equation

When deriving optimal closed-loop control policies for nonlinear systems, one
typically distinguishes between two complementary formulations: discrete-time
and continuous-time.

---

### [PDF p.107 | Book p.105]

closed-loop control & trajectory tracking

In the discrete-time setting, the primary tool is dynamic programming, originally developed by Richard Bellman in the 1950s. Dynamic programming provides a systematic framework for solving optimal control problems with additive cost functions and nonlinear dynamics, and it underlies numerous classical and modern optimal control algorithms, including many learning-based
approaches14 . Intuitively, dynamic programming decomposes the optimization
problem into a sequence of smaller subproblems that can be solved recursively by
exploiting the principle of optimality, which informally states that for a sequence
of optimal decisions, the tail of the optimal sequence is also optimal for a tail subproblem. This recursive structure leads to the celebrated Bellman equation, which
dramatically simplifies the search for optimal policies by transforming the global
optimization problem into a tractable sequence of smaller optimization problems.
In the continuous-time setting, the analogous formulation is given by the HJB
equation. The HJB equation is a nonlinear partial differential equation whose
solution enables the derivation of an optimal control law. Conceptually, it captures the infinitesimal version of the dynamic programming principle, providing
a continuous-time characterization of optimality.
Both the discrete-time dynamic programming paradigm and the continuoustime HJB equation offer powerful, theoretically grounded approaches for deriving
globally optimal closed-loop policies for nonlinear systems. However, they also
suffer from severe computational challenges, such as the curse of dimensionality,
which limit their direct applicability to high-dimensional systems.
Practical methods inspired by dynamic programming principles will be explored further in Chapter 18, while for an in-depth discussion of the HJB framework, we refer the reader to Bertsekas [12].

3.3.2

Linear Methods for Nonlinear Tracking Control

A common strategy for controlling nonlinear systems is to approximate their dynamics locally by a linear system and then apply linear control techniques, such
as LQR tracking from Section 3.2.2. The process of approximating a nonlinear
system by a linear one is called linearization and it leverages the fact that any
smooth nonlinear function can be approximated locally by its first-order Taylor
expansion. Below, we first describe the linearization process and then show how
to apply LQR tracking to the resulting linearized system.
Linearization of nonlinear systems.

Consider the nonlinear system dynamics:

ẋ(t) = f ( x(t), u(t)),

(3.39)

where f : Rn × Rm → Rn is a smooth nonlinear function that governs the system’s evolution. Let ( x̄(t), ū(t)) denote a nominal state and control trajectory that
satisfies the dynamics, that is:
x̄˙ (t) = f ( x̄(t), ū(t)).

(3.40)

105

For instance, reinforcement learning
algorithms discussed in Chapter 18.
14

---

### [PDF p.108 | Book p.106]

106

principles of robot autonomy

For the purposes of trajectory-tracking, we are interested in controlling the system so that it remains close to this nominal trajectory, i.e., such that the state
deviations δx(t) = x(t) − x̄(t) are small. As in the linear case (see Section 3.2.2),
let us first derive the dynamics of these deviation variables and then design a
controller to stabilize them around zero.
Using Equations (3.39) and (3.40), the deviation dynamics can be written as:
δ ẋ(t) = ẋ(t) − x̄˙ (t) = f ( x(t), u(t)) − f ( x̄(t), ū(t)),

(3.41)

where, to approximate the right-hand side, we can linearize the nonlinear function f around the nominal trajectory. Specifically, assuming that the deviations
δx(t) and δu(t) = u(t) − ū(t) are small, a first-order Taylor expansion of f yields:
f ( x(t), u(t)) ≈ f ( x̄(t), ū(t)) +

∂f
∂f
( x̄(t), ū(t)) δx(t) + ( x̄(t), ū(t)) δu(t), (3.42)
∂x
∂u
|
|
{z
}
{z
}
:= A(t)

:= B(t)

where A(t) ∈ Rn×n and B(t) ∈ Rn×m are the Jacobians of f with respect to
the state and control input, evaluated along the nominal trajectory, that is, at
( x̄(t), ū(t)).
Substituting the approximation from Equation (3.42) into Equation (3.41), we
obtain:


δ ẋ(t) ≈ f ( x̄(t), ū(t)) + A(t) δx(t) + B(t) δu(t) − f ( x̄(t), ū(t)),

(3.43)

which yields the linearized dynamics for the deviation variables:
δ ẋ(t) ≈ A(t)δx(t) + B(t)δu(t).

(3.44)

Applying LQR tracking to the linearized system. Once in this form, standard linear control techniques, such as the LQR tracking framework, can be directly
applied to design a feedback controller that stabilizes the deviation dynamics
around zero. For instance, applying the finite-horizon LQR tracking framework
from Section 3.2.2 yields the optimal feedback law:
δu(t) = −K (t) δx(t).
which, expressed in the original variables, gives the closed-loop controller:

u(t) = ū(t) − K (t) x(t) − x̄(t) ,
where K (t) is the time-varying feedback gain computed by solving the differential
Riccati equation associated with the linearized system.
Linearizing around an equilibrium point. A particularly important special case arises
when the nominal trajectory corresponds to a constant equilibrium ( x̄, ū). A state
x̄ is referred to as an equilibrium if there exists a control input ū (called the

---

### [PDF p.109 | Book p.107]

closed-loop control & trajectory tracking

107

equilibrium input) such that f ( x̄, ū) = 0. In other words, if the system is initialized at x̄ and the constant input ū is applied for all t ≥ t0 , the state will remain
fixed at x̄ indefinitely. Linearizing about ( x̄, ū) produces a system of the form
in Equation (3.44), where A and B would be constant matrices (not time-varying)
evaluated at the equilibrium.
Local validity of linearization. It is important to highlight that linearization provides only a local approximation, and the linearized model accurately captures
the system dynamics only in a neighborhood of the nominal trajectory. If the
state deviates significantly from x̄(t), the linear approximation may no longer
hold, and the resulting controller may perform poorly or even destabilize the
system.
Below, we illustrate the linearization process with a concrete example.
Example 3.3.1 (Inverted pendulum). Consider the inverted pendulum shown in
Figure 3.3. Its nonlinear dynamics are given by:
ml 2 θ̈ = mgl sin(θ ) + u,
where m denotes the mass, l is the length of the rod, g is the acceleration due
to gravity, θ is the pendulum angle, and u is the control torque. Introducing the
 ⊤
state vector x := θ θ̇ , the system can be written in state-space form as:
"
#
θ̇
ẋ = f ( x, u) = g
.
1
l sin( θ ) + ml 2 u
The upright stationary position x̄ = [0, 0]⊤ is an equilibrium point for this system
with equilibrium control input ū = 0. Linearizing about this equilibrium—one
where δx = x − x̄ = x and δu = u − ū = u—yields the linear model:
"
#
" #
0
0 1
δ ẋ = g
δx + 1 δu,
0
l
ml 2
whose state matrix has one eigenvalue with positive real part, and is therefore
unstable.
To stabilize the pendulum, we can design a proportional–derivative controller
of the form:
δu(t) = −k p θ (t) − k d θ̇ (t),
which would yield the closed-loop dynamics:
"
#
0
1
δ ẋ = g
δx.
1
1
l − ml 2 k p − ml 2 k d
By selecting suitable gains k p > 0 and k d > 0, we can ensure that both eigenvalues of the closed-loop system have negative real parts, ensuring stability around
the upright position—analogously to the double-integrator PD design in Example 3.1.1. Of course, PD control is only one option, and other methods—such as
the LQR—can also be applied to the linearized model.

Figure 3.3: An inverted pendulum consisting of a point mass m
attached to a rigid rod of length
l. The motion is described by the
angle θ from the upright vertical,
and u denotes the control torque
applied about the pivot.

---

### [PDF p.110 | Book p.108]

108

principles of robot autonomy

Algorithm 9 shows a Python implementation of the linearization process for
the inverted pendulum example using JAX, a library for high-performance numerical computing and automatic differentiation.
Inverted Pendulum Dynamics Linearization
import jax
import jax.numpy as jnp
def inverted_pendulum_dynamics(x, u, g=9.81, m=1, l=1):
"""
Evaluate the inverted pendulum dynamics.
"""
|$\theta$|, d|$\theta$|_dt = x
dx_dt = jnp.array([d|$\theta$|_dt, (g/l)*jnp.sin(|$\theta$|) + (1/m*l**2)*u])
return dx_dt
# Linearize around the stationary upright position with zero
# control (i.e. the pendulum is perfectly balanced)
f_jac = jax.jacobian(inverted_pendulum_dynamics, argnums=(0, 1))
x = jnp.array([0., 0.])
u = 0.
A, B = f_jac(x, u) # Evaluate Jacobian at equilibrium point

Algorithm 9: Linearizing the inverted pendulum dynamics from Example 3.3.1
in Python using the JAX library. The code for this example is available in the
repository github.com/StanfordASL/pora-exercises in the notebook ch03/jax
_linearization.ipynb.

3.3.3

Iterative LQR (iLQR) and Differential Dynamic Programming (DDP)

In the previous sections, we saw how the LQR framework—along with its various extensions—provides a principled foundation for regulation and tracking,
and how the same ideas can be applied to both linear and nonlinear systems.
Specifically, we highlighted how LQR can be naturally embedded within a twostep design paradigm, serving as a practical alternative to directly solving the full
nonlinear optimal control problem by combining elements of open-loop trajectory
generation and closed-loop tracking control.
In this section, we adopt a different yet complementary perspective, and explore how ideas from linearization and LQR can be extended to develop algorithms that simultaneously generate an open-loop trajectory and a closed-loop
tracking controller in two-step design form. This approach leads to two closely
related algorithms: the iterative linear quadratic regulator (iLQR) and differential dynamic programming (DDP). As we will see, the key insight underlying both meth-

---

### [PDF p.111 | Book p.109]

closed-loop control & trajectory tracking

ods is that the structure which makes LQR tractable—namely, quadratic cost and
linear dynamics—can be embedded within an iterative optimization scheme to
efficiently handle nonlinear dynamics and non-quadratic costs.
Iterative LQR. Recall from the LQR tracking problem in Section 3.2.2 that the
controller acts to drive deviation variables (δx, δu) to zero, thereby ensuring the
system follows a specified reference. At its core, iLQR uses the same machinery,
but with a different objective: instead of driving the deviation variables to zero,
the optimal deviations are used to modify the nominal trajectory itself. By repeating
this process, iLQR gradually refines the trajectory until no further improvement
can be made, yielding a locally optimal solution.
Formally, consider the discrete-time finite-horizon nonlinear optimal control
problem:
N −1

minimize
u

h ( x N ) + ∑ g ( x t , u t ),

(3.45)

t =0

subject to

x t +1 = f ( x t , u t ),

t = 0, . . . , N − 1,

Given a feasible nominal trajectory ( x̄0 , ū0 , . . . , x̄ N , ū N ), let us linearize the dynamics and quadratize the cost around the nominal trajectory as:
δxt+1 ≈

∂f
∂f
0 ,
( x̄t , ūt ) δxt +
( x̄t , ūt ) δut + |{z}
|∂x {z }
|∂u {z }
:=ct

:= Bt

:= At

1
h( x N ) ≈ h ( x̄ N ) + ∇ h ( x̄ N ) δx N + δx N ∇2 h ( x̄ N ) δx N ,
2
| {z }
| {z } | {z }
:=α f

:=q f

:= Q f

gt ( xt , ut ) ≈ gt ( x̄t , ūt ) + ∇ x g ( x̄t , ūt ) δxt + ∇u g ( x̄t , ūt ) δut
{z
}
|
{z
}
| {z } |
:=αt

:=qt

(3.46)

:=rt

1
1
+ δx⊤
∇2 gt ( x̄t , ūt ) δxt + δu⊤
∇2 gt ( x̄t , ūt ) δut
2 t | xx {z
2 t | uu {z
}
}
:= Rt

:= Qt

2
+ δx⊤
t ∇ xu gt ( x̄t , ūt ) δut ,

|

{z

:=St

}

where Q, R, S are Hessians and q, r the gradients of the cost with respect to state
and input, evaluated along ( x̄, ū). This reduces the problem to the LQR formulation introduced in Equation (3.27), which can be solved via the Riccati equations
to obtain the optimal deviations (δx∗ , δu∗ ).
iLQR alternates between two complementary steps:
• Backward pass: linearize the dynamics and quadratize the cost around ( x̄, ū).
Solve the resulting LQR problem to obtain the affine control law for the deviation variables:
δu∗t = −Kt δxt − k t .

(3.47)

109

---

### [PDF p.112 | Book p.110]

110

principles of robot autonomy

• Forward pass: starting from the initial condition x0 , propagate the nonlinear
system forward using:
ut = ūt − k t − Kt ( xt − x̄t ),

(3.48)

and update the nominal trajectory to ( x̄, ū) = ( x, u).
These steps are repeated until the trajectory converges, typically measured by
negligible improvement in cost or small changes in the control sequence.
Practical considerations. While iLQR provides a powerful framework for trajectory optimization, its performance depends critically on several implementation
details:
• Local optimality. iLQR produces solutions that are only locally optimal. The
resulting open-loop trajectory ( x̄, ū) minimizes the cost only in a neighborhood
of the initial guess, and the associated feedback law stabilizes the system only
locally. Consequently, a good initialization of the nominal trajectory is often
critical to success.
• Second-order terms. The quadratic expansion of the cost introduces secondorder terms Hxx,t and Huu,t , which in general may not be positive semidefinite
and positive definite, respectively. To ensure well-posed Riccati recursions,
these terms are often regularized to be invertible, for example by adding a
multiple of the identity matrix ( Hxx,t + µI, Huu,t + µI ), with µ > 0, or by
projecting them to the nearest valid matrices.
• Termination criteria. Since iLQR is iterative, a stopping rule must be defined. In
practice, iterations are terminated either when the change in the control trajectory is sufficiently small, or when the improvement in cost between successive
iterations falls below a chosen threshold.
• Forward pass robustness. During the forward pass, care must be taken to ensure
that the updated trajectory does not deviate too far from the one used in the
linearization. Common strategies include penalizing large deviations more
heavily or performing a line search on the step size used to update the controls
and states.
These considerations are critical for achieving robust and efficient performance in
practice. A comprehensive collection of tips and detailed mathematical treatment
of iLQR can be found in Tassa [146].
Differential dynamic programming. Closely related to iLQR is DDP, an algorithm
rooted in both LQR and dynamic programming15 . Like iLQR, DDP alternates between a backward pass (computing locally optimal gains) and a forward rollout
(updating the trajectory). The key difference lies in the treatment of the backward
pass. In iLQR, the dynamics are linearized to first order, so the resulting formulation involves second-order terms only from the cost function. In contrast, DDP

Introduced in Section 3.3.1 and which
will be further discussed in Chapter 17.
15

---

### [PDF p.113 | Book p.111]

closed-loop control & trajectory tracking

111

also expands the dynamics to second order, so that curvature information from
the nonlinear dynamics explicitly enters the Riccati recursion.
Formally, compared to the solution introduced in Equation (3.29), DDP augments the matrices Hxx,t , Huu,t , and Hxu,t with additional second-order terms, as
follows:
n

2
Hxx,t := Qt + A⊤
t Pt+1 At + ∑ pt+1,i ∇ xx f i ( x̄t , ūt ),
i =1

n

Huu,t := Rt + Bt⊤ Pt+1 Bt + ∑ pt+1,i ∇2uu f i ( x̄t , ūt ),

(3.49)

i =1
n

2
Hxu,t := St + A⊤
t Pt+1 Bt + ∑ pt+1,i ∇ xu f i ( x̄t , ūt ).
i =1

In practice, this richer approximation often improves convergence behavior and
solution accuracy, especially in strongly nonlinear systems. However, it also
makes DDP more computationally expensive than iLQR, since it requires evaluating and storing second-order derivatives of the dynamics at every iteration.

3.4

Model Predictive Control (MPC)

We now turn to Model Predictive Control (MPC), also known as Receding Horizon
Control (RHC), which has become one of the most influential methodologies in
modern control, both in theory and in practice. To appreciate its role, it is helpful
to revisit the distinction between open-loop and closed-loop control.
In an open-loop formulation, the control problem is posed as finding a trajectory u(t) that optimizes a given performance criterion subject to system constraints. While conceptually straightforward and computationally cheaper, this
approach does not account for disturbances or deviations from the nominal trajectory that may arise during execution.
By contrast, closed-loop control directly maps the measured state to a control
action through a feedback policy. This design enables the control input to adapt
to the current system state. However, computing optimal feedback policies can
quickly become intractable, even for systems of moderate size16 .
At a high level, MPC can be seen as a principled unification of these two
paradigms, using repeated open-loop optimization to effectively achieve closedloop behavior. At each time step, MPC solves a finite-horizon open-loop optimal
control problem, yielding an input sequence u0 , u1 , . . . , u N −1 . Only the first control action u0 is applied, after which the horizon shifts forward, the state is remeasured, and the optimization is solved again. This receding-horizon strategy
effectively embeds feedback into open-loop optimization, combining the robustness of closed-loop adaptation with the computational tractability of open-loop
planning.
Naturally, MPC requires additional design elements to ensure reliable operation. Two key concerns are persistent feasibility (the guarantee that a valid solution can be found at each step) and stability (ensuring the closed-loop system

Earlier, we introduced PID controllers
and LQR as computationally efficient examples of closed-loop control. These
methods, however, are restricted to relatively simple settings such as linear systems with quadratic costs. More general cases often quickly become computationally prohibitive.
16

---

### [PDF p.114 | Book p.112]

112

principles of robot autonomy

Figure 3.4: The receding horizon principle. At each time
step, a finite-horizon optimal
control problem is solved based
on the current state measurement. Only the first control input is applied, and the process
repeats at the next time step.

behaves well over time). These are typically addressed through terminal constraints, tailored terminal costs, or other problem-specific design choices, which
we will return to later in this section.

Historically, MPC emerged in the 1970s within the process control community,
particularly in chemical engineering. This application domain was ideal for two
reasons. First, safety-critical constraints (e.g., temperature limits) could be enforced explicitly within the optimization problem. Second, chemical processes
evolve on relatively slow timescales, giving ample time to solve optimization
problems online—even with the limited computational power of the era. With
today’s hardware, these limitations have largely disappeared, and MPC is now
deployed in real-time domains such as robotics, where numerical optimization
problems may be solved at tens or hundreds of Hertz.
Today, MPC is considered one of the cornerstones of modern control. Alongside PID control and LQR, it is among the most widely applied methodologies,
valued for its ability to explicitly handle constraints while maintaining robustness. The material in this section provides the foundations necessary to understand and implement MPC. For readers interested in deeper coverage of both
theory and practice, we recommend the textbooks by Borrelli, Bemporad, and
Morari [19] and Rawlings, Mayne, and Diehl [120].

---

### [PDF p.115 | Book p.113]

closed-loop control & trajectory tracking

3.4.1

The Receding Horizon Framework

The underlying setting for MPC is the discrete-time infinite-horizon optimal control problem. That is, in principle, we would like to design a feedback policy
that minimizes a cost accumulated over an infinite time horizon, that is, with
final time t f = +∞. Solving for closed-loop policies in this setting is, however,
typically intractable.
MPC addresses this challenge through a suboptimal—but computationally
tractable—approximation. Essentially, instead of solving the infinite-horizon problem directly, it repeatedly solves a finite-horizon optimal control problem. The
idea is simple and illustrated in Section 3.4.1. At the current time t, the system
state is measured, and an optimal control sequence is computed over a horizon of
length N. As in any open-loop formulation, the optimization relies on the system
model to predict how the state will evolve under candidate input sequences, selecting the one that minimizes the cost over the finite horizon. This process yields
a sequence of control inputs:
u t , u t +1 , . . . , u t + N −1 ,
along with the corresponding predicted state trajectory. Crucially, only the first
control input ut is applied to the system. Once time advances to t + 1, the remaining inputs ut+1 , . . . , ut+ N −1 are discarded, and a new optimization problem
is solved based on the updated state measurement. This process is then repeated
recursively.
This scheme is often referred to as the receding horizon framework, where the
horizon “moves forward” with time, and at each step a new optimization problem
is solved based on the latest state information. While it may appear wasteful to
discard the unused portion of the control trajectory, this is precisely what allows
MPC to incorporate updated measurements and disturbances, ensuring feedback
is embedded into the process.
If the finite-horizon problems are designed and tuned carefully—through appropriate horizon lengths, terminal costs, or constraints—the closed-loop behavior of MPC can closely approximate that of the true infinite-horizon optimal controller. In practice, MPC often achieves performance nearly indistinguishable
from the infinite-horizon optimal solution, while remaining computationally feasible.

3.4.2

Basic Formulation

To formalize the ideas introduced above, consider the discrete-time linear timeinvariant (LTI) system:
xt+1 = Axt + But ,
(3.50)
where xt ∈ Rn and ut ∈ Rm denote the state and input vectors, respectively. Both
are subject to constraints of the form:
xt ∈ X ,

ut ∈ U ,

∀t ≥ 0,

(3.51)

113

---

### [PDF p.116 | Book p.114]

114

principles of robot autonomy

where X ⊆ Rn and U ⊆ Rm are convex polyhedral sets describing admissible
states and inputs.
At time t, given the measured state xt , MPC computes an input sequence over
a prediction horizon of length N:
u t | t , u t +1| t , . . . , u t + N −1| t ,
where the notation ut+k|t indicates “the input applied at time t + k as predicted
at time t”. Correspondingly, we denote the predicted state trajectory as:
x t | t , x t +1| t , . . . , x t + N | t ,

with xt|t = xt .

Finite-horizon problem. The control inputs are obtained by solving the finitehorizon optimal control problem:
N −1

Ut→t+ N |t

h ( x t + N | t ) + ∑ g ( x t + k | t , u t + k | t ),

subject to

xt+k+1|t = Axt+k|t + But+k|t ,

Jt∗ ( xt ) = minimize

k =0

xt+k|t ∈ X , ut+k|t ∈ U ,
xt+ N |t ∈ X f ,

k = 0, . . . , N − 1,

(3.52)

k = 0, . . . , N − 1,

xt|t = xt ,

where Ut→t+ N |t denotes the sequence of decision variables ut|t , . . . , ut+ N −1|t , X f
is a terminal set, and the functions g(·, ·) and h(·) represent stage and terminal
costs.
Control law.
the system:

Only the first element of the optimal input sequence is applied to
ut = u∗t|t ( xt ),

(3.53)

where the dependency on xt arises from the fact that the optimization problem
in Equation (3.52) has the condition xt|t = xt . At the next step, t + 1, the state is
re-measured, and Problem (3.52) is solved again with updated information. This
iterative procedure defines the receding horizon control law, embedding feedback
into the overall process.
Closed-loop dynamics.
as:

The resulting closed-loop system can be written compactly

xt+1 = Axt + Bπt ( xt ) = f cl ( xt ),

t ≥ 0,

(3.54)

where πt ( xt ) := u∗t|t ( xt ) is the MPC feedback law at time t. Because the dynamics,
cost, and constraints are time-invariant, the problem can be equivalently written
by fixing the initial time t = 0. Formally, let x0 = xt and U0 = u0 , . . . , u N −1 , we

---

### [PDF p.117 | Book p.115]

closed-loop control & trajectory tracking

115

can rewrite the problem in Equation (3.52) as:
J0∗ ( xt ) = minimize
U0

subject to

N −1

h ( x N ) + ∑ g ( x k , u k ),
k =0

k = 0, . . . , N − 1,

xk+1 = Axk + Buk ,
xk ∈ X , uk ∈ U ,
xN ∈ X f ,

(3.55)

k = 0, . . . , N − 1,

x0 = x t .

This formulation is often more convenient for analysis, since it avoids carrying
the explicit time index through the condition x0 = xt .
Typical cost functions. In practice, MPC problems are often defined by quadratic
stage and terminal costs of the form:
h( x N ) = x⊤
N Q f xN ,

⊤
g( xk , uk ) = x⊤
k Qxk + uk Ruk ,

(3.56)

with Q f ⪰ 0, Q ⪰ 0, and R ≻ 0. This leads to the overall cost function:
N −1

⊤
⊤
J0 ( x0 ) = x⊤
N Q f x N + ∑ xk Qxk + uk Ruk .

(3.57)

k =0

Quadratic costs are not only natural but also lead to convex optimization problems when paired with polyhedral constraints. Alternative norms, such as ℓ1 or
ℓ∞ , are sometimes used to promote robustness or sparsity in the control actions17 .
Implementation challenges. While MPC provides a powerful framework, it also
raises two critical implementation challenges:
1. Persistent feasibility. Even if the optimization problem is feasible at the current
time step, there is no guarantee that feasibility will be preserved in the future,
as the chosen inputs may drive the system into a region of the state space from
which no admissible solution exists. This situation arises when the controller
fails to “look ahead” sufficiently to maintain long-term feasibility. For example,
consider an autonomous car driving towards an obstacle at high speed, and the
MPC controller chooses to brake too late because of a short-sighted horizon.
As a result, the car may end up in a state where it cannot stop in time to avoid
a collision, leading to infeasibility in subsequent control steps.
2. Closed-loop stability. Feasibility alone does not guarantee that the closed-loop
trajectories converge to the origin. In fact, it is possible for the MPC law to
produce admissible control inputs that indefinitely satisfy the constraints but
fail to stabilize the system.
These issues highlight a fundamental tension: MPC is based on solving shorthorizon problems, yet we ultimately require effective long-term behavior. How
can a strategy that looks only N steps ahead ensure both feasibility and stability
over a potentially infinite horizon?

For instance, ℓ1 penalties are commonly used in predictive control formulations for systems with actuator limitations or to induce sparse actuation.
17

---

### [PDF p.118 | Book p.116]

116

principles of robot autonomy

A central insight is that these properties can be enforced through appropriate
design of the terminal cost and terminal constraint set—denoted as h(·) and X f
in (3.52), respectively. Roughly speaking, the terminal cost serves as a surrogate
for the infinite-horizon tail of the problem, while the terminal set ensures that
the system remains within a region where the behavior is well-understood and
manageable. Together, these design choices represent a flexible tool to reconcile
the short-sighted nature of MPC with the long-term guarantees we ultimately
care about.
While a full treatment of these issues is beyond the scope of this book, we refer
the interested reader to Borrelli, Bemporad, and Morari [19] for comprehensive
discussions and rigorous treatments of these topics.

3.4.3

MPC for Tracking: Delta Input (δu) Formulation

A particularly common use case for MPC is reference tracking, where the objective is to have the system state follow a reference trajectory r0 , r1 , . . . over time.
Here, rt ∈ R p may denote the full state reference (in which case p = n) or a
partial output reference (with p < n). In this section, we introduce the δu formulation18 which is particularly advantageous in trajectory tracking and regulation
tasks around nonzero operating points.
Formally, consider the following LTI system:
xt+1 = Axt + But ,
ut = ut−1 + δut ,

(3.58)

yt = Cxt ,
where δut ∈ Rm represents the change in control input from the previous time
step, yt ∈ R p denotes the system output at time t, and C ∈ R p×n is a linear
transformation mapping the state to the output. Assuming the pair ( A, B) is
controllable, it is often desirable to parameterize the optimization problem in
terms of the control increments rather than the absolute control inputs. Instead of
optimizing the inputs ut , ut+1 , . . . , ut+ N −1 directly, the controller optimizes their
increments:
δut = ut − ut−1 ,

(3.59)

and reconstructs the actual inputs recursively as:
ut = ut−1 + δut ,

(3.60)

with the idea that, once the system has reached a steady state, the control inputs
will remain constant (that is, δut = 0).

F. Borrelli, A. Bemporad, and M.
Morari. Predictive Control for Linear and
Hybrid Systems. Cambridge University
Press, 2017
18

---

### [PDF p.119 | Book p.117]

closed-loop control & trajectory tracking

As a result, the MPC problem can be readily reformulated as:
J0∗ ( xt ) = minimize

N −1

∑ y⊤k Qx̄k + δu⊤k Rδuk ,

δu0 ,...,δu N −1

k =0

subject to

xk+1 = Axk + Buk ,
yk = Cxk ,
xk ∈ X ,

k = 0, . . . , N − 1,

k = 0, . . . , N − 1,
uk ∈ U ,

k = 0, . . . , N − 1,

uk = uk−1 + δuk ,

k = 0, . . . , N − 1,

(3.61)

xN ∈ X f ,
x0 = x ( t ),

u −1 = u ( t − 1 ),

where x(t) and u(t − 1) denote the current state and the last applied control
input, respectively.
Ultimately, the δu formulation does not change the fundamental structure of
MPC but reparameterizes the optimization problem in a way that is better conditioned for tracking tasks.

3.4.4

Receding Horizon as a General Principle for Real-World Control

In practice, virtually all implementations of optimal control—whether framed as
MPC, closed-loop form, or as a two-step design—operate according to the receding horizon framework. Even when a nominal trajectory is first computed offline and subsequently tracked by a feedback controller, the controller is typically
reinitialized and re-optimized as new state information becomes available. In
other words, the nominal trajectory serves only as a temporary reference, continuously adjusted as the system evolves and new measurements are obtained. This
viewpoint helps reconcile the apparent distinction between MPC and trajectorytracking control: both ultimately rely on repeated, finite-horizon optimization
combined with feedback, differing mainly in how frequently and to what extent
the optimization is repeated. Recognizing this continuity is important, as it clarifies that the so-called “receding horizon” behavior is not unique to MPC, but
rather a practical necessity in virtually all control architectures that seek robustness to uncertainty and disturbances.

3.5

Summary

In this chapter, we introduced strategies for closed-loop control and trajectory
tracking. Specifically, we discussed how the goal of closed-loop control is to
compute a control policy that continuously adapts to the system’s evolving state.
While generally more computationally demanding than open-loop methods, closedloop control provides substantial advantages in terms of robustness to disturbances, model inaccuracies, and external perturbations.
We also introduced a tractable compromise through the concept of a two-step
design, in which an open-loop trajectory is first computed and then tracked us-

117

---

### [PDF p.120 | Book p.118]

118

principles of robot autonomy

ing a feedback controller. This formulation allowed us to naturally transition
to trajectory-tracking control, bridging open-loop optimization and closed-loop
stabilization.
Building on these concepts, the chapter presented several key methods for
closed-loop control and trajectory tracking. We began with classical feedback
control, illustrated by the PID controller and its application to trajectory tracking, particularly for differentially flat systems. We then introduced linear optimal
control methods, focusing on the linear quadratic regulator, which provides an elegant closed-form solution for linear systems via the Riccati equation and extends
naturally to tracking problems.
Next, we turned to nonlinear optimal control. We first contextualized techniques for obtaining globally optimal closed-loop solutions—namely dynamic
programming and the HJB equation—and then showed how the notion of linearization enables the use of LQR for local stabilization and trajectory tracking
in nonlinear systems. Building on this, we discussed how algorithms such as
iLQR and DDP extend these principles to simultaneously generate an open-loop
trajectory and a closed-loop tracking controller in two-step design form.
Finally, we presented model predictive control as a powerful framework that
unifies open-loop optimization with closed-loop feedback through a recedinghorizon strategy, offering a versatile method for handling constraints in real-time
applications.

To learn more. For a deeper exploration of the topics covered in this chapter,
several key resources are available. An in-depth treatment of feedback control
and PID controllers can be found in Aström and Murray [9]. For a rigorous
treatment of optimal control from a dynamic programming perspective, which
provides the theoretical underpinnings for the Riccati equation, Bertsekas [12] is
an essential reference. Finally, for comprehensive coverage of model predictive
control, from fundamental principles to advanced theory and applications, we
refer the reader to the textbooks by Rawlings, Mayne, and Diehl [120] and Borrelli,
Bemporad, and Morari [19].

3.6

Exercises

The starter code for the exercises provided below is available online through
GitHub. To get started, download the code by running in a terminal window:
git clone https://github.com/StanfordASL/pora-exercises.git

We denote Problems requiring hand-written solutions and coding in Python
with and , respectively.

---

### [PDF p.121 | Book p.119]

closed-loop control & trajectory tracking

Problem 1: Inverted Pendulum PD Control
In the notebook ch03/exercises/pid_control.ipynb, implement the PD controller for the inverted pendulum dynamics. Then, play around with different
values of the gains k p and k d and use JAX and NumPy to compute the Jacobian of the closed-loop dynamics. Verify the eigenvalues of the linearized matrix
are stable. Finally, run the provided code to simulate the nonlinear closed-loop
dynamics.

Problem 2: Cart-pole LQR Control
In this problem, we consider a cart-pole formulation in which we will design a
controller to balance an inverted pendulum by linearizing the dynamics around
a single stationary point. Therefore, we will consider a trajectory initialized in a
neighborhood about the final, upright state and the optimal control is a closedform solution derived through Riccati recursion. This system has two degrees of
freedom corresponding to the horizontal position x of the cart, and the angle θ
of the pendulum (where θ = 0 occurs when the pendulum is hanging straight
downwards). We can apply a force u ∈ R to push the cart horizontally, where
u > 0 corresponds to a force in the positive x-direction. With the state s :=
( x, θ, ẋ, θ̇ ) ∈ R4 , we can write the continuous-time dynamics of the cart-pole
system as:




ṡ = f (s, u) = 



ẋ
θ̇

−

m p (ℓθ̇ 2 + g cos θ ) sin θ +u
mc +m p sin2 θ
(mc +m p ) g sin θ +m p ℓθ̇ 2 sin θ cos θ +u cos θ
ℓ(mc +m p sin2 θ )





,



where m p is the mass of the pendulum, mc is the mass of the cart, ℓ is the length
of the pendulum, and g is the acceleration due to gravity. We can discretize the
continuous-time dynamics using Euler integration with a fixed time step ∆t to
get the approximate discrete-time dynamics:
sk+1 ≈ sk + ∆t f (sk , uk ),
where sk and uk are the state and control input, respectively, at time t = k∆t. The
code for this exercise is located in
ch03/exercises/cartpole_lqr_control.ipynb.
1. Consider the upright state s̄ := (0, π, 0, 0) with ū := 0, and define s̃k := sk − s̄.
Linearizing the approximate discrete-time dynamics sk+1 ≈ sk + ∆t f (sk , uk )
about (s̄, ū) yields an approximate LTI system of the form:
s̃k+1 ≈ As̃k + Buk .

119

---

### [PDF p.122 | Book p.120]

120

principles of robot autonomy

Express A and B in terms of m p , mc , ℓ, g, and ∆t. You may use the fact that:


0

0

1


0
∂f

(s̄, ū) = 
0
∂s

0

0

0

mp g
mc
(mc +m p ) g
mc ℓ

0




1

,
0 0

0 0



0





 0 
∂f


(s̄, ū) =   .
 1 
∂u
 mc 
1
mc ℓ

We will design a stabilizing LQR controller for this discrete-time LTI system to
solve:

∞ 
1 T
1 T
minimize
∑ 2 s̃k Qs̃k + 2 uk Ruk ,
u
k =0
subject to

s̃k+1 = As̃k + Buk , ∀k ∈ N≥0 ,

for fixed Q, R ≻ 0. Recall that after N iterations of the discrete-time Riccati
recursion:
Kk = −( R + BT Pk+1 B)−1 BT Pk+1 A,
Pk = Q + AT Pk+1 ( A + BKk ),
the cost-to-go matrices { Pk }kN=0 and the time-varying feedback gains {Kk }kN=−01
describe the optimal LQR controller for a finite-horizon version of the problem
above. If ( A, B) is stabilizable, then these iterates asymptotically converge to
some P∞ ≻ 0 and K∞ . In fact, J ∗ (s0 ) := (s0 − s̄)T P∞ (s0 − s̄) is the infinite-horizon
optimal cost-to-go for any initialization s0 , and uk = K∞ s̃k is the optimal feedback
policy, which happens to be linear and time-invariant19 .
2. Write code to approximate P∞ and K∞ for the linearized, discretized cart-pole
system by initializing P∞ = 0 and then applying the Riccati recursion until
convergence with respect to the maximum element-wise norm condition ∥ Pk −
Pk−1 ∥max < 10−4 . Use m p = 2 kg, mc = 10 kg, ℓ = 1 m, g = 9.81 m/s2 ,
∆t = 0.1 s, Q = I4 , and R = I1 . Report the value of K∞ with two decimal
places for each entry.
3. Use the provided code to simulate the continuous-time, nonlinear cart-pole
system with the linear feedback controller u = K∞ s̃. Initialize the system at
s = (0, 3π/4, 0, 0), and use a controller sampling rate of 10 Hz. Verify from the
simulation output that the behavior stabilizes as expected.
4. We will now use an LQR controller to track a time-varying trajectory. Specifically, we will aim to balance the pendulum upright (that is, θ̄ (t) ≡ π) while oscillating the position of the cart to track a desired reference x̄ (t) = a sin(2πt/T ),
where a > 0 and T > 0 are known constants.
(a) Normally, as discussed in this chapter, you would have to re-linearize the
system around the desired trajectory at each time step. Why is this not the
case for this particular problem (that is, why can you just reuse A and B)?

The infinite-horizon LQR problem also
converges for fixed Q ⪰ 0 and R ≻ 0, as
long as ( A, B) is stabilizable and ( A, Q)
is detectable.
19

---

### [PDF p.123 | Book p.121]

closed-loop control & trajectory tracking

(b) Repeat part (c) for this case with a = 10 and T = 10, except this time
initialize the system upright at s(0) = (0, π, 0, 0). For each state plot, overlay
the corresponding entry from the reference trajectory s̄(t).
(c) You may notice that this controller does not have good tracking performance. You could try increasing the state penalty matrix Q to, e.g., Q =
10I4 . However, this should only improve tracking for x (t) and ẋ (t), while
θ (t) and θ̇ (t) still oscillate around π and 0, respectively. What physical characteristic of the desired trajectory (or lack thereof) causes this to happen?

Problem 3: Cart-pole Swing Up (iLQR)
In this problem, we will implement a controller to solve the cart-pole “swing up”
problem and will assume that we do not have actuation constraints. In the swingup problem, the pendulum begins hanging downwards and is then brought to
the upright position. Unlike in the cart-pole balancing problem, it is no longer
sufficient to linearize around a single stationary point. Therefore, we will formulate the optimal control problem into a convex sub-problem and iteratively
solve for optimal perturbations from a reference trajectory. Since we do not consider the case with limited actuation capabilities, the solution to each convex
sub-problem can be solved with Riccati recursion, i.e., we will iteratively develop
our solution using iterative LQR (iLQR) control. In this case, iLQR control provides an elegant and easy to implement closed-loop policy. However, through
the standard LQR formulation at each iteration, we generally cannot reason, at
least directly, over constraints on the state or control space: in the case of limited
actuation, we require the more flexible and sophisticated framework provided
by Sequential Convex Programming. The code for this exercise is located in
ch03/exercises/cartpole_iterative_lqr.ipynb.
Recall that the cart-pole is a continuous-time system with dynamics of the
form ṡ = f (s, u). To compute the iLQR control law, we will consider the Euler
discretized dynamics:
sk+1 ≈ f (sk , uk ) := sk + ∆t f (sk , uk ),

(3.62)

with time step ∆t > 0. The provided code will then simulate this control law on
the original continuous-time system.
1. For a given operating point (s̄k , ūk ), suppose we define the Jacobians:
∂f
∂f
(s̄ , ū ), Bk :=
(s̄ , ū ).
(3.63)
∂s k k
∂u k k
Use JAX in the function linearize to write a single line of code that computes
Ak and Bk , given f , s̄k and ūk .
Ak :=

For our iLQR controller, we will use the quadratic cost function:
J (s, u) :=


1
1 N −1 
(s N − sgoal )T Q N (s N − sgoal ) + ∑ (sk − sgoal )T Q(sk − sgoal ) + uT
Ru
,
k
k
2
2 k =0
(3.64)

121

---

### [PDF p.124 | Book p.122]

122

principles of robot autonomy

where sgoal is the goal state (i.e., the upright position). The entries of Q N ≻ 0 are
chosen to be large so that the terminal cost acts as a soft terminal “constraint”.
2. Rewrite the cost function in terms of the deviations s̃ N := s N − s̄ N , s̃k := sk − s̄k ,
and ũk := uk − ūk . This will result in a quadratic cost function with linear terms
T
T
of the form qT
N s̃ N , qk s̃k , and rk ũk . Identify the vectors q N , qk , and rk .
3. Complete the iLQR controller code in the function
discreteIterativeLQR.solve. Specifically, your code must update the controller gain and offset terms {Yk }kN=−01 and {yk }kN=−01 , respectively20 , the nominal
trajectory (s̄, ū), and the deviations (s̃, ũ).
4. Implement the function compute _ control for the discreteIterativeLQR
class to apply either the open-loop iLQR control input or the closed-loop iLQR
policy, depending on the value of the Boolean flag closed _ loop. Run your
code for both cases to simulate the system and generate plots of the state and
control input over time. You should notice that the iLQR control sequence does
not accomplish the task if applied open-loop.

Problem 4: Linear MPC
In Section 3.4, we introduced some of the fundamental aspects of model predictive control. For this exercise, you will implement a simple MPC scheme for a
linear system to drive the system to the origin while minimizing the cost function:
∞

⊤
J ( x0 ) = ∑ x ⊤
t Qxt + ut Rut ,
t =0

and satisfying the inequality constraints on the state and control, xt ≤ xu , xt ≥ xl ,
and ∥ut ∥∞ ≤ ru . To solve this problem with a finite-horizon MPC scheme, we
will use the cost function from Equation (3.57) which adds a terminal cost and we
will also add a terminal constraint ∥ x N ∥∞ ≤ r N to the problem. In the notebook
ch03/exercises/linear_mpc.ipynb:
1. Implement the function solve_mpc to solve a finite horizon MPC problem with
the quadratic stage and terminal costs, inequality constraints on the state and
control, and the terminal constraint discussed above.
2. Run the provided code to simulate the closed-loop system with the terminal
cost Q f = Q and with no terminal constraint (that is, set r N = ∞). Analyze
the resulting plots, explain why there is a difference between the trajectory
computed in each MPC iteration’s optimization problem and the final closedloop trajectory.
3. Next, run the provided code that specifies a different terminal cost matrix Q f
by the solution to the discrete-time algebraic Riccati equation (DARE) from
Equation (3.22) in the section on the linear quadratic regulator. What do you

In Section 3.3.3, we labeled these terms
as Kt and k t , but here we try to avoid
confusion with the discrete index k.
20

---

### [PDF p.125 | Book p.123]

closed-loop control & trajectory tracking

notice about the difference between the MPC trajectory computed at each time
step and the closed-loop system behavior? Why is this different than when
using Q f = Q? Notice that the total cost of the closed-loop trajectory is lower
when using the DARE terminal cost matrix, why is that?
4. As we discussed in Section 3.4, persistent feasibility is a challenge with MPC,
where we want to guarantee that if we find a feasible solution at one time
step then we will be able to find a feasible solution at future time steps. One
simple solution to this problem is to apply a terminal constraint x N = 0, which
forces the optimizer to find a trajectory to the origin by the end of the finite
horizon, thereby eliminating the issue with being short-sighted. However, this
will cause the controller to be sub-optimal and can require a longer horizon
to find a feasible solution. Run the provided code and play around with the
controller’s horizon, how does the closed-loop trajectory’s cost change as the
horizon changes?

Problem 5: Extended Unicycle Trajectory Tracking Control
In Example 3.1.2, we introduced a closed-loop trajectory tracking problem for a
dynamically extended unicycle model where we apply a PD controller. In this
example, we showed that since the system is differentially flat we could write
its dynamics as the second order linear system in Equation (3.6). From these
dynamics, we can develop a PD controller for the virtual inputs w1 and w2 given
by Equation (3.7), and then can map these virtual controls back into the actual
controls ( a, ω ) algebraically using:
" #
a

"

= J −1 (θ, v)

ω

w1
w2

#
.

In this exercise, you will compute a desired reference trajectory for the extended unicycle and then will design a PD controller to track the reference in
the presence of external disturbances. The code implementation aspects of the
exercise can be completed in the notebook
ch03/exercises/unicycle_trajectory_tracking.ipynb.
1. First, you will design the reference trajectory for the unicycle to follow. While
there are several ways to accomplish this, for this exercise you will use a polynomial basis expansion of the form:
n

xd (t) = ∑ xi ψi (t),
i =1

n

yd (t) = ∑ yi ψi (t),
i =1

where ψi for i = 1, . . . , n are the basis functions, and xi and yi are coefficients
that can be selected. Use the basis functions ψ1 (t) = 1, ψ2 (t) = t, ψ3 (t) = t2 ,
ψ4 (t) = t3 .

123

---

### [PDF p.126 | Book p.124]

124

principles of robot autonomy

(a) Write a set of linear equations in the coefficients xi and yi for i = 1, . . . , 4 to
express the following initial and final conditions:
x (0) = x0 ,
x (t f ) = x f ,

y (0) = y0 ,
y(t f ) = y f ,

v (0) = v0 ,

θ (0) = θ0 ,

v(t f ) = v f ,

θ (t f ) = θ f .

(b) Implement the function compute_traj_coeffs to compute the coefficients
xi and yi .
(c) Then, implement the function compute _ traj to use the coefficients and
the basis functions to compute the full reference trajectory xd (t) and yd (t).
Additionally, compute_traj should also compute vd (t)21 , θd (t), ẋd (t), ẏd (t),
ẍd (t), and ÿd (t).
(d) Now, implement the function compute_controls to compute a(t) and ω (t)
for a given state trajectory. Run the provided code to compute a trajectory
and control sequence for the initial and final conditions:
x (0) = 0,
x (t f ) = 5,

y(0) = 0,
y(t f ) = 5,

1
π
, θ (0) = − ,
2
2
π
1
v(t f ) = , θ (t f ) = − ,
2
2
v (0) =

with t f = 25. Why do we have to choose v(t f ) > 0? What would happen if
we let v(t) = 0 at some point along the trajectory?
(e) Run the provided code to simulate the unicycle system with the controls a(t)
and ω (t) computed previously in open-loop while subject to disturbances.
Notice how the system does not reach the target state in the presence of
noise.
2. Now that we can compute a reference trajectory for the unicycle to follow, we
want to compute a closed-loop controller to track the trajectory robustly in
the presence of disturbances. Specifically, you will use the PD controller from
Equation (3.7) to compute the virtual controls w1 and w2 .
(a) Write down a system of equations for computing the control inputs a and
ω in terms of the virtual controls w1 = ẍ and w2 = ÿ and the unicycle state
x = [ x, y, v, θ ]⊤ . Use this to implement the function
TrajectoryTracker.compute_control.
(b) Run the provided code to run the closed-loop tracking controller. How
does the performance compare to the open-loop? Experiment with different
starting and ending conditions, and different amounts of noise.

Hint: from
p the dynamics model we can
see v = ẋ2 + ẏ2 .
21

---

### [PDF p.127 | Book p.125]

closed-loop control & trajectory tracking

References
[9]

K. J. Aström and R. M. Murray. Feedback Systems. Princeton University
Press, 2009.

[12]

D. Bertsekas. Dynamic Programming and Optimal Control. Athena Scientific,
2000.

[19]

F. Borrelli, A. Bemporad, and M. Morari. Predictive Control for Linear and
Hybrid Systems. Cambridge University Press, 2017.

[80]

J. Levine. Analysis and Control of Nonlinear Systems: A Flatness-based Approach. Springer, 2009.

[101]

R. M. Murray. Optimization-Based Control. California Institute of Technology, 2009.

[120]

J. Rawlings, D. Q. Mayne, and M. Diehl. Model Predictive Control: Theory,
Computation, and Design. Nob Hill Publishing, 2017.

[146]

Y. Tassa. Theory and Implementation of Biomimetic Motor Controllers. PhD
Thesis. The Hebrew University of Jerusalem, 2011.

125

---

### [PDF p.128 | Book p.126]

> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]
