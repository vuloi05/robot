# Prospects — Xu hướng nghiên cứu Robot Autonomy

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Tổng kết
- **Trang sách:** 511–518 | **Trang PDF:** 513–520
- **Độ ưu tiên cho dự án:** `THAM KHẢO`
- **Tóm tắt:** Tổng quan hành trình công nghệ tự hành và hướng mở rộng tương lai (Physical AI, World Models).

---

### [PDF p.513 | Book p.511]

Prospects
A Journey through the landscape of Robot Autonomy
At the outset of this book, we asked a deceptively simple question: What is robot
autonomy? We described a space between two extremes, where on one end we
have the fantastical general-purpose android of science fiction, and on the other
end we have the simple, pre-programmed machine that is capable of only a single,
narrowly defined task. In that middle ground lives the modern autonomous
robot, a system that must perceive, reason, and act in a world that is complex,
dynamic, and uncertain.
In this book, we have explored the core principles that underpin the design
and operation of modern autonomous robots. Specifically, we anchored our discussion in the See-Think-Act cycle, which provides a structured way to understand
the flow of information and decision-making in an autonomous system. By now,
that abstraction should feel less like a theoretical construct and more like a technical blueprint. Let us briefly revisit each of these stages and reflect on the key
insights that emerged from our exploration:
See. We emphasized how the See stage is not merely about the passive acquisition of data, but about the active process of extracting meaningful information
from the environment. Much of this discussion appeared in Part II, where we began by examining the fundamental properties and limitations of common sensing
modalities, both proprioceptive and exteroceptive, and by establishing the physical and geometric principles that govern their measurements. Building on this
foundation, we explored how raw sensor data can be transformed into structured
and informative representations. We first surveyed classical approaches, including filtering techniques, feature detection, and methods for extracting geometric
information about the environment. We then turned to modern, learning-based
techniques, examining how deep neural network architectures enable end-to-end
learning of rich representations directly from raw sensory inputs, including images as well as point-based and voxel-based representations of 3D geometry. Finally, we discussed higher-level visual understanding tasks such as object detection and segmentation, in which algorithms must interpret scenes by identifying
object instances and reasoning about their spatial relationships.
Taken together, the See phase is not simply about sensing, but about percep-

---

### [PDF p.514 | Book p.512]

512

principles of robot autonomy

tion, where the robot must transform raw sensory signals into the rich, semantic
representations that are necessary for it to think and act intelligently.
Think. Once the See stage has produced a structured and semantically meaningful representation of the world, the Think stage is where that representation
is transformed into actionable intent. This is the stage in which the robot reasons about where it is with respect to its environment, its goals, and how its
actions will shape future outcomes. In Part III, we discussed how this process
typically begins with robot localization and mapping, where local sensor measurements are synthesized into a coherent global estimate of the robot’s state
and a map of the environment. Building on this foundation, Part IV introduced
techniques for high-level decision-making. Specifically, we discussed approaches
to sequential decision-making, where the robot determines, loosely speaking, what
to do, ultimately defining the objectives that guide subsequent stages of planning and control. To address this problem, we explored methods rooted in optimal control, such as dynamic programming, and extended this perspective to
modern learning-based approaches, such as reinforcement learning and imitation
learning. Across these frameworks, we emphasized different but complementary
strategies for reasoning under uncertainty, balancing model-based formulations
with data-driven approximations.
Viewed holistically, the Think phase emerges as a structured process that transforms information about the environment and abstract goals into concrete plans
and intentions that can be executed by the robot.
Act. The final stage of the cycle, Act, is where high-level decisions are translated
into physical motion. While the Think stage determines what the robot should do,
the Act stage determines how those decisions are realized by a dynamical system
subject to physical constraints. In Part I, we developed the tools required to bridge
this gap. We began with modeling the robot as a dynamical system, introducing
the representations and notation needed to describe its motion and constraints.
Building on this foundation, we discussed how desired behaviors are converted
into feasible trajectories through motion planning and trajectory optimization.
Motion planning algorithms produce geometrically feasible, collision-free paths,
while trajectory optimization refines these paths into time-parameterized motions that respect dynamics, actuator limits, and task requirements. Execution,
however, is never merely the blind following of precomputed motor commands.
The real world is inherently uncertain, subject to external disturbances, sensor
noise, actuator limitations, and inevitable inaccuracies in the robot’s internal dynamic models. For this reason, execution must be grounded in the principle of
feedback control. Rather than assuming that a planned trajectory will unfold exactly as predicted, feedback control continuously compares the robot’s measured
state against its desired state and corrects deviations in real time. Our discussion spanned a spectrum of closed-loop control strategies, from classical PID
to optimization-based methods, such as Linear Quadratic Regulators (LQR) and

---

### [PDF p.515 | Book p.513]

prospects

Model Predictive Control (MPC), which explicitly reason about system dynamics,
performance objectives, and constraints.
Viewed in the context of the full See-Think-Act cycle, the Act phase closes the
loop between intention and reality. It is where plans meet physical embodiment,
and where the robot’s ability to adapt and respond to the unpredictable nature
of the real world is put to the test.

From Modular Pipelines to End-to-End Autonomy.
Throughout this book, we have emphasized that the stages of See, Think, and
Act are not isolated modules, but deeply interconnected processes with information flowing asynchronously at different rates, and with multiple feedback loops.
At the same time, the field is undergoing a noticeable shift from carefully engineered, modular autonomy stacks toward increasingly end-to-end frameworks.
In classical architectures, perception, state estimation, planning, and control are
designed and tuned as distinct components, each with explicit interfaces and
well-defined responsibilities. In contrast, modern data-driven systems often blur
or even collapse these boundaries, and can now solve tasks that were once considered beyond the reach of traditional, non-learning-based systems.
This shift toward end-to-end learning has been enabled by the availability of
large-scale datasets, increasingly realistic simulation environments, and unprecedented computational resources. End-to-end learning promises greater adaptability, reduced manual engineering, and the ability to capture complex couplings
that are difficult to model analytically. Yet, this evolution does not make the material in this book any less relevant, as the principles and techniques of sensing,
estimation, planning, and control continue to underpin the design and analysis
of these end-to-end systems. For instance, modular components often serve as
strong baselines against which end-to-end approaches are compared. Classical
algorithms frequently reappear as safety layers, fallback strategies, or constraintenforcing mechanisms wrapped around learned policies, ensuring that the system maintains a degree of interpretability, reliability, and safety. Moreover, this
data-centric paradigm introduces new system-level challenges. The design of
datasets, labeling pipelines, simulation environments, evaluation metrics, and
benchmarking protocols becomes even more critical, and often draws heavily
on traditional techniques from perception, state estimation, and control. In this
sense, the traditional See-Think-Act abstraction continues to provide not only a
conceptual framework, but also a powerful lens through which to analyze, debug,
and responsibly deploy the increasingly end-to-end systems that are shaping the
future of robot autonomy.

The Road Ahead
As we write this book, we find ourselves at a remarkable inflection point in
robotics research, where advances in computation, sensing, machine learning,

513

---

### [PDF p.516 | Book p.514]

514

principles of robot autonomy

and large-scale data are rapidly reshaping how autonomous systems are designed, developed, and operated. In this final section, we will briefly reflect on
some of the most exciting emerging trends in robotics research, and how they are
shaping the future of robot autonomy.
Foundation Models (FMs). Over the past few years, artificial intelligence has undergone a dramatic shift driven by large-scale foundation models. Citing the seminal work of Bommasani et al. [18], we define foundation models as:
“[Foundation models are] models that are trained on broad data (generally using self-supervision
at scale) that can be adapted (e.g., fine-tuned) to a wide range of downstream tasks.”

Importantly, the term “foundation model” is not meant to refer to a specific architecture. Rather, it describes a class of models characterized by scale, broad
pretraining, and adaptability. Well-known examples include large language models (LLMs) 28 29 , which underpin systems such as ChatGPT, as well as visionlanguage models (VLMs) 30 , video generation models 31 , and other large-scale
architectures 32 . Beyond their impact on purely digital applications, foundation
models are increasingly being integrated into physical robotic systems.
Their growing relevance in robotics stems from several key properties. First,
foundation models provide broad priors about the world. Trained on large and
diverse datasets, they encode a wealth of information about the structure of language, visual concepts, and physical interactions, enabling improved generalization in settings with limited task-specific data.
Second, foundation models are inherently multimodal. Many modern architectures jointly process text, images, video, audio, and structured data. Robotics, by
its very nature, is a multimodal domain where robots must integrate information
from diverse sensory modalities such as vision, proprioception, tactile sensing,
and language-based instructions. Multimodal foundation models offer a unified
representational framework in which these heterogeneous data streams can be
fused and reasoned over coherently.
Third, foundation models provide a powerful and flexible interface for humanrobot interaction. Language-conditioned policies enable users to specify goals in
natural language rather than low-level commands. This dramatically lowers the
barrier between human intent and robotic execution, enabling more intuitive
forms of supervision, correction, and collaboration.
Within this broader paradigm, several emerging instantiations of foundation
models are particularly influential in robotics:
Vision–language–action (VLA) and reasoning models. VLA models 33 34 35 represent an emerging class of architectures that directly couple vision and language
representations to action outputs. In contrast to traditional pipelines where perception, planning, and control are engineered as separate modules, VLA models
attempt to learn end-to-end mappings from multimodal inputs to motor commands or high-level actions, essentially learning the See-Think-Act cycle as a single, integrated process. Typically pretrained on large-scale vision and language

A. Radford et al. “Language Models
are Unsupervised Multitask Learners”.
In: (2019)
29
T. B. Brown et al. “Language Models
are Few-Shot Learners”. In: Advances
in Neural Information Processing Systems.
2020, pp. 1877–1901
28

A. Radford et al. “Learning Transferable Visual Models From Natural Language Supervision”. In: Proceedings of
the 38th International Conference on Machine Learning. 2021, pp. 8748–8763
30

J. Ho et al. “Imagen Video: High
Definition Video Generation with Diffusion Models”.
In: arXiv preprint
arXiv:2210.02303 (2022)
32
A. Rives et al. “Biological structure and
function emerge from scaling unsupervised learning to 250 million protein sequences”. In: Proceedings of the National
Academy of Sciences 118.15 (2021)
31

B. Zitkovich et al. “RT-2: VisionLanguage-Action Models Transfer Web
Knowledge to Robotic Control”. In: Proceedings of The 7th Conference on Robot
Learning. 2023, pp. 2165–2183
33

K. Black et al. “
pi0: A Vision-Language-Action Flow
Model for General Robot Control”. In:
(2024)
35
M. J. Kim et al. “OpenVLA: An OpenSource Vision-Language-Action Model”.
In: Proceedings of The 8th Conference on
Robot Learning. 2025, pp. 2679–2713
34

---

### [PDF p.517 | Book p.515]

prospects

data and subsequently fine-tuned on robotic interaction data, these models aim
to combine broad semantic understanding with embodied control.
A closely related development is the emergence of reasoning models within embodied systems 36 37 38 . Beyond mapping observations directly to actions, these
architectures allocate explicit computation to intermediate deliberation, generating structured reasoning traces—often in natural language—that attempt to
make causal relationships, counterfactuals, and task constraints explicit before
committing to specific actions. Inspired by advances in large language models
where inference-time reasoning improves robustness and accuracy, reasoningenabled robotic systems treat deliberation itself as a tunable resource, where more
complex or safety-critical situations can trigger deeper chains of thought, selfreflection, or verification steps. In embodied contexts, however, reasoning cannot
remain purely textual. It must be grounded in geometry, dynamics, and physical feasibility, and must remain consistent with the actions ultimately executed.
The central challenge, therefore, is not merely to produce articulate explanations,
but to ensure alignment between internal rationale and external behavior, so that
reasoning becomes a functional component of autonomy rather than a post-hoc
narrative.

515

W. Huang et al. “Inner Monologue:
Embodied Reasoning through Planning
with Language Models”. In: Proceedings
of The 6th Conference on Robot Learning.
2023, pp. 1769–1782
36

NVIDIA. “Alpamayo-R1: Bridging
Reasoning and Action Prediction for
Generalizable Autonomous Driving in
the Long Tail”.
In: arXiv preprint
arXiv:2511.00088 (2025)
38
M. Zawalski et al. “Robotic Control
via Embodied Chain-of-Thought Reasoning”. In: Proceedings of The 8th Conference on Robot Learning. 2024
37

World models. Another especially important instantiation of the foundation
model paradigm for robotics is the development of world models. Broadly speaking, world models aim to capture how the world evolves over time, including its
39
physical, spatial, and visual dynamics 39 40 . Unlike traditional dynamics models,
D.
Ha
and
J.
Schmidhuber.
“World
Models”.
In:
arXiv
preprint
which operate on carefully designed state representations, modern world modarXiv:1803.10122 (2018)
els are learned directly from rich, high-dimensional inputs such as images, video,
40
NVIDIA. “Cosmos World Foundation Model Platform for Physical AI”. in:
depth, and other multimodal signals. This allows them to model complex aspects
arXiv preprint arXiv:2501.03575 (2025)
of real-world environments—such as object persistence, scene geometry, contact
interactions, and temporal visual change—that are difficult to specify analytically
but are essential for robust autonomy.
This richer predictive interface is particularly valuable in robotics, where data
is a fundamental bottleneck. Robot interaction data is expensive to collect, embodimentspecific, and limited in scale. In contrast, visual data—especially video—is abundant and diverse. World models provide a pathway for leveraging this disparity
by learning general physical and semantic structure from large-scale, largely passive observations. In doing so, they enable a partial decoupling between world
understanding and control, allowing robots to acquire broad knowledge about how
environments behave without requiring equivalent amounts of task-specific interaction data.
At a high level, world models equip robots with the ability to predict and imagine. Given a current situation and, potentially, a proposed action sequence, a
world model can forecast how the environment and the robot within it may
evolve. This enables planning through the evaluation of imagined futures, where
a robot may compare alternative outcomes, select actions that lead toward desirable states, or optimize behavior by reasoning directly over predicted trajectories.
A second major advantage is that world models can support the generation of

---

### [PDF p.518 | Book p.516]

516

principles of robot autonomy

realistic synthetic data. Because they model visual, spatial, and physical regularities, world models can be used to synthesize new scenarios, including rare edge
cases or safety-critical situations that are difficult to collect in practice. In this
way, world models can augment traditional simulation, providing a data-driven
substrate for training and evaluating autonomous systems in a broader range of
conditions, while maintaining high visual fidelity.
The precise form that such world models should take remains an open research question. Some approaches focus on predicting high-dimensional sensory observations such as future video frames conditioned on actions 41 . Others
learn compact latent representations of the environment and predict future states
within this lower-dimensional space rather than at the raw pixel level 42 . Additional work explores structured representations that encode objects, physical
interactions, or causal relationships in an effort to improve generalization and
data efficiency 43 .
Taken together, while the integration of foundation models into robotics remains
an active and rapidly evolving area of research, recent developments suggest
that they may fundamentally reshape how autonomous systems are designed,
developed, and operated. Rather than building task-specific autonomy stacks
from scratch, future robots may increasingly rely on large pretrained models as
adaptable cores, as well as key enablers across the entire autonomy development
pipeline.
In this sense, foundation models are not merely new building blocks within
the autonomy stack, but are beginning to redefine the abstractions and workflows
used to construct it.
Simulation and Closing the Gap to Reality. In parallel, progress in simulation has
accelerated dramatically, expanding both its fidelity and its role within the autonomy development pipeline. Advances in physics-based engines, high-fidelity rendering, differentiable simulators, and large-scale synthetic data generation now
enable training and evaluation in increasingly realistic environments 44 . At the
same time, the emergence of generative simulation has begun to complement
traditional simulators by producing realistic, diverse, and often open-ended scenarios directly from data.
Simulation has long been an essential tool in robotics, but it is increasingly
becoming a central substrate for large-scale training, evaluation, and red-teaming
of autonomous systems.
Physical AI Safety. As autonomy stacks incorporate more data-driven components, the question of safety becomes increasingly critical. Data-driven models
can hallucinate, extrapolate poorly outside their training distribution, or produce
internally inconsistent reasoning traces. In physical systems, such failures carry
real-world consequences.
Physical AI safety is therefore becoming a central topic. This includes research
on detecting and mitigating failure modes of data-driven models, developing ro-

Google DeepMind. Genie 3: A New
Frontier for World Models. Research blog.
2025. url: https://deepmind.google/
41

blog / genie - 3 - a - new - frontier - for world-models/

M. Assran et al. “V-JEPA 2: SelfSupervised Video Models Enable Understanding, Prediction and Planning”. In:
arXiv preprint arXiv:2506.09985 (2025)
42

F. Locatello et al. “Object-Centric
Learning with Slot Attention”. In: Advances in Neural Information Processing
Systems 33. 2020, pp. 11525–11538
43

V. Makoviychuk et al. “Isaac Gym:
High Performance GPU Based Physics
Simulation For Robot Learning”. In: Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks. 2021
44

---

### [PDF p.519 | Book p.517]

prospects

bust training and evaluation protocols, and combining data-driven learning with
traditional control-theoretic safety guarantees 45 46 47 48 . At the systems level,
emerging frameworks such as NVIDIA’s Halos platform aim to provide end-toend safety validation pipelines for autonomous systems, integrating simulation,
scenario generation, and formal evaluation to stress-test models under diverse
and safety-critical conditions 49 . Such efforts highlight the growing recognition
that safety must be addressed holistically, spanning model design, data curation,
evaluation, and deployment.

517

R. Sinha et al. “Real-Time Anomaly
Detection and Reactive Planning with
Large Language Models”. In: Proceedings of Robotics: Science and Systems. 2024
45

S. Sagawa et al. “Distributionally Robust Neural Networks for Group Shifts:
On the Importance of Regularization for
Worst-Case Generalization”. In: Proceedings of the International Conference on
Learning Representations. 2020
46

J. Hoffman et al. “CyCADA: CycleConsistent Adversarial Domain Adaptation”. In: Proceedings of the 35th International Conference on Machine Learning.
2018, pp. 1994–2003
47

An Open Frontier
One thing is clear: it is an exciting time to be working in robotics. Autonomous
systems that were once confined to research laboratories are increasingly deployed in real-world environments and embedded within critical infrastructure.
From autonomous vehicles and aerial systems to space robotics and medical platforms, the impact of robotics is expanding rapidly.
With this book, our aim has been twofold. First, to provide the reader with the
mathematical and algorithmic foundations that underpin modern robot autonomy, so that they can understand the core principles and techniques that enable
robots to perceive, plan, and act in complex environments. Second, to cultivate
a systems-level perspective, so that the reader may understand not only individual algorithms, but how they interconnect and compose into complete autonomy
stacks. The future of robotics will not be built by isolated techniques, but by
thoughtful integration. It will be shaped by engineers and researchers who understand both theory and systems, both abstraction and embodiment. The tools
are evolving rapidly, but the underlying principles will remain enduring guides.
The next chapter of robot autonomy will be written by those who are willing to
build, and we hope this book has given the reader the foundation to do just that.

A. Taylor et al. “Learning for SafetyCritical Control with Control Barrier
Functions”. In: Learning for Dynamics and
Control. 2020, pp. 708–717
48

NVIDIA. NVIDIA Halos: Autonomous
Vehicle Safety. 2024. url: https://www.
49

nvidia.com/en- us/ai- trust- center/
halos/autonomous-vehicles/

---

### [PDF p.520 | Book p.518]

> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]
