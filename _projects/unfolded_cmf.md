---
layout: page
title: Unfolded Covariance Matrix Fitting
description: Covariance matrix fitting using ISTA variants.
importance: 1
category: research
img: /assets/img/project/unfolded_cmf/thumbnail.png
toc:
    sidebar: left
#redirect: https://github.com/metersquared/physics_sim
---
> *Stack : Python, PyTorch, TensorFlow*
> 
> *Collaborator : [Adam Kujawski](https://www.tu.berlin/akustik/ueber-uns/team-personen/adam-kujawski)*

This is a project that I did as a student assistant at the Chair of Technical Acoustics at TU Berlin. The project aims to do covariance matrix fitting of acoustic data using ISTA.

# Motivation

## Sound propagation model through matrix

Assuming a linear time-invariant propagation model, the sound pressure at a microphone located at position $\xi_m \in \mathbb{R}^3$ is described in the frequency domain for an angular frequency $\omega$ as

$$
p_m(\omega) = \sum_{j=1}^{J} h(r_{m,j}(\omega)) s_j(\omega) + n_m(\omega),
$$

where $s_j(\omega)$ is the sound emitted by the $j$-th source, $h(r_{m,j}(\omega))$ is the acoustic transfer function between the $j$-th source and the microphone at distance $r_{m,j}=\|\xi_m - \xi_j\|$, and $n_m(\omega)$ is the noise at the microphone. The goal of covariance matrix fitting (CMF) is to estimate the power of the sound sources from the measured cross-spectral matrix (CSM) of the microphone signals.

When dealing with stationary broadband signals, recovering source contributions from a single single snapshot is not possible. Instead, a microphone array measurement consisting of a finite sequence of L measure snapshots is used, expressed i the multiple measurement vector (MMV) model as

$$
P=HS+N,
$$

where $P\in\mathbb{C}^{M\times L}$ is the matrix of microphone signals, $H\in\mathbb{C}^{M\times J}$ is the acoustic transfer matrix, $S\in\mathbb{C}^{J\times L}$ is the matrix of source signals, and $N\in\mathbb{C}^{M\times L}$ is the noise matrix.

Finding the source contributions through $S$ is undesirable, as it has many unknowns, and thus a better solution is to describe the microphone source and noise contributions through the cross-spectral matrix (CSM). The CSM of microphone signals of $L\rightarrow \infty$ is

$$
C^*=\langle pp^H \rangle =A\langle ss^H \rangle A^H +\langle nn^H \rangle
$$

where $\langle\cdot\rangle$ is the expectation operator, and $A$ is the acoustic transfer matrix. In advanced microphone array methods, the CSM of the microphones is approximated by

$$
\hat{C}= AQA^{H} + \sigma^2 I,
$$

where $Q$ is a diagonal matrix that contains the power of the sound sources, $\sigma^2$ is the noise power, and $I$ is the identity matrix.


## Covariance Matrix Fitting

Covariance matrix fitting (CMF) solves an inverse mathematical problem to characterize the sound sources by minimizing the discrepancy between the measured cross-spectral matrix (CSM) $C$ and the modeled CSM $\hat{C}= AQA^{H} + \sigma^2 I$. The problem can be formulated as

$$
    \underset{Q}{\text{argmin}} \| C - AQA^{H} - \sigma^2 I \|_F^2,
$$

where $\|\cdot\|_F$ is the Frobenius norm. This optimization problem is non-convex and can be solved using iterative algorithms such as the Iterative Shrinkage-Thresholding Algorithm (ISTA) by vectorizing the CSM and the modeled CSM as

$$
\text{vec}(\hat{C}) = (A \otimes A) \text{vec}(\hat{Q}) \implies y=\Psi x,
$$

where $\otimes$ is the Kronecker product, $y=\text{vec}(C-\sigma^2 I)$, $\Psi=A\otimes A$, and $x=\text{vec}(Q)$. We call $\Psi$ the sensing matrix.

Then, we have

$$
 {\text{minimize}} \frac{1}{2} \| y - \Psi x \|_{2}^2+\lambda \| x \|_1, s.t. x \geq 0.
$$

# State-of-the-art

## Iterative Shrinkage-Thresholding Algorithm (ISTA)

ISTA is a special case of the proximal gradient method that is used to solve optimization problems of the form

$$
\underset{x}{\text{argmin}} f(x) + g(x),
$$

In this case, 

$$f(x)=\frac{1}{2} \| y - \Psi x \|_{2}^2$$ 

and 

$$g(x)=\lambda \| x \|_1.$$

The gradient operator is

$$\nabla f(x) = \Psi^T(\Psi x - y),
$$

and the proximate operator is the shrinkage operator $S_{\theta}(x)$, which is defined as

$$S_{\theta}(x) = \text{sign}(x) \cdot \max(|x| - \theta, 0).$$

ISTA iteratively updates the solution as 

$$x^{(k+1)} = S_{\theta} (x^{(k)} - \alpha \nabla f(x^{(k)})),$$

where $\alpha$ is the step size and $k$ is the iteration index.

The main drawback of ISTA is that it can be slow to converge, especially for large-scale problems. Issues include: 

- the constant step size $\alpha$, which can lead to slow convergence, 
- and that ot does not take into account the structure of the problem, which can lead to suboptimal performance.

## Fast ISTA (FISTA)

FISTA is an accelerated version of ISTA that introduces a momentum term to speed up convergence. The update rule for FISTA is given by

$$\begin{aligned}
y^{(k)} &= x^{(k)} + \frac{t_{k-1} - 1}{t_k} (x^{(k)} - x^{(k-1)}), \\
x^{(k+1)} &= S_{\theta} (y^{(k)} - \alpha \nabla f(y^{(k)})),
\end{aligned}$$

where $t_k$ is a sequence defined as $t_k = \frac{1 + \sqrt{1 + 4 t_{k-1}^2}}{2}$ with $t_0 = 1$. FISTA has been shown to have a convergence rate of $O(1/k^2)$, which is faster than the $O(1/k)$ convergence rate of ISTA.

## Algorithm Unfolding 

Algorithm unfolding is a technique that unrolls the iterations of an optimization algorithm into a machine learning model, where the parameters of the model can be learned from data. This approach has been shown to improve the performance of optimization algorithms by learning the optimal parameters for a given problem.

In the context of CMF, we can unfold the iterations of ISTA or FISTA by treating hyperparameters such as the step size $\alpha$ and the regularization parameter $\lambda$ as learnable parameters. The unfolded model can be trained using backpropagation to minimize the loss function, which is typically the mean squared error between the predicted source powers and the true source powers.

# The work

In this project, we explored the use of algorithm unfolding to improve the preformance of ISTA and its variants for covariance matrix fitting. We considered two approaches to unfolding:
- Analytical approach: We derived the gradients of the loss function with respect to the hyperparameters and used them to update the parameters during training.
- Neural network approach: We designed a neural network architecture that mimics the iterations of the optimization algorithm and trained it end-to-end to learn the optimal parameters.

Multiple variants of ISTA were explored, including:
- **Trainable ISTA (TISTA)**: Utilizes a trainable step size $\alpha$ that is trained incrementally at each iteration. ([Ito &amp; Takabe, 2019](https://doi.org/10.1109/TSP.2019.2912879)).
- **Learnable ISTA (LISTA)**: Utilizes reparameterization of weight matrices $W_1=\lambda \Psi^T$ and $W_2=I-\alpha \Psi^T\Psi$ and treat them as learnable parameters along with the shrinkage parameter $\theta$. ([Gregor &amp; LeCun, 2010](https://icml.cc/Conferences/2010/papers/449.pdf)).
- **Analytic LISTA (ALISTA)**: Reduces the number of learnable parameters and treats only the step size $\alpha$ as learnable, while keeping the weight matrix as $W^{(k)}=\alpha^{(k)} \Psi^T$ ([Chen et al., 2019](https://openreview.net/forum?id=B1lnzn0ctQ)).
- **Hyperparameter tuning LISTA (HyperLISTA)**: Uses a gradient-free hyperparameter tuning method on three simple hyperparameters $c_1$, $c_2$, and $c_3$ that defines the step size and momentum ([Chen et al., 2021](https://doi.org/10.48550/arXiv.2110.15900)).
- **Neurally-augmented ALISTA (NA-ALISTA)**: Uses an LSTM network to augment the step size $\alpha$ in ALISTA ([Behrens et al., 2020](https://doi.org/10.48550/arXiv.2010.01930)).

We evaluated the performance of these unfolded algorithms on synthetic data constructed from [Acoular](https://www.acoular.org/) and real data from the air foil dataset measured at the Chair of Technical Acoustics at TU Berlin.

# Findings

In general, we found that due to the complexity of the problem, there is no analytical solution for the optimal parameters of ISTA. Therefore, the analytical approach seems to be infeasible for this problem and the neural network approach seems to be more promising.

{% include figure.liquid loading="eager" path="/assets/img/project/unfolded_cmf/parameter_study.png" class="img-fluid rounded z-depth-1" %}

However, the performance of the unfolded algorithm shows significant improvement for synthetic source mapping data, even for low number of iterations. On the other hand, for real data, the performance improvement is not significant, which can be attributed to the fact that the real data is more complex and has more noise than the synthetic data.

{% include figure.liquid loading="eager" path="/assets/img/project/unfolded_cmf/nmse_plot.png" class="img-fluid rounded z-depth-1" %}

 Nevertheless, while the performance is significant in sythetic data, the performance improvement, while better, is limited which can be attributed to the fact that the real data is more complex and has more noise than the synthetic data. This suggests that while algorithm unfolding can improve the performance of optimization algorithms, it may not always be effective in real-world scenarios where the data is noisy and complex. This is particularly shown in the similar performance between FISTA and AdaNA-ALFISTA, an adaptive variant of NA-ALISTA using FISTA as the base algorithm, and the data structure as an input to the LSTM network.

 {% include figure.liquid loading="eager" path="/assets/img/project/unfolded_cmf/adanaalfista.png" class="img-fluid rounded z-depth-1" %}

# Future work

The project is still ongoing, and further work includes exploring the effects of different LSTM inputs and architectures on the performance of NA-ALISTA, as well as exploring other unfolded algorithms such as HyperLISTA. 
