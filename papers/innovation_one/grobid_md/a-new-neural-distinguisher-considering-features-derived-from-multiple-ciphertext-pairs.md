# A New Neural Distinguisher Considering Features Derived from Multiple Ciphertext Pairs

**Authors:** Yi Chen, Yantian Shen, Hongbo Yu, Sitong Yuan

**Source PDF:** `2021_chen_multiple_ciphertext_pairs_neural_distinguisher.pdf`

## Abstract

Neural aided cryptanalysis is a challenging topic, in which the neural distinguisher (N D) is a core module. In this paper, we propose a new N D considering multiple ciphertext pairs simultaneously. Besides, multiple ciphertext pairs are constructed from different keys. The motivation is that the distinguishing accuracy can be improved by exploiting features derived from multiple ciphertext pairs. To verify this motivation, we have applied this new N D to five different ciphers. Experiments show that taking multiple ciphertext pairs as input indeed brings accuracy improvement. Then, we prove that our new N D applies to two different neural aided key recovery attacks. Moreover, the accuracy improvement is helpful for reducing the data complexity of the neural aided statistic attack. The code is available at https://github.com/AI-Lab-Y/ND_mc .

## INTRODUCTION

In CRYPTO'19, Gohr improved attacks on round reduced Speck32/64 using deep learning [1] , which created a precedent for neural aided cryptanalysis. The neural distinguisher (N D) proposed by Gohr plays a core role in [1] . Its target is to distinguish real ciphertext pairs (C 0 , C 1 ) corresponding to plaintext pairs with a specific difference from random ciphertext pairs. N D takes a ciphertext pair (C 0 , C 1 ) as input, and gives the classification result.

The performance of N D is important for neural aided cryptanalysis. For Gohr's key recovery attack [1] , the most important step is identifying the right plaintext structure that passes the differential placed before N D. To attack 11-round Speck32/64, Gohr adopted a 6round N D and 7-round N D for identifying the right plaintext structure. The identification result is given by the 6-round N D instead of 7-round N D. Compared with the 7-round N D, the 6-round N D achieves higher distinguishing accuracy. This implies that a stronger ND is more helpful for Gohr's attacks. Recently, Chen et al proposed a generic neural aided statistical attack (NASA) for cryptanalysis [2] . The data complexity of NASA is strongly related to the distinguishing accuracy of N D.

To improve the performance of N D, researchers have explored N D from different directions. The most popular direction is adopting different neural networks. In [3] , Jain et al proposed a multi-layer perceptron network (MLP) to build N Ds against PRESENT reduced to 3, 4 rounds. In [4] , Yadav et al also built an MLP-based 3-round N D against Speck32/64. In [5] , Bellini et al compared MLP-based and Convolutional Neural Network-based distinguishers with classic distinguishers.

In [6] , Pareek et al proposed fully-connected network-based distinguisher against the key scheduling algorithm of PRESENT. Another popular direction is changing the input of N D. In [7] , Baksi et al used the ciphertext difference C 0 ⊕ C 1 as the input. In [2] , Chen et al suggested that the ND can be built by flexibly taking some bits of a ciphertext pair as input. In [8] , Hou et al investigate the influence of input difference pattern on the accuracy of N Ds against round reduced Simon32/64. These above N Ds can be viewed as the same type since only features hidden in a single ciphertext pair are exploited. Thus, another natural way is taking more ciphertexts as the input. In [9] , Benamira et al initially tested this idea as follows. First, a group of B ciphertexts is constructed from the same key. Second, take a group of B ciphertexts as the input of N D. Finally, based on a large B, the accuracy of N Ds against 5-round and 6-round Speck32/64 is increased to 100%, which is a huge improvement.

Previous findings especially the work in [9] inspired us to think about the deeper motivation of taking Y. Chen, Y. Shen, H. Yu, S. Yuan more ciphertexts as input. We believe that the deeper motivation stands for a generic method for improving N D. The N D processing a group of B ciphertexts has two important characteristics: (1) the input contains more ciphertexts, (2) all the ciphertexts in a group share the same key. Since Ankele and Kölbl [10] , as well as Gohr [1] , reported significant key-dependency in the output distribution in round reduced Speck, we wonder whether the same key is a core factor that brings significant improvement.


## Our Contributions

In this paper, our work contains five contributions:

• By introducing a clear deep motivation, we propose a new N D considering multiple ciphertext pairs simultaneously. The motivation is as follows.

When ciphertext pairs corresponding to plaintext pairs with a specific difference obey a non-uniform distribution, there are some derived features from multiple ciphertext pairs. Once neural networks capture these features, N D would obtain performance improvement.

• We prove that the same key is not the core factor that brings significant improvement in [9] . We made the conclusion by testing the accuracy of N Ds against round reduced Speck32/64 under two different scenarios: one is that ciphertext pairs in a group share the same key, one is that ciphertext pairs in a group adopt different keys. In the first scenario, the key for generating a ciphertext group each time is randomly selected. Experiments show that the same key has small or no influence on N Ds.

• We design a verification framework for further directly checking that derived features from multiple ciphertext pairs are learned. This framework is composed of two tests: false-negative test (FNT), false-positive test (FPT).

• We build two types of N Ds for five round reduced ciphers: Speck32/64, Chaskey, PRESENT, DES, SHA3-256. The first one is the N D proposed by Gohr, and the other one is our new N D. These experiments further prove the advantage of taking multiple ciphertext pairs as input and support the presented deep motivation.

• We prove that the N D taking multiple ciphertext pairs as input applies to key recovery, which is not discussed in previous research. At the time of writing, there are only two key recovery attacks [1, 2] based on the N D proposed by Gohr. We show how to apply new N D to these two attacks. Due to the performance improvement, the data complexity of the attack [2] can be reduced by using the new N D.


## Outlines

This paper is organized as follows:

• Section 2 presents preliminaries, including some important notations and five related ciphers.

• In section 3, the N D proposed by Gohr and two key recovery attacks are briefly reviewed.

• Section 4 presents the new N D including the motivation, model, the neural network for implementing the new N D, and the training pipeline.

• Section 5 presents the verification framework.

• In section 6, we build N Ds for five ciphers and perform an analysis.

• In section 7, we show how to perform key recovery attacks using the new N D. A data reuse strategy is also proposed in this section.


## PRELIMINARIES


## Notations


## P, C Plaintext, Ciphertext α

Plaintext difference N, M

The number of plaintext or ciphertext pairs N D k=?

N D with k ciphertext pairs as input Z

The output of an N D r

The number of reduced rounds


## Five Ciphers

We choose five different ciphers for supporting our work.

• Speck32/64 [11] is a lightweight block cipher whose block size is 32 bits. Its non-linear component is the modular addition.

• Chaskey [12] is a Message Authentication Code (MAC) algorithm whose intermediate state size is 128 bits. Its non-linear component is the modular addition.

• Present64/80 [13] is a block cipher whose block size is 64 bits. Its non-linear component is a 4×4 Sbox.

• DES [14] is a block cipher whose block size is 64 bits. Its non-linear component is given by eight different 6 × 4 Sboxes.

• SHA3-256 [15] is a hash function whose intermediate state size is 1600 bits. Its non-linear component can be seen as the application of a 5-bit Sbox applied in parallel 320 times.

We refer readers to [11, 12, 13, 14, 15] for more details of these ciphers.


## Computing Resources

In this paper, the available computing resources are: an Intel(R) Core(TM) i5-7500 CPU @ 3.40GHz, a graphics card (NVIDIA GeForce GTX 1060 6GB).


## A New Neural Distinguisher Considering Features Derived from Multiple Ciphertext Pairs 3


## RELATED WORK


## Gohr's Neural Distinguisher

In [1] , Gohr built N Ds against round reduced Speck32/64. The N D proposed by Gohr is a generic distinguisher since it only requires a plaintext difference constraint.

Consider a cipher E and a plaintext difference α. Gohr's N D aims at distinguishing two classes of ciphertext pairs

where (C 0 , C 1 ) is the ciphertext pair corresponding to the plaintext pair (P 0 , P 1 ), and Y is the label of (C 0 , C 1 ). We denote ciphertext pairs corresponding to plaintext pairs with the target difference α as positive samples, and denote ciphertext pairs corresponding to plaintext pairs with a random difference as negative samples.

If a neural network achieves a distinguishing accuracy higher than 0.5 over randomly selected ciphertext pairs, the neural network is a valid N D.

In [1] , Gohr chose a residual network [16] with one output neuron. Thus, the output Z of Gohr's N D is also used as the following posterior probability

where f (C 0 , C 1 ) stands for features learned by the ND from (C 0 , C 1 ), F 1 (•) is the posterior probability estimation function learned by the N D. If P r(Y = 1|(C 0 , C 1 )) > 0.5, the label of (C 0 , C 1 ) predicted by the N D is 1.


## Gohr's Key Recovery Attack

Given an N D, we denote the output of N D as Z. Positive samples are expected to obtain a higher posterior probability than negative samples, which is the core idea of Gohr's key recovery attack [1] . Consider an (r + 1)-round cipher E and an r-round N D built over a plaintext difference α. Gohr's attack recovers the subkey of the (r + 1) -th round as follows:

1. Generate m positive samples with α randomly. 2. For each possible subkey guess kg:

3. Return kg with the highest key rank score as the final subkey guess.

The value of c 1 and m is set experimentally.


## FIGURE 1.

The key recovery process. The prepended differential ∆P → α is satisfied with a probability p0. The intermediate state pair is (S0, S1).

A differential ∆P → α can be placed before the N D to extend the rounds covered by the attack (see Fig. 1 ). With the help of neutral bits [17] , ciphertext structures consisting of m positive samples or negative samples can be generated. Then a high rank score occurs only when the structure consisting of positive samples is decrypted by the true subkey. More details can refer to [1] .


## Neural Aided Statistical Attack

The neural aided statistical attack proposed by Chen et al [2] is performed as follows:

1. Randomly generate N plaintext pairs with a difference ∆P . 2. Collect the ciphertext pairs. 3. For each possible subkey guess kg:

4) (d) If T exceeds a decision threshold t, save kg as a subkey candidate.

4. Return all the surviving subkey candidates.

Chen et al proposed a theoretical framework to estimate N and t. The value of c 2 is set in advance, which doesn't influence the estimation of N, t.

According to Fig. 1 , Chen et al summarized three types of probabilities:

where sk is the true subkey. These three probabilities p 1 , p 2 , p 3 are related to the N D. NASA returns all the possible subkey candidates. Besides, NASA allows us to set two ratios β 0 , β 1 in advance. The ratio β 0 is the expected probability that the true subkey sk survives the attack. The ratio β 1 is the expected probability that wrong subkey guesses survive the attack.

Based on p 0 , p 1 , p 2 , p 3 , β 0 , β 1 , the required N is:

where

and z 1-β0 , z 1-β1 are the quantiles of the standard normal distribution. The decision threshold t is:

where

If c 2 = 0.5, the distinguishing accuracy of the ND is (p 1 + 1 -p 3 ) × 0.5. Thus the data complexity of NASA is strongly related to the N D. We refer readers to [2] for more details of NASA.


## NEW NEURAL DISTINGUISHER


## Motivations

The motivations of our new neural distinguisher contain two aspects.

First, in the machine learning community, providing more features is a common method to improve the accuracy of neural networks. For example, depth map estimation [18] and action recognition [19] are both tackled by feeding various features (eg. stereo knowledge [20] , depth maps [21] ) into neural networks simultaneously. Second, there are some useful features among multiple samples drawn from the same non-uniform distribution. Fig. 2 shows a simple example. If we randomly draw two samples (x 1 1 , x 1 2 )/(x 2 1 , x 2 2 ) from a Gaussian distribution or a uniform distribution, the average distance of two samples is d 1 /d 2 . Then it is expected that d 1 < d 2 , which is useful for distinguishing the two distributions.

Based on the two common phenomena, we obtain the idea of building a new neural distinguisher by considering multiple ciphertext pairs.


## New Distinguisher Model

Our new N D needs to distinguish two types of ciphertext groups (C 1,1 , C 1,2 , • • • , C k,1 , C k,2 ):

where Y is the label of ciphertext groups, and (C j,1 , C j,2 ) is the ciphertext pair corresponding to the plaintext pair (P j,1 , P j,2 ), j ∈ [1, k] .

According to the introduced motivation, the requirement is that ciphertext pairs in a group are randomly sampled from the same distribution. To minimize influencing factors, we ask that a ciphertext group is constructed from k random keys if the cipher needs a key. This ensures that k ciphertext pairs do not have any same properties except for the same plaintext difference constraint.

Our new N D can be described as

where f (X i ) represents the basic features extracted from the ciphertext pair X i , ϕ (•) is the derived features, and F 2 (•) is the new posterior probability estimation function.

The motivation also puts forward some design guidelines for the neural network to be used. Since we hope more features ϕ(f (X 1 ), • • • , f (X k )) are extracted from the distribution of basic features f (X i ), i ∈ [1, k], N D should learn basic features from each ciphertext pair firstly.

From the perspective of neural networks, this requirement can be satisfied by placing one-dimensional convolutional layers before two-dimensional convolutional layers.


## Residual Network


## Network Architecture

The network architecture adopted by Gohr [1] is also applied in this article. According to the requirement of the motivation, except for the first one-dimensional convolutional layer, the remaining one-dimensional convolutional layers are replaced by two-dimensional convolutional layers.

Figure 3 shows the neural network architecture. The input consisting of k ciphertext pairs is arranged in a [16] . FC is a fully connected layer that has d1 or d2 neurons. BN is batch normalization. Relu and Sigmoid are two different activation functions. The output of Sigmoid ranges from 0 to 1.


## k×w× 2L

w array. L represents the block size of the target cipher and w is the size of a basic unit. For example, L is 32 and w is 16 for Speck32/64.

The network architecture contains two core modules. The first one (Module 1) is a bit slice layer that contains convolution kernels with a size of 1 × 1. This layer can learn basic features from each input ciphertext pair that is arranged in a 1 × w × 2L w array. The second one (Module 2) is a residual block that is built over a twodimensional convolutional layer. The two-dimensional filters with a size of K s × K s can learn derived features from k ciphertext pairs. In this article, we use one residual block for building our new N Ds.


## Training Pipeline

New N Ds are obtained by following three processes: 1. Data Generation:

Consider a plaintext difference ∆P and a cipher E. Randomly generate k plaintext pairs with ∆P . If E needs a key, randomly generate k keys. Collect the k ciphertext pairs with E and k keys. Regard these k ciphertext pairs as a ciphertext group with a size of k, and the label is Y = 1. We denote a ciphertext group with Y = 1 as a positive sample. If the plaintext differences of k plaintext pairs are random, the label of the resulting ciphertext group is Y = 0. And we denote it as a negative sample. A training set is composed of N 2k positive samples and

positive samples and M 2k negative samples. We need to generate a training set and a testing set. 2. Training: Train the neural network (Figure 3 ) on the training dataset.

3. Testing: Test the distinguishing accuracy of the trained neural network on the testing dataset. If the test accuracy exceeds 0.5, return the neural network as a valid N D. Or choose a different α and start from the data generation process again.

In the training phase, the neural network is trained for E s epochs with a batch size of B s . The cyclic learning rate scheme in [1] is adopted. Optimization is performed against the following loss function:

where Z i,p is the output of the N D, Y i is the true label, W is the parameters of the neural network, and λ is the penalty factor. The Adam algorithm [22] with default parameters in Keras [23] is applied to the optimization.


## THE VERIFICATION FRAMEWORK

Although the distinguishing accuracy of new N D k is the best evidence for supporting the motivation of taking k ciphertext pairs as input, we propose an auxiliary verification framework to further show that new N D k captures features derived from multiple ciphertext pairs. This framework is composed of two tests: False Negative Test (FNT), False Positive Test (FPT). The idea of FPT and FNT is as follows. When features f (X i ), i ∈ [1, k] hidden in a single ciphertext pair do not lead to the right classification, only derived features ϕ (f (X 1 ) , • • • , f (X k )) can provide useful clues for classification.

It is hard to directly select k ciphertext pairs that satisfy the above requirement based on the N D k itself. Thus, An N D that takes a single ciphertext pair as input is used to select k wrongly classified ciphertext pairs. This is an approximate but reasonable method that is based on the following reasons • When we build N D k , all the ciphertext pairs are constructed from different keys. This ensures that only two types of features are available: one is features hidden in a single ciphertext pair, the other one is features derived from multiple ciphertext pairs.

• When the N D that takes one ciphertext pair as input has high accuracy, it means that features hidden in the ciphertext pair provide strong clues leading to wrong classifications. If new N D k still correctly classifies such k ciphertext pairs with a high probability, we can believe that this is due to features derived from multiple ciphertext pairs.


## False Negative Test (FNT)

If k ciphertext pairs with label 1 are all wrongly classified by the N D that takes a single ciphertext pair as input

such ciphertext pairs are false negative samples. These k samples are combined into a ciphertext group and fed into N D k . Generate a large number of such ciphertext groups and feed them to N D k . What we care about is the following pass ratio

. The final pass ratio under such a setting can show whether derived features have been learned and their effects. If N D k can obtain a non-negligible pass ratio, then ϕ (f (X 1 ) , • • • , f (X k )) can offset the negative influence of f (X i ) , i ∈ [1, k] . If the pass ratio is high, derived features from k ciphertext pairs play a vital role in classification for this kind of ciphertext pair.


## False Positive Test (FPT)

Similarly, if k ciphertext pairs with label 0 are wrongly classified such ciphertext pairs are false positive samples. These k samples are combined into a ciphertext group and fed into N D k . Now what we care about is the following pass ratio


## APPLICATIONS TO FIVE CIPHERS

We apply our new N D as well as Gohr's N D to five ciphers introduced in section 2.2. The training pipeline of Gohr's N D is presented in [1] . Table 1 summarizes the parameters that are related to the residual network and training pipeline that are introduced in section 4.3. Since Gohr provided N Ds against round reduced Speck32/64 in CRYPTO'19, we perform in-depth analysis by taking the application to Speck32/64 as an example. Applications to the remaining four ciphers are listed as supporting materials. For convenience, we denote Gohr's N D as N D k=1 .


## Experiments on Speck32/64


## Neural Distinguishers

The plaintext difference is α = (0x0040, 0) introduced in [24] .

We built N D k , k ∈ {2, 4, 8, 16} against Speck32/64 reduced to 5, 6, and 7 rounds respectively.

Table 2 lists the accuracy of N Ds. Compared with N D k=1 , all the N D k , k > 1 achieve accuracy improvement. Besides, we find that the overfitting phenomenon [25] always appears in the training process of N D k=16 against 7-round Speck32/64. If this problem could be solved, it is possible to further improve the accuracy.

In the above setting, our distinguishers take k ciphertext pairs as input while Gohr's distinguishers take one ciphertext pair as input. To prove the positive influence of features derived from multiple ciphertext pairs, we compare the distinguishing accuracy under a fair setting.

The concrete process is as follows:

1. Generate n ciphertext pairs with the same sample label. It is worth noticing that n random keys are used. 2. For Gohr's distinguishers N D k=1 , feed n ciphertext pairs into N D k=1 , and use the median value of n outputs to give the prediction label of the n ciphertext pairs. 3. For our new distinguishers N D k>1 , collect m ciphertext groups by uniformly sampling from the n ciphertext pairs, feed m ciphertext groups into N D k>1 , and use the median value of n outputs to give the prediction label. 4. Repeat the above steps 10 6 times and count the distinguishing accuracy.

Such a setting ensures that our distinguishers do not use more prior knowledge. Taking N D k=2 , N D k=4 as examples, we have performed several experiments under the setting. Table 3 summarizes our experiment results. Under the fair setting, our distinguishers achieve higher accuracy. This proves that some features derived from multiple ciphertext pairs have been captured by our distinguishers, and these features bring accuracy improvement.

Besides, we find that the distinguishing accuracy can be further improved, if we increase m by adopting the data reuse strategy that will be introduced in Section 7.1.


## The Impact of the Same Key Setting

As introduced in section 1, Benamira et al also tested the idea of taking multiple ciphertext pairs as input [9] . The difference with our N Ds is that ciphertext pairs belonging to a group are constructed from the same key in [9] .

To prove that the same key setting is not the core factor that brings huge accuracy improvement in [9] , we build N Ds by adopting the same key setting as follows

• we randomly generate a key for each ciphertext group.

• k ciphertext pairs belonging to a group are constructed from the same key.

Then we test the distinguishing accuracy of these N Ds over two kinds of testing sets • testing set 1: k ciphertext pairs of a group are constructed from k different keys. • testing set 2: k ciphertext pairs of a group are constructed from the same key.

Table 4 summarizes the accuracy of N Ds over two kinds of testing sets. Based on the comparision with results as shown in Table 2 , we find that the same key setting has small or no influence on the accuracy.


## The comparison of Neural Network parameters

Since the neural network adopted in this paper is different from the neural network adopted by Gohr in [1] , we also focus on the comparison of neural network parameters.

Table 5 summarizes the comparison of neural network parameters as well as the accuracy of some N Ds. Gohr reported the best accuracy of 5-round and 6round N D k=1 by using 10 residual blocks. Besides, Gohr also provided N D k=1 by using 1 residual block. These two kinds of distinguishers almost achieve the same accuracy.

Compared with N D k=1 with 10 residual blocks, our new distinguishers N D k=2 achieve significant accuracy improvement but contains fewer parameters. This comparison proves that taking more ciphertext pairs as input is the reason that brings accuracy improvement.


## The Results of FPT and FNT

We further perform the FPT and FNT. Corresponding pass ratios are presented in Table 6 . For each N D k , there is at least one type of pass ratio higher than 0. This further proves that N D k captures derived features from k ciphertext pairs.


## Experiments on Chaskey

Based on the plaintext difference α = (0x8400, 0x0400, 0, 0) [12] , we build N Ds against Chaskey reduced to 3, 4 rounds. The accuracies are presented in Table 7 . Table 8 summarizes the results of the FPT and FNT.


## Experiments on Present64/80

Based on the plaintext difference α = (0, 0, 0, 0x9) provided in [26] , we build N Ds against Present64/80 reduced up to 6, 7 rounds respectively. The penalty factor is 10 -4 and other related parameters are the same as Table 1 . The distinguishing accuracies are presented in Table 9 . Table 10 summarizes the results of FPT and FNT.


## Experiments on DES

Based on the analysis of DES in [27] , the plaintext difference α = (0x40080000, 0x04000000) is adopted. We build N Ds against DES reduced to 5, 6 rounds. The batch size is adjusted to 5000. The penalty factor is increased to 8 × 10 -4 . Other related parameters are the same as Table 1 . The distinguishing accuracies are presented in Table 11 . The pass ratios of the FPT and FNT of N Ds are presented in Table 12 .


## Experiments on SHA3-256

SHA3-256 is a hash function. When one message block is fed into reduced SHA3-256, we collect the first 32 bytes of the output process after r-rounds permutation is applied to this message block. Given a message difference α = 1, we build N Ds against SHA3-256 reduced up to 3 rounds.

The number of ciphertext pairs is N = 2 × 10 6 . The batch size is 500, and the penalty factor is 10 -5 . The accuracies are presented in Table 13 . The pass ratios of the FPT and FNT of N Ds are presented in Table 14 .


## KEY RECOVERY ATTACKS

In this section, we propose a data reuse strategy for reducing data complexity. Then we prove that our N D can be applied to the two key recovery attacks introduced in section 3. Since the data complexity of NASA is directly related to the performance of N Ds, NASA is first performed to highlight the extra superiority of our N Ds.


## Data Reuse Strategy for Reducing Data Complexity

There is a potential problem when we directly apply our new N D to key recovery attacks. Assuming Gohr's distinguisher and our new N D k have the same performance, and a certain attack requires M random inputs. If we directly reshape M ×k ciphertext pairs into M ciphertext groups, the data complexity of our N D k is k times as much as the data complexity of Gohr's distinguisher.

Given M ciphertext pairs X i = (C i,0 , C i,1 ), i ∈ [1, M ], there are a total of M k options for composing a ciphertext group, which is much larger than M k . Thus we can randomly select M ciphertext groups from M k options. Such a strategy can help reduce data complexity. In fact, it is equivalent to attach more importance to derived features from k ciphertexts.

However, the subsequent key recovery attacks using this naive strategy do not obtain good results. The main reason is that the sampling randomness of M ciphertext groups is destroyed. Two new concepts are proposed for overcoming this problem.


## Maximum Reuse Frequency:

During the generation of M ciphertext groups, a ciphertext pair is likely to be reused several times. We denote the reuse frequency of the i th ciphertext pair as RF i , i ∈ [1, M ]. Maximum Reuse Frequency (M RF ) is defined as the maximum value of RF i :

Sample Similarity Degree: For any two ciphertext groups G i , G j , the similarity of these two ciphertext groups is defined as the number of the same ciphertext pairs. As for M ciphertext groups, Sample Similarity Degree (SSD) is defined as the maximum of any two ciphertext groups' similarity:

M RF can ensure that the contribution of each ciphertext pair is similar. SSD can increase the distribution uniformity of M ciphertext groups as much as possible. Based on the above two concepts, we propose the following Data Reuse Strategy (see Algorithm 1) that can reduce data complexity and maintain sampling randomness.


## Algorithm 1 Data Reuse Strategy

Require: M RF ; SSD; k; M . Ensure: M ciphertext groups with a size of k.

1: Randomly select k ciphertext pairs from M ciphertext pairs to form a ciphertext group. 2: Repeat step 2 for M times to obtain M ciphertext groups. 3: Compute M RF and SSD. If two values are both smaller than the threshold we set, return the M ciphertext groups. Or start from step 1 again.


## Application to NASA

When we replace Gohr's distinguisher with our new N D, the process of NASA does not change. The only difference is the data collection.


## Data Collection

Consider the attack process as shown in Fig. 1 .

Assuming that our new N D is built with α. Now, we need to generate ciphertext groups. Generate k plaintext pairs (P i 0 , P i 1 ), i ∈ [1, k] with the difference ∆P . Collect corresponding ciphertexts

The intermediate states are

Y. Chen, Y. Shen, H. Yu, S. Yuan

According to the introduction in section 4.2, these k ciphertext pairs should satisfy

simultaneously. We use neutral bits [17] to generate such k ciphertext pairs. Here we briefly review the definition of neutral bits. Let E denote the encryption function. We focus on the following conforming pairs

holds where e j = 1 << j, the j-th bit is a neutral bit.

Thus, we can generate 2 m k ciphertext pairs using m neutral bits. The probability that these k ciphertext pairs satisfy the difference transition ∆P → α simultaneously is still p 0 . Then N ciphertext groups with a size of k can be generated as 1. Randomly generate N plaintext pairs with ∆P . 2. Generate N plaintext structures using m neutral bits. 3. Randomly pick k plaintext pairs from a structure and collect the ciphertext pairs.

The total data complexity is N × k.

It is worth noticing that the data reuse strategy is still applicable here. More precisely, the data collection is performed as 1. Randomly generate N M plaintext pairs with ∆P . 2. Generate N M plaintext structures using m neutral bits. 3. Randomly pick M plaintext pairs from a structure, and generate M ciphertext groups using the data reuse strategy (Algorithm 1).

The total data complexity is N now.


## Experiments on Speck32/64

To prove that our N D applies to NASA, we perform experiments on Speck32/64. Our new N D achieves higher accuracy than the N D proposed by Gohr. Since the data complexity of NASA is related to the accuracy of N D, it is possible to reduce the data complexity of NASA by adopting our new N D.


## Experiment settings.

We adopt a 2-round differential ∆P = 0x211/0xa04 p0=2 -6

-----→ α = 0x40/0x0 as the prepended differential. Let β 0 = 0.005, β 1 = 2 -16 , c 2 = 0.5. The meaning of these parameters is defined in section 3.3. Since c 2 is set, the values of p 1 , p 3 are experimentally estimated based on N Ds.

The estimation of p 2 is complex. Let p 2|d denote the estimated value of p 2 where d is the Hamming distance between the correct key tk and wrong keys kg. According to the introduction in [2] , when d increases, p 2|d will decrease. Moreover, when p 2 increases, the data complexity of NASA also increases. Thus, if we TABLE 15 . Data complexity comparisons when p0 = 2 -6 , d = 2, β0 = 0.005, β1 = 2 -16 , c2 = 0.5. The prepended differential is a 3-round differential that is extended from 0x211/0xa04 p 0 -→ 0x40/0x0 without loss of transition probability.


## Distinguisher

Data Complexity (log 2 N ) r = 5 r = 6 r = 7 hope the Hamming distance between tk and surviving kg does not exceed d, the value of p 2 is

In this paper, we choose two different settings:

Comparison of data complexity. Table 15 and Table 16 show the comparison of data complexity under two experiment settings respectively.

The second row corresponds to the data complexity when Gohr's N D is adopted. These results are also used as the baseline. When an r-round N D with a group size of k is adopted, the corresponding data complexity is displayed in bold if it is smaller than the baseline.

We test 12 new N Ds in total. Table 15 and Table 16 show that the data complexity is reduced in most cases. There is only one case in which the data complexity is not reduced.


## Analysis of the data complexity.

There are two questions to be explained: (1) why does the accuracy improvement of N Ds bring the reduction of the data complexity? (2) why does the data complexity is not reduced in the only failed case shown in Table 16 ?

To answer the first question, we need to analyze how the data complexity is influenced by p 1 , p 3 . Based on Equation 8 in section 3.3, we get two following conclusions: • when p 1 |p 1 0.5 increases, the data complexity N decreases.

• when p 3 |p 3 0.5 decreases, the data complexity N decreases.

During the training of N Ds, the accuracy can be formulated as

where T P R is the true positive rate and T N R is the true negative rate.

If we set c 2 = 0.5, the following conclusions hold

Thus, when the accuracy acc of N Ds increases, there are three phenomena: p 1 increases, or p 3 decreases, or the former two phenomena both occur. No matter which phenomenon occurs, it is helpful for reducing the data complexity. This is why the data complexity is reduced in most cases shown in Table 15 and Table 16 .

To answer the second question, we need to consider the impact of p 2 . For convenience, we summarized the values of p 1 , p 2 , p 3 related to the 5-round N Ds in Table 17 .

The value of p 2 also increases as shown in Table 17 . Chen et al presented that the impact of p 1 , p 2 on N is O((p 1 -p 2 ) -2 ) [2] . Therefore, the increase of p 2 has a negative impact on the data complexity. If p 2 is very close to p 1 , the positive impact of the accuracy improvement may be offset. This is why the data complexity is not reduced when the 5-round N D k=16 is adopted.

Actually, when p 0 becomes smaller, the reduction of data complexity is more significant. Table 18 shows an example.


## Practical experiments.

Based on the attack settings shown in Table 15 , we perform NASA against 10-round Speck32/64 based on the N D k=1 and N D k=2 (r = 6) respectively. The target is to recover sk 10 . Since d = 2, the number of surviving subkey guesses should not exceed 137 × (1 -β 0 ) + (2 16 -137) × β 1 = 137.31.

Since the data complexity presented in Table 15 is not low, the attack may take too much time. We adopt an optimization method proposed in [2] to accelerate this attack. This method is building a student distinguisher to reduce the key space to be searched. The student distinguisher is built over 14 ciphertext bits {30 ∼ 23, 14 ∼ 7}. Then in the first stage, we guess 8 subkey bits sk 10 [8 ∼ 0]. In the second stage, we guess the complete sk 10 based on surviving guesses of sk 10 [8 ∼ 0]. To filter sk 10 [8 ∼ 0], the student distinguisher with k = 1 requires 2 18.888 plaintext pairs. In the second stage, we select N = 2 16.911 plaintext pairs from 2 18.888 plaintext pairs. When we perform NASA with Gohr's 6-round distinguishers 100 times, the results are 1. the true subkey sk 10 survives in 97 trails. 2. the average numbers of surviving subkey guesses in two stages are 14.98, 15.16 respectively. 3. in all the 100 trails, the number of surviving subkey guesses is lower than 137.31.

To filter sk 10 [8 ∼ 0], the student distinguisher with k = 2 requires 2 17.785 plaintext pairs. In the second stage, we select N = 2 15.821 plaintext pairs from 2 17.785 plaintext pairs. When we perform NASA with our 6round N D k=2 100 times, the results are 1. the true subkey sk 10 survives in 90 trails. 2. the average numbers of surviving subkey guesses in two stages are 11.82, 25.07 respectively. 3. In all the 100 trails, the number of surviving subkey guesses is lower than 137.31.

Figure 4 shows the runtime comparison of the 200 experiments. The practical experiments further prove that our new N Ds can be applied to NASA. Besides, with smaller data complexity, the NASA based on our N D achieves a competitive result.


## Application to Gohr's Attack

Gohr's attack is not directly related to the distinguishing accuracy of N Ds. Thus, we mainly verify whether our new N D applies to Gohr's attack.

In [1] , Gohr performed a key recovery attack on 11round Speck32/64. In this section, we first perform the same attack using our new N D k=2 . Then we present a deeper discussion.


## Key Recovery Attack on 11-round Speck32/64

The target of this attack is to recover the last two subkeys (sk 11 , sk 10 ). This attack returns a pair of subkey guesses (kg 11 , kg 10 ). If kg 11 = sk 11 and kg 10 is different from sk 10 at most 2 bits, this attack is viewed as a success [1] .


## Experiment settings.

A 6-round and 7-round N D k=2 are built over α = (0x40, 0x0). A prepended 3round differential is extended from a 2-round differential ∆P = (0x211, 0xa04) p0=2 -6 -----→ α = (0x40, 0x0). Six neutral bits {14, 15, 20, 21, 22, 23} are used to generate plaintext structures consisting of 64 plaintext pairs. The data reuse strategy is also adopted by letting M RF = 2 and SSD = 1.

The whole attack is performed as 1. Randomly generate 100 plaintext pairs with a difference ∆P . 2. Generate 100 plaintext structures using 6 neutral bits above, and collect corresponding ciphertext structures. 3. For each ciphertext structure:

(a) collect possible kg 11 using the method introduced in section 3.2. (b) For each possible kg 11 :

i. Decrypt the current ciphertext structure with kg 11 . ii. Collect possible subkey guess pairs (kg 11 , kg 10 ) using the method introduced in section 3.2.

4. Return surviving (kg 11 , kg 10 ) with the highest rank score as the final subkey guess.

In section 3.2, we have reviewed how Gohr's attack recovers the subkey sk r+1 with an r-round N D. This method needs a rank score threshold. In steps 3a and 3(b)ii, we need a threshold c 3 , c 4 respectively. In this paper, let c 3 = 18 and c 4 = 150. Experiment results. Run 1000 experiments each time, and repeat 5 times. These experiments based on Gohr's distinguishers N D k=1 were also performed using the same ciphertexts. Table 19 summarizes the success rates.


## Posterior Probability Analysis

We have proved that our N D applies to Gohr's attack. Moreover, the attack based on our N Ds shows a minor advantage in terms of the success rate. This minor advantage is interesting since the success rate of Gohr's attack is not directly determined by the distinguishing accuracy. To better understand the influence of accuracy improvement on Gohr's attack, we perform a deeper analysis from the perspective of the key rank score.

Consider an (r + 1)-round cipher E. We first build a r-round N D based on a difference α. Then we collect numerous ciphertext pairs corresponding to plaintext pairs with a difference α. We decrypt these ciphertext pairs with a subkey guess kg and feed the partially decrypted ciphertext pairs into the N D.

Let tk denote the true subkey of the (r + 1)-round. Besides, the Hamming distance between tk and kg is d. We focus on the expectation of the following conditional posterior probability

where X is the input of the N D, and F is N D. If the N D is Gohr's distinguisher, X is a decrypted ciphertext pair. If the N D is our distinguisher N D k , X is a ciphertext group consisting of k decrypted ciphertext pairs. Taking N D k=2 against Speck32/64 reduced to 6, 7 rounds as examples, we estimate the expectations of the above conditional posterior probability. As a comparison, we also estimate the expectations based on N D k=1 . The final estimation results are shown in Figure 5 , Figure 6 .

There are two important phenomena. First, compared with Gohr's distinguishers N D k=1 , our distinguishers N D k=2 bring higher expectations P r(Y = 1|X, d = 0). Second, the value of P r(Y = 1|X, d = 0) -P r(Y = 1|X, d = i), i ∈ [1, 16] increases.

The first phenomenon makes that a large key rank score threshold (eg. c 3 = 18, c 4 = 150) is applicable. 9 10 11 12 13 14 15 16 Gohr's 6-round ND New 6-round ND with k=2 0.4 0.42 0.44 0.46 0.48 0.5 0.52 0.54 0.56 0.58 0.6 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 Gohr's 7-round ND New 7-round ND with k=2 FIGURE 6. The expectations of the conditional posterior probability (Equation 21) of 7-round N Ds against Speck32/64.

The second phenomenon makes the gap between the rank score of the true key and that of wrong keys increase. By setting a high key rank score threshold, wrong keys are less likely to obtain a key rank score higher than the threshold. Thus, a higher success rate is more likely to be obtained by replacing Gohr's NDs with our NDs.


## OPEN PROBLEMS


## Our work in this paper raises some open problems:

• What features derived from multiple ciphertext pairs are learned by our distinguishers? • The influence of features derived from multiple ciphertext pairs is rather complex. More exactly, except for its positive influence, we find that these features also have a negative influence. For example, when we compare the distinguishing accuracy of N Ds under a fair setting (see Section 6.1.1), if we give the prediction label based on the following metric:

where Z i , i ∈ [1, m] is the output of N Ds, our distinguishers have tiny or no advantage in terms of the distinguishing accuracy. Table 20 shows our experiment results based on the above metric. Thus, an important problem is how to make full use of these features and bring more significant positive influence?

These problems are out of scope of this paper. We will explore in future research.


## CONCLUSIONS

In this paper, we focus on the neural distinguisher which is the core module in neural aided cryptanalysis. By considering multiple ciphertext pairs simultaneously, we propose a new neural distinguisher and have performed a deep exploration of it. Compared with the neural distinguisher considering a single ciphertext pair, this new neural distinguisher achieves higher distinguishing accuracy, which is verified by applications to five different ciphers. Moreover, we prove that the accuracy improvement results from features derived from multiple ciphertext pairs.

Our new neural distinguisher also applies to key recovery attacks.

We show how to perform two different key recovery attacks based on our new neural distinguishers.

The first one is the neural aided statistical attack. Due to the accuracy improvement, the data complexity of neural aided statistical attack is reduced by adopting our new neural distinguisher. A data reuse strategy is proposed to strengthen this advantage. The second one is the key recovery attack proposed by Gohr at CRYPTO'19. Our new neural distinguisher applies to this attack but does not bring a significant positive influence, since this attack is not related to the distinguishing accuracy.

Our new neural distinguisher is full of potential. In the future, as long as neural aided key recovery attacks are related to the performance of neural distinguishers, our new neural distinguisher could be a priority choice. Besides, our neural distinguisher also introduces a novel cryptanalysis direction by considering multiple ciphertext pairs simultaneously.

> (a) Decrypt m positive samples with kg. (b) Feed partially decrypted samples into the N D and collect the outputs Z i , i ∈ [1, m]. (c) Compute the rank score V kg of kg as:

> (a) Decrypt N ciphertext pairs with kg. (b) Feed partially decrypted ciphertext pairs into the ND and collect the outputs Z i , i ∈ [1, N ]. (c) Count the following statistic T :

> 2 FIGURE 2 . FIGURE 2. P1(x) : a Gaussian distribution. P2(x) : a uniform distribution.

> 3 FIGURE 3 . FIGURE 3.The network architecture of our new ND. Conv stands for a convolution layer with N f filters. The size of each filter is Ks × Ks. Module 2 also adopts the skip connection [16] . FC is a fully connected layer that has d1 or d2 neurons. BN is batch normalization. Relu and Sigmoid are two different activation functions. The output of Sigmoid ranges from 0 to 1.

> 4 FIGURE 4 . FIGURE 4. The runtime of 100 experiments. When Gohr's 6-round distinguisher N D k=1 is used, the average runtime of NASA is 612 seconds. When our 6-round distinguisher N D k=2 is used, the average runtime of NASA is 492 seconds.

> A New Neural Distinguisher Considering Features Derived from Multiple Ciphertext Pairs 13

> 576 FIGURE 5 .Gohr's 7 -FIGURE 6 . FIGURE 5.The expectations of the conditional posterior probability (Equation21) of 6-round N Ds against Speck32/64.

> 1 TABLE 1 . Parameters for constructing our new N D

> 3 TABLE 3 . Distinguishing accuracy of N Ds against Speck32/64 under the fair setting.

> 4 TABLE 4 . Distinguishing accuracy of N Ds over two kinds of testing sets. These N Ds are built under the same key setting.

> 5 TABLE 5 . The comparison of neural network parameters as well as the accuracy of N D k , k ∈ {1, 2}.

> 6 TABLE 6 . Pass ratios of FPT and FNT of N D k against Speck32/64.

> 8 TABLE 8 . Pass ratios of FPT and FNT of N Ds against Chaskey.

> 11 TABLE 11 . Distinguishing accuracy of N Ds against DES.

> 12 TABLE 12 . Pass ratios of FNT and FPT of N Ds against DES.

> 14 TABLE 14 . Pass ratios of FNT and FPT of N Ds against SHA3-256.

> 16 TABLE 16 . Data complexity comparisons when p0 = 2 -6 , d = 1, β0 = 0.005, β1 = 2 -16 , c2 = 0.5.

> 17 TABLE 17 . The value of p1, p2, p3 related to the 5-round N Ds when c2 = 0.5, d = 1, r = 5. p0 = 2 -6 .

> 18 TABLE 18 . The value of p1, p2, p3 related to the 5-round N Ds when c2 = 0.5, d = 1, r = 5. p0 = 2 -12 .

> 19 TABLE 19 . Success rates of performing 1000 experiments (Gohr's attack). Repeat 5 times. The first row represents the success rate when Gohr's distinguishers are used. The second row represents the success rate when our new distinguishers with k = 2 are used.

> 20 TABLE 20 . Distinguishing accuracy of N Ds against Speck32/64 under the fair setting. If v > 0 (see Formula 22), the prediction label is 1. r / n N D k=1 N D k=2 , m = n

## Acknowledgements

This work is supported by the National Key Research and Development Program of China ( 2018YFB0803405 , 2017YFA0303903 ).

## References

1. b0: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019-08-18. DOI: 10.1007/978-3-030-26951-7_6
2. b1: Yi Chen, Yantian Shen, Hongbo Yu. "Neural-Aided Statistical Attack for Cryptanalysis". The Computer Journal. 2020. DOI: 10.1093/comjnl/bxac099
3. b2: A Jain, V Kohli, G Mishra. "Deep learning based differential distinguisher for lightweight cipher PRESENT". IACR Cryptol. 2020
4. b3: Tarun Yadav, Manoj Kumar. "Differential-ML Distinguisher: Machine Learning Based Generic Extension for Differential Cryptanalysis". Lecture Notes in Computer Science. 2020. DOI: 10.1007/978-3-030-88238-9_10
5. b4: Emanuele Bellini, Matteo Rossi. "Performance Comparison Between Deep Learning-Based and Conventional Cryptographic Distinguishers". Lecture Notes in Networks and Systems. 2020. DOI: 10.1007/978-3-030-80129-8_48
6. b5: M Pareek, G Mishra, V Kohli. "Deep learning based analysis of key scheduling algorithm of PRESENT cipher". IACR Cryptol. 2020
7. b6: Anubhab Baksi, Jakub Breier, Yi Chen, Xiaoyang Dong. "Machine Learning Assisted Differential Distinguishers For Lightweight Ciphers". 2021 Design, Automation & Test in Europe Conference & Exhibition (DATE). 2021-02-01. DOI: 10.23919/date51398.2021.9474092
8. b7: Z Hou, J Ren, S Chen. "Cryptanalysis of round-reduced SIMON32 based on deep learning". IACR Cryptol. ePrint Arch. 2021
9. b8: Adrien Benamira, David Gerault, Thomas Peyrin, Quan Quan Tan. "A Deeper Look at Machine Learning-Based Cryptanalysis". Lecture Notes in Computer Science. 2021-10-17. DOI: 10.1007/978-3-030-77870-5_28
10. b9: Ralph Ankele, Stefan Kölbl. "Mind the Gap - A Closer Look at the Security of Block Ciphers against Differential Cryptanalysis". Lecture Notes in Computer Science. 2018-08-15. DOI: 10.1007/978-3-030-10970-7_8
11. b10: Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks, Louis Wingers. "The SIMON and SPECK lightweight block ciphers". Proceedings of the 52nd Annual Design Automation Conference. 2015-06-07. DOI: 10.1145/2744769.2747946
12. b11: Nicky Mouha, Bart Mennink, Anthony Van Herrewege, Dai Watanabe, Bart Preneel, Ingrid Verbauwhede. "Chaskey: An Efficient MAC Algorithm for 32-bit Microcontrollers". Lecture Notes in Computer Science. 2014. DOI: 10.1007/978-3-319-13051-4_19
13. b12: "Selected Areas in Cryptography – SAC 2024". Selected Areas in Cryptography -SAC 2014 -21st International Conference. 2014. DOI: 10.1007/978-3-031-82841-6
14. b13: A Bogdanov, L R Knudsen, G Leander, C Paar, A Poschmann, M J B Robshaw, et al.. "PRESENT: An Ultra-Lightweight Block Cipher". Lecture Notes in Computer Science. 2007-09-10. DOI: 10.1007/978-3-540-74735-2_31
15. b14: Don Coppersmith, Chris Holloway, Stephen M Matyas, Nev Zunic. "The data encryption standard". Information Security Technical Report. 1997-01. DOI: 10.1016/s1363-4127(97)81325-8
16. b15: Senyang Huang, Xiaoyun Wang, Guangwu Xu, Meiqin Wang, Jingyuan Zhao. "Conditional Cube Attack on Reduced-Round Keccak Sponge Function". Lecture Notes in Computer Science. 2017-04-30. DOI: 10.1007/978-3-319-56614-6_9
17. b16: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun. "Deep Residual Learning for Image Recognition". 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2016-06-27. DOI: 10.1109/cvpr.2016.90
18. b17: E Biham, R Chen. "Advances in Cryptology – CRYPTO 2004". Advances in Cryptology -CRYPTO 2004, 24th Annual International Cryptolo-gyConference. 2004-08-15. DOI: 10.1007/b99099
19. b18: Jae-Han Lee, Minhyeok Heo, Kyung-Rae Kim, Chang-Su Kim. "Single-Image Depth Estimation Based on Fourier Domain Analysis". 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2018-06-18. DOI: 10.1109/cvpr.2018.00042
20. b19: C Schuldt, I Laptev, B Caputo. "Recognizing human actions: a local SVM approach". Proceedings of the 17th International Conference on Pattern Recognition, 2004. ICPR 2004.. 2004-08-23. DOI: 10.1109/icpr.2004.1334462
21. b20: Fabio Tosi, Filippo Aleotti, Matteo Poggi, Stefano Mattoccia. "Learning Monocular Depth Estimation Infusing Traditional Stereo Knowledge". 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 2019-06-16. DOI: 10.1109/cvpr.2019.01003
22. b21: Yi Chen, Li Yu, Kaoru Ota, Mianxiong Dong. "Hierarchical Posture Representation for Robust Action Recognition". IEEE Transactions on Computational Social Systems. 2019-10. DOI: 10.1109/tcss.2019.2934639
23. b22: D P Kingma, J Ba. "Information Processing in Cells and Tissues". 3rd International Conference on Learning Representations, ICLR 2015. 2015-05-07. DOI: 10.1007/978-3-319-23108-2
24. b23: F Chollet. Keras. 2015
25. b24: Farzaneh Abed, Eik List, Stefan Lucks, Jakob Wenzel. "Differential Cryptanalysis of Round-Reduced Simon and Speck". Lecture Notes in Computer Science. 2014-03-03. DOI: 10.1007/978-3-662-46706-0_27
26. b25: R Roelofs, V Shankar, B Recht, S Fridovich-Keil, M Hardt, J Miller, et al.. "A metaanalysis of overfitting in machine learning". Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019. 2019-12-08
27. b26: M Wang. "Progress in Cryptology – AFRICACRYPT 2008". Progress in Cryptology -AFRICACRYPT 2008, First International Conference on Cryptology in Africa. 2008-06-11. DOI: 10.1007/978-3-540-68164-9
28. b27: Eli Biham, Adi Shamir. "Differential cryptanalysis of DES-like cryptosystems". Journal of Cryptology. 1991-01. DOI: 10.1007/bf00630563
