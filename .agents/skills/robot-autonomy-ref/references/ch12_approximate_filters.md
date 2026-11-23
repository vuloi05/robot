# Ch 12: Approximate Filters for State Estimation

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Part III: Localization & Mapping
- **Trang sách:** 299–326 | **Trang PDF:** 301–328
- **Độ ưu tiên cho dự án:** `CỐT LÕI`
- **Tóm tắt:** Phân phối Gauss, bộ lọc Kalman (KF), EKF/UKF và bộ lọc hạt (Particle Filter).

---

### [PDF p.301 | Book p.299]

12
Approximate Filters for State Estimation
In Chapter 11, we introduced the Bayes filter as the canonical framework for
state estimation. The Bayes filter uses a recursive procedure that alternates between prediction, using a probabilistic state transition model, and correction, using
a probabilistic measurement model. Intuitively, the prediction step answers the
question, “Where do we expect to be now, given where we were and how we
moved?”, while the correction step asks, “How should we revise that expectation
in light of the new sensor data?”
While conceptually elegant, the Bayes filter is rarely tractable to implement
in its full generality. The integrals in the prediction step and the normalization
in the correction step can be computationally intractable for continuous, highdimensional state spaces. In discrete domains, exact enumeration is possible in
principle but becomes impractical as the number of states grows. As a result,
practical state estimation algorithms rely on approximations of the belief distribution. Over time, two broad families of approximations have emerged:
• Parametric filters: parametric filters assume that the belief distribution belongs
to a specific parametric family (most commonly Gaussian), characterized by a
fixed set of parameters such as mean and covariance [148]. By exploiting the
structure of this representation, the belief can be updated efficiently at each
time step. The Kalman filter and its variants, including the extended Kalman
filter and unscented Kalman filter, are prominent examples.
• Non-parametric filters: non-parametric filters do not assume a fixed functional
form for the belief distribution. Instead, the distribution is approximated directly, either through discretization as in histogram filters or through sampling
as in particle filters. This flexibility allows non-parametric methods to represent multimodal and highly irregular belief distributions, although often at a
higher computational cost.
Viewed together, parametric and non-parametric filters represent two ends
of a spectrum. Parametric filters trade representational flexibility for computational efficiency, while non-parametric filters trade efficiency for expressiveness.
In robotics practice, both families play a critical role. Parametric filters often suf-

---

### [PDF p.302 | Book p.300]

300

principles of robot autonomy

fice when the problem structure is close to Gaussian and unimodal, while nonparametric filters are indispensable when ambiguity, multimodality, or strong
nonlinearities are present. It is helpful to view them as complementary rather
than mutually exclusive. Many systems use non-parametric methods for global
reasoning, then switch to parametric filters for fast local tracking once a unique
hypothesis has been identified. For instance, imagine a mobile robot navigating
a building. Early in the mission, it may be unsure which corridor or even which
floor it is on. In this case, its belief is naturally multimodal and non-parametric
methods shine. As the robot gathers more information and locks onto a unique
hypothesis, its uncertainty becomes locally well-approximated by a single Gaussian, and parametric filters become attractive for their speed and simplicity.
In the remainder of this chapter, we develop both approaches within a unified narrative. We begin by reviewing the Gaussian distribution in Section 12.1,
which forms the foundation of parametric filters. We then introduce the Kalman
filter and its variants in Section 12.2 and Section 12.3, which are the most widely
used parametric filters in robotics. Next, we turn to non-parametric filters in Section 12.4, where we relax these assumptions and represent beliefs more directly
through discretization (Section 12.4.1) or sampling (Section 12.4.2).

12.1

The Gaussian Distribution

Before we introduce specific filters, it is worth pausing to review the Gaussian distribution, which is the workhorse of parametric state estimation. The Gaussian
distribution1 is one of the most widely used probability distributions in science
and engineering and plays a central role in robotics state estimation. Its importance arises not only from its frequent appearance in natural noise processes,
but also from its favorable mathematical properties that make recursive filtering
tractable.
Informally, in one dimension, a Gaussian distribution resembles the familiar
“bell curve”: it is centered at its mean, µ, and its spread is controlled by its
variance, σ2 . In higher dimensions, a Gaussian describes an ellipsoidal cloud of
probability mass in the state space. It is high near the mean, low far away, and its
covariance matrix tells us in which directions the uncertainty is large or small.
Univariate case. The probability density function of a one-dimensional2 Gaussian
random variable X with mean µ and variance σ2 is:
p( x ) = √

1
2πσ2



( x − µ )2
exp − 12 σ2
.

(12.1)

We write this compactly as X ∼ N (µ, σ2 ), and say that “X is distributed as
a Gaussian with mean µ and variance σ2 ”. The mean, µ indicates the center
of mass of the distribution, and the variance, σ2 , measures how spread out the
distribution is around that center.

Also referred to as the Normal distribution.
1

We refer to a one-dimensional Gaussian
as univariate and to higher-dimensional
cases as multivariate.
2

---

### [PDF p.303 | Book p.301]

approximate filters for state estimation

301

Multivariate case. For an n-dimensional random vector X ∈ Rn with mean µ ∈
Rn and covariance matrix Σ ∈ Rn×n , the multivariate Gaussian distribution is
defined by:
p( x) = p

1
det(2πΣ)



exp − 21 ( x − µ)⊤ Σ−1 ( x − µ) ,

(12.2)

and we compactly write X ∼ N (µ, Σ). The covariance Σ captures both the spread
of each component of x and their pairwise correlations. Geometrically, the level
sets of a multivariate Gaussian3 are ellipsoids centered at µ, with shape and
orientation determined by the covariance matrix Σ.
The Gaussian distribution exhibits several important mathematical properties
related to affine transformations, addition, and multiplication, which make it
particularly attractive for use in filtering algorithms. We highlight three that will
be used repeatedly in what follows.
Affine transformations. The first useful property of the Gaussian distribution is
that an affine transformation of a Gaussian random variable is also a Gaussian
random variable. If the random vector X has a multivariate Gaussian distribution
with mean µ and covariance Σ, then the random variable Y computed from an
affine transformation:
Y = AX + b,
also has a multivariate Gaussian distribution with mean Aµ + b and covariance
AΣA⊤ . In other words, if X ∼ N (µ, Σ), then Y ∼ N ( Aµ + b, AΣA⊤ ).
In the context of robotics, this tells us that if our belief over the current state
is Gaussian and the dynamics are linear with additive Gaussian noise, then the
predicted state is also Gaussian. We can therefore keep track of just the mean and
covariance instead of an entire arbitrary density.
Sum. The next useful property of Gaussians is that the sum of two independent Gaussian random variables is also a Gaussian random variable. Suppose X1
and X2 have multivariate Gaussian distributions with means µ1 and µ2 and covariances Σ1 and Σ2 . Then, the random variable Y computed by the sum:
Y = X1 + X2 ,
also has a multivariate Gaussian distribution with mean µ1 + µ2 and covariance Σ1 + Σ2 . In other words, if X1 ∼ N (µ1 , Σ1 ) and X2 ∼ N (µ2 , Σ2 ), then
Y ∼ N ( µ1 + µ2 , Σ1 + Σ2 ).
In robotics, this property commonly appears when modeling additive noise.
For example, if a robot’s predicted state is Gaussian and we add independent
Gaussian process noise, the resulting state distribution remains Gaussian with
covariance equal to the sum of the individual covariances.

Each level set contains points of equal
probability density.
3

---

### [PDF p.304 | Book p.302]

302

principles of robot autonomy

Product. The product of two Gaussian probability density functions is also a
Gaussian probability density function. Consider two Gaussian probability density functions:
1


1
exp − ( x − µ1 )⊤ Σ1−1 ( x − µ1 )
2
det(2πΣ1 )

1
1
p2 ( x ) = p
exp − ( x − µ2 )⊤ Σ2−1 ( x − µ2 ) .
2
det(2πΣ2 )

p1 ( x ) = p

Their product is:
p ( x ) = p1 ( x ) · p2 ( x )

exp − 21 ( x − µ1 )⊤ Σ1−1 ( x − µ1 ) − 12 ( x − µ2 )⊤ Σ2−1 ( x − µ2 )
p
p
=
(2π )d det(Σ1 ) det(Σ2 )


exp − 12 ( x − µ)⊤ Σ−1 ( x − µ) exp − 21 (µ1⊤ Σ1−1 µ1 + µ2⊤ Σ2−1 µ2 − µ⊤ Σ−1 µ)
p
p
=
,
(2π )d det(Σ1 ) det(Σ2 )
where d is the dimension of the covariance matrices, and we can see that the
second exponential is constant with respect to x. Therefore, the product is a
Gaussian probability density function with mean µ and covariance Σ:
Σ = (Σ1−1 + Σ2−1 )−1 ,
µ = Σ(Σ1−1 µ1 + Σ2−1 µ2 ).
This property underlies the Bayes filter measurement update, where multiplying a Gaussian prior by a Gaussian likelihood yields a Gaussian posterior. The
update simply shifts the mean and shrinks or expands the covariance according
to how informative and reliable the measurement is.
Why Gaussians in filtering? These properties ensure that when both the transition
and measurement models are linear with Gaussian noise, the Bayes filter reduces
to simple recursive updates of the mean and covariance. This leads directly to
the family of Kalman filters, which we will introduce in the next section. From
a computational point of view, this is extremely attractive. Instead of carrying
around an entire function p( xt ), we only need to carry a vector µt and a matrix Σt
and update them at each time step.

12.2

Kalman Filter

The Kalman filter is the canonical parametric realization of the Bayes filter for
systems with linear dynamics and Gaussian noise. Specifically, the Kalman filter
uses a multivariate Gaussian distribution to parameterize the belief distribution
over possible states. In other words, we assume xt ∼ N (µt , Σt ), so that:
bel( xt ) = p


1
1
exp − ( xt − µt )⊤ Σ−
t ( xt − µt ) .
2
det(2πΣt )
1

---

### [PDF p.305 | Book p.303]

approximate filters for state estimation

303

Example 12.2.1 (Constant-velocity motion in one dimension). Consider a robot
moving along a straight corridor. The state encodes position and velocity:
" #
pt
xt =
,
vt
and the robot receives noisy position measurements from a range sensor. A common linear-Gaussian model is:
xt = At xt−1 + Bt ut + ϵt ,
zt = Ct xt + δt ,
where:

"

1
At =
0

#
∆t
,
1

"
Bt =

1
2
2 ∆t

#

∆t

,

h
Ct = 1

i
0 ,

and where the random variables ϵt ∼ N (0, Qt ), δt ∼ N (0, Rt ) model process
noise and measurement noise, respectively. In this setting, the Kalman filter provides the optimal recursive estimator of xt in the mean-squared error sense.
Like the Bayes filter, the Kalman filter is split up into two steps, a prediction
step and measurement update step. Both steps update the mean µ and covariance Σ of the Gaussian belief and rely on several structural assumptions about
the system.
We first assume that the initial belief bel( x0 ) is Gaussian with x0 ∼ N (µ0 , Σ0 ).
We also assume that the state transition model is linear and evolves according to:
xt = At xt−1 + Bt ut + ϵt ,

(12.3)

where xt−1 denotes the previous state, ut is the current control input, ϵt is an independent process noise that is normally distributed according to ϵt ∼ N (0, Qt ),
and At and Bt are time-varying matrices that define the dynamics. The matrix Qt ∈ Rn×n is the process noise covariance and captures uncertainty in the
motion model4
The affine structure of the dynamics together with Gaussian noise ensures that
the distribution of the next state remains Gaussian. That is, if xt−1 is Gaussian,
then xt is also Gaussian. The corresponding probabilistic transition model can
therefore be written as:
p ( x t | x t −1 , u t ) =
1

p


1
1
exp − ( xt − At xt−1 − Bt ut )⊤ Q−
t ( xt − At xt−1 − Bt ut ) ,
2
det(2πQt )

and therefore the next state is normally distributed with:
xt ∼ N ( At xt−1 + Bt ut , Qt ).
We also assume that the measurement model is linear and of the form:
zt = Ct xt + δt ,

(12.4)

Examples include unmodeled accelerations and environmental disturbances.
4

---

### [PDF p.306 | Book p.304]

304

principles of robot autonomy

where δt is an independent measurement noise that is normally distributed according to δt ∼ N (0, Rt ), and Ct is a time-varying matrix that defines how the
state maps to measurements. The matrix Rt ∈ Rm×m is the measurement noise
covariance that describes the uncertainty in the sensor measurements.
Under these assumptions, the probabilistic measurement model can be expressed as:
p(zt | xt ) = p

1


1
1
exp − (zt − Ct xt )⊤ R−
t ( zt − Ct xt ) ,
2
det(2πRt )

which implies that zt | xt ∼ N (Ct xt , Rt ). In many robotics applications, the matrix Ct selects a subset of the state variables. For example a sensor may measure
position but not velocity.
To summarize, the Kalman filter assumes that the initial belief is Gaussian
and that both the state transition model and measurement model are linear with
additive Gaussian noise. These assumptions guarantee that the belief distribution
remains Gaussian after each prediction and measurement update. As a result, the
algorithm only needs to propagate the mean µ and covariance Σ rather than a full
probability distribution. Therefore, while this property makes the Kalman filter
computationally efficient, it also limits its applicability to systems that satisfy the
assumptions of linearity and Gaussian noise.

12.2.1

Algorithm (Predict–Correct Form)

For clarity, we distinguish between the predicted belief, obtained after applying the
control but before incorporating the new measurement, and the corrected belief,
obtained after the measurement update. Algorithm 12.1 details the full algorithm,
where we denote the predicted mean and covariance by µ̄t and Σ̄t .

Intuition. The Kalman filter can be understood as a repeated negotiation between the model prediction and the sensor measurement. The prediction step
propagates the belief through the system dynamics while adding process uncertainty. The measurement update then adjusts this prediction using the newly
observed measurement, where the amount of adjustment depends on how reliable the model prediction and the sensor reading are relative to one another.
Specifically, the residual z̃t measures the discrepancy between the predicted measurement and the actual observation. The matrix St describes the expected uncertainty of this residual and is known as the innovation covariance. The Kalman gain
Kt determines how strongly the estimate should respond to the measurement:
when sensor noise is large, Kt becomes small and the filter relies more heavily on
the prediction; when the model uncertainty is large but the sensor is precise, Kt
increases and the estimate is pulled more strongly toward the measurement.

---

### [PDF p.307 | Book p.305]

approximate filters for state estimation

Algorithm 12.1: Kalman Filter (linear-Gaussian)
Data: µt−1 , Σt−1 , ut , zt
Result: µt , Σt
// Prediction (motion update)

µ̄t ← At µt−1 + Bt ut
Σ̄t ← At Σt−1 A⊤
t + Qt
// Innovation (measurement residual)

z̃t ← zt − Ct µ̄t
St ← Ct Σ̄t Ct⊤ + Rt
// Kalman gain

Kt ← Σ̄t Ct⊤ St−1
// Correction (measurement update)

µt ← µ̄t + Kt z̃t
// Covariance update (Joseph form for numerical stability)

Σt ← ( I − Kt Ct ) Σ̄t ( I − Kt Ct )⊤ + Kt Rt Kt⊤
return µt , Σt

12.2.2

Derivation

One way to derive the Kalman filter algorithm is by explicitly evaluating the
Bayes filter updates from Chapter 11 with the Gaussian belief structure and probabilistic transition and measurement models. This would involve explicitly computing an integral of p( xt | xt−1 , ut ) p( xt−1 ) for the prediction step. Instead,
we consider a more intuitive approach that directly leverages the properties of
Gaussians presented in Section 12.1 to show that the familiar update equations in
Algorithm 12.1 are an exact consequence of the linear-Gaussian assumptions.
First, from the prior belief distribution, bel( xt−1 ) ∼ N (µt−1 , Σt−1 ), we compute the predicted belief, bel( xt−1 ), by using the affine transformation property
of Gaussian random variables and the property concerning the sum of two independent Gaussian random variables. Specifically, we apply these properties to
the linear state transition model in Equation (12.3) to give the predicted mean:
µ̄t = At µt−1 + Bt ut + 0,
where the 0 comes from the mean of the independent Gaussian process noise, ϵt ∼
N (0, Qt ). The predicted covariance is then:
Σ̄t = At Σt−1 A⊤
t + Qt .
For the measurement update step of the Bayes filter, we have:
bel( xt ) ∝ p(zt | xt )bel( xt ),
where p(zt | xt ) ∼ N (Ct xt , Rt ) and bel( xt ) ∼ N (µ̄t , Σ̄t ). We can therefore use
the fact that the product of two Gaussians probability density functions is also a

305

---

### [PDF p.308 | Book p.306]

306

principles of robot autonomy

Gaussian probability density function to compute:
bel( xt ) = η exp −

1 
Jt ,
2

where η is a normalization constant and:
⊤ −1
1
Jt = (zt − Ct xt )⊤ R−
t ( zt − Ct xt ) + ( xt − µ̄t ) Σ̄t ( xt − µ̄t ).

We compute the mean, µt , for this new probability density function by finding
where the first derivative of bel( xt ) with respect to xt is zero, which occurs when
the derivative of Jt with respect to xt is zero. Similarly, we compute the new
covariance, Σt , as the inverse of the second derivative of Jt with respect to xt .
Therefore, we have the conditions:
−1
1
0 = −Ct⊤ R−
t ( zt − Ct µt ) + Σ̄t ( µt − µ̄t ),
1
⊤ −1
−1
Σ−
t = Ct Rt Ct + Σ̄t ,

which give:
1
−1 −1
Σt = (Ct⊤ R−
t Ct + Σ̄t ) .

Through algebraic manipulation, we write the mean in terms of the covariance Σt :
1
µt = µ̄t + Σt Ct⊤ R−
t ( zt − Ct µ̄t ).

With a few additional algebraic steps, we now transform these equations in the
form of the Kalman filter equations in Algorithm 12.1. From the matrix inversion
lemma, we write:
1
−1 −1
(Ct⊤ R−
= Σ̄t − Σ̄t Ct⊤ (Ct Σ̄t Ct⊤ + Rt )−1 Ct Σ̄t ,
t Ct + Σ̄t )

and then we define the Kalman gain as Kt := Σ̄t Ct⊤ (Ct Σ̄t Ct⊤ + Rt )−1 so that the
covariance is given by:
Σt = Σ̄t − Kt Ct Σ̄t .
Through some additional algebraic manipulations, we express the mean in terms
of the Kalman gain to get:
µt = µ̄t + Kt (zt − Ct µ̄t ).
Further details on this derivation and the algebraic steps involved can be found
in Thrun, Burgard, and Fox [148].

12.2.3

Practical Considerations

The Kalman filter exploits the structure of the Gaussian distribution, which makes
it a computationally efficient algorithm for filtering in a continuous state space.

---

### [PDF p.309 | Book p.307]

approximate filters for state estimation

However, the use of Gaussian beliefs also restricts the flexibility of the probabilistic model, since we have to assume the sufficiency of linear state transition
and measurement models. In practice, this linearity assumption may not be very
accurate with respect to the real world behavior of the robot and sensors. The
structure also limits the belief distribution to be unimodal, which may limit performance in some applications5 .
Despite these limitations, Kalman filters are ubiquitous in robotics. They are
widely used for fusing inertial sensors, tracking moving objects, estimating velocities from position-only measurements, and many other tasks where the state
is reasonably well modeled as evolving linearly with Gaussian noise. In the next
section, we introduce extensions to the Kalman filter that relax the linearity assumptions while retaining the Gaussian belief structure, which further expands
the applicability of this family of filters to a wider range of robotics problems.

12.3

Kalman Filter Extensions

The Kalman filter provides an exact recursive solution to the Bayes filter when the
dynamics and measurement models are linear and all uncertainty is Gaussian. In
robotics, however, these assumptions are often only approximately true, since
robot motion and sensing commonly involve nonlinear relationships. To address
this limitation, several extensions have been developed that preserve the Gaussian
belief representation while accommodating nonlinear models.
In this section, we introduce two of the most widely used approaches: the extended Kalman filter (EKF) and the unscented Kalman filter (UKF). The EKF handles
nonlinearities by linearizing the dynamics and measurement models around the
current belief mean, while the UKF propagates a carefully chosen set of sample points through the nonlinear models to capture how the belief distribution
transforms. Together, these methods provide practical and widely used tools for
nonlinear state estimation when a unimodal Gaussian approximation remains
appropriate.

12.3.1

Extended Kalman Filter (EKF)

The EKF generalizes the Kalman filter to nonlinear process and measurement
models while retaining a Gaussian belief parameterization. It does so by locally
linearizing the nonlinear models and then applying Kalman-style predict–correct
updates to the mean and covariance. This makes the EKF a practical default
for many robotics state estimation tasks with smooth nonlinear dynamics and
sensing.
Instead of the linear models in Equation (12.3) and Equation (12.4) used by the
Kalman filter, the EKF considers general nonlinear state transition and measurement models of the form:
x t = f ( x t − 1 , u t ) + ϵt ,
zt = h( xt ) + δt ,

(12.5)

307

For example, in robot localization tasks,
a multimodal distribution can better
capture the global distribution.
5

---

### [PDF p.310 | Book p.308]

308

principles of robot autonomy

where ϵt ∼ N (0, Qt ) and δt ∼ N (0, Rt ) are normally distributed process and
measurement noise terms.
The EKF incorporates these nonlinear models into the prediction and measurement update steps of the filter in two ways. First, by evaluating the nonlinear
models directly, and second, by linearizing them via a first-order Taylor series expansion. We perform the first-order Taylor series expansion of the state transition
model, f ( xt−1 , ut ), about the most likely state from the current belief distribution,
which is the expected value, µt−1 :
f ( xt−1 , ut ) ≈ f (µt−1 , ut ) + Ft ( xt−1 − µt−1 ),
where Ft = ∇ x f (µt−1 , ut ) is the Jacobian of f ( xt−1 , ut ) evaluated at µt−1 . Using
this linear approximation, we write the probabilistic state transition model as:
p ( x t | x t −1 , u t ) = p

1


1
−1
exp − ∆x⊤
t Qt ∆xt ,
2
det(2πQt )

where:
∆xt = xt − f (µt−1 , ut ) − Ft ( xt−1 − µt−1 ).
The prediction step of the EKF leverages the nonlinear state transition model and
the linearized model to update the mean and covariance as:
µ̄t = f (µt−1 , ut ),
Σ̄t = Ft Σt−1 Ft⊤ + Qt ,
which exhibits a strong similarity to the Kalman filter prediction step.
We use a similar procedure for the measurement corrections. Specifically, we
approximate the measurement model using a first-order Taylor series expansion
about the predicted point, µ̄t , to yield:
h( xt ) ≈ h(µ̄t ) + Ht ( xt − µ̄t ),
where Ht = ∇ x h(µ̄t ) is the Jacobian of h( xt ) evaluated at µ̄t . We then write the
probabilistic measurement model using this approximation as:
p(zt | xt ) = p

1


1
−1
exp − ∆z⊤
t Rt ∆zt ,
2
det(2πRt )

where ∆zt = zt − h(µ̄t ) − Ht ( xt − µ̄t ). The measurement update step of the EKF
uses the nonlinear measurement model and the linear approximation to compute:
µt = µ̄t + Kt (zt − h(µ̄t )),
Σt = ( I − Kt Ht )Σ̄t ,
where the Kalman gain is Kt = Σ̄t Ht⊤ ( Ht Σ̄t Ht⊤ + Rt )−1 . Again, we can see that
this is very similar to the Kalman filter measurement update step.
We combine the EKF prediction and measurement update steps together in
the overall EKF algorithm definition in Algorithm 12.2. Compare this to Algorithm 12.1 and you will notice only the small difference that the EKF uses a
combination of the nonlinear models and linear approximations from their Jacobians.

---

### [PDF p.311 | Book p.309]

approximate filters for state estimation

Algorithm 12.2: Extended Kalman Filter (EKF)
Data: µt−1 , Σt−1 , ut , zt
Result: µt , Σt
// Linearize dynamics at (µt−1 , ut )
Ft ← ∂ f /∂x (µ , u )
t −1

Lt ← ∂ f /∂ϵ (µ

t

t −1 , u t )

// Prediction

µ̄t ← f (µt−1 , ut )
Σ̄t ← Ft Σt−1 Ft⊤ + Lt Qt L⊤
t
// Linearize measurement at µ̄t

Ht ← ∂h/∂x µ̄

t

// Innovation and gain

z̃t ← zt − h(µ̄t )
St ← Ht Σ̄t Ht⊤ + Rt
Kt ← Σ̄t Ht⊤ St−1
// Correction

µt ← µ̄t + Kt z̃t
// Joseph-form covariance update (numerically robust)

Σt ← ( I − Kt Ht ) Σ̄t ( I − Kt Ht )⊤ + Kt Rt Kt⊤
return µt , Σt

Intuition. The EKF carries out a first-order approximation of the nonlinear models around the mean estimate, which is the most plausible operating point. The
Kalman filter formulas then apply to this locally linear surrogate. The quality of
the update hinges on the local linearity of f and h around the chosen linearization points and on the fidelity of the noise covariances. If the robot frequently
operates in regions where the models are strongly nonlinear over the uncertainty
region, or where uncertainty is large, the linearization may be poor and the EKF
can become inconsistent or even diverge.

Practical considerations. The EKF provides more accurate results than the Kalman
filter in many applications due to its ability to consider more general nonlinear
models. However, because it relies on a first-order Taylor expansion, it can perform poorly or diverge if the models are highly nonlinear over the region of
uncertainty or if the linearization point is far from the true state. The EKF also
inherits the unimodal Gaussian belief representation from the Kalman filter and
thus cannot represent multi-hypothesis uncertainty.
In practice, successful EKF deployments rely on good initializations, careful
tuning of the noise covariances, and models that are only mildly nonlinear over
the region of interest.

309

---

### [PDF p.312 | Book p.310]

310

principles of robot autonomy

12.3.2

Unscented Kalman Filter (UKF)

The UKF improves upon a core weakness of the EKF that first-order linearization can poorly capture how nonlinear transformations distort a Gaussian belief.
Instead of linearizing the nonlinear functions f and h, the UKF approximates
the belief distribution itself. It does so by propagating a carefully chosen set of
deterministically sampled points called sigma points through the true nonlinear
functions, and then recomputing the mean and covariance from the transformed
points.
Intuitively, if we start from a Gaussian belief, we can summarize it with a small
cloud of representative points that capture its shape. If we pass those points
through the nonlinear dynamics and sensing models, we can then reconstruct
a new mean and covariance that more accurately reflect how the nonlinearity
distorts the belief. This idea is formalized by the unscented transform.
Unscented transform (UT). Consider an n-dimensional Gaussian N (µ, Σ) and a
nonlinear function g(·). The UT constructs a deterministic set of 2n + 1 sigma
points {X (i) } that capture the mean and covariance of the Gaussian:

X (0) = µ,

X (i ) = µ + ci ,

X (i+n) = µ − ci , i = 1, . . . , n,

where the vectors ci are the columns of a matrix square root of (n + λ)Σ (for
example, a Cholesky factor). The scalar λ controls the spread of the sigma points
via tuning parameters (α, β, κ ), with:
λ = α2 (n + κ ) − n.
Each sigma point is assigned an associated weight for the mean and covari(i )

(i )

ance, {Wm , Wc }. A common choice is:
(0)

Wm =

λ
,
n+λ

(0)

=

Wc

and for i > 0:
(i )

(i )

Wm = Wc =

λ
+ (1 − α2 + β ),
n+λ
1
.
2( n + λ )

Here, α ∈ (0, 1] controls how far the sigma points spread from the mean, β incorporates prior knowledge about the distribution, and κ is an additional scaling
parameter. To apply the UT to a nonlinear transformation g(·), we simply pass
the sigma points through g:
Y (i) = g(X (i) ),
and then reconstruct the mean and covariance of the transformed variable as:

⊤
(i )
(i )
ȳ = ∑ Wm Y (i) ,
Pyy = ∑ Wc Y (i) − ȳ Y (i) − ȳ .
i

i

The cross-covariance between x and y = g( x) is computed analogously. This
cross-covariance quantifies how deviations in the state around µ correlate with
deviations in the transformed quantity around ȳ, and it is exactly the object
needed to form the Kalman gain in the UKF.

---

### [PDF p.313 | Book p.311]

approximate filters for state estimation

Accuracy of the UT. For Gaussian priors, the UT matches the mean and covariance of y = g( x) to at least second order6 in a Taylor expansion of g, without
evaluating any Jacobians. In contrast, the EKF’s linearization is only first-order
accurate. Intuitively, the symmetry of the sigma points around µ causes many
first- and second-order terms in the Taylor series to cancel in the weighted sums,
leaving high-order terms as the dominant approximation error. We refer the
reader to Julier and Uhlmann [60] for a detailed analysis.
From a practical point of view, the UT gives us a plug-and-play tool. We can
feed in a Gaussian belief and a nonlinear function, and it returns an updated
Gaussian that better reflects the nonlinear mapping than a first-order Taylor series.
UKF recursion (additive noise). Algorithm 12.3 can be read as a Kalman filter
where the prediction and measurement steps are implemented via the unscented
transform. For the common case with additive process and measurement noise,
the UKF proceeds as follows:
1. Sigma point generation: from the current Gaussian belief (µt−1 , Σt−1 ), construct
a set of sigma points and weights using the UT.
2. Dynamics propagation: pass each sigma point through the nonlinear state transition model f (·, ut ) to obtain predicted points. Compute the predicted mean
µ̄t and covariance Σ̄t by weighted averaging, and add the process noise covariance Qt .
3. Measurement prediction: apply the measurement model h(·) to each predicted
sigma point. Compute the predicted measurement mean ẑt , the measurement
covariance St , and the cross-covariance between state and measurement, Pf h .
4. Update: form the Kalman gain Kt = Pf h St−1 , update the mean via µt = µ̄t +
Kt (zt − ẑt ), and update the covariance Σt = Σ̄t − Kt St Kt⊤ .
For non-additive noise models, we typically augment the state vector with noise
variables and construct sigma points in this augmented space.
EKF vs. UKF: when to use each. The choice between EKF and UKF depends on the
specific problem characteristics, including the degree of nonlinearity, the availability and reliability of Jacobians, and computational constraints.
• The EKF algorithm is appropriate when the dynamics and measurement models f and h are mildly nonlinear, their Jacobians are straightforward to compute
and accurate, and the computational budget is tight. The EKF is first-order accurate in the sense that it relies on a linear approximation of f and h around the
mean and can be biased when nonlinearities are strong over the uncertainty
region.
• The UKF algorithm excels when nonlinearities in the dynamics or sensing are
substantial, derivatives are difficult to obtain or unreliable, or measurements

311

For certain choices of parameters, can
be accurate to third order.
6

---

### [PDF p.314 | Book p.312]

312

principles of robot autonomy

Algorithm 12.3: Unscented Kalman Filter (UKF)
Data: µt−1 , Σt−1 , ut , zt , (α, β, κ )
Result: µt , Σt
// Build sigma point set from (µt−1 , Σt−1 )

λ ← α2 ( n + κ ) − n
X (0) ← µ t −1
(0)

λ
Wm ← n+
λ

(0)

Wc

← n+λ λ + (1 − α2 + β)

(>0)

(>0)

Wm
← Wc
← 2(n1+λ)
C ← Cholesky((n + λ)Σt−1 )
for i = 1 to n do
X ( i ) ← µ t −1 + c i
X ( i + n ) ← µ t −1 − c i
// Propagate sigma points through dynamics

for i = 0 to 2n do
Y (i) ← f (X (i) , ut )
// Predicted mean and covariance
(i )

µ̄t ← ∑i Wm Y (i)
(i )

Pf f ← ∑i Wc Y (i) − µ̄t
Σ̄t ← Pf f + Qt



Y (i) − µ̄t

⊤

// Propagate sigma points through measurement model

for i = 0 to 2n do
Z (i) ← h(Y (i) )
// Predicted measurement mean and covariances
(i )

z̄ ← ∑i Wm Z (i)

⊤
(i )
Phh ← ∑i Wc Z (i) − z̄ Z (i) − z̄

⊤
(i )
Pf h ← ∑i Wc Y (i) − µ̄t Z (i) − z̄
// Compute gain and correction

St ← Phh + Rt
Kt ← Pf h St−1
µt ← µ̄t + Kt (zt − z̄)
// Covariance update

Σt ← Σ̄t − Kt St Kt⊤
return µt , Σt

are strongly nonlinear (for example, bearing-only measurements). For Gaussian priors, the UKF is second-order accurate in the mean and covariance, and
often higher, and typically captures the belief’s evolution more accurately than
the EKF in these regimes, at the cost of evaluating the dynamics and measurement models at 2n + 1 sigma points per step.
Example 12.3.1 (Range–bearing update (nonlinear sensing)). To see the EKF and

---

### [PDF p.315 | Book p.313]

approximate filters for state estimation

UKF in action, consider a planar robot whose state is its pose xt = [ p x , py , θ ]⊤
and that observes a fixed landmark at position ℓ = [ℓ x , ℓy ]⊤ . The robot carries a
sensor that measures the range and bearing to the landmark:

 q
(ℓ x − p x )2 + (ℓy − py )2
.
h( xt ) = 
atan2(ℓy − py , ℓ x − p x ) − θ
Both the square root and the atan2 function make this a strongly nonlinear measurement model, especially when the robot is close to the landmark or uncertain
in orientation.
EKF approach. In the EKF, we handle this nonlinearity by linearizing h around
the predicted mean µ̄t = [ p̄ x , p̄y , θ̄ ]⊤ . The resulting Jacobian:
Ht =

∂h
,
∂x µ̄t

captures how small changes in pose affect the range and bearing. Intuitively,
moving the robot towards the landmark shortens the range, while rotating the
robot changes the bearing. The measurement innovation is:
z̃t = zt − h(µ̄t ),
with the bearing residual wrapped into (−π, π ] to avoid jumps across the angle discontinuity. The standard EKF correction step then uses Ht , Rt , and the
predicted covariance to compute the Kalman gain and update the state.
Algorithm 11 shows a Python implementation of this EKF update. The structure closely mirrors the math: predict, linearize, compute the innovation and its
covariance, compute the gain, and correct.
UKF approach. The UKF handles the same problem by avoiding Jacobians altogether. Starting from the current Gaussian belief, it constructs sigma points in
the pose space, propagates them through the nonlinear motion model and the
nonlinear range–bearing sensor model, and then recomputes the predicted mean,
covariance, and cross-covariance from the transformed sigma points.
Because the UKF sees the full curvature of the measurement function through
these propagated points, it can more accurately capture how the range–bearing
observation tightens or shifts the belief, especially in regimes where the EKF’s
linear approximation is poor.
Algorithm 12 provides a Python implementation of the UKF update for this
example. Its structure is analogous to the EKF code, but with explicit sigmapoint generation, propagation, and weighted recombination in place of Jacobian
calculations.
Comparing the EKF and UKF. The two filters have the same high-level structure:
prediction, measurement prediction, computation of an innovation and its covariance, formation of a Kalman gain, and correction of the mean and covariance.
The key differences are:

313

---

### [PDF p.316 | Book p.314]

314

principles of robot autonomy

Range-Bearing Robot EKF Update
def ekf_update(prior_mean, prior_cov, z, R, landmark):
# Prediction
F = robot_jacobian(prior_mean)
pred_mean = robot_dynamics(prior_mean)
pred_cov = F @ prior_cov @ F.T
# Innovation and gain
H = range_bearing_jacobian(prior_mean, landmark)
z_hat = range_bearing(pred_mean, landmark)
innov = np.array([z[0] - z_hat[0],
wrap_angle(z[1] - z_hat[1])])
S = H @ prior_cov @ H.T + R
K = pred_cov @ H.T @ np.linalg.inv(S)
# Correction
mean = pred_mean + K @ innov
I = np.eye(3)
cov = (I - K @ H) @ pred_cov @ (I - K @ H).T + K @ R @ K.T
mean[2] = wrap_angle(mean[2])
return mean, cov

Algorithm 11: EKF update for the robot with a range-bearing sensor described in
Example 12.3.1. The code for this example is available in the repository github.c
om/StanfordASL/pora-exercises in the notebook ch12/ekf_ukf_range_bearing
.ipynb.

---

### [PDF p.317 | Book p.315]

approximate filters for state estimation

Range-Bearing Robot UKF Update
def ukf_update(prior_mean, prior_cov, z, R, landmark):
# Compute sigma points and predicted mean/covariance
X, Wm, Wc = compute_sigma_points(prior_mean, prior_cov)
Y = np.array([robot_dynamics(x) for x in X])
pred_mean = np.zeros(3)
pred_mean[0] = np.sum(Wm * Y[:,0])
pred_mean[1] = np.sum(Wm * Y[:,1])
pred_mean[2] = angle_mean(Wm, Y[:,2])
# Compute predicted measurement
Z = np.array([range_bearing(y, landmark) for y in Y])
pred_z = np.zeros(2)
pred_z[0] = np.sum(Wm * Z[:,0])
pred_z[1] = angle_mean(Wm, Z[:,1])
# Compute predicted covariances
Pff = np.zeros((3,3))
Phh = np.zeros((2,2))
Pfh = np.zeros((3,2))
for i in range(Y.shape[0]):
dz = np.array([Z[i,0] - pred_z[0],
wrap_angle(Z[i,1] - pred_z[1])])
dy = Y[i] - pred_mean
dy[2] = wrap_angle(dy[2])
Pff += Wc[i] * np.outer(dy, dy)
Phh += Wc[i] * np.outer(dz, dz)
Pfh += Wc[i] * np.outer(dy, dz)
# Compute gain and correction
pred_cov = Pff
S = Phh + R
K = Pfh @ np.linalg.inv(S)
innov = np.array([z[0] - pred_z[0],
wrap_angle(z[1] - pred_z[1])])
mean = pred_mean + K @ innov
mean[2] = wrap_angle(mean[2])
cov = pred_cov - K @ S @ K.T
return mean, cov

Algorithm 12: UKF update for the robot with a range-bearing sensor described
in Example 12.3.1. The code for this example is available in the repository gith
ub.com/StanfordASL/pora-exercises in the notebook ch12/ekf_ukf_range_bea
ring.ipynb.

315

---

### [PDF p.318 | Book p.316]

316

principles of robot autonomy

1. The EKF uses Jacobians (Ft , Ht ) and linear formulas for the prediction and
update, whereas the UKF uses explicit sigma-point generation, propagation,
and weighted recombination.
2. The UKF recomputes predicted covariances and cross-covariances by weighted
outer products of transformed sigma points instead of using linear covariance
propagation.
Discussion. The EKF and UKF are two sides of the same Gaussian belief coin.
The EKF linearizes the models and keeps the belief exact as a Gaussian, while
the UKF keeps the models exact and approximates the belief via sigma points.
Both are grounded in the Bayes filter and both maintain a single Gaussian over
the state.
This example also highlights when the extra effort of the UKF is worthwhile.
If the robot’s pose uncertainty is small and the landmark is far away, the measurement model is nearly linear locally and the EKF performs well at lower computational cost. If the robot is close to the landmark, has substantial heading
uncertainty, or the geometry is strongly nonlinear in other ways, the UKF more
faithfully captures how the observation reshapes the belief.
In the repository github.com/StanfordASL/pora-exercises, the notebook
ch12/ekf _ ukf _ range _ bearing.ipynb visualizes the EKF and UKF updates for
this problem and lets you experiment with different levels of nonlinearity and
uncertainty.

12.4

Non-parametric Filters: From Grids to Particles

Parametric filters gain efficiency by committing to a fixed belief shape7 . This
commitment is powerful when the world behaves roughly as assumed, but it
can be too rigid when uncertainty is multimodal, the dynamics or sensing are
strongly nonlinear, or data association is ambiguous.
Non-parametric filters remove this structural assumption and approximate the
belief directly. They typically do so either by:

As discussed earlier in this chapter,
usually a Gaussian distribution.
7

1. discretizing the state space into bins (histogram filters), or
2. representing the belief with samples (particle filters).
Both methods are direct approximations of the Bayes filter and trade additional
computation for representational flexibility.
Up to this point, we have mostly assumed that beliefs can be summarized by
a single Gaussian. In many robotics problems this is not realistic8 . A unimodal
Gaussian cannot represent such a situation well because it spreads probability
mass between the plausible hypotheses rather than concentrating it at those locations. Non-parametric filters are designed to address precisely this kind of
scenario.

For example, in global localization a
mobile robot may initially have no idea
which part of a building it is in, leading
to several widely separated hypotheses.
8

---

### [PDF p.319 | Book p.317]

approximate filters for state estimation

317

In the remainder of this section, we introduce two widely used non-parametric
filters that build on the Bayes filter from Chapter 11. We first discuss the histogram
filter in Section 12.4.1, which discretizes the state space, and then the particle filter
in Section 12.4.2, which represents the belief with samples.

12.4.1

Histogram Filter

The histogram filter is a non-parametric filter that can be viewed as an extension
of the discrete Bayes filter from Chapter 11 to continuous state spaces. It proceeds
by discretizing the continuous state space into a finite number of regions and then
representing the belief distribution as a set of probabilities over these regions.
Conceptually, we overlay a grid on the state space and store one number per grid
cell representing the probability that the state lies in that cell.
Mathematically, for the random state vector X, we discretize the continuous
state space, X , into a finite set of regions, or bins, such that:

X = b1 ∪ b2 ∪ . . . ∪ bK ,
where bk is the k-th bin and K is the total number of bins. For example, if a
one-dimensional state variable takes values in the interval [0, 1], the interval can
be divided into a set of equally spaced sub-intervals. The belief distribution
bel( xt ) is then represented by assigning a probability mass pk,t to each bin bk .
This quantity represents the probability that the state xt lies inside bin bk at time
t. The histogram representation can also be interpreted as a piecewise-constant
probability density function, where the density is constant within each bin and
given by:
pk,t
p( xt ) =
, x t ∈ bk ,
| bk |
where |bk | denotes the area or volume of the bin.9
To connect the histogram filter to the underlying continuous models, it is
useful to define the binwise transition and likelihood that the filter approximates. Let the continuous transition and measurement models be p( xt | xt−1 , ut )
and p(zt | xt ), respectively. We define the corresponding binwise quantities as:
(t)

Tki := p( xt ∈ bk | xt−1 ∈ bi , ut ) =

(t)

Lk := p(zt | xt ∈ bk ) =

1
| bk |

Z
x t ∈ bk

1
p( xt | xt−1 , ut ) dxt dxt−1 ,
| bi | x t − 1 ∈ bi x t ∈ b k
(12.6)
Z

Z

p(zt | xt ) dxt .

(12.7)

In principle this formulation is exact, however, in practice, directly evaluating the
integrals is usually intractable.
A common approximation associates each bin bk with a representative state
defined as the bin mean:
Z
1
x̂k :=
x dx.
(12.8)
| bk | bk

9
By construction ∑k pk,t = 1. In practice,
the probabilities are renormalized after
the correction step to maintain this property.

---

### [PDF p.320 | Book p.318]

318

principles of robot autonomy

Algorithm 12.4: Histogram Filter
Data: { pk,t−1 }, ut , zt
Result: { pk,t }
foreach k do
pk,t ← ∑i p(bk,t | bi,t−1 , ut ) pi,t−1
pk,t ← p(zt | bk,t ) pk,t
// Normalization (to enforce ∑k pk,t = 1; use log-weights if
probabilities are very small)

η ← (∑k pk,t )−1
foreach k do
pk,t ← η pk,t
return { pk,t }

Using these mean states, we approximate the binwise transition model p(bk,t |
bi,t−1 , ut ) by:
p(bk,t | bi,t−1 , ut ) ≈ η |bk | p( x̂k,t | x̂i,t−1 , ut ),
(12.9)
where p( x̂k,t | x̂i,t−1 , ut ) is the original (continuous) state transition model evaluated at the mean bin states, and η is a normalization constant.10 We discretize
the probabilistic measurement model in a similar way:
p(zt | bk,t ) ≈ p(zt | x̂k,t ),

(12.10)

so that the measurement probability associated with bin bk is approximated by
the measurement probability at the representative state x̂k .11
Once we have discretized the state space with bins bk and approximated the
transition and measurement models using the bin mean states, the histogram
filter follows the same structure as the discrete Bayes filter in Algorithm 11.2. We
summarize it in Algorithm 12.4.
A few implementation insights make the histogram filter more practical:

If the bin areas |bk | are equal, we can
absorb this term into the normalization
constant η. For higher fidelity, we may
sample multiple points per bin and average.
10

For angular variables such as headings, ensure the representative state respects periodicity and wrap residuals
appropriately.
11

• The transition matrix is typically sparse. Most motion models move probability
only to nearby bins. Rather than looping over all bin pairs (i, k ), it is often
more efficient to loop over each bi and distribute its mass to a small set of
neighboring bk .
• If p( xt | xt−1 , ut ) is shift-invariant12 , the prediction step becomes a discrete
convolution. In such cases the computation can be accelerated using separable
kernels or fast Fourier transforms in one- or two-dimensional grids.
• At domain boundaries, boundary conditions must be chosen to match the
physical system. Common choices include reflecting, absorbing, or wraparound boundaries.13
Like the discrete Bayes filter, the main disadvantage of the histogram filter is
that it can become computationally intractable when the number of bins grows

For example, additive Gaussian motion in a grid.
12

For example, orientation variables on
S1 are naturally periodic and therefore
use wrap-around boundaries.
13

---

### [PDF p.321 | Book p.319]

approximate filters for state estimation

large. This occurs when high spatial resolution is required for accuracy or when
the state space is high dimensional. For example, in a robot localization problem
where we estimate a planar pose ( x, y, θ ), discretizing x and y at 1 meter resolution in a modestly sized building and θ at 1◦ resolution can easily yield hundreds
of thousands of bins.14
Example 12.4.1 (One-dimensional motion with Gaussian noise + range sensing).
Consider a robot moving along a line segment [0, L]. We discretize this interval
into K equal bins of width ∆ = L/K, with bin k spanning [ xk− , xk+ ] and centroid
x̂k = (k − 21 )∆. The robot follows a simple additive motion model and receives a
noisy range measurement to the wall at the origin:
x t = x t −1 + u t + ϵ t ,

ϵt ∼ N (0, σu2 ),

zt = xt + νt ,

319

Cost scales roughly as O(K nnbr )
per step, where nnbr is the number
of motion-neighbor bins (often small).
Memory is O(K ). This “curse of dimensionality” is a primary motivation for
particle filters.

14

νt ∼ N (0, σz2 ).

Prediction. After applying control ut , the robot’s position distribution is shifted
and blurred according to motion noise. For each pair of bins (i, k ), the probability
of moving from bin i to bin k can be approximated by the Gaussian mass over bk
centered at x̂i + ut :
 x+ −( x̂ +u ) 
 x− −( x̂ +u ) 
(t)
Tki ≈ Φ k σui t − Φ k σui t ,
where Φ is the standard normal CDF. The predicted belief pk,t is obtained by
summing these contributions over all bins i.
Correction. Given a measurement zt , each bin is reweighted according to how
likely its centroid x̂k is under the measurement model:

(t)
Lk ≈ N zt ; x̂k , σz2 .
(t)

The posterior is then pk,t ∝ Lk pk,t , followed by normalization so that ∑k pk,t = 1.
Discussion. This process naturally captures both unimodal and multimodal beliefs. Starting from a uniform prior, the filter may, for some time, maintain several
peaks if the measurement is ambiguous15 . As more controls and measurements
accumulate, inconsistent modes gradually lose probability, and the posterior collapses to a single sharp peak near the true location. In this way, the histogram filter provides a simple yet powerful tool for global localization in low-dimensional
settings.

12.4.2

For example, if the environment has
repeated structures.
15

Particle Filter

The particle filter is a non-parametric filter that is often more computationally
tractable than the histogram filter for continuous, higher-dimensional state spaces.
Rather than discretizing the state space a priori, it represents the belief distribution by a finite set of samples from the state space, called particles.16 The key idea
is to place more particles in regions of high probability and fewer in regions of
low probability so that the particle set adapts to the shape of the belief.

The particle filter is sometimes referred to as a Monte Carlo algorithm due
to its sampling-based nature.
16

---

### [PDF p.322 | Book p.320]

320

principles of robot autonomy

We define the set of particles at time t as:
[1]

[2]

[K ]

Pt := { xt , xt , . . . , xt },
[k]

(12.11)

[k]

where xt is the k-th particle. Each particle xt represents a hypothesis about
the true state xt , and regions of the state space with more particles correspond
to regions of higher probability. Ideally, the particles are distributed according to
the current belief:
[k]

xt ∼ bel( xt ),
but in practice this holds only approximately for finite K.17
Following the Bayes filter paradigm, the particle filter updates the prior belief,
represented by Pt−1 , via a prediction step and a measurement update step.
[k]

Prediction (sampling through the dynamics). For each particle xt−1 in the prior set,
we draw a new sample from the state transition model:
[k]

[k]

x̄t ∼ p( xt | xt−1 , ut ).
This step plays the role of the motion update where the cloud of particles is
[k]

pushed forward according to the control and process noise. The resulting set { x̄t }
approximates the predicted belief bel( xt ).
Measurement weighting and resampling. We next assess how well each predicted
particle is supported by the new measurement zt . For each predicted particle, we
compute a weight:
[k]

[k]

wt = p(zt | x̄t ),
so that particles that are more consistent with the measurement receive larger
weights. We collect the predicted particles and their weights into a weighted
[k]

[k]

set P̄t = {( x̄t , wt )}, which approximates the unnormalized posterior.
The particle filter’s measurement update step then consists of resampling (with
replacement) a new set of K particles from P̄t , according to the normalized
[k]

weights wt . Particles with large weights are likely to be selected many times,
while particles with negligible weights may disappear. The resampled set Pt
approximates the updated belief bel( xt ).
We summarize the algorithm in Algorithm 12.5 and illustrate a few iterations
of the particle filter for a simple robot localization problem in Section 12.4.2.
The resampling step is important for more than just incorporating the measurement. Without resampling, repeated multiplication of weights would gradually
concentrate probability on a tiny subset of particles, while most particles would
have negligible weight and effectively be wasted. This phenomenon is known
as particle degeneracy. Resampling combats degeneracy by repeatedly discarding
low-weight particles and replicating high-weight particles, keeping the effective
sample size roughly constant.

As K → ∞, the empirical distribution
of the particles converges to the true belief under mild conditions. In many applications, on the order of K ≈ 103 particles already provides useful approximations.
17

---

### [PDF p.323 | Book p.321]

approximate filters for state estimation

Algorithm 12.5: Particle Filter
Data: Pt−1 , ut , zt
Result: Pt
P̄t ← ∅
for k = 1 to K do
[k]

[k]

Sample x̄t ∼ p( xt | xt−1 , ut )
[k]

[k]

wt ← p(zt | x̄t )
[k]

[k] 

P̄t ← P̄t ∪ x̄t , wt

// Resampling step (with replacement) according to weights

Pt ← ∅
for k = 1 to K do
[i ]

Draw index i with probability ∝ wt
[i ]
Pt ← Pt ∪ { x̄t }

return Pt

This effect has a nice interpretation in evolutionary terms: particles that explain the data well “survive and reproduce”, while those that do not are gradually removed. From a computational perspective, resampling focuses particles in
high-probability regions of the state space and reduces the number of particles
required for a given level of accuracy.

12.5

Summary

In this chapter, we examined practical approximations to the Bayes filter for continuous and high-dimensional state estimation problems in robotics. We began
by motivating the need for tractable filtering methods and introduced two broad
families of approximate filters, parametric and non-parametric, each with its own
strengths and weaknesses.
Parametric filters, such as the Kalman filter and its nonlinear extensions, the
EKF and the UKF, represent the belief as a Gaussian distribution, enabling efficient recursive updates of mean and covariance. We discussed how these filters
exploit linear or locally linear models to achieve computational efficiency, along
with their limitations in representing multimodal or highly nonlinear beliefs.
We then introduced non-parametric filters, including the histogram and particle filters, which relax parametric assumptions and directly approximate the
belief distribution through discretization or sampling. These methods trade additional computation for representational flexibility, making them effective in situations involving global uncertainty, nonlinear dynamics, or non-Gaussian noise.
Section 12.5 summarizes the main characteristics of these approaches and highlights their complementary strengths. In practice, robotic systems often combine
elements of both families in order to balance accuracy, robustness, and computational efficiency.

321

---

### [PDF p.324 | Book p.322]

322

principles of robot autonomy

Figure 12.1: A particle filter
used for robot localization. We
first update the initial set of particles according to the transition
model, and then weight them
according to the observation. Finally, we generate a new set of
particles through weighted resampling.

High-level decision guide. It is useful to relate common robotics scenarios to appropriate filter architectures. Kalman-style filters are well suited for local tracking
problems with smooth motion and reliable sensors, whereas histogram or particle filters are better suited for global localization, ambiguous data association, or
highly nonlinear environments.
1. If the robot’s dynamics or sensing models are mildly nonlinear and beliefs stay
near unimodal ⇒ EKF.
2. If the Jacobians of the dynamics or sensor models are hard to compute or their
nonlinearities are significant ⇒ UKF (or square-root UKF).
3. If there is global or multimodal uncertainty, or severe non-Gaussian noise ⇒
Particle filter.
4. If the state is low-dimensional and a map or grid is available ⇒ Histogram filter.

---

### [PDF p.325 | Book p.323]

approximate filters for state estimation

Parametric (KF / EKF / UKF)
Belief

Multimodality
Dimensionality

Single Gaussian (mean, covariance)
EKF (linearize), UKF (sigma
points)
Poor (unimodal)
Scales well with state dim

Computation

Cheap per step

When it shines

Smooth models, near-Gaussian
noise, good observability

Pitfalls

Linearization bias (EKF), covariance inconsistency

Nonlinearity

Non-parametric (Histogram /
Table 12.1: Parametric vs. NonParticle)
parametric Filters (at a glance)
Grid masses or weighted samples
Native; no Jacobians needed
Natural (multi-peak)
Histogram: suffers; Particle:
scalable with K
Histogram: grows with bins;
Particle: O(K )
Ambiguity, strong nonlinearities, non-Gaussian noise, global
localization
Degeneracy without resampling; sample impoverishment

To learn more. For a comprehensive and accessible treatment of probabilistic state
estimation and filtering methods, readers are encouraged to consult the classic
text by Thrun, Burgard, and Fox [148]. Detailed derivations and discussions
of Kalman filtering theory can also be found in Maybeck [93], while Julier and
Uhlmann [60] provide the seminal introduction to the Unscented Kalman Filter. For further reading on non-parametric filters and their applications to robot
localization, see Dellaert et al. [30]. A modern perspective that unifies filtering,
smoothing, and mapping under a probabilistic framework is presented in Carlone
et al. [24], which connects the foundations of state estimation to contemporary
SLAM and spatial-AI systems.

12.6

323

Exercises

The starter code for the exercises provided below is available online through
GitHub. To get started, download the code by running in a terminal window:
git clone https://github.com/StanfordASL/pora-exercises.git

We denote Problems requiring hand-written solutions and coding in Python
with and , respectively.

Problem 1: Kalman Filter for Landmark Localization
In this exercise, you will implement a Kalman Filter to localize a set of fixed
landmarks given knowledge about a robot’s motion. Specifically, consider an
environment where there are four landmarks, and we define the state of landmark

---

### [PDF p.326 | Book p.324]

324

principles of robot autonomy

positions as the vector:
h
m
xm
=
xt 1
t

m

yt 1

xtm2

2
ym
t

m

xt 3

m

yt 3

m

xt 4

m

yt 4

i⊤

,

which we assume we can directly measure (i.e. zt = xt ) with a noisy sensor.
In the file ch12/exercises/kalman_filter.ipynb, perform the following tasks:
1. Define the state transition matrix A from Equation (12.3) and observation matrix C from Equation (12.4) for the Kalman filter algorithm. The matrix A
should correspond to the motion of the landmarks, which we assume are stationary, and C should represent the direct measurement of the landmark positions.
2. Implement the Kalman filter predict and update steps to compute the means
and covariances at each time step.
3. Run the provided code to see the results.

---

### [PDF p.327 | Book p.325]

approximate filters for state estimation

References
[24]

L. Carlone et al., eds. SLAM Handbook. From Localization and Mapping to
Spatial Intelligence. Cambridge University Press, 2026.

[30]

F. Dellaert et al. “Monte carlo localization for mobile robots”. In: Proceedings 1999 IEEE international conference on robotics and automation (Cat. No.
99CH36288C). Vol. 2. IEEE. 1999, pp. 1322–1328.

[60]

S. J. Julier and J. K. Uhlmann. “New extension of the Kalman filter to
nonlinear systems”. In: Signal processing, sensor fusion, and target recognition
VI. Vol. 3068. Spie. 1997, pp. 182–193.

[93]

P. S. Maybeck. Stochastic models, estimation, and control. Vol. 3. Academic
press, 1982.

[148]

S. Thrun, W. Burgard, and D. Fox. Probabilistic Robotics. MIT Press, 2005.

325

---

### [PDF p.328 | Book p.326]

> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]
