# Neural Aided Statistical Attack for Cryptanalysis

**Authors:** No Institute No Institute

**Source PDF:** `2020_chen_yu_neural_aided_statistical_attack_eprint.pdf`

## Abstract

In Crypto'19, Gohr proposed the first deep learning-based key recovery attack on 11-round Speck32/64, which opens the direction of neural aided cryptanalysis. Until now, neural aided cryptanalysis still faces two problems: (1) the attack complexity estimations rely purely on practical experiments. There is no theoretical framework for estimating theoretical complexity. (2) it does not work when there are not enough neutral bits that exist in the prepended differential. To the best of our knowledge, we are the first to solve these two problems. In this paper, we propose a Neural Aided Statistical Attack (NASA) that has the following advantages: (1) NASA supports estimating the theoretical complexity. (2) NASA does not rely on any special properties including neutral bits. (3) NASA is applicable to large-size ciphers. Moreover, we propose three methods for reducing the attack complexity of NASA. One of the methods is based on a newly proposed concept named Informative Bit that reveals an important phenomenon. Four attacks on 9-round or 10-round Speck32/64 are executed to verify the correctness of NASA. To further highlight the advantages of NASA, we have performed a series of experiments. At first, we apply NASA and Gohr's attack to round reduced DES. Since NASA does not rely on neutral bits, NASA breaks 10-round DES while Gohr's attack breaks 8-round DES. Then, we compare the time consumption of attacks on 11round Speck32/64. When the newly proposed three methods are used, the time consumption of NASA is almost the same as that of Gohr's attack. Besides, NASA is applied to 13-round Speck32/64. At last, we introduce how to analyze the resistance of large-size ciphers with respect to NASA, and apply NASA to 14-round Speck96/96. The code of this paper is available at https://github.com/AI-Lab-Y/NASA . Our work arguably raises a new direction for neural aided cryptanalysis.

## Introduction

Deep learning has received much expectation in the cryptography community since the last century. Rivest in [17] reviewed various connections between machine learning and cryptography. Some possible directions of research in cryptanalytic applications of machine learning were also suggested. Greydanus proved that a simplified version of Enigma can be simulated by recurrent neural networks [14] .

Although deep learning has shown its superiorities in various fields such as computer vision [16] , natural language processing [3] , and smart medical [8] , its application in the field of conventional cryptanalysis has been stagnant. A few valuable applications are only concentrated in the side-channel analysis [7, 15] .

In Crypto'19, Gohr proposed a deep learning-based distinguisher [13] that is also called neural distinguisher (N D). By placing a differential before N D, Gohr developed a key recovery attack on 11-round Speck32/64, which shows considerable advantages in terms of attack complexity over the differential attack [5] . In Eurocrypto'20, Benamira et al [2] presented a deeper analysis of N D.

In [13] , each key guess corresponds to a key rank score that is directly determined by the output of N D. A key guess is returned as a candidate when its key rank score exceeds a threshold. Since the output of N D is unpredictable and the threshold is set without any theoretical basis, the adversary does not foresee the required data complexity to attack a specific cipher. As a result, the estimation of the attack complexity and success rate must rely on practical experiments that are finished within an acceptable runtime. This is unfavorable for evaluating the security of ciphers against machine learning. Besides, when a differential is placed before N D, enough neutral bits [4] must exist in this prepended differential. Otherwise, the attack in [13] does not work.

In this paper, we have explored neural aided cryptanalysis and made contributions as follows.

-We propose a Neural Aided Statistical Attack (NASA) which supports theoretical complexity estimation and does not rely on neutral bits. NASA is based on a neural aided statistical distinguisher. And the key recovery is transformed into the distinguishing between two normal distributions, which tells the required data complexity of NASA. Four attacks on 9-round or 10round Speck32/64 proves the correctness of NASA. Experiments on round reduced DES further prove that NASA has more potential than Gohr's attack when there are not enough neutral bits. -We propose three methods to reduce the attack complexity of NASA. The first one is reducing the key space by building N D on partial ciphertext bits. This method comes from the truth that only partial ciphertext bits have a significant influence on N D. We call these bits informative bits and propose a Bit Sensitivity Test to identify them. The initial N D proposed by Gohr takes the complete ciphertext pair as input, which forces the adversary to guess all the key bits simultaneously. By building N D on partial informative bits, the adversary guesses partial key bits at a time. The second one is a highly selective Bayesian key search algorithm. It allows the adversary to search for the most promising key guesses instead of traversing all the key guesses. The third one is reducing the data complexity by exploiting neutral bits. When there are available neutral bits, the data complexity of NASA can be reduced. When these three methods are adopted, the average time consumption of NASA on 11-round Speck32/64 is almost the same as that of Gohr's attack.

-At last, we introduce how to analyze the resistance of large-size ciphers with respect to NASA by applying NASA to 14-round Speck96/96. A practical attack on 10-round Speck96/96 is provided together.

Organization Sections 3, 4 presents the neural aided statistical distinguisher and NASA respectively. The three optimization methods are introduced in sections 5, 6, 7. Applications to DES, Speck32/64, and Speck96/96 are presented in sections 8, 9, 10. At last, we summarize this paper and provide more discussion.


## Related Work

Let (P 0 , P 1 ) denote a plaintext pair with difference ∆P . The corresponding intermediate states, ciphertexts are (S 0 , S 1 ), (C 0 , C 1 ).


## Neutral Bit

Consider a differential ∆P → ∆S. Let E denote the encryption function covering the differential. We denote the probability that the following condition holds as the neutrality of the j-th bit E(P 0 ⊕ e j ) ⊕ E(P 1 ⊕ e j ) = ∆S, e j = 1 j, where (P 0 , P 1 ) stands for plaintext pairs conforming to the differential. If the neutrality is 1, the j-th bit is called a neutral bit [4] .

Based on k neutral bits {j 1 , • • • , j k } and a plaintext pair (P 0 , P 1 )|P 0 ⊕ P 1 = ∆P , we can generate a plaintext structure consisting of 2 k plaintext pairs. Once (P 0 , P 1 ) satisfies the differential, the remaining 2 k -1 plaintext pairs also conform to the differential.


## Neural Distinguisher

The target of N D [13] is to distinguish two classes of ciphertext pairs

where Y = 1 or Y = 0 is the label of (C 0 , C 1 ). If the difference between S 0 and S 1 is the target difference ∆S, the pair (C 0 , C 1 ) is regarded as a positive sample drawn from the target distribution. Otherwise, (C 0 , C 1 ) is regarded as a negative sample that comes from a uniform distribution. A neural network is trained over N 2 positive samples and N 2 negative samples. The neural network can be used as an N D if the distinguishing accuracy over a testing database is higher than 0.5. The training pipeline refers to [13] .

Given a sample (C 0 , C 1 ), N D will output a score Z which is used as the posterior probability

When Z > 0.5, the predicted label of (C 0 , C 1 ) is 1 [13] . In this paper, let N D h denote an h-round neural distinguisher.


## Gohr's Key Recovery Attack

Algorithm 1 summarizes the core idea of the basic version (unaccelerated version) of Gohr's key recovery attack [13] .


## Algorithm 1 Basic version of Gohr's key recovery attack

Require: k neutral bits that exist in ∆P → ∆S; An N D built over ∆S;

A key rank score threshold, c1; A maximum number of iterations. Ensure: A possible key candidate.

1: repeat 2: Random generate a plaintext pair (

Create a plaintext structure consisting of 2 k plaintext pairs by k neutral bits; 4:

Collect corresponding ciphertext pairs, (C i 0 , C i 1 ), i ∈ {1, • • • , 2 k }; 5:

for each key guess kg do 6:

Partially decrypt 2 k ciphertext pairs with kg; 7:

Feed decrypted ciphertext pairs to N D and collect the outputs; 8:

Calculate the key rank score v kg based on collected outputs

where Zi is the output of N D. 9:

if v kg > c1 then 10:

stop the key search and return kg as the key candidate; 11:

end if 12:

end for 13: until a key candidate is returned or the maximum number of iterations is reached.

The rank score v kg is likely to exceed c 1 only when the plaintext structure passes the prepended differential and kg is the right key. If the plaintext structure does not pass the differential or the key guess is wrong, the rank score should be very low. Thus, the right key can be identified by comparing the rank score with a threshold. When the performance of N D is weak, 2 k needs to be large. Then more neutral bits are required.


## Distinguishing between Two Normal Distributions

Consider two normal distributions: N (µ r , σ r ), and N (µ w , σ w ). A sample s is sampled from either N (µ r , σ r ) or N (µ w , σ w ). We have to decide if this sample is from N (µ r , σ r ) or N (µ w , σ w ).

The decision is made by comparing the value s to some threshold t. Without loss of generality, assume that µ r > µ w . If s t, the decision is s ∈ N (µ r , σ r ). If s < t, the decision is s ∈ N (µ w , σ w ). Then there are error probabilities of two types:

When a sample s is sampled from N (µ r , σ r ), the probability that the decision is s ∈ N (µ w , σ w ) is β r .

Here a condition is given on µ r , µ w , σ r , σ w such that the error probabilities are β r and β w . The proof can refer to related research [11, 12] .

Proposition 1. For the test to have error probabilities of at most β r and β w , the parameters of the normal distribution N (µ r , σ r ) and N (µ w , σ w ) with µ r = µ w have to be such that

where z 1-βr and z 1-βw are the quantiles of the standard normal distribution.


## Neural Aided Statistical Distinguisher


## A Chosen Plaintext Statistical Distinguisher

Consider a cipher E and a differential ∆P p0 -→ ∆S where ∆P, ∆S ∈ F m 2 and p 0 is the transition probability. Build an N D over ∆S. Randomly generate N plaintext pairs with a difference ∆P and collect corresponding ciphertext pairs. The adversary needs to distinguish between this cipher and a random permutation.

The concrete process is as follows. For each ciphertext pair C i 0 , C i 1 , i ∈ {1, • • • , N }, the adversary feeds it into the N D and obtains its output Z i . Setting a threshold value c 2 , the adversary calculates the statistic T

When p 0 > 2 -m holds, it's expected that the value of the statistic T for the cipher is higher than that for a random permutation. In a key recovery setting, the right key will result in the statistic T being among the highest values for all candidate keys if N is large enough. Next, we give this a theoretical analysis.


## Distribution of the Statistic under Right and Wrong keys

First, we regard a ciphertext pair as a point in a high-dimensional space. For a given threshold c 2 , it is equivalent to creating a stable classification hyperplane in this space using an N D. Thus the classification over a ciphertext pair is modeled as a Bernoulli experiment. It provides us with a theoretical analysis framework.

According to the key recovery process, there are four possible situations when we decrypt a ciphertext pair with a key guess kg as shown in Fig. 1: • Decrypting a positive sample with the right key: the ciphertext pair satisfies the differential and the key guess is right.

• Decrypting a positive sample with wrong keys: the ciphertext pair satisfies the differential but the key guess is wrong. • Decrypting a negative sample with the right key: the ciphertext pair does not satisfy the differential but the key guess is right.

• Decrypting a negative sample with wrong keys: the ciphertext pair does not satisfy the differential and the key guess is wrong.

Given an N D, we denote the probability of Z > c 2 as p 1 , p 2 , p 3 , p 4 for the four situations respectively. Then the distributions of the statistic (formula 6) in these four situations are

if N 1 , N 2 , N 3 , N 4 are high enough. N (µ i , σ i ) is a normal distribution with mean µ i and standard deviation σ i , i ∈ {1, 2, 3, 4}. An empirical condition is

If the probability of the differential ∆P → ∆S is p 0 and N ciphertext pairs are collected randomly, then

Besides, the distributions of the statistic (formula 6) under the right key and wrong keys are both a mixture of two normal distributions.

Right key guess This case contains two situations in which corresponding distributions are N (µ 1 , σ 1 ) and N (µ 3 , σ 3 ). Since a mixture of two independent normal distributions is still a normal distribution, the distribution of the statistic (formula 6) under the right key guess is:

Wrong key guess This case also contains two situations in which corresponding distributions are N (µ 2 , σ 2 ) and N (µ 4 , σ 4 ). Then the distribution of the statistic (formula 6) under wrong key guesses is:

Negative samples in the high-dimensional space approximately obey uniform distribution, thus p 3 = p 4 holds theoretically and experiments also verify it. Since the accuracy of N D is higher than 0.5, p 1 > p 2 also holds with a high probability. When we set c 2 = 0.5, we ensure p 1 > p 2 . Thus µ r > µ w also holds.

Since the distributions of T r , T w are different, the right key can be recovered based on Proposition 1.


## Data Complexity of the Statistical Distinguisher

Based on Proposition 1, one obtains the condition:

where the values of µ r , σ r , µ w , σ w refer to formula 10, 11, 13, 14 respectively. In a key recovery setting, 1 -β r is the minimum probability that the right key survives, β w is the maximum probability that wrong keys survive. Since we do not know the real classification hyperplane learned by N D, p 1 , p 2 , p 3 , and p 4 are estimated experimentally. Then the estimated values of p 3 and p 4 will be slightly different even they should be theoretically equal. When the probability p 0 of the differential is very low, the slight distinction p 3 -p 4 may dominate µ r -µ w , which is wrong. Thus we neglect the minor difference and replace p 3 , p 4 with p n .

Then the condition (formula 15) is simplified as

where

The decision threshold t is:

The data complexity N is directly calculated when β r and β w are set. The impacts of p 0 , p 1 , p 2 , p n on N are about O(p -2 0 ), O((p 1 -p 2 ) -2 ), O(p n ) respectively. The proof is presented in Appendix A.


## Estimation of p 1 , p n

Consider an N D against a cipher, the values of p 1 , p n are estimated as:

1. Randomly generate M positive/negative samples and decrypt them for 1 round with the right/wrong subkeys. 2. Feed partially decrypted samples into N D.


## Calculate the final ratio of Z > c 2 .

The ratio is the statistical expectation of p 1 or p n . A large M can make the statistical expectation accurate enough.


## Further Analysis and Estimation of p 2

When we decrypt a positive sample with a wrong key guess (Fig. 1 (2)), the final value of p 2 is related to the Hamming distance between the wrong key guess and the right key. Such a phenomenon is based on Property 1 and Property 2. Property 1. Decrypt a ciphertext for one round with two different subkeys,

If kg 1 and kg 2 are only different at a few bits (e.g. just 1 bit or 2 bits), the Hamming distance between C 1 h-1 and C 2 h-1 will be very small in high probability.

Property 2. Consider a neural network F (•). If two input samples s 1 , s 2 are very close to each other in the input space, two outputs F (s 1 ), F (s 2 ) of the neural network may satisfy F (s 1 ) ≈ F (s 2 ) in high probability.

Although the distance metric in the input space of neural networks is complex and unknown, the Hamming distance is a good alternative. Thus, it is expected that p 2 is related to the Hamming distance between the right key and wrong key guesses.

Suppose we decrypt a positive sample (C h+x,0 , C h+x,1 ) with x subkey guesses simultaneously

where kg h+j is the subkey guess of the (h + j)-th round. (C h,0 , C h,1 ) is fed into an N D for estimating the probability of Z > c 2 .

When the last x -1 subkey guesses kg h+j , j ∈ [2, • • • , x] are all right, (C h+1,0 , C h+1,1 ) is still a positive sample. Then the final probability of Z > c 2 would be high if kg h+1 is different from the right subkey at few bits. However, if kg h+j , j ∈ {2, • • • , x} are not all right, (C h+1,0 , C h+1,1 ) is not a positive sample anymore. Then the final probability of Z > c 2 is closer to p n .

Thus, we consider x Hamming distances for estimating p 2 at first. Let d j denotes the Hamming distance between the right subkey and subkey guess in the

Require: a cipher with a subkey size of m; an N D h built over ∆P ; M random plaintext pairs, (P i 0 , P i 1 ),

1: Encrypt each plaintext pair (P i 0 , P i 1 ) with a master key M Ki for h + x rounds; 2: Save the ciphertext pair (C i 0 , C i 1 ) and subkeys sk i h+j , j ∈ {1, • • • , x}; 3: for d1 = 0 to m, • • • , dx = 0 to m do 4:

for i = 1 to M do 5:

Randomly draw x subkey guesses kg i j , j ∈ {1, • • • , x} where the Hamming distance between kg i j and sk i h+j is dj; 6:

Decrypt (C i 0 , C i 1 ) with kg i j , j ∈ {1, • • • , x} for x rounds; 7:

Feed the decrypted ciphertext pair into N D h and save the output as Z i|d 1 ,••• ,dx ; 8:

end for 9:

Count the number of Z i|d 1 ,••• ,dx > c2, and denote it as

Verification. Gohr provided N D 5 , N D 6 , N D 7 , N D 8 against Speck32/64 [13] , which are built over a plaintext difference (0x0040, 0). We have performed tests on these four distinguishers. Let M = 10 7 , Table 1 and Table 2 show the estimation results of p 2|d1 and p 2|d1,d2 respectively.

Table 1 . The estimation of p 2|d 1 of 4 neural distinguishers against round reduced Speck32/64. For N D5, N D6, N D7, c2 = 0.55. For N D8, c2 = 0.5. p 2|d 1 =0 = p1. Only four decimal places are presented in this paper. Actually, we kept more decimal places during follow-up experiments.


## N D5

0 1 2 3 4 5 6 7 8 ∼ 16 p 2|d 1 0.8889 0.5151 0.3213 0.2168 0.1556 0.1189 0.0956 0.08 0.0694 N D6 d1 0 1 2 3 4 5 6 7 8 ∼ 16 p 2|d 1 0.6784 0.4430 0.3135 0.2394 0.1958 0.1691 0.1522 0.1410 0.1336 N D7 d1 0 1 2 3 4 5 6 7 8 ∼ 16 p 2|d 1 0.4183 0.3369 0.2884 0.2607 0.2442 0.234 0.2276 0.2236 0.2211 N D8 d1 0 1 2 3 4 5 6 7 8 ∼ 16 p 2|d 1 0.5183 0.5056 0.4993 0.4958 0.4939 0.4927 0.4925 0.4918 0.4917

The test results have verified the analysis of p 2 . When two subkeys are guessed simultaneously, p 2|d1,d2 decreases sharply even if the subkey guess of the last round is wrong at only 1 bit.

Table 2 . the estimation of p 2|d 1 ,d 2 of N D7 against Speck32/64. c2 = 0.55. the columns correspond to d2. the rows correspond to d1. all results only retain two decimal places. the same value is replaced by an uppercase letter. Y = 0.21, E = 0.22, J = 0.23, U = 0.25, and V = 0.26. 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16

Thus, the choice of p 2 depends on the target of the key recovery attack. If we think the attack is successful as long as the Hamming distance between the subkey guess and the right subkey does not exceed a threshold d, the value of p 2 should be

This choice is based on the following truth. By setting a proper threshold c 2 such as c 2 0.5, we ensure

According to formula 16, the higher p 2 is, the higher the required data complexity is. The decision threshold also increases when p 2 increases. Thus we only need to focus on the highest data complexity required for filtering wrong keys. Take N D 7 as an example. Let d = 2, it means that the attack is successful if the recovered subkey is different from the right subkey at most 2 bits. Then p 2 = p 2|3 = 0.2607 or p 2 = p 2|0,1 = p 2|3,0 = 0.26.


## Neural Aided Statistical Attack


## Key Recovery Attack Model

This neural aided statistical distinguisher is used to determine whether a key guess may be the right key. This is done by the Statistical Test as shown in Algorithm 3. Algorithm 4 summarizes the Neural Aided Statistical Attack (NASA) based on the statistical distinguisher.


## Algorithm 3 Statistical test for a key guess

Require: An N D; A key guess, kg;

A posterior probability threshold, c2; The decision threshold, t; N ciphertext pairs (C i 0 , C i 1 ) encrypted from (P i 0 , P i 1 ), P i 0 ⊕ P i 1 = ∆P, i ∈ [1, N ]. 1: Decrypt N ciphertext pairs with kg; 2: Feed decrypted ciphertext pairs into N D, and collect the outputs Zi, i ∈ [1, N ]; 3: Calculate the statistic T in formula 6; 4: if T t then 5:

Return kg as a key candidate. 6: end if


## Algorithm 4 Neural Aided Statistical Attack

Require: The attacked cipher;

The differential with a probability of p0, ∆P Perform the statistical test (Algorithm 3); 8: end for 9: Test surviving key candidates against a necessary number of plaintext-ciphertext pairs according to the unicity distance for the attacked cipher.


## Verification of the Key Recovery Attack Model

Four practical attacks on h-round Speck32/64 are performed to verify NASA. The target is to recover the last subkey sk h . It's expected that returned subkey guesses are different from sk h at most d = 2 bits. NASA should work as long as the adopted N D has a distinguishing accuracy higher than 0.5. Besides, the data complexity should be correctly estimated once ∆P p0 -→ ∆S, N D, d, β r , and β w are provided. Thus, different settings about these factors are considered.

Four distinguishers N D 5 , N D 6 , N D 7 , N D 8 provided by Gohr [13] are adopted. Table 3 shows two different differentials adopted in the verification. Since no key addition happens in Speck before the first nonlinear operation, these two differentials can be extended to a 2/3-round differential respectively.

The verification plan consists of three steps:

1. Set the value of β r , β w . Calculate the data complexity N (formula 16). 2. Perform NASA 100 times with N samples.


## Check the following observation indexes: (a)

The ratio that the right subkey (d 1 = 0) survives. Table 4 summarizes the settings related to four attacks. Table 1 shows the estimations of p 2|d1 related to N D 5 , N D 6 , N D 7 , N D 8 . The value of p 2 is p 2|d1=3 in four attacks. Attack 1: recover sk 9 of 9-round Speck32/64 In the first attack setting, we get N = 15905 ≈ 2 13.957 ( see formula 16) . The decision threshold is t = 758. The right subkey (d 1 = 0) should survive with a 1 -β r = 0.995 probability at least. Wrong subkey guesses (d 1 3) should survive with a β w = 2 -16 probability at most. The number of surviving subkey guesses should not exceed 137 + (2 16 -137) × 2 -16 = 137.998.

After performing this attack 100 times, we find:

-The right key (d 1 = 0) has survived in all the 100 experiments.

-The average number of surviving subkey guesses is 18.41.

-The number of surviving subkey guesses does not exceed 137.998 in 100 experiments.

Attack 2: recover sk 9 of 9-round Speck32/64 In the second attack setting, N = 475 ≈ 2 8.893 and t = 101. The number of surviving subkey guesses should not exceed 137 + (2 16 -137) × 2 -16 ≈ 137.998. After performing this attack 100 times, we find:

-The right subkey has survived in all the 100 experiments.

-The average number of surviving subkey guesses is 33.43.

-The number of surviving subkey guesses does not exceed 137.998 in 100 experiments.

Attack 3: recover sk 10 of 10-round Speck32/64 In the third attack setting, N = 5272 ≈ 2 12.364 and t = 1325. The number of surviving subkey guesses should not exceed 137 + (2 16 -137) × 2 -16 ≈ 137.998. After performing this attack 100 times, we find:

-The right subkey (d 1 = 0) has survived in 99 experiments.

-The average number of surviving subkey guesses is 63.54.

-The number of surviving subkey guesses does not exceed 137.998 in 98 experiments.

Attack 4: recover sk 10 of 10-round Speck32/64 N D 8 is a very weak distinguisher. Its distinguishing accuracy is only about 0.518. In the fourth attack setting, N = 25680 ≈ 2 14.65 and t = 13064. The number of surviving subkey guesses should not exceed 137 + (2 16 -137) × 2 -16 ≈ 137.998. After performing this attack 100 times, we find:

-The right subkey (d 1 = 0) has survived in all the 100 experiments.

-The average number of surviving subkey guesses is 77.47.

-The number of surviving subkey guesses does not exceed 137.998 in 85 experiments. In the other 15 experiments, the ratio that subkey guesses with d 1 = 3 survive is a little higher than that in the 85 experiments.

It's clear that these four attacks 1 have achieved the most important two targets of NASA. This proves the Hamming distance is a good distance metric for estimating p 2 . The correctness of NASA is also well verified.


## Reduce the Key Space

So far we need to guess all the bits of the subkey simultaneously since N D takes the complete ciphertext pairs (C 0 , C 1 ) as input. When the subkey has a large size, this is a serious bottleneck.


## An Intuitive Method for Reducing the Key Space

An intuitive method for reducing the key space is building N D on partial ciphertext bits

where C i [0] is the least significant bit of the ciphertext C i , Γ is the subscript set of selected ciphertext bits. Such a method significantly reduces the key space to be searched. But which ciphertext bits should we select for building N D? Can we develop a generic and efficient framework for guiding this selection? In order to better introduce our work for solving these problems, three new concepts are proposed first.

Definition 1 An informative bit is the ciphertext bit that is helpful to distinguish between the cipher and a pseudo-random permutation.

Definition 2 For a cipher reduced to h rounds, the neural distinguisher trained on the complete ciphertexts (C 0 , C 1 ) is denoted as the teacher distinguisher N D t h , the neural distinguisher trained on partial ciphertext bits (ϕ(C 0 , Γ ), ϕ(C 1 , Γ )) is denoted as the student distinguisher N D s h . The teacher distinguisher is viewed as a special student distinguisher.


## Identify Informative Bits by Bit Sensitivity Test

It's clear that student distinguishers should be built on informative bits. However, it's hard to identify informative bits according to Definition 1. Thus we propose an approximate definition of the informative bit.

Definition 3 For an N D t , if the distinguishing accuracy is significantly affected by the j-th bit of C 0 or C 1 , the j-th ciphertext bit is an informative bit.

An N D t works since it has learned knowledge from ciphertext bits. According to Definition 1, only informative bits provide knowledge. Thus the ciphertext bit that has a significant influence on the distinguishing accuracy of N D t must be an informative bit.

Definition 3 does not ensure each informative bit that obeys Definition 1 is identified successfully. But we only care about informative bits that are captured by an N D t . This approximate definition helps develop a simple but effective framework for identifying informative bits.

The proposed framework is named Bit Sensitivity Test (BST). Its core idea is to test whether the distinguishing accuracy of an N D t drops after we remove some knowledge related to the specific bit.

Gohr in [13] has proved that N D t h , h ∈ {5, 6, 7, 8} against Speck32/64 captures the knowledge about the ciphertext difference and some unknown features. Consider the j-th ciphertext bit. We remove the knowledge about the j-th ciphertext bit difference by

where η is a random mask that could be 0 or 1.

We have performed an extreme test on N D t h , h ∈ {5, 6, 7, 8} against Speck32/64. If we XOR each bit of C 0 or C 1 with a random mask, N D t h , h ∈ {5, 6, 7, 8} can not distinguish positive samples and negative samples anymore. These tests imply that knowledge about unknown features is also removed by one of the two operations presented in formula 26.

After the knowledge related to a ciphertext bit is removed, the accuracy decrease of N D t is named Bit Sensitivity, which is used to identify informative bits. Algorithm 5 summarizes the BST.


## Algorithm 5 Bit Sensitivity Test

Require: a cipher with a block size of m;

an N D t against this cipher; a test dataset consisting of M 2 positive samples and M 2 negative samples. Ensure: An array sen that saves the bit sensitivity of m ciphertext bits.

1: Test the distinguishing accuracy of N D t on the test dataset. Save it to sen[m]; 2: for j = 0 to m -1 do 3: for i = 1 to M do 4:

Generate a random mask η ∈ {0, 1}; 5:

Feed the new sample (C i,new 0 , C i 1 ) to N D t ; 7:

end for 8:

Count the current accuracy cp; 9: sen[j] = sen[m] -cp; 10: end for Examples and analysis. We have applied the BST to N D t h , h ∈ {5, 6, 7} against Speck32/64. The results of the BST under three scenarios are shown in Fig. 2 and Fig. 3 respectively.

We observe that sen 0 ≈ sen 1 . This proves that C 0 ⊕ (η j) is equivalent to C 1 ⊕ (η j). Besides, we know -If sen 0 [j] > 0, the j-th ciphertext bit is an informative bit.

-If sen 0,1 [j] > 0, the j-th ciphertext bit provides some useful unknown features. Since the knowledge about the bit difference is not removed, then only useful unknown features can lead to a decrease in the accuracy. -If sen 0 [j] ≈ sen 0,1 [j], the j-th ciphertext bit difference has little influence on N D t h . Reverse verification about identified informative bits. To further verify Definition 3, a reverse verification about identified informative bits is performed. First, select some informative bits. Second, train an N D s on selected informative bits and observe the distinguishing accuracy.

Taking N D t 7 against Speck32/64 as an example, we have performed the reverse verification based on results in Fig. 3(b) . Table 5 shows the distinguishing accuracies under two settings. For Speck32/64, the j-th and (j + 16)-th bit are (a) (b) Fig. 3. Results of BST of N D t 6 (a) and N D t 7 (b) against Speck32/64, M = 10 6 .

directly related to the same subkey bit. Thus the 8-th and 1st ciphertext bits are also considered. The accuracy of N D t 7 is 0.6067. When all the identified informative bits are considered, the resulted N D s 7 obtains a distinguishing accuracy of 0.6065, which is almost the same as 0.6067. Such an experiment shows that Definition 3 can help identify all the ciphertext bits that have a significant influence on teacher distinguishers.

Once informative bits are identified by the Bit Sensitivity Test, the whole key space can be divided into several subspaces. In each subspace, NASA is performed to recover specific key bits. This informative-bit-based method is the first generic technique for reducing the attack complexities of NASA.


## Selective Key Search

In Algorithm 4, each possible key guess kg is tested. Inspired by the analysis of p 2 in Section 3.5, we develop a highly selective key search strategy for further reducing the attack complexity.

Specifically, we do not need to traverse all the key guesses. Some key guesses that are most likely to be the right key are recommended based on the key guesses that have been tested.


## Distribution of the Statistic Under Different Keys

We discuss the distribution of the statistic (formula 6) under different keys again. We still take Fig. 1 as an example.

Suppose that the size of the key guess kg is m. According to the analysis in Section 3.5, we know there are the following m + 1 probabilities

where d 1 is the Hamming distance between kg and the right key.

Then there are m + 1 distributions of the statistic (formula 6)

The parameters of these m + 1 distributions are obtained offline. These distributions are used as prior knowledge to develop a Bayesian key search strategy.


## Bayesian Key Search Strategy

Algorithm 6 summarizes the newly proposed Bayesian key search algorithm, which is the second technique for reducing the attack complexities of NASA.


## Reduce the Data Complexity

Consider the prepended differential ∆P p0 -→ ∆S. As we have presented in section 3.3, the impact of p 0 on the data complexity is about O(p -2 0 ). Neutral bits seldom exist in a long differential characteristic. But there usually are numerous neutral bits in a short differential characteristic. This section shows how to reduce the data complexity of NASA by neutral bits.


## Algorithm 6 Bayesian Key Search Algorithm

Require: Ciphertext pairs, (C i 0 , C i 1 ), i ∈ {1, • • • , N }; A neural distinguisher, N D; Prior knowledge µ d 1 and σ d 1 , d1 ∈ {0, • • • , m}; The number of key guess candidates to be generated within each iteration, n cand ; The number of iterations, niter. Ensure: The list L of tuples of recommended key guesses and statistics.

1: K = {kg 1 , • • • , kg cand } ← choose n cand values at random without replacement from the set of all subkey candidates. 2: L ← {} 3: for t = 1 to niter do 4:

for each kg ∈ K do 5:

for i = 1 to N do 6:

Decrypt C i 0 , C i 1 with kg. 7:

Feed partially decrypted ciphertext pair into N D. 8:

Collect the output Z i,kg of N D. 9:

end for 10:

Compute the statistic (formula 6), T kg ; 11:

L ← L||(kg, T kg ). 12:

end for 13:

for sk ∈ {0, • • • , 2 m -1} do 14:

the Hamming distance between kg and sk */ 15: end for 16: K ← argsort sk (λ)[0 : n cand -1]. /* Pick n cand key guesses with the n cand smallest score to form the new set of key guess candidates K */ 17: end for 18: Return L


## Improved Neural Aided Statistical Attack

We still take the key recovery attack with 1-round decryption as an example to introduce the improved NASA.

Its core idea is to divide the long differential into two short ones: ∆P q -→ ∆B, and ∆B p -→ ∆S where p 0 = q × p. The statistical distinguisher only covers the second differential ∆B → ∆S. Neutral bits that exist in the first part ∆P → ∆B are exploited. Algorithm 7 summarizes the details of the improved NASA.

Now, only the impact of p on the total data complexity is O(p -2 ). The impact of q on the total data complexity is O(q -1 ). Thus, the total impact of the prepended differential is O(q -1 p -2 ) instead of O(p -2 0 ) = O(q -2 p -2 ). The data complexity is reduced by a factor of about q -1 .


## Further Improvement Based On Early Stopping

In Algorithm 7, 1 q plaintext structures are generated. But only one plaintext structure P is expected to satisfy the differential ∆P → ∆B.


## Algorithm 7 Improved neural aided statistical attack

Require: The attacked cipher;

The prepended differential, ∆P q -→ ∆B p -→ ∆S; Neutral bits that exist in ∆P → ∆B; Two maximum error probabilities, βr, βw; A posterior probability threshold, c2. Ensure: All possible key candidates.

1: Train an N D over ∆S; 2: Estimate p1, pn, p2 using N D (Section 3.4, Algorithm 2); 3: Calculate the data complexity N1 based on p, p1, pn, p2 (Section 3.3); 4: for j from 1 to 1 q do 5:

Based on ∆P and neutral bits, randomly generate a plaintext structure P consisting of N1 plaintext pairs. 6:

Perform the basic NASA based on P (Algorithm 4). 7: end for 8: Test surviving key candidates against a necessary number of plaintext-ciphertext pairs according to the unicity distance for the attacked cipher.

This plaintext structure is called valid plaintext structure while other plaintext structures are called invalid plaintext structures. If a valid plaintext structure is identified once it arises, Algorithm 7 can be early stopped at step 4.

We propose an identification method that does not change the process of Algorithm 7. At a high level, the identification method is as follows:

1. Generate a plaintext structure P consisting of M plaintext pairs. 2. Filter key guesses based on the statistic T (formula 6) and a decision threshold t M . 3. If the number of surviving key guesses exceeds a threshold t P , P is a valid plaintext structure.

By setting proper parameters t M , the number of surviving key guesses exceeds t P only when P is a valid plaintext structure. Next, we present a theoretical analysis of M, t M , t P . For convenience, we rewrite the statistic T (formula 6) as

The four situations as shown in Fig. 1 also exist in this identification process.

The following notations are adopted again:

p 2|d1 : the probability P r{Z > c 2 |S 0 ⊕S 1 = ∆S} when the Hamming distance between the key guess and the right key is

Distribution of the statistic under valid plaintext structures When P is a valid plaintext structure that satisfies ∆P → ∆B, there are M × p positive samples and M × (1 -p) negative samples.

At first, we do not set d 1 clearly and denote p 2|d1 as p V . The distribution of the statistic(formula 28) is

Select a specific d 1 , we have p V = p 2|d1 . Let K V denote the set of key guesses with a Hamming distance d 1 from the right key. Then only kg ∈ K V makes the above T V hold.


## Distribution of the statistic under invalid plaintext structures

When P is an invalid plaintext structure, all the M samples are negative samples.

The distribution of the statistic(formula 28) is

Let K denote the set of all possible key guesses. Then any kg ∈ K makes the above T I hold.

Distinguishing between T V and T I Since T V and T I are two different normal distributions, the technique in Section 2.4 is used to distinguish these two distributions. According to Proposition 1, the condition for distinguishing T V and

where

and s stands for a sample. We present a deeper explanation about the two error probabilities β I , β V . When P is an invalid plaintext structure, the maximum probability that key guesses kg ∈ K survive the attack is β I . When P is a valid plaintext structure, the minimum probability that key guesses kg ∈ K V survive the attack is 1

By simplifying formula 34, we know that the required data complexity M is

And the decision threshold t M is

where z 1-β V and z 1-β I are the quantiles of the standard normal distribution.

Identify valid plaintext structures by counting surviving keys When P is a valid plaintext structure, The lower bound of the number of surviving subkeys is

. When P is an invalid plaintext structure, The upper bound of the number of surviving subkeys is |K| × β I . By setting two proper error probabilities β V , β I , we ensure the following condition always holds

Let t P satisfy the following condition

where x y means that x is much larger than y here. Then valid plaintext structures is identified by by comparing the number of surviving subkey guesses with t P foot_2 .


## Algorithm 8 Identify valid plaintext structures

Require: a plaintext structure P with a size of M (formula 37); an N D trained over ∆S; the posterior probability threshold c2; a decision threshold tM for filtering subkey guesses; a decision threshold tP for identifying valid plaintext structures. Ensure: the classification of P.

1: Collect the M ciphertext pairs corresponding to P; 2: Initialize a counter cp ← 0; 3: for each possible subkey guess kg do 4: Decrypt M ciphertext pairs with kg; 5:

Feed partially decrypted ciphertext pairs into N D; 6:

Save the outputs of N D, Zi, i ∈ [1, M ]; 7:

Count the number of Zi > c, and denote it as TM ; 8:

if TM > tM then 9:

cp ← cp + 1; 10:

end if 11: end for 12: if cp tP then 13:

Return 1 (P is a valid plaintext structure). 14: else 15:

Return 0 (P is an invalid plaintext structure). 16: end if Algorithm 8 summarizes the concrete identification process. Since the identification is based on the same statistic as the key recovery, Algorithm 8 and Algorithm 7 are able to be performed simultaneously. The necessary condition is that the size of a plaintext structure P should exceed N 1 and M . Further analysis about p V . The data complexity M is related to p V . And p V is related to the Hamming distance d 1 .

When p V increases, M (Equation 37 ) decreases since

If p V increases, the numerator will decrease and the denominator will increase. Then M will decrease. When the Hamming distance d 1 decreases, p 2|d1 will increase in high probability. But the number of subkey guesses in the subspace may decrease sharply when d 1 decreases, which may make the condition (formula 39) not hold. Thus, there is a trade-off. As long as the condition (formula 39) holds, we advise p V = p 2|d1 where d 1 should be as small as possible.


## Application to DES

This section proves that NASA has more potential than Gohr's attack when enough neutral bits do not exist in the prepended long differential.

DES [9] is a block cipher with a block size of 64 bits. The structure of DES is the classical Feistel structure. Its round function f is given by eight different S-boxes. More details refer to [9] , please. We perform key recovery attacks on round reduced DES.


## Prepended Differentials

Two optimal 2-round iterative differentials found in [6] are 0x19600000/0

Based on these 2-round differentials, we can get longer iterative differentials. These iterative differentials are used as the prepended differential ∆P → ∆S for attacking round reduced DES.

According to the definition of the neutral bit, We measure the neutrality of each ciphertext bit experimentally. We find that 18 neutral bits {33, • • • , 50} exist in the above 2-round iterative differentials. As for 4-round iterative differentials, no neutral bits exist anymore.


## Build Neural Distinguishers Against DES

Let ∆S = 0x19600000/0, we build teacher distinguishers against DES up to 5 rounds. The distinguishing accuracy of the 5-round teacher distinguisher is 0.58.

Based on the BST, we find that 4 bits {39, 50, 56, 61} related to the fifth S-box S5 and 4 bits {59, 37, 43, 49} related to the eighth S-box S8 are all informative bits.

In order to introduce the next experiment more clearly, we focus on the student distinguisher N D s 5 built over the bits {39, 50, 56, 61} for now. Let the posterior probability threshold be c 2 = 0.5, we get p 1 = 0.6041 and p n = 0.4890. Table 6 shows the estimation of p 2|d1 .


## Attack DES with Gohr's Attack

By placing the 2-round differential 0x19600000/0

5 , with the help of the 18 neutral bits {33, • • • , 50}, 8-round DES is broken by Gohr's attack. The 6 key bits related to S5 of the last round are recovered.

Since no neutral bits exist in the 4-round differential 0x19600000/0 234 -2 ----→ 0x19600000/0, 10-round DES can not be broken by Gohr's attack under the current setting.


## Neural Aided Statistical Attack on DES

Consider the basic NASA (Algorithm 4) on 10-round DES foot_3 . We also adopt the 4-round prepended differential 0x19600000/0 234 -2 ----→ 0x19600000/0 and N D s 5 . Let d = 0, we have p 2 = 0.5113 based on Table 6 . Besides, let β r = 0.005, and β w = 2 -6 . Since p 0 = 234 -2 , the required data complexity is N = 2 40.824 chosen plaintext pairs. Since the output of an S-box only contains 4 bits, we build a look-up table offline for saving the tuple ((C 0 , C 1 ), N D s 5 (C 0 , C 1 )). Then the time complexity is not related to N D s 5 anymore. In other words, the time complexity of this attack is N ×2×2 6 = 2 47.824 . Thus, 10-round DES is broken by the basic NASA under the same setting.


## Gohr's Attack on Speck32/64

Based on the 2-round prepended differential ∆P → ∆S and N D t 7 , N D t 6 , Gohr presented a key recovery attack (Algorithm 1) on 11-round Speck32/64. Besides, Gohr provided some optimization techniques for accelerating it.

The target is to recover the last two subkeys sk 10 , sk 11 . Gohr counted a key guess as successful if the last subkey was guessed correctly and if the second subkey was at Hamming distance at most two of the real key sk 10 . Finally, the success rate of Gohr's attack is about 52%.

We have performed this accelerated attack again based on the code provided by Gohr. By adopting an Intel(R) Core(TM) i5-7500 CPU and one graphics card (NVIDIA GeForce GTX 1060(6GB)), we find that the average time consumption of performing this attack one time is about 70 seconds.


## Neural Aided Statistical Attack on Speck32/64

At first, we consider the neural aided statistical attack on 11-round Speck32/64. At a high level, the attack contains five stages:

stage 1: Identify the valid plaintext structure P that satisfies ∆P → ∆B by N D s 7 (Algorithm 8). The subkey to be searched is sk 11 In stage 2, we set p 2 = p 2|d1=3 , β r = 0.005, β w = 2 -8 . The required data complexity is N = 22586 ≈ 2 14.463 plaintext pairs, and the decision threshold for filtering subkey guess is t = 6690.

In stage 3, we filter kg 11 based on each surviving kg 11 [7 ∼ 0]. Let p 2 = p 2|d1=3 , β r = 0.005, β w = 2 -16 , we have N = 5271 ≈ 2 12.364 , t = 1325.

In stage 4, we filter (kg 10 [7 ∼ 0], kg 11 ) based on each surviving kg 11 . Let p 2 = p 2|d1=2 , β r = 0.001, β w = 2 -14 , we have N = 5228 ≈ 2 12.36 , t = 1589.

In stage 5, we filter (kg 10 , kg 11 ) based on each surviving (kg 10 [7 ∼ 0], kg 11 ). Let p 2 = p 2|d1=2 , β r = 0.001, β w = 2 -16 , we have N = 829 ≈ 2 9.697 , t = 180.

We use 16 high probabilistic neutral bits {0, 1, 3 ∼ 5, 11, 14, 15, 20 ∼ 24, 26 ∼ 28} that exist in ∆P → ∆B to generate plaintext structures P consisting of M = 37938 plaintext pairs with a difference ∆P = (0x211, 0xa04). The probability that P is a valid plaintext structure is about 2 -4.2 . In stage 1, if no valid plaintext structures occur after 24 plaintext structures are generated, the attack is stopped and viewed as a failure.

Once one valid plaintext structure P is found, the remaining 4 stages are performed based on this structure P. Moreover, 22586, 5271, 5228, 829 plaintext pairs are selected from this valid plaintext structure respectively. In stage 1 ∼ 5, the proposed Bayesian key search strategy (Algorithm 6) is applied in each stage.

The settings related to the Bayesian key search strategy are as follows. In stage 1 and stage 2, the number of iterations is n iter = 3. For each iteration, we search n cand = 32 subkey guesses. In stage 3, we set n iter = 4, n cand = 32. In stage 4 and stage 5, we set n iter = 3, n cand = 32.

We count a key guess as successful if the right subkey pair (sk 10 , sk 11 ) survives. We have performed 500 experiments under the same hardware environment used in section 9.3, . Valid plaintext structures occurred in 339 experiments and were all identified successfully. The attack was successful in 265 out of 339 trials. Besides, the attack was successful in 4 out of the remaining 161 trials. We find that the invalid plaintext structure in the 4 trials contains many plaintext pairs that pass the differential ∆P → ∆B. The average numbers of surviving key guesses in the last four stages were 8.2, 32.9, 14.8, 11.1 respectively. The average number of generated plaintext structures is 10.73. The average time consumption of this attack is about 77.9 seconds, which is very close to the time consumption of Gohr's attack.

According to the attack settings in stages 2 ∼ 5, the probability that the right keys survive should be (1 -0.005) 2 × (1 -0.001) 2 ≈ 0.988. We argue that the reason why the attack failed in 74 out of 339 experiments is that the sampling randomness is destroyed by neutral bits. To verify this argument, we randomly generate 22586 plaintext pairs with a difference ∆B to form a plaintext structure and have performed the attack 100 times again. The attack was successful in 99 out of 100 trials.

We wonder how many rounds NASA could attack at most. By adopting N D t 8 (let p 2 = p 2|d1=3 ) and 19 neutral bits, we guess and recover sk 13 , sk 12 simultaneously. The theoretical data complexity is about 2 22.73 chosen-plaintext pairs, which is lower than the data complexity (2 25 chosen plaintexts) of the previous best attack [10] on 13-round Speck32/64. For NASA, the basic operation contains two steps: (1) partially decrypt a ciphertext pair with a subkey guess, (2) feed the decrypted ciphertext pair into N D and obtain the output. Under the hardware environment used in section 9.3, it takes about 2.8 seconds to perform 2 20 basic operations with N D t 8 . As a comparison, it takes about 0.28 seconds to process 2 20 key guesses by force key search. Thus, the theoretical time complexity is about δ × 2 22.73+32 where δ = 2.8 0.28 = 10, and 13-round Speck32/64 is broken by NASA 4 .


## Application to Speck96/96

NASA can be used to analyze the resistance of large-size ciphers with respect to deep learning. We introduce the general idea by adopting the application to Speck96/96 [1] as an example.

First, we train a student distinguisher N D s 7 over ∆S = (0x80, 0) by setting Γ = {69 ∼ 56, 21 ∼ 8}. Second, a practical attack foot_5 based on N D s 7 is performed to confirm that NASA is applicable. More precisely, the practical attack is used to verify whether the Hamming distance is a good distance metric for estimating p 2 related to N D s 7 . Third, estimate the theoretical complexity of NASA on round reduced Speck96/96.

By placing a prepended 6-round differential extended from the 5-round differential ∆P = (0x900900480001, 0x11003084008) 2

---→ ∆S = (0x80, 0), we find that the theoretical data complexity for recovering 14 subkey bits sk 14 [13 ∼ 0] of 14-round Speck96/96 is 2 70.22 chosen plaintext pairs. Thus, the theoretical time complexity is δ × 2 70.22+14 where δ ≈ 4.85 under the hardware environment used in section 9.3.


## Conclusion

In this article, we propose a Neural Aided Statistical Attack (NASA) and three methods for reducing the complexity of NASA. NASA recovers the right key based on distinguishing between two different normal distributions. NASA is the first deep learning-based cryptanalysis technique that supports theoretical complexity estimation and does not rely on any special properties such as neutral bits. Applications to round reduced DES, Speck32/64, and Speck96/96 prove the superiorities of NASA.

Our work in this article also provides many inspirations for neural aided cryptanalysis. First, if we replace the neural network with other machine learning models, NASA still works. Thus, it is possible to further accelerate NASA by adopting other machine learning-based distinguishers. Second, when we try to reduce the key space, we find that ciphertext bits have a different influence on the neural distinguisher. This finding is not only useful for neural aided cryptanalysis. The traditional differential attack may be improved by exploiting knowledge extracted from neural distinguishers. Third, the data complexity for distinguishing two normal distributions is very high, which makes the data complexity of basic NASA is also high. If some new probability distributions are more suitable for simulating the key recovery process, new neural aided attacks with a lower complexity are able to be developed. Fourth, if a distance metric is better than the Hamming distance, NASA would give more accurate estimations. At last, the negative influence of neutral bits needs to be further explored.


## A Analysis of the Data Complexity of Basic NASA

The data complexity of NASA is related to N D and the prepended differential. In this appendix, we present the analysis of each part's impact on the data complexity.


## A.1 The Differential's Impact on the Data Complexity

According to formula 16, the data complexity N is affected by the probability p 0 of the prepended differential as where a 5 = 2 × a 4 × a 3 + (a 1 -a 3 )p 0 × a 3 + (a 2 -a 3 )p 0 . Thus the impact of the probability p 0 of the differential is O(p -2 0 ).


## A.2 The Neural Distinguisher's Impact on the Data Complexity

Three probabilities p 1 , p 2 , p n are related to the neural distinguisher. Since p n is related to negative samples and p 1 , p 2 are related to positive samples, we discuss p n separately.

> 1 Fig. 1 . Fig.1. Four situations of decrypting a ciphertext pair with a key guess.

> 0 p 0 - → ∆S; Two maximum error probabilities, βr, βw; A posterior probability threshold, c2. Ensure: All possible key candidates.1: Train an N D over ∆S; 2: Estimate p1, pn, p2 using N D (Section 3.4, Algorithm 2); 3: Calculate the data complexity N and the decision threshold t (Section 3.3); 4: Randomly generate N plaintext pairs (P i 0 , P i 1 ), P i 0 ⊕ P i 1 = ∆P, i ∈ {1, • • • , N }; 5: Collect corresponding N ciphertext pairs, (C i 0 , C i 1 ), i ∈ {1, • • • , N }; 6: for each key guess kg do 7:

> 23 Fig. 2 .Fig. 3 . Fig.2. Results of BST of N D t 5 against Speck32/64, M = 10 6 . sen0 is the results of performing C0 ⊕ (η j), sen1 is the results of performing C1 ⊕ (η j), sen0,1 is the results of performing two operations simultaneously, j ∈ {0, • • • , 31}. Only three decimal places are kept.

> 7 [ 7 ∼ 0]. stage 2: Recover sk 11 [7 ∼ 0] by N D s 7 (Algorithm 4). stage 3: Recover sk 11 by N D t 7 (Algorithm 4). stage 4: Recover (sk 11 , sk 10 [7 ∼ 0]) by N D s 6 (Algorithm4). stage 5: Recover (sk 11 , sk 10 ) by N D t 6 (Algorithm 4). In stage 1, we set p V = p 2|d1=1 , β V = 0.1, β I = 2 -8 . It means that the number of surviving subkey guess kg 11 [7 ∼ 0] should exceed 8 × (1 -0.1) = 7.2 when P is a valid plaintext structure. Otherwise, the number of surviving subkey should not exceed 2 8 ×2 -8 = 1. Based on this setting, each plaintext structure P should contain M = 37938 ≈ 215.211 plaintext pairs. The decision threshold for filtering subkey guesses is t M = 11103. When the number of surviving subkey guess exceeds 7 (t P = 8), P is a valid plaintext structure.

> 13120103233135 √ N = z 1 - 3 (p 1 -p 2 ) × p 0 ∝ z 1 - 0 ∝ a 3 +N ∝ p - 2 0a 3 + a 2 4 a 3 + (a 1 -a 3 + a 2 4 a 2 -a 2 4 a 3 )p 0 + a 5 βr p 0 a 1 + (1 -p 0 )a 3 + z 1-βw p 0 a 2 + (1 -p 0 )a βr a 3 + (a 1 -a 3 )p 0 + z 1-βw a 3 + (a 2 -a 3 )p 0 p (a 1 -a 3 )p 0 + a 4 × a 3 + (a 2 -a 3 )p 0 p 0where a 4 = z 1-βw z 1-βr . We further know

> 3 Table 3 . two options of the prepended differential of Speck32/64. nr is the number of encryption rounds covered by the differential.

> 4 Table 4 . Settings of the four attacks on round reduced Speck32/64. DID is the differential's ID in Table3.

> 5 Table 5 . accuracies of neural distinguishers trained on selected ciphertext bits

> 6 Table 6 . The estimation of p 2|d 1 of N D s 5 against round reduced DES. c2 = 0.5. N D s

> 7 Table 7 . The estimation of p 2|d 1 of N D s 6 , N D s 7 against Speck32/64. c2 = 0.55. The subscript set of selected ciphertext bits is Γ = {30 ∼ 23, 14 ∼ 7}

> 8 Table 8 . The estimation of p1, pn of N D s

## References

1. b0: Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks, Louis Wingers. "The SIMON and SPECK lightweight block ciphers". Proceedings of the 52nd Annual Design Automation Conference. 2015-06-07. DOI: 10.1145/2744769.2747946
2. b1: Adrien Benamira, David Gerault, Thomas Peyrin, Quan Quan Tan. "A Deeper Look at Machine Learning-Based Cryptanalysis". Lecture Notes in Computer Science. 2021. DOI: 10.1007/978-3-030-77870-5_28
3. b2: Y Bengio, R Ducharme, P Vincent. "A neural probabilistic language model". Advances in Neural Information Processing Systems 13, Papers from Neural Information Processing Systems (NIPS) 2000. 2000
4. b3: E Biham, R Chen. "Advances in Cryptology – CRYPTO 2004". Advances in Cryptology -CRYPTO 2004, 24th Annual International CryptologyConference. 2004. DOI: 10.1007/b99099
5. b4: Eli Biham, Adi Shamir. "Differential fault analysis of secret key cryptosystems". Lecture Notes in Computer Science. 1990. DOI: 10.1007/bfb0052259
6. b5: Eli Biham, Adi Shamir. "Differential cryptanalysis of DES-like cryptosystems". Journal of Cryptology. 1991-01. DOI: 10.1007/bf00630563
7. b6: Eleonora Cagli, Cécile Dumas, Emmanuel Prouff. "Convolutional Neural Networks with Data Augmentation Against Jitter-Based Countermeasures". Lecture Notes in Computer Science. 2017. DOI: 10.1007/978-3-319-66787-4_3
8. b7: Yi Chen, Li Yu, Kaoru Ota, Mianxiong Dong. "Robust Activity Recognition for Aging Society". IEEE Journal of Biomedical and Health Informatics. 2018-11. DOI: 10.1109/jbhi.2018.2819182
9. b8: Donald W Davies. "Some Regular Properties of the ‘Data Encryption Standard’ Algorithm". Advances in Cryptology. 1982. DOI: 10.1007/978-1-4757-0602-4_8
10. b9: Itai Dinur. "Improved Differential Cryptanalysis of Round-Reduced Speck". Lecture Notes in Computer Science. 2014. DOI: 10.1007/978-3-319-13051-4_9
11. b10: W Feller. "An introduction to probability theory and its applications". Population. 1968
12. b11: Richard Gisselquist, Paul G Hoel, Sidney C Port, Charles J Stone. "Introduction to Probability Theory.". The American Mathematical Monthly. 1974-11. DOI: 10.2307/2319331
13. b12: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
14. b13: S Greydanus. Learning the enigma with recurrent neural networks. 2017
15. b14: Jaehun Kim, Stjepan Picek, Annelie Heuser, Shivam Bhasin, Alan Hanjalic. "Make Some Noise. Unleashing the Power of Convolutional Neural Networks for Profiled Side-channel Analysis". IACR Transactions on Cryptographic Hardware and Embedded Systems. 2019-05-09. DOI: 10.46586/tches.v2019.i3.148-179
16. b15: Alex Krizhevsky, Ilya Sutskever, Geoffrey E Hinton. "ImageNet classification with deep convolutional neural networks". Communications of the ACM. 2012. DOI: 10.1145/3065386
17. b16: Ronald L Rivest. "Cryptography and machine learning". Lecture Notes in Computer Science. 1991. DOI: 10.1007/3-540-57332-1_36
