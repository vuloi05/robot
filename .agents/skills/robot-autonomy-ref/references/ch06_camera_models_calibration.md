# Ch 6: Camera Models and Calibration

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Part II: Robot Perception
- **Trang sách:** 171–192 | **Trang PDF:** 173–194
- **Độ ưu tiên cho dự án:** `CỐT LÕI`
- **Tóm tắt:** Mô hình camera lỗ kim, phép chiếu phối cảnh, chuyển đổi tọa độ và hiệu chuẩn camera (nội/ngoại tham) cho AprilTag.

---

### [PDF p.173 | Book p.171]

6
Camera Models and Calibration
While the previous chapter surveyed various sensor types used in robotics, vision sensors warrant special attention due to their unique ability to capture rich,
high-dimensional information about the environment. A single camera image
can contain information about object identity, pose, color, texture, and spatial
relationships—information that would require multiple specialized sensors to
obtain otherwise. However, extracting useful information from camera images
requires understanding how three-dimensional scenes are projected onto twodimensional image planes, and how we can calibrate cameras to enable accurate
measurements.
This chapter explores the mathematical foundations of camera models, from
the basic pinhole model to modern RGB-D sensors, and presents practical methods for camera calibration that enable quantitative vision-based perception. In
Section 6.1 we introduce the principles of image formation and the mathematical
models that describe how cameras capture images. Next, in Section 6.2, we derive
the perspective projection equations and discuss practical considerations such as
lens distortion. Then, we will discuss an increasingly popular type of camera,
RGB-D cameras, in Section 6.3, which provide both color and depth information.
Finally, in Section 6.4 and Section 6.5, we derive the mathematical model for perspective projection and present methods for camera calibration, which is essential
for using these models in practice.

6.1

Digital Cameras and Image Formation

Modern cameras consist of a sensor that captures light and converts the resulting
signal into a digital image. Light falling on an imaging sensor is usually picked
up by an active sensing area, integrated for the duration of the exposure1 , and
then passed to a set of sense amplifiers.

6.1.1

Image Sensors

The two main kinds of sensors used in digital cameras today are charge-coupled
devices (CCD) and complementary metal-oxide-semiconductor (CMOS) sensors.

The duration of exposure is usually expressed as the shutter speed, such as
1/125, 1/60, or 1/30 of a second.
1

---

### [PDF p.174 | Book p.172]

172

principles of robot autonomy

A CCD chip is an array of light-sensitive picture elements called pixels, and can
contain between 20,000 and several million pixels total. We can think of each
pixel as a light-sensitive discharging capacitor that is 5 to 25µm in size. While
complementary metal oxide semiconductor (CMOS) chips also consist of an array of pixels, they are quite different from CCD chips. In particular, along the
side of each pixel are several transistors specific to that pixel. CCD sensors have
typically outperformed CMOS for quality-sensitive applications such as digital
single-lens-reflex cameras, while CMOS sensors are better for low-power applications. However, today, CMOS sensors are standard in most digital cameras.

6.1.2

Image Formation

Rays of light reflected by an object tend to be scattered in many directions and
may consist of different wavelengths. Averaged over time, the emitted wavelengths and directions for a specific object can be precisely described using objectspecific probability distribution functions. In particular, the light reflection properties of a given object are the result of how light is reflected, scattered, or absorbed based on the object’s surface properties and the wavelength of the light.
For example, an object might look blue because blue wavelengths of light are
primarily scattered off the surface while other wavelengths are absorbed.
Cameras capture images by sensing reflected light rays on a photoreceptive
surface such as a CCD or a CMOS sensor. Since light reflecting off an object is
generally scattered in many directions, exposing a planar photoreceptive surface
to these reflected rays would result in many rays being captured at each pixel,
which would lead to blurry images. A solution to this issue is to add a barrier in
front of the photoreceptive surface that only lets some of the rays pass through an
aperture, as we show in Section 6.1.2. The earliest approach to filtering light rays
in this way was to have a small hole in the barrier surface. We refer to cameras
with this type of filter as pinhole cameras.

6.2

Camera Models

6.2.1

Pinhole Camera Model

A pinhole camera has no lens but rather a single small aperture. Light from the
scene passes through this pinhole aperture and projects an inverted image onto

Figure 6.1: Light rays on a photoreceptive surface, referred to
as the image plane. On the left,
numerous rays being reflected
and scattered by the object leads
to blurry images whereas, on the
right, a barrier has been added
so that the scattered light rays
can be distinguished.

---

### [PDF p.175 | Book p.173]

camera models and calibration

173

the image plane, as we show in Section 6.2.1. While modern cameras do not
operate in this way, we can use the principles of the pinhole camera to derive
useful mathematical models.
Figure 6.2:
Pinhole camera
model. Due to the geometry of
the pinhole camera system, the
object’s image is inverted on the
image plane. In this figure, O
is the camera center, c is the image center, and p is the principal
point.

We start by defining several useful references to help develop the mathematical
pinhole camera model. First, the camera reference frame is centered at a point, O,
that is at a focal length, f , in front of the image plane, as we show in Section 6.2.1.
We define this reference frame, with directions (i, j, k ), such that the k axis is
coincident with the optical axis that points toward the image plane. We denote
the coordinates of a point in the camera frame by P = ( X, Y, Z ). When a ray of
light is emitted from a point, P, and passes through the pinhole at point O, it
gets captured on the image plane at a point p. Since these points are all collinear,
we can deduce the following relationships between the coordinates P = ( X, Y, Z )
and p = ( x, y, z):
x = λX, y = λY, z = λZ,
for some λ ∈ R. This leads to the relationship:
λ=

x
y
z
= = .
X
Y
Z

From the geometry of the camera, we can see that z = f where f is the focal
length, such that we can rewrite these expressions as:
x= f

X
,
Z

y= f

Y
.
Z

(6.1)

Therefore, we can compute the position of the pixel on the image plane that
captures a ray of light from the point P.

6.2.2

Thin Lens Model

One of the main issues with having a fixed pinhole aperture is that there is a
trade-off associated with the aperture’s size. A large aperture allows a greater
number of light rays to pass through, which leads to image blurring. A small

---

### [PDF p.176 | Book p.174]

174

principles of robot autonomy

aperture lets through fewer light rays, but the resulting image is darker. As a
solution, lenses focus light by refraction and can be used to replace the aperture,
avoiding the need for these trade-offs.
We can develop a mathematical model for lenses similar to the pinhole model
by using properties from Snell’s law. Section 6.2.2 shows a diagram of the most
basic lens model, which is the thin lens model2 . Snell’s law states that rays passing
through the center of the lens are not refracted, and those that are parallel to the
optical axis are focused on the focal point, labeled F ′ . In addition, all rays passing
through P are focused by the thin lens on the point p. We develop a mathematical
model similar to Equation (6.1) from the geometry of similar triangles:
y
z
= ,
Y
Z

y
z− f
z
=
= − 1,
Y
f
f

The thin lens model assumes no optical
distortion due to the curvature of the
lens.
2

(6.2)

where again the point P has coordinates ( X, Y, Z ), its corresponding point, p, on
the image plane has coordinates ( x, y, z), and f is the focal length. Combining
these two equations yields the thin lens equation:
1
1
1
+ = .
z
Z
f

(6.3)

Note that in this model, and for a particular focal length, f , a point, P, is only in
sharp focus if the image plane is located a distance z from the lens. In practice, an
acceptable focus is possible within some range of distances referred to as depth of
field or depth of focus. Additionally, if Z approaches infinity, light would focus a
distance of f away from the lens. Therefore, this model is essentially the same as
a pinhole model if the lens is focused at a distance of infinity.

Figure 6.3: The thin lens model.

6.2.3

Radial Distortion

The pinhole camera model provides a nominal camera model for which it is
relatively straightforward to develop a mathematical model of the perspective
projection. However, in practice, this model is not a perfect representation of the
imaging process. One effect that is not captured by the pinhole model is radial
distortion, which is an effect seen in real lenses where either barrel distortion or

---

### [PDF p.177 | Book p.175]

camera models and calibration

175

pincushion distortion will affect the real pixel coordinates. We show images of
barrel and pincushion distortion in Section 6.2.3.

Figure 6.4: Different kinds of radial distortions that are seen in
real lenses, which may affect the
accuracy of the pinhole camera
model.

There are methods we can use to correct for image distortion. A simple and
efficient way is to model the relationship between the ideal pixel coordinates,
(u, v), and the distorted pixel coordinates, (ud , vd ), as:
# " #
"
" #
u
u − ucd
ud
2
(6.4)
+ cd ,
= (1 + kr )
vcd
v − vcd
vd
where k ∈ R is the radial distortion factor, (ucd , vcd ) are the pixel coordinates of
the image center, and r2 = (u − ucd )2 + (v − vcd )2 is the square of the distance
between the ideal pixel location and the center of distortion. Note that k differs
across cameras and needs to be predetermined through calibration.

6.3

RGB-D Cameras

While traditional cameras capture color information through RGB channels, RGBD cameras additionally provide depth information for each pixel, creating a 2.5D
representation of the scene. These sensors have become increasingly important in
robotics due to their ability to provide both appearance and geometric information in a single, compact package.

6.3.1

Depth Sensing Technologies

RGB-D cameras employ various technologies to capture depth information alongside color:
Structured light. These sensors project a known infrared pattern onto the scene
and use triangulation to compute depth from the pattern’s deformation. The
original Microsoft Kinect exemplifies this approach, projecting a speckle pattern
that is captured by an IR camera offset from the projector. Structured light sensors
provide high accuracy at close range (0.5 to 4 m) but struggle in bright ambient
light conditions.

---

### [PDF p.178 | Book p.176]

176

principles of robot autonomy

Time-of-flight (ToF). ToF cameras emit modulated infrared light and measure the
phase shift of the reflected signal to determine distance. These sensors offer good
accuracy across their operating range and work well in varying lighting conditions, though they typically have lower resolution than structured light sensors
and can suffer from multipath interference.
Stereo infrared. Some RGB-D cameras, such as the Intel RealSense D-series, use
stereo vision with infrared cameras and an optional IR pattern projector. This
approach combines the robustness of stereo vision with active illumination to
handle textureless surfaces.

6.3.2

Applications in Robotics and Practical Considerations

RGB-D cameras have enabled significant advances in several robotics applications, particularly in structured indoor environments. For indoor navigation and
mapping, RGB-D sensors are ideal when GPS is unavailable and lighting can be
controlled. They provide dense 3D point clouds at frame rate, enabling real-time
obstacle avoidance and map building, with popular SLAM systems like RGB-D
SLAM and ElasticFusion leveraging these sensors for creating detailed 3D maps.
In object manipulation tasks, RGB-D cameras excel by providing both the object’s
appearance and its precise 3D geometry, allowing robots to identify objects using
color and texture while planning grasps based on accurate depth information.
The relatively high accuracy at close range (typically 0.5 to 4 m) makes them
well-suited for tabletop manipulation and pick-and-place operations.
However, several practical considerations limit their use. Most consumer RGBD sensors operate effectively only between 0.5 and 5 meters, with accuracy degrading quadratically with distance—millimeter accuracy at one meter may degrade to several centimeters at maximum range. Material properties significantly
affect performance: transparent and highly reflective surfaces cannot be measured, while dark materials may return weak signals leading to missing depth
values. RGB-D cameras also require careful calibration between the color and
depth sensors, which are typically offset from each other, and factory calibration may not suffice for high-precision applications. Additionally, multiple RGBD cameras can interfere with each other’s IR projectors, and ambient infrared
light (such as sunlight) makes outdoor use challenging. Despite these limitations,
RGB-D cameras offer an attractive balance of cost, size, and capability for many
indoor robotics applications, providing rich 3D perception without the computational complexity of stereo matching or the cost of laser scanners.

6.4

Perspective Projection and Coordinate Transformations

The pinhole camera model can be used to mathematically define relationships
between points in the scene and points on the image plane. Our objective is to
derive a mathematical model that maps a point PW expressed in world frame

---

### [PDF p.179 | Book p.177]

camera models and calibration

177

coordinates to a point p on the image plane in pixel coordinates. We accomplish
this by combining two transformations: from world frame to camera frame coordinates (PW → PC ), and from camera coordinates to image coordinates (PC → p).

6.4.1

Camera Frame to Image Coordinates (PC → p)

The first step we consider is how to map a point in the scene expressed in camera
frame coordinates, PC , to the corresponding point on the image plane, p, using the
pinhole camera model. In Section 6.2, we presented the pinhole camera equations:
x= f

XC
,
ZC

y= f

YC
,
ZC

(6.5)

where PC = ( XC , YC , ZC ), p = ( x, y), and f is the focal length of the pinhole
camera3 .
Note that the quantities x and y are coordinates in the camera frame, but it is
often desirable to express the point p in terms of pixel coordinates. Pixel coordinates are generally defined with respect to a reference frame in the lower corner
of the image plane to avoid negative coordinates. We show this new reference
frame in Section 6.4.1, where we define the image center, c, with coordinates
˜ is the notation we use to denote a coordinate with respect to
( x̃0 , ỹ0 ), where (·)
this new reference frame. In this new reference frame, we map the point PC to

We generally do not include the z term
of p simply because z = f is a fixed
value.
3

Figure 6.5: We define a new reference frame with coordinates
˜ with its origin
denoted by (·)
in the lower corner of the image plane. The image center coordinates in this new frame are
( x̃0 , ỹ0 ).

the coordinates ( x̃, ỹ) by:
x̃ = f

XC
+ x̃0 ,
ZC

ỹ = f

YC
+ ỹ0 .
ZC

(6.6)

Finally, given the number of pixels per unit distance, we can map these new
coordinates to pixel coordinates. In particular, we map the point PC to pixel
coordinates (u, v) by:
u=α

XC
+ u0 ,
ZC

v=β

YC
+ v0 ,
ZC

(6.7)

where α = k x f , u0 = k x x̃0 , β = k y f , v0 = k y ỹ0 , and k x and k y are the number of
pixels per unit distance in image coordinates.

---

### [PDF p.180 | Book p.178]

178

principles of robot autonomy

Note that the transformation from the point PC in camera frame coordinates
to p in pixel coordinates given by Equation (6.7) is not linear. However, we can
represent this transformation as a linear mapping4 through an additional change
of coordinates. In particular, we will express the points PC and p in homogeneous
coordinates.
For a two-dimensional point ( x1 , x2 ) or a three-dimensional point ( x1 , x2 , x3 )
in Euclidean space, we represent the point in homogeneous coordinates by the
transformation:

( x1 , x2 ) → (αx1 , αx2 , α) ,

and

( x1 , x2 , x3 ) → (αx1 , αx2 , αx3 , α) ,

Expressing the perspective projection
as a linear map will simplify the mathematics later on.
4

(6.8)

for any α ̸= 0. These new coordinates are called homogeneous coordinates because we can choose the scaling factor, α, arbitrarily as long as α ̸= 0. We transform a set of homogeneous coordinates back by:




y1 y2
y1 y2 y3
,
, and (y1 , y2 , y3 , y4 ) →
,
,
.
(6.9)
( y1 , y2 , y3 ) →
y3 y3
y4 y4 y4
We will denote when a point is described in homogeneous coordinates using the
superscript h. For example, we express the point PC = ( XC , YC , ZC ) in camera
frame coordinates with α = 1 in homogeneous coordinates by:
PCh = ( XC , YC , ZC , 1) ,
and we can express the pixel coordinate p = (u, v) in homogeneous coordinates
by:
ph = ( ZC u, ZC v, ZC ) = (αXC + u0 ZC , βYC + v0 ZC , ZC ) ,
by choosing α = ZC and substituting the expressions from Equation (6.7). With
the expression of these points in homogeneous coordinates, we can see that their
relationship is transformed from the nonlinear relationship in Equation (6.7) to
the linear relationship:
 
 Xc



αXc + u0 Zc
α 0 u0 0  
  Yc  


(6.10)
 0 β v0 0   =  βYc + v0 Zc  .
 Zc 
0 0 1 0
Zc
1
Often, in practice, we also add a skewness parameter, γ5 , and we can write
this linear relationship in the more compact form:


α γ u0
h
i


(6.11)
K 03×1 PCh = ph , K :=  0 β v0  .
0 0 1
We refer the matrix K in Equation (6.11) as the camera matrix or matrix of intrinsic
parameters because it contains the five parameters that define the fundamental
characteristics of the camera from the perspective of the pinhole camera model.
While these parameters may be specified by the camera manufacturer, we often
estimate them in practice by performing a camera calibration.

The skewness parameter generally
ends up being close to zero.
5

---

### [PDF p.181 | Book p.179]

camera models and calibration

6.4.2

179

World Frame to Camera Frame (PW → PC )

We can express a point, P, in the scene (see Section 6.2.1) either in terms of camera
frame coordinates, PC , or world frame coordinates, PW . While we discussed the
use of the pinhole model to map PC coordinates to pixel coordinates, p, in the
previous section, in this section we discuss the mapping between the camera and
world frame coordinates of the point P, as we show in Section 6.4.2.

Figure 6.6: A depiction of the
point P expressed either in camera coordinates, PC , or in world
frame coordinates, PW . We denote the world frame origin by
OW and the camera frame origin
by OC .

From Section 6.4.2, we can write PC as:
PC = t + q,

(6.12)

where t is the vector from OC to OW , expressed in camera frame coordinates, and
q is the vector from OW to P, expressed in camera frame coordinates. However,
the vector q is the same vector as PW , just expressed with respect to a different
coordinate frame. The coordinates are related by a rotation:
q = RPW ,

(6.13)

where R is the rotation matrix relating the camera frame to world frame defined
as:


iw · i jw · i k w · i


(6.14)
R :=  iw · j jw · j k w · j  ,
iw · k jw · k k w · k
where i, j, and k are the unit vectors that define the camera frame and iw , jw , and
k w are the unit vectors that define the world frame. To summarize, we can map
the point PW to camera frame coordinates PC by:
PC = t + RPW ,

(6.15)

where t is the vector in camera frame coordinates from OC to OW and R is the
rotation matrix defined in Equation (6.14). Similar to the previous section, we can

---

### [PDF p.182 | Book p.180]

180

principles of robot autonomy

equivalently express this transformation for the case where the points PW and PC
are expressed in homogeneous coordinates:
" # "
#" #
PC
R
t PW
.
(6.16)
=
1
01×3 1
1

6.4.3

Complete Projection Pipeline (PW → p)

The objective of the perspective projection task is to find a way to mathematically
relate the position of a point in world frame coordinates, denoted PW , to the
corresponding pixel coordinates, p, on the image plane. With the relationship
from Equation (6.16) that we developed for mapping PW to the camera frame
coordinates, PC , and the relationship in Equation (6.11) for mapping PC to pixel
coordinates, p, we can now define the direct mapping from PW to p. In particular,
combining the two transformations together yields:
"
#
h
i R
t
h
p = K 03×1
Ph ,
01×3
1 W
which we can simplify to:
h
ph = K R

i
h
.
t PW

(6.17)

h is the homogeneous coordinate representation of P and
In Equation (6.17), PW
W
h
p is the homogeneous coordinate representation of p. Recall that the matrix K ∈
R3×3 is the matrix of intrinsic camera parameters, and the matrix [ R t] ∈ R3×4
contains extrinsic parameters6 . Note that the total number of degrees of freedom
is 11, where 5 are from the intrinsic parameters that define K, 3 are from the
rotation matrix, R, and 3 are from the position vector, t.

6.5

Camera Calibration

Before we can use camera models in practice, we need to determine the camera’s
intrinsic and extrinsic parameters. Camera calibration is the process of estimating
these parameters, which is essential for quantitative computer vision applications.
We present two main approaches: the Direct Linear Method for basic calibration,
and auto-calibration for cases where calibration targets are unavailable.

6.5.1

Direct Linear Method

One approach is the direct linear calibration method, which requires a set of known
correspondences, pi ←
→ PW,i for i = 1, . . . , n.
Direct linear calibration: Step 1. For direct linear calibration, the first step is to
write each corresponding pair of points, pi = (ui , vi ) and PW,i = ( XW,i , YW,i , ZW,i ),
in homogeneous coordinates and then use the expression in Equation (6.17) to
write:
h
pih = MPW,i
, i = 1, . . . , n,
(6.18)

Extrinsic parameters describe the camera’s position and orientation relative to
the points in the scene.
6

---

### [PDF p.183 | Book p.181]

camera models and calibration

where we refer to M = K [ R t] as the projection matrix. Next, we use the n correspondences to estimate the projection matrix, M, and then later we can extract
the intrinsic and extrinsic parameters from M. A useful first step to determine M
is to rewrite it in terms of its rows:
 
m1
 
M =  m2  ,
(6.19)
m3
where mi ∈ R1×4 is the i-th row of M. By considering the rows of M individually,
we can write the relationship in Equation (6.18) as:
  

h
m1 · PW,i
αui
  
h ,
i = 1, . . . , n

 αvi  = m2 · PW,i
h
α
m3 · PW,i
which by mapping the homogeneous coordinates, pih , back to the original coordinates, pi , yields the 2n expressions:
ui =
vi =

h
m1 · PW,i
h
m3 · PW,i
h
m2 · PW,i
h
m3 · PW,i

,

i = 1, . . . , n,

,

i = 1, . . . , n,

or equivalently, by some algebraic manipulation, yields the expressions:
h
h
ui (m3 · PW,i
) − (m1 · PW,i
) = 0,

i = 1, . . . , n

h
h
vi (m3 · PW,i
) − (m2 · PW,i
) = 0,

i = 1, . . . , n.

(6.20)

We can now combine these 2n equations together in one large matrix equation:


m1⊤


P̃m = 0, m := m2⊤  ,
(6.21)
m3⊤
where m ∈ R12×1 is a vector consisting of the stacked rows of M and P̃ ∈ R2n×12
h .
is a matrix of known coefficients determined by the quantities ui , vi , and PW,i
For a more concrete representation of how we define P̃, the first couple rows are
given by:


h )⊤
h )⊤
−( PW,1
01×4
u1 ( PW,1
 0
h )⊤ v ( Ph )⊤ 
−( PW,1


1×4
1 W,1

P̃ = −( Ph )⊤
(6.22)
h )⊤ 
.
0
u
(
P
2 W,2
1×4
W,2


..
..
..
.
.
.
Note that we must have at least six correspondences, n ≥ 6, to ensure that m
is uniquely defined. With this sufficient number of correspondences, we could
ideally directly solve Equation (6.21). However, in practice, a more robust procedure is to build P̃ with more than 6 points, which gives an overdetermined set of

181

---

### [PDF p.184 | Book p.182]

182

principles of robot autonomy

equations that may not have a solution7 . Therefore, to compute m, we formulate
an optimization problem:
minimize

∥ P̃m∥2 ,

subject to

∥m∥2 = 1,

m

(6.23)

where the constraint ∥m∥2 = 1 is required to ensure that the optimization problem cannot be solved by trivially choosing mi = 0 for each i = 1, . . . , 12. We call
this optimization problem a constrained least-squares problem.
Example 6.5.1 (Constrained least-squares optimization). The constrained least
squares problem:
minimize

∥ Ax ∥2 ,

subject to

∥ x ∥2 = 1,

x

with x ∈ Rn and A ∈ Rm×n and m > n is a finite-dimensional optimization
problem. Consider the corresponding Lagrangian:
L = x ⊤ A⊤ Ax + λ(1 − x ⊤ x ),
and the necessary optimality conditions:

∇ x L = 2( A⊤ A − λI ) x = 0,
∇λ L = 1 − x ⊤ x = 0.
We can write the first necessary optimality condition as A⊤ Ax = λx, and therefore any x that satisfies this condition must be an eigenvector of the matrix A⊤ A.
Additionally, while all the eigenvectors satisfy this condition, the optimum is the
eigenvector associated with the smallest eigenvalue. We can efficiently compute
this eigenvector by using a singular value decomposition of A = UΣV ⊤ and then
choosing x to be the column of V associated with the smallest singular value,
since A⊤ A = VΣ2 V ⊤ .
Direct linear calibration: Step 2. Once we have solved the optimization problem in
Equation (6.23) to compute the vector m, the projection matrix, M, is completely
defined. The next step in the camera calibration process is to extract the intrinsic
and extrinsic camera parameters from the matrix M. For this step, we will express
the matrix M in terms of its columns:
h
i
M = c1 c2 c3 c4 ,
where ci is the i-th column of M. We can factorize M as:
h
i
M=K R t ,

(6.24)

by taking the first three columns of M and performing a RQ factorization:
h
i
c1 c2 c3 = KR,

(6.25)

where R is an orthogonal matrix and K is an upper triangular matrix. Once K is
known, we can compute the vector t by t = K −1 c4 .

This is particularly true in real-world
applications where noise corrupts the
data.
7

---

### [PDF p.185 | Book p.183]

camera models and calibration

6.5.2

183

A Flexible Camera Calibration Method

The projection matrix, M, is defined for a specific set of extrinsic parameters R
and t. In practice, however, it might be desirable for us to estimate the camera’s intrinsic parameters from N different images from different perspectives,
and therefore with N different projection matrices due to the varying extrinsic
parameters. In this case, we can apply an alternative procedure8 to the direct
linear calibration method to extract the intrinsic parameters, K.
We begin by assuming that the known points, PW , for each individual image
lie on a plane. For example, the calibration scene might consist of a pattern, such
as a checkerboard pattern, on a planar surface. In this case, we can assume that
the world frame origin lies on the plane such that ZW = 0 for all points on the
h given
plane. Since ZW = 0, we can simplify the relationship between ph and PW
by Equation (6.17) to:
h
ph = H P̃W
,

(6.26)

with:
h
H = K r1

r2

i
t ,

h
h
P̃W
= XW

YW

1

i⊤

,

(6.27)

h is the simplified position of the
where H is called the homography matrix9 , P̃W
point P in world frame, written in homogeneous coordinates, and ri is the i-th
column of the rotation matrix, R. Note that we can still estimate the homography
matrix, H, using the same procedure discussed earlier.
Next, we identify a set of constraints on the intrinsic parameter matrix, K, by
writing the homography, H, as:

h
H = Kr1

Kr2

i h
Kt = c̃1

i
c̃3 ,

c̃2

and noting that since r1 and r2 are orthonormal we have:
c̃1⊤ Bc̃2 = 0,

c̃1⊤ Bc̃1 = c̃2⊤ Bc̃2 ,

(6.28)

where B = K −⊤ K −1 ∈ R3×3 is a symmetric matrix. We can therefore solve for
the intrinsic camera parameters, K, by using the constraints in Equation (6.28)
to solve for the symmetric matrix B and then backing out the parameters that
define K. To compute the matrix B from the constraints in Equation (6.28), we
can employ several useful tricks. The main trick is to notice that even though
B consists of nine parameters, it is symmetric, and, therefore, we only need six
parameters to specify it fully. Therefore, we reparameterize the matrix B ∈ R3×3
as a vector b ∈ R6 as:
h
b = B11

B12

B22

B13

B23

B33

i⊤

.

(6.29)

This reparameterization is useful because it allows us to rewrite the expression
c̃i⊤ Bc̃ j as:
c̃i⊤ Bc̃ j = vij⊤ b,

Z. Zhang. “A Flexible New Technique
for Camera Calibration”. In: IEEE Transactions on Pattern Analysis and Machine Intelligence 22 (2000)
8

(6.30)

The homography matrix maps points
between
two-dimensional
planes
while a projection matrix maps threedimensional points to points on a
two-dimensional plane.
9

---

### [PDF p.186 | Book p.184]

184

principles of robot autonomy

where:
h
vij = c̃i1 c̃ j1 ,

c̃i1 c̃ j2 + c̃i2 c̃ j1 ,

c̃i2 c̃ j2 ,

c̃i3 c̃ j1 + c̃i1 c̃ j3 ,

c̃i3 c̃ j2 + c̃i2 c̃ j3 ,

c̃i3 c̃ j3

i⊤

,

and where c̃ik is the k-th element of the column vector c̃i and c̃ jk is the k-th element of the column vector c̃ j . With this reparameterization, we can rewrite the
constraints in Equation (6.28) as:
⊤
c̃1⊤ Bc̃2 = 0 =⇒ v12
b = 0,

c̃1⊤ Bc̃1 = c̃2⊤ Bc̃2 =⇒ (v11 − v22 )⊤ b = 0,
or by combining them:
"

#
⊤
v12
b = 0,
(v11 − v22 )⊤

(6.31)

which is linear with respect to the unknowns vector b. Importantly, while the
homographies, H, are different for each image due to the different extrinsic parameters, the intrinsic camera parameters represented by the vector b are the
same. Therefore, with N images from the same camera, even with potentially
different perspectives, we can stack the constraints in Equation (6.31) to give:
Vb = 0,

(6.32)

where V ∈ R2N ×6 . In the case where we include the skewness parameter, γ,
in K, there must be N ≥ 3 images in order to specify B uniquely. Similarly to
the approach for computing the projection matrix in the previous section, we can
compute the vector b as the solution to the constrained least squares problem:
minimize

∥Vb∥2 ,

subject to

∥b∥2 = 1.

b

(6.33)

Once we have computed b, we can solve for the intrinsic camera parameters, K, by
leveraging the definition of B = K −T K −1 . In particular, we compute the intrinsic
parameters by:
v0 =

B12 B13 − B11 B23
,
2
B11 B22 − B12

B2 + v0 ( B12 B13 − B11 B23 )
,
λ = B33 − 13
B11
s
λ
α=
,
B11
s
λB11
β=
,
2
B11 B22 − B12

− B12 α2 β
,
λ
γv0
B α2
u0 =
− 13 ,
β
λ
γ=

(6.34)

---

### [PDF p.187 | Book p.185]

camera models and calibration

where we can think of λ as a scaling parameter that accounts for the fact that
there are five unknown camera intrinsic parameters but six degrees of freedom
in B.
Once we have extracted the camera intrinsic parameters, K, from this procedure, given any new homography, H, we can compute the extrinsic parameters
by:
r1 =

K −1 c̃1
,
∥K −1 c̃1 ∥

r2 =

K −1 c̃2
,
∥K −1 c̃2 ∥

(6.35)

r3 = r1 × r2 ,
t=

K −1 c̃3
.
∥K −1 c̃1 ∥

As one final step, we note that the matrix R defined with column vectors r1 , r2 ,
and r3 will not generally satisfy the orthonormality property of a rotation matrix.
We can correct this issue by again using optimization methods to compute a valid
rotation matrix that best corresponds to these column vectors:
minimize

∥ R − Q ∥2 ,

subject to

R⊤ R = I,

h
Q = r1

r2

R

(6.36)

where:
i
r3 .

We solve this problem by choosing R = UV ⊤ , where U and V are defined by the
singular value decomposition of Q = UΣV ⊤ .

6.5.3

Camera Auto-Calibration

The direct linear transformation from Section 6.5.1 and Zhang’s flexible calibration method from Section 6.5.2 require point correspondences to calculate the intrinsic and extrinsic parameters. Auto-calibration offers an alternative approach
that does not make this assumption by utilizing multiple views of a static scene to
determine the camera’s intrinsic and extrinsic parameters. This approach leverages the fact that a camera’s intrinsic parameters remain constant across different
views of the same scene. By identifying correspondences between points in multiple images, we can estimate the intrinsic matrix, K, and extrinsic matrices, R and
t, by bundle adjustment based on the static scene geometry. In total, the camera
auto-calibration process consists of five key steps.
First, we use an algorithm such as scale-invariant feature transform (SIFT) to
identify key points in the scene and their correspondence points across multiple
images from different views. The SIFT algorithm is a computer vision method
to detect, describe, and match local features in images. It is robust in detecting

185

---

### [PDF p.188 | Book p.186]

186

principles of robot autonomy

and describing local features in images, making it effective for finding correspondences under varying conditions. Details of the SIFT algorithm will be discussed
in the following chapters.
Second, we use the correspondences between a pair of images to compute the
fundamental matrix. The fundamental matrix, F ∈ R3×3 , relates corresponding
points between a pair of images of the same scene10 . For a pair of images ( I, I ′ )
of the same scene, the fundamental matrix, F, satisfies:
p⊤ Fp′ = 0,

(6.37)

where p and p′ are corresponding points in images I and I ′ , respectively. We will
discuss the fundamental matrix more in the context of stereo vision in Chapter 7.
To compute the fundamental matrix for the image pair, we first construct a
point correspondence matrix, W, where each row represents a correspondence
between points in the two images. Let (ui , vi ) and (ui′ , vi′ ) be the coordinates of
one set of matched points, pi and pi′ . We form each row of the matrix W using
one set of corresponding coordinates as:


u1 u ′
 . 1
W=
 ..
un u′n

u1 v1′
..
.
un v′n

u1
..
.
un

v1 u1′
..
.
vn u′n

v1 v1′
..
.
vn v′n

v1
..
.
vn

u1′
..
.
u′n

v1′
..
.
v′n


1
.. 

..
1

(6.38)

From this point correspondence matrix, we then compute the fundamental matrix by solving the linear system W f = 0 using a singular value decomposition
(SVD), where f is the vectorized form of the fundamental matrix. We describe
the specifics of this procedure in more detail in Section 7.1.1.
Third, we compute the essential matrix, which is similar to the fundamental matrix in that it relates corresponding points in two images based on scene geometry.
For two images, I and I ′ , we define the essential matrix by the rotation matrix, R,
and translation vector, t, relating the coordinate frames of the two images by:
E = [t]× R,

(6.39)

where [t]× is the matrix representation of the cross product. Assuming the intrinsic matrix, K, remains the same between the images, we can also define the
essential matrix, E, with respect to the fundamental matrix as:
E = K ⊤ FK.

(6.40)

Therefore, we can first compute the essential matrix from the previously computed fundamental matrix and the intrinsic parameter matrix, K, and then we
can compute the camera extrinsic rotation and translation parameters, R and t,
by the singular value decomposition:
E = UΣV ⊤ ,

(6.41)

The fundamental matrix describes the
epipolar geometry between two image
views.
10

---

### [PDF p.189 | Book p.187]

camera models and calibration

187

where Σ = diag(1, 1, 0). From this decomposition, there are two possible solutions for the camera extrinsic parameters:

where:

R1 = UWV ⊤ ,

R2 = UW ⊤ V ⊤ ,

t1 = U [:, 2],

t2 = −U [:, 2],


0

W = 1
0


−1 0

0 0 .
0 1

(6.42)

(6.43)

We can identify the correct solution by using each to compute the three-dimensional
points from the two-dimensional matched correspondence points, as we describe
in the next step. The extrinsic parameters, R and t, we should use are the ones
that ensure that most of the three-dimensional points lie in front of both cameras,
meaning they will have positive depth values.
The fourth step is to perform triangulation to compute the 3D points in the
scene from the 2D image correspondence points. We define the projection matrix,
P, for an image as:
h
i
P=K R

t ,

(6.44)

where again K is the camera intrinsic matrix, R is the rotation matrix, and t is
the translation vector. This projection matrix maps a 3D point in homogeneous
coordinates into the 2D camera frame coordinates by:
 
 
X
u
Y 
 
 
(6.45)
v = P   .
Z
1
1
Therefore, for matched points across two images, we can compute the 3D coordinates by solving the linear system:
 

X
uP3⊤ − P1⊤
 vP⊤ − P⊤   Y 




2
(6.46)
 ′ 3′⊤
   = 0,
u P3 − P1′⊤   Z 
1
v′ P3′⊤ − P2′⊤
where (u, v) are the coordinates and P1 , P2 , and P3 are the first, second, and third
rows of the projection matrix, P, for image I, respectively, and (u′ , v′ ) are the
coordinates and P1′ , P2′ , and P3′ are the rows of the projection P′ for image I ′ . We
can solve Equation (6.46) using a least squares method.
So far, we have used correspondences in pairs of images from the same camera of the same scene to estimate the image extrinsics, R and t, and computed
estimates of the 3D scene points by triangulation. These computations require
knowledge of the camera intrinsic matrix, K, which is the quantity we are trying to estimate. We can leverage the previous steps to compute K by using an
iterative optimization-based procedure, where we begin with an estimate11 of K

For example, we could start with an estimate by referencing the camera manufacturer’s data, or using some other simpler method.
11

---

### [PDF p.190 | Book p.188]

188

principles of robot autonomy

and refine it until convergence. In particular, we refine the estimate of the camera
intrinsics and extrinsics by solving the optimization:
N

M

∑ ∑ ∥ pij − Pi (K, Ri , ti )Xj ∥2 ,

(6.47)

i =1 j =1

where pij is an observed 2D point in image i that corresponds to the j-th 3D point,
X j is the j-th estimated 3D point, Pi (K, Ri , ti ) is the projection matrix for image
i, M is the total number of triangulated 3D points, and N is the total number of
images. Note that each projection matrix is a function of the intrinsic parameters, which are constant across all images, as well as the extrinsic parameters for
the image. We can optimize this cost function by applying a nonlinear method,
such as Levenberg-Marquardt, to compute a new set of parameters. We then repeat the steps listed above, computing new extrinsics, triangulation points, and
optimizing, until convergence.

6.6

RGB-D Camera Calibration

RGB-D cameras present additional calibration challenges beyond traditional cameras. In addition to calibrating the RGB camera using standard methods, we must
also:
• Calibrate the depth sensor’s intrinsic parameters
• Determine the extrinsic transformation between RGB and depth sensors
• Correct for systematic depth measurement errors
• Account for the different fields of view and resolutions of the two sensors
Many manufacturers provide factory calibration, but applications requiring high
accuracy often necessitate custom calibration procedures using specialized targets
that are visible in both RGB and infrared.

6.7

Summary

This chapter presented the mathematical foundations of camera models and calibration techniques essential for vision-based robotics. Starting from the basic
pinhole model, we developed the perspective projection equations that relate
3D world points to 2D image coordinates. We explored practical considerations
including lens models and distortion, and extended our discussion to modern
RGB-D sensors that provide both color and depth information. The calibration
methods presented enable us to estimate the camera parameters necessary for
quantitative vision applications. With calibrated cameras, we can now proceed to
extract three-dimensional information from images, which we explore in the next
chapter through stereo vision and structure from motion techniques.

---

### [PDF p.191 | Book p.189]

camera models and calibration

To learn more. For a deeper dive into camera models and calibration techniques,
readers are encouraged to refer to the Foundations of Computer Vision textbook
by Torralba, Isola, and Freeman [150] for a more in-depth discussion on image
systems and camera models. For practical calibration algorithms and implementations, the OpenCV library12 provides extensive resources and code examples.
Interested readers can consult the works directly from Tsai [152], Lowe [87], and
Triggs et al. [151] for further insights into the algorithms discussed.

6.8

Exercises

The starter code for the exercises provided below is available online through
GitHub. To get started, download the code by running in a terminal window:
git clone https://github.com/StanfordASL/pora-exercises.git

We denote Problems requiring hand-written solutions and coding in Python
with and , respectively.

Problem 1: Camera Calibration: Extrinsics
In this exercise, you will implement the key parts of a method to compute the
camera extrinsic parameters R and t. Specifically, you will use the steps in Section 6.5.1 to compute the homography matrix H given a calibration image. Then,
given the camera intrinsic matrix K, you will use the method at the end of Section 6.5.2 to compute the extrinsics, R and t, for the image. For this exercise, you
will use a chessboard with known dimensions to help with the camera calibration
process. This is a convenient choice because it provides a high contrast and the
grid corner features are easy to detect.
In the file ch06/exercises/camera_extrinsics.ipynb:
1. First, implement the function generate_chessboard_3D_world_coordinates
to compute a grid of 3D world coordinates that correspond to the grid corners
of the chessboard. Note that we can choose to set all of the z-coordinates
to be 0 since we know the chessboard is a 2D plane. Then, implement the
function generate _ chessboard _ 2D _ pixel _ coordinates to compute the 2D
pixel coordinates of the grid corners from an image using the function findCh
essboardCorners from the open-source computer vision package cv2.
2. Second, implement the function compute_homography using the method from
Section 6.5.1. Note that generally in Section 6.5.1 we are computing the projection matrix M ∈ R3×4 , but in this problem we have a slightly simplified
problem of computing the homography matrix H ∈ R3×3 which just maps
points between two 2D planes (since we know the chessboard grid points lie
on a common plane). In other words, when using the approach from Section 6.5.1 rather than dealing with rows mi ∈ R1×4 you should be consid-

189

G. Bradski. “The OpenCV Library”.
In: Dr. Dobb’s Journal of Software Tools
(2000)
12

---

### [PDF p.192 | Book p.190]

190

principles of robot autonomy

ering rows of the homography matrix hi ∈ R1×3 and be using the vectors
h = [ X , Y , 1]⊤ . Once the homography matrix is available, implement the
PW
W W
function compute _ extrinsics using the method at the end of Section 6.5.2
to compute the extrinsics R and t given the intrinsic matrix K. Additionally,
implement the function transform_world_to_pixel to transform a point in
the world frame into the pixel coordinates from the camera intrinsics and extrinsics. Run the provided code to see the result of your computations on some
example chessboard images.

Problem 2: Camera Calibration: Intrinsics
In Problem 1, we provided the camera intrinsic matrix, K. In this exercise13 , you
will use the flexible calibration method described in Section 6.5.2 to compute the
intrinsic matrix yourself. Specifically, explore the notebook
ch06/exercises/camera _ intrinsics.ipynb. You will need to implement the
function compute_intrinsics to compute the matrix K from a list of homography
matrices from different calibration images.

Note you will need to first complete
Problem 1 since this will leverage some
of that problem’s code.
13

---

### [PDF p.193 | Book p.191]

camera models and calibration

References
[20]

G. Bradski. “The OpenCV Library”. In: Dr. Dobb’s Journal of Software Tools
(2000).

[87]

D. G. Lowe. “Object recognition from local scale-invariant features”. In:
Proceedings of the seventh IEEE international conference on computer vision.
Vol. 2. Ieee. 1999, pp. 1150–1157.

[150]

A. Torralba, P. Isola, and W. T. Freeman. Foundations of Computer Vision.
Available under CC-BY-ND-NC license. Cambridge, MA: The MIT Press,
2024. isbn: 978-0-262-04897-2.

[151]

B. Triggs et al. “Bundle adjustment—a modern synthesis”. In: Vision Algorithms: Theory and Practice: International Workshop on Vision Algorithms
Corfu, Greece, September 21–22, 1999 Proceedings. Springer. 2000, pp. 298–
372.

[152]

R. Tsai. “A Versatile Camera Calibration Technique for High-accuracy 3D
Machine Vision Metrology Using Off-the-shelf TV Cameras and Lenses”.
In: IEEE Journal on Robotics and Automation 3.4 (1987), pp. 323–344.

[165]

Z. Zhang. “A Flexible New Technique for Camera Calibration”. In: IEEE
Transactions on Pattern Analysis and Machine Intelligence 22 (2000).

191

---

### [PDF p.194 | Book p.192]

> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]
