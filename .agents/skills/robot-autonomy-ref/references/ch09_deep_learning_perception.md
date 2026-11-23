# Ch 9: Deep Learning Architectures for Perception

- **PDF gốc:** `docs/2608.03496v2.pdf` (*Principles of Robot Autonomy*, Gammelli et al., 2026)
- **Phần:** Part II: Robot Perception
- **Trang sách:** 227–250 | **Trang PDF:** 229–252
- **Độ ưu tiên cho dự án:** `THAM KHẢO`
- **Tóm tắt:** Mạng CNN, Transformer, xử lý đám mây điểm 3D (PointNet) và Voxel.

---

### [PDF p.229 | Book p.227]

9
Deep Learning Architectures for Perception
Modern computer vision has shifted from hand-crafted features to end-to-end
learning with deep neural networks. Rather than manually designing feature
extractors like SIFT or HOG descriptors, contemporary approaches learn hierarchical representations directly from data, achieving strong performance across
diverse visual tasks. This transformation has been particularly impactful for
robotics, where robust visual perception is essential for autonomous operation
in complex, unstructured environments. Consider a mobile robot navigating indoors: it must process RGB images to recognize objects while interpreting 3D
LiDAR point clouds to understand spatial layout and plan collision-free paths.
An autonomous vehicle must fuse information from multiple cameras and LiDAR scanners, processing both 2D image grids and irregular 3D point clouds in
real-time. These scenarios require neural network architectures that effectively
process different data modalities. Convolutional Neural Networks (CNNs) leverage spatial locality for processing camera images. Transformers use self-attention
to capture long-range dependencies and enable transfer learning. For 3D data,
point-based networks like PointNet process unordered point clouds directly, while
voxel-based architectures discretize 3D space into regular grids. Each architecture
provides learned feature representations essential for downstream robotic tasks.
In this chapter, we explore fundamental neural network architectures for robotic
perception. We begin with CNNs in Section 9.1 and Transformers in Section 9.2
for image processing, then discuss point-based approaches in Section 9.3 and
voxel-based approaches in Section 9.4 for 3D sensor data. These architectural
foundations serve as building blocks for the detection, segmentation, and scene
understanding methods in subsequent chapters.

9.1

Convolutional Neural Networks

Convolutional neural networks (CNNs) are a type of deep learning architecture
that is very common in the fields of computer vision and image processing. The
architecture of a CNN contains a special structure that leverages convolution
filters similar to those we discussed in Chapter 8. However, in the context of
machine learning, the convolution filters embedded in the structure of a CNN

---

### [PDF p.230 | Book p.228]

228

principles of robot autonomy

are optimized for the desired task and do not require human specification, giving higher performance and reducing the amount of required manual engineering. CNN architectures comprise several main components: convolutional layers,
nonlinear activations, pooling layers, and fully-connected layers. In the following
sections, we discuss these components in more detail.

9.1.1

Convolution Layers

Figure 9.1: A convolution filter being applied to a 3-channel
RGB image.

One of the main structural concepts that is unique to the architecture of a CNN
is the use of convolution layers. Convolution layers exploit the underlying spatial locality structure in images by using sliding, learned filters which are often
much smaller than the image itself. Mathematically, these filters perform operations in a manner similar to other linear filters used in image processing, such as
Gaussian smoothing filters. For a 2D convolution operation, we can express the
computation at each output location as:
m −1 n −1

Yi,j = ∑ ∑ Xi+u,j+v · Wu,v + b,

(9.1)

u =0 v =0

where (i, j) represents the spatial position in the output feature map, X is the
input image, W is the filter with dimensions m × n, and b is the bias term. This
operation slides the filter across the input, computing a weighted sum at each
position. For multi-channel inputs like RGB images with C channels, the convolution extends to:
C −1 m −1 n −1

Yi,j = ∑ ∑ ∑ Xi+u,j+v,c · Wu,v,c + b,
c =0 u =0 v =0

where the filter now has dimension m × n × C and aggregates information across
all input channels to produce a single output value at each spatial location. For
example, in Section 9.1.1, we show how a filter is applied over an image with
three color channels (red, green, and blue), so C = 3. In this case, the filter
has dimension m × n × 3, which is vectorized to a weight vector, w, with 3mn

---

### [PDF p.231 | Book p.229]

deep learning architectures for perception

elements. The stride of the filter describes how many positions it shifts by when
sliding over the input. The output of the filter is then passed through a nonlinear
activation1 .
Once we have applied the filter to the entire image, the collection of outputs
from the nonlinear activation function creates a new filtered image, which we
typically refer to as an activation map, as shown in Section 9.1.1. In practice, a

1

229

Typically a ReLU function.

Figure 9.2: The outputs of a
convolution filter and activation
function applied across an image make up a new image,
called an activation map.

number of different filters are usually learned in each convolution layer, which
produces a corresponding number of activation maps as the output2 . This is
crucial such that each filter can focus on learning one specific relevant feature. We
show examples of different filters that might be learned in different convolution
layers of a CNN in Section 9.1.13 . Notice that the low-level features which are
learned in earlier convolution layers look a lot like edge detectors, which are
more basic and fundamental features, while later convolution layers have filters
that look more like actual objects.

Besides the number of filters applied to
the input, the width and height of the
filter, the amount of padding on the input, and the stride of the filter are other
hyperparameters.
2

M. D. Zeiler and R. Fergus. “Visualizing and Understanding Convolutional
Networks”. In: European Conference on
Computer Vision (ECCV). Springer, 2014,
pp. 818–833
3

Figure 9.3: Low-level, mid-level,
and high-level feature visualizations in a convolutional neural
network from Zeiler and Fergus
(2014).

In general, using convolution layers to exploit the spatial locality of images
provides several benefits. First, parameter sharing applies the same filter parameters at all spatial locations, keeping the total number of learned parameters much
smaller than fully-connected layers would require. Second, sparse interactions
from having filters smaller than the image enable better detection of small, meaningful features and improve computational efficiency through fewer operations.
Third, convolutional layers are equivariant to translation, meaning that convolving
a shifted image produces the same result as shifting the convolution output of
the original image4 , allowing feature detection regardless of position. Finally,
convolutional layers can naturally handle images of varying sizes when needed.

However, convolution is not equivariant to changes in scale or rotation.
4

---

### [PDF p.232 | Book p.230]

230

principles of robot autonomy

9.1.2

Important CNN Components

In addition to convolution layers, there are several other important components
that make up the architecture of a CNN.
Pooling layers. Pooling is the second major structural component in CNNs. Pooling layers typically come after convolution layers and their nonlinear activation
functions. The primary function of a pooling layer is to replace the output of the
convolution layer’s activation map at particular locations with a summary statistic from other spatially local outputs. This helps make the network more robust
against small translations in the input, helps improve computational efficiency
by reducing the size of the input5 , and is useful in enabling the input images to
vary in size6 . The most common type of pooling is max pooling, but other types
also exist, such as mean pooling. A typical max-pooling operation is shown in
Figure 9.4.
Computationally, both max and mean pooling layers operate with the same
filtering idea as in the convolution layers. Specifically, a filter of width, m, and
height, n, slides around the layer’s input with a particular stride. The difference
between the two comes from the mathematical operation performed by the filter,
which as their names suggest are either a maximum element or the mean over the
filter. If the output of the convolution layer has N activation maps, the output of
the pooling layer will also have N images, since the pooling filter is only applied
across the spatial dimensions.

This occurs because it lowers the resolution.
5

The size of the pooling can be modified
to keep the size of the pooling layer output constant.
6

Figure 9.4: Max pooling example with 2 × 2 filter and stride of
2.

Fully connected layers. Downstream of the convolution and pooling layers are
fully connected layers. These layers make up what is essentially just a standard
neural network, which is appended to the end of the network. The function of
these layers is to take the output of the convolution and pooling layers, which we
can think of as a highly condensed representation of the image, and perform a
classification or regression. Generally, the total number of fully connected layers
at the end of the CNN will only make up a fraction of the total number of layers.
CNN performance. We can say that a CNN learns how to process images end-toend because it essentially learns how to perform two steps simultaneously: feature extraction and classification or regression7 . In contrast, classical approaches
to image processing use hand-engineered feature extractors. Since 2012, the performance of end-to-end learning approaches to image processing have dominated
and continue to improve8 . This continuous improvement has generally been realized with the use of deeper networks with more parameters, and also by combining CNN architectures with other techniques such as Transformers.

9.1.3

Notable CNN Architectures

Several landmark CNN architectures have significantly advanced computer vision and demonstrated the power of deep learning.

In other words, it learns the entire process from image input to the desired output.
7

In some specific applications, handengineered features may still be better.
For example, we might use engineering insight to identify a structure to the
problem that a CNN could not easily
learn.
8

---

### [PDF p.233 | Book p.231]

deep learning architectures for perception

AlexNet (2012). AlexNet was the first deep CNN to achieve breakthrough performance on ImageNet, popularizing the use of ReLU activations and dropout
regularization. It demonstrated that deeper networks could dramatically outperform traditional hand-engineered methods, marking a turning point in computer
vision.
ResNet (2015). ResNet introduced residual connections that allow information
to skip layers, enabling the training of much deeper networks—up to 152 layers—without suffering from vanishing gradients. ResNet showed that network
depth itself could be a key factor in improving performance, establishing residual connections as a fundamental architectural component.
YOLO (You Only Look Once). YOLO pioneered real-time object detection by treating detection as a single regression problem rather than a multi-stage classification task. YOLO demonstrated how CNN architectures can be adapted for various computer vision tasks beyond image classification, proving that speed and
accuracy need not be mutually exclusive.
These architectures have not only achieved state-of-the-art results in their respective domains but have also influenced countless subsequent designs and established important principles for CNN development.

9.2

Transformers

Transformers are deep learning architectures that have been widely applied across
various domains, including natural language processing, computer vision, robotics,
and more. Compared to CNNs, Transformers enforce fewer structural constraints
on the input data. As long as we can organize the input into a set or sequence
of tokens, it can be processed by a Transformer-based model. Since the internal structure of the Transformer is purely learned from data rather than handengineered, it requires less domain-specific knowledge, which makes it easier
to generalize across different data modalities. Transformers are also computationally efficient and scalable due to their ability to be parallelized, allowing for
extremely large models with hundreds of billions of parameters to be trained.

9.2.1

Transformer Architecture Fundamentals

The core innovation of the Transformer architecture is the self-attention mechanism, which allows the model to learn relationships between different elements
in the input sequence or set. Unlike CNNs that have built-in spatial inductive
biases through convolution operations, Transformers learn all spatial and semantic relationships directly from data. This flexibility comes at a cost: Transformers
typically require larger datasets to achieve similar performance as architectures
with stronger inductive biases, but they can also achieve superior performance
when sufficient data is available.

231

---

### [PDF p.234 | Book p.232]

232

principles of robot autonomy

Tokens and embeddings. Transformers take inputs in the form of a set or sequence
of tokens. A token is a numeric representation of the raw input data, expressed
as a vector. The process of converting raw inputs into tokens is called tokenization, and the specific method depends on the data modality. For language tasks,
a token might represent a word, subword, or character, generated through a
learned dictionary lookup. For computer vision tasks, a token typically represents a patch—a square subset of the input image. For example, we can convert
an image patch of size P × P with C color channels into a token vector of size CP2
by flattening the patch into a one-dimensional vector.
We then transform each token into a token embedding vector, which is a highdimensional latent space representation. The embedding process is typically a
learned linear operation that maps tokens into a space where semantically or
structurally similar tokens have similar representations. We also add a positional
embedding to each token embedding to encode information about the token’s position in the sequence or spatial location. This positional information is crucial
because the self-attention mechanism itself is permutation-invariant and does not
inherently encode order or position. For example, if a sentence places dog before
cat, the model needs that ordering to capture the sentence’s correct meaning.
Similarly, in vision tasks, knowing which patch came from the top-left versus
bottom-right of an image provides essential spatial context9 .
Once we have transformed the raw input into embedding vectors, we aggregate them as rows of an input matrix, X 0 ∈ R N × D , where N is the context size10
and D is the dimensionality of the embedding space.

Positional embeddings can be learned
parameters or fixed sinusoidal functions.
Learned embeddings are more flexible
but require more data, while fixed embeddings can generalize to sequence
lengths not seen during training.
9

In general, larger context sizes will
give better performance because we
can capture more unique information.
However, this comes at the cost of
increased computational requirements,
which scale quadratically with context
size due to the attention mechanism.
10

Self-attention mechanism. The self-attention mechanism is the key component that
allows Transformers to learn relationships between all elements in the input. Each
embedding vector in X 0 initially represents only a single token and does not
contain contextual information from other tokens. For example, when the phrase
toy car appears in a sentence, the embedding vector for car does not yet encode
the modifier toy. The goal of self-attention is to allow the model to modify each
embedding vector based on its relevance to all other tokens in the sequence.
Mathematically, scaled dot-product self-attention is defined as:
!
QK ⊤
O = Attention( Q, K, V ) = softmax √
V,
(9.2)
dk
where Q ∈ Rm×dk is the query matrix, K ∈ Rn×dk is the key matrix, V ∈ Rn×dv is
the value matrix, and O ∈ Rm×dv is the output matrix. The intuition behind this
formulation is that the term QK ⊤ computes the dot product between all pairs
of queries and keys, where a larger dot product indicates that a particular pair
are similar or relevant to each other. We then apply the softmax function to each
row of the resulting matrix to normalize the rows so that their elements sum to
one11 . Finally, multiplication by the value matrix V produces an output where
each row is a weighted sum of all value vectors, with weights determined by the
normalized attention scores.

√
The division by dk , where dk is the
dimensionality of the keys and queries,
helps stabilize gradients during training
by preventing the dot products from becoming too large.
11

---

### [PDF p.235 | Book p.233]

deep learning architectures for perception

233

In the Transformer architecture, we typically define these matrices as Q =
XWQ , K = XWK , and V = XWV , where X is the input matrix with each row
corresponding to one embedding vector, and WQ , WK , and WV are matrices of
learnable parameters. While we present the mathematical form using matrix
notation for implementation clarity, it is often easier to reason about the transformation of a single embedding vector. Returning to our toy car example, the
attention mechanism would modify the car embedding vector into a new vector
that captures relevant information from other words in the sentence. The value
matrix V provides potential modifications corresponding to each word, and the
attention scores determine which modifications to apply. In this case, the relevance weighting would likely show a strong match between car and toy, resulting
in an updated embedding that represents toy car rather than a generic car.
A single attention mechanism is limited in the types of relationships it can capture, constrained by the finite parameter matrices WQ , WK , and WV . To increase
the model’s expressive capacity, Transformers use multi-head attention, which runs
multiple attention mechanisms in parallel, each with unique parameter matrices
i , W i , and W i for i = 1, . . . , h, where h is the number of attention heads.
WQ
V
K
The outputs from all heads are concatenated and multiplied by another learned
matrix WO to produce the final output. This allows the model to attend to different types of relationships simultaneously—for example, one head might learn
syntactic relationships while another learns semantic relationships.
Transformer layer components. Each Transformer layer consists of two main components arranged sequentially: a multi-head self-attention layer followed by a
feed-forward network, with both components wrapped in residual connections
and layer normalization operations, as shown in Section 9.2.1.

Figure 9.5: A single Transformer
layer showing the multi-head attention block and feed-forward
network, each with residual connections and layer normalization from the Illustrated Transformer (2018).

After the multi-head self-attention layer processes the input, we add the attention output back to the input in what is called a residual connection:
X̄ = X + MultiHeadAttention( X ).
This residual connection allows gradients to flow more easily during training and
helps the network learn identity mappings when beneficial. We then apply layer

---

### [PDF p.236 | Book p.234]

234

principles of robot autonomy

normalization to stabilize training:
X̃ = LayerNorm( X̄ ).
Next, we pass the normalized output through a position-wise feed-forward
network, typically implemented as a multi-layer perceptron (MLP). This MLP consists of two linear transformations with a non-linear activation function12 in between:

The ReLU or GELU activation functions are commonly used.
12

FFN( x ) = W2 · ReLU(W1 x + b1 ) + b2 ,
where the MLP is applied independently to each position (each row of the input
matrix). The feed-forward network typically expands the dimensionality in the
first layer and then projects back to the original dimension in the second layer,
allowing the network to learn complex non-linear transformations of the attention
outputs. This component is followed by another residual connection and layer
normalization:
X ′ = LayerNorm( X̃ + FFN( X̃ )).
A complete Transformer architecture consists of multiple such layers stacked
in sequence, where the output of one layer becomes the input to the next. The
depth of the network (number of stacked layers) is a key hyperparameter that
significantly impacts model capacity and performance13 . Note that the dimensions of the inputs and outputs of each Transformer layer are typically the same
(N × D), allowing for flexible stacking of arbitrary depth.
Final linear and unembedding layer. After passing through all Transformer layers,
we must convert the final embedding representations back into a format suitable
for the specific task. The unembedding layer transforms the learned embedding
vectors into task-specific outputs. For classification tasks, we typically take a
single embedding vector—either a special classification token or an aggregated
representation of all tokens—and pass it through a linear layer followed by a
softmax function:
o = softmax( xW + b),
where x is the selected embedding vector, and W and b are learned parameters.
The output o is a probability distribution over the possible classes, where the
vector size matches the number of classes and all elements sum to one.
For other tasks, the unembedding layer may take different forms. In sequenceto-sequence tasks like machine translation, we apply a linear transformation to
each position’s embedding to predict the next token in the output sequence. In
dense prediction tasks like image segmentation, we may upsample the embeddings back to the original input resolution and apply per-position classification.
The specific design of the final layers depends entirely on the task requirements,
while the core Transformer layers remain largely the same across different applications.

Modern Transformers can have dozens
or even hundreds of layers. For example,
GPT-3 has 96 layers, while some vision
models use 32 or more layers.
13

---

### [PDF p.237 | Book p.235]

deep learning architectures for perception

9.2.2

235

Vision Transformers (ViTs)

Vision Transformers14 represent the most important Transformer architecture for
robotics practitioners, serving as the foundation for modern perception pipelines
in embodied AI systems. Unlike earlier vision models that required careful handengineering of features and architectural components, ViTs enable end-to-end
learning from raw images to task-specific outputs. They have become ubiquitous
in robotic applications, from object recognition and scene understanding in autonomous navigation systems to visual representations for manipulation policies
and multi-modal reasoning in household robots. The ability to pre-train ViTs on
large-scale image datasets and then fine-tune them for specific robotic tasks with
limited data has made them particularly valuable for real-world deployments
where collecting task-specific training data is expensive or impractical.
Architecture adaptation for images. Vision Transformers adapt the general Transformer architecture to process images by treating image patches as tokens. Given
an input image of size H × W with C color channels, ViT divides the image into a
grid of non-overlapping patches of size P × P, resulting in N = HW
patches. Each
P2
2
patch is flattened into a vector of dimension C · P and then linearly projected to
the embedding dimension D through a learned embedding matrix. Common
choices for patch size include P = 16 or P = 32, which balance the trade-off
between computational cost (smaller patches create more tokens) and the ability
to capture fine-grained details15 .
In addition to the patch embeddings, ViT introduces a special learnable class token, denoted xcls , which is prepended to the sequence of patch embeddings. This
class token has no correspondence to any image patch but serves as a global representation that the network can use to aggregate information from all patches
for classification tasks. The class token’s embedding after passing through all
Transformer layers is used as the input to the final classification head. Vision
Transformers use learnable 2D positional embeddings that encode each patch’s
spatial location in the original image grid. Unlike 1D positional embeddings
used in language models, these embeddings must capture 2D spatial structure.
The standard approach uses a separate learned embedding for each position in
the patch grid, which is added to the corresponding patch embedding. Alternative approaches include using sinusoidal positional encodings extended to 2D or
learning relative positional biases. The complete input to the first Transformer
layer is thus:
pos p
pos
pos
p
p
X 0 = [ xcls , x1 + e1 , x2 + e2 , . . . , x N + e N ],
p

pos

where xi are the linearly embedded patches and ei
dings.

are the positional embed-

Training considerations. A key characteristic of Vision Transformers is their data
requirements compared to CNNs. Because ViTs lack the built-in inductive biases
of convolution operations—such as translation equivariance and local connec-

A. Dosovitskiy et al. “An Image is
Worth 16x16 Words: Transformers for
Image Recognition at Scale”. In: International Conference on Learning Representations. 2021
14

For a standard 224 × 224 image with
P = 16, this creates 14 × 14 = 196 patch
tokens.
15

---

### [PDF p.238 | Book p.236]

236

principles of robot autonomy

tivity—they require substantially larger training datasets to achieve comparable
performance with similar model sizes. When trained on smaller datasets like
ImageNet-1K (1.3 million images), ViTs typically underperform similarly-sized
CNNs. However, when pre-trained on larger datasets such as ImageNet-21K (14
million images) or even larger proprietary datasets, ViTs can match or exceed
CNN performance, and their performance continues to improve with dataset
scale in ways that CNNs do not.
This observation has led to a standard training paradigm for ViTs: pre-training
on large-scale datasets followed by fine-tuning on smaller, task-specific datasets.
Pre-training can be done with supervised learning on labeled image datasets
or through self-supervised methods that learn representations from unlabeled
images. Self-supervised pre-training methods such as masked image modeling—where random patches are masked and the model learns to predict them—have
proven particularly effective for ViTs and enable training on massive unlabeled
image corpora. After pre-training, the model can be fine-tuned on downstream
tasks with relatively small amounts of labeled data, often requiring only the final
classification layers to be retrained while the Transformer layers remain largely
fixed or are fine-tuned with small learning rates.
For robotics applications, this pre-training and fine-tuning paradigm is especially valuable. Robotic systems often operate in specialized environments with
limited task-specific data, but can leverage visual representations learned from
generic internet-scale image datasets. A ViT pre-trained on diverse visual data
captures general-purpose features like edge detection, object recognition, and
spatial relationships that transfer effectively to robotic tasks like grasping, navigation, and scene understanding.
Practical considerations. The choice between Vision Transformers and CNNs for
robotic applications involves several practical trade-offs. ViTs excel when large
pre-trained models are available and when the task benefits from modeling longrange dependencies across the entire image. Their flexibility in handling variable
input sizes and their ability to scale to very large model sizes make them attractive
for applications where computational resources are available and high accuracy
is critical. However, CNNs remain competitive or superior in scenarios with
limited data, real-time constraints on resource-constrained hardware, or tasks
where strong spatial inductive biases are beneficial.
Computationally, ViTs have quadratic complexity with respect to the number of patches due to the self-attention mechanism, making them more expensive
than CNNs for high-resolution images. Recent variants like Swin Transformer address this by using local attention windows and hierarchical structures, combining some of the efficiency benefits of CNNs with the flexibility of Transformers.
For robotics practitioners, the decision often comes down to whether pre-trained
models are available for the specific visual domain, the computational budget of
the deployment platform, and whether the task requires the global reasoning capabilities that attention mechanisms provide. In many modern robotic systems,

---

### [PDF p.239 | Book p.237]

deep learning architectures for perception

237

hybrid approaches that combine CNN backbones for efficient feature extraction
with Transformer layers for high-level reasoning have proven effective, leveraging
the complementary strengths of both architectures.

9.3

Point Cloud Processing and Point-Based Networks

Robotic systems operating in 3D environments frequently rely on LiDAR sensors, depth cameras, and other sensing modalities that produce point cloud data.
Point clouds represent 3D data as collections of points in space, where each point
is defined by its position p and may include additional attributes such as color,
intensity, or surface normals16 . In autonomous driving, LiDAR sensors capture
millions of points per second to create detailed 3D maps enabling real-time obstacle detection and navigation. Unlike images with regular 2D grid structure,
point clouds possess unique characteristics requiring specialized neural network
architectures.

9.3.1

Common representations include
Cartesian coordinates ( x, y, z), spherical
coordinates (r, θ, ϕ), or cylindrical
coordinates (r, θ, z) depending on the
sensor type.
16

Point Cloud Characteristics

Point clouds differ fundamentally from images in three key ways that shape neural network design. Point clouds are unordered sets with no inherent sequential or spatial ordering. A point cloud with N points can be represented as
{p1 , p2 , . . . , p N } where each point pi ∈ Rd (typically d = 3). Crucially, any permutation of these points represents the same geometric object, requiring neural
networks to be permutation invariant.

Figure 9.6: LiDAR point cloud
data from an autonomous vehicle showing cars and road infrastructure.

Point clouds exhibit variable cardinality, containing vastly different numbers of
points across samples. While images have fixed resolution (e.g., 224 × 224 pixels),
point clouds might contain anywhere from 1,000 to 100,000 points depending on
scanning resolution, sensor distance, and object complexity, posing challenges for
batch processing and network design. Section 9.3.1 and Section 9.3.1 illustrate this
variability. Point clouds are also sparse and irregular, with points distributed non-

---

### [PDF p.240 | Book p.238]

238

principles of robot autonomy

Figure 9.7: Point clouds of
different objects showing variable cardinality: a simple table
(fewer points), a detailed chair
(more points), and a toy building facade (most points).

uniformly throughout 3D space at varying local densities determined by scanning
angle, distance, and surface properties. Most 3D space contains no points, and
local neighborhood structure around each point varies significantly, contrasting
sharply with the dense, regular grid of image pixels.

9.3.2

PointNet Architecture

PointNet17 approaches point cloud processing through several key architectural
innovations that ensure permutation invariance while extracting meaningful geometric features. The architecture consists of point-wise feature extraction, symmetric aggregation functions, and spatial transformation components that work
together to process unordered point sets effectively.

C. R. Qi et al. “Pointnet: Deep learning on point sets for 3d classification
and segmentation”. In: Proceedings of the
IEEE conference on computer vision and pattern recognition. 2017, pp. 652–660
17

Figure 9.8:
PointNet architecture showing point-wise
MLPs, transformation networks
(T-Net), and symmetric aggregation for classification and
segmentation tasks, from Qi et
al. (2017).

Point-wise multi-layer perceptrons. PointNet applies multi-layer perceptrons (MLPs)
independently to each point in the cloud. Given N points where each point
pi ∈ R3 represents spatial coordinates, PointNet computes:
hi = MLP( pi ),
where hi ∈ Rk is the learned feature representation. This point-wise processing
maintains permutation invariance because the same transformation applies to
each point regardless of input order. The MLP consists of fully connected layers
with ReLU activations, progressively increasing dimensionality from 3D coordinates to higher-dimensional spaces (e.g., 64, 128, 1024 dimensions). The MLP
parameters are shared across all points, similar to parameter sharing in CNN filters, but without spatial locality constraints. The overall architecture is shown in
Section 9.3.2.

---

### [PDF p.241 | Book p.239]

deep learning architectures for perception

Symmetric aggregation functions. After extracting point-wise features, PointNet
must aggregate these features into a single global representation while preserving permutation invariance. This is achieved through symmetric functions that
produce the same output regardless of input ordering. The most commonly used
symmetric function in PointNet is the element-wise maximum:
g = maximize
i =1,...,N

hi ,

where the max operation is applied element-wise across all feature vectors hi .
This is provably permutation invariant because for any permutation σ:
max hσ(i) = max hi .
i

i

While alternative symmetric functions like summation or mean could be used,
max pooling has the advantage of being selective, allowing the network to focus
on the most discriminative features across all points. However, this global aggregation approach means that PointNet captures only global features and may miss
important local geometric structures, which motivates the hierarchical extensions
in PointNet++, which we will discuss later in this section.
Transformation networks (T-Nets). To achieve invariance to geometric transformations such as rotation and translation, PointNet incorporates transformation networks (T-Net) that learn to align point clouds to a canonical orientation. The
T-Net is itself a mini-PointNet that predicts a transformation matrix T ∈ Rk×k :
T = T-Net({ p1 , p2 , . . . , p N }).
This transformation matrix is then applied to either the input coordinates (input transform) or intermediate features (feature transform). For the input transform, T ∈ R3×3 aligns the spatial coordinates, while for the feature transform,
T ∈ R64×64 normalizes the feature space. To ensure the stability of optimization,
a regularization term is added to the loss function that encourages the transformation matrix to be close to orthogonal:
Lreg = || I − TT T ||2F ,
where || · || F denotes the Frobenius norm. This regularization prevents the transformation from becoming degenerate and helps maintain the geometric properties of the point cloud.

9.3.3

Notable Point-Based Architectures

Several landmark point-based architectures have extended PointNet’s core ideas
to address its limitations and improve performance on complex 3D understanding tasks.

239

---

### [PDF p.242 | Book p.240]

240

principles of robot autonomy

PointNet++. While PointNet effectively captures global features, it struggles to
learn local geometric patterns due to its reliance on global max pooling. PointNet++18 addresses this limitation by introducing a hierarchical architecture that
learns features at multiple scales, similar to how CNNs build hierarchical representations through multiple convolutional layers. PointNet++ introduces set
abstraction layers that recursively apply PointNet to local regions. Given a point
cloud with N points, each set abstraction layer samples N ′ representative points
(where N ′ < N), groups nearby points around each representative point, and
applies a PointNet to extract local features. This process creates a hierarchical
pyramid of features, where early layers capture fine-grained local details and
later layers capture broader geometric patterns.
Set abstraction in PointNet++ consists of three key operations: sampling, grouping, and feature extraction. Sampling uses farthest point sampling (FPS) to select
representative points that provide good coverage of the entire point cloud. Given
a set of points, FPS iteratively selects the point that is farthest from all previously
selected points, ensuring diverse spatial coverage. Grouping then defines local
regions around each selected point using either ball query (all points within radius r) or k-nearest neighbors. This creates local point sets of varying sizes that
capture the local geometry around each representative point. Feature extraction
applies PointNet to each local region to learn features that capture local geometric patterns while maintaining permutation invariance within each region. For
tasks requiring point-wise predictions like semantic segmentation, PointNet++
includes feature propagation layers that upsample features from coarser to finer
resolutions. These layers use inverse distance weighted interpolation to propagate features from subsampled points back to the original point cloud:
( j −1)

f

( j)

(x) =

∑ik=1 wi ( x ) f i

∑ik=1 wi ( x )

,

wi ( x ) =

C. R. Qi et al. “Pointnet++: Deep hierarchical feature learning on point sets in
a metric space”. In: Advances in neural
information processing systems 30 (2017)
18

1
,
d( x, xi ) p

where f ( j) represents features at layer j, d( x, xi ) is the distance between points,
and p is typically set to 2. Skip connections between corresponding abstraction
and propagation layers help preserve fine-grained details, similar to U-Net architectures in image segmentation.
Dynamic graph CNN (DGCNN). An alternative approach to processing point
clouds treats them as graph structures, where points serve as nodes and edges
are defined based on spatial proximity or learned relationships. Dynamic Graph
Convolutional Neural Networks (DGCNN)19 exemplify this approach by constructing graphs dynamically in feature space rather than just coordinate space.
DGCNN applies edge convolution operations that aggregate information from
neighboring points:
xi′ = maximize hθ ( xi , x j − xi ),
j:(i,j)∈E

where xi and x j are feature vectors of connected points, hθ is a learnable function
(typically an MLP), and the edge set E is dynamically updated based on feature

Y. Wang et al. “Dynamic graph cnn
for learning on point clouds”. In: ACM
Transactions on Graphics (tog) 38.5 (2019),
pp. 1–12
19

---

### [PDF p.243 | Book p.241]

deep learning architectures for perception

similarity after each layer. This dynamic graph construction allows the network
to capture both geometric and semantic relationships that evolve as features are
learned. The edge convolution operation differs from standard graph convolutions by explicitly modeling the edge information ( x j − xi ), which captures the
relative geometric relationships between neighboring points. This approach has
shown success in tasks like point cloud classification and part segmentation.

9.3.4

Applications and Limitations

After processing through these point-based architectures—PointNet’s point-wise
MLPs and symmetric aggregation, PointNet++’s hierarchical set abstraction layers, or DGCNN’s dynamic graph convolutions—the networks produce rich pointwise feature representations that encode both local geometric patterns and global
shape information. These learned features serve as inputs for downstream tasks
including 3D object detection, semantic segmentation of points into categories
like road, building, or vegetation, and instance segmentation for identifying individual objects. We will explore training methods for these detection and segmentation tasks in subsequent chapters.
Despite their effectiveness, point-based methods face computational challenges
when processing large-scale point clouds. Real-world applications like autonomous
driving can generate point clouds with millions of points per frame, making
the O( N 2 ) complexity of neighborhood search in DGCNN or the recursive sampling in PointNet++ computationally prohibitive. Memory requirements also
scale poorly, as each point must be processed individually, leading to irregular memory access patterns that are inefficient on modern GPU architectures. In
the following section, we discuss voxel-based and pillar-based approaches that
leverage regular grid structures for efficient 3D convolutions. By discretizing 3D
space into regular voxels or vertical pillars, these methods can apply standard
convolutional operations while maintaining spatial locality and enabling efficient
parallel processing. This structured representation trades some geometric precision for computational efficiency and scalability, making it particularly suitable
for real-time applications in autonomous driving and robotics where processing
speed is critical.

9.4

Voxel-Based 3D Processing

In the previous section, we discussed that the computational limitations of pointbased methods have motivated the development of grid-based approaches that
discretize 3D space into regular structures, enabling the application of efficient
convolutional operations. Rather than processing individual points with irregular neighborhoods, voxel-based and pillar-based methods transform point clouds
into structured representations where standard CNNs can be applied. This paradigm
shift trades some geometric precision for substantial computational advantages,
making real-time processing of large-scale point clouds feasible for applications

241

---

### [PDF p.244 | Book p.242]

242

principles of robot autonomy

like autonomous driving. By leveraging the regularity of grid structures, these
methods can utilize optimized convolution implementations and parallel processing capabilities of modern hardware.

9.4.1

Grid-Based Representations

Grid-based methods transform irregular point clouds into structured representations by discretizing 3D space into regular units. Two primary approaches have
emerged: voxel-based representations that divide space into cubic voxels, and
pillar-based20 representations that use vertical columns extending through the
entire height of the scene.

Frequently used in autonomous vehicle or navigation domain, where the
scene can be viewed as a 2D “map” instead of a true 3D scene, for computational efficiency.
20

Figure 9.9: Comparison of point
cloud representations: original
point cloud (dots) overlaid on
the voxel-based discretization
into 3D cubic cells from Kang et
al. (2018).

The voxel-based representation (Section 9.4.1) creates a full 3D regular grid structure of size L × W × H by partitioning space into cubic cells of size vl × vw × vh 21 ,
where each voxel can contain zero or more points from the original point cloud.
This approach preserves complete spatial relationships in all three dimensions,
enabling rich 3D feature learning through volumetric convolutions. Points within
each voxel are aggregated into a single feature representation, typically through
operations like mean pooling, max pooling, or learned aggregation functions.
In contrast, the pillar-based representation adopts a 2.5D approach, looking at
the scene from a bird’s-eye view, and treats vertical columns (“pillars”) as the
fundamental processing unit. The space is transformed into a 2D grid structure
of size L × W. Each pillar extends vertically through the entire height range of
the point cloud, effectively collapsing the height dimension during initial processing. This approach is particularly useful in self-driving settings, where the
scene processed is often very large and the reduction to 2D significantly improves
computational efficiency. Points within each pillar are aggregated while preserving some height information through encoding strategies, but the primary spatial
reasoning occurs in the horizontal, bird’s-eye view plane.
The choice between these representations involves significant trade-offs in computational complexity and spatial information preservation. Voxel-based methods provide richer spatial context by maintaining full 3D neighborhood relationships with memory scaling as O( L × W × H ), enabling detection of complex
3D geometric patterns but requiring computationally expensive 3D convolutions.

In practice, these dimensions are often
set to be equal, creating cubic voxels.
21

---

### [PDF p.245 | Book p.243]

deep learning architectures for perception

243

Pillar-based approaches reduce complexity by projecting the problem into 2D
with memory scaling as O( L × W ), enabling the use of mature 2D CNN architectures and optimized implementations, but potentially losing important vertical
structure information crucial for multi-level feature detection. Both representations face spatial resolution trade-offs, where finer grids capture more geometric
detail at exponentially higher computational cost, and must address sparsity challenges where most grid cells remain empty, motivating the development of sparse
convolution techniques.

9.4.2

3D Convolution Fundamentals

Once point clouds are discretized into regular grid structures, we can apply convolutional operations to learn hierarchical feature representations. This section
covers the fundamental operations that enable efficient processing of voxelized
3D data.
3D convolution operations. 3D Convolutional Neural Networks extend the successful principles of 2D CNNs to volumetric data by operating directly on 3D
grids of voxels. While 2D convolutions slide filters across height and width dimensions of images, 3D convolutions add depth as a third spatial dimension,
enabling the network to capture spatial relationships to understand the 3D scene.
Specifically, a 3D convolution applies a filter of size (k x , k y , k z ) across all three
spatial dimensions of the input volume. Mathematically, for an input volume X
and filter W, the 3D convolution operation can be expressed as:
k x −1 k y −1 k z −1

Yi,j,k = ∑

∑ ∑ Xi+u,j+v,k+w · Wu,v,w + b,

(9.3)

u =0 v =0 w =0

where (i, j, k ) represents the spatial position in the output volume and b is the
bias term. Note that in practice, both the input X and output Y typically have an
additional channel dimension for multi-channel feature maps, and the weight W
is a 4D tensor that includes both spatial dimensions and input/output channel
dimensions, while the bias b is a vector with one element per output channel. The
geometric interpretation is shown in Section 9.4.2.

Figure 9.10: A 3D convolution filter sliding across a volumetric input, showing how the
(k x , k y , k z ) filter operates in all
three spatial dimensions.

Common kernel sizes include 3 × 3 × 3 for capturing local 3D patterns and
1 × 1 × 1 for channel-wise feature mixing without spatial aggregation22 . The key

Larger kernels like 5 × 5 × 5 can capture broader spatial context but significantly increase computational cost due
to the cubic scaling of operations.
22

---

### [PDF p.246 | Book p.244]

244

principles of robot autonomy

advantage of 3D convolutions over approaches that process 2D slices independently is their ability to learn features that span multiple depths, such as the full
3D shape of objects or volumetric textures. The receptive field in 3D grows cubically with network depth, allowing deeper layers to capture increasingly global
context, though this rapid growth must be balanced against increased computational cost.
Sparse convolutions. Real-world point clouds exhibit extreme sparsity when discretized into voxel grids. In many applications such as autonomous driving and
indoor scene processing, the majority of 3D space consists of empty air or unoccupied regions. Standard dense 3D convolutions waste significant computation
on empty space, making them impractical for large-scale applications. Sparse
convolutions address this by computing only on occupied voxels and their neighborhoods, using efficient data structures to maintain compact representations of
non-empty regions23 .

Popular implementations include
for PyTorch/TensorFlow and
Minkowski Engine for general sparse
tensor operations.
23

spconv

Example 9.4.1 (Memory savings in sparse convolutions). A typical autonomousvehicle LiDAR scene discretized at 10cm resolution over a 100m × 100m × 10m
volume would require:
Grid size =

100m 100m
10m
×
×
= 1000 × 1000 × 100,
0.1m
0.1m
0.1m

Total voxels = 1000 × 1000 × 100 = 100 million voxel features per layer,
In contrast, sparse representations store only the occupied voxels, making memory usage proportional to the number of non-empty voxels rather than total grid
size. The sparser the scene, the greater the memory savings.

9.4.3

Notable Voxel-Based Architectures

Several landmark architectures have demonstrated the effectiveness of grid-based
representations for 3D perception tasks, particularly in autonomous driving applications where real-time performance is critical.
VoxelNet. VoxelNet24 was one of the pioneering architectures for processing
voxel-based representations. The architecture addresses the challenge of processing irregular point clouds by first voxelizing them into a 3D voxel grid, then
leveraging 3D convolutions to extract features and detect objects. A core component of VoxelNet is its Voxel Feature Encoding (VFE) layers, which process the
variable number of points within each voxel to produce fixed-size feature representations. The full architecture is shown in Section 9.4.3. Given a voxel containing points { p1 , p2 , . . . , pn }, where each point pi = ( xi , yi , zi , ri ) includes spatial
coordinates and optional reflectance intensity, the VFE layers apply point-wise
multi-layer perceptrons to each point independently:
f i = MLP( pi ).

Y. Zhou and O. Tuzel. “Voxelnet: Endto-end learning for point cloud based 3d
object detection”. In: Proceedings of the
IEEE conference on computer vision and pattern recognition. 2018, pp. 4490–4499
24

---

### [PDF p.247 | Book p.245]

deep learning architectures for perception

245

Figure 9.11: VoxelNet architecture from Zhou and Tuzel
(2018), showing the complete
pipeline from point cloud voxelization through VFE layers, 3D
convolutional middle layers, to
the Region Proposal Network
for 3D object detection.

To capture contextual information within each voxel, VoxelNet augments each
point with the centroid of all points in the same voxel. For a voxel containing
n points, the centroid is computed as p̄ = n1 ∑in=1 pi , and each point is then represented as the concatenation [ pi , pi − p̄], providing both absolute and relative
spatial information. The VFE layers then aggregate features across all points in
the voxel using element-wise max pooling, ensuring permutation invariance:
v = maximize
i =1,...,n

fi ,

where v is the final voxel-level feature representation. This aggregation step converts the variable-sized point sets within each voxel into fixed-size feature vectors
suitable for subsequent 3D convolution operations.
After voxel feature encoding, VoxelNet applies a series of 3D convolutional
middle layers to build hierarchical representations of the scene. These layers follow standard 3D CNN design principles, progressively increasing receptive field
size while extracting increasingly abstract features. The sparse nature of voxel
occupancy makes this stage well-suited for sparse convolution implementations
to improve computational efficiency. The 3D convolutional layers aggregate information across neighboring voxels to capture larger geometric structures, build
multi-scale representations through progressive downsampling, and prepare features for the final object detection stage.
PointPillars. While VoxelNet processes full 3D voxels, PointPillars25 takes a different approach by using vertical pillars that extend through the entire height of
the scene. The key innovation lies in the Pillar Feature Network (PFN), which
encodes points within each pillar and then converts the resulting pillar features
into a 2D “pseudo-image” representation. This transformation allows PointPillars
to leverage mature 2D CNN architectures for subsequent processing, rather than
computationally expensive 3D convolutions. The pillar-based approach offers
significant computational advantages by reducing the problem from 3D to 2.5D,
enabling the use of optimized 2D convolution operations and existing hardware

A. H. Lang et al. “Pointpillars: Fast
encoders for object detection from point
clouds”. In: Proceedings of the IEEE/CVF
conference on computer vision and pattern
recognition. 2019, pp. 12697–12705
25

---

### [PDF p.248 | Book p.246]

246

principles of robot autonomy

Figure 9.12: PointPillars architecture showing pillar feature
encoding and 2D CNN backbone for efficient real-time 3D
object detection, from Lang et al.
(2019).

accelerations designed for image processing. This design choice makes PointPillars particularly suitable for real-time applications where computational efficiency is crucial, achieving inference speeds suitable for autonomous driving
while maintaining competitive detection accuracy, as shown in Section 9.4.3.
Other variants. Building on the success of VoxelNet and PointPillars, several variants have been developed to further improve performance and efficiency. SECOND (Sparsely Embedded Convolutional Detection)26 combines voxel-based processing with sparse convolution techniques for improved efficiency, significantly
reducing computational requirements while maintaining accuracy. Voxel R-CNN
extends the voxel-based approach with refined detection stages, while VoxelNet introduces architectural improvements that further push the boundaries of
voxel-based 3D detection performance. Similar to point-based architectures, after
processing through these voxel-based architectures—VoxelNet’s VFE layers and
3D convolutions, or PointPillars’ pillar encoding and 2D CNNs—the networks
produce rich feature representations that encode geometric patterns and spatial
relationships across the scene. These learned features serve as input to Region
Proposal Networks (RPNs) that generate 3D bounding box proposals for object
detection. The key contribution of these approaches lies in demonstrating that
the entire pipeline—from raw point cloud processing to 3D object detection—can
be trained end-to-end, allowing the networks to learn optimal feature representations specifically for the detection task rather than relying on hand-crafted features. We will explore the details of training object detection networks and designing appropriate loss functions in subsequent chapters on object detection and
segmentation.

9.5

Summary

In this chapter, we explored fundamental neural network architectures that form
the backbone of modern robotic perception, which has shifted from hand-crafted
features to end-to-end learning from data. We began with Convolutional Neural Networks (CNNs), detailing their core components—convolutional layers,
pooling, and fully-connected layers—that leverage spatial locality and translation
equivariance for processing image data. We discussed landmark architectures like
AlexNet, ResNet, and YOLO that demonstrated the power of deep, hierarchical

Y. Yan, Y. Mao, and B. Li. “Second:
Sparsely embedded convolutional detection”. In: Sensors 18.10 (2018), p. 3337
26

---

### [PDF p.249 | Book p.247]

deep learning architectures for perception

feature learning. We then introduced the Transformer architecture, whose selfattention mechanism captures long-range dependencies without built-in spatial
biases. We covered its key elements, including tokenization, positional embeddings, and multi-head attention, and focused on its adaptation to vision through
Vision Transformers (ViTs), which process images as sequences of patches and
excel when pre-trained on large datasets. Finally, we addressed the challenge
of 3D sensor data by examining point-based networks like PointNet, which use
permutation-invariant operations on point sets, and its hierarchical extension,
PointNet++. We then discussed voxel-based methods, which discretize point
clouds into regular grids to enable efficient 3D convolutions, as seen in VoxelNet, and pillar-based approaches like PointPillars that project data into a 2D
representation for computational efficiency.
To learn more. For a deeper exploration of the topics covered in this chapter,
several key resources are available. A comprehensive foundation in deep learning concepts relevant to all architectures discussed can be found in Goodfellow,
Bengio, and Courville [41]. The seminal paper on the Transformer architecture
is presented by Vaswani et al. [154], while its application to vision is detailed
in Dosovitskiy et al. [32]. For in-depth studies on 3D perception, the original
papers on PointNet [111] and VoxelNet [167] are essential reading. Finally, for
a broader perspective on computer vision algorithms that contextualize these
learning-based approaches, we refer the reader to Szeliski [145].

9.6

Exercises

The starter code for the exercises provided below is available online through
GitHub. To get started, download the code by running in a terminal window:
git clone https://github.com/StanfordASL/pora-exercises.git

We denote Problems requiring hand-written solutions and coding in Python
with and , respectively.

Problem 1: Convolutional Neural Network (CNN)
In this exercise you will implement a basic convolutional neural network and use
it to classify images from the CIFAR-10 dataset. The CIFAR-10 dataset consists of
a large number of small RGB images of objects belonging to ten different classes.
In the notebook ch09/exercises/cnn.ipynb, complete the following:
1. Run the provided code to load the CIFAR-10 dataset. Take a look at some of
the sample images, what is the dimension of each image?
2. Complete the implementation of the SimpleCNN class to define the model architecture. Specifically, your model should have two convolution layers with

247

---

### [PDF p.250 | Book p.248]

248

principles of robot autonomy

ReLU activation and max pooling. Use the provided values to define the parameters of each of the features, such as the convolution kernel size and number of output channels. Following the convolution layers, your model should
have two fully connected layers separated by a ReLU activation. Use the provided value to define the dimension of the hidden layer, and you should be
able to determine the appropriate size of the first fully connected layer input
based on the last convolution layer output size. Additionally, implement the
remaining code in the training loop to train your model using the provided
criterion and optimizer. Run the provided code to train your model and
evaluate the model’s performance on a test dataset.
3. Run the provided code to display the confusion matrix from the test dataset
results. What is this showing you? Are there any surprising results or does
this match your intuition?
4. How many parameters does your model have in total?

---

### [PDF p.251 | Book p.249]

deep learning architectures for perception

References
[2]

J. Alammar. The Illustrated Transformer. https : / / jalammar . github . io /
illustrated-transformer/. Blog post. Accessed: 2026-04-09. June 2018.

[32]

A. Dosovitskiy et al. “An Image is Worth 16x16 Words: Transformers for
Image Recognition at Scale”. In: International Conference on Learning Representations. 2021.

[41]

I. Goodfellow, Y. Bengio, and A. Courville. Deep Learning. http://www.
deeplearningbook.org. MIT Press, 2016.

[64]

Z. Kang et al. “Voxel-Based Extraction and Classification of 3-D Pole-Like
Objects From Mobile LiDAR Point Cloud Data”. In: IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 11 (Nov. 2018),
pp. 4287–4298. doi: 10.1109/JSTARS.2018.2869801.

[75]

A. H. Lang et al. “Pointpillars: Fast encoders for object detection from
point clouds”. In: Proceedings of the IEEE/CVF conference on computer vision
and pattern recognition. 2019, pp. 12697–12705.

[111]

C. R. Qi et al. “Pointnet: Deep learning on point sets for 3d classification
and segmentation”. In: Proceedings of the IEEE conference on computer vision
and pattern recognition. 2017, pp. 652–660.

[112]

C. R. Qi et al. “Pointnet++: Deep hierarchical feature learning on point
sets in a metric space”. In: Advances in neural information processing systems
30 (2017).

[145]

R. Szeliski. Computer vision: algorithms and applications. Springer Science &
Business Media, 2010.

[154]

A. Vaswani et al. “Attention is All you Need”. In: Advances in Neural Information Processing Systems. Vol. 30. Curran Associates, Inc., 2017.

[157]

Y. Wang et al. “Dynamic graph cnn for learning on point clouds”. In: ACM
Transactions on Graphics (tog) 38.5 (2019), pp. 1–12.

[160]

Y. Yan, Y. Mao, and B. Li. “Second: Sparsely embedded convolutional
detection”. In: Sensors 18.10 (2018), p. 3337.

[162]

M. D. Zeiler and R. Fergus. “Visualizing and Understanding Convolutional Networks”. In: European Conference on Computer Vision (ECCV). Springer,
2014, pp. 818–833.

[167]

Y. Zhou and O. Tuzel. “Voxelnet: End-to-end learning for point cloud
based 3d object detection”. In: Proceedings of the IEEE conference on computer
vision and pattern recognition. 2018, pp. 4490–4499.

249

---

### [PDF p.252 | Book p.250]

> [Trang ít chữ / trang hình minh họa — xem trực tiếp PDF gốc nếu cần]
