# Ch 19: Imitation Learning

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Part IV: Robot Decision Making
- **Trang sách:** 495–510 | **Trang PDF:** 497–512
- **Độ ưu tiên cho dự án:** `THAM KHẢO`
- **Tóm tắt:** Học bắt chước (Behavior Cloning) và Inverse Reinforcement Learning.

---

### [PDF p.497 | Book p.495]

19
Imitation Learning
In Chapter 16, we introduced a strategy for autonomous robot decision making
that requires a very manual and sometimes intractable process of specifying desired actions from every possible state. Then, in Chapter 17 and Chapter 18,
we formulated the sequential decision making problem as an optimization problem where we must specify a cost or reward function that we want the robot
to minimize or maximize. This optimization-based approach is more general
and scalable, but it still requires us to figure out how to appropriately embed
our preferences into the form of a mathematical function. Reward design can be
very challenging in practice, and by the nature of optimization-based approaches,
the cost or reward function can be inadvertently exploited in undesirable ways.
Additionally, in the reinforcement learning context, we require continuous and
exploratory interactions with the environment that could be costly or unsafe1 as
well as sophisticated learning algorithms that are able to learn from experience.
In practice, it can sometimes be easier, more efficient, or safer for human experts to demonstrate the desired task or behavior than it is to precisely program
it, try to encode it in a cost function, or let the robot freely interact with the
environment. The goal of imitation learning in the context of robotics is to leverage a limited set of expert demonstrations to accelerate or completely train a
robot to autonomously perform a desired behavior. In this chapter, we begin
in Section 19.1 by introducing the concept of imitation learning in the context
of robotics, provide a formal problem formulation, and discuss key design considerations. We then present a canonical imitation learning approach known as
Behavior Cloning in Section 19.2, which aims to directly learn a policy from expert
demonstrations. Lastly, in Section 19.3, we introduce Inverse Reinforcement Learning, an alternative approach to imitation learning that learns a reward function
from expert demonstrations.

19.1

Imitation Learning in Robotics

Imitation learning is a class of methods that enable skills to be transferred from
an expert to a learner. In the context of robotics, the expert is typically a human
operator or a pre-existing control policy, and the learner is the robot that aims to

For example, some robots operate in
close collaboration with humans or in
other safety-critical environments where
the risk of exploring sub-optimal actions
is significant.
1

---

### [PDF p.498 | Book p.496]

496

principles of robot autonomy

mimic the expert’s behavior. While the literature on imitation learning is vast, in
this section, we focus on core design decisions and concepts essential for understanding and applying imitation learning to robotic systems. Specifically, when
designing an imitation learning system, several key aspects must be considered:

Is imitation learning the right approach? Imitation learning might not always be the
most suitable method for learning a task. For example, reinforcement learning
might be a more effective approach if it is inexpensive for us to obtain samples
from the environment2 . Moreover, if the expert’s behavior is suboptimal or inconsistent, imitation learning may not yield the desired performance. Therefore, it
is crucial to evaluate whether imitation learning is the most appropriate method
for the given task.

What should we learn to imitate? Expert demonstrations often contain a substantial amount of information that is irrelevant to the task at hand. For example,
not all sensor measurements or control signals observed in a demonstration are
necessary for successful task execution. Consequently, a central challenge is to
identify and extract the aspects of the expert’s behavior that are truly relevant
and should be imitated by the learner.

Who is the expert? The choice of expert can significantly impact the quality of
the learned behavior. In many cases, the expert is a human operator who demonstrates the task. However, the expert could also be a pre-existing control policy,
a set of historical data, or a mixture of multiple experts. Understanding which
expert to learn from is crucial for the success of the imitation learning process.

How should we represent the policy? The choice of policy representation can greatly
influence the learning process. For instance, expert behavior can equivalently be
represented at different levels of abstraction, such as low-level motor commands,
high-level symbolic actions, or trajectory-level demonstrations. Moreover, different functional forms of the policy, such as whether the policy is defined as a linear
function or a neural network, can impact the expressiveness and generalization
capabilities of the learned policy.

What learning algorithm is most suitable? The choice of learning algorithm can
significantly impact the efficiency and performance of the imitation learning process. Many algorithms have been proposed for imitation learning, each with
its own strengths and limitations. Understanding the characteristics of different
algorithms and their suitability for the given task is essential for designing an
effective imitation learning system.

Such as if we have a good simulator for
the task because it could be very safe and
cheap to collect data.
2

---

### [PDF p.499 | Book p.497]

imitation learning

19.1.1

Differences Among Imitation Learning, Supervised Learning, and Reinforcement Learning

Imitation learning is often compared with supervised learning and reinforcement
learning, as all three paradigms involve learning from data. While these methods
share similarities, they also differ in several key aspects.
Supervised learning aims to learn a mapping from input data to output labels3 based on a dataset of input-output pairs. While the imitation learning task
of deriving a policy from a dataset of expert demonstrations is closely related to
supervised learning, there are several key differences. First, in imitation learning,
the solution may have inherent structural properties, such as physical constraints
or temporal dependencies4 , that are not present in standard supervised learning
tasks. Second, in a traditional supervised learning setting, we assume that the
source domain, which includes the dataset used for training, and the target domain, which includes the test data, are the same. In imitation learning, we may
not be able to directly transfer the expert’s behavior to the learner’s environment.
For example, the embodiment of the expert may differ from the learner, such as
if the expert is a human and the learner is a robot, leading to expert demonstrations of actions that are not directly executable by the robot. Imitation learning is
also typically exposed to the covariate shift problem, where the distribution of the
expert’s data may differ from the distribution of the learner’s data. Specifically,
the learner may encounter situations not represented in the expert’s demonstrations, requiring it to generalize beyond the expert’s behavior5 . Lastly, obtaining
expert demonstrations can be costly or time-consuming, making data collection a
significant concern.
Imitation learning is also closely related to reinforcement learning, as both
paradigms involve learning a policy from data that maximizes a reward. However, reinforcement learning methods typically require a predefined reward function to guide the robot’s behavior. In contrast, imitation learning assumes that the
expert directly provides optimal, or at least good, behavior, bypassing the need
for a reward function.

19.1.2

497

Problem Formulation

In imitation learning problems, we typically assume that we have access to a
dataset, D , of expert demonstrations. The dataset generally consists of a set of
trajectories and contexts, and we denote it mathematically as D = {(τi , si )}iN=1
where N is the number of samples and τi = { xi,0 , ui,0 , . . . , xi,T } is a trajectory
executed by the expert in a given context, si . The context si may represent a task
description, an environmental configuration, or any other relevant information
characterizing the expert’s behavior. Alternatively, the dataset may consist of
state-action pairs, where we would write D = {( xi , ui )}iN=1 .
Given such a dataset, we can broadly identify two main strategies for reproducing the expert’s behavior. A first approach is to directly learn a mapping
from contexts to trajectories, or from states to actions, using supervised learning

For example, from camera image inputs to object category outputs.
3

For example, in robot planning and
control we often have actuation limits.
4

Strategies for addressing the issues
arising from covariate shift will be discussed in more depth later in this chapter.
5

---

### [PDF p.500 | Book p.498]

498

principles of robot autonomy

techniques. That is, to learn:
π (s) = τ

or

π ( x) = u.

This approach is commonly referred to as Behavior Cloning (BC)6 .
Alternatively, we can use the expert demonstrations to learn a reward function,
R( x, u), that implicitly defines the expert’s behavior, and then infer a policy that
maximizes this reward:
"
#
π ∗ ( x) = arg max V π = arg max Eτ ∼ pπ (τ )
π

π

T. Osa et al. “An Algorithmic Perspective on Imitation Learning”. In: (2018).
url: https : / / arxiv . org / abs / 1811 .
6

06711

T −1

∑ γt R( xt , ut ) ,

t =0

where V π is the expected sum of future rewards for policy π where the expectation is over possible trajectories τ that are distributed according to p(τ ). This
approach is known as Inverse Reinforcement Learning (IRL)7 or Inverse Optimal Control (IOC).
Behavior cloning and inverse reinforcement learning are the two primary approaches to imitation learning, each with distinct strengths and limitations. In
the following sections, we discuss these approaches in more detail and provide
insights into when each method is most appropriate.

19.2

Behavior Cloning

Behavior cloning is an approach to imitation learning that focuses on directly
learning a mapping from states (or contexts) to actions (or trajectories) without
explicitly modeling the reward function. The behavior cloning task can be formulated as a supervised learning problem, where the policy π is learned by solving
a regression problem. We outline the general procedure for behavior cloning in
Algorithm 19.1.
Algorithm 19.1: Behavior Cloning
Collect a dataset, D , of expert demonstrations.
Define a model architecture for the policy, πθ.
Define a loss function, L.
Optimize the loss function, L, with respect to the model parameters, θ.
return Trained policy, πθ.
The first step consists of collecting a dataset D of expert demonstrations, for
example from logged data generated by a human operator. Next, a model architecture for the policy πθ is specified, which may take the form of a neural
network, a linear model, or another function class described by parameters θ.
The choice of model architecture depends on the complexity of the task and the
amount of available data, since the model must be expressive enough to capture
the expert’s behavior, yet not excessively complex to avoid overfitting. Then, a
loss function L is defined to quantify the discrepancy between the actions predicted by the policy and those demonstrated by the expert. Common choices

S. Arora and P. Doshi. “A survey of
inverse reinforcement learning: Challenges, methods and progress”. In: Artificial Intelligence 297 (2021), p. 103500
7

---

### [PDF p.501 | Book p.499]

imitation learning

499

include mean squared error, ℓ1 loss, hinge loss, and Kullback–Leibler divergence.
Finally, the policy parameters θ are optimized by minimizing the loss function L
over the demonstration dataset.
Behavior cloning methods are an attractive approach to learning-based decision making, primarily due to their simplicity, effectiveness, and broad applicability. However, ensuring the learned policy performs reliably in real-world settings
presents significant challenges. One of the primary obstacles to trustworthy deployment of policies learned through behavior cloning is the issue of covariate
shift.

19.2.1

The Covariate Shift Problem

Formally, covariate shift refers to a mismatch between the distribution of data
encountered during training and the distribution observed at deployment. In the
context of behavior cloning, this issue arises when the learned policy is executed
in the environment, causing small prediction errors to accumulate over time. As
these errors compound, the learner is increasingly likely to visit states that were
rarely or never encountered in the expert’s demonstrations, thereby drifting into
poorly represented regions of the state space. As a result, the agent is forced to
make decisions in unfamiliar situations, leading to poor performance and potentially catastrophic failures.
While it is impractical to gather data covering all possible states a robot might
encounter, several strategies have been developed to mitigate the impact of covariate shift. These strategies typically follow an iterative process that alternates
between updating the robot’s policy and targeted data collection based on the
robot’s current state distribution. In this section, we outline two primary approaches to address covariate shift: confidence-based methods and data aggregation
methods.

Confidence-Based Methods. In the class of confidence-based methods8 , the agent
is endowed with a mechanism for estimating uncertainty in its predictions. This
uncertainty estimate is used to identify situations in which the learned policy
is likely to make errors, thereby enabling targeted corrective interventions. A
common strategy exploits the uncertainty measure to detect regions of the state
space where the agent’s decisions are unreliable, after which additional data is
collected in those regions to improve policy performance. In some cases, this data
collection is also prompted by expert intervention, where the expert temporarily
takes control to correct the agent’s actions.
At a high level, methods based on this iterative refinement process seek to
empirically align the training data distribution with the state distribution induced
by the learned policy, thereby mitigating the effects of covariate shift. A schematic
overview of this approach is presented in Algorithm 19.2.

S. Chernova and M. Veloso. “Interactive policy learning through confidencebased autonomy”. In: Journal of Artificial
Intelligence Research 34.1 (2009), pp. 1–25.
issn: 1076-9757
8

---

### [PDF p.502 | Book p.500]

500

principles of robot autonomy

Algorithm 19.2: Confidence-based Methods
Data: Dataset of expert demonstrations, D , confidence estimation
function, c( x), confidence threshold, c0
Result: Trained policy, πθ
Train a policy, πθ, on the dataset, D .
while true do
Observe the state, xt .
Compute the confidence estimate, c( xt ).
if c( xt ) < c0 or expert intervention is necessary then
expert
Compute additional demonstration data, ( xt , ut
).
expert
D ← D ∪ {( xt , ut
)}.
Train the policy, πθ, on the updated dataset, D .
return Trained policy, πθ.

Data Aggregation Methods. Data aggregation methods constitute another major
class of approaches within behavior cloning. A prominent example is DAGGER9 ,
which mitigates covariate shift by explicitly collecting expert demonstrations under the state distribution induced by the learner’s own policy.
As outlined in Algorithm 19.3, DAGGER follows an iterative two-step procedure. First, the agent is allowed to interact with the environment, thereby generating states according to its current policy and induced state distribution. Second,
these visited states are relabeled with expert actions, and the resulting data is aggregated into the training set to refine the policy.
Algorithm 19.3: DAGGER Algorithm
Data: Initial dataset of expert demonstrations, D , initial policy, πθ1 ,
number of iterations, N
Result: Trained policy, πθN
for i = 1, 2, . . . , N do
Collect trajectories, τ = {( xt , urobot
)}, using the policy πθi .
t
Gather dataset of states visited by the robot and actions given by the
expert
expert, D i = {( xt , ut
)}.
Aggregate the dataset, D ← D ∪ D i .
Train the policy, πθi+1 , on the updated dataset, D .
return Trained policy, πθN .
In its simplest form, DAGGER begins by initializing the policy, πθ1 , using a set
of previously collected expert demonstrations. The robot then interacts with the
environment with policy πθ1 , collecting trajectories τ that reflect the state distribution under the current policy. These trajectories are subsequently relabeled using
the expert’s actions for the visited states. The relabeled trajectories are used to
train an updated policy πθ2 , which is then employed to collect additional trajectories under the state distribution induced by the updated policy. This process is

S. Ross, G. Gordon, and D. Bagnell.
“A Reduction of Imitation Learning and
Structured Prediction to No-Regret Online Learning”. In: Proceedings of the
Fourteenth International Conference on Artificial Intelligence and Statistics. 2011,
pp. 627–635
9

---

### [PDF p.503 | Book p.501]

imitation learning

501

repeated for a fixed number of iterations, resulting in the final trained policy πθN .
By collecting expert demonstrations under the learner’s state distribution, DAGGER
effectively reduces covariate shift and enhances the performance of the learned
policy. The method can be viewed as a form of interactive supervised learning,
in which the agent actively gathers data to refine its performance. This iterative
process minimizes the amount of expert data required and has proven highly
effective across a wide range of tasks.
In summary, confidence-based methods and data aggregation techniques both
provide solutions for addressing the covariate shift problem in behavior cloning.
While there are many variations of these methods, the core principles we outline in Algorithm 19.2 and Algorithm 19.3 provide a foundational understanding
of how to mitigate covariate shift through targeted data collection. However,
methods following these principles still suffer from other common limitations of
behavior cloning, such as dependence on the quality of expert demonstrations. In
Section 19.2.2, we discuss approaches that leverage ideas from behavior cloning
to learn from broader, and potentially suboptimal, sets of expert demonstrations.

19.2.2

Reinforcement Learning via Supervised Learning (RvS)

Recent work10 has explored the idea of converting the reinforcement learning
problem, which we discussed in Chapter 18, into a conditional, filtered, or weighted
imitation learning problem. These approaches are motivated by a simple but
powerful insight: rather than relying exclusively on optimal demonstrations, one
can leverage a much broader collection of demonstrations generated by suboptimal policies or gathered across diverse—yet related—tasks. Methods in this class
are often referred to as reinforcement learning via supervised learning (RvS). These
approaches typically operate by conditioning the policy on goals or desired reward levels, and may additionally incorporate mechanisms for reweighting or
filtering demonstrations
Filtering or Weighting Demonstrations. One common approach to RvS is to filter
or weight the expert demonstrations based on their quality or relevance to the
task. For example, one might assign higher weights to expert demonstrations that
obtain higher rewards. Revisiting the outline of the behavior cloning algorithm
in Algorithm 19.1, this idea can be instantiated by modifying the dataset to retain
only high-quality demonstrations, as measured by reward information.
A simple instantiation of this approach proceeds as follows. First, expert
demonstrations are ranked according to their return11 :
T −1

r ( τ ) = ∑ γ t R ( x t , u t ).
t =0

Then, the original dataset D is filtered to retain only the top k% of trajectories
based on their return:
D̃ = {τ ∈ D | r (τ ) ≥ r̄ }.

S. Emmons et al. “RvS: What is Essential for Offline RL via Supervised Learning?” In: 2021
10

The return of a trajectory is the sum
of rewards accumulated along the trajectory. When ranking trajectories, it
is generally desirable to consider longterm performance rather than immediate rewards.
11

---

### [PDF p.504 | Book p.502]

502

principles of robot autonomy

where r̄ denotes the return threshold such that k% of the trajectories in D achieve
a return greater than or equal to this value. Finally, the policy πθ is trained using
the filtered dataset D̃ .
This process represents a simple instance of RvS, in which expert trajectories
are filtered according to their return. More sophisticated variants instead operate at the level of individual transitions, rather than filtering entire trajectories.
In these cases, the quality of individual actions can be assessed using their advantage12 or, equivalently, their Q-value, instead of relying solely on immediate
rewards.
Once action weights have been computed, they can be incorporated into the
behavior cloning procedure by modifying the loss function in Algorithm 19.1 as:

L(θ) = E(x,u)∼D̃ [− log πθ (u | x) A( x, u)] .

Recall from Chapter 18 that the advantage of an action is defined as the difference between the action-value function and the value function, A( xt , ut ) =
Q( xt , ut ) − V ( xt ). Intuitively, the advantage quantifies how much better an action is relative to the average action in a
given state.
12

This objective can be interpreted as a weighted version of the standard behavior
cloning loss, where the log-likelihood of each action is scaled by its corresponding advantage. This method, commonly referred to as advantage-weighted behavior cloning, has been shown to improve the empirical performance of behavior
cloning by upweighting higher-quality actions during training.
Goal or Reward Conditioning. Another common approach to RvS is to condition
the policy on a goal or reward value. This approach is particularly useful in
settings where the expert demonstrations are suboptimal or collected from a different task. Consider a dataset of previously collected trajectories, D = {τi }. Each
trajectory τi might be described using different outcomes13 , such as the final state
of the trajectory, the total reward obtained, or a specific state visited during the
trajectory. Let ω denote a specific outcome occurring in a trajectory τ. The goal of
conditioning-based RvS is to learn an outcome-conditioned policy, πθ (u | x, ω ),
that optimizes:
L(θ) = E(x,u,ω )∼D [− log πθ (u | x, ω )] .
Among the various conditioning strategies, goal-conditioned and state-conditioned
RvS are particularly relevant. In these approaches, the policy is conditioned on
a desired outcome, typically specified as a target state or goal ω = x ∈ X that
the agent is expected to reach. For instance, in a robotic manipulation task, the
policy may be conditioned on achieving a specific end-effector configuration. Another widely used conditioning strategy is reward-conditioned RvS, in which the
policy is conditioned on a target reward value, ω = ∑tT=−01 R( xt , ut ). In this setting,
the conditioning variable encodes the desired level of performance, allowing the
policy to adapt its behavior accordingly.
In both cases, conditioning on outcomes enables the robot to extract meaningful information from suboptimal or diverse expert demonstrations, often leading to improved performance in practice. For example, consider two policies,
πθ1 (u | x) and πθ2 (u | x, ω ), that are trained on the same dataset D . Suppose
πθ1 is trained to imitate expert demonstrations that implicitly optimize a specific reward function. This reward-centric approach restricts πθ1 to behaviors that

In other words, a condition that is verified during or at the end of the trajectory.
13

---

### [PDF p.505 | Book p.503]

imitation learning

503

closely follow the expert’s trajectory distribution. On the other hand, πθ2 is goalconditioned and trained to achieve any specified goal state, ω, independent of the
underlying reward function. By explicitly incorporating the goal into its policy,
πθ2 decouples the process of achieving desired outcomes from the reward structure. As a result, πθ2 is likely to generalize better to novel tasks or unseen goal
states, as it learns a flexible mapping from states and goals to actions. In contrast,
πθ1 remains constrained by the expert’s reward-aligned demonstrations, making
it less adaptable to scenarios with divergent or ambiguous reward structures.

19.3

Inverse Reinforcement Learning

In the previous section, we discussed behavior cloning as a form of imitation
learning that directly learns a policy from expert demonstrations. Inverse reinforcement learning14 takes an orthogonal approach to imitation learning by attempting to recover a reward function from a policy, or from demonstrations of a
policy. In certain cases, identifying the reward function can offer deeper insights
into the task’s underlying structure, making it potentially more informative than
directly learning a policy. Additionally, a policy that is optimal for the expert
may not be optimal for the agent if they have different dynamics, morphologies,
or capabilities15 .
Example 19.3.1 (Inverse Reinforcement Learning vs Behavior Cloning). Consider
a scenario where the robot’s objective is to drive across a city as quickly as possible. In the context of imitation learning, we assume the reward function is
unknown, but an expert provides example routes to navigate the city. Behavior
cloning approaches attempt to replicate the expert’s actions, such as by learning
to turn right at a particular intersection. This strategy lacks robustness since it
can fail when the robot encounters intersections that the expert never visited. Inverse reinforcement learning approaches offer a more generalizable alternative by
focusing on identifying key features of the expert’s trajectories, rather than just
mimicking actions. For example, instead of merely copying the expert’s turns,
the robot could learn to recognize useful patterns, such as preferring roads with
higher speed limits or fewer stop signs. The robot can then develop a policy that
takes routes with similar advantageous characteristics, even if they differ from
the exact paths the expert took.
Formally, the goal of inverse reinforcement learning is to recover a reward
function, R : X × U → R, from a set of expert demonstrations, D = {τi }, where
τi = {( x0 , u0 , . . . , x T )} is an example trajectory. The recovered reward function
can then be used to train a policy that is optimal with respect to this reward. In
particular, given a parametric representation of the reward function with parameters w, inverse reinforcement learning seeks a parameter configuration that best
explains the observed expert behavior.
However, the inverse reinforcement learning problem is inherently ill-posed:
multiple reward functions may induce the same optimal policy, making the re-

A. Ng and S. Russell. “Algorithms
for Inverse Reinforcement Learning”. In:
Proceedings of the Seventeenth International
Conference on Machine Learning. 2000,
pp. 663–670
14

Learned reward representations can
also potentially generalize across different robot platforms that tackle similar
problems.
15

---

### [PDF p.506 | Book p.504]

504

principles of robot autonomy

ward unidentifiable from demonstrations alone. To mitigate this ambiguity, a
variety of alternative objectives have been proposed in the literature, including
maximum-margin formulations that separate optimal and suboptimal policies16 ,
as well as maximum-entropy approaches that prefer the least-committal reward
function consistent with the demonstrations17 .
In practice, most inverse reinforcement learning algorithms follow an iterative
optimization procedure involving two coupled steps. First, the reward function
parameters w are updated according to an algorithm-specific objective. Second,
the policy parameters θ are adjusted to maximize the expected return under the
current reward estimate. These steps are repeated until convergence. Although
individual inverse reinforcement learning methods differ in how these updates
are performed, Algorithm 19.4 provides a high-level schematic overview of the
inverse reinforcement learning process.

N. Ratliff, J. A. Bagnell, and M. Zinkevich. “Maximum Margin Planning”.
In: Proceedings of the 23rd International
Conference on Machine Learning. 2006,
pp. 729–736
16

B. D. Ziebart et al. “Maximum Entropy Inverse Reinforcement Learning”.
In: Proceedings of the Twenty-Third AAAI
Conference on Artificial Intelligence. 2008,
pp. 1433–1438
17

Algorithm 19.4: High-level IRL Algorithm
Data: Expert demonstrations, D , initialized reward function parameters,
w, initialized policy parameters, θ
Result: Learned reward function parameters, w, learned policy
parameters, θ
while not converged do
Update the reward function parameters, w.
Update the policy parameters, θ, to maximize the current estimate of
the reward function.
return Optimized reward and policy parameters: w, θ.
In the following sections, we first introduce the concept of feature expectation
and then discuss three popular inverse reinforcement learning methods: apprenticeship learning, maximum margin planning, and maximum entropy IRL.

19.3.1

Feature Expectation

We begin by assuming the existence of a true reward function R∗ that can be
expressed as a linear combination of features:
R∗ ( x, u) = w∗ ⊤ ϕ( x, u),
where ϕ : X × U → [0, 1]d denotes a vector of feature functions18 . In Chapter 18, we saw that the value function for a policy π is defined as the expected
cumulative discounted reward as:
"
#
VTπ ( x) = Eτ ∼ pπ (τ )

T −1

∑ γt R(xt , π (xt )) | x0 = x .

(19.1)

t =0

Substituting the linear reward model R( x, u) = w⊤ ϕ( x, u) into the expression
above yields:
VTπ ( x) = w⊤ µ(π, x),
(19.2)

To ensure that rewards are bounded by
1, we assume ∥w∗ ∥2 ≤ 1.
18

---

### [PDF p.507 | Book p.505]

imitation learning

where:

"
µ(π, x) = Eτ ∼ pπ (τ )

505

#

T −1

∑ γt ϕ(xt , π (xt )) | x0 = x .

t =0

The quantity µ(π, x ) is referred to as the feature expectation of policy π 19 .
An important insight is that, by definition, the optimal expert policy π ∗ will
always yield a value function greater than or equal to that of any other policy
and therefore:
∗
VTπ ( x) ≥ VTπ ( x), ∀ x ∈ X , ∀π.

For brevity, we may also denote
µ(π, x ) simply as µ(π ) when the dependence on the initial state is clear or omitted.
19

Using the feature-expectation formulation of the value function in Equation (19.2),
this condition can be equivalently expressed as:
w∗ ⊤ µ(π ∗ , x) ≥ w∗ ⊤ µ(π, x),

∀x ∈ X ,

∀π.

(19.3)

In principle, one could attempt to recover the expert’s reward vector w∗ by finding a vector w that satisfies the inequality in Equation (19.3). However, this formulation is inherently ambiguous. For example, the trivial choice w = 0 satisfies the inequality for all policies without conveying any meaningful preference.
More generally, multiple reward functions may induce the same optimal policy, a
phenomenon known as reward ambiguity. This issue lies at the core of inverse reinforcement learning20 , and the algorithms discussed below introduce additional
structure or optimization criteria to resolve this ambiguity.

19.3.2

Apprenticeship Learning

The apprenticeship learning algorithm21 addresses the problem of reward ambiguity by finding a policy π such that the feature expectation induced by π is
close to that of the expert policy π ∗ . Mathematically, the goal of apprenticeship
learning is to find a policy such that ∥µ(π, x) − µ(π ∗ , x)∥2 ≤ ϵ for all x ∈ X ,
where ϵ is a small positive constant. For such a policy π, we would have that for
any w with ∥w∥2 ≤ 1:
∗

|VTπ ( x) − VTπ ( x)| = |w⊤ µ(π, x) − w⊤ µ(π ∗ , x)|,
≤ ∥w∥2 ∥µ(π, x) − µ(π ∗ , x)∥2

(19.4)

≤ 1 · ϵ = ϵ,
where the first equality follows from the definition of the value function as a function of the feature expectation in Equation (19.2), the first inequality follows from
the fact that | x ⊤ y| ≤ ∥ x ∥2 ∥y∥2 for any vectors x and y, and the second inequality
follows from the assumption that ∥w∥2 ≤ 1. This result motivates a practical reformulation of the inverse reinforcement learning problem: rather than attempting to recover the true reward parameters w∗ , it suffices to learn a policy whose
feature expectations match those of the expert within a small tolerance. Under
this condition, the learned policy is guaranteed to achieve performance comparable to that of the expert, even when the recovered reward function differs from
the true underlying reward.

A. Ng and S. Russell. “Algorithms
for Inverse Reinforcement Learning”. In:
Proceedings of the Seventeenth International
Conference on Machine Learning. 2000,
pp. 663–670
20

P. Abbeel and A. Ng. “Apprenticeship Learning via Inverse Reinforcement
Learning”. In: Proceedings of the TwentyFirst International Conference on Machine
Learning. 2004
21

---

### [PDF p.508 | Book p.506]

506

principles of robot autonomy

Within this framework, the inverse reinforcement learning problem reduces
to finding a policy π whose induced feature expectation µ(π ) closely matches
the one of the expert policy, µ(π ∗ ). A schematic overview of the apprenticeship
learning algorithm is provided in Algorithm 19.5.
Algorithm 19.5: Apprenticeship Learning
Data: Expert’s feature expectations, µ∗ = µ(π ∗ ), initial policy, π0
Result: Learned parameters, w, and policy, π̂ ∗
i←1
while true do
Compute µ(i−1) = µ(πi−1 ) (or approximate via Monte
Carlo

 methods).

Compute t(i) = maxw:∥w∥2 ≤1 min j∈{0,...,(i−1)} w⊤ µ∗ − µ( j) by solving:

(wi , ti ) ← maximize t,
w,t

subject to

w⊤ µ∗ ≥ w⊤ µ( j) + t,

∀ j ∈ {0, . . . , (i − 1)},

∥w∥2 ≤ 1.
(19.5)
if ti ≤ ϵ then
π̂ ∗ ←
− best feature matching policy from {π0 , . . . , πi−1 }
∗
ŵ ←
− wi
return π̂ ∗ , ŵ∗
Compute an optimal policy, πi , for the reward function defined by ŵ.
i ← i+1

At iteration i of Algorithm 19.5, we have already identified a set of policies
π0 , π1 , . . . , πi−1 along with their corresponding feature expectations µ(0) , µ(1) , . . . , µ(i−1) .
Within the inner loop, we solve the optimization problem defined in Equation (19.5)
to estimate a reward parameter vector w that explains the expert’s behavior.
Specifically, using the feature-expectation formulation of the value function in
Equation (19.2), the constraint:
w⊤ µ∗ ≥ w⊤ µ( j) + t,
can be rewritten as:
∗

πj

VTπ ( x0 ) ≥ VT ( x0 ) + t,
meaning that, under the recovered reward function, the expert outperforms each
previously learned policy by a margin of at least t. Given the resulting reward
parameters wi , we then compute a new policy πi 22 that is optimal with respect
to this reward. This iterative procedure continues until the margin ti falls below
a predefined threshold ϵ, indicating that the feature expectations of the learned
policy sufficiently match those of the expert.

For example, using reinforcement
learning methods introduced in Chapter 18.
22

---

### [PDF p.509 | Book p.507]

imitation learning

19.3.3

Maximum Margin Planning

Maximum margin planning (MMP)23 is a generalization of apprenticeship learning that aims to find a reward function that maximally separates the expert policy
from a set of policies. Specifically, MMP modifies Equation (19.5) from the apprenticeship learning algorithm as follows:
ŵ∗ = arg min
w,ξ

subject to

N. Ratliff, J. A. Bagnell, and M. Zinkevich. “Maximum Margin Planning”.
In: Proceedings of the 23rd International
Conference on Machine Learning. 2006,
pp. 729–736
23

∥w∥22 + Cξ,
w⊤ µ∗ ≥ w⊤ µ( j) + m(π ∗ , π ( j) ) − ξ,

∀ j ∈ {0, . . . , (i − 1)},
(19.6)

where m(π, π ′ ) is a distance function24 between two policies π and π ′ , ξ is a
slack variable that allows for violations of the margin constraints, and C is a
hyperparameter that controls the penalty for such violations. Intuitively, this
formulation enforces larger margins for policies that are more dissimilar from
the expert policy π ∗ .
An advantage of the MMP formulation over the apprenticeship learning approach in Equation (19.5) arises when the expert is suboptimal. In such cases, it
may be impossible to find a reward vector w that makes the expert policy outperform all other policies. As a result, the apprenticeship learning optimization
problem may yield trivial solutions such as wi = 0 and ti = 0. By contrast, the
MMP formulation introduces slack variables that relax the margin constraints, enabling the computation of a nontrivial and informative reward vector even when
the expert demonstrations are imperfect. This added flexibility allows MMP to
remain effective in realistic scenarios where expert behavior may be noisy or suboptimal.

19.3.4

507

For example, m(π, π ′ ) could measure
the number of states in which π and π ′
select different actions.
24

Maximum Entropy Inverse Reinforcement Learning

As we described in Section 19.3, the inverse reinforcement learning problem is
inherently ill-posed since there are infinitely many reward functions that could
explain the expert’s behavior. While maximum margin approaches are highly
effective when there is a single reward function that is clearly better than alternatives, in some cases, optimizing for a distribution of reward functions is more
appropriate. Maximum entropy inverse reinforcement learning (MaxEnt IRL)25
aims to find a distribution over reward functions that explains the expert’s behavior, that matches the feature expectations of the expert26 , and has maximum
entropy27 .
Let us denote the distribution over trajectories induced by a policy π as pπ (τ ).
The feature expectations can be rewritten in terms of this distribution as:
µ(π ) = Eπ [ f (τ )] =

Z

pπ (τ ) f (τ )dτ,

where f (τ ) = ∑tT=−01 γt ϕ( xt , π ( xt )). Within this framework, MaxEnt IRL seeks a

B. D. Ziebart et al. “Maximum Entropy Inverse Reinforcement Learning”.
In: Proceedings of the Twenty-Third AAAI
Conference on Artificial Intelligence. 2008,
pp. 1433–1438
25

26

Similar to maximum margin methods.

That is, remaining as non-committal
or “random” as possible beyond the imposed constraints.
27

---

### [PDF p.510 | Book p.508]

508

principles of robot autonomy

trajectory distribution that maximizes entropy:

H( p(τ )) =

Z

− p(τ ) log p(τ )dτ,

(19.7)

subject to the constraints:
Z
Z

p(τ ) f (τ )dτ =

Z

pπ ∗ (τ ) f (τ )dτ,
(19.8)

p(τ )dτ = 1,

where the first constraint enforces that the feature expectations of the learned
behavior match those of the expert policy, while the second ensures that p(τ ) is
a valid probability distribution.
Among the distributions that satisfy the constraint:
Z

p(τ ) f (τ )dτ =

Z

pπ ∗ (τ ) f (τ )dτ,

the maximum entropy distribution follows the exponential form:
p(τ ) ∝ exp(w⊤ f (τ )).
Specifically, we can express the trajectory distribution as a function of w as:


1
p(τ | w) =
exp w⊤ f (τ ) ,
(19.9)
Z (w)
R

where Z (w) is the partition function given by Z (w) = exp w⊤ f (τ ) dτ.
However, Equation (19.9) only holds for deterministic environments where
the next state is fully determined by the current state and action. In stochastic
environments, the trajectory distribution is also influenced by the random environment dynamics, and in this case we express the distribution over trajectories
as:

 T −1
1
(19.10)
p(τ | w) =
exp w⊤ f (τ ) ∏ p( xt+1 | xt , ut ).
Z (w)
t =0
We can therefore obtain the parameter vector w for the reward function by maximizing the likelihood of the observed data under the maximum entropy distribution defined in Equation (19.10) as:
ŵ∗ = arg max LMLE = arg max ∑ ln p(τ | w).
w

19.4

w

(19.11)

τ ∈D

Summary

In this chapter, we introduced imitation learning, a paradigm for learning control
policies by demonstration. We began by formally defining the imitation learning
problem, discussing key design considerations, and highlighting its relationship
with, and key differences from, supervised and reinforcement learning. Central to this formulation, we identified two primary strategies: directly learning a
policy and inferring an underlying reward function.

---

### [PDF p.511 | Book p.509]

imitation learning

The first strategy, behavior cloning, was presented as a straightforward approach that treats imitation as a supervised learning problem, mapping expert
states to actions. We discussed its primary limitation, the covariate shift problem, where small errors accumulate and lead the robot to unfamiliar states. To
address this, we explored interactive methods like DAGGER, which mitigate covariate shift by collecting new demonstrations in states visited by the learner’s
policy. We also introduced reinforcement learning via supervised learning, an
extension that leverages suboptimal or diverse demonstration data by filtering,
weighting, or conditioning the policy on outcomes like rewards or goals.
The second strategy, inverse reinforcement learning, was introduced as an
alternative that seeks to recover the expert’s underlying reward function from
demonstrations. We highlighted that this approach can lead to more generalizable and robust policies, as it captures the expert’s intent rather than their exact
actions. We discussed the core concept of feature expectation matching and explored several prominent inverse reinforcement learning algorithms, including
Apprenticeship Learning, Maximum Margin Planning, and Maximum Entropy
IRL, each offering a different method to resolve the inherent ambiguity in recovering a reward function.
To learn more. For a comprehensive survey of imitation learning in robotics, including behavior cloning and its variants, we refer the reader to Osa et al. [107].
The seminal paper on the DAGGER algorithm is presented by Ross, Gordon, and
Bagnell [125]. For an introduction to inverse reinforcement learning, the foundational work by Ng and Russell [102] is essential. A modern survey on inverse
reinforcement learning methods can be found in Arora and Doshi [6]. Specific
influential algorithms, such as Apprenticeship Learning and Maximum Entropy
IRL, are detailed in Abbeel and Ng [1] and Ziebart et al. [168], respectively.

509

---

### [PDF p.512 | Book p.510]

510

principles of robot autonomy

References
[1]

P. Abbeel and A. Ng. “Apprenticeship Learning via Inverse Reinforcement Learning”. In: Proceedings of the Twenty-First International Conference
on Machine Learning. 2004.

[6]

S. Arora and P. Doshi. “A survey of inverse reinforcement learning: Challenges, methods and progress”. In: Artificial Intelligence 297 (2021), p. 103500.

[26]

S. Chernova and M. Veloso. “Interactive policy learning through confidencebased autonomy”. In: Journal of Artificial Intelligence Research 34.1 (2009),
pp. 1–25. issn: 1076-9757.

[34]

S. Emmons et al. “RvS: What is Essential for Offline RL via Supervised
Learning?” In: 2021.

[102]

A. Ng and S. Russell. “Algorithms for Inverse Reinforcement Learning”.
In: Proceedings of the Seventeenth International Conference on Machine Learning. 2000, pp. 663–670.

[107]

T. Osa et al. “An Algorithmic Perspective on Imitation Learning”. In:
(2018). url: https://arxiv.org/abs/1811.06711.

[118]

N. Ratliff, J. A. Bagnell, and M. Zinkevich. “Maximum Margin Planning”.
In: Proceedings of the 23rd International Conference on Machine Learning. 2006,
pp. 729–736.

[125]

S. Ross, G. Gordon, and D. Bagnell. “A Reduction of Imitation Learning
and Structured Prediction to No-Regret Online Learning”. In: Proceedings
of the Fourteenth International Conference on Artificial Intelligence and Statistics. 2011, pp. 627–635.

[168]

B. D. Ziebart et al. “Maximum Entropy Inverse Reinforcement Learning”.
In: Proceedings of the Twenty-Third AAAI Conference on Artificial Intelligence.
2008, pp. 1433–1438.
