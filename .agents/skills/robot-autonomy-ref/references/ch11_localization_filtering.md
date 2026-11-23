# Ch 11: Introduction to Localization and Filtering

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Part III: Localization & Mapping
- **Trang sách:** 281–298 | **Trang PDF:** 283–300
- **Độ ưu tiên cho dự án:** `CỐT LÕI`
- **Tóm tắt:** Xác suất nền tảng, mô hình Markov và bộ lọc Bayes tổng quát cho định vị robot.

---

### [PDF p.283 | Book p.281]

11
Introduction to Localization and Filtering
We have already discussed the robot motion planning problem and surveyed
common algorithms for it, ranging from optimal control to sampling-based methods. All of these approaches implicitly assume access to the robot’s current state,
for example for initializing trajectory optimization methods or for closing the
loop in feedback control. In practice, however, this state cannot be read directly;
it must be estimated from noisy, partial sensor data.
Robot perception, as introduced in previous chapters, tackles the challenge of
extracting semantic and geometric information from raw sensor streams. These
methods are indispensable for local, instantaneous awareness. For instance, detecting nearby obstacles with a laser scanner or identifying objects in view with
a camera. Yet this information is inherently local and relative to the robot’s current position. It suffices for collision avoidance, but not for the global reasoning
required by full planning and control schemes.
This gap is addressed by robot localization and mapping, one of the core components of the “think” stage in the classical “see-think-act” cycle. The goal of robot
localization and mapping is to synthesize local sensor data into a coherent global
estimate of the robot’s state and map the surrounding environment. In this chapter, we focus on localization, which is the ability to infer the robot’s current state
with respect to a global frame or map 1 . For instance, before a robot can navigate
to a target room on the floor plan shown in Chapter 11, it must first establish
where in the building it is located.

S. Thrun, W. Burgard, and D. Fox.
Probabilistic Robotics. MIT Press, 2005,
R. Siegwart, I. R. Nourbakhsh, and D.
Scaramuzza. Introduction to Autonomous
Mobile Robots. MIT Press, 2011
1

Figure 11.1: Localization is crucial for autonomy: to move
from A to B, the robot must
know which room it occupies,
and that the only path to B
runs through the hallway. Inferring such global information
from local range measurements
requires specialized algorithms.

---

### [PDF p.284 | Book p.282]

282

principles of robot autonomy

A central challenge in localization is uncertainty. Sensor data is noisy, incomplete, and sometimes ambiguous. To handle this, localization is cast in a probabilistic framework: instead of maintaining a single guess of the robot’s state, we
maintain a belief distribution over possible states. This representation allows us to
extract both point estimates and measures of uncertainty. Uncertainty quantification is vital for downstream tasks. For example, a planner may avoid high-risk
trajectories under localization uncertainty, or even select actions that deliberately
reduce uncertainty through information gathering.
The rest of this chapter is organized as follows. In Section 11.1, we review key
concepts in probability theory, including random variables, probability distributions, conditional probabilities, and Bayes’ rule. In Section 11.2, we introduce
Markov models as a probabilistic representation of robot motion and sensing.
Finally, in Section 11.3, we derive the Bayes filter, a recursive algorithm for maintaining and updating a belief distribution as controls are applied and new measurements arrive.

11.1

Preliminary Concepts in Probability

Tools from probability theory provide us with a way to systematically reason
about uncertainty in robotics. Specifically, these tools provide the language to
model noisy sensor measurements, uncertain robot states, and stochastic environments. In this section, we review several key building blocks that form the
foundation for probabilistic filtering algorithms such as the Bayes filter, namely
random variables, probability distributions, conditional probabilities, and Bayes’
rule.

11.1.1

Random Variables

We can model uncertain quantities in robotics, such as sensor measurements,
robot states, or environmental properties, as random variables. Depending on the
domain of possible values, random variables are classified as discrete or continuous.
Definition 11.1.1 (Discrete random variable). A discrete random variable X takes
values from a countable set. The probability that X takes on a specific value x is
denoted by p( X = x ), or more compactly p( x ). The function p( x ) is called the
probability mass function (PMF), and it must satisfy:

∑ p(x) = 1,
x

where the sum is over all possible values of X.
Definition 11.1.2 (Continuous random variable). A continuous random variable X
takes values in an uncountable set, typically a subset of Rn . Its distribution is
characterized by a probability density function (PDF) p( x ), which satisfies:
Z ∞
−∞

p( x ) dx = 1.

---

### [PDF p.285 | Book p.283]

introduction to localization and filtering

283

Unlike the discrete case, the probability that a continuous random variable takes
on any exact value is zero:
P( X = x ) = 0.
Intuitively, this is because a single point has zero width and probability mass only
accumulates over intervals. Consequently, probabilities are defined over regions
rather than individual values. For example, the probability that X lies in the
interval [ a, b] is:
P( a ≤ X ≤ b) =

Z b
a

p( x ) dx.

Example 11.1.1 (Discrete vs. continuous random variables). A coin flip is a discrete random variable, X ∈ {heads, tails}, with a probability mass function:
p(heads) = 12 ,

p(tails) = 12 .

In robotics, we typically model the robot’s pose as a continuous random variable.
For example, a planar robot pose x ∈ SE(2)2 can take infinitely many values
because both its position and orientation vary continuously.
Probability distributions. The probability mass function for discrete random variables and probability density function for continuous random variables are often
collectively referred to as probability distributions. There are many ways to parameterize a probability distribution. For discrete variables, the distribution can be
specified explicitly by assigning a probability to each possible value. For continuous variables, the distribution is often described by a parametric function defined
by a small number of parameters. Choosing an appropriate representation is important in robotics, since it determines both how uncertainty is modeled and how
efficiently algorithms can reason about it.

11.1.2

Joint Distributions, Independence, and Conditioning

Many robotics problems involve more than one uncertain quantity at a time.
For example, a robot might simultaneously reason about its pose, the position
of an obstacle, and a sensor reading. In such cases, it is useful to describe the
probabilities of multiple random variables together using a joint distribution.
Definition 11.1.3 (Joint distribution). The joint distribution of two random variables X and Y specifies the probability that both take on specific values simultaneously. It is denoted by p( X = x, Y = y), or more compactly p( x, y).
Independence. Random variables can be related to each other in important ways.
For example, the random variables X = “today is cloudy” and Y = “today it is
raining” are correlated: if there are no clouds, it is unlikely to rain. In contrast,
two random variables are probabilistically independent if the value of one does not
provide any information about the other.

SE(2) is the special Euclidean group
in two dimensions. It represents planar rigid-body transformations and consists of a position ( x, y) and an orientation θ.
For robots operating in
three-dimensional space, the pose lies in
SE(3), which represents 3D position and
orientation.
2

---

### [PDF p.286 | Book p.284]

284

principles of robot autonomy

Definition 11.1.4 (Probabilistic independence). Two random variables X and Y
are probabilistically independent if and only if:
p( x, y) = p( x ) p(y).

(11.1)

Example 11.1.2 (Independent sensor measurements). Suppose a robot uses a
proximity sensor and a temperature sensor, modeled by random variables X
and Y. Let X ∈ {close, medium, far} and Y ∈ {low, med, high}, with p( X =
close) = 1/3 and p(Y = med) = 1/5. If the two sensors are independent, the
joint probability of observing “close” and “med” is:
1
p( X = close, Y = med) = 13 · 15 = 15
.

Conditional probability. Another key concept is the probability of one random
variable given that another has already been observed.
Definition 11.1.5 (Conditional probability). The conditional probability of a random
variable X taking value x, given that Y took value y, is:
p( x | y) :=

p( x, y)
.
p(y)

(11.2)

Conditional probabilities allow us to update beliefs when new information
becomes available. If X and Y are independent, then p( x | y) = p( x ), meaning
that knowing Y provides no additional information about X.
Example 11.1.3 (Sensor conditional probabilities). Building on Example 11.1.2,
consider an obstacle detection variable Z ∈ {detected, not detected}. Assume
that the detection probability depends on the proximity sensor value:
p( Z = detected | X = close) = 56 ,
p( Z = detected | X = medium) = 13 ,
p( Z = detected | X = far) = 15 .
If p( X = close) = 13 , then the probability that the robot both detects an obstacle
and registers “close” is:
p( Z = detected, X = close) = p( Z = detected | X = close) p( X = close)
5
= 18
.

Conditional independence. Finally, independence can also hold given the outcome
of another variable. This concept is known as conditional independence and plays a
central role in probabilistic modeling.
Definition 11.1.6 (Conditional independence). Two random variables X and Y
are said to be conditionally independent given a third variable Z if:
p( x, y | z) = p( x | z) p(y | z),

(11.3)

---

### [PDF p.287 | Book p.285]

introduction to localization and filtering

for all values of x, y, and z. Equivalently:
p( x | y, z) = p( x | z).

(11.4)

We denote conditional independence as:
X ⊥ Y | Z.
Intuitively, conditional independence means that once the value of Z is known,
learning the value of Y provides no additional information about X. However,
if Z is not known, the variables X and Y may still appear correlated. In other
words, the variable Z explains the dependence between X and Y.
Example 11.1.4 (Conditional independence in robotics). A mobile robot equipped
with two wheel encoders produces measurements of traveled distance: one from
the left wheel (X) and one from the right wheel (Y). At first glance, these two measurements may seem correlated, since the robot’s motion affects both. However,
if we condition on the underlying hidden variable Z = “true distance traveled,”
the two encoder readings are independent:
p( x, y | z) = p( x | z) p(y | z).
That is, once the actual distance traveled is known, the left and right encoder
readings do not provide additional information about each other. This is a typical
use of conditional independence in probabilistic sensor models.

11.1.3

Law of Total Probability

The law of total probability links marginal, joint, and conditional probabilities. It
provides a systematic way to compute the probability of one random variable by
accounting for all possible outcomes of another.
Definition 11.1.7 (Law of total probability). For discrete random variables X and
Y:
p( x ) = ∑ p( x, y) = ∑ p( x | y) p(y).
y

y

For continuous random variables:
p( x ) =

Z

p( x, y) dy =

Z

p( x | y) p(y) dy.

Intuitively, the law of total probability states that to find the probability of X
taking value x, we can sum (or integrate) over all possible values of Y, weighting
the conditional probability of X given each value of Y by the probability of that
value of Y itself. This process is known as marginalization, and p( x ) is called the
marginal probability of X.
Example 11.1.5 (Robot localization via marginalization). Suppose a robot’s position X depends on which hallway Y it is currently in. We can compute the

285

---

### [PDF p.288 | Book p.286]

286

principles of robot autonomy

probability of being at a particular location x by considering every possible hallway y:
p ( x ) = ∑ p ( x | y ) p ( y ).
y

In practice, this means we marginalize over the possible hallways, combining
both the likelihood of being in each hallway and the probability of observing x
given that hallway.

11.1.4

Bayes’ Rule

The joint probability, p( x, y), between two random variables, X and Y, is related
to the conditional probabilities, p( x | y) and p(y | x ), from the definition of a conditional probability in Equation (11.2). Since we can express the joint probability
using either conditional probability, we have:
p( x, y) = p( x | y) p(y) = p(y | x ) p( x ).
This relationship is commonly referred to as Bayes’ rule3 .

Sometimes also referred to as Bayes’ theorem.
3

Definition 11.1.8 (Bayes’ rule). For discrete random variables, X and Y, Bayes’
rule states that:
p(y | x ) p( x )
.
(11.5)
p( x | y) =
p(y)
Bayes’ rule is useful because it provides a relationship between the “inverse”
conditional probabilities, p( x | y) and p(y | x ). This is particularly important for
probabilistic inference problems where we need to infer the value of one random
variable from another. For example, suppose we have a good initial guess of the
probability distribution4 , p( x ), for a random variable, X. Given new information
about the outcome of a second random variable, Y, that is related to X, we can
use Bayes’ rule to update our belief about the probability distribution of X by
computing p( x | y)5 . Bayes’ rule also extends to cases with additional random
variables. For example, with three random variables, X, Y, and Z, Bayes’ rule is:
p( x | y, z) =

p(y | x, z) p( x | z)
.
p(y | z)

Example 11.1.6 (Bayes’ rule). Consider a scenario where a robot is trying to figure
out if it is in room A or room B inside of a building. The robot has an initial guess
that the probability it is in room A is p( A) = 34 , and the robot has a camera that
can be used to improve the estimate. Suppose that a single image, I, is captured
and the features extracted from the image are compared to the known room
features which gives the conditional probabilities:
p( I | A) =

3
,
4

p( I | B) =

1
.
2

We can use Bayes’ rule to compute the posterior probability:
p( A | I ) =

p( I | A) p( A)
,
p( I )

When we have an estimate of the probability distribution p( x ) before any new
information is used to update it, we will
refer to it as the prior probability.
4

This new distribution, which we obtained by updating the prior distribution p( x ) with the new information
about Y, is commonly referred to as the
posterior probability.
5

---

### [PDF p.289 | Book p.287]

introduction to localization and filtering

287

where we use the law of total probability to compute:
p( I ) = p( I, A) + p( I, B) = p( I | A) p( A) + p( I | B) p( B),
and using p( B) = 1 − p( A).

11.1.5

Expectation, Variance, and Covariance

Probability distributions describe uncertainty in full detail by assigning probabilities to every possible outcome of a random variable. In practice, however, we
often summarize a distribution using more compact statistics. Some of the most
common statistics used to summarize a distribution include the expected value,
variance, and covariance.
Expectation. The expectation of a random variable is a measure of the central
tendency of its distribution.
Definition 11.1.9 (Expectation). The expectation6 of a random variable X is denoted by E [ X ]. For discrete random variables:
E [ X ] = ∑ x p ( x ),
x

where the sum is over all outcomes of X. For continuous random variables:
E [X] =

Z

x p( x ) dx.

The expected value can be interpreted as the average outcome obtained if the
random variable were sampled repeatedly an infinite number of times.
The expectation has several useful properties. One particularly important
property is linearity, which states that the expectation of a linear transformation
of a random variable is equal to the linear transformation of the expectation of
the random variable. Formally, for any random variable X and constants a, b ∈ R,
we have:
E [ aX + b] = aE [ X ] + b.
This property holds regardless of the distribution of X.
For vector-valued random variables X = [ X1 , . . . , Xn ]⊤ , the expectation is defined component-wise:


E [ X1 ]
 . 

E [X ] = 
 ..  .
E [ Xn ]
Variance. While the expected value describes the center of a distribution, it does
not capture how uncertain the variable is. This uncertainty is measured by the
variance.
Definition 11.1.10 (Variance). The variance of a random variable X is defined as:
h
i
Var( X ) = E ( X − E [ X ])2 .

Also referred to as the mean or the first
moment of a distribution.
6

---

### [PDF p.290 | Book p.288]

288

principles of robot autonomy

The variance measures the average squared deviation of the variable from its
mean. A large variance indicates that the variable can take values far from the
mean, while a small variance indicates that the variable is tightly concentrated
around the mean. The square root of the variance is called the standard deviation,
often denoted by σ.
Covariance. When dealing with multiple random variables, it is often important
to understand how their uncertainties are related. This relationship is captured
by the covariance.
Definition 11.1.11 (Covariance). The covariance between two random variables X
and Y is denoted cov( X, Y ) and defined as:
h
i
cov( X, Y ) = E ( X − E [ X ])(Y − E [Y ])⊤
h
i
= E XY ⊤ − E [ X ] E [Y ]⊤ .
Intuitively, the covariance describes how two random variables vary together.
If the covariance is positive, the variables tend to increase or decrease together.
If it is negative, one variable tends to increase when the other decreases. If the
covariance is zero, the variables are uncorrelated.
Example 11.1.7 (Robot motion uncertainty). Suppose X represents the forward
displacement of a robot and Y represents its lateral displacement during a single motion step. If wheel slip increases as the robot moves farther forward, then
larger values of X tend to be associated with larger sideways deviations, producing a positive covariance between X and Y.
Conversely, if the robot’s mechanical design or control system tends to stabilize
lateral motion during forward travel, the covariance between X and Y may be
negative. If forward and lateral displacements arise from unrelated sources, the
covariance will be close to zero.

11.2

Markov Models

In Chapter 1, we modeled robot motion using kinematics and dynamics, obtaining a set of first-order differential equations (see Equation (1.1)) that deterministically describe how the state x evolves in time given the current state and control
input u. In this section, we generalize this view to a probabilistic setting by introducing Markov models, which describe how the state evolves under uncertainty.
Markov models are fundamental to robotics, appearing in localization, mapping,
planning, and decision-making under uncertainty problems.
State, controls, and measurements. As in Chapter 1, the state x ∈ Rn collects all
variables relevant to the task at hand. In motion planning and control, this typically includes the robot’s physical state (pose, velocity, etc.), while in localization

---

### [PDF p.291 | Book p.289]

introduction to localization and filtering

or higher-level planning it may also include environment variables such as landmark positions or object features. We work in discrete time, writing xt for the
state at time t. We also use the shorthand xt1 :tn := xt1 , xt2 , . . . , xtn for sequences of
states, with analogous notation for control inputs ut1 :tn and measurements zt1 :tn .7
Unlike deterministic dynamics, Markov models specify probability distributions over possible states and observations. In full generality, the state evolution
is modeled as:
p( xt | x0:t−1 , z1:t−1 , u1:t ),
(11.6)
which captures the distribution of the current state xt conditioned on the entire
history of past states, controls, and measurements. Following the convention
used throughout this chapter, the robot first executes the control ut , then receives
the measurement zt based on the resulting state xt . The corresponding probabilistic measurement model is:
p(zt | x0:t , z1:t−1 , u1:t ).

(11.7)

The Markov property. In many applications, we define the state xt to be complete,
meaning it contains all the information necessary to predict future states. Formally, this assumption implies that past states and measurements provide no
additional predictive power beyond xt−1 and ut . This is known as the Markov
property, under which the models simplify to:
p ( x t | x t −1 , u t ),

(11.8)

p ( z t | x t ),

(11.9)

for the state transition, and:
for the measurement model.
Markov models in robotics. A Markov model thus consists of a state transition distribution (11.8) and a measurement distribution (11.9). Intuitively, the transition
model captures process uncertainty (e.g., wheel slip when applying a control),
while the measurement model captures sensor noise (e.g., rangefinder variability). Together, these components form the foundation of probabilistic state estimation (Section 11.2).
The probabilistic model described above belongs to a broader family of models
that assume the system state evolves according to the Markov property. Several
closely related formulations exist, depending on whether control inputs and observability are considered.
In robotics, the state of the system is typically not directly observable. Instead,
sensors provide indirect and noisy measurements that depend on the underlying
state. Models with this structure are often referred to as partially observable Markov
models.
If control inputs are not present, the model reduces to a hidden Markov model
(HMM). In this case, the state evolves according to a Markov process, and observations provide partial information about that state. The term “hidden” reflects

289

Measurements can come from any of
the sensors introduced earlier, such as
cameras, lidar, or inertial units.
7

---

### [PDF p.292 | Book p.290]

290

principles of robot autonomy

x t −1

u t −1

Figure 11.2: Graphical representation of a Markov model. At
each time step, the control ut influences the new state xt , and
the resulting state generates a
measurement zt .

u t +1

ut

z t −1

x t +1

xt

zt

z t +1

the fact that the true state xt cannot be observed directly and must instead be
inferred from the sequence of measurements.

11.3

Bayes Filter

Robot localization is a classic instance of a filtering problem8 where our goal is
to compute a probability distribution over the current state xt given the history
of control inputs u1:t , and measurements z1:t . One of the canonical approaches to
this filtering problem is known as the Bayes filter or recursive Bayesian estimation.
The Bayes filter leverages a Markov model to recursively update a belief distribution, which is a probability distribution over xt . Mathematically, we denote the
belief distribution as bel( xt ) and define it as:
bel( xt ) := p( xt | z1:t , u1:t ).

Localization is one instance of the more
general filtering problem referred to as
state estimation.
8

(11.10)

In other words, the belief bel( xt ) is a posterior probability distribution over the
state conditioned on the available history information. We also define a distribution called the prediction distribution as:
bel( xt ) := p( xt | z1:t−1 , u1:t ),

(11.11)

which does not include the most recent measurement zt . We call the process of
using the new measurement zt to compute the belief bel( xt ) from the predicted
belief bel( xt ) a correction or measurement update. The Bayes filter consists of a prediction step for computing bel( xt ) from the prior belief followed by a correction
step for computing bel( xt ) given the new measurement zt .

11.3.1

Algorithm

The recursive structure of the Bayes filter is summarized in Algorithm 11.1. At
each time step, the filter maintains a belief distribution belief bel( xt ) over the
system state. The inputs to the filter are the previous belief9 , the current control
input ut , and the latest sensor measurement zt .
The algorithm proceeds in two stages. First, a prediction step computes the
distribution bel( xt ) over possible states after applying the control input. This

In practice, we initialize the prior distribution bel( x0 ) using either a best guess
of the initial state or a uniform distribution when no prior information is available.
9

---

### [PDF p.293 | Book p.291]

introduction to localization and filtering

291

step propagates uncertainty forward using the state transition model from Equation (11.8). Second, a correction step incorporates the new measurement using the
measurement model from Equation (11.9), adjusting the predicted belief to better
match the observed data.
Intuitively, the prediction step estimates where the robot might be after executing the control, while the correction step refines this estimate using information
from the sensors.
Algorithm 11.1: Bayes Filter
Data: bel( xt−1 ), ut , zt
Result: bel( xt )
foreach xt do
// Prediction (motion update)

bel( xt ) =

R

p( xt | xt−1 , ut ) bel( xt−1 ) dxt−1

// Correction (measurement update)

bel( xt ) = η p(zt | xt ) bel( xt )
return bel( xt )
In Algorithm 11.1, η is a normalization constant ensuring bel( xt ) integrates (or
sums) to one.10 Conceptually, the Bayes filter performs a repeated predict–correct
cycle, where the motion model spreads the belief forward to account for process
uncertainty, while the measurement model reshapes the belief according to how
consistent each state is with the observed sensor measurement.

11.3.2

Derivation

We now derive the Bayes filter recursion from the definition of the belief distribution introduced in Section 11.3. Applying Bayes’ rule to Equation (11.10) yields:
bel( xt ) = p( xt | z1:t , u1:t )

= η p(zt | xt , z1:t−1 , u1:t ) p( xt | z1:t−1 , u1:t ),

(11.12)

where η is a normalization constant:
η=

1
.
p(zt | z1:t−1 , u1:t )

Measurement update. Using the conditional independence assumptions of the
Markov model (Section 11.2), the current measurement depends only on the current state. Therefore:
p(zt | xt , z1:t−1 , u1:t ) = p(zt | xt ).
Substituting this simplification into Equation (11.12) gives:
bel( xt ) = η p(zt | xt ) p( xt | z1:t−1 , u1:t ).

10
In practice, η = 1/p(zt | z1:t−1 , u1:t ),
which follows directly from Bayes’ rule.

---

### [PDF p.294 | Book p.292]

292

principles of robot autonomy

Recall the definition of the prediction belief from Equation (11.11):
bel( xt ) := p( xt | z1:t−1 , u1:t ),
we obtain:
bel( xt ) = η p(zt | xt ) bel( xt ),
which corresponds to the measurement update step of the Bayes filter.
Prediction update. Next we derive an expression for the prediction belief bel( xt ).
Starting from its definition in Equation (11.11), we apply the law of total probability to marginalize over the previous state xt−1 :
bel( xt ) =

=

Z
Z

p( xt , xt−1 | z1:t−1 , u1:t )dxt−1
p( xt | xt−1 , z1:t−1 , u1:t ) p( xt−1 | z1:t−1 , u1:t )dxt−1 .

Using the Markov assumption again, the next state depends only on the previous state and the current control input:
p( xt | xt−1 , z1:t−1 , u1:t ) = p( xt | xt−1 , ut ).
Furthermore, the control input ut does not influence the previous state xt−1 ,
so:
p( xt−1 | z1:t−1 , u1:t ) = p( xt−1 | z1:t−1 , u1:t−1 ).
Recognizing that, by definition:
bel( xt−1 ) = p( xt−1 | z1:t−1 , u1:t−1 ),
we obtain the prediction step:
bel( xt ) =

11.3.3

Z

p( xt | xt−1 , ut ) bel( xt−1 ) dxt−1 .

Discrete Bayes Filter

When the state space is finite, the belief distribution can be represented as a
probability mass function over a discrete set of states { xk }. In this case, the belief
at time t is described by a collection of probabilities { pk,t }, where pk,t denotes
the probability that the system is in state xk at time t. The Bayes filter recursion
can then be written in discrete form by replacing the integrals in Algorithm 11.1
with summations over the possible states. The resulting algorithm, shown in
Algorithm 11.2, follows the same two-step procedure as the continuous Bayes
filter, with a prediction step using the transition model, followed by a correction
step using the measurement model. Here pk,t denotes the predicted probability of
state xk before incorporating the measurement, and η is a normalization constant
ensuring that the probabilities sum to one.

---

### [PDF p.295 | Book p.293]

introduction to localization and filtering

Algorithm 11.2: Discrete Bayes Filter
Data: { pk,t−1 }, ut , zt
Result: { pk,t }
foreach k do
pk,t = ∑i p( xt | xi , ut ) pi,t−1
pk,t = η p(zt | xk ) pk,t
return { pk,t }

11.3.4

Practical Considerations

The Bayes filter provides a general and principled framework for probabilistic
state estimation. However, applying it directly is often computationally challenging in realistic robotics problems.
In continuous state spaces, the prediction step requires evaluating integrals over
the entire state space. Computing these integrals exactly is often intractable,
resulting in the need for approximations or numerical methods to estimate the
belief distribution. In discrete state spaces, the recursion can be computed exactly,
but the required summations scale with the number of possible states. As the
dimensionality of the state increases, the number of discrete states grows rapidly,
making exact inference computationally expensive.
Despite these challenges, the Bayes filter serves as the conceptual foundation
for many practical state estimation algorithms. Widely used filters such as the
Kalman filter, extended Kalman filter (EKF), unscented Kalman filter (UKF), and
particle filter can all be viewed as specific implementations of the Bayes filter
that exploit additional assumptions or approximations to make the computation
tractable.
Example 11.3.1 (Robot in a hallway). Consider a robot moving along a straight
hallway represented by a one-dimensional line. The hidden state xt is the robot’s
position along this line. At each time step t the robot receives a control input ut
representing a commanded forward displacement and a measurement zt representing the noisy distance to the nearest door in front of the robot, obtained from
a range sensor.

Prediction. Suppose the robot starts at position xt−1 = 2 m with a belief concentrated around that location and issues a command ut = +0.5 m forward. Due to
wheel slip and actuator noise, the true displacement may vary, which we model
as:
∆x ∼ N (ut , 0.12 ).
The prediction step therefore spreads the belief forward, producing belief bel( xt )
centered at 2.5 m but with larger variance than the previous belief.

293

---

### [PDF p.296 | Book p.294]

294

principles of robot autonomy

Correction. At the same step, the robot’s range sensor reports zt = 2.4 m to the
next door. The sensor is noisy and modeled by:
p(zt | xt ) = N (zt ; true distance( xt ), 0.052 ).
If the predicted belief assigns significant probability to states near xt ≈ 2.5 m
and the hallway map indicates that the next door lies roughly 2.4 m ahead from
that position, the measurement is consistent with the prediction. The correction
step therefore increases the probability of these states and sharpens the belief
distribution around them. States that would predict very different measurements
are downweighted.
Recursive operation. Over time, the filter alternates prediction and correction.
The prediction step tends to broaden the belief because motion introduces uncertainty, while the correction step can concentrate the belief when informative
measurements are received. In hallways with repeating structures, several positions may initially produce similar sensor readings, causing the belief to remain
multimodal. As the robot gathers additional observations, the Bayes filter resolves
this ambiguity and the belief collapses around the robot’s true location.
In the repository github.com/StanfordASL/pora-exercises, the notebook
ch11/discrete_bayes.ipynb provides a concrete implementation of the discrete
Bayes filter for this hallway example. Running the notebook illustrates how the
belief distribution evolves over time as the robot moves and collects measurements.

11.4

Summary

In this chapter, we introduced the probabilistic foundations underlying robot localization and state estimation. We began by motivating why localization is essential for autonomy: robots must infer their pose from noisy and partial sensor
data rather than directly observing it. To reason systematically about this uncertainty, we reviewed key concepts in probability theory, including random variables, probability distributions, conditional independence, and Bayes’ rule. These
concepts provide the mathematical framework for representing and updating uncertainty in robotic systems.
Building on these foundations, we introduced Markov models as probabilistic representations of robot motion and sensing. These models define how the
robot’s state evolves over time and how measurements relate to that state, forming the basis for probabilistic inference in dynamic systems. Finally, we derived
the Bayes filter, a recursive algorithm for estimating a belief distribution over the
robot’s state as it moves and collects new measurements. The Bayes filter provides
the conceptual foundation for many practical estimation algorithms. Widely used
methods such as the Kalman filter, extended Kalman filter, unscented Kalman filter, and particle filter can all be understood as specific implementations of this
general framework. In the following chapters, we build on these ideas to develop

---

### [PDF p.297 | Book p.295]

introduction to localization and filtering

practical algorithms for localization, mapping, and simultaneous localization and
mapping.
To learn more. For a comprehensive introduction to probabilistic robotics, including localization and filtering, readers are referred to the seminal text by Thrun,
Burgard, and Fox [148], which provides an intuitive and rigorous treatment of
the Bayes filter and its extensions. Additional foundational perspectives on probabilistic reasoning and estimation in robotics can be found in Siegwart, Nourbakhsh, and Scaramuzza [135] and Maybeck [93]. For readers interested in a
more theoretical background in stochastic systems and control, Gelb et al. [39] offers a classical reference on estimation theory. Finally, Carlone et al. [24] presents
a modern, unified treatment of localization, filtering, and mapping under a common probabilistic framework.

11.5

Exercises

The starter code for the exercises provided below is available online through
GitHub. To get started, download the code by running in a terminal window:
git clone https://github.com/StanfordASL/pora-exercises.git

We denote Problems requiring hand-written solutions and coding in Python
with and , respectively.

Problem 1: Airport Security
Suppose that travelers passing through an airport carry prohibited items 1% of
the time. Each passenger passes through a simple detector that has a true positive
detection rate of 92% and false positive detection rate of 8%. Passengers that
trigger the detector alarm are sent to a more accurate secondary screening that
has a true positive detection rate of 98% and a false positive detection rate of 10%.
1. Given that a randomly selected passenger was flagged by the second screening,
what is the probability a passenger was carrying a prohibited item?
2. How does the probability change in this case if all passengers were to get the
more accurate secondary screening and the first simple detector was not used?

Problem 2: Cookie Machine
You operate a cookie-making machine that when activated will produce a random
number of cookies in the range [1, . . . , N ], with each quantity equally likely with
probability N1 . Each cookie costs $1 to produce.

295

---

### [PDF p.298 | Book p.296]

296

principles of robot autonomy

1. Each of your customers will pay a fixed price to activate the machine. What is
the minimum fixed price you should charge each customer to ensure that you
don’t lose money in the long run? In other words, what is the expected cost of
each customer activation?
Suppose the machine manufacturer produces machines with N = 6 and N = 10,
and unfortunately they don’t know which one they sent you, but the chance you
received either machine is equally likely. However, they did record that in a test
run of your machine it produced 5 cookies.
2. What is the probability that you received a machine configured with N = 6?
3. What is the expected number of cookies that will be produced the first time
you operate the machine?

---

### [PDF p.299 | Book p.297]

introduction to localization and filtering

References
[24]

L. Carlone et al., eds. SLAM Handbook. From Localization and Mapping to
Spatial Intelligence. Cambridge University Press, 2026.

[39]

A. Gelb et al. Applied optimal estimation. MIT press, 1974.

[93]

P. S. Maybeck. Stochastic models, estimation, and control. Vol. 3. Academic
press, 1982.

[135]

R. Siegwart, I. R. Nourbakhsh, and D. Scaramuzza. Introduction to Autonomous Mobile Robots. MIT Press, 2011.

[148]

S. Thrun, W. Burgard, and D. Fox. Probabilistic Robotics. MIT Press, 2005.

297

---

### [PDF p.300 | Book p.298]

> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]
