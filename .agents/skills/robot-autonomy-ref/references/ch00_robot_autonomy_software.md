# Robot Autonomy Software — Nguyên lý phần mềm & ROS

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Nền tảng
- **Trang sách:** 15–22 | **Trang PDF:** 17–24
- **Độ ưu tiên cho dự án:** `CỐT LÕI`
- **Tóm tắt:** Nguyên lý kiến trúc phần mềm robot, ROS nodes/topics/services/actions và tích hợp hệ thống.

---

### [PDF p.17 | Book p.15]

Robot Autonomy Software

Modern autonomous robots are built as collections of interacting software components that perceive the environment, reason about goals, and execute actions in
real time. As discussed in the Preface, autonomy is not defined by any single algorithm, but by the integration of many components across the See–Think–Act cycle.
Turning that conceptual paradigm into a functioning robotic system requires a
practical software substrate through which sensing, estimation, planning, and
control modules can communicate and operate together. These components must
operate concurrently, exchange information reliably, and adapt to changing conditions, all while meeting real-world constraints on timing, safety, and robustness.
Coordinating such systems is as much a software challenge as it is an algorithmic
or mechanical one.
In practice, most contemporary robotic systems are developed on top of a
shared software infrastructure that helps manage this complexity. In this brief
note, we provide a high-level overview of the Robot Operating System (ROS)1 , 2 ,
which has emerged as the de facto standard software framework for robotics
research, education, and many industrial applications. Despite its name, ROS
is not an operating system in the traditional sense. Rather, it is a middleware
framework: a collection of tools, libraries, and design conventions that support
modular, distributed robot software development.
ROS is best understood as a common language and ecosystem for robotics
software rather than a fixed or complete solution. It provides abstractions for
communication, data sharing, configuration, and system integration that allow
developers to focus on higher-level autonomy and control algorithms. At the
same time, the robotics software landscape is evolving rapidly, and ROS itself
continues to change, with new versions, extensions, and alternatives appearing
regularly. As such, this chapter is not intended as a comprehensive guide or
tutorial, but rather as an orienting overview of the dominant software paradigms
in modern robotics. Readers are encouraged to view this material as a snapshot of
current practice and to supplement it with the extensive and continually updated
resources available online.

L. Joseph. Robot Operating System (ROS)
for Absolute Beginners: Robotics Programming Made Easy. Apress, 2018
1

M. Quigley, B. Gerkey, and W. D.
Smart. Programming Robots with ROS: A
Practical Introduction to the Robot Operating System. O’Reilly Media, 2015
2

---

### [PDF p.18 | Book p.16]

16

Why Robot Software Is Different
At first glance, robot programming may appear to be a straightforward application of classical software engineering. However, robots impose a unique set of
constraints that distinguish them from most conventional software systems. A
robot must simultaneously interface with numerous hardware devices, process
streaming sensor data, make decisions under uncertainty, and generate real-time
control signals, all while operating in a physical world that is only partially observable and constantly changing.
Unlike many traditional software applications, robot software must coordinate
many heterogeneous components operating concurrently. A single robot may
include cameras, lidars, inertial sensors, encoders, motors, and communication
interfaces, each producing or consuming data at different rates. As a result, robot
software must support:
• Multitasking: autonomous robots inherently require concurrent execution. Multiple sensing, estimation, planning, and control processes must run in parallel,
often at different frequencies, while exchanging data in a timely and reliable
manner.
• Low-level device control: robots must interface directly with a wide variety of
hardware devices using communication protocols such as GPIO, USB, SPI, and
others. This requires being able to support multiple programming languages,
such as C++ and Python.
• High-level object-oriented abstractions: as autonomy stacks grow in size and
complexity, software modularity becomes essential. Encapsulation, inheritance, and code reuse enable developers to build complex robotic systems from
reusable components.
• Community libraries and shared infrastructure: given the breadth of robotics as a
field, it is impractical for every developer to reimplement common algorithms
from scratch. Access to third-party libraries and an active user community
dramatically accelerates development and encourages standardization.
These requirements motivate the need for a software middleware specifically
designed for robotics, one that bridges the gap between hardware-level control
and high-level autonomy algorithms.

A Brief History of ROS
Before the development of ROS, robotics software was largely fragmented. Code
written for one robot or laboratory was often difficult to reuse elsewhere, hindering collaboration and slowing progress across the field. In 2007, early versions
of ROS emerged from the Stanford AI Robot (STAIR) project, motivated by the
vision of a free and open-source robotics framework that would promote collaboration, reuse, and rapid experimentation.

---

### [PDF p.19 | Book p.17]

17

This vision was further realized when the startup company Willow Garage,
led by Scott Hassan, assumed stewardship of the project. Under this guidance,
ROS evolved into a standardized development platform featuring a rich set of
tools, libraries, and conventions. The release of ROS 0.4 in 2009 coincided with
the deployment of the PR2 mobile manipulation robot (Figure 3), several units
of which were distributed to universities to catalyze collaborative development.
ROS 1.0 followed in 2010.
Oversight of ROS transitioned in 2012 to the Open Source Robotics Foundation
(OSRF), supporting its development, distribution, and adoption. The first longterm support release, ROS Indigo Igloo, appeared in 2014. In 2017, OSRF was
rebranded as Open Robotics, reflecting its broader mission of supporting opensource robotics software beyond ROS itself. Today, ROS is widely regarded as the
closest thing to an industry standard for robot software, underpinning systems
ranging from research prototypes to commercial autonomous platforms.
As robotics applications expanded beyond research settings into safety-critical
and real-time domains, important limitations of ROS 1 became apparent. In particular, ROS 1 was not designed with real-time guarantees, deterministic communication, or multi-robot deployments over unreliable networks as first-class
concerns. These challenges motivated the development of ROS 2, a major architectural redesign that builds on modern middleware standards such as the Data
Distribution Service (DDS).
ROS 2 introduces native support for real-time communication, improved security, better handling of distributed and multi-robot systems, and more explicit
control over quality-of-service parameters. As such, ROS 2 reflects the evolving needs of the robotics community and is increasingly adopted in applications
where reliability, scalability, and real-time performance are critical.

Design Philosophy of ROS
The architectural choices embodied in ROS reflect a deliberate set of design
goals shaped by the practical realities of building large-scale robotic systems.
Rather than attempting to provide a monolithic, all-encompassing framework,
ROS adopts a minimalist philosophy that emphasizes flexibility, reuse, and composability. ROS’ philosophy can be summarized in the following main principles:
Peer-to-peer. At its core, ROS is designed around a peer-to-peer communication
model. Computation is distributed across multiple processes, potentially running
on different machines, which discover and connect to one another dynamically at
runtime. This approach avoids centralized bottlenecks and allows robotic systems
to scale naturally across heterogeneous computing resources, such as embedded
controllers, edge devices, and cloud servers.
Multi-language. Another key design principle is language neutrality. Robotic systems often benefit from combining high-performance compiled code for time-

Figure 3: The PR2 robot, one of
the first platforms to be widely
supported by ROS.

---

### [PDF p.20 | Book p.18]

18

critical components with higher-level scripting languages for rapid development
and experimentation. ROS supports this hybrid approach by defining communication interfaces independently of any specific programming language, allowing
components written in different languages to interoperate seamlessly.
Tools-based. ROS is also explicitly tools-based. Instead of embedding all functionality within a single runtime environment, ROS provides a collection of commandline tools and graphical utilities for tasks such as launching systems, inspecting
communication graphs, logging data, replaying experiments, and visualizing internal state. This modular tooling approach simplifies debugging and experimentation, enabling developers to inspect and modify a running system without
recompilation or redeployment.
Thin. Finally, ROS is intentionally thin. The middleware itself provides communication, configuration, and coordination mechanisms, but encourages core
algorithms and device drivers to be implemented as standalone libraries with
minimal dependence on ROS-specific infrastructure. This separation improves
testability, promotes code reuse outside of ROS, and reduces long-term maintenance costs as software systems evolve.
Free and open-source. ROS is released under the BSD license, which allows nearly
unrestricted use, modification, and distribution, making it freely available for
both academic and commercial use. As such, ROS has fostered a vibrant ecosystem of users and contributors who share code, documentation, and best practices.
Taken together, these principles position ROS not as a rigid framework, but
as an enabling substrate upon which diverse robotic architectures can be constructed.

Core ROS Concepts
To reason effectively about ROS-based systems, it is helpful to understand a set
of foundational abstractions that recur throughout the ecosystem.
Nodes. A node is a single executable process that performs computation. Nodes
are intended to be lightweight and focused, each responsible for a well-defined
function. For example, a mobile robot might have separate nodes for processing
camera images, fusing sensor data into a state estimate, generating motion plans,
and sending commands to the motors. A complete robotic system typically consists of many nodes executing concurrently.
Messages and Topics. Nodes communicate by exchanging messages, which are
data structures defined by user-specified types. Messages are transmitted over
named topics using a publisher and subscriber model, shown schematically in

---

### [PDF p.21 | Book p.19]

19

Publisher

Subscriber
Message

Message

Node C

Node A

Publisher

Subscriber
Message

Message
Node B

Node D

Perception

Navigation

Vehicle Interface

Lidar

Localization

Task
Planning

Steering Control

Radar

Obstacle
Detection

Path Planning

Throttle/Brake
Control

GPS & IMU

Pose Estimation

Sensor Interface

Figure 4:
Publish/Subscribe
Communication Model in ROS.
Topics are best used for unidirectional streaming communication, where a publisher continuously sends messages to one or
more subscribers.

Wheel Encoder

User Interface (UI)
Global Services
Emergency Stop
Vehicle Health State
Graphical UI
Data Logger

Figure 4. A node that produces data publishes messages to a topic, while any
number of other nodes may subscribe to that topic to receive the data. Publishers
and subscribers are decoupled, meaning that they do not need to be aware of
each other’s existence or lifecycle, only the topic name and message type. This
communication pattern naturally supports streaming data flows, such as sensor
measurements, state estimates, and control commands, and enables flexible oneto-many and many-to-many information sharing.

Services. In addition to asynchronous message passing, ROS also supports synchronous request-response interactions through services. A service defines a pair
of message types, one for the request and one for the response. Nodes can advertise services that other nodes can call, allowing for more structured interactions
such as parameter queries, configuration changes, or one-off computations. For
example, a node might request an updated map, or portion of a map, from a
mapping node.

Figure 5: Example structure of
a mobile robot software framework in ROS. Each white box
represents a package that contains multiple nodes (red boxes)
responsible for specific functionality. The arrows indicate communication pathways between
different packages.

---

### [PDF p.22 | Book p.20]

20

Packages. A package is a directory that contains related ROS nodes, libraries,
datasets, configuration files, and any other resources needed to build and run a
particular piece of functionality. Packages are the primary unit of code organization and distribution in ROS, and can be shared and reused across different
projects and robots. An example of this modular structure is illustrated in Figure 5. By separating functionality into well-defined components, ROS enables
scalable development, testing, and maintenance of complex robotic systems.

Software as the Glue of Autonomy
While the algorithms presented in this book form the intellectual core of robot
autonomy, their practical realization depends critically on software infrastructure. In real robotic systems, autonomy is not executed as a single loop but as a
distributed graph of asynchronously updating components operating at different
rates and exchanging information continuously. Throughout this text, we focus
on the core algorithms and their mathematical foundations, but it is important
to recognize that software engineering is the glue that holds these components
together in a functioning system.

---

### [PDF p.23 | Book p.21]

21

References
[58]

L. Joseph. Robot Operating System (ROS) for Absolute Beginners: Robotics
Programming Made Easy. Apress, 2018.

[114]

M. Quigley, B. Gerkey, and W. D. Smart. Programming Robots with ROS: A
Practical Introduction to the Robot Operating System. O’Reilly Media, 2015.

---

### [PDF p.24 | Book p.22]

> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]
