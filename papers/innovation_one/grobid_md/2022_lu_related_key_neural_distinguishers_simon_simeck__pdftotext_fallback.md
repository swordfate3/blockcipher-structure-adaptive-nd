# Improved Related-Key Differential-Based Neural Distinguishers for Simon and Simeck Block Ciphers

**Source PDF:** `2022_lu_related_key_neural_distinguishers_simon_simeck.pdf`

**Extraction:** `pdftotext -layout` fallback copy because the GROBID title slug is shared with the ePrint version and would otherwise overwrite one Markdown file.

## Extracted Text

```text
Improved (Related-key)
                                                                  Differential-based Neural
                                                                Distinguishers for SIMON and
                                                                   SIMECK Block Ciphers
                                                         Jinyu Lu1,2,3 , Guoqiang Liu1,2,4∗ , Bing Sun1,2,3 , Chao Li1,2,3 and
                                                                                     Li Liu5,6
arXiv:2201.03767v3 [cs.CR] 15 Nov 2022




                                                         1
                                                           College of Liberal Arts and Sciences, National University of Defense Technology, Hunan,
                                                                                            Changsha 410073, China
                                                         2
                                                           Hunan Engineering Research Center of Commercial Cryptography Theory and Technology
                                                                                 Innovation, Hunan, Changsha 410073, China
                                                                  3
                                                                    State Key Laboratory of Cryptology, P.O.Box 5159, Beijing 100878, China
                                                            4
                                                              State Key Laboratory of Information Security (Institute of Information Engineering,
                                                                              Chinese Academy of Sciences, Beijing 100093, China
                                                            5
                                                              College of Systems Engineering, National University of Defense Technology, Hunan,
                                                                                            Changsha 410073, China
                                                         6
                                                           Center for Machine Vision and Signal Analysis, University of Oulu, Oulu 90570, Finland
                                                                                      Email: liuguoqiang87@hotmail.com


                                                       In CRYPTO 2019, Gohr made a pioneering attempt and successfully applied deep
                                                       learning to the differential cryptanalysis against NSA block cipher Speck32/64,
                                                       achieving higher accuracy than the pure differential distinguishers. By its very
                                                       nature, mining effective features in data plays a crucial role in data-driven
                                                       deep learning. In this paper, in addition to considering the integrity of the
                                                       information from the training data of the ciphertext pair, domain knowledge
                                                       about the structure of differential cryptanalysis is also considered into the training
                                                       process of deep learning to improve the performance. Meanwhile, taking the
                                                       performance of the differential-neural distinguisher of Simon32/64 as an entry
                                                       point, we investigate the impact of input difference on the performance of the
                                                       hybrid distinguishers to choose the proper input difference. Eventually, we
                                                       improve the accuracy of the neural distinguishers of Simon32/64, Simon64/128,
                                                       Simeck32/64, and Simeck64/128. We also obtain related-key differential-based
                                                       neural distinguishers on round-reduced versions of Simon32/64, Simon64/128,
                                                                      Simeck32/64, and Simeck64/128 for the first time.

                                                         Keywords: Deep Learning; (Related-key) Differential Distinguisher; Simon; Simeck; Input
                                                                                               Difference



                                         1.   INTRODUCTION                                              improve the accuracy and efficiency in cryptanalysis
                                                                                                        of block ciphers, where the cryptanalytic models are
                                         The security analysis of many cryptographic primitives         often transformed into MILP problems [5,6], SAT/SMT
                                         (such as pseudo-random number generators, hash                 problems [7,8] or CP problems [9,10]. Automatic search
                                         functions, etc.) is usually attributed to attacks on           technology has improved the analysis ability of block
                                         the underlying block ciphers. Various cryptanalytic            ciphers. The improvement and development of these
                                         methods have been proposed over the past few                   automatic search technologies provide an inexhaustible
                                         decades, including differential cryptanalysis [1], linear      source of thought for the design and analysis of
                                         cryptanalysis [2], integral cryptanalysis [3], zero-           block ciphers. However, these search technologies do
                                         correlation linear cryptanalysis [4], etc. A block cipher      not extract any new features that are not available
                                         must be able to resist all known cryptanalysis to              manually.     Therefore, once optimal distinguishers
                                         obtain a strong security statement. In recent years,           are obtained, these automatic tools would exert less
                                         solver-based automatic tools and dedicated heuristic           influence in improving attacks.
                                         search algorithms have been extensively adopted to                Recently, under the joint driven form of big
data and the availability of computing hardware,                    tions. Also, we employ the SE-ResNet network
deep learning [11, 12] has made remarkable progress                 (Fig. 2) due to the success of ResNet on Speck [16]
and spread over almost every field of science                       and SENet on Simon [18], as well as their superior
and technology.        Some researchers explored the                performance on classification tasks.
feasibility of applying machine learning to the field of     •      We notice that the choice of the ND or
cryptography. In ASIACRYPT 1991, Rivest [13] made                   connecting difference is critical to obtain the
preliminary explorations of the possible connection                 best hybrid distinguishers. Therefore, taking the
between cryptography and machine learning, and some                 performance of the differential-neural distinguisher
researchers applied machine learning in side channel                of Simon32/64 as an entry point, we investigate
analysis successfully, such as [14, 15]. However, few               the impact of input difference on the performance
researchers focused on the application of machine                   of the hybrid distinguishers to choose the proper
learning to black box cryptanalysis, until the process of           input difference.        As a result, the input
applying deep learning to black box cryptanalysis was               difference (0,ei ) is a good choice to obtain hybrid
accelerated by the remarkable work of Gohr [16].                    distinguishers for Simon-like ciphers.
   Deep learning algorithms can analyze data and learn       •      Eventually, we build neural distinguishers for
effective patterns for predicting new samples. Based                Simon32/64, Simon64/128, Simeck32/64 and
on this, Gohr trained a deep neural network using the               Simeck64/128. The results are shown in Table 1,
labeled (labels 0 and 1) ciphertext pairs as training               which shows that we improve the accuracy of
data, where the data with label 1 comes from the                    the distinguishers. Meanwhile, we successfully
encrypted plaintext pair with fixed input difference,               construct the related-key neural distinguishers
and the data with label 0 is a random number. The                   against Simon32/64, Simon64/128, Simeck32/64
trained neural network then is used to distinguish                  and Simeck64/128 for the first time.
between the real ciphertext pairs and random pairs.
When his network is applied to Speck32/64, higher              In this paper, the experiment is conducted by Python
accuracy than the classical differential (CD) is achieved.   3.6.10 in Ubuntu 18.04. The models are implemented
Although the number of rounds using his network has          by Tensorflow 2.5.0. The experiment uses a server with
not yet surpassed the number of rounds achieved by           Intel(R) Xeon(R) Gold 6248 CPU *4 with 2.50GHz,
the most advanced technology, the neural distinguisher       512GB RAM, and NVIDIA Tesla T4 16GB. The source
(ND) under the same number of rounds uses some               code is available on Github1 .
information that the CD has not tapped.
   More importantly, a potent key recovery attack            Organization. Section 2 recalls Simon-like ciphers,
is created by combining NDs with CDs and highly              (related-key) differential cryptanalysis and CNN net-
selective key search strategies. In essence, the NDs         work. Section 3 introduces improved (related-key)
are too short to be used in key recovery and must be         differential-based neural distinguishers, including the
prepended with CDs to get the hybrid distinguishers          batches of ciphertext pairs with new data format, and
(HDs). Making the resulting HDs usable in a key              the network architecture. Section 4 compares the
recovery attack requires better NDs or prepended             performance of the hybrid distinguisher with differ-
CDs. Researchers have provided solutions from various        ent input difference. Section 5 gives the (related-
angles. Benamira et al. [17] analyzed and explained          key) differential-neural distinguishers for round-reduced
the inner workings of Gohr’s neural network and              Simon32/64 and Simon64/128. Section 6 provides
enhanced the accuracy of the NDs by creating batches         the (related-key) differential-neural distinguishers for
of ciphertext inputs instead of pairs. Bao et al. [18]       round-reduced Simeck32/64 and Simeck64/128. Sec-
enhanced the CD’s neutral bits and trained better NDs        tion 7 concludes this paper.
by investigating different neural networks, enabling key
recovery attacks for the 13-round Speck32/64 and 16-         2.     RELATED WORKS
round Simon32/64.                                            2.1.     Notations

Our contribution:                                            Table 2 presents the notations used in this paper.

•   In this paper, we present (related-key) differential-    2.2.     A Brief Description of Simon and Simeck
    based neural distinguishers on Simon and Simeck                   Ciphers
    block ciphers.            To better match our neural
                                                             Simon. The lightweight family of AND-RX block
    network and increase the accuracy of the neu-
                                                             ciphers Simon was proposed by the National Security
    ral distinguisher, we adopt the multiple ci-
                                                             Agency (NSA) in 2013. It adopts the Feistel structure
    phertext pairs (8 ciphertext pairs) to train
                                                             and the round function consists of bitwise AND
    the neural network fed with the data of form
                                                             (⊙), bitwise XOR (⊕) and cyclic left shift γ bit
    (∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1   r−2
                                        R , p∆R ). Fig. 1
    shows a schematic representation of these nota-               1 https://github.com/JIN-smile/Improved-Related-key-Differential-b
TABLE 1: The comparison of (related-key) neural distinguishers attacks on Simon32/64, Simon64/128,
Simeck32/64, and Simeck64/128 with 8 ciphertext pairs as a sample. ND: neural distinguisher, RKND: related-key
neural distinguisher. TPR: True Positive Rate, TNR: True Negative Rate. †: For NDs fed with single ciphertext pairs,
the combine-response distinguisher (CRD) obtained for the case of 8 ciphertext pairs. *: This neural distinguisher
is trained using the staged training method.

               Attack
   Ciphers               Round             Input difference           Accuracy       TPR         TNR       Source
               Model
                           9†             (0x0,0x40)                   0.8940       0.8728       0.9152      [18]
                            9             (0x0,0x40)                   0.9176       0.9052       0.9299        5
                          10*†            (0x0,0x40)                   0.6865       0.6817       0.6912      [18]
                           10             (0x0,0x40)                   0.6975       0.6662       0.7287        5
                ND
                          11*†            (0x0,0x40)                   0.5568       0.5419       0.5717      [18]
    Simon                  11             (0x0,0x40)                   0.5609       0.5366       0.5852        5
    32/64                  12              (0x1,0x4)                   0.5152       0.4799       0.5505
                                                                                                              5
                          12*             (0x0,0x40)                   0.5142       0.5029       0.5254
                           10     (0x0,0x40),(0x0,0x0,0x0,0x40)           1            1            1
                           11     (0x0,0x40),(0x0,0x0,0x0,0x40)        0.9604       0.9639       0.9569
               RKND                                                                                           5
                           12     (0x0,0x40),(0x0,0x0,0x0,0x40)        0.6477       0.6518       0.6435
                           13     (0x0,0x40),(0x0,0x0,0x0,0x40)        0.5262       0.5437       0.5081
                            9             (0x0,0x40)                   0.9952       0.9989       0.9914
                           10             (0x0,0x40)                   0.7354       0.7207       0.7501
                ND                                                                                            6
                          11              (0x0,0x40)                   0.5646       0.5356       0.5936
   Simeck
                          12*             (0x0,0x40)                   0.5146       0.4770       0.5522
    32/64
                          13      (0x0,0x40),(0x0,0x0,0x0,0x40)        0.9950       0.9990       0.9910
               RKND       14      (0x0,0x40),(0x0,0x0,0x0,0x40)        0.6679       0.6425       0.6933       6
                          15      (0x0,0x40),(0x0,0x0,0x0,0x40)        0.5467       0.5173       0.5762
                           11             (0x0,0x40)                   0.9181       0.9045       0.9318
                          12              (0x0,0x40)                   0.7117       0.6705       0.7530
                ND        13              (0x0,0x40)                   0.5722       0.5230       0.6215       5
    Simon                  14             (0x0,0x40)                   0.5148       0.4697       0.5600
    64/128                14*             (0x0,0x40)                   0.5185       0.4663       0.5707
                          12      (0x0,0x40),(0x0,0x0,0x0,0x40)        0.9880       0.9894       0.9865
               RKND        13     (0x0,0x40),(0x0,0x0,0x0,0x40)        0.8398       0.8389       0.8408       5
                           14     (0x0,0x40),(0x0,0x0,0x0,0x40)        0.5788       0.5894       0.5682
                           14             (0x0,0x40)                   0.9142       0.8914       0.9371
                          15              (0x0,0x40)                   0.7663       0.6981       0.8345
                          16              (0x0,0x40)                   0.6356       0.5245       0.7467
                ND                                                                                            6
                          17              (0x0,0x40)                   0.5577       0.4301       0.6853
                           18             (0x0,0x40)                   0.5202       0.3917       0.6486
   Simeck
                          18*             (0x0,0x40)                   0.5218       0.3927       0.6510
   64/128
                          18      (0x0,0x40),(0x0,0x0,0x0,0x40)        0.9066       0.8837       0.9295
                           19     (0x0,0x40),(0x0,0x0,0x0,0x40)        0.7558       0.6845       0.8270
               RKND        20     (0x0,0x40),(0x0,0x0,0x0,0x40)        0.6229       0.5104       0.7354       6
                           21     (0x0,0x40),(0x0,0x0,0x0,0x40)        0.5519       0.4248       0.6790
                           22     (0x0,0x40),(0x0,0x0,0x0,0x40)        0.5180       0.3906       0.6455
 TABLE 2: The notations used throughout the paper                                              Definition 2.2 (Differential Pair). [1] Let α, β be
                                                                                            n-bit vectors, the difference value of the input pair
  Notation                   Description
                                                                                            (X, X ′ ) of the block cipher is X ⊕ X ′ = α, after r-
  x = (xn−1 , . . . , x0 )   Binary vector of n bits; xi is the bit in position i with x0
                             the least significant one.                                     round of encryption, the difference value of the output
  x⊙y                        Bitwise AND between x and y.                                   pair (Y, Y ′ ) is Y ⊕ Y ′ = β, and let a round function
  x⊕y                        Bitwise XOR between x and y.
  xky                        Concatenation of x and y.                                      f : Fn2 → Fn2 , then (α, β) is called an r-round differential
  x ≪ γ, S γ (x)             Circular left shift of x by γ bits.                            pair of block cipher, where α is the input difference
  x ≫ γ, S −γ (x)            Circular right shift of x by γ bits.
  (Pl , Pr , Pl′ , Pr′ )     A set of plaintext pairs with left and right branches where    of round function f , β is the output difference of
                             P = Pl k Pr and P ′ = Pl′ k Pr′ .
  (Cl , Cr , Cl′ , Cr′ )     A set of ciphertext pairs with left and right branches where
                                                                                            f . In particular, when r = 1, (α, β) characterizes
                             C = Cl k Cr and C ′ = Cl′ k Cr′ .                              the differential propagation characteristics of the round
                                                                                            function f .
                                                                                               For a specific cipher, the differential must be carefully
(S γ ) operation composition. The designer provides
                                                                                            selected to make the differential attack successful. This
ten versions, all marked as Simon2n/mn, where 2n
                                                                                            makes researchers need to study the internal process
represents the block size, mn represents the key length,
                                                                                            of the algorithm. The basic method is to track
n ∈ {16, 24, 32, 48, 64}, m ∈ {2, 3, 4}. The round
                                                                                            a path passed by a high probability differential at
function of Simon algorithm is defined as:
                                                                                            different stages of encryption. This is called differential
         f8,1,2 (x) = S 8 (x) ⊙ S 1 (x) ⊕ S 2 (x) .                                         characteristics in cryptography and is defined as follows.
                                       

   The round keys are generated using a linear key                                             Definition 2.3 (Differential Characteristics). [1]
schedule through the K = (km−1 , km−2 , . . . , k0 ). A                                     Let X, X ′ be n-bit vectors and βi be an n-bit constant.
more complete description can refer to paper [19].                                          When the difference value of the input pair (X, X ′ )
Simeck. The Simeck family of lightweight block                                              satisfies X ⊕ X ′ = β0 , the difference value of the
ciphers was designed by Yang et al. [20], aiming at                                         intermediate state (Yi , Yi′ ) satisfies Yi ⊕ Yi′ = βi during
improving the hardware implementation cost of Simon.                                        the r-th round of encryption, where, 1 ≤ i ≤ r.
Simeck2n/4n denotes an instance with a 2n-bit block                                         Then, Ω = (β1 , β2 , . . . , βr ) can be named an r-round
and a 4n-bit key for n ∈ {16, 24, 32}. The round                                            differential characteristic of an iterative block cipher.
function of Simeck algorithm is defined as:                                                   For given differential characteristics, use the following
                                                                                            definition to calculate its probability.
         f5,0,1 (x) = S 5 (x) ⊙ S 0 (x) ⊕ S 1 (x) .
                                       
                                                                                               Definition 2.4. [1] The probability DP (Ω)
   Conversely, Simeck uses the non-linear key schedule                                      corresponding to an r-round differential characteristic
which reuses the cipher’s round function to generate the                                    Ω = (β1 , β2 , . . . , βr ) of the iterative block cipher refers
round keys. A more complete description can be found                                        to the case where the input X and the round keys
in [20].                                                                                    are independent and random distributed, when the
Simon-like ciphers.          Iterated ciphers that use                                      differential value of the input pair (X, X ′ ) is X ⊕ X ′ =
Simon’s round function and generalize it to accept                                          β1 , in the i-round encryption process, the difference
arbitrary rotational parameters are known as Simon-                                         value of the intermediate state (Yi , Yi′ ) satisfies the
like ciphers (a, b, c).   The Simon-like      function is                                   probability of Yi ⊕ Yi′ = βi , where 1 ≤ i ≤ r. Under
then fa,b,c (x) = S a (x) ⊙ S b (x) ⊕ S c (x), which the
                                    
                                                                                            the above assumption, the probability of the differential
rotational parameters (a, b, c) are (8,1,2) and (5,0,1) for                                 characteristic is equal to the product of the differential
all Simon and Simeck versions, respectively.                                                propagation probabilities of each round, i.e.,:
                                                                                                          r
2.3.        (Related-key) Differential Cryptanalysis                                                      Y
                                                                                             DP (Ω) =           P r(βi−1 → βi )
Differential cryptanalysis is a chosen-plaintext attack                                                   i=1
introduced by Biham and Shamir in [1]. It analyzes                                                        Yr
                                                                                                              {Yi−1 |f (Yi−1 ) ⊕ f (Yi−1 ⊕ βi−1 ) = βi }
the effect of the difference of a plaintext pair on the                                               =                                                  .
                                                                                                                                  2n
difference of succeeding round outputs in an iterated                                                     i=1

cipher. Differential cryptanalysis is a widely used
                                                                                              When the input difference undergoes a linear
tool for the cryptanalysis of encryption algorithms and
                                                                                            operation, it will be propagated through the operation
the development of new attacks due to its generality.
                                                                                            with probability 1, and the output difference is
Resistance to differential cryptanalysis became one of
                                                                                            deterministic, such as XOR (⊕) and cyclic shift (≪
the basic criteria in the evaluation of the security of
                                                                                            , ≫) in the ARX operation. When the input difference
block ciphers.
                                                                                            passes through a non-linear operation, the difference
  Definition 2.1 (Difference). [1] Let X and X ′ be                                         propagation is often probabilistic.
two bit strings of length n, then the difference between                                      Related-key differential cryptanalysis was introduced
X and X ′ is defined as: ∆X = X ⊕ X ′ .                                                     by Biham in [21]. Unlike the single-key differentials
that have differences only in the plaintexts, related-         network training.
key differential distinguishers have differences in the           Residual Network (ResNet) is one of the most
master keys as well. It exploits the output differences        representative CNNs, which was proposed by He et
given a pair of plaintexts P and P ′ encrypted by a            al. [25] in 2015. ResNet can train a deeper CNN model
pair of related keys K and K ′ , respectively. Related-        to achieve higher accuracy. The core idea is to establish
keys differential cryptanalysis is also one of the basic       “shortcuts (skip) connections” between the front layer
criteria in the evaluation of the security of block ciphers,   and the back layer. It is composed of a series of residual
which has successfully attacked many block ciphers,            blocks. A residual block can be expressed as:
such as [22–24].
                                                                                   xl+1 = xl + F (xl ).
2.4.   Convolutional Neural Network                            It is divided into two parts: the direct mapping part
Convolutional neural network (CNN) is an                       and the residual part. F (xl ) is the residual part,
important paradigm in deep learning. CNN is usually            which is generally composed of two or three convolution
composed of the convolutional layer, non-linear layer,         operations. The activation functions of ReLU and BN
pooling layer and fully connected layer. According             can be rearranged to create a variety of residual block
to the convolution dimension of the feature map, it            variants.
can be divided into one-, two-, and three-dimensional             Squeeze-and-Excitation Network (SENet) is a
convolutional neural network (i.e., 1D-CNN, 2D-CNN             new network structure proposed by Hu et al. that
and 3D-CNN), where the 1D-CNN applies a convolution            won the first place in ILSVRC 2017 classification
over a fixed (multi-)temporal input signal.                    competition [26]. The “Squeeze-and-Excitation” (SE)
   Convolution Layer (CONV). Convolution is the                block adaptively recalibrates channel-wise feature
basic operation of CNN, and its main purpose is to             responses by explicitly modelling interdependencies
extract features. The core task of CNN is to learn             between channels. It can be integrated into standard
parameters to extract effective patterns. In the forward       architectures by insertion after the non-linearity
propagation, the training data will go through the             following each convolution. In this paper, SE block is
convolution kernel with initial parameters to obtain the       used directly with the residual network, i.e., the SE-
initial output. In the back propagation, a loss function       ResNet network.
will be applied to adjust the parameters to minimize
the gap between the initial output and the target label.       3.     IMPROVED         (RELATED-KEY)
After several iterations, when the loss stabilizes, the               DIFFERENTIAL-BASED NEURAL DIS-
training process will be finished. Note that in this paper            TINGUISHERS
we apply 1D-CNN, then the convolution layer can be
                                                               3.1.    Dateset: Multiple Ciphertext Pairs with
denoted by Conv1D.
                                                                       New Data Format
   Non-linear layer. The main purpose of the non-
linear layer is to introduce non-linear characteristics        Data plays a very important role in deep learning, data
into the system. The most common non-linear layer              preparation is a fundamental step for deep learning
in a CNN network is the rectified linear unit (ReLU)           model development. Some researchers explored the use
function, defined as f (x) = max(0, x). Effectively,           of multiple ciphertext pairs to improve the performance
it removes negative values from an activation map              of differential-based neural distinguishers [17, 27,
by setting them to zero. It increases the nonlinear            28].       Some researchers also performed additional
properties of the decision function and of the overall         transformations on each pair of ciphertexts before
network without affecting the receptive fields of the          feeding them into the network.               Concretely, in
convolution layer. Other functions are also used to            Gohr’s work, the n-round NDs fed with data of form
increase nonlinearity, such as the sigmoid function.           (Cl , Cr , Cl′ , Cr′ ). Subsequently, Benamira et al. [17]
ReLU is often preferred to other functions because it          conjected the first convolution layer of Gohr’s neural
trains the neural network several times faster without         network transforms the input (Cl , Cr , Cl′ , Cr′ ) into (Cl ⊕
a significant penalty to generalization accuracy.              Cl′ , Cl ⊕ Cl′ ⊕ Cr ⊕ Cr′ , Cl ⊕ Cr , Cl′ ⊕ Cr′ ) and a linear
   Fully connected layer (FC). The fully connected             combination of those terms. In [28], Hou et al. designed
layer is generally located in the back layers of the           the NDs model with multiple output differences as a
network for performing the classification task. Usually,       sample, i.e., the n-round NDs fed multiple pairs with
the input of the fully connected layer is the flatten          data of form (Cl ⊕Cl′ , Cr ⊕Cr′ ) , (∆rL , ∆rR ). In [18], Bao
feature map generated by convolution layer.                    et al. accepted the r-round NDs fed with data of form
   In addition, some functional layers may be used in          (Cr , Cr′ , ∆r−1
                                                                             R ), where ∆R
                                                                                             r−1
                                                                                                 = ((Cr ≪ 8) ⊙ (Cr ≪
CNN. For example, Batch Normalization (BN) can                 1) ⊕ (Cr ≪ 2) ⊕ Cl ) ⊕ ((Cr′ ≪ 8) ⊙ (Cr′ ≪ 1) ⊕ (Cr′ ≪
be applied after the convolution layer to reduce the           2) ⊕ Cl′ ) for Simon ciphers.
internal covariate shift, which can effectively prevent           In this paper,             we employ multiple ci-
the gradient disappearance problem and speed up                phertext         pairs    with    new     data      of    form
(∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1   r−2
                                    R , p∆R ) to          improve       each module contains two Conv1D layers and one SE
the performance of neural distinguishers (the reason                    block. To make the network learning more stable and
for choosing this data format is given in Section 5.3).                 alleviate the problem of gradient disappearance, a BN
Then, the process of constructing a dataset can be                      layer is applied after each Conv1D layer, and then
described.                                                              followed by an activation layer with ReLU function.
  For the differential-neural distinguisher, first encrypt              Finally, in predict layer, to make the data smoothly
the s plaintext pairs ((P, P ′ )1 , (P, P ′ )2 , . . . , (P, P ′ )s )   transform from the convolutional layer to the fully
with a random key to get the s ciphertext pairs. Then,                  connected layer, we introduce a flatten layer to perform
use the s ciphertext pairs to get the data:                             one-dimensional flattening of the data output from the
                                                                        convolutional layer. The fully connected layer consists
          (∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1   r−2 1
                                              R , p∆R ) ,               of two Dense layers where each has 64 neurons and an
          (∆L , ∆R , Cl , Cr , Cl , Cr , ∆R , p∆r−2
             r     r               ′     ′    r−1       2
                                                    R ) ,               output unit with only one neuron.
                                     ..                                    We set the batch size to 30000, cyclic learning rate
                                      .
          (∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1   r−2 s               li = α + (n−i)mod(n+1)     · (β − α) with α = 0.0001,
                                              R , p∆R ) .                                 n
                                                                        β = 0.003, n = 29 for epoch i, which is denoted as
where the set (∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1   r−2 i           cyclic lr(30, 0.003, 0.0001). Adam [29] is used as the
                                                  R , p∆R ) of
row i is denoted by Ω .i                                                optimizer with mean squared error (MSE) loss function
  Finally, splice Ωi and convert it into a string of binary             and L2 regularization parameterized by c = 0.00001.
as a sample, and each sample will be attached a label                   Each dataset is trained with 120 epochs for the basic
Y:                                                                      training method. The accuracy, TPR, and TNR of the
                       (                                                ND are the average results after 5 repetitions.
     1    2       s
                         1, if P i ⊕ (P ′ )i = ∆p , 1 ≤ i ≤ s,
Y Ω ||Ω · · · ||Ω =
                          0,                                  else.     4.   COMPARING THE PERFORMANCE OF
                                                                             THE HYBRID DISTINGUISHER WITH
where ∆p is a constant input difference. It examines                         DIFFERENT INPUT DIFFERENCE
how to select the ∆p in Section 4.
   Unlike differential-neural distinguisher, which uses                 In this section, we investigate the effect of input differ-
a random key K to encrypt the s plaintext pairs,                        ence on the performance of the hybrid distinguishers.
related-key differential-neural distinguisher uses a pair               Essentially, to be used in key-recovery, the NDs are too
of keys (K, K ′ ) with a difference of ∆k to encrypt the                short such that they have to be prepended with clas-
s plaintext pairs.                                                      sical differentials. Whether the resulting HDs can be
   We construct the dataset based on the above steps                    used in a key-recovery attack depends on whether the
and set s = 8. In the basic training process, the                       input difference of NDs leads to better accuracy and,
size of the training set is 2 × 107 , and the test set is               at the same time, leads to prepended CDs with high
2 × 106 . Meanwhile, there is an independent key used                   differential probability.
for each sample. Therefore, the training set has 2 × 107                   Therefore, taking the performance of the hybrid
corresponding random keys, and the test set has 2 × 106                 distinguisher of Simon32/64 as an entry point, we
corresponding random keys.                                              investigate the issue in two phases. In the first stage,
                                                                        we study the performance of all input differences with
3.2.    Network Architecture                                            Hamming weights of 1, 2, and 3 on the 11-round
                                                                        ND, and filter the input differences that can obtain a
A deep learning architecture is a multilayer stack of                   non-marginal advantage (accuracy above 0.50). Then
simple modules, most of which are subject to learning,                  study the performance of these filtered input differences
and many of which compute non-linear input-output                       on 12-round ND. In the second stage, we study the
mappings. Each module in the stack transforms its                       probability of the prepended CDs with these filtered
input to increase both the selectivity and the invariance               input differences.
of the representation. With multiple non-linear layers,
say a depth of 5 to 20, a system can implement                          The First Stage
extremely intricate functions of its inputs that are
simultaneously sensitive to minute details.                                Let HW(∆p ) denote the Hamming weight of the input
   Given the success of ResNet on Speck [16] and SENet                  difference, then there are 32 + 496 + 4960 = 5488 input
on Simon [18], as well as their superior performance                    difference with HW(∆p ) ≤ 3. Based on Section 3,
on classification tasks, we use the SE-ResNet network.                  traversing these input difference ∆p with the batch
As shown in Fig. 2, the network consists of three main                  size 30000 and cyclic lr(30, 0.003, 0.0001), we construct
components: input layer, iteration layer and predict                    11-round ND of Simon32/64, respectively. There are
layer. The input layer uses one Conv1D layer and two                    128 input differences filtered, of which 48 have an
Dense layers to receive fixed length training data. In                  accuracy between 0.51-0.52 and 80 have an accuracy
the iteration layer, use 5 SE-ResNet modules where                      between 0.54-0.56. Therefore, we mainly focus on the
                                                                                 ‫݌‬ο௥ିଶ
                                                                                   ோ   ൌ ሺ‫ܽ ڗ ܣ‬ሻ ٖ ሺ‫ܾ ڗ ܣ‬ሻ ْ ሺ‫ܿ ڗ ܣ‬ሻ۩‫ܥ‬௥ ۩ሺ‫ܣ‬Ԣ ‫ܽ ڗ‬ሻ ٖ ሺ‫ܣ‬Ԣ ‫ܾ ڗ‬ሻ ْ ሺ‫ܣ‬Ԣ ‫ܿ ڗ‬ሻ۩‫ܥ‬௥ᇱ
                              ο௥ିଶ  ௥ିଵ  ௥ିଵ
                               ௅ ൌ οோ ൌ ‫ܥ‬௥   ْ ሺ‫ܥ‬௥௥ିଵ ሻԢ                         ‫ܥ‬௥௥ିଶ ൌ ሺሺ‫݇۩ܣ‬௥ ሻ ‫ܽ ڗ‬ሻ ٖ ሺሺ‫݇۩ܣ‬௥ ሻ ‫ܾ ڗ‬ሻ ْ ሺሺ‫݇۩ܣ‬௥ ሻ ‫ܿ ڗ‬ሻ۩‫ܥ‬௥ ۩݇௥ିଵ
                                                                                 ሺ‫ܥ‬௥௥ିଶ ሻԢ ൌ ሺሺ‫ܣ‬Ԣ۩݇௥ ሻ ‫ܽ ڗ‬ሻ ٖ ሺሺ‫ܣ‬Ԣ۩݇௥ ሻ ‫ܾ ڗ‬ሻ ْ ሺሺ‫ܣ‬Ԣ۩݇௥ ሻ ‫ܿ ڗ‬ሻ۩‫ܥ‬௥ᇱ ۩݇௥ିଵ

                                                                   <<< a
                                                                                                          ۨ                          ۩
                                                                   <<< b
                                                                   <<< c                                                             ۩
                                                                                                                                     ۩            ݇௥ିଵ



                                                                                                   ο௥ିଵ
                                                                                                    ோ   ൌ ‫ܥ‬௥௥ିଵ ْ ሺ‫ܥ‬௥௥ିଵ ሻԢ
                                      ο௥ିଵ  ௥         ᇱ
                                       ௅ ൌ οோ ൌ ‫ܥ‬௥ ْ ‫ܥ‬௥                                            ‫ܥ‬௥௥ିଵ ൌ ሺ‫ܥ‬௥ ‫ܽ ڗ‬ሻ ٖ ሺ‫ܥ‬௥ ‫ܾ ڗ‬ሻ ْ ሺ‫ܥ‬௥ ‫ܿ ڗ‬ሻ۩‫ܥ‬௟ ۩݇௥ ‫݇۩ܣ ؜‬௥
                                                                                                   ሺ‫ܥ‬௥௥ିଵ ሻԢ ൌ ሺ‫ܥ‬௥ᇱ ‫ܽ ڗ‬ሻ ٖ ሺ‫ܥ‬௥ᇱ ‫ܾ ڗ‬ሻ ْ ሺ‫ܥ‬௥ᇱ ‫ܿ ڗ‬ሻ۩‫ܥ‬௟ᇱ ۩݇௥ ‫ܣ ؜‬Ԣ۩݇௥

                                                                   <<< a
                                                                                                          ۨ                          ۩
                                                                   <<< b
                                                                   <<< c                                                             ۩
                                                                                                                                     ۩            ݇௥



                                          ο௥௅ ൌ ‫ܥ‬௟ ْ ‫ܥ‬௟ᇱ                                                                     ο௥ோ ൌ ‫ܥ‬௥ ْ ‫ܥ‬௥ᇱ


                                                             FIGURE 1: Notation of the data format.

                             Conv1D
                              ks = 1
                               same
                           filters = 64
     Input                                                   Dense                    Dense                    Residual Blocks   Flatten        Dense                 Dense             Dense Sigmoid Output

             Reshape
                                                   B re                   B re                     B re                                                  B re                   B re
                                          Ă
                       Ă




                                                                                                                    Ă




                                                   N lu                   N lu                     N lu                                                  N lu                   N lu


   (None1024)     (None8128)    (None864)             (None864)           (None864)                   (None864)   (None512) (None128)                 (None128)          (None)


                                                                                                                                                        SE Blocks
                                                             Conv1D                                         Conv1D
                                                              ks = 3                                         ks = 3                                  Global pooling
                                                               same                                           same                                  Reshape
                                                           filters = 64                                   filters = 64                                   Dense


                                                                                  B           re                                 B         re             Relu
                                                                     Ă




                                                                                                      Ă



                                                                                                                         Ă
                                                     Ă




                                                                                  N           lu                                 N         lu
                                                                                                                                                         Dense

                                                                                                                                                         Sigmoid



                                                                                                               5-blocks


                                               FIGURE 2: Network architecture proposed in this paper.


performance of these 80 input differences. The results                                                            (0000,1000), (0000,2000), (0000,4000), (0000,8000),
with these 80 input differences are shown in Fig. 3.
                                                                                                              can construct 11-round ND of Simon32/64 with an
   It is discovered that 11-round ND with input
                                                                                                              accuracy of about 0.561.
difference ∆p = (a, b) and input difference ∆′p = (a ≪
                                                                                                                For HW(∆p ) = 2, using the input difference:
i, b ≪ i) have similar accuracy, for 0 ≤ i < 16. Thus,
we only list one of these 16 input differences in Table 4.                                                        (0001,0004), (0002,0008), (0004,0010), (0008,0020),
Specifically, for HW(∆p ) = 1, using the input difference                                                         (0010,0040), (0020,0080), (0040,0100), (0080,0200),
(omit the 0x symbol):                                                                                             (0100,0400), (0200,0800), (0400,1000), (0800,2000),
                                                                                                                  (1000,4000), (2000,8000), (4000,0001), (8000,0002),
  (0000,0001), (0000,0002), (0000,0004), (0000,0008),
  (0000,0010), (0000,0020), (0000,0040), (0000,0080),                                                         can build 11-round ND of Simon32/64 with an
  (0000,0100), (0000,0200), (0000,0400), (0000,8000),                                                         accuracy of about 0.560.
FIGURE 3: The input differences with Hamming weights of 1, 2, and 3 that can obtain a clear non-marginal
advantage (accuracy above 0.52) on the 11-round ND of Simon32/64 with 8 ciphertext pairs as a sample.


  For HW(∆p ) = 3, there are three sets of (a, b). Using    TABLE 3: Experiment with Different Input Difference
the input difference:                                       of 12-round ND for Simon32/64 with 8 ciphertext pairs
                                                            as a sample.
 (0001,0104), (0002,0208), (0004,0410), (0008,0820),
 (0010,1040), (0020,2080), (0040,4100), (0080,8200),           Cipher Input Difference       Acc      TPR      TNR
 (0100,0401), (0200,0802), (0400,1004), (0800,2008),
 (1000,4010), (2000,8020), (4000,0041), (8000,0082),                 (0x0000,0x0001) 0.5004          0.1149    0.8857
                                                                     (0x0001,0x0004) 0.5152          0.4799    0.5505
can construct 11-round ND of Simon32/64 with an                Simon
                                                                     (0x0001,0x0104) 0.5151          0.4901    0.5401
accuracy of about 0.560.                                       32/64
                                                                     (0x0001,0x0006) 0.5152          0.4852    0.5453
  Using the input difference:
                                                                     (0x0001,0x4004) 0.5135          0.4331    0.5940
  (0001,0006), (0002,000c), (0004,0018), (0008,0030),
  (0010,0060), (0020,00c0), (0040,0180), (0080,0300),
  (0100,0600), (0200,0c00), (0400,1800), (0800,3000),
  (1000,6000), (2000,c000), (4000,8001), (8000,0003),
                                                            input differential (0x1,0x4) and (0x1,0x6) performed
can obtain 11-round ND of Simon32/64 with an                the best, with an accuracy of 0.5152.
accuracy of about 0.560.
  Using the input difference:                               The Second Stage
 (0001,4004), (0002,8008), (0004,0011), (0008,0022),
                                                              The NDs are prepended with 3 rounds of CDs in [18],
 (0010,0044), (0020,0088), (0040,0110), (0080,0220),
                                                            so we use 3 rounds prepended CDs as a benchmark to
 (0100,0440), (0200,0880), (0400,1100), (0800,2200),
                                                            test the performance of the input differential filtered in
 (1000,4400), (2000,8800), (4000,1001), (8000,2002),
                                                            the first stage. An SMT solver is used to determine
can get 11-round ND of Simon32/64 with an accuracy          the probability of prepended CDs. We first decide if
of about 0.549.                                             a differential characteristic with probability p exists,
   It can be found that the effect of the 16 input          then enumerate all differential characteristics with a
differeces (0x0001 ≪ i,0x4004 ≪ i) (0 ≤ i < 16)             probability of p. The results are presented in Table 4.
is slightly inferior to the other 64 (80 − 16 = 64) input   It can be seen that the probability of the 3 rounds
differeces for 11-round ND.                                 prepended CDs with the input difference (0x0000 ≪
   Then, with the input differences (0x0,0x1),              i,0x0001 ≪ i), 0 ≤ i < 16 (i.e., (0,ei )) are the
(0x1,0x4),(0x1,0x104),(0x1,0x6),(0x1,0x4004)                highest, followed by 2-bit input differential (0x0001
separately, we construct 12-round ND of Simon32/64          ≪ i,0x0004 ≪ i), 0 ≤ i < 16, and the worst are
by using the basic training method. The results are         (0x0001 ≪ i,0x4004 ≪ i), 0 ≤ i < 16.
shown in Table 3. It shows the accuracy exceeds 0.50          As a result, after these two steps of filtering, the
except for the input difference (0x0,0x1) ((0x0,0x1)        input difference (0,ei ) is possibly the best option for
can get an accuracy of 0.5142 by using the staged train-    hybrid distinguishers. Meanwhile, the input difference
ing method). Therefore, a total of 64 input differences     (0x0001 ≪ i,0x0004 ≪ i), 0 ≤ i < 16 is also a good
can make 12-round ND obtain non-marginal advantage          choice. But we cannot yet give a clearer opinion on how
by using the basic training method. Meanwhile, the          much i is set.
TABLE 4: Comparing the performance of the hybrid distinguisher with different input difference for Simon32/64.
The NDs is 11-round. The number on the arrow represents the probability of the differential characteristic
                                                                                                         from   the
                                                                                           (0011,0040)     2−8 (#20)
input difference to the output difference, and the number of characteristics. For example:                −−−−−−→
                                                                                                    ...
(0000,0001) means that when the input differences are (0000,0001) etc. and the output difference is (0000,0001),
there are 20 characteristics with a probability of 2−8 for 3-round Simon32/64. And these input differences in the
prepended CDs are the smallest Hamming weight in these characteristics.

      HW(∆p )           ∆p         ND’s     ND’s      ND’s              Prepended CDs (3-round)
                                   Acc      TPR       TNR
                                                                                    −8             
                                                                   (0011,0040)         2 (#20) 
                                                                                      −−−−−−→ 
                                                                              ... 
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                    (0010,0146)         2−9
                                                                                            (#4)
                                                                                                    
                                                                                                    
                                                                                       −−−−−→ 
                                                                                                    
                                                                               ...
                                                                                                    
                                                                                                    
                                                                                 −10               
         1-bit     (0000,0001)     0.5607   0.5407   0.5807      (0011,0040)        2     (#232)      (0000,0001)
                                                                                   −−−−−−−→ 
                                                                           ...                     
                                                                                                    
                                                                                                    
                                                                 (0011,0040)        2−11 (#352) 
                                                                                                    
                                                                                   −−−−−−−→ 
                                                                                                    
                                                                           ...
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                               ...
                                                                                                    
                                                                                     −8            
                                                                    (0040,0111)         2 (#4) 
                                                                                       −−−−−→ 
                                                                               ... 
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                   (0140,0511)
                                                                                                    
                                                                                       2 (#10) 
                                                                                        −9
                                                                                      −−−−−−→ 
                                                                                                    
                                                                              ... 
                                                                                                    
                                                                                                    
                                                                                                    
         2-bit     (0001,0004)     0.5602   0.5059   0.6145       (1040,0101)        2 −10
                                                                                           (#72)      (0001,0004)
                                                                                    −−−−−−−→ 
                                                                            ...                    
                                                                                                    
                                                                                                    
                                                                 (1060,0101)        2−11 (#124) 
                                                                                                    
                                                                                   −−−−−−−→ 
                                                                                                    
                                                                           ...
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                               ...
                                                                                                    
                                                                                    −10            
                                                                   (0040,0111)         2    (#4) 
                                                                                      −−−−−−→ 
                                                                              ... 
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                  (0140,0110)        2 −11
                                                                                           (#48) 
                                                                                                    
                                                                                    −−−−−−−→ 
                                                                                                    
                                                                            ... 
                                                                                                    
                                                                                                    
                                                                                                    
                   (0001,0104)     0.5601   0.5024   0.6179       (1040,0101)        2 −12
                                                                                           (#80)      (0001,0104)
                                                                                    −−−−−−−→ 
                                                                            ...                    
                                                                                                    
                                                                                                    
                                                                 (0200,4201)        2−13 (#620) 
                                                                                                    
                                                                                   −−−−−−−→ 
                                                                                                    
                                                                           ...
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                               ...
                                                                                                    
                                                                                    −10            
                                                                   (0040,0111)         2    (#4) 
                                                                                      −−−−−−→ 
                                                                              ... 
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                   (0140,0511)
                                                                                                    
                                                                                       2−11
                                                                                            (#8)   
                                                                                      −−−−−−→ 
                                                                              ... 
                                                                                                    
                                                                                                    
                                                                                                    
         3-bit     (0001,0006)     0.5597   0.4972   0.6221       (1040,0101)        2 −12
                                                                                           (#72)      (0001,0006)
                                                                                    −−−−−−−→ 
                                                                            ... 
                                                                                                    
                                                                                                    
                                                                                                    
                                                                 (1060,0101)        2−13 (#296) 
                                                                                                    
                                                                                   −−−−−−−→ 
                                                                                                    
                                                                           ...
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                               ...
                                                                                                    
                                                                                    −12            
                                                                   (4044,0101)         2    (#80) 
                                                                                      −−−−−−−→ 
                                                                              ... 
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                  (4064,0101)        2 −13
                                                                                           (#344) 
                                                                                                    
                                                                                                    
                                                                                    −−−−−−−→
                   (0001,4004)     0.5495   0.4433   0.6557                 ...                       (0001,4004)
                                                                 (0144,0140)        2−14 (#1072) 
                                                                                                    
                                                                                                    
                                                                                   −−−−−−−−→ 
                                                                           ...
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                ...
                                                                                                    
5.     (RELATED-KEY)      DIFFERENTIAL-                       Training using the Staged Training Method. The
       NEURAL     DISTINGUISHERS   FOR                        best 14-round distinguisher for Simon64/128 is trained
       ROUND-REDUCED SIMON32/64 AND                           using the staged training method.
       SIMON64/128                                               In the first stage, the retained best 12-round
                                                              distinguisher is trained and tested with 11-round 225
In this section, the NDs are trained using the basic          and 223 samples of Simon64/128 with the input
training method and the staged training method. The           difference (0x00000440,0x00000100). The number
training model is based on Section 3.                         of epochs is 30 and the learning rate is 10−4 . The
                                                              learning rate scheduler used in this stage is cyclic
5.1.    Differential-Neural Distinguishers                    lr(30, 0.001, 0.0001).
                                                                 Then the best network from the first stage is
Simon32/64                                                    trained in the second stage.         The number of
                                                              examples for training and for testing are 225 and
Training using the basic scheme. Using the input
                                                              223 , using 14-round Simon64/128 data with the input
difference (0x0000,0x0040), we build NDs against
                                                              difference (0x00000000,0x00000040). This stage is
Simon32/64 cover to 9-, 10-, and 11-round with 0.9176,
                                                              done in 30 epochs with learning rate of 10−4 . The
0.6975, and 0.5609 accuracy, respectively. Using the
                                                              learning rate scheduler used in this stage is cyclic
input difference (0x0001,0x0004), we build 12-round
                                                                lr(30, 0.001, 0.0001). Finally, the accuracy of the
ND with 0.5152 accuracy. Table 1 presents the results.
                                                              resulting ND is 0.5185.
   Note that for NDs fed with single ciphertext pairs,
with multiple ciphertext pairs with the same label, one
can directly obtain a combine-response distinguisher
                                                              5.2.     Related-key            Differential-Neural              Distin-
(CRD) using the formula (3) in [16]. Similar to the
                                                                       guishers
NDs fed with multiple ciphertext pairs, the CRDs’
accuracy improves quickly with increasing the number          We use the basic training method to train the related-
of ciphertext pairs. Therefore, we compare the accuracy       key differential-neural distinguishers. Based on the
of NDs with CRDs under the number of ciphertext pairs         plaintext difference (0x0000,0x0040) and the key
with the same label. Compared with [18], the accuracy         difference (0x0000,0x0000,0x0000,0x0040), we enjoy
of our NDs are improved.                                      1, 0.9604, 0.6477, and 0.5262 accuracy for 10-, 11-
                                                              , 12-, and 13-round RKNDs against Simon32/64,
Training using the Staged Training Method. We                 respectively.
also use several stages of pre-training to train a 12-           Based       on      the      plaintext   difference
round differential-neural distinguisher for Simon32/64.       (0x00000000,0x00000040) and the key difference
In the first stage, the best 10-round distinguisher is        (0x00000000,0x00000000,0x00000000,0x00000040),
retained to recognize 9-round Simon32/64 with the             we build RKNDs cover to 12-, 13-, and 14-round with
input difference (0x0440,0x0100). The number of               0.9880, 0.8398, and 0.5788 accuracy for Simon64/128,
samples for training and for testing are 225 and 223 ,        respectively. To the best of our knowledge, this is
respectively. The number of epochs is 30 and the              the first successful application of the RKNDs against
learning rate is 10−4 .                                       Simon-like ciphers.
   In the second stage, the best network of the first stage
is retained to recognize 12-round Simon32/64 with the         5.3.     Experiment with Different Data Format
input difference (0x0000,0x0040). For this stage, 225
and 223 examples are freshly generated for training and       In order to improve the accuracy of the
testing, respectively. The learning rate is 10−4 for 30       ND,        we      introduce          a      new        data          format
epochs.                                                       (∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1
                                                                                                  R    , p∆ r−2
                                                                                                            R    )      suitable        for
   Cyclical learning rates are also used for these training   the network architecture in this paper. Here, we ex-
stages, the first and second stage both use a minimum         plain the reason for choosing this data format. We
learning rate of 0.0001 and a maximum of 0.001. All           mainly compare the effect of the different data for-
cycle lengths in these stages are set to 30 epochs.           mat on the performance of the network based on
Eventually, the resulting ND achieves an accuracy of          the experiment of 9-, 10-, and 11-round NDs for
0.5142.                                                       Simon32/64.
                                                                 We use the basic method to train the 9-, 10-
Simon64/128                                                   , and 11-round NDs based the input difference
                                                              (0x0000,0x0040), batch size 30000, and cyclic
Training using the basic scheme. Based on the                 lr(30, 0.003, 0.0001).            The results are presented in
input difference (0x00000000,0x00000040), the NDs             Table 5.
reach 0.9181, 0.7117, 0.5722, and 0.5148 accuracy for            It shows that the NDs using data formats of
11-, 12-, 13-, and 14-round, respectively. As shown in        (Cr , Cr′ , ∆r−1
                                                                           R ),                  (∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1
                                                                                                                                      R ),
Table 1, the results are summarized.                          (∆L , ∆R , Cl , Cr , Cl , Cr , ∆r−1
                                                                  r     r              ′     ′
                                                                                                  R    , p∆ r−2
                                                                                                            R    )     can         achieve
11-round, and the accuracy with data format                       in this stage is cyclic lr(30, 0.001, 0.0001). Lastly, the
(∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1    r−2
                                    R , p∆R ) is greater than     ND produced has an accuracy of 0.5146.
others. This is the primary cause for using this data
format in the paper.                                              Simeck64/128
  Meanwhile, it is noted that the accuracy dropped
when the p∆r−2         component was deleted from the data        Training using the basic scheme. Similarly, based
                  R
format (∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1   r−2              on the input difference (0x00000000,0x00000040),
                                           R , p∆R ), i.e., the
neural network benefits from providing data p∆r−2                 the NDs reach accuracies of 0.9142, 0.7663, 0.6356,
                                                        R . In
fact, p∆r−2       denotes the partial ∆r−2                        0.5577, and 0.5202 for 14-, 15-, 16-, 17-, and 18-round,
           R                                 R , and it can be
determined without the round key when the ciphertext              respectively. The results are shown in Table 1.
pair is given.
                                                                  Training using the Staged Training Method. We
  It is important to note that this comparison is
                                                                  use the staged training method to obtain the best 18-
only to show that the data format used in this
                                                                  round distinguisher for Simeck64/128.
paper better matches the current network for better
                                                                     In the first stage, the retained best 16-round
performance. Different results may occur when the
                                                                  distinguisher is trained and tested with 15-round 225
network is changed.
                                                                  and 223 samples of Simeck64/128 with the input
                                                                  difference (0x0000140,0x00000080). The number of
6.     (RELATED-KEY)     DIFFERENTIAL-                            epochs is 30 and the learning rate is 10−4 .
       NEURAL    DISTINGUISHERS   FOR                                Then the best network from the first stage is trained
       ROUND-REDUCED SIMECK32/64 AND                              in the second stage. The number of freshly generated
       SIMECK64/128                                               examples for training and for testing are 225 and 223 ,
Simeck is a lightweight block cipher family that                  using 18-round Simeck64/128 data with the input
combines the good design components of Simon and                  difference (0x00000000,0x00000040). This stage is
Speck to make it even more compact and efficient.                 done in 30 epochs with learning rate of 10−4 .
In this section, we build NDs and RKNDs for round-                   Cyclical learning rates are used for these training
reduced Simeck32/64 and Simeck64/128.                             stages, the first and second stage both use a minimum
                                                                  learning rate of 0.0001 and a maximum of 0.001. All
6.1.    Differential-Neural Distinguishers                        cycle lengths in these stages are set to 30 epochs. As a
                                                                  final result, the ND produced has an accuracy of 0.5218.
Simeck32/64

Training using the basic scheme. Using the input
                                                                  6.2.    Related-key      Differential-Neural        Distin-
difference (0x0000,0x0040), we build NDs against
                                                                          guishers
Simeck32/64 cover to 9-, 10-, and 11-round with
0.9952, 0.7354, and 0.5646 accuracy, respectively. The            For related-key differential-neural distinguishers, based
results are presented in Table 1.                                 on the input difference (0x0000,0x0040) and the key
                                                                  difference (0x0000,0x0000,0x0000,0x0040), it covers
Training using the Staged Training Method.                        to 13-, 14-, and 15-round with 0.9950, 0.6679 and 0.5467
A 12-round differential-neural distinguisher for                  accuracy for Simeck32/64, respectively.
Simeck32/64 is also obtained by utilizing several                    For Simeck64/128, based on the input difference
stages of pre-training.                                           (0x00000000,0x00000040) and the key difference
   The first stage selects the best 10-round distinguisher        (0x00000000,0x00000000,0x00000000,0x00000040),
to recognize 9-round Simeck32/64 with the input                   it cover to 18-, 19-, 20-, 21-, and 22-round with
difference (0x0140,0x0080).         Note that the most            0.9066, 0.7558, 0.6229, 0.5519, and 0.5180 accuracy for
likely difference to appear three rounds after the input          Simeck64/128, respectively. It can be seen the gap
difference (0x0000,0x0040) is (0x0140,0x0080), and                of RKNDs for Simon and Simeck is obvious, and Si-
the probability is about 2−4 .                                    mon’s key-expansion algorithm offers better resistance.
   It freshly generates 225 and 223 samples to train              This is consistent with the conclusion that Lu et al.
and test the distinguisher, respectively. This stage              get using rotational-XOR cryptanalysis in [30].
has 30 epochs and a learning rate of 10−4 . The
learning rate scheduler used in this stage is cyclic
                                                                  7.     CONCLUSION
lr(30, 0.001, 0.0001).
   The best network obtained from the first stage is              In this paper, we provide an in-depth analysis
retained to recognize 12-round Simeck32/64 with the               of the (related-key) differential-neural distinguishers
input difference (0x0000,0x0040). The number of                   for Simon and Simeck ciphers.                  We adopt the
examples for training and for testing are 225 and 223 ,           multiple ciphertext pairs with data of the form
respectively. The number of epochs is 30 and the                  (∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1   r−2
                                                                                                      R , p∆R ) fed to the neu-
learning rate is 10−4 . The learning rate scheduler used          ral network to improve the accuracy of the neural
TABLE 5: Experiment with different data format of 9-, 10-, and 11-round NDs for Simon32/64. The best NDs for
9-, 10-, and 11-round are shown shaded.

     Cipher    Round                    Data Format                           Acc          TPR          TNR           Source
                                       (Cl , Cr , Cl′ , Cr′ )               0.7524        0.7304       0.7743          [16]
                                            (∆rL , ∆rR )                    0.6895        0.6613       0.7176          [28]
                  9                     (Cr , Cr′ , ∆r−1
                                                       R )                  0.8908        0.8786       0.9031          [18]
                              (∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1
                                                                   R )      0.8945        0.8834       0.9057      This Paper.
                         (∆rL , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1
                                                             R    , p∆r−2
                                                                      R )   0.9176        0.9052       0.9299      This Paper.
                                       (Cl , Cr , Cl′ , Cr′ )               0.5007        0.7015       0.2989          [16]
                                            (∆rL , ∆rR )                    0.5605        0.5402       0.5809          [28]
     Simon
                 10                     (Cr , Cr′ , ∆r−1
                                                       R )                  0.6856        0.6610       0.7102          [18]
     32/64
                              (∆L , ∆R , Cl , Cr , Cl′ , Cr′ , ∆r−1
                                 r     r
                                                                   R )      0.6889        0.6639       0.7139      This Paper.
                         (∆L , ∆R , Cl , Cr , Cl , Cr , ∆R , p∆r−2
                            r     r               ′     ′    r−1
                                                                      R )   0.6975        0.6662       0.7287      This Paper.
                                       (Cl , Cr , Cl′ , Cr′ )               0.5006        0.4148       0.5863          [16]
                                            (∆rL , ∆rR )                    0.5007        0.8110       0.1898          [28]
                 11                     (Cr , Cr′ , ∆r−1
                                                       R )                  0.5555        0.5437       0.5673          [18]
                              (∆L , ∆R , Cl , Cr , Cl′ , Cr′ , ∆r−1
                                 r     r
                                                                   R )      0.5578        0.5455       0.5700      This Paper.
                         (∆L , ∆rR , Cl , Cr , Cl′ , Cr′ , ∆r−1
                            r
                                                             R    , p∆r−2
                                                                      R )   0.5609        0.5366       0.5852      This Paper.


distinguisher. Meanwhile, we investigate the impact                     [2] Matsui, M. Linear cryptanalysis method for des
of input difference on the performance of the hybrid                        cipher. Workshop on the Theory and Application of
distinguishers to select the appropriate input differ-                      of Cryptographic Techniques, pp. 386–397. Springer.
ence. For Simon32/64, Simon64/128, Simeck32/64                          [3] Knudsen, L. and Wagner, D. Integral cryptanalysis.
and Simeck64/128, we construct the (related-key)                            International Workshop on Fast Software Encryption,
                                                                            pp. 112–127. Springer.
differential-neural distinguishers with higher accuracy.
                                                                        [4] Bogdanov, A. and Rijmen, V. Linear hulls with
   It is undeniable that there are many factors that
                                                                            correlation zero and linear cryptanalysis of block
can affect the performance of neural distinguishers.                        ciphers. Designs, codes and cryptography, 70, 369–383.
This paper explores its impact on the performance                       [5] Mouha, N., Wang, Q., Gu, D., and Preneel, B.
of neural distinguishers from the perspective of data                       Differential and linear cryptanalysis using mixed-
format and input difference. In the future, we plan to                      integer linear programming. International Conference
further explore ways that can improve the performance                       on Information Security and Cryptology, pp. 57–76.
of neural networks from multiple dimensions, such as                        Springer.
using methods of feature engineering to extract more                    [6] Sun, S., Hu, L., Wang, P., Qiao, K., Ma, X., and Song,
essential features of the training data and so on.                          L. Automatic security evaluation and (related-key)
                                                                            differential characteristic search: application to simon,
                                                                            present, lblock, des (l) and other bit-oriented block
ACKNOWLEDGEMENTS                                                            ciphers. International Conference on the Theory and
This work was supported in part by the National                             Application of Cryptology and Information Security,
                                                                            pp. 158–178. Springer.
Key Research and Development Program of China
                                                                        [7] Mouha, N. and Preneel, B. A proof that the arx cipher
[No.2021YFB3100800]; and the State Key Laboratory
                                                                            salsa20 is secure against differential cryptanalysis.
of Information Security [2020-MS-02]; and the National                      IACR Cryptol. ePrint Arch., 2013, 328.
Natural Science Foundation of China [grant numbers                      [8] Kölbl, S., Leander, G., and Tiessen, T. Observations
61872379, 61702537]; and the Academy of Finland                             on the simon block cipher family. Annual Cryptology
[grant number 331883].                                                      Conference, pp. 161–185. Springer.
                                                                        [9] Minier, M., Solnon, C., and Reboul, J. Solving a
DATA AVAILABILITY                                                           symmetric key cryptographic problem with constraint
                                                                            programming. ModRef 2014, Workshop of the CP 2014
The data underlying this article are available in the                       Conference 13.
article and in its online supplementary material.                      [10] Gerault, D., Minier, M., and Solnon, C. Constraint
                                                                            programming models for chosen key differential
                                                                            cryptanalysis. International Conference on Principles
REFERENCES
                                                                            and Practice of Constraint Programming, pp. 584–601.
 [1] Biham, E. and Shamir, A. Differential cryptanalysis of                 Springer.
     des-like cryptosystems. Journal of CRYPTOLOGY, 4,                 [11] LeCun, Y., Bengio, Y., and Hinton, G. Deep learning.
     3–72.                                                                  nature, 521, 436–444.
[12] Bengio, Y., Lecun, Y., and Hinton, G. Deep learning         [28] Hou, Z., Ren, J., and Chen, S. Improve neural
     for ai. Communications of the ACM, 64, 58–65.                    distinguishers of simon and speck.       Security and
[13] Rivest, R. L. Cryptography and machine learning. In-             Communication Networks, 2021.
     ternational Conference on the Theory and Application        [29] Kingma, D. P. and Ba, J. Adam: A method for
     of Cryptology, pp. 427–439. Springer.                            stochastic optimization.
[14] Maghrebi, H., Portigliatti, T., and Prouff, E. Breaking     [30] Lu, J., Liu, Y., Ashur, T., and Li, C. On the effect of
     cryptographic implementations using deep learning                the key-expansion algorithm in simon-like ciphers. The
     techniques.     International Conference on Security,            Computer Journal, 65, 2454–2469.
     Privacy, and Applied Cryptography Engineering, pp. 3–
     26. Springer.
[15] Hospodar, G., Gierlichs, B., De Mulder, E., Ver-
     bauwhede, I., and Vandewalle, J. Machine learning in
     side-channel analysis: a first study. Journal of Crypto-
     graphic Engineering, 1, 293.
[16] Gohr, A. Improving attacks on round-reduced
     speck32/64 using deep learning. Annual International
     Cryptology Conference, pp. 150–179. Springer.
[17] Benamira, A., Gerault, D., Peyrin, T., and Tan, Q. Q.
     A deeper look at machine learning-based cryptanalysis.
     Annual International Conference on the Theory and
     Applications of Cryptographic Techniques, pp. 805–835.
     Springer.
[18] Bao, Z., Guo, J., Liu, M., Ma, L., and Tu, Y. Enhancing
     differential-neural cryptanalysis. International Confer-
     ence on the Theory and Application of Cryptology and
     Information Security. Springer.
[19] Beaulieu, R., Shors, D., Smith, J., Treatman-Clark,
     S., Weeks, B., and Wingers, L. The simon and speck
     lightweight block ciphers. Proceedings of the 52nd
     Annual Design Automation Conference, pp. 1–6.
[20] Yang, G., Zhu, B., Suder, V., Aagaard, M. D., and
     Gong, G. The simeck family of lightweight block
     ciphers.    International Workshop on Cryptographic
     Hardware and Embedded Systems, pp. 307–329.
     Springer.
[21] Biham, E. New types of cryptanalytic attacks using
     related keys. Journal of Cryptology, 7, 229–246.
[22] Jakimoski, G. and Desmedt, Y. Related-key differential
     cryptanalysis of 192-bit key aes variants. International
     Workshop on Selected Areas in Cryptography, pp. 208–
     221. Springer.
[23] Ko, Y., Hong, S., Lee, W., Lee, S., and Kang, J.-S.
     Related key differential attacks on 27 rounds of xtea
     and full-round gost. International Workshop on Fast
     Software Encryption, pp. 299–316. Springer.
[24] Biryukov, A. and Nikolić, I. Automatic search for
     related-key differential characteristics in byte-oriented
     block ciphers: Application to aes, camellia, khazad and
     others. Annual International Conference on the Theory
     and Applications of Cryptographic Techniques, pp. 322–
     344. Springer.
[25] He, K., Zhang, X., Ren, S., and Sun, J. Deep residual
     learning for image recognition. Proceedings of the IEEE
     conference on computer vision and pattern recognition,
     pp. 770–778.
[26] Hu, J., Shen, L., and Sun, G. Squeeze-and-excitation
     networks.     Proceedings of the IEEE conference on
     computer vision and pattern recognition, pp. 7132–7141.
[27] Chen, Y., Shen, Y., Yu, H., and Yuan, S. A new neural
     distinguisher considering features derived from multiple
     ciphertext pairs. bxac019.
```
