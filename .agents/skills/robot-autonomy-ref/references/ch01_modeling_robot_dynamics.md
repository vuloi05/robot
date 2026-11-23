# Ch 1: Modeling Robot Dynamics (Wheeled Robot Motion Models)

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Part I: Motion Planning & Control
- **Trang sách:** 25–54 | **Trang PDF:** 27–56
- **Độ ưu tiên cho dự án:** `CỐT LÕI`
- **Tóm tắt:** Mô hình không gian trạng thái, động học & động lực học, mô hình xe bánh vi sai (unicycle/diff-drive), ràng buộc Pfaffian.

---

### [PDF p.27 | Book p.25]

1
Modeling Robot Dynamics
Robots can take on a wide variety of forms: they may have rigid or flexible structures, rely on different types of actuators for control, perceive their surroundings
through diverse sensing modalities, or even exist as purely virtual agents. Despite this variety of embodiments, nearly all robotic systems share a fundamental
characteristic—they are dynamic agents whose states evolve over time. The most
immediate example of robot dynamics is physical motion, encompassing changes
in position, velocity, joint configurations, and sensor orientations. A deep understanding of the dynamical properties of a robotic system is essential to its effective
design and control. For instance, building a bipedal robot capable of walking or
running requires detailed modeling of its motion to ensure that the mechanical
structure and actuators can withstand the forces and torques involved. Accurate dynamic models are also critical for designing control strategies that achieve
stable, efficient, and responsive locomotion.
This chapter introduces several foundational topics in modeling robotic systems. We will start with Section 1.1 by introducing the concept of a state space
model, which provides a mathematical framework to describe the behavior of a
robot’s state over time. Next, in Section 1.2, we will detail how a robot’s kinematics and dynamics are used to derive these state space models, focusing on the
principles that govern physical motion and constraints. We will then explore specific motion models for wheeled robots in Section 1.3, including the unicycle and
differential drive models, to illustrate practical applications of these concepts. Finally, in Section 1.4, we will discuss computational techniques for simulating robot
dynamics, emphasizing numerical integration methods such as the Euler and
Runge-Kutta methods to approximate and analyze the time evolution of robotic
systems.

1.1

State Space Models

A state space model is a mathematical framework for describing the behavior of
a dynamical system. Every state space model consists of two key components: a
state and a model.

---

### [PDF p.28 | Book p.26]

26

principles of robot autonomy

Definition 1.1.1 (State). The state of a dynamical system at time t0 is a minimal
set of variables x(t0 ) such that, given the control input u(t) for all t ≥ t0 , the
future evolution of the system’s state x(t) for all t ≥ t0 is uniquely determined,
independently of the system’s behavior for t < t0 .
Formally, the state is a sufficient statistic of the system’s history: given the
current state and the external inputs to the system, the system’s future behavior
is fully determined, independently of how that state was reached. The state of a
robotic system can be finite or infinite-dimensional. For example, a simple mobile robot with a rigid body can be represented by a finite and low-dimensional
state (e.g., the position and velocity of its center of mass), whereas a flexible robot
might require an infinite-dimensional state to describe the continuous deformation of its body (e.g., a deflection function that describes the displacement at every
point along the robot’s length).
When modeling the dynamics of a robot, it is important to define the state
in a way that aligns with the specific goals and requirements of the application.
In practice, the complexity of the state representation can often be reduced by
omitting parts of the robot’s dynamics that are irrelevant to the problem at hand.
For instance, in developing software to enable an autonomous car to navigate
urban environments, it may be sufficient to model only its position, orientation,
and velocity, while abstracting away the internal mechanics of the engine, tires,
or suspension. Conversely, if the car is being designed for high-performance
racing, these specifics become critical to accurately capture and optimize its behavior. Throughout this book, we focus on applications where the state is finitedimensional and represent it as a vector x ∈ Rn , referred to as the state vector.
The second key component of a state space model is the model itself, which
defines the rules and equations governing the evolution of the state over time by
relating it to a set of inputs and outputs.
The inputs to a model refer to external factors or control signals that influence
the behavior of the system.1 These can include forces, torques, voltages, commands, or any other external stimuli that drive the system’s dynamics. As with
the state, the dimensionality of the input may vary, but throughout this book we
assume the input is represented by a finite-dimensional vector, u ∈ Rm .
The outputs of a model are the observable variables or measurements derived
from the system. These typically come from sensors or other measurement devices that capture data reflecting the system’s state and behavior. For example,
a robot equipped with a global navigation satellite system (GNSS) sensor may
directly measure its position but not its heading. In some cases, the relationship
between the state and the output is complex—for example, the connection between a robot’s inertial pose and a red-green-blue-depth (RGB-D) camera image.
The process of inferring the state from the outputs is referred to as state estimation, and it will be explored in detail in Chapters 11 - 15. We assume the output
is finite-dimensional and denote it by the vector y ∈ Rq .
Definition 1.1.2 (Model). A model describes the evolution of a dynamical system

The term input is used interchangeably
with control and action in different domains of robotics.
1

---

### [PDF p.29 | Book p.27]

modeling robot dynamics

27

through two types of equations: state equations and observation equations. The
state equations specify how the state evolves as a function of the current state
and inputs, while the observation equations define how the state influences the
measurable outputs.
State equations are typically modeled as differential equations2 describing the
changes in the state with respect to an independent variable, usually time:
ẋ = f ( x(t), u(t)),

(1.1)

dx(t)

where ẋ = dt is the time derivative of the state vector x(t), and f : Rn × Rm →
Rn is the dynamics function of the system.
Observation equations take the form:
y(t) = h( x(t), u(t)),

(1.2)

where y(t) denotes the output at time t, and h : Rn × Rm → Rq is a function that
relates the state and inputs to the system’s output.
Together, the definitions of the state x, input u, output y, and Equations (1.1)
and (1.2), form the state space model3 .
Throughout this book, we assume that time is the independent variable and
simplify our notation by writing θ in place of θ (t) for time-dependent variables.
Accordingly, we use θ̇ to represent time derivatives, θ̈ =
tives, and θ (m) =

dm θ (t)
dtm for higher-order derivatives.

d2 θ ( t )
for second derivadt2

In summary, state space models provide a powerful formalism for modeling,
analyzing, and controlling robotic systems. Mastering and effectively utilizing
state space models is crucial for advancing robotic capabilities, enabling systems
to autonomously navigate, interact, and adapt in dynamic and complex environments.

1.1.1

Ordinary differential equations are
most commonly used to model robotic
systems. However, partial differential
equations may be needed for more complex cases, such as systems with flexible
or deformable structures, where dynamics vary over both space and time.
2

In some contexts, it may be convenient to represent the evolution of a system using discrete-time difference equations. As we will discuss in Chapter 2, discrete-time models are particularly well-suited for systems that naturally evolve in discrete steps, or for
approximating continuous-time systems
within computational frameworks.
3

Types of State Space Models

State space models, as represented in Equation (1.1) and Equation (1.2), can be
classified based on two key properties: linearity and time-invariance.
A model is said to be time-invariant if the functions f and h do not explicitly
depend on time t; otherwise, it is time-varying. A model is said to be linear4 if
the functions f and h are linear functions of both the state x and control u. More
generally, a system is linear if it satisfies the superposition principle, which states
that the response to a linear combination of inputs is the corresponding linear
combination of the individual responses. Formally, if x1 (t) and x2 (t) are solutions
corresponding to inputs u1 (t) and u2 (t), respectively, then for any scalars α, β ∈
R, the trajectory αx1 (t) + βx2 (t) is a solution corresponding to the input αu1 (t) +
βu2 (t). If this property does not hold, the system is said to be nonlinear.
Example 1.1.1 (Linear time-invariant model). Consider the system:
ẋ = x + u,
y = x.

4

Often referred to as a linear system.

---

### [PDF p.30 | Book p.28]

28

principles of robot autonomy

This model is linear and time-invariant because the functions describing the system depend linearly on x and u and there is no explicit time dependence.
Example 1.1.2 (Nonlinear time-varying model). Consider the system:
ẋ = tx + u,
y = x2 .
This model is nonlinear due to the quadratic output term x2 , and it is also timevarying because the state equation explicitly depends on time through the term tx.
Note, however, that the state equation ẋ = tx + u is linear, as it satisfies the
superposition principle with respect to x and u. Therefore, the nonlinearity in
this system arises solely from the output equation, not from the state dynamics.
Linear models and their standard form. Linear models are particularly important
due to their analytical tractability and widespread applicability. They are commonly expressed in a standard matrix form:
ẋ = A(t) x + B(t)u,
y = C (t) x + D (t)u,

(1.3)

where the matrices A(t), B(t), C (t), D (t) are of appropriate dimensions and define the linear relationships for the state dynamics and the output. We refer to the
matrix A(t) as the dynamics matrix, B(t) as the control matrix, C (t) as the output
or sensor matrix, and D (t) as the direct or feed-forward matrix5 .
Despite the inherent nonlinear nature of many real-world systems, linear models are often employed due to their simplicity and ease of manipulation. A common practice is to approximate nonlinear systems with linear models around
specific operating points using a technique known as linearization. As we will discuss in Chapter 3, this approach simplifies analysis and control design, making
linear models a fundamental tool in engineering and control theory.

1.1.2

Converting Higher-Order Models Into State Space Form

The state space model, as described by Equation (1.1), is represented by first-order
differential equations. However, many robotics applications involve higher-order
differential equation models, such as those governing the dynamics of robotic
arms or wheeled robots. To analyze and control these systems in a unified framework, we can convert higher-order models into first-order state space form by
introducing additional state variables.
Consider a linear n-th order differential equation:
θ (n) + an−1 θ (n−1) + . . . + a1 θ̇ + a0 θ = u,

(1.4)

where ai ∈ R are constants and θ is the state variable. To convert this differential
equation into state space form, that is, a set of first-order differential equations,

If
the
matrices
A ( t ), B ( t ), C ( t ),
and D (t) are time-invariant, we have
a Linear Time-Invariant (LTI) system,
which is a cornerstone of control theory.
5

---

### [PDF p.31 | Book p.29]

modeling robot dynamics

29

we can define an n-dimensional state vector:
 ( n −1) 
 
θ
x1
 ( n −2) 
 

θ
 x2 



x=
 ..  :=  ..  .
 . 
 . 
xn
θ
Given that ẋ1 = θ (n) , ẋ2 = x1 , ẋ3 = x2 and so on, we can express the higher-order
differential equation as a system of first-order state space equations:
  
  
u
− a n −1 x 1 − . . . − a 0 x n
ẋ1
  
  
x1
 0
 ẋ2  
+..
 . =
..
 .
 .  
 .
 .  
.
ẋn

x n −1

0

In this particular case, the model is linear, so it can be represented in matrix form:


 
− a n −1 − a n −2 . . . − a 1 − a 0
1

 1
0
...
0
0 
 

0


0
1
0
0  x ( t ) +  .  u ( t ).
ẋ = 
.


.. 
 ..
.
..

 .
.
.
0
0
0
1
0
Let us consider a practical example of this technique:
Example 1.1.3 (Converting Newton’s second law to state space form). Many
robotic systems, such as robotic arms and wheeled robots, involve dynamics that
can be described by Newton’s second law. Understanding how to convert these
higher-order dynamics into state space form is crucial for controlling and analyzing numerous robotics systems.
Newton’s second law describes the acceleration response of a mass m resulting
from a force F:
F = ms̈,
where s represents the one-dimensional positional displacement of the mass.
Newton’s second law, in this form, is a classic example of a double integrator
system6 .
To convert this second-order differential equation into state space form, we
first define the state vector:
" #
s
x :=
.
ṡ
Then, we represent the dynamics in state space form:
"
#
" #
0 1
0
ẋ =
x + 1 u,
0 0
m
where u represents the applied force F. By defining the state vector x and expressing the original second-order differential equation in this manner, we have
effectively transformed it into a set of first-order differential equations.

In control theory, a double integrator
describes a system in which the output
(here, the position s) is obtained by integrating the input (acceleration) twice.
6

---

### [PDF p.32 | Book p.30]

30

principles of robot autonomy

1.2

Kinematics and Dynamics

Understanding a robot’s physical motion is essential for enabling its autonomous
operation. For instance, it is crucial to determine how an autonomous vehicle’s
actions, such as adjusting throttle and steering, affect its state and interaction with
the environment. Similarly, it is important to understand how a robot manipulator’s movements impact its ability to manipulate objects. A crucial aspect of this
understanding involves the concepts of kinematics and dynamics, which govern
the robot’s physical motion and the constraints it must adhere to.
Definition 1.2.1 (Kinematics). Kinematics is the study of the motion of physical
systems, concerned with describing positions, velocities, and accelerations over
time, without reference to the forces or torques that produce the motion.
A robot’s kinematics outline limitations on its motion that are determined by
its physical state or geometry. These constraints arise from the physical structure
of the system, such as joint limits, actuator placement, linkage geometry, and the
ways in which different components are mechanically connected. They determine
how the system can move, independent of any external forces. For example,
consider a wheeled robot. Static friction restricts the wheels from sliding laterally,
meaning they cannot move in the direction parallel to the rotation axis. This
kinematic constraint significantly limits the robot’s ability to navigate and affects
its overall maneuverability. By understanding these constraints, one can better
grasp the feasible movements of the robot within its environment, which in turn
informs how it can effectively interact with the world around it.
Definition 1.2.2 (Dynamics). Dynamics is the study of the motion of physical
systems as determined by the forces and torques acting upon them. It seeks to
relate a system’s motion to the underlying physical causes of that motion, such
as gravity, friction, or applied inputs.
In the context of robotic or mechanical systems, dynamics are typically governed by Newton’s Second Law, which states that the acceleration of a body is
proportional to the net force acting on it. For example, the dynamics of an autonomous vehicle are described by the relationship between its acceleration and
the external forces acting on it, including tire-road interaction, gravitational effects on slopes, and aerodynamic drag.
From the definitions above, kinematics describe constraints that arise from
the robot’s physical state or geometry, whereas dynamics explain how forces or
inputs influence the robot’s motion. In this section, we first introduce the concept
of generalized coordinates for defining the physical configuration of a robot and
discuss how the robot’s kinematics and dynamics can be expressed in terms of
these coordinates. Then, we will demonstrate how to use the system’s kinematics
and dynamics to define a state space model for the robot’s physical motion. In
the following chapters, we will explore how these models are applied to develop
robust and high-performing algorithms for motion planning and control.

---

### [PDF p.33 | Book p.31]

modeling robot dynamics

1.2.1

Generalized Coordinates

A robot’s physical state, also referred to as its configuration, provides a complete
specification of the position of every point on the robot at a given instant 7 . A
configuration can be represented using a set of variables known as generalized
coordinates, denoted by q(t) ∈ Rn g . Generalized coordinates form a set of parameters that uniquely describe the robot’s configuration relative to a reference frame.
Depending on the system, they may include joint angles, Cartesian positions, orientations, or other parameters defining the robot’s physical arrangement8 .
Importantly, the configuration, namely the generalized coordinates, typically
constitutes only a part of the full system state x. As discussed in previous sections, in a state-space model, the state is a complete set of variables sufficient
to determine the system’s future evolution, given an external input. This usually includes both the generalized coordinates q and their time derivatives, called
generalized velocities, denoted as q̇. In some systems, the state may also include
additional internal variables such as actuator dynamics, sensor states, or environmental parameters.
Example 1.2.1 (Rolling Wheel). The configuration of a wheel rolling on a plane,
as illustrated in Section 1.2.1, can be represented by three parameters: the contact
point position coordinates ( x, y) and the heading angle θ relative to a fixed reference frame. This set of parameters, q = [ x, y, θ ]⊤ , constitutes just one possible
choice of generalized coordinates to define the wheel’s configuration. Alternatively, the configuration could also be represented using the heading angle θ
along with a polar coordinate representation of the contact point position.

1.2.2

Kinematic Constraints

Once a specific set of generalized coordinates, q, is chosen to represent a robot’s
configuration, we can identify the relevant kinematic constraints for the robot.
These kinematic constraints establish relationships between the generalized coordinates and the generalized velocities, thereby describing the limitations on the
robot’s motion. We refer the reader to Siciliano et al. [132] for a comprehensive
treatment of robotic kinematics and the formulation of the associated constraint
equations.
Definition 1.2.3 (Kinematic Constraints). Kinematic constraints are a set of con-

31

Figure 1.1: Generalized coordinates for a wheel rolling without
slipping on a plane.
T. Lozano Perez. “Spatial planning: a
configuration space approach”. In: Autonomous Robot Vehicles. 1990
7

The terms “configuration” and “generalized coordinates” are often used interchangeably. However, while the configuration refers to the robot’s physical arrangement in space, generalized coordinates are a specific mathematical representation of that arrangement. Multiple
choices of generalized coordinates may
represent the same configuration.
8

---

### [PDF p.34 | Book p.32]

32

principles of robot autonomy

straints imposed on the generalized coordinates, q, and generalized velocities, q̇.
We express kinematic constraints mathematically as:
ãi (q, q̇) = 0,

i = 1, . . . , k < n g ,

(1.5)

where k is the number of constraints and n g is the number of generalized coordinates.
In many robotics applications, kinematic constraints are linear with respect to
the generalized velocities. These are known as Pfaffian constraints, and can be
mathematically expressed as:
ai⊤ (q)q̇ = 0,

i = 1, . . . , k < n g ,

(1.6)

where ai (q) ∈ Rn g . Pfaffian constraints can also be compactly represented in
matrix form as:
A⊤ (q)q̇ = 0,
(1.7)
where A(q) ∈ Rn g ×k .
Example 1.2.2 (Pendulum). Figure 1.2 shows a simple pendulum with a point
mass and a rigid, massless, rod that rotates about a fixed pivot point. We can
choose to represent the configuration of the pendulum by the Cartesian coordinate position of the mass, assuming the pivot point is the reference frame origin.
The generalized coordinate vector for this choice is q = [ x, y]⊤ , and the generalized velocity vector is q̇ = [ ẋ, ẏ]⊤ . The fact that the rod connecting the pivot point
to the mass is rigid introduces a restriction on the motion of this system, which
we represent by the kinematic constraint:
ã1 (q, q̇) = x2 + y2 − L2 = 0,

(1.8)

where L is the length of the rod. While this constraint is not in Pfaffian form, we
can equivalently express it as a Pfaffian constraint by noting that:
∂ ã1 (q, q̇)
= 0.
∂t
For the pendulum kinematic constraint in Equation (1.8), we have:
ã1 (q, q̇) = 0 =⇒

∂ ã1 (q, q̇)
= 2x ẋ + 2yẏ,
∂t
and therefore we can write the constraint in the Pfaffian form of Equation (1.6)
with:
h
i
ai⊤ (q) = 2x 2y .
(1.9)
The Pfaffian constraint in Equation (1.9) implies that Equation (1.8) holds as long
as the pendulum starts in a state q(0) satisfying ã1 (q(0)) = 0.
An alternative choice of generalized coordinates to represent the pendulum’s
configuration is to consider the angle θ between the vertical and the pendulum’s
rod orientation, q = [θ ]. This choice fully specifies the configuration without
requiring us to define any kinematic constraints, making it a more natural choice
for this system. Note that since x = L sin θ and y = − L cos θ the kinematic
constraint in Equation (1.8) is trivially satisfied for all θ.

Figure 1.2: Generalized coordinates for a simple pendulum.

---

### [PDF p.35 | Book p.33]

modeling robot dynamics

Example 1.2.3 (Rolling Wheel). Consider the wheel illustrated in Section 1.2.1,
which we can represent with the generalized coordinates q = [ x, y, θ ]⊤ . For this
system, we can assume that the friction at the contact point between the wheel
and the surface induces a no-slip condition. This no-slip condition is a constraint
on the motion of the wheel that restricts the velocity component of the wheel in
the lateral direction to always be zero. Since the unit vector ev = [cos θ, sin θ ]⊤
describes the heading of the wheel, the lateral direction is given by the perpendicular unit vector ev,⊥ = [sin θ, − cos θ ]⊤ . We can compute the lateral velocity
from the dot product of the lateral direction unit vector and the velocity vector, v = [ ẋ, ẏ]⊤ , which gives the no-slip kinematic constraint:
a1 (q, q̇) = ẋ sin θ − ẏ cos θ = 0.

(1.10)

This constraint is linear in the generalized velocities, ( ẋ, ẏ), and therefore is a
Pfaffian constraint.

1.2.3

Holonomic and Nonholonomic Constraints

Kinematic constraints often fall into two categories: holonomic or nonholonomic,
depending on how they restrict the motion of the system. Holonomic constraints
can be expressed solely as functions of the generalized coordinates, without involving generalized velocities. In contrast, nonholonomic constraints involve the
generalized velocities and cannot be expressed solely in terms of the generalized
coordinates.
Definition 1.2.4 (Holonomic Constraints). Kinematic constraints that can be expressed in the form:
ãi (q) = 0, i = 1, . . . , k < n g ,
(1.11)
are called holonomic.
In robotics applications, holonomic constraints generally arise due to mechanical interconnections, such as rigid links and joints of a robotic arm. We refer to a
system that is only subject to holonomic constraints as a holonomic system. These
constraints are a unique subclass of kinematic constraints that restrict the accessible configurations of the system. Specifically, for a system with n generalized
coordinates under k holonomic constraints, the dimension of the space of accessible configurations is n − k. Holonomic constraints can always be equivalently
expressed as Pfaffian constraints of the form Equation (1.6). This is because:
ãi (q) = 0 =⇒

∂ ãi (q)
= 0,
∂t

and by differentiating the expression:
∂ ãi (q)
∂ ã (q)
= i
q̇ = ai⊤ (q)q̇,
∂t
∂q

(1.12)

as we demonstrated in Example 1.2.2. However, it is important to note that not
all Pfaffian constraints are holonomic. For a Pfaffian constraint to be holonomic,

33

---

### [PDF p.36 | Book p.34]

34

principles of robot autonomy

it must be integrable to the form in Equation (1.11). Specifically, there must exist
a scalar function ãi (q) such that:
ai⊤ (q)q̇ =

∂ ãi (q)
q̇ = 0.
∂q

(1.13)

This implies that the Pfaffian constraint, when integrated, yields a constraint
solely dependent on the generalized coordinates q, without any explicit dependence on their time derivatives q̇.
Example 1.2.4 (Pendulum). Consider the pendulum from Example 1.2.2. The
kinematic constraint in Equation (1.8) restricts the pendulum mass to lie on a
circle of radius L, which is a subset of all possible generalized coordinates. This
constraint is holonomic since we can express it as a function of only the generalized coordinates.
Example 1.2.5 (Rolling Wheel). Consider the wheel from Example 1.2.3, where
the kinematic constraint in Equation (1.10) restricts the direction of motion. In
contrast to the pendulum, this constraint does not limit the wheel’s ability to
reach any configuration of generalized coordinates, namely the position and
heading. Mathematically, we cannot integrate the constraint in Equation (1.10)
to yield a constraint of the form ãi (q) = 0, and thus this constraint is not holonomic.
While holonomic constraints restrict the system’s accessible configurations,
kinematic constraints can also limit the motion between configurations. We refer
to these constraints as nonholonomic constraints. A system that is subject to at
least one nonholonomic constraint is referred to as a nonholonomic system.
Definition 1.2.5 (Nonholonomic Constraints). Constraints that can be described
in Pfaffian form, ai (q)⊤ q̇ = 0, but cannot be integrated to the form ãi (q) = 0 are
called nonholonomic.
That is, the Pfaffian expressions cannot be written as the total time derivative
of any scalar function that depends only on the generalized coordinates. In other
d
words, there exists no scalar function ãi (q) such that dt
ãi (q) = ai (q)⊤ q̇. Geometrically, nonholonomic constraints restrict the instantaneous generalized velocities
to lie in the null space of A(q)⊤ , where A(q) is the matrix whose rows are the
vectors ai (q)⊤ corresponding to each nonholonomic constraint.
Example 1.2.6 (Rolling Wheel). Consider the wheel example from Example 1.2.3,
which has a nonholonomic constraint:
h
i
a1 (q)⊤ q̇ = sin θ − cos θ 0 q̇ = 0.
The null space of a1 (q)⊤ in this case is spanned by the vectors [cos θ, sin θ, 0]
and [0, 0, 1], which suggests that all motion must be made up of a linear combination of these vectors. Intuitively, we expect this because [cos θ, sin θ, 0] is the
rolling direction and [0, 0, 1] is the axis the wheel rotates about.

---

### [PDF p.37 | Book p.35]

modeling robot dynamics

35

In summary, holonomic constraints restrict a system’s motion by confining
its configurations to lower-dimensional manifolds—specifically, level sets defined
by scalar equations of the form ãi (q) = 0. For a system with n generalized coordinates and k independent holonomic constraints, the configuration space is
effectively reduced to a manifold of dimension n − k. This reduction reflects a
true loss of accessibility in the configuration space: the system can only evolve
along a restricted subset of configurations determined by the initial conditions
and the constraint equations. In contrast, nonholonomic constraints act directly
on the system’s instantaneous velocities, typically expressed in Pfaffian form
as A(q)⊤ q̇ = 0, where A(q)⊤ is a full-rank matrix of dimension k × n. These
constraints restrict the allowed directions of motion at each configuration by confining q̇ to lie in an (n − k )-dimensional subspace. However, since nonholonomic
constraints are not integrable, they do not reduce the dimensionality of the configuration space itself. That is, although motion is constrained at each instant,
the system may still be able to reach any configuration in the configuration space
through admissible trajectories that respect the velocity constraints. Thus, while
holonomic constraints reduce the number of independent configuration variables
and confine the system to a lower-dimensional subset of the configuration space,
nonholonomic constraints preserve full accessibility of the configuration space
but restrict how that space can be traversed.

1.2.4

Kinematic Models

Once we have chosen an appropriate set of generalized coordinates q and have
identified the relevant kinematic constraints, we can convert the kinematic constraints into a state space model of the form in Equation (1.1), which we refer to
as a kinematic model.
Definition 1.2.6 (Kinematic Model). Given a generalized coordinate vector q ∈
Rn g , and k Pfaffian constraints9 , A⊤ (q)q̇ = 0, a kinematic model is a state space
model of the form:
q̇ = G (q)u,
(1.14)
where u ∈ R p is the input and where the column space of G (q) ∈ Rn g ×n g −k spans
the null space of A⊤ (q).
Each input in u corresponds to one degree of freedom of the system, and
for any initial condition q(0) and sequence of inputs u(t) the solutions to the
kinematic model are guaranteed to satisfy the Pfaffian constraints. We can prove
that the trajectories of the kinematic model will satisfy the Pfaffian constraints by
writing the model in the equivalent form:
n−k

q̇ = G (q)u = ∑ gi (q)ui ,
i =1

where gi ∈ R is the i-th column of G and ui is the i-th input. In this form, we
can more easily see that each input acts on the generalized velocity q̇ through
ng

These Pfaffian constraints can come
from a combination of holonomic and
non-holonomic constraints.
9

---

### [PDF p.38 | Book p.36]

36

principles of robot autonomy

a particular mode that is defined by the vector gi . Since we have specified in
Theorem 1.2.6 that the column space of G spans the null space of A⊤ (q), we
know that by definition:
A⊤ (q) gi (q)ui = 0,
for any input ui ∈ R and for all coordinates q. Therefore, by definition each
component of the input vector can only influence the generalized velocity in a
way that satisfies the Pfaffian constraints. Another way to see this mathematically
is by substituting the kinematic model into the Pfaffian constraint equation:
A⊤ (q)q̇ = A⊤ (q) G (q)u,

= A⊤ (q)

n−k

∑ gi ( q ) ui ,


i =1
n−k

= ∑ A ⊤ ( q ) gi ( q ) ui ,
i =1

= 0.
Example 1.2.7 (Rolling Wheel). Consider the rolling wheel example from Example 1.2.3, which has a single nonholonomic constraint:
h
i
a1 (q)⊤ q̇ = sin θ − cos θ 0 q̇ = 0,
where q = [ x, y, θ ]⊤ . The null space of a1 (q)⊤ is spanned by the vectors [cos θ, sin θ, 0]⊤
and [0, 0, 1]⊤ and therefore the kinematic model is given by:

  
cos θ 0 " #
ẋ
 u1
  
.
(1.15)
 ẏ  =  sin θ 0
u2
0
1
θ̇
In this case, the inputs u1 and u2 have an intuitive physical meaning: u1 is the
speed at which the wheel is moving, and u2 is the wheel’s angular rotation rate.

1.2.5

Dynamics Models

Kinematic models describe the geometric constraints that limit a robot’s motion—
for example, the fact that a robotic arm can only rotate about its joints. However,
kinematics alone does not explain how motion is generated or resisted. For that,
we turn to dynamics, which describe how forces and torques influence motion by
producing accelerations.
Newton’s second law of motion is the foundation of robot dynamics, relating
the net force acting on a body to its acceleration. Applied to a single point mass,
the law takes the form:
F (q, q̇) = mq̈,
(1.16)
where m is the mass of the particle, q = [ x, y, z]⊤ is its position vector, and F is
the total force acting on the particle.

---

### [PDF p.39 | Book p.37]

modeling robot dynamics

37

Example 1.2.8 (Mass-spring-damper system). A fundamental example in the study
of dynamics is the one-dimensional mass-spring-damper system. The system
consists of a mass m attached to a spring and a damper, constrained to move
along a line. The total force acting on the mass is typically composed of three
terms:
1. an external input force Fexternal ,
2. a spring force −kx that resists displacement from the equilibrium position, and
3. a damping force −c ẋ that resists velocity.
The net force on the mass is:
F = Fexternal − kx − c ẋ,
where k > 0 and c > 0 are the spring and damping coefficients, respectively,
and x is the displacement from equilibrium. Substituting this expression into
Newton’s second law yields the following second-order differential equation:
m ẍ + c ẋ + kx = Fexternal .
This equation models oscillatory motion with damping, and it arises in many
robotics applications—for example, when analyzing joint compliance, actuator
dynamics, or contact interactions.
While the mass-spring-damper system illustrates the dynamics of a single particle in one dimension, real-world robotic systems are often more complex. To
capture their behavior, we extend Newton’s second law to systems of interconnected particles, typically modeled in robotics as rigid bodies. A rigid body is an
idealized object in which the relative positions of all constituent particles remain
fixed over time, regardless of external forces. This assumption implies that the
body does not deform and allows us to reduce a complex system of interacting
particles to a simpler model governed by the motion of a finite set of parameters,
for example, position and orientation of a frame fixed to the body. As a result,
rigid body dynamics provide a powerful and tractable framework for analyzing
and simulating robotic systems10 .
The motion of a rigid body in three-dimensional space can be described in
terms of its translational and rotational dynamics. Translational dynamics govern
the motion of the body’s center of mass and are described by Newton’s second
law, as expressed in Equation (1.16), where the position variable refers specifically to the center of mass. In three-dimensional space, a rigid body has three
translational degrees of freedom, corresponding to movement along each of the
Cartesian axes. Rotational dynamics, on the other hand, describe how the body’s
orientation evolves over time. A rigid body also has three degrees of freedom
associated with its orientation in three-dimensional space, corresponding to rotation about each of its principal axes. Unlike translation, orientation cannot be
represented by a single vector, and several parameterizations are commonly used.

Interesting examples in robotics where
the rigid body assumption may not
hold include soft robots, robots with
compliant end-effectors, or robots with
lightweight flexible structures.
10

---

### [PDF p.40 | Book p.38]

38

principles of robot autonomy

Notable examples include rotation matrices, which provide a full and unambiguous representation at the cost of redundancy; Euler angles, which use a sequence
of three rotations to represent orientation, and quaternions, which offer a compact
and singularity-free alternative well-suited for numerical applications.
The rotational dynamics11 of a rigid body are governed by the time evolution
of its angular momentum. Specifically, they are described by:
M = Ḣ,

(1.17)

We refer the reader to Shuster [130] for
an in-depth treatment of rotational dynamics and attitude representations.
11

where M denotes the total external moment (or torque) acting on the body, and H
is the angular momentum, typically computed about the center of mass. This relationship is commonly referred to as Euler’s equation for rotational dynamics and
captures how applied torques influence changes in the body’s rotational motion.
An alternative to the Newton-Euler method—defined by Equations (1.16)-(1.17)—
for deriving the equations of motion for a rigid body is the Lagrange Method. This
approach is closely tied to the notion of generalized coordinates, generalized velocities, and kinematic constraints, and takes an energy-based approach. In the
Lagrange method, the dynamics of a rigid body are derived from a scalar quantity
called the Lagrangian, defined as the difference between the kinetic and potential
energies:
L(q, q̇) = T (q, q̇) − V (q),
(1.18)
where T (q, q̇) and V (q) denote the kinetic and potential energies of the system,
respectively. The evolution of the system is governed by Lagrange’s equations 12 , 13 ,
which incorporate both external influences and kinematic constraints. In the absence of constraints, the equations of motion are given by:

B. Siciliano et al. Robotics: Modelling,
Planning and Control.
Springer Publishing Company, Incorporated, 2008.
Chap. 7
12

K. M. Lynch and K. C. Park. Modern
Robotics: Mechanics, Planning, and Control. Cambridge University Press, 2017.
Chap. 8
13

d  ∂L  ∂L
−
= Qj,
dt ∂q̇ j
∂q j

j = 1, . . . , n g ,

(1.19)

where Q j ∈ R is a non-conservative generalized force associated with the generalized coordinate q j 14 , and n g corresponds to the system’s degrees of freedom.
Equations (1.19) describe how the generalized forces acting on the system relate
to its position, velocity, and acceleration, providing a systematic way to derive
the system’s dynamic model from its kinetic and potential energies.
In the presence of Pfaffian constraints15 , Lagrange’s equations take the form:
k
d  ∂L  ∂L
−
= Q j + ∑ λi aij (q),
dt ∂q̇ j
∂q j
i =1

j = 1, . . . , n g ,

ai⊤ (q)q̇ = 0,

i = 1, . . . , k,

(1.20)

where aij is the j-th component of the i-th Pfaffian constraint vector ai (q) and λi ∈
R is a Lagrange multiplier. The first n g equations describe the dynamics of the generalized coordinates under the influence of both external and constraint forces,
while the remaining k equations represent the kinematic constraints themselves.
The complete system thus comprises n g + k equations in n g + k unknowns (the
generalized coordinates and the Lagrange multipliers), and is commonly referred

Generalized forces are projections of
physical forces and torques into the
generalized coordinate space. Forces
not derived from a potential—such as
friction—are termed non-conservative.
In contrast, forces like gravity are conservative.
14

While Lagrange’s method can accommodate general constraints, we focus
here on Pfaffian constraints for simplicity.
15

---

### [PDF p.41 | Book p.39]

modeling robot dynamics

to as the standard non-holonomic form. If the system is holonomic and the generalized coordinates are chosen to be independent, the constraints are implicitly
satisfied, and Lagrange’s equations reduce to the simpler, unconstrained form
introduced in Equation (1.19).
Example 1.2.9 (Pendulum). Consider again the pendulum depicted in Figure 1.2.
To model its dynamics, we analyze how gravity drives the motion of the mass.
Specifically, we will demonstrate four distinct approaches for deriving the equations of motion—using both Cartesian and polar coordinates, and applying both
the Newton-Euler and Lagrange methods. This comparison will highlight how
the choice of generalized coordinates can influence the complexity of the derivation.
We begin by using Newton’s second law to derive the dynamics of the pendulum, focusing on the two forces acting on the mass: gravity and the force from
the rod. We assume that the rod’s force acts purely along its axis. Since the
pendulum’s length is fixed, this force must counteract the component of gravity
along the rod and generate the required centripetal acceleration. The axial force
exerted by the rod is given by:
Fr = mg cos θ +

mv2
,
L

where m is the mass of the pendulum, g is gravitational acceleration, L is the
length of the rod, and v is the speed of the mass. The gravitational force is:
Fg = mg,
acting along the negative y-direction. To compute the net force in Cartesian coordinates, we project both the rod’s force and the gravitational force onto the xand y-axes:
mv2
sin θ − mg sin θ cos θ,
L
mv2
Fy =
cos θ − mg sin2 θ.
L

Fx = −

Applying Newton’s second law as defined in Equation (1.16) yields the equations
of motion:
ẍ = −
ÿ =

v2
sin θ − g sin θ cos θ,
L

v2
cos θ − g sin2 θ.
L

To express these equations purely in terms of Cartesian coordinates, we substitute x = L sin θ and y = − L cos θ, leading to:
1
( gxy − xv2 ),
L2
1
ÿ = − 2 ( gx2 + yv2 ),
L

ẍ =

(1.21)

39

---

### [PDF p.42 | Book p.40]

40

principles of robot autonomy

with v2 = ẋ2 + ẏ2 . This method requires careful force analysis, as the kinematic
constraint (fixed-length rod) is handled implicitly through the projected components of the rod’s force.
As a second approach to deriving the equations of motion using Cartesian
coordinates, we now apply the Lagrange method, which yields a slightly simpler
formulation. We begin by defining the kinetic and potential energies:
T=

1
m( ẋ2 + ẏ2 ),
2

V = mgy,

and observe that there are no external non-conservative generalized forces16 . As
discussed in Example 1.2.2, we recall the system’s single Pfaffian constraint:
x ẋ + yẏ = 0.
Thus, using Lagrange’s equations introduced in Equation (1.20), we obtain:
m ẍ = λx,
mÿ + mg = λy,

(1.22)

x ẋ + yẏ = 0.
We can solve for the Lagrange multiplier λ by differentiating the constraint with
respect to time:
d
( x ẋ + yẏ) = ẋ2 + ẏ2 + x ẍ + yÿ = 0,
dt
and by substituting the expressions for ẍ and ÿ from the first two Lagrange’s
equations in (1.22) to obtain:
ẋ2 + ẏ2 +

1 2
1
x λ + y2 λ − gy = 0.
m
m

Solving for λ yields:

m
( gy − v2 ),
L2
where we used L2 = x2 + y2 and v2 = ẋ2 + ẏ2 . Finally, substituting the expression
for λ back into the equations of motion and simplifying, we find:
λ=

1
( gxy − xv2 ),
L2
1
ÿ = − 2 ( gx2 + yv2 ),
L

ẍ =

(1.23)

which matches the result previously obtained using Newton’s method in Equation (1.21).
After applying both the Newton-Euler and Lagrange methods in Cartesian coordinates, we now replicate the derivation in polar coordinates. To apply Euler’s
equation for rotational dynamics as given in Equation (1.17), we adopt a coordinate frame fixed at the pivot point. The gravitational force acting on the mass
generates a moment about the pivot:
M = −mgL sin θ,

Gravity is a conservative force, so no
generalized non-conservative forces appear.
16

---

### [PDF p.43 | Book p.41]

modeling robot dynamics

41

while the angular momentum of the system about the same point is:
H = mL2 θ̇,
where mL2 is the moment of inertia17 about the pivot. Substituting into Euler’s
equation yields the system dynamics:
θ̈ = −

g
sin θ,
L

(1.24)

In Euler’s equation, the moment of inertia plays a role analogous to mass in
Newton’s second law.
17

which are considerably more compact than the corresponding equations derived
in Cartesian coordinates.
The Lagrange method also becomes significantly simpler when using the polar
coordinate θ, as there is no need to handle Pfaffian constraints explicitly. In this
formulation, the kinetic and potential energies of the system are:
T=

1
mL2 θ̇ 2 ,
2

V = −mgL cos θ.

Applying Equation (1.20), and noting the absence of non-conservative generalized
forces or constraints, we obtain the following equation of motion:
θ̈ = −

g
sin θ,
L

(1.25)

which, as expected, matches the result derived using Euler’s equation in Equation (1.24).

1.3

Wheeled Robot Motion Models

Robots are developed in diverse forms, sizes, and configurations, each featuring distinct mobility solutions tailored to specific applications. Among these,
wheeled robots are particularly common because of their excellent mobility and
simple design. In this section, we demonstrate how the concepts from the preceding sections can be applied to two classic and widely used motion models for
simple wheeled robots: the unicycle model and the differential drive model.

1.3.1

Unicycle Model

The unicycle model is one of the simplest kinematic models used for modeling
robot motion. This model leverages the kinematics of the rolling wheel discussed
in Example 1.2.3, essentially assuming the robot is constrained only by a no-slip
constraint from a single wheel. Figure 1.3 illustrates a simplified diagram of the
generalized coordinates for the unicycle model.
The kinematic model is identical to the one presented in Equation (1.15), namely:
  

ẋ
cos θ 0 " #
  
 v
,
(1.26)
 ẏ  =  sin θ 0
ω
θ̇
0
1

Figure 1.3: Generalized coordinates for a unicycle.

---

### [PDF p.44 | Book p.42]

42

principles of robot autonomy

where v represents the forward speed and ω denotes the rotational rate.
While the unicycle model may be a simplified representation of the robot’s true
kinematics, it remains valuable in many contexts where detailed dynamics are
unnecessary. Its main advantage lies in its simplicity, which often enables more
computationally efficient algorithms. In practice, such lower-fidelity models are
often used in the early stages of a system’s design or decision-making process,
and are later refined or supplemented with more accurate models when higher
precision is required.

1.3.2

Differential Drive Model

The differential drive model is a variation on the unicycle model from the previous section, with two wheels fixed on a shared rear axle and a passive front wheel
that induces no additional kinematic constraints. This model uses the same generalized coordinates as the unicycle model, q = [ x, y, θ ]⊤ , but also requires the
definition of certain geometric parameters: the width of the rear axle, denoted by
L, and the radius of the wheels, denoted by r, as illustrated in Figure 1.4.
The differential drive model assumes the wheels roll without slipping, making the derivation of its kinematic constraints similar to that of a single rolling
wheel, as discussed in Example 1.2.3. The heading vector of each wheel is given
by ev = [cos θ, sin θ ]⊤ , and the lateral direction is ev,⊥ = [sin θ, − cos θ ]⊤ . Using
the lateral direction vector, we define the no-slip kinematic constraints for the
wheels as:
ṗ⊤
ṗr⊤ ev,⊥ = 0,
l ev,⊥ = 0,
where ṗl and ṗr are the velocity vectors of the left and right wheels, respectively.
Next, we express the wheel velocity vectors ṗl and ṗr as functions of the generalized coordinates and velocities by leveraging the robot’s geometry. The positions
of the left and right wheel centers, denoted as pl and pr , respectively, can be
computed from the generalized coordinates by:
#
"
#
"
x − L2 sin θ
x + L2 sin θ
pl =
, pr =
.
y + L2 cos θ
y − L2 cos θ
Taking the time derivative of these positions yields the velocity vectors:
"
#
"
#
ẋ − θ̇ L2 cos θ
ẋ + θ̇ L2 cos θ
ṗl =
, ṗr =
.
ẏ − θ̇ L2 sin θ
ẏ + θ̇ L2 sin θ
After some algebraic manipulation, we find that the no-slip kinematic constraints
for each wheel are equivalent:
⊤
ṗ⊤
l ev,⊥ = ṗr ev,⊥ = ẋ sin θ − ẏ cos θ = 0,

indicating that the no-slip constraint for both wheels is redundant, and thus the
constraint matches the single wheel constraint from Example 1.2.3. This is intuitive because the wheels are rigidly connected; hence, if one wheel cannot move

Figure 1.4: Generalized coordinates for a differential drive
robot.

---

### [PDF p.45 | Book p.43]

modeling robot dynamics

laterally, neither can the other. The kinematic model for the differential drive
model is also identical to the single wheel model in Equation (1.26), but the inputs can now be expressed in a more realistic form relative to the actual geometry
of the robot.
In particular, instead of using the forward speed v and body rotation rate ω as
inputs, as in Equation (1.26), the differential drive model uses the rotation rates of
the left and right wheels, ωl and ωr . We can derive a relationship between these
sets of inputs by considering the geometry of the robot and the no-slip wheel
assumption. First, denote the position p = [ x, y]⊤ in terms of the wheel center
positions by p = 21 ( pl + pr ), thus the velocity vector is ṗ = 12 ( ṗl + ṗr ). By the
no-slip wheel assumption, the velocity v can be expressed as v = e⊤
v ṗ, leading to:
v = e⊤
v ṗ,
1 ⊤
e ( ṗ + ṗr ),
2 v l
1
= ( v l + v r ),
2
r
= ( ω l + ωr ),
2

=

where r is the radius of the wheel and vl and vr are the speeds of the left and
right wheels, respectively. Additionally, the no-slip condition on each wheel is
⊤
given by vl = e⊤
v ṗl and vr = ev ṗr , expanded as:
L
= vl ,
2
L
ẋ cos θ + ẏ sin θ + θ̇ = vr .
2
ẋ cos θ + ẏ sin θ − θ̇

Since ẋ cos θ + ẏ sin θ = v, we simplify these expressions to:
L
θ̇ = vr − v,
2
L
θ̇ = v − vl .
2
Combining these gives:
Lθ̇ = vr − vl ,

= r ( ωr − ω l ),
establishing the relationship between the generalized velocity θ̇ and the wheel
rotational speeds.
In summary, the mapping between the inputs can be defined as:
v=

r
( ω + ωr ),
2 l

ω=

r
( ωr − ω l ).
L

which allows us to define the differential drive model:
  

r
r
" #
ẋ
2 cos θ
2 cos θ
ωr
  r

.
 ẏ  =  2 sin θ 2r sin θ 
ωl
r
r
θ̇
−
L
L

(1.27)

43

---

### [PDF p.46 | Book p.44]

44

principles of robot autonomy

Despite the slight increase in complexity over the unicycle model, this model
leverages the geometry of the robot to make the inputs more intuitive. This enhancement makes the differential drive model more suitable for certain motion
planning and control tasks, as the robot’s actuation typically originates from motors attached to the wheels’ axles.
More generally, a kinematic state-space model should be interpreted only as a
subsystem of a more comprehensive dynamical model. In particular, kinematic
models typically assume direct control over certain motion variables—such as
velocity or angular rate—without accounting for how these quantities are generated or constrained by the physical system. For more realistic modeling, it is
often necessary to extend the kinematic model to include additional integrators
in front of the control inputs.
Example 1.3.1 (Dynamic extension of the unicycle model). The unicycle model
introduced in Equation (1.26) assumes direct control over the forward velocity v
and angular velocity ω, with the state defined by the variables ( x, y, θ ). To reflect
the fact that velocity v is itself the result of integrating an acceleration input a,
the model can be extended by treating v as an additional state, yielding the augmented state ( x, y, θ, v) and input (ω, a). The dynamics become:

  
v cos θ
ẋ
 ẏ   v sin θ 

  
.
 =
 θ̇   ω 
a
v̇

(1.28)

This dynamic extension accounts for acceleration as a control input and enables
the modeling of more realistic scenarios, such as those involving actuation limits.

1.3.3

Bicycle/Simple Car Model

The bicycle model is a simplified kinematic model commonly used to approximate the motion of vehicles with two front-steered wheels and two rear-driven
wheels, such as cars or mobile robots with similar geometry. The model captures key steering dynamics while assuming no slip at the contact points of the
wheels. It is called a “bicycle” model because the two front wheels and two rear
wheels are collapsed into a single front and rear wheel aligned on a common axis,
forming a virtual two-wheeled vehicle. Compared to the unicycle and differential
drive models introduced earlier, the bicycle model enforces more realistic kinematic constraints on how the system can turn. In particular, it captures the fact
that the vehicle must steer to follow curved paths, and cannot rotate in place. As
such, it provides a better approximation for many wheeled systems while still
remaining relatively simple.
Figure 1.5 shows the simplified geometry of the bicycle model. This model
can be derived by enforcing nonholonomic constraints on the rolling direction
of each wheel and assuming ideal no-slip contact, following the discussion in

---

### [PDF p.47 | Book p.45]

modeling robot dynamics

45

previous sections. Figure 1.6 illustrates how the same kinematic model can be interpreted in the context of a four-wheeled vehicle. The key idea is that both front
wheels steer with a common angle ϕ, and the vehicle moves forward with velocity v, subject to the no-slip constraints. These assumptions lead to the following
differential equations characterizing the car model:

ẋ = v cos θ,
ẏ = v sin θ,
v
θ̇ = tan ϕ,
L

(1.29)

where ( x, y) is the position of the rear axle center, θ is the heading angle, v is
the forward speed, ϕ is the steering angle, and L is the length of the wheelbase
(the distance between the front and rear axles). Therefore, we define the state as
x = [ x, y, θ ]⊤ and the control input as u = [v, ϕ]⊤ .

1.4

Simulating Robot Dynamics

In Section 1.1, we introduced the concept of a state space model to mathematically
describe the evolution of a robot’s state over time. In Section 1.2 we demonstrated
how a robot’s kinematics and dynamics are used to derive a state space model that
represents its physical motion. In this section, we present several computational
techniques for simulating the changes in a robot’s state over time.
The state space model in Equation (1.1) is a general system of ordinary differential equations, which in most cases cannot be solved analytically. Numerical
simulation provides a practical approach to obtaining approximate solutions, allowing us to better understand a robot’s dynamics and to test and validate algorithms for robot autonomy. Typically, when we refer to simulating a system, we
mean approximately solving an initial value problem (IVP) for a system of differential equations, as defined in Equation (1.1):
ẋ = h( x(t), t),

x ( t0 ) = x0 ,

where h( x(t), t) = f ( x(t), u(t)), and the input u(t) may either be explicitly defined as a known function of time (e.g., a predefined control sequence), or computed at each time step based on the current state.
The objective of this initial value problem is to find the trajectory x(t), starting
from x(t0 ), that satisfies the differential equation18 . By the Fundamental Theorem
of Calculus19 , the solution at time t can be written as:
x ( t ) = x ( t0 ) +

Z t
t0

h( x(τ ), τ )dτ.

Figure 1.5: The bicycle model
approximates the motion of a
four-wheeled vehicle by collapsing each axle into a single wheel,
aligned with the vehicle’s centerline. The state consists of the
position, ( x, y), of the rear axle
center and the heading angle, θ.
The control inputs are the forward velocity, v, and the steering angle, ϕ.

Figure 1.6: The same bicycle
model applied to a car-like vehicle. The control and state definitions are identical to Figure 1.5,
but the visualization makes explicit the mapping between the
simplified model and a fourwheeled car.

If h is Lipschitz continuous in x (t) and
continuous in t, the trajectory x (t) exists
and is unique.
18

This expresses the inverse relationship
between differentiation and integration:
integrating the derivative ẋ = h( x(t), t)
over time recovers the original function x(t).
19

In general, evaluating this integral analytically for arbitrary functions h( x(t), t) is
intractable. Therefore, we typically resort to numerical integration methods that

---

### [PDF p.48 | Book p.46]

46

principles of robot autonomy

involve a discretization in time:
N −1 Z t k +1

x ( t ) = x ( t0 ) + ∑

k =0

tk

h( x(τ ), τ )dτ,

(1.30)

where t0 < t1 < · · · < t N = t define a time grid, and each interval has
width ∆tk = tk+1 − tk . This decomposition breaks the continuous integration
problem into a sum of smaller integrals over short intervals. Within each interval [tk , tk+1 ], we can then approximate the integral using various numerical
quadrature rules—such as the Euler method, the Midpoint method, or higherorder Runge-Kutta schemes—which trade off computational cost and accuracy.
In this section, we provide a concise introduction to some of the most widely
used methods.
Example 1.4.1 (Simple IVP). To illustrate the different numerical integration methods, we will consider the initial value problem defined below and presented in
Algorithm 1 as an example:
ẋ (t) = x (t) sin2 (t),

x (0) = 1.

Our goal is to approximate the trajectory x (t) over the interval [0, 10] using various integration methods.
Concretely, we will explore different techniques to approximate the following
analytical solution:


t − t0 − sin(t − t0 ) cos(t + t0 )
x (t) = x0 exp
,
2
which, for our specific initial conditions x0 = 1 and t0 = 0, simplifies to:


t − sin(t) cos(t)
x (t) = exp
.
2

1.4.1

Euler Method

One of the simplest techniques for approximating the integral within each time
interval of the discretized problem, as shown in Equation 1.30, is the Euler
method20 . This method approximates the integral over a short interval [tk , tk+1 ]
by evaluating the integrand at the beginning of the interval.
Given that the trajectory x(t) satisfies:
x ( t k +1 ) = x ( t k ) +

Z t
tk

k +1

h( x(τ ), τ )dτ,

the Euler method approximates this integral by assuming h( x(τ ), τ ) is constant
within the interval, yielding:
x(tk+1 ) ≈ x(tk ) + ∆t · h( x(tk ), tk ),
where ∆t = tk+1 − tk is the time step.

Named after the Swiss mathematician
Leonhard Euler and often referred to as
the forward Euler method.
20

---

### [PDF p.49 | Book p.47]

modeling robot dynamics

Simple IVP (Running Example)
import numpy as np
# Define the derivative function h(x, t)
def h(x, t):
return x * np.sin(t) ** 2
# Define initial conditions and final time
x0 = 1.0 # Initial state x(t0)
t0 = 0.0 # Initial time t0
tf = 10.0 # Final time tf
|$\Delta$|t = 0.5 # Discretization step
t = np.arange(t0, tf + |$\Delta$|t, |$\Delta$|t) # Array of timestamps
# Compute analytical solution
x_true = x0*np.exp(((t-t0) - np.sin(t-t0)*np.cos(t+t0))/2)
def integrate(h, x0, t, method):
x = np.zeros((t.size, x0.size))
x[0] = x0
for i in range(t.size - 1):
|$\Delta$|t = t[i + 1] - t[i]
x[i + 1] = method(h, x[i], t[i], |$\Delta$|t)
return x
def method(h, x, t, |$\Delta$|t):
# Implement here numerical integration method
# Test a specific numerical method
x_method = integrate(h, x0, t, method)

Algorithm 1: Definition of an illustrative initial value problem. The code for this
example is available in the repository github.com/StanfordASL/pora-exercises
in the notebook ch01/simulation.ipynb. In the following sections, we will
explore different numerical integration methods and implement them in a custom
method function.
This approximation corresponds to a first-order Taylor series expansion:
x(t + ∆t) ≈ x(t) + ∆t ẋ(t),

= x(t) + ∆t · h( x(t), t),
which treats the rate of change ẋ(t) as constant across the interval.

(1.31)

47

---

### [PDF p.50 | Book p.48]

48

principles of robot autonomy

Alternatively, the Euler method can be interpreted as a finite difference approximation of the time derivative:
x(t + ∆t) − x(t)
.
∆t
While computationally inexpensive, the Euler method has limited accuracy due
to its reliance on information from the beginning of each interval. The local
truncation error21 is of order O(∆t2 ), and errors can accumulate significantly
over long trajectories unless small time steps are used.
As a concrete illustration, consider the running example introduced in Example 1.4.1. A simple implementation of Euler’s method is presented in Algorithm 2.
ẋ(t) ≈

Euler Method
def euler(h, x, t, |$\Delta$|t):
return x + |$\Delta$|t * h(x, t)
x_euler = integrate(h, x0, t, euler)

Algorithm 2: Python implementation of Euler’s method.

1.4.2

Midpoint Method

The Midpoint method is a refinement of the Euler method that improves accuracy
by evaluating the derivative at the midpoint of the time interval, rather than at
its beginning. Recall that Euler’s method approximates the next state using the
derivative ẋ evaluated at time t:
x(t + ∆t) ≈ x(t) + ∆t · h( x(t), t).
In contrast, the Midpoint method approximates the integral by using the value of
the derivative at t + ∆t
2 :
 


∆t
∆t
x(t + ∆t) ≈ x(t) + ∆t · h x t +
,t+
.
(1.32)
2
2
While this yields a more accurate estimate, it is not yet explicit, since the value
x(t + ∆t
2 ) is not known in advance.
To resolve this, we approximate the midpoint using a single Euler step of size
∆t
:
2


∆t
∆t
≈ x(t) +
· h ( x ( t ), t ).
(1.33)
x t+
2
2
Substituting this estimate into Equation (1.32), we arrive at the explicit form of
the Midpoint method:


∆t
∆t
x(t + ∆t) ≈ x(t) + ∆t · h x(t) +
· h ( x ( t ), t ), t +
.
2
2

That is, the error introduced in a single
time step.
21

---

### [PDF p.51 | Book p.49]

modeling robot dynamics

The Midpoint method improves the local truncation error with respect to the
Euler method from O(∆t2 ) to O(∆t3 ), providing significantly better accuracy for
small step sizes. The improvement comes at the cost of computing the derivative
twice per step—once at the start of the interval and once at its midpoint.
As an illustration, a simple implementation for the running example introduced in Example 1.4.1 is presented in Algorithm 3.
Midpoint Method
def midpoint(h, x, t, |$\Delta$|t):
t_mid = t + |$\Delta$|t / 2
x_mid = x + (|$\Delta$|t / 2) * h(x, t)
return x + |$\Delta$|t * h(x_mid, t_mid)
x_midpoint = integrate(h, x0, t, midpoint)

Algorithm 3: Python implementation of the Midpoint method.

1.4.3

Runge-Kutta-4 Method

Both the Euler and Midpoint methods approximate the change in x over a time
step interval by evaluating the derivative ẋ at one or two specific points within
the interval. The Runge-Kutta family of methods generalizes this idea by using
multiple evaluations of the derivative to achieve higher accuracy. One of the
most widely used methods in this family is the fourth-order Runge-Kutta method22 ,
which computes four derivative estimates over the interval [t, t + ∆t]:
x(t + ∆t) ≈ x(t) +

∆t
(k + 2k2 + 2k3 + k4 ),
6 1

where:
k 1 = h ( x ( t ), t ),
∆t
∆t
k1 , t +
),
2
2
∆t
∆t
k3 = h( x(t) +
k2 , t +
),
2
2
k4 = h( x(t) + ∆tk3 , t + ∆t).

k2 = h( x(t) +

RK4 improves the local truncation error to O(∆t5 ), offering significantly better
accuracy than the Euler or Midpoint methods. This comes at the cost of evaluating h( x, t) four times per step, but the method remains computationally efficient
and stable for many practical applications.
Using the running example from Example 1.4.1, an implementation of RK4 is
shown in Algorithm 4.

22

Often abbreviated as RK4.

49

---

### [PDF p.52 | Book p.50]

50

principles of robot autonomy

RK4 Method
def rk4(h, x, t, |$\Delta$|t):
k1 = h(x, t)
k2 = h(x + (|$\Delta$|t / 2) * k1, t + |$\Delta$|t / 2)
k3 = h(x + (|$\Delta$|t / 2) * k2, t + |$\Delta$|t / 2)
k4 = h(x + |$\Delta$|t * k3, t + |$\Delta$|t)
return x + (|$\Delta$|t / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
x_rk4 = integrate(h, x0, t, rk4)

Algorithm 4: Python implementation of the RK4 method.

Analytical Solution
RK4 Method
Midpoint Method
Euler Method

x t

()

100
50
0

0

2

4

6

8

10

Figure 1.7: Visual comparison
of various numerical integration
methods and their approximations compared to the analytical solution for the initial value
problem introduced in Example 1.4.1, with ∆t = 0.5.

t

To compare the performance of these methods, we can visualize their outputs
against the analytical solution:
It is important to highlight that advanced simulation techniques extend far
beyond these numerical integration methods, allowing for the high-fidelity simulation of robotic systems, including visualization in pixel space. These techniques
can incorporate detailed physical modeling, sensor data fusion, and learningbased approaches to create realistic and accurate simulations23 . As we will discuss in later chapters on perception, these advancements are crucial for tasks such
as robot training, planning under uncertainty, and evaluating the autonomy stack
in novel and previously unseen scenarios.

1.5

Summary

In this chapter, we introduced the fundamental principles underlying the modeling and simulation of robotic systems. We began by introducing state space
models, which provide a mathematical framework to describe the evolution of a
robot’s state over time. Next, we discussed a robot’s kinematics and dynamics,
which characterize its motion and the constraints acting on it. This included a
discussion of generalized coordinates and kinematic constraints—both holonomic

One notable example is the use of
Neural Radiance Fields (NeRFs) for generating photorealistic scenes.
23

---

### [PDF p.53 | Book p.51]

modeling robot dynamics

51

and nonholonomic—along with the formulation of kinematic models using Pfaffian constraints. Throughout this chapter, we examined practical examples such
as the rolling wheel, the pendulum, and wheeled robots like the unicycle and differential drive models. Finally, we introduced numerical integration techniques
for simulating robot dynamics over time. We presented the Euler, Midpoint, and
Runge-Kutta methods, highlighting their trade-offs and applications through concrete code examples.
To learn more. For readers interested in a deeper and more rigorous treatment
of the concepts presented in this chapter, Siciliano and Khatib [131] and Siciliano et al. [134] offer comprehensive and widely adopted references. These texts
cover the mathematical foundations of robot kinematics, dynamics, and control
in greater depth, and provide additional examples, derivations, and exercises that
complement and extend the material introduced here.

1.6

Exercises

The starter code for the exercises provided below is available online through
GitHub. To get started, download the code by running in a terminal window:
git clone https://github.com/StanfordASL/pora-exercises.git

We denote Problems requiring hand-written solutions and coding in Python
with and , respectively.

Problem 1: Numerical Integration Methods
In Example 1.4.1 we introduced a simple IVP and in Section 1.4.3 we showed the
differences between the Euler, midpoint, and fourth-order Runge-Kutta methods
for solving it. In this exercise we will explore the use of a more advanced numerical integration scheme provided by the SciPy Python library called odeint. Open
the notebook ch01/exercises/simulation.ipynb and practice by implementing
the dynamics models for a damped pendulum and a bicycle, and then simulating
them using odeint.

Problem 2: Nonholonomic Wheeled Robot Dynamics
The goal of this exercise is to familiarize yourself with some Python fundamentals
that will be used throughout the book, such as NumPy and inheritance, as well
as techniques for controlling nonholonomic wheeled robots.
Consider a simple robot with two wheels whose state is defined by the position
of the center of the axle and the heading angle, shown in Figure 1.8. This robot’s
motion can be described by the simplest nonholonomic wheeled robot model, the
unicycle model.

Figure 1.8: Generalized coordinates for a robot with unicycle
kinematics.

---

### [PDF p.54 | Book p.52]

52

principles of robot autonomy

The kinematic model we will use reflects the rolling without side-slip constraint,
and is given below in Equation (1.34).
ẋ (t) = v(t) cos(θ (t)),
ẏ(t) = v(t) sin(θ (t)),

(1.34)

θ̇ (t) = ω (t).
In this model, the robot state is x = [ x, y, θ ]⊤ , where [ x, y]⊤ is the Cartesian
location of the robot center and θ is its heading with respect to the x-axis. The
robot control inputs are u = [v, ω ]⊤ , where v is the velocity along the main axis
of the robot and ω is the angular velocity, subject to the control constraints:

|v(t)| ≤ 0.75 m/s,

and

|ω (t)| ≤ 1.0 rad/s.

In this problem, we will demonstrate the use of class inheritance in Python
classes and the use of NumPy for vectorized operations. The notebook associated
with this problem is ch01/exercises/nonholonomic_wheeled_robot_dynamics.i
pynb.
We will be using a Dynamics base class for two different dynamics models: the
wheeled robot dynamics model in this exercise and a double integrator model in
the next exercise. The base class contains two unimplemented functions: step
and rollout. The step function will propagate the dynamics a single time step
with disturbances, and the rollout function will apply the step function multiple
times to retrieve a trajectory of states over multiple time steps. Because the feedforward dynamics are subject to disturbances, the same control sequence will
result in different trajectories. We will observe this by executing multiple rollouts
of the dynamics using the same control sequence from the same initial state.
In the ch01/exercises/nonholonomic_wheeled_robot_dynamics.ipynb notebook, complete the RobotDynamics class. Implement the function step using
discrete-time Euler integration with the kinematic equations described in Equation (1.34). Then in the same class, implement the function rollout with two
for-loops, calling the step function. Run the cells that rollout the robot’s dynamics and plot the control and state trajectories (this code has been written for
you).

Problem 3: Double Integrator Dynamics
In this exercise, we consider the double integrator dynamics model:
ẋ (t) = v x (t),
ẏ(t) = vy (t),
v̇ x (t) = a x (t),

(1.35)

v̇y (t) = ay (t).
In this model, the robot state is x = [ x, y, v x , vy ]⊤ and the robot control inputs
are u = [ a x , ay ]⊤ .

---

### [PDF p.55 | Book p.53]

modeling robot dynamics

Notice that in the previous problem, we used a for-loop to rollout several
trajectories of the robot’s dynamics. In this problem, we will use the same base
dynamics class for a DoubleIntegratorDynamics class, and use batching to reduce
the number of for-loops needed to perform multiple rollouts. The notebook for
this problem is ch01/exercises/double_integrator_dynamics.ipynb.
i. To reduce the number of for-loops needed to perform multiple rollouts, we
will batch the dynamics equations applied in the function step. Implement
the function step in the DoubleIntegratorDynamics class.
ii. Fill in the code in function rollout in the DoubleIntegratorDynamics class
using the step function you just wrote. Note that you should only need one
for-loop!

53

---

### [PDF p.56 | Book p.54]

54

principles of robot autonomy

References
[88]

T. Lozano Perez. “Spatial planning: a configuration space approach”. In:
Autonomous Robot Vehicles. 1990.

[90]

K. M. Lynch and K. C. Park. Modern Robotics: Mechanics, Planning, and
Control. Cambridge University Press, 2017. Chap. 8.

[130]

M. D. Shuster. “Survey of attitude representations”. In: Journal of the Astronautical Sciences 41.4 (1993), pp. 439–517.

[131]

B. Siciliano and O. Khatib. Springer Handbook of Robotics. Springer-Verlag,
2007.

[132]

B. Siciliano et al. Robotics: Modelling, Planning and Control. Springer Publishing Company, Incorporated, 2008. Chap. 2.

[133]

B. Siciliano et al. Robotics: Modelling, Planning and Control. Springer Publishing Company, Incorporated, 2008. Chap. 7.

[134]

B. Siciliano et al. Robotics: Modelling, Planning and Control. Springer Publishing Company, Incorporated, 2008.
