# Improved (Related-key) Differential-based Neural Distinguishers for SIMON and SIMECK Block Ciphers

**Authors:** Jinyu Lu, Guoqiang Liu, Bing Sun, Chao Li, Li Liu

**Source PDF:** `2022_lu_related_key_neural_distinguishers_simon_simeck_eprint.pdf`

## Abstract

In CRYPTO 2019, Gohr made a pioneering attempt and successfully applied deep learning to the differential cryptanalysis against NSA block cipher Speck32/64, achieving higher accuracy than the pure differential distinguishers. By its very nature, mining effective features in data plays a crucial role in data-driven deep learning. In this paper, in addition to considering the integrity of the information from the training data of the ciphertext pair, domain knowledge about the structure of differential cryptanalysis is also considered into the training process of deep learning to improve the performance. Meanwhile, taking the performance of the differential-neural distinguisher of Simon32/64 as an entry point, we investigate the impact of input difference on the performance of the hybrid distinguishers to choose the proper input difference. Eventually, we improve the accuracy of the neural distinguishers of Simon32/64, Simon64/128, Simeck32/64, and Simeck64/128. We also obtain related-key differential-based neural distinguishers on round-reduced versions of Simon32/64, Simon64/128, Simeck32/64, and Simeck64/128 for the first time.

## INTRODUCTION

The security analysis of many cryptographic primitives (such as pseudo-random number generators, hash functions, etc.) is usually attributed to attacks on the underlying block ciphers. Various cryptanalytic methods have been proposed over the past few decades, including differential cryptanalysis [1] , linear cryptanalysis [2] , integral cryptanalysis [3] , zerocorrelation linear cryptanalysis [4] , etc. A block cipher must be able to resist all known cryptanalysis to obtain a strong security statement. In recent years, solver-based automatic tools and dedicated heuristic search algorithms have been extensively adopted to improve the accuracy and efficiency in cryptanalysis of block ciphers, where the cryptanalytic models are often transformed into MILP problems [5, 6] , SAT/SMT problems [7, 8] or CP problems [9, 10] . Automatic search technology has improved the analysis ability of block ciphers. The improvement and development of these automatic search technologies provide an inexhaustible source of thought for the design and analysis of block ciphers. However, these search technologies do not extract any new features that are not available manually.

Therefore, once optimal distinguishers are obtained, these automatic tools would exert less influence in improving attacks.

Recently, under the joint driven form of big data and the availability of computing hardware, deep learning [11, 12] has made remarkable progress and spread over almost every field of science and technology. Some researchers explored the feasibility of applying machine learning to the field of cryptography. In ASIACRYPT 1991, Rivest [13] made preliminary explorations of the possible connection between cryptography and machine learning, and some researchers applied machine learning in side channel analysis successfully, such as [14, 15] . However, few researchers focused on the application of machine learning to black box cryptanalysis, until the process of applying deep learning to black box cryptanalysis was accelerated by the remarkable work of Gohr [16] .

Deep learning algorithms can analyze data and learn effective patterns for predicting new samples. Based on this, Gohr trained a deep neural network using the labeled (labels 0 and 1) ciphertext pairs as training data, where the data with label 1 comes from the encrypted plaintext pair with fixed input difference, and the data with label 0 is a random number. The trained neural network then is used to distinguish between the real ciphertext pairs and random pairs. When his network is applied to Speck32/64, higher accuracy than the classical differential (CD) is achieved. Although the number of rounds using his network has not yet surpassed the number of rounds achieved by the most advanced technology, the neural distinguisher (ND) under the same number of rounds uses some information that the CD has not tapped.

More importantly, a potent key recovery attack is created by combining NDs with CDs and highly selective key search strategies. In essence, the NDs are too short to be used in key recovery and must be prepended with CDs to get the hybrid distinguishers (HDs). Making the resulting HDs usable in a key recovery attack requires better NDs or prepended CDs. Researchers have provided solutions from various angles. Benamira et al. [17] analyzed and explained the inner workings of Gohr's neural network and enhanced the accuracy of the NDs by creating batches of ciphertext inputs instead of pairs. Bao et al. [18] enhanced the CD's neutral bits and trained better NDs by investigating different neural networks, enabling key recovery attacks for the 13-round Speck32/64 and 16round Simon32/64.


## Our contribution:

• In this paper, we present (related-key) differentialbased neural distinguishers on Simon and Simeck block ciphers.

To better match our neural network and increase the accuracy of the neural distinguisher, we adopt the multiple ciphertext pairs (8 ciphertext pairs) to train the neural network fed with the data of form (∆ r L , ∆ r R , C l , C r , C l , C r , ∆ r- foot_0 R , p∆ r-2 R ). Fig. 1 shows a schematic representation of these nota-tions. Also, we employ the SE-ResNet network (Fig. 2 ) due to the success of ResNet on Speck [16] and SENet on Simon [18] , as well as their superior performance on classification tasks.

• We notice that the choice of the ND or connecting difference is critical to obtain the best hybrid distinguishers. Therefore, taking the performance of the differential-neural distinguisher of Simon32/64 as an entry point, we investigate the impact of input difference of the ND on the performance of the hybrid distinguishers to choose the proper input difference. As a result, the input difference (0,e i ) is a good choice to obtain hybrid distinguishers for Simon-like ciphers.

• Eventually, we build neural distinguishers for Simon32/64, Simon64/128, Simeck32/64 and Simeck64/128. The results are shown in Table 1 , which shows that we improve the accuracy of the distinguishers. Meanwhile, we successfully construct the related-key neural distinguishers against Simon32/64, Simon64/128, Simeck32/64 and Simeck64/128 for the first time.

In this paper, the experiment is conducted by Python 3.6.10 in Ubuntu 18.04. The models are implemented by Tensorflow 2.5.0. The experiment uses a server with Intel(R) Xeon(R) Gold 6248 CPU *4 with 2.50GHz, 512GB RAM, and NVIDIA Tesla T4 16GB. The source code is available on Github 1 .


## Organization.

Section 2 recalls Simon-like ciphers, (related-key) differential cryptanalysis and CNN network. Section 3 introduces improved (related-key) differential-based neural distinguishers, including the batches of ciphertext pairs with new data format, and the network architecture. Section 4 compares the performance of the hybrid distinguisher with different input difference. Section 5 gives the (relatedkey) differential-neural distinguishers for round-reduced Simon32/64 and Simon64/128. Section 6 provides the (related-key) differential-neural distinguishers for round-reduced Simeck32/64 and Simeck64/128. Section 7 concludes this paper.


## RELATED WORKS


## Notations

Table 2 presents the notations used in this paper.


## A Brief Description of Simon and Simeck Ciphers

Simon. The lightweight family of AND-RX block ciphers Simon was proposed by the National Security Agency (NSA) in 2013. It adopts the Feistel structure and the round function consists of bitwise AND ( ), bitwise XOR (⊕) and cyclic left shift γ bit (S γ ) operation composition. The designer provides ten versions, all marked as Simon2n/mn, where 2n represents the block size, mn represents the key length, n ∈ {16, 24, 32, 48, 64}, m ∈ {2, 3, 4}. The round function of Simon algorithm is defined as:

The round keys are generated using a linear key schedule through the K = (k m-1 , k m-2 , . . . , k 0 ). A more complete description can refer to paper [19] . Simeck. The Simeck family of lightweight block ciphers was designed by Yang et al. [20] , aiming at improving the hardware implementation cost of Simon. Simeck2n/4n denotes an instance with a 2n-bit block and a 4n-bit key for n ∈ {16, 24, 32}. The round function of Simeck algorithm is defined as:

Conversely, Simeck uses the non-linear key schedule which reuses the cipher's round function to generate the round keys. A more complete description can be found in [20] .


## Simon-like ciphers.

Iterated ciphers that use Simon's round function and generalize it to accept arbitrary rotational parameters are known as Simonlike ciphers (a, b, c).

The Simon-like function is then f a,b,c (x) = S a (x) S b (x) ⊕ S c (x), which the rotational parameters (a, b, c) are (8,1,2) and (5,0,1) for all Simon and Simeck versions, respectively.


## (Related-key) Differential Cryptanalysis

Differential cryptanalysis is a chosen-plaintext attack introduced by Biham and Shamir in [1] . It analyzes the effect of the difference of a plaintext pair on the difference of succeeding round outputs in an iterated cipher. Differential cryptanalysis is a widely used tool for the cryptanalysis of encryption algorithms and the development of new attacks due to its generality. Resistance to differential cryptanalysis became one of the basic criteria in the evaluation of the security of block ciphers.

Definition 2.1 (Difference). [1] Let X and X be two bit strings of length n, then the difference between X and X is defined as: ∆X = X ⊕ X .

Definition 2.2 (Differential Pair). [1] Let α, β be n-bit vectors, the difference value of the input pair (X, X ) of the block cipher is X ⊕ X = α, after rround of encryption, the difference value of the output pair (Y, Y ) is Y ⊕ Y = β, and let a round function f : F n 2 → F n 2 , then (α, β) is called an r-round differential pair of block cipher, where α is the input difference of round function f , β is the output difference of f . In particular, when r = 1, (α, β) characterizes the differential propagation characteristics of the round function f . For a specific cipher, the differential must be carefully selected to make the differential attack successful. This makes researchers need to study the internal process of the algorithm.

The basic method is to track a path passed by a high probability differential at different stages of encryption. This is called differential characteristics in cryptography and is defined as follows.

Definition 2.3 (Differential Characteristics). [1] Let X, X be n-bit vectors and β i be an n-bit constant. When the difference value of the input pair (X, X ) satisfies X ⊕ X = β 0 , the difference value of the intermediate state (Y i , Y i ) satisfies Y i ⊕ Y i = β i during the r-th round of encryption, where, 1 ≤ i ≤ r. Then, Ω = (β 1 , β 2 , . . . , β r ) can be named an r-round differential characteristic of an iterative block cipher.

For given differential characteristics, use the following definition to calculate its probability.

Definition 2.4. [1] The probability DP (Ω) corresponding to an r-round differential characteristic Ω = (β 1 , β 2 , . . . , β r ) of the iterative block cipher refers to the case where the input X and the round keys are independent and random distributed, when the differential value of the input pair (X, X ) is X ⊕ X = β 1 , in the i-round encryption process, the difference value of the intermediate state (Y i , Y i ) satisfies the probability of Y i ⊕ Y i = β i , where 1 ≤ i ≤ r. Under the above assumption, the probability of the differential characteristic is equal to the product of the differential propagation probabilities of each round, i.e.,:

When the input difference undergoes a linear operation, it will be propagated through the operation with probability 1, and the output difference is deterministic, such as XOR (⊕) and cyclic shift (≪ , ≫) in the ARX operation. When the input difference passes through a non-linear operation, the difference propagation is often probabilistic.

Related-key differential cryptanalysis was introduced by Biham in [21] . Unlike the single-key differentials that have differences only in the plaintexts, relatedkey differential distinguishers have differences in the master keys as well. It exploits the output differences given a pair of plaintexts P and P encrypted by a pair of related keys K and K , respectively. Relatedkeys differential cryptanalysis is also one of the basic criteria in the evaluation of the security of block ciphers, which has successfully attacked many block ciphers, such as [22] [23] [24] .


## Convolutional Neural Network

Convolutional neural network (CNN) is an important paradigm in deep learning. CNN is usually composed of the convolutional layer, non-linear layer, pooling layer and fully connected layer. According to the convolution dimension of the feature map, it can be divided into one-, two-, and three-dimensional convolutional neural network (i.e., 1D-CNN, 2D-CNN and 3D-CNN), where the 1D-CNN applies a convolution over a fixed (multi-)temporal input signal.

Convolution Layer (CONV). Convolution is the basic operation of CNN, and its main purpose is to extract features. The core task of CNN is to learn parameters to extract effective patterns. In the forward propagation, the training data will go through the convolution kernel with initial parameters to obtain the initial output. In the back propagation, a loss function will be applied to adjust the parameters to minimize the gap between the initial output and the target label. After several iterations, when the loss stabilizes, the training process will be finished. Note that in this paper we apply 1D-CNN, then the convolution layer can be denoted by Conv1D.

Non-linear layer. The main purpose of the nonlinear layer is to introduce non-linear characteristics into the system. The most common non-linear layer in a CNN network is the rectified linear unit (ReLU) function, defined as f (x) = max(0, x). Effectively, it removes negative values from an activation map by setting them to zero. It increases the nonlinear properties of the decision function and of the overall network without affecting the receptive fields of the convolution layer. Other functions are also used to increase nonlinearity, such as the sigmoid function. ReLU is often preferred to other functions because it trains the neural network several times faster without a significant penalty to generalization accuracy.

Fully connected layer (FC). The fully connected layer is generally located in the back layers of the network for performing the classification task. Usually, the input of the fully connected layer is the flatten feature map generated by convolution layer.

In addition, some functional layers may be used in CNN. For example, Batch Normalization (BN) can be applied after the convolution layer to reduce the internal covariate shift, which can effectively prevent the gradient disappearance problem and speed up network training.

Residual Network (ResNet) is one of the most representative CNNs, which was proposed by He et al. [25] in 2015. ResNet can train a deeper CNN model to achieve higher accuracy. The core idea is to establish "shortcuts (skip) connections" between the front layer and the back layer. It is composed of a series of residual blocks. A residual block can be expressed as:

It is divided into two parts: the direct mapping part and the residual part. F(x l ) is the residual part, which is generally composed of two or three convolution operations. The activation functions of ReLU and BN can be rearranged to create a variety of residual block variants.

Squeeze-and-Excitation Network (SENet) is a new network structure proposed by Hu et al. that won the first place in ILSVRC 2017 classification competition [26] . The "Squeeze-and-Excitation" (SE) block adaptively recalibrates channel-wise feature responses by explicitly modelling interdependencies between channels. It can be integrated into standard architectures by insertion after the non-linearity following each convolution. In this paper, SE block is used directly with the residual network, i.e., the SE-ResNet network.


## IMPROVED (RELATED-KEY) DIFFERENTIAL-BASED NEURAL DIS-TINGUISHERS


## Dateset: Multiple Ciphertext Pairs with

New Data Format Data plays a very important role in deep learning, data preparation is a fundamental step for deep learning model development. Some researchers explored the use of multiple ciphertext pairs to improve the performance of differential-based neural distinguishers [17, 27, 28] . Some researchers also performed additional transformations on each pair of ciphertexts before feeding them into the network.

Concretely, in Gohr's work, the n-round NDs fed with data of form (C l , C r , C l , C r ). Subsequently, Benamira et al. [17] conjected the first convolution layer of Gohr's neural network transforms the input (C l , C r , C l , C r ) into (C l ⊕ C l , C l ⊕ C l ⊕ C r ⊕ C r , C l ⊕ C r , C l ⊕ C r ) and a linear combination of those terms. In [28] , Hou et al. designed the NDs model with multiple output differences as a sample, i.e., the n-round NDs fed multiple pairs with data of form (C l ⊕C l , C r ⊕C r ) (∆ r L , ∆ r R ). In [18] , Bao et al. accepted the r-round NDs fed with data of form (C r , C r , ∆ r-1 R ), where

In this paper, we employ multiple ciphertext pairs with new data of form (∆ r L , ∆ r R , C l , C r , C l , C r , ∆ r-1 R , p∆ r-2 R ) to improve the performance of neural distinguishers (the reason for choosing this data format is given in Section 5.3). Then, the process of constructing a dataset can be described.

For the differential-neural distinguisher, first encrypt the s plaintext pairs ((P, P ) 1 , (P, P ) 2 , . . . , (P, P ) s ) with a random key to get the s ciphertext pairs. Then, use the s ciphertext pairs to get the data:

where the set (

Finally, splice Ω i and convert it into a string of binary as a sample, and each sample will be attached a label Y :

where ∆ p is a constant input difference. It examines how to select the ∆ p in Section 4. Unlike differential-neural distinguisher, which uses a random key K to encrypt the s plaintext pairs, related-key differential-neural distinguisher uses a pair of keys (K, K ) with a difference of ∆ k to encrypt the s plaintext pairs.

We construct the dataset based on the above steps and set s = 8. In the basic training process, the size of the training set is 2 × 10 7 , and the test set is 2 × 10 6 . Meanwhile, there is an independent key used for each sample. Therefore, the training set has 2 × 10 7 corresponding random keys, and the test set has 2 × 10 6 corresponding random keys.


## Network Architecture

A deep learning architecture is a multilayer stack of simple modules, most of which are subject to learning, and many of which compute non-linear input-output mappings. Each module in the stack transforms its input to increase both the selectivity and the invariance of the representation. With multiple non-linear layers, say a depth of 5 to 20, a system can implement extremely intricate functions of its inputs that are simultaneously sensitive to minute details.

Given the success of ResNet on Speck [16] and SENet on Simon [18] , as well as their superior performance on classification tasks, we use the SE-ResNet network. As shown in Fig. 2 , the network consists of three main components: input layer, iteration layer and predict layer. The input layer uses one Conv1D layer and two Dense layers to receive fixed length training data. In the iteration layer, use 5 SE-ResNet modules where each module contains two Conv1D layers and one SE block. To make the network learning more stable and alleviate the problem of gradient disappearance, a BN layer is applied after each Conv1D layer, and then followed by an activation layer with ReLU function. Finally, in predict layer, to make the data smoothly transform from the convolutional layer to the fully connected layer, we introduce a flatten layer to perform one-dimensional flattening of the data output from the convolutional layer. The fully connected layer consists of two Dense layers where each has 64 neurons and an output unit with only one neuron.

We set the batch size to 30000, cyclic learning rate l i = α + (n-i)mod(n+1) n • (β -α) with α = 0.0001, β = 0.003, n = 29 for epoch i, which is denoted as cyclic lr(30, 0.003, 0.0001). Adam [29] is used as the optimizer with mean squared error (MSE) loss function and L2 regularization parameterized by c = 0.00001. Each dataset is trained with 120 epochs for the basic training method. The accuracy, TPR, and TNR of the ND are the average results after 5 repetitions.


## COMPARING THE PERFORMANCE OF THE HYBRID DISTINGUISHER WITH DIFFERENT INPUT DIFFERENCE

In this section, we investigate the effect of input difference of the NDs on the performance of the hybrid distinguishers. Essentially, to be used in key-recovery, the NDs are too short such that they have to be prepended with classical differentials. Whether the resulting HDs can be used in a key-recovery attack depends on whether the input difference of NDs leads to better accuracy and, at the same time, leads to prepended CDs with high differential probability. Therefore, taking the performance of the hybrid distinguisher of Simon32/64 as an entry point, we investigate the issue in two phases. In the first stage, we study the performance of all input differences with Hamming weights of 1, 2, and 3 on the 11-round ND, and filter the input differences that can obtain a non-marginal advantage (accuracy above 0.50). Then study the performance of these filtered input differences on 12-round ND. In the second stage, we study the probability of the prepended CDs with these filtered input differences.


## The First Stage

Let HW(∆ p ) denote the Hamming weight of the input difference, then there are 32 + 496 + 4960 = 5488 input difference with HW(∆ p ) ≤ 3. Based on Section 3, traversing these input difference ∆ p with the batch size 30000 and cyclic lr(30, 0.003, 0.0001), we construct 11-round ND of Simon32/64, respectively. There are 128 input differences filtered, of which 48 have an accuracy between 0.51-0.52 and 80 have an accuracy between 0.54-0.56. Therefore, we mainly focus on the Input (None 1024) Reshape (None 8 128) Conv1D ks = 1 same filters = 64 Residual Blocks Flatten (None 512) re lu B N Output re lu B N re lu B N Conv1D ks = 3 same filters = 64 Conv1D ks = 3 same filters = 64 5-blocks (None 8 64) (None 8 64) SE Blocks Global pooling Dense Relu Dense Sigmoid Reshape Dense (None 8 64) re lu B N Dense (None 8 64) re lu B N Dense (None 128) re lu B N Dense (None 128) re lu B N Dense (None ) Sigmoid FIGURE 2: Network architecture proposed in this paper.

performance of these 80 input differences. The results with these 80 input differences are shown in Fig. 3 . It is discovered that 11-round ND with input difference ∆ p = (a, b) and input difference ∆ p = (a ≪ i, b ≪ i) have similar accuracy, for 0 ≤ i < 16. Thus, we only list one of these 16 input differences in Table 4 . Specifically, for HW(∆ p ) = 1, using the input difference (omit the 0x symbol):

(0000,0001), (0000,0002), (0000,0004), (0000,0008), (0000,0010), (0000,0020), (0000,0040), (0000,0080), (0000,0100), (0000,0200), (0000,0400), (0000,8000), (0000,1000), (0000,2000), (0000,4000), (0000,8000), can construct 11-round ND of Simon32/64 with an accuracy of about 0.561.

For HW(∆ p ) = 2, using the input difference:

(0001,0004), (0002,0008), (0004,0010), (0008,0020), (0010,0040), (0020,0080), (0040,0100), (0080,0200), (0100,0400), (0200,0800), (0400,1000), (0800,2000), (1000,4000), (2000,8000), (4000,0001), (8000,0002), can build 11-round ND of Simon32/64 with an accuracy of about 0.560. For HW(∆ p ) = 3, there are three sets of (a, b). Using the input difference:

(0001,0104), (0002,0208), (0004,0410), (0008,0820), (0010,1040), (0020,2080), (0040,4100), (0080,8200), (0100,0401), (0200,0802), (0400,1004), (0800,2008), (1000,4010), (2000,8020), (4000,0041), (8000,0082), can construct 11-round ND of Simon32/64 with an accuracy of about 0.560.

Using the input difference:

(0001,0006), (0002,000c), (0004,0018), (0008,0030), (0010,0060), (0020,00c0), (0040,0180), (0080,0300), (0100,0600), (0200,0c00), (0400,1800), (0800,3000), (1000,6000), (2000,c000), (4000,8001), (8000,0003), can obtain 11-round ND of Simon32/64 with an accuracy of about 0.560. Using the input difference:

(0001,4004), (0002,8008), (0004,0011), (0008,0022), (0010,0044), (0020,0088), (0040,0110), (0080,0220), (0100,0440), (0200,0880), (0400,1100), (0800,2200), (1000,4400), (2000,8800), (4000,1001), (8000,2002), can get 11-round ND of Simon32/64 with an accuracy of about 0.549. It can be found that the effect of the 16 input differeces (0x0001 ≪ i,0x4004 ≪ i) (0 ≤ i < 16) is slightly inferior to the other 64 (80 -16 = 64) input differeces for 11-round ND.

Then, with the input differences (0x0,0x1), (0x1,0x4),(0x1,0x104),(0x1,0x6),(0x1,0x4004) separately, we construct 12-round ND of Simon32/64 by using the basic training method. The results are shown in Table 3 . It shows the accuracy exceeds 0.50 except for the input difference (0x0,0x1) ((0x0,0x1) can get an accuracy of 0.5142 by using the staged training method). Therefore, a total of 64 input differences can make 12-round ND obtain non-marginal advantage by using the basic training method. Meanwhile, the


## The Second Stage

The NDs are prepended with 3 rounds of CDs in [18] , so we use 3 rounds prepended CDs as a benchmark to test the performance of the input differential filtered in the first stage. An SMT solver is used to determine the probability of prepended CDs. We first decide if a differential characteristic with probability p exists, then enumerate all differential characteristics with a probability of p. The results are presented in Table 4 . It can be seen that the probability of the 3 rounds prepended CDs with the input difference (0x0000 ≪ i,0x0001 ≪ i), 0 ≤ i < 16 (i.e., (0,e i )) are the highest, followed by 2-bit input differential (0x0001 ≪ i,0x0004 ≪ i), 0 ≤ i < 16, and the worst are

As a result, after these two steps of filtering, the input difference (0,e i ) is possibly the best option for hybrid distinguishers. Meanwhile, the input difference (0x0001 ≪ i,0x0004 ≪ i), 0 ≤ i < 16 is also a good choice. But we cannot yet give a clearer opinion on how much i is set. In this section, the NDs are trained using the basic training method and the staged training method. The training model is based on Section 3.


## Differential-Neural Distinguishers


## Simon32/64

Training using the basic scheme. Using the input difference (0x0000,0x0040), we build NDs against Simon32/64 cover to 9-, 10-, and 11-round with 0.9176, 0.6975, and 0.5609 accuracy, respectively. Using the input difference (0x0001,0x0004), we build 12-round ND with 0.5152 accuracy. Table 1 presents the results.

Note that for NDs fed with single ciphertext pairs, with multiple ciphertext pairs with the same label, one can directly obtain a combine-response distinguisher (CRD) using the formula (3) in [16] . Similar to the NDs fed with multiple ciphertext pairs, the CRDs' accuracy improves quickly with increasing the number of ciphertext pairs. Therefore, we compare the accuracy of NDs with CRDs under the number of ciphertext pairs with the same label. Compared with [18] , the accuracy of our NDs are improved.

Training using the Staged Training Method. We also use several stages of pre-training to train a 12round differential-neural distinguisher for Simon32/64. In the first stage, the best 10-round distinguisher is retained to recognize 9-round Simon32/64 with the input difference (0x0440,0x0100). The number of samples for training and for testing are 2 25 and 2 23 , respectively. The number of epochs is 30 and the learning rate is 10 -4 .

In the second stage, the best network of the first stage is retained to recognize 12-round Simon32/64 with the input difference (0x0000,0x0040). For this stage, 2 25 and 2 23 examples are freshly generated for training and testing, respectively. The learning rate is 10 -4 for 30 epochs.

Cyclical learning rates are also used for these training stages, the first and second stage both use a minimum learning rate of 0.0001 and a maximum of 0.001. All cycle lengths in these stages are set to 30 epochs. Eventually, the resulting ND achieves an accuracy of 0.5142.


## Simon64/128

Training using the basic scheme. Based on the input difference (0x00000000,0x00000040), the NDs reach 0.9181, 0.7117, 0.5722, and 0.5148 accuracy for 11-, 12-, 13-, and 14-round, respectively. As shown in Table 1 , the results are summarized.

Training using the Staged Training Method. The best 14-round distinguisher for Simon64/128 is trained using the staged training method.

In the first stage, the retained best 12-round distinguisher is trained and tested with 11-round 2 25 and 2 23 samples of Simon64/128 with the input difference (0x00000440,0x00000100). The number of epochs is 30 and the learning rate is 10 -4 . The learning rate scheduler used in this stage is cyclic lr(30, 0.001, 0.0001).

Then the best network from the first stage is trained in the second stage.

The number of examples for training and for testing are 2 25 and 2 23 , using 14-round Simon64/128 data with the input difference (0x00000000,0x00000040). This stage is done in 30 epochs with learning rate of 10 -4 . The learning rate scheduler used in this stage is cyclic lr(30, 0.001, 0.0001). Finally, the accuracy of the resulting ND is 0.5185.


## Related-key Differential-Neural Distinguishers

We use the basic training method to train the relatedkey differential-neural distinguishers. Based on the plaintext difference (0x0000,0x0040) and the key difference (0x0000,0x0000,0x0000,0x0040), we enjoy 1, 0.9604, 0.6477, and 0.5262 accuracy for 10-, 11-, 12-, and 13-round RKNDs against Simon32/64, respectively. Based on the plaintext difference (0x00000000,0x00000040) and the key difference (0x00000000,0x00000000,0x00000000,0x00000040), we build RKNDs cover to 12-, 13-, and 14-round with 0.9880, 0.8398, and 0.5788 accuracy for Simon64/128, respectively. To the best of our knowledge, this is the first successful application of the RKNDs against Simon-like ciphers.


## Experiment with Different Data Format

In order to improve the accuracy of the ND, we introduce a new data format (∆ r L , ∆ r R , C l , C r , C l , C r , ∆ r-1 R , p∆ r-2 R ) suitable for the network architecture in this paper. Here, we explain the reason for choosing this data format. We mainly compare the effect of the different data format on the performance of the network based on the experiment of 9-, 10-, and 11-round NDs for Simon32/64.

We use the basic method to train the 9-, 10-, and 11-round NDs based the input difference (0x0000,0x0040), batch size 30000, and cyclic lr(30, 0.003, 0.0001).

The results are presented in Table 5 .

It shows that the NDs using data formats of (C r , C r , ∆ r-1 R ), (∆ r L , ∆ r R , C l , C r , C l , C r , ∆ r-1 R ), (∆ r L , ∆ r R , C l , C r , C l , C r , ∆ r-1 R , p∆ r-2 R ) can achieve 11-round, and the accuracy with data format (∆ r L , ∆ r R , C l , C r , C l , C r , ∆ r-1 R , p∆ r-2 R ) is greater than others. This is the primary cause for using this data format in the paper.

Meanwhile, it is noted that the accuracy dropped when the p∆ r-2 R component was deleted from the data format (∆ r L , ∆ r R , C l , C r , C l , C r , ∆ r-1 R , p∆ r-2 R ), i.e., the neural network benefits from providing data p∆ r-2 R . In fact, p∆ r-2 R denotes the partial ∆ r-2 R , and it can be determined without the round key when the ciphertext pair is given.

It is important to note that this comparison is only to show that the data format used in this paper better matches the current network for better performance. Different results may occur when the network is changed.


## (RELATED-KEY) DIFFERENTIAL-NEURAL DISTINGUISHERS FOR ROUND-REDUCED SIMECK32/64 AND SIMECK64/128

Simeck is a lightweight block cipher family that combines the good design components of Simon and Speck to make it even more compact and efficient. In this section, we build NDs and RKNDs for roundreduced Simeck32/64 and Simeck64/128.


## Differential-Neural Distinguishers


## Simeck32/64

Training using the basic scheme. Using the input difference (0x0000,0x0040), we build NDs against Simeck32/64 cover to 9-, 10-, and 11-round with 0.9952, 0.7354, and 0.5646 accuracy, respectively. The results are presented in Table 1 .


## Training using the Staged Training Method.

A 12-round differential-neural distinguisher for Simeck32/64 is also obtained by utilizing several stages of pre-training.

The first stage selects the best 10-round distinguisher to recognize 9-round Simeck32/64 with the input difference (0x0140,0x0080).

Note that the most likely difference to appear three rounds after the input difference (0x0000,0x0040) is (0x0140,0x0080), and the probability is about 2 -4 .

It freshly generates 2 25 and 2 23 samples to train and test the distinguisher, respectively. This stage has 30 epochs and a learning rate of 10 -4 . The learning rate scheduler used in this stage is cyclic lr(30, 0.001, 0.0001).

The best network obtained from the first stage is retained to recognize 12-round Simeck32/64 with the input difference (0x0000,0x0040). The number of examples for training and for testing are 2 25 and 2 23 , respectively. The number of epochs is 30 and the learning rate is 10 -4 . The learning rate scheduler used in this stage is cyclic lr(30, 0.001, 0.0001). Lastly, the ND produced has an accuracy of 0.5146.


## Simeck64/128

Training using the basic scheme. Similarly, based on the input difference (0x00000000,0x00000040), the NDs reach accuracies of 0.9142, 0.7663, 0.6356, 0.5577, and 0.5202 for 14-, 15-, 16-, 17-, and 18-round, respectively. The results are shown in Table 1 .

Training using the Staged Training Method. We use the staged training method to obtain the best 18round distinguisher for Simeck64/128.

In the first stage, the retained best 16-round distinguisher is trained and tested with 15-round 2 25 and 2 23 samples of Simeck64/128 with the input difference (0x0000140,0x00000080). The number of epochs is 30 and the learning rate is 10 -4 .

Then the best network from the first stage is trained in the second stage. The number of freshly generated examples for training and for testing are 2 25 and 2 23 , using 18-round Simeck64/128 data with the input difference (0x00000000,0x00000040). This stage is done in 30 epochs with learning rate of 10 -4 .

Cyclical learning rates are used for these training stages, the first and second stage both use a minimum learning rate of 0.0001 and a maximum of 0.001. All cycle lengths in these stages are set to 30 epochs. As a final result, the ND produced has an accuracy of 0.5218.


## Related-key Differential-Neural Distinguishers

For related-key differential-neural distinguishers, based on the input difference (0x0000,0x0040) and the key difference (0x0000,0x0000,0x0000,0x0040), it covers to 13-, 14-, and 15-round with 0.9950, 0.6679 and 0.5467 accuracy for Simeck32/64, respectively. For Simeck64/128, based on the input difference (0x00000000,0x00000040) and the key difference (0x00000000,0x00000000,0x00000000,0x00000040), it cover to 18-, 19-, 20-, 21-, and 22-round with 0.9066, 0.7558, 0.6229, 0.5519, and 0.5180 accuracy for Simeck64/128, respectively. It can be seen the gap of RKNDs for Simon and Simeck is obvious, and Simon's key-expansion algorithm offers better resistance. This is consistent with the conclusion that Lu et al. get using rotational-XOR cryptanalysis in [30] .


## CONCLUSION

In this paper, we provide an in-depth analysis of the (related-key) differential-neural distinguishers for Simon and Simeck ciphers.

We adopt the multiple ciphertext pairs with data of the form (∆ r L , ∆ r R , C l , C r , C l , C r , ∆ r-1 R , p∆ r-2 R ) fed to the neural network to improve the accuracy of the neural distinguisher. Meanwhile, we investigate the impact of input difference on the performance of the hybrid distinguishers to select the appropriate input difference. For Simon32/64, Simon64/128, Simeck32/64 and Simeck64/128, we construct the (related-key) differential-neural distinguishers with higher accuracy. It is undeniable that there are many factors that can affect the performance of neural distinguishers. This paper explores its impact on the performance of neural distinguishers from the perspective of data format and input difference. In the future, we plan to further explore ways that can improve the performance of neural networks from multiple dimensions, such as using methods of feature engineering to extract more essential features of the training data and so on.

> 12 FIGURE 1 :FIGURE 2 : FIGURE 1: Notation of the data format.

> 3 FIGURE 3 : FIGURE 3: The input differences with Hamming weights of 1, 2, and 3 that can obtain a clear non-marginal advantage (accuracy above 0.52) on the 11-round ND of Simon32/64 with 8 ciphertext pairs as a sample.

> 1 TABLE 1 : The comparison of (related-key) neural distinguishers attacks on Simon32/64, Simon64/128, Simeck32/64, and Simeck64/128 with 8 ciphertext pairs as a sample. ND: neural distinguisher, RKND: related-key neural distinguisher. TPR: True Positive Rate, TNR: True Negative Rate. †: For NDs fed with single ciphertext pairs, the combine-response distinguisher (CRD) obtained for the case of 8 ciphertext pairs. *: This neural distinguisher is trained using the staged training method.

> 2 TABLE 2 : The notations used throughout the paper

> 3 TABLE 3 : Experiment with Different Input Difference of 12-round ND for Simon32/64 with 8 ciphertext pairs as a sample.

> 4 TABLE 4 : Comparing the performance of the hybrid distinguisher with different input difference for Simon32/64. The NDs is 11-round. The number on the arrow represents the probability of the differential characteristic from the input difference to the output difference, and the number of characteristics * .

> 5 TABLE 5 : Experiment with different data format of 9-, 10-, and 11-round NDs for Simon32/64. The best NDs for 9-, 10-, and 11-round are shown shaded.

## Acknowledgements

This work was supported in part by the National Key Research and Development Program of China [No. 2021YFB3100800 ]; and the State Key Laboratory of Information Security [ 2020-MS-02 ]; and the National Natural Science Foundation of China [grant numbers 62172427 , 61872379 , 61702537 ]; and the Academy of Finland [grant number 331883 ]; and Postgraduate Scientific Research Innovation Project of Hunan Province [grant number CX20220016 ].

## References

1. b0: Eli Biham, Adi Shamir. "Differential cryptanalysis of DES-like cryptosystems". Journal of Cryptology. 1991-01. DOI: 10.1007/bf00630563
2. b1: Mitsuru Matsui. "Linear Cryptanalysis Method for DES Cipher". Lecture Notes in Computer Science. 1994. DOI: 10.1007/3-540-48285-7_33
3. b2: Lars Knudsen, David Wagner. "Integral Cryptanalysis". Lecture Notes in Computer Science. 2002. DOI: 10.1007/3-540-45661-9_9
4. b3: Andrey Bogdanov, Vincent Rijmen. "Linear hulls with correlation zero and linear cryptanalysis of block ciphers". Designs, Codes and Cryptography. 2012-05-30. DOI: 10.1007/s10623-012-9697-z
5. b4: Nicky Mouha, Qingju Wang, Dawu Gu, Bart Preneel. "Differential and Linear Cryptanalysis Using Mixed-Integer Linear Programming". Lecture Notes in Computer Science. 2012. DOI: 10.1007/978-3-642-34704-7_5
6. b5: Siwei Sun, Lei Hu, Peng Wang, Kexin Qiao, Xiaoshuang Ma, Ling Song. "Automatic Security Evaluation and (Related-key) Differential Characteristic Search: Application to SIMON, PRESENT, LBlock, DES(L) and Other Bit-Oriented Block Ciphers". Lecture Notes in Computer Science. 2014. DOI: 10.1007/978-3-662-45611-8_9
7. b6: N Mouha, B Preneel. "A proof that the arx cipher salsa20 is secure against differential cryptanalysis". IACR Cryptol. 2013
8. b7: Stefan Kölbl, Gregor Leander, Tyge Tiessen. "Observations on the SIMON Block Cipher Family". Lecture Notes in Computer Science. 2015. DOI: 10.1007/978-3-662-47989-6_8
9. b8: M Minier, C Solnon, J Reboul. "Solving a symmetric key cryptographic problem with constraint programming". Workshop of the CP 2014 Conference 13
10. b9: David Gerault, Marine Minier, Christine Solnon. "Constraint Programming Models for Chosen Key Differential Cryptanalysis". Lecture Notes in Computer Science. 2016. DOI: 10.1007/978-3-319-44953-1_37
11. b10: Yann Lecun, Yoshua Bengio, Geoffrey Hinton. "Deep learning". Nature. 2015-05-27. DOI: 10.1038/nature14539
12. b11: Yoshua Bengio, Yann Lecun, Geoffrey Hinton. "Deep learning for AI". Communications of the ACM. 2021-06-21. DOI: 10.1145/3448250
13. b12: Ronald L Rivest. "Cryptography and machine learning". Lecture Notes in Computer Science. 1993. DOI: 10.1007/3-540-57332-1_36
14. b13: Houssem Maghrebi, Thibault Portigliatti, Emmanuel Prouff. "Breaking Cryptographic Implementations Using Deep Learning Techniques". Lecture Notes in Computer Science. 2016. DOI: 10.1007/978-3-319-49445-6_1
15. b14: Gabriel Hospodar, Benedikt Gierlichs, Elke De Mulder, Ingrid Verbauwhede, Joos Vandewalle. "Machine learning in side-channel analysis: a first study". Journal of Cryptographic Engineering. 2011-10-27. DOI: 10.1007/s13389-011-0023-x
16. b15: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
17. b16: Adrien Benamira, David Gerault, Thomas Peyrin, Quan Quan Tan. "A Deeper Look at Machine Learning-Based Cryptanalysis". Lecture Notes in Computer Science. 2021. DOI: 10.1007/978-3-030-77870-5_28
18. b17: Zhenzhen Bao, Jian Guo, Meicheng Liu, Li Ma, Yi Tu. "Enhancing Differential-Neural Cryptanalysis". Lecture Notes in Computer Science. 2022. DOI: 10.1007/978-3-031-22963-3_11
19. b18: Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks, Louis Wingers. "The SIMON and SPECK lightweight block ciphers". Proceedings of the 52nd Annual Design Automation Conference. 2015-06-07. DOI: 10.1145/2744769.2747946
20. b19: Gangqiang Yang, Bo Zhu, Valentin Suder, Mark D Aagaard, Guang Gong. "The Simeck Family of Lightweight Block Ciphers". Lecture Notes in Computer Science. 2015. DOI: 10.1007/978-3-662-48324-4_16
21. b20: Eli Biham. "New types of cryptanalytic attacks using related keys". Journal of Cryptology. 1994-12. DOI: 10.1007/bf00203965
22. b21: Goce Jakimoski, Yvo Desmedt. "Related-Key Differential Cryptanalysis of 192-bit Key AES Variants". Lecture Notes in Computer Science. 2004. DOI: 10.1007/978-3-540-24654-1_15
23. b22: Youngdai Ko, Seokhie Hong, Wonil Lee, Sangjin Lee, Ju-Sung Kang. "Related Key Differential Attacks on 27 Rounds of XTEA and Full-Round GOST". Lecture Notes in Computer Science. 2004. DOI: 10.1007/978-3-540-25937-4_19
24. b23: Alex Biryukov, Ivica Nikolić. "Automatic Search for Related-Key Differential Characteristics in Byte-Oriented Block Ciphers: Application to AES, Camellia, Khazad and Others". Lecture Notes in Computer Science. 2010. DOI: 10.1007/978-3-642-13190-5_17
25. b24: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun. "Deep Residual Learning for Image Recognition". 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2016-06. DOI: 10.1109/cvpr.2016.90
26. b25: Jie Hu, Li Shen, Gang Sun. "Squeeze-and-Excitation Networks". 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2018-06. DOI: 10.1109/cvpr.2018.00745
27. b26: Yi Chen, Yantian Shen, Hongbo Yu, Sitong Yuan. "A New Neural Distinguisher Considering Features Derived From Multiple Ciphertext Pairs". The Computer Journal. 2022-03-11. DOI: 10.1093/comjnl/bxac019
28. b27: Zezhou Hou, Jiongjiong Ren, Shaozhen Chen. "Improve Neural Distinguishers of SIMON and SPECK". Security and Communication Networks. 2021-12-31. DOI: 10.1155/2021/9288229
29. b28: D P Kingma, J Ba, Adam. A method for stochastic optimization
30. b29: Jinyu Lu, Yunwen Liu, Tomer Ashur, Chao Li. "On the Effect of the Key-Expansion Algorithm in Simon-like Ciphers". The Computer Journal. 2021-07-05. DOI: 10.1093/comjnl/bxab082
