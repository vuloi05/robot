# Ch 13: Robot Localization

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Part III: Localization & Mapping
- **Trang sách:** 327–344 | **Trang PDF:** 329–346
- **Độ ưu tiên cho dự án:** `CỐT LÕI`
- **Tóm tắt:** Định vị trên bản đồ biết trước: Markov Localization, EKF Localization và Monte Carlo Localization (MCL/AMCL).

---

### [PDF p.329 | Book p.327]

13
Robot Localization
The filtering algorithms developed in Chapter 11 and Chapter 12 provide general
tools for estimating the state of a dynamical system from noisy measurements.
In mobile robotics, one of the most important instances of this general problem is
localization: estimating a robot’s pose with respect to a map of the environment.
In this chapter, we specialize the Bayesian filtering framework to the robot
localization problem. We begin in Section 13.1 with a taxonomy that organizes
different localization scenarios—pose tracking versus global localization, static
versus dynamic environments, active versus passive sensing, and single-robot
versus multi-robot settings. This taxonomy provides a mental model for the kinds
of problems that arise in practice.
In Section 13.2, we then express localization formally as a Bayesian filtering
problem in which the state is the robot pose and the map is an additional, known
variable that influences both motion and measurements. This leads to map-aware
state transition and measurement models, which we discuss in Section 13.3.
Building on this formulation, in Section 13.4 we introduce Markov localization,
a general Bayes filter for estimating a robot’s pose that explicitly incorporates a
map. Markov localization is conceptually clean but rarely implemented directly;
instead, it serves as a reference from which more specialized algorithms are derived.
We then present two specializations of Markov localization. In Section 13.5, we
develop an EKF localization algorithm for feature-based maps that are well suited
to pose tracking with moderate uncertainty. Finally, in Section 13.6 we introduce
Monte Carlo Localization (MCL), a particle filter–based method that can handle
global localization and strongly multimodal beliefs. Along the way, we discuss
data association and practical considerations that arise in map-based localization.

13.1

A Taxonomy of Robot Localization Problems

Robot localization problems can differ substantially depending on how much
is known about the initial pose, how the environment evolves, how actions are
chosen, and how many robots are involved. Before turning to specific algorithms,
it is helpful to organize these variations using a taxonomy.

---

### [PDF p.330 | Book p.328]

328

principles of robot autonomy

Axis

Representative cases

Typical algorithmic implications

Initial pose

Pose tracking (local),
global localization, kidnapped robot

Environment

Static, slowly varying,
strongly dynamic

Action selection

Passive,
active
(information-seeking)

Number
robots

Single robot, multi-robot
(cooperative)

Tracking often amenable to unimodal Gaussian filters; global and
kidnapped scenarios typically require non-parametric, multimodal
beliefs (e.g., particle filters).
Static maps simplify modeling; dynamic elements motivate robust
measurement models and possibly
explicit dynamic object tracking.
Passive use treats controls as given;
active localization couples the filter
with planning methods that trade
off task progress and information
gain.
Multi-robot settings introduce
shared maps and inter-robot observations, leading to coupled
estimation problems and opportunities for improved robustness.

of

We will use the term pose to refer to the robot’s position and orientation in a
global coordinate frame. For a planar mobile robot, the pose is typically xt =
( xt , yt , θt ) at time t, where ( x, y) is the planar position and θ is the heading angle.
Pose tracking and global pose localization. One of the first distinctions among robot
localization problems concerns what we assume we know about the initial pose:
• Pose tracking (local localization). In pose tracking problems, the initial pose is
known with reasonably small uncertainty. For example, a robot may be placed
at a known charging station or docking location, with a prior belief concentrated in a small neighborhood. The goal is to maintain an accurate estimate
of pose over time as the robot moves and senses, despite process and measurement noise.
• Global localization. In global localization, the robot has very little prior information about its initial pose. For instance, it may know only that it is somewhere
within a building, but not which floor, corridor, or room. The belief over poses
must therefore represent multiple plausible hypotheses, often spread over a
large region of the map.
• Kidnapped robot problem. A challenge related to global localization arises when
a robot that has been successfully tracking its pose is suddenly transported
to a different, unknown location without its sensors or localization algorithm

Table 13.1: A taxonomy of robot
localization problems along four
key axes.

---

### [PDF p.331 | Book p.329]

robot localization

being aware of the event. This kidnapped robot problem requires the localization
method to recover from a grossly incorrect belief and reinitialize globally.
Pose tracking problems are often amenable to unimodal Gaussian approximations, such as EKF-based methods, whereas global localization and kidnapped
robot scenarios typically require non-parametric methods capable of representing multiple hypotheses, such as histogram or particle filters.
Static and dynamic environment localization. A second axis in the taxonomy of
robot localization concerns how the environment changes over time:
• Static environments. In the simplest case, the environment map is fixed and
does not change. Walls and landmarks remain in place, and any moving
objects (such as people) are ignored or treated as noise. Many foundational
localization algorithms are developed under this assumption.
• Dynamic environments. In more realistic settings, parts of the environment
change over time. Examples include doors that open and close, furniture that
moves, or other agents that occupy the same space. In these cases, the map
may be time varying or may explicitly model dynamic objects.
In this chapter, we primarily consider localization with respect to a static map,
while allowing for noisy measurements that may occasionally be corrupted by
dynamic elements. Handling fully dynamic maps is closely related to SLAM and
tracking, and will be revisited in Chapter 14.
Active and passive localization. Localization algorithms also differ in how they
interact with the environment:
• Passive localization. In passive localization, the algorithm treats the sequence
of controls u1:t as given; it does not attempt to choose actions to improve localization performance. Many navigation systems fall into this category when
localization is treated as a background process.
• Active localization. In active localization, the robot chooses its actions with the
explicit goal of reducing uncertainty about its pose. For example, the robot
may move to viewpoints that disambiguate map symmetries or collect measurements that are expected to be highly informative.
The algorithms developed in this chapter apply in both settings. When used
in an active framework, they provide the state and uncertainty estimates needed
for planning information-seeking actions.
Single and multi-robot localization.
or multiple robots:

Finally, localization problems can involve one

329

---

### [PDF p.332 | Book p.330]

330

principles of robot autonomy

• Single-robot localization. A single robot must estimate its pose using on-board
sensors and possibly an external reference, such as GPS, relative to a map that
we assume is given.
• Multi-robot localization. In multi-robot settings, several robots localize simultaneously, often sharing information. Robots may observe each other, exchange
measurements, or maintain a shared map. This introduces additional structure
and opportunities for cooperation, but also coupling between the individual
localization problems.
Throughout this chapter, we focus on single-robot localization in a known,
largely static map. The methods we develop form the basis for more advanced
multi-robot and SLAM systems.

13.2

Robot Localization via Bayesian Filtering

In previous chapters, we introduced several well-known variations of the Bayes
filter, including the parametric EKF and the non-parametric particle filter in
Chapter 12. These algorithms propagate a belief distribution over a state xt using
a probabilistic Markov state transition model and a probabilistic measurement
model. Recall that for a general state-space model, the belief at time t is defined
as:
bel( xt ) := p( xt | z1:t , u1:t ),

(13.1)

where z1:t are all measurements up to time t and u1:t are the applied controls.
In map-based localization, the state xt represents the robot pose, and we assume that a map m of the environment is given. The map encodes information
about the environment that constrains both how the robot can move and what it
can measure. Our goal is to compute the posterior over robot poses conditioned
on the map:
bel( xt ) := p( xt | z1:t , u1:t , m).
To incorporate the map into the filtering framework, we modify both the state
transition model and the measurement model. Specifically, in Section 13.3, we introduce a map-aware state transition model p( xt | xt−1 , ut , m) that captures the fact
that some poses are inconsistent with the environment. Then, in Section 13.3.1,
we introduce a map-aware measurement model p(zt | xt , m) that reflects how local sensor readings depend on nearby structures in the map. The combination
of these two models leads directly to the localization algorithms we introduce in
Section 13.5 and Section 13.6.
Map representation. Before modifying the probabilistic models, it is useful to
briefly review how we represent maps in this chapter. We assume that the environment can be described by a collection of spatial entities—either discrete landmarks or volumetric cells—with associated properties. Formally, we denote the

---

### [PDF p.333 | Book p.331]

robot localization

331

Figure 13.1: Two examples of
location-based maps. Both represent the map as a set of volumetric objects, which in these
examples are cells.

map as:
m = { m1 , m2 , . . . , m N },
where each element mi describes a portion of the environment.
Depending on the application, mi may represent the occupancy state of a grid
cell (occupied/free/unknown), the position of a point landmark, mi = (mi,x , mi,y )
in a global frame, or more complex attributes such as semantic labels or reflectivity. We will use the generic term “map element” for mi , and refer informally to
these as “objects” or “cells” when helpful.
Two important map families arise frequently in mobile robotics:
• Feature-based maps, where each mi is a compact feature, such as a point landmark or line segment, with precisely defined geometry. Section 13.2 shows
two examples of feature-based maps, one represented by lines and another by
a graph of nodes and edges.1
• Cell-based (occupancy grid) maps, where the environment is discretized into a
grid of cells, each with an associated occupancy probability. This is closely
related to the grid-based motion planning representations discussed in Section 4.2. Section 13.2 shows examples where the environment is represented
by a set of volumetric cells.
Cell-based maps trade off resolution and computational cost: smaller cells provide finer spatial detail but increase memory usage and computation time, while
larger cells reduce cost but blur detail and can misrepresent narrow passages. We
refer back to the grid-based planning discussion in Section 4.2 for a deeper treatment of these trade-offs. In this chapter, we treat the choice of map representation
as given, and focus on how the map enters the filtering equations.

Figure 13.2: Two examples of
feature-based maps. One uses a
collection of lines and the other
uses a graph representation of
the empty spaces.

Graph-based maps are generally referred to as topological maps.
1

---

### [PDF p.334 | Book p.332]

332

13.3

principles of robot autonomy

Map-Aware State Transition Model

The map influences how the robot can move. For example, a mobile robot cannot
pass through walls or leave the known workspace. A purely kinematic transition
model p( xt | xt−1 , ut ) does not capture these constraints: it might assign nonzero
probability to states that lie inside obstacles or outside the mapped area.
To incorporate the map, we consider the map-aware transition model p( xt |
xt−1 , ut , m). Directly modeling this distribution for arbitrary maps is difficult,
so we adopt an approximation that reuses the original transition model and a
separate, map-induced prior. Specifically, we define p( xt | m) as the probability
of a pose given only the map. This term characterizes how consistent a pose is
with the environment. For example, p( xt | m) = 0 for a pose inside a wall or
outside the mapped region.
Using Bayes’ rule, we can approximate the map-aware transition model as:
p ( x t | x t −1 , u t , m ) ≈ η

p ( x t | x t −1 , u t ) p ( x t | m )
,
p( xt )

(13.2)

where η is a normalization constant that ensures the left-hand side integrates to
one. Equation (13.2) can be derived step-by-step by starting from Bayes’ rule:
p ( x t | x t −1 , u t , m ) =

p ( m | x t , x t −1 , u t ) p ( x t | x t −1 , u t )
.
p ( m | x t −1 , u t )

Since p(m | xt−1 , ut ) does not depend on xt , we can absorb it into a constant η ′ :
p ( x t | x t −1 , u t , m ) = η ′ p ( m | x t , x t −1 , u t ) p ( x t | x t −1 , u t ).
Next, we assume that the influence of the past on the map is captured entirely
through the current pose xt :
p ( m | x t , x t −1 , u t ) ≈ p ( m | x t ).
Intuitively, once we know the current pose, the specific path taken to get there
does not provide additional information about the static map.2 With this assumption:
p ( x t | x t −1 , u t , m ) ≈ η ′ p ( m | x t ) p ( x t | x t −1 , u t ).
Applying Bayes’ rule again to p(m | xt ) gives:
p(m | xt ) =

p( xt | m) p(m)
.
p( xt )

Substituting into the previous expression and absorbing constant factors that do
not depend on xt into a new normalization constant η yields:
p ( x t | x t −1 , u t , m ) ≈ η
which is Equation (13.2).

p ( x t | x t −1 , u t ) p ( x t | m )
,
p( xt )

This approximation becomes more accurate as the time step between t − 1 and
t shrinks, so that the robot moves only a
short distance between successive poses.
2

---

### [PDF p.335 | Book p.333]

robot localization

In this approximation, p( xt | m) is the probability of a state given only the
map and captures the geometric consistency of that state with respect to the environment3 . The factor p( xt | xt−1 , ut ) encodes the motion model, and p( xt | m)
acts as a map-based correction that suppresses physically implausible states.
From a computational perspective, Equation (13.2) is attractive because it allows us to reuse existing implementations of the motion model and incorporate
the map through a relatively inexpensive correction:
• We first generate a kinematic prediction of the new pose using p( xt | xt−1 , ut ),
which depends only on the robot model and control.
• We then reweight or prune these predictions using p( xt | m), which often
reduces to simple operations such as checking whether the pose lies in free
space (for occupancy grids) or near a corridor (for semantic maps).
Thus, the map-aware transition model modifies the likelihood of proposed poses
without requiring a complete redesign of the underlying motion model.

13.3.1

Map-Aware Measurement Model

The map also strongly influences sensor measurements. For instance, the range
returned by a lidar beam depends on where that beam first intersects an obstacle
in the map, and the bearing to a visual landmark depends on the landmark’s
position in the global frame. To reflect this dependence, we introduce a mapaware measurement model:
p ( z t | x t , m ).
In many systems, a measurement vector zt ∈ R p consists of individual components, such as individual range beams or landmark observations. A common
simplifying assumption is that the individual components of the measurement
vector zt ∈ R p are conditionally independent given the state and map. Under
this assumption, we can factor the measurement model as:
p

p(zt | xt , m) = ∏ p(zit | xt , m).

(13.3)

i =1

The conditional independence assumption is not exact. For example, nearby
range beams may be correlated if they hit the same object. However, this assumption greatly simplifies inference and works well in many practical settings.
It allows us to process multiple sensor readings either in a batch or sequentially,
using the same underlying model p(zit | xt , m) for each component.

13.4

Markov Localization

The first map-based localization algorithm we introduce is Markov localization.
Markov localization applies the Bayes filter from Chapter 11 to the map-aware
models introduced above. The belief over robot pose at time t is:
bel( xt ) := p( xt | z1:t , u1:t , m),

333

For example, p( xt | m) = 0 for a state
xt that lies inside a wall or outside the
known map.
3

---

### [PDF p.336 | Book p.334]

334

principles of robot autonomy

and the map m is treated as known and fixed.
Using the map-aware transition and measurement models p( xt | xt−1 , ut , m)
and p(zt | xt , m), the Bayes filter recursion becomes:
Z

p( xt | xt−1 , ut , m) bel( xt−1 ) dxt−1 ,

Prediction:

bel( xt ) =

Correction:

bel( xt ) = η p(zt | xt , m) bel( xt ),

where bel( xt ) denotes the predicted belief and η is a normalization constant choR
sen so that bel( xt ) dxt = 1. We summarize this recursion in Algorithm 13.1.
Algorithm 13.1: Markov Localization
Data: bel( xt−1 ), ut , zt , m
Result: bel( xt )
foreach xt do
R
bel( xt ) = p( xt | xt−1 , ut , m)bel( xt−1 )dxt−1
bel( xt ) = η p(zt | xt , m)bel( xt )
return bel( xt )
Conceptually, Markov localization has the same structure as the Bayes filter
from Chapter 11: a prediction step that propagates the belief through the motion
model, followed by a correction step that incorporates the latest measurement.
The only difference is that both the prediction and correction now depend explicitly on the map m.
In its most general form, however, Markov localization is not directly computationally tractable. The integral over all possible poses and the need to maintain
an arbitrary belief function are prohibitive in high-dimensional or continuous
state spaces. As in Chapter 12, the key to practicality is to choose a representation
for the belief that is expressive enough for the problem at hand, yet structured
enough to admit efficient computation.
In Section 13.5, we adopt a unimodal Gaussian belief and derive an EKF-based
localization algorithm, which is well suited for pose tracking with moderate uncertainty. In Section 13.6, we adopt a particle-based representation and derive
Monte Carlo Localization, capable of handling global localization and multimodal beliefs.

13.5

EKF Localization

We now develop an EKF-based realization of Markov localization. The EKF localization algorithm assumes that the belief over the robot’s pose can be approximated by a single Gaussian:
bel( xt ) ∼ N (µt , Σt ),
and applies the EKF prediction and update equations from Chapter 12 using
map-aware models. This Gaussian structure significantly improves computa-

---

### [PDF p.337 | Book p.335]

robot localization

tional efficiency relative to the full Markov localization algorithm, at the cost
of not being able to represent multiple well-separated pose hypotheses.4
We assume the same nonlinear state transition model as in Section 12.3.1:
x t = f ( x t − 1 , u t ) + ϵt ,

335

As in Chapter 12, this unimodality assumption is well suited to pose tracking
but generally insufficient for global localization.
4

where ϵt ∼ N (0, Qt ) is zero-mean Gaussian process noise. The corresponding
state transition Jacobian is:
Ft = ∇ x f (µt−1 , ut ),

(13.4)

where µt−1 is the mean of the previous belief bel( xt−1 ).
The main difference between the general EKF and EKF localization is the presence of a feature-based map and a measurement model that relates robot poses
to observed landmarks. We assume we have a map m of N point landmarks:
m = { m1 , m2 , . . . , m N },

m j = (m j,x , m j,y ),

where each landmark m j is given by its two-dimensional location (m j,x , m j,y ) in
the global coordinate frame. At time t the robot obtains a set of landmark measurements:
zt = {z1t , z2t , . . . },
where each zit is associated (implicitly or explicitly) with one landmark.
Given a pose xt and the index j of the corresponding landmark, the measurement model is:
zit = h( xt , j, m) + δt ,
where δt ∼ N (0, Rt ) models zero-mean Gaussian sensor noise, and h(·) encodes
the expected range, bearing, or other features to landmark m j . For each measurement, the Jacobian of the measurement model with respect to the state is:
ci

Ht t = ∇ x h(µ̄t , cit , m),

(13.5)

where µ̄t is the predicted mean from the EKF prediction step, and cit is the index
of the map feature associated with measurement i.
A new challenge in feature-based localization is data association. Given a set
of measurements zt , which landmark does each measurement correspond to?
We denote the correspondence for measurement i at time t by cit ∈ {1, . . . , N +
1}, where cit = j means that measurement i corresponds to landmark m j , and
cit = N + 1 indicates that measurement i does not correspond to any known
landmark5 .
We first consider the simpler case where we assume the correspondences cit are
known.

13.5.1

EKF Localization with Known Correspondences

Assume for the moment that the correspondences ct = {c1t , c2t , . . . } are known.
The EKF localization algorithm then resembles the standard EKF from Chapter 12, with two key modifications:

For example, due to a spurious detection.
5

---

### [PDF p.338 | Book p.336]

336

principles of robot autonomy

Algorithm 13.2: EKF Localization with Known Correspondences
Data: µt−1 , Σt−1 , ut , zt , ct , m
Result: µt , Σt
// Prediction (motion update)

µ̄t = f (µt−1 , ut )
Σ̄t = Ft Σt−1 Ft⊤ + Qt
// Correction:

loop over landmark measurements

foreach zit do
j = cit
j
j
Sti = Ht Σ̄t [ Ht ]⊤ + Rt
j

Kti = Σ̄t [ Ht ]⊤ [Sti ]−1
µ̄t = µ̄t + Kti (zit − h(µ̄t , j, m))
j
Σ̄t = ( I − Kti Ht )Σ̄t
// Final posterior

µt = µ̄t
Σt = Σ̄t
return µt , Σt

1. The measurement model relates the pose to map features via h( xt , j, m).
2. Multiple landmark measurements are processed at each time step.
Given the pose xt and the map m, and given known correspondences ct , the
joint likelihood of the measurement set zt can be written as:
p ( z t | x t , c t , m ).
Using the conditional independence assumption from Equation (13.3)—now applied at the level of individual landmark measurements—we have:
p(zt | xt , ct , m) = ∏ p(zit | xt , cit , m).
i

Each factor p(zit | xt , cit , m) is a Gaussian distribution whose mean is given by
h( xt , cit , m) and whose covariance is Rt .
Because the prior over xt is Gaussian and each measurement likelihood term
is Gaussian, the posterior remains Gaussian. Moreover, under the conditional
independence assumption, we can apply the standard EKF measurement update
sequentially for each zit and obtain the same result as if we had processed all
measurements in a single stacked update. This is a consequence of the fact that,
for Gaussian models, multiplication of likelihood terms can be carried out in any
order.
Algorithm 13.2 summarizes the EKF localization recursion in the known-correspondence
case. This algorithm provides a useful baseline: if we knew which measurement
came from which landmark, EKF localization would be a straightforward specialization of the standard EKF. The main additional difficulty in practice is that the

---

### [PDF p.339 | Book p.337]

robot localization

correspondences cit are typically unknown and must be estimated jointly with the
robot state.

13.5.2

EKF Localization with Unknown Correspondences

In realistic scenarios, the correspondences cit are not given and must be inferred
from the data. One common approach is to estimate the correspondences using a
maximum likelihood (MLE) criterion. At each time step, we choose ct = {cit } to
maximize the likelihood of the current measurements:
ĉt = arg max p(zt | c1:t , m, z1:t−1 , u1:t ).
ct

In words, we select the assignment of measurements to landmarks that makes the
observed data most probable, given the map and the past history.
To make this optimization tractable, we first marginalize over the unknown
pose xt :
p(zt | c1:t , m, z1:t−1 , u1:t ) =

=

Z
Z

p(zt | xt , c1:t , m, z1:t−1 , u1:t ) p( xt | c1:t , m, z1:t−1 , u1:t )dxt ,
p(zt | xt , ct , m) bel( xt )dxt ,

where we used the Markov assumption to simplify p(zt | xt , c1:t , m, z1:t−1 , u1:t ) =
p(zt | xt , ct , m), and defined the predicted belief:
bel( xt ) := p( xt | c1:t , m, z1:t−1 , u1:t ).
The term p(zt | xt , ct , m) is the measurement model with known correspondences. Using the conditional independence assumption from Equation (13.3),
we can factor it as:
p(zt | xt , ct , m) = ∏ p(zit | xt , cit , m).
i

Substituting into the integral, we obtain:
p(zt | c1:t , m, z1:t−1 , u1:t ) =

Z

bel( xt ) ∏ p(zit | xt , cit , m) dxt .
i

Although the measurements are conditionally independent given xt , they become coupled after marginalizing over xt . A common approximation is therefore
to select correspondences independently by scoring each measurement-landmark
pairing under the predicted belief:
ĉit = arg max
cit

Z

p(zit | xt , cit , m) bel( xt ) dxt .

Under the Gaussian assumptions on the belief and measurement model, the
integral above is a Gaussian distribution with mean and covariance:
Z

ci
ci 
p(zit | xt , cit , m) bel( xt ) dxt ∼ N ẑt t , St t ,

337

---

### [PDF p.340 | Book p.338]

338

principles of robot autonomy

Algorithm 13.3: EKF Localization with Unknown Correspondences
Data: µt−1 , Σt−1 , ut , zt , m
Result: µt , Σt
µ̄t = f (µt−1 , ut )
Σ̄t = Ft Σt−1 Ft⊤ + Qt
foreach zit do
foreach landmark k in the map do
ẑkt = h(µ̄t , k, m)
Stk = Htk Σ̄t [ Htk ]⊤ + Rt
j = arg mink (zit − ẑkt )⊤ [Stk ]−1 (zit − ẑkt )
j
j
Kti = Σ̄t [ Ht ]⊤ [St ]−1
j

µ̄t = µ̄t + Kti (zit − ẑt )
j
Σ̄t = ( I − Kti Ht )Σ̄t

µt = µ̄t
Σt = Σ̄t
return µt , Σt

where:
j

j

j

j

St = Ht Σ̄t ( Ht )⊤ + Rt .

ẑt = h(µ̄t , j, m),

Maximizing the likelihood is therefore equivalent to choosing cit to maximize
j j
the Gaussian density N (zit | ẑt , St ), or equivalently to minimize the associated
Mahalanobis distance:
i,ci
ĉit = arg min dt t ,
(13.6)
cit

where:
ij

j

j

j

dt = (zit − ẑt )⊤ (St )−1 (zit − ẑt ),

(13.7)

is the Mahalanobis distance between the actual measurement zit and its prediction
j
ẑt under landmark j.
In practice, additional validation gates are often imposed: if the minimum disi ĉi

tance dt t exceeds a threshold, the measurement is treated as unmatched (assigned to the “no landmark” index N + 1) and excluded from the EKF update.
Once the correspondences ĉt have been determined, they are treated as known
in Algorithm 13.3, yielding the full EKF localization algorithm with unknown
correspondences.
Example 13.5.1 (Differential drive robot with range and bearing measurements).
Consider a differential drive robot with state x = [ x, y, θ ]⊤ and a sensor that
measures the range r and bearing ϕ to landmarks m j ∈ m in the robot’s local
coordinate frame. We assume that at each time step the robot collects multiple
measurements corresponding to different features:
zt = {[rt1 , ϕt1 ]⊤ , [rt2 , ϕt2 ]⊤ , . . . },
where each measurement zit contains the range rti and bearing ϕti .

---

### [PDF p.341 | Book p.339]

robot localization

339

Assuming the correspondences are known, the measurement model for the
range and bearing of landmark j is:
"q
#
(m j,x − x )2 + (m j,y − y)2
h( xt , j, m) =
.
(13.8)
atan2(m j,y − y, m j,x − x ) − θ
j

The measurement Jacobian Ht corresponding to a measurement from landmark j
is therefore:


m j,x −µ̄t,x
m j,y −µ̄t,y
−√
−√
0
2 +( m − µ̄ )2
2 +(m − µ̄ )2
j
(
m
−
µ̄
)
(
m
−
µ̄
)
t,x
t,y
t,x
t,y
j,x
j,y
j,x
j,y
.
(13.9)
Ht = 
m j,y −µ̄t,y
m j,x −µ̄t,x
−
−
1
2
2
2
2
(m −µ̄ ) +(m −µ̄ )
(m −µ̄ ) +(m −µ̄ )
j,x

t,x

j,y

t,y

j,x

t,x

j,y

t,y

It is also common to assume a diagonal covariance for the measurement noise:
#
"
σr2 0
,
Rt =
0 σϕ2
where σr is the standard deviation of the range measurement noise and σϕ is the
standard deviation of the bearing measurement noise. This reflects the assumption that range and bearing errors are uncorrelated.

13.6

Monte Carlo Localization (MCL)

The second practical realization of Markov localization we consider is Monte
Carlo localization (MCL). This algorithm leverages the non-parametric particle filter
framework from Chapter 12 and is particularly well suited to global pose localization and the kidnapped robot problem.6
Like the particle filter, MCL represents the belief distribution bel( xt ) by a set
of K particles:
[K ]
[1] [2]
Pt := { xt , xt , ..., xt },
[k]

where each particle xt represents a hypothesis about the true state xt . Regions
of the state space with more particles correspond to higher belief.
At each step of the algorithm, we:
1. propagate particles forward using the map-aware state transition model, and
2. weight and resample the particles using the map-aware measurement model.
This is summarized in Algorithm 13.4, which is nearly identical to the particle
filter algorithm in Algorithm 12.5, the only difference being that the map m now
appears in the probabilistic state transition and measurement models.
In global localization, MCL typically starts from a broad prior, such as having
particles spread over the entire map. As the robot moves and gathers measurements, inconsistent hypotheses are down-weighted and vanish during resampling, while particles near the true pose accumulate. This makes MCL a powerful tool for environments with strong ambiguities, repeated structures, or very
uncertain initial conditions.

We can also use MCL to solve the kidnapped robot problem by injecting new
randomly sampled particles at each step
so that the filter remains sensitive to unexpected measurements.
6

---

### [PDF p.342 | Book p.340]

340

principles of robot autonomy

Algorithm 13.4: Monte Carlo Localization
Data: Pt−1 , ut , zt , m
Result: Pt
P̄t = Pt = ∅
for k = 1 to K do
[k]

[k]

Sample x̄t ∼ p( xt | xt−1 , ut , m)
[k]

[k]

wt = p(zt | x̄t , m)
[k]
[k] 
P̄t = P̄t ∪ x̄t , wt
for k = 1 to K do
[i ]

Draw i with probability ∝ wt

[i ]
Add x̄t to Pt

return Pt

13.7

Summary

In this chapter, we examined the fundamental concepts and algorithms underlying robot localization—the process of estimating a robot’s pose relative to a
known map of the environment. We began with a taxonomy of localization
problems, distinguishing between pose tracking and global localization, static
and dynamic environments, active and passive strategies, and single-robot versus
multi-robot settings. This taxonomy provides a conceptual checklist for matching
real-world scenarios to appropriate algorithmic tools.
Building on the Bayesian estimation framework introduced earlier, we extended the state transition and measurement models to explicitly incorporate
map information. This led to the Markov localization algorithm, a general Bayesian
filter that serves as a conceptual foundation for map-aware localization.
We then explored two important realizations of this framework: EKF localization, which represents the belief as a unimodal Gaussian and is effective for pose
tracking with moderate uncertainty; and MCL, which uses a particle-based, nonparametric representation suitable for multi-hypothesis and global localization
problems. We discussed data association—the challenge of determining correspondences between sensor measurements and known map features—and techniques such as maximum-likelihood matching and validation gates to improve
robustness.
Together, these methods form the core of modern localization systems, enabling robots to estimate their position and orientation using noisy sensors, partial maps, and uncertain environments. In later chapters, these ideas will reappear in more complex settings such as simultaneous localization and mapping
(SLAM), where the robot must estimate both its pose and the map at the same
time.

---

### [PDF p.343 | Book p.341]

robot localization

To learn more. For a detailed and foundational treatment of probabilistic localization, Thrun, Burgard, and Fox [148] remains the canonical reference. The original
formulation of the Monte Carlo Localization algorithm is presented by Dellaert
et al. [30], while Leonard and Durrant-Whyte [79] provide an early and influential treatment of EKF-based localization with geometric landmarks. Readers
interested in recent advances and the connection between localization and SLAM
may refer to Cadena et al. [22] and the comprehensive modern text by Carlone
et al. [24], which unify localization and mapping under a common probabilistic
and optimization-based framework.

13.8

Exercises

The starter code for the exercises provided below is available online through
GitHub. To get started, download the code by running in a terminal window:
git clone https://github.com/StanfordASL/pora-exercises.git

We denote Problems requiring hand-written solutions and coding in Python
with and , respectively.

Problem 1: Extended Kalman Filter Localization
In this problem, you will implement an extended Kalman filter (EKF) for robot
localization in an environment where the robot can collect relative position measurements to a set of four landmarks. We will consider a robot with a discretetime dynamics model xt+1 = f ( xt , ut ) + ϵt defined by:
xt+1 = xt + Vt cos(θt )∆t + ϵtx ,
y

yt+1 = yt + Vt sin(θt )∆t + ϵt ,
θt+1 = θt + ωt ∆t + ϵtθ ,
and the goal is to estimate the unknown robot pose, xt = [ xt , yt , θt ]⊤ . The noise
y
vector ϵt = [ϵtx , ϵt , ϵtθ ]⊤ is a random variable with a zero mean Gaussian distribution ϵt ∼ N (0, Q), where Q = 0.1∆t2 I. In this problem, we assume the global
ground truth positions of the four landmarks are known. The landmarks are
stationary objects in the environment, and their combined state vector is:
h
i⊤
m = m1,x m1,y m2,x m2,y m3,x m3,y m4,x m4,y .
As the robot navigates through its environment, it receives noisy measurements
of the positions of four landmarks in the environment relative to the robot’s current pose. The measurement for landmark i is the relative position with the
measurement model:
"
# "
# " #
cos(θt )
sin(θt )  mi,x
x 
i
− t
+ δt ,
zt = h( xt , i, m) + δt =
− sin(θt ) cos(θt )
mi,y
yt

341

---

### [PDF p.344 | Book p.342]

342

principles of robot autonomy

where the measurements have an associated measurement noise with δt ∼ N (0, R),
where R = 0.25I. The full measurement vector of all landmarks is:
 1
zt
 z2 
 t
zt =  3  .
zt 
z4t
In the file ch13/exercises/ekf_localization.ipynb, complete the following:
1. Implement the functions robot_dynamics and robot_measurement to match
the dynamics and measurement models described above.
2. Implement the function dynamics_jacobian to compute the dynamics Jacobian
Ft = ∇ x f ( xt , ut ).
3. Implement the function measurement_jacobian to compute the measurement
model Jacobian Ht = ∇ x h( xt , m) for the model that computes the full measurement vector zt .
4. Implement the function ekf _ localization _ update to implement the EKF
localization update described in Algorithm 13.2. Note that you won’t need to
explicitly have a for loop in this function for each measurement since we have
defined the update to be vectorized for all measurements at once.
5. Run the provided code to see how the algorithm performs for the simulated
robot.

Problem 2: Particle Filter Localization
In this problem, we consider the same problem setup defined in Problem 1, where
we are localizing a robot given relative position measurements to a set of four
known landmarks. In the file ch13/exercises/particle_filter_localization.
ipynb, complete the following:
1. Implement the functions robot_dynamics and robot_measurement to match
the dynamics and measurement models described above. Note: you can reuse
your solution from the previous problem.
2. Implement the particle filter algorithm update function particle_filter_up
date as described in Algorithm 13.4.
3. Run the provided code to see how the algorithm performs for the simulated
robot.

---

### [PDF p.345 | Book p.343]

robot localization

References
[22]

C. Cadena et al. “Past, present, and future of simultaneous localization
and mapping: Toward the robust-perception age”. In: IEEE Transactions on
robotics 32.6 (2017), pp. 1309–1332.

[24]

L. Carlone et al., eds. SLAM Handbook. From Localization and Mapping to
Spatial Intelligence. Cambridge University Press, 2026.

[30]

F. Dellaert et al. “Monte carlo localization for mobile robots”. In: Proceedings 1999 IEEE international conference on robotics and automation (Cat. No.
99CH36288C). Vol. 2. IEEE. 1999, pp. 1322–1328.

[79]

J. J. Leonard and H. F. Durrant-Whyte. “Simultaneous map building and
localization for an autonomous mobile robot.” In: IROS. Vol. 3. 1991,
pp. 1442–1447.

[148]

S. Thrun, W. Burgard, and D. Fox. Probabilistic Robotics. MIT Press, 2005.

343

---

### [PDF p.346 | Book p.344]

> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]
