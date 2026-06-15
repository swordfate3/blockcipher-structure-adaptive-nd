# On the Explanation and Enhancement of Neural-inspired Differential Cryptanalysis

**Authors:** Weixi Zheng, Liu Zhang, Zilong Wang

**Source PDF:** `2024_theoretical_explanation_improvement_deep_learning_distinguisher.pdf`

## Abstract

Neural networks have been applied to symmetric cryptanalysis, and Gohr demonstrated that a neural-network-based distinguisher achieves higher accuracy than classical differential distinguishers at CRYPTO 2019. In this work, we analyze ciphertext data through the lens of probability distributions, identifying non-random features that provide indirect insights into how neural networks distinguish ciphertexts from random data. In parallel, we improve the key-recovery attack process by adopting the Bayesian-UCB method, which achieves a better balance between exploration and exploitation of ciphertext structures. These enhancements reduce the runtime of key-recovery attacks while simultaneously increasing their success rate.

## Introduction

Recent advances in deep learning have led to remarkable progress across diverse and challenging tasks, ranging from machine translation and autonomous driving to achieving superhuman performance in abstract board games. On the theoretical side, the long-recognized connection between cryptography and machine learning, as highlighted in the survey of [1] , continues to provide valuable insights. At CRYPTO 2019, Gohr [2] introduced differential-neural cryptanalysis, where a neural network is trained as a differential-neural distinguisher (DN D) to separate ciphertext pairs with a fixed input difference from random ones. Since then, numerous works have investigated how neural networks achieve this. Gohr showed that they capture features beyond those exploited in classical differential cryptanalysis. Benamira et al. [3] related this ability to approximating the differential distribution table (DDT). Gohr et al. [4] further proved that, for SIMON32/64, neural networks can rely solely on differential features. More recently, Bao et al. [5] demonstrated that their strong performance on SPECK32/64 stems from leveraging additional features such as Intra-XOR and Cross-XOR.

To extend neural distinguishers to key-recovery attacks, a short classical differential (CD) is often prepended and combined with techniques such as the BayesianKeySearch algorithm, wrong-key response profiling, and the upper confidence bound (UCB) strategy to improve efficiency.

In this work, we pursue two directions: deepening the understanding of neural network mechanisms and improving the efficiency of key-recovery attacks.

• Explanation of the Working Mechanism. From the perspective of probability distributions, we analyze the features embedded in the ciphertext pair of SPECK32/64 and infer that, in addition to classical difference information, ciphertext pairs also contain extra XOR-based features. Based on this observation, we reduce both the dimensionality of the training data and the size of the neural network, while maintaining its performance.

• Improved Key Recovery Attacks. To mitigate the tendency of UCB to become trapped in wrong ciphertext structures, we employ Bayesian-UCB as a new ciphertext-structure selection strategy to strengthen the key-recovery attack process. Furthermore, we refine the BayesianKeySearch algorithm by retaining the highest-scoring key, which reduces errors caused by incorrect ciphertext structures. Combined, these improvements lower the time complexity and substantially increase the success rate of key-recovery attacks on SPECK32/64, as shown in Table 1 .


## Preliminary


## Brief Description of SPECK32/64

Let n be the word size in bits and 2n the state size. Denote the internal state after round i as (C i L , C i R ) and the i-th round subkey as k i . We use ⊕ for XOR, ⊞ for addition modulo 2 n , and ≫ / ≪ for right/left rotation.

SPECK32/64 is a lightweight block cipher from the SPECK family [7] . It encrypts 32-bit blocks with a 64-bit key, using 16-bit words for both state and subkeys. In round i, the state update is:


## Differential Scenario

Given an encryption function E : F np 2 × F n k 2 → F nc 2 , a differential distinguisher separates:

• Encryption samples: (E(p 1 , k), E(p 2 , k)), with p 1 ⊕ p 2 = ∆;

• Random samples: (E(p 1 , k), E(p 2 , k)), with p 1 , p 2 chosen independently at random.

Here, ∆ is a fixed input difference, and p 1 , p 2 , k are uniformly random. In differential-neural cryptanalysis, these are labeled as positive (encryption) and negative (random) examples to train the DN D.


## Explanation of the Working Mechanism

The encryption sample is (c 1 , c 2 ) = (E(k, p), E(k, p ⊕ ∆)), where k and p are uniform. If E(k, •) is bijective, c 1 and c 2 are each uniform, so distinguishing requires analyzing them jointly. Since the key is random, ciphertext bits are independent; however, when c 1 and c 2 are considered together, their differences cancel out the randomness from the last key addition.


## Probability Distribution of Ciphertext Pair for SPECK32/64

According to the round function of SPECK32/64, both X and Y depend on the same subkey K, as illustrated in Equation 1. We consider (X, Y ) = (C i L , C i R ) as the known ciphertext state, and analyze the probability distribution of the ciphertext pair (


## The detailed proof is shown in Appendix A.

As shown in Lemma 1, ciphertext pairs contain not only classical difference information but also XOR relations between the left and right branches within a single ciphertext or between two ciphertexts. This observation is consistent with the conclusion in [5] .


## Lemma Verification through Modified Network Architecture

New Data Format. Previously, the ciphertext pair (X 1 , Y 1 , X 2 , Y 2 ) was used directly as network input. By Lemma 1, SPECK32/64 ciphertexts yield only six distinct difference combinations. Thus, we use (

) as input, from which the network can infer the other three differences.

Modified the Network Architecture. In Gohr's network [2] (Fig. B .3), the initial convolutional layer (Module 1) was used to capture simple bit-sliced operations. Benamira et al. [3] later showed that this layer mainly performs linear combinations of ciphertext-pair differences. Since Lemma 1 already characterizes these features, the layer is redundant. We therefore remove it, as shown in Fig. 1 . The modified network (15,383 parameters) is much smaller than Gohr's original (44,865 parameters), with detailed hyperparameters given in the Appendix B. Performance Evaluation of DN D.

Table 2 summarizes the accuracy (acc) of our DN D compared with previous work.

Notably, removing the initial convolutional layer and reformulating the input data format according to the derived lemma does not lead to a significant loss in accuracy, thereby confirming the validity of Lemma 1.


## Improved Key Recovery Attack

By refining the UCB-based selection of ciphertext structures and the BayesianKeySearch algorithm, we accelerate key recovery and improve the attack success rate. 1


## Improved Select Strategy of Ciphertext Structure

In differential-neural cryptanalysis, a CD is combined with a DN D to extend the reach of key recovery attacks. The overall process is shown in Fig. 2 ; further details are provided in Appendix C.

The s-round CD (δ → ∆) is probabilistic: a plaintext structure with input difference δ may or may not yield a ciphertext structure with output difference ∆. We call the former correct and the latter wrong. To efficiently select promising structures, Gohr [2] applied the UCB strategy:

where X max (i) is the maximum score of structure i before iteration p, N p (i) its usage count, and γ = √ n cts with n cts denoting the number of ciphertext structures.

The UCB strategy can identify promising ciphertext structures but depends heavily on the weight γ, making it hard to balance exploration and 1 Experiments were conducted on Ubuntu 20.04 with Python 3.7.15 and Tensor-Flow 2.5.0, using dual Intel Xeon Gold 6226R CPUs (2.90 GHz), 256 GB RAM, and five NVIDIA RTX 2080Ti GPUs (12 GB each). exploitation. It may also get stuck in wrong structures with deceptively high DN D scores, wasting computation and reducing success rates. Separately, Kaufmann et al. [9] proposed Bayesian Upper Confidence Bound (Bayes-UCB), a general bandit algorithm. Unlike frequency-based UCB, Bayes-UCB assigns each arm a prior distribution and selects structures based on cumulative scores.

Let X j be the DN D score at the j-th selection. For structure i, define 1(I p = i) = 1 if I p = i at iteration p, and 0 otherwise. The cumulative score before iteration p is s p (i). With Q(1ν, ρ) the quantile of distribution ρ and T (d) the t-distribution with d degrees of freedom, the priority of structure i is

where

The first term estimates the mean score, and the second adds an exploration bonus. At each iteration, the structure with the highest priority is selected. We carried out 11-round key recovery attacks on SPECK32/64 using Bayes-UCB with the DN Ds from [2] , keeping all parameters the same except for the ciphertext structure selection strategy. A key guess is deemed successful if the last-round subkey is correct and the Hamming distance between the penultimate-round subkey and the true subkey does not exceed two. The results are presented in Table 3 . These results confirm the effectiveness of Bayes-UCB in enhancing both the efficiency and reliability of key recovery attacks.


## Improved BayesianKeySearch Algorithm

In key recovery, we find that the correct key with an incorrect ciphertext structure may yield a high score. To mitigate this, we propose an improved BayesianKeySearch Algorithm 1 (refer to Appendix D), which retains the best key and adds it to the new candidate key. The experiment share identical parameters except for the search method, and the results are shown in Table 4 .


## Bayes-UCB + Improved BayesianKeySearch

We evaluated Bayes-UCB and improved BayesianKeySearch through 11-, 12-, and 13-round key recovery attacks on SPECK32/64, using the DN Ds of SPECK32/64 trained in [2] . For comparison, the results of [2] and [10] were reproduced on our setup (Table 1 ).

These results demonstrate that combining Bayes-UCB with the improved BayesianKeySearch algorithm not only reduces time complexity but also achieves a significant improvement in success rate, highlighting the effectiveness of our approach.


## Conclusion

In this work, we revisited differential-neural cryptanalysis on SPECK32/ 64. We characterized non-random XOR-based features in ciphertext pairs beyond classical differentials and used these insights to redesign the data format and simplify the neural network, yielding a smaller model without loss of accuracy. For key recovery, we introduced Bayes-UCB for ciphertext structure selection and improved the BayesianKeySearch algorithm. Together, these refinements lower time complexity and raise success rates, offering both theoretical insight into learned features and practical gains in attack efficiency.

Let v = x 1 ⊕ k. As k ranges over F n 2 , so does v, and we get

Thus the event is exactly

which, by straightforward XOR combinations of the defining equalities, yield the following six pairwise relations:

Conversely, these six pairwise relations imply the original three defining equations, so the corresponding events are equivalent and have identical probability. Table B.5: Hyperparameters of the modified neural network for SPECK32/64 Batch Size β α depth d 1 d 2 k s N f N w L2 2000 3.5 × 10 -3 10 -4 10 64 64 3 32 3 5 × 10 -7 key addition occurs in SPECK32/64 prior to the first non-linear operation, plaintext pairs with input difference δ can be extended by one round without extra cost, enabling a (1 + s + r + 1)-round key recovery attack. This attack requires both the main r-round DN D and an auxiliary (r -1)-round DN D, each trained on ciphertext pairs whose corresponding plaintext pairs satisfy the input difference ∆.


## Output

For ciphertext generation, we first generate about c × 2 p data pairs with input difference δ (denoted n cts ), where c is a small constant. Each pair is then expanded into a structure of n b pairs using the neutral bits of the sround CD. Next, the n cts structures are decrypted by one round with subkey 0 to obtain the corresponding plaintext structures. Finally, each plaintext structure is encrypted for 1 + s + r + 1 rounds to produce the ciphertext structures. When only one round of trial decryption is used, the wrong-key 1 if K best = None then S ← sample n cand keys uniformly at random from the key space K (w/o replacement) ; 2 else S ← {K best } ∪ (sample n cand -1 keys from K \ {K best }) ; 3 L ← ∅; 4 for t = 1 to ℓ do 5 foreach k i ∈ S do 6 for j = 0 to n cts -1 do 7 C ′ j,k i ← DecryptOneRound(C j , k i );

,k i ; // log-odds 10 end 11 s k i ← ncts-1 j=0 z j,k i ; // combined score via neutral bits 12 L ← L ∪ {(k i , s k i )}; 13 m k i ← 1 n cts ncts-1 j=0 z j,k i ; // mean log-odds 14 end 15 foreach k ∈ K do 16 λ(k) ← n cand -1 i=0 m k iµ k i ⊕k 2 σ 2 k i ⊕k ; 17 end 18 S ← arg min k∈K λ(k)[0 : n cand -1] 19 end 20 return L

> 11 1 SigmoidFigure 1 : Figure 1: Modified network architecture

> Figure2: (1 + s + r + 1)-round key recovery attack of differential-neural cryptanalysis in [2] .

> Figure2: (1 + s + r + 1)-round key recovery attack of differential-neural cryptanalysis in [2] .

> 13 1 SigmoidFigure B. 3 : Figure B.3: Network architecture used in [2]

> 1 Algorithm 1 : Improved BayesianKeySearch Input: Ciphertext structures C = {C 0 , . . . , C ncts-1 }; number of candidates n cand per iteration; (optional) current best key K best ; number of iterations ℓ; DN D; wrong-key response profile (µ, σ). Output: List L of tuples (key, score)

> 1 Table 1 : Summary of key-recovery attacks on SPECK32/64

> 2 Table 2 : Accuracy comparison of DN D on different rounds

> 3 Table 3 : The result of key recovery attack using the Bayes-UCB Algorithm Round c 1 c 2 n cts n it N e . c 1 , c 2 : cutoffs for last-round and penultimate-round subkeys. 2. Ne: number of experiments 3. n it : number of iterations in key recovery.

> 4 Table 4 : The key recovery attack using the improved BayesianKeySearch Algorithm Round c 1 c 2 n cts n it N e

## References

1. b0: Ronald L Rivest. "Cryptography and machine learning". Lecture Notes in Computer Science. 1991. DOI: 10.1007/3-540-57332-1_36
2. b1: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
3. b2: Adrien Benamira, David Gerault, Thomas Peyrin, Quan Quan Tan. "A Deeper Look at Machine Learning-Based Cryptanalysis". Lecture Notes in Computer Science. 2021. DOI: 10.1007/978-3-030-77870-5_28
4. b3: A Gohr, G Leander, P Neumann. "Figure 5: The framework of basic and enhanced related-key differential neural distinguishers.". Cryptology ePrint Archive. 2022. DOI: 10.7717/peerj-cs.2566/fig-5
5. b4: Zhenzhen Bao, Jinyu Lu, Yiran Yao, Liu Zhang. "More Insight on Deep Learning-Aided Cryptanalysis". Lecture Notes in Computer Science. 2023. DOI: 10.1007/978-981-99-8727-6_15
6. b5: Liu Zhang, Zilong Wang, Baocang Wang. "Improving Differential-Neural Cryptanalysis". IACR Communications in Cryptology. 2024-10-07. DOI: 10.62056/ay11wa3y6
7. b6: Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks, Louis Wingers. "The SIMON and SPECK lightweight block ciphers". Proceedings of the 52nd Annual Design Automation Conference. 2013. DOI: 10.1145/2744769.2747946
8. b7: Yi Chen, Yantian Shen, Hongbo Yu, Sitong Yuan. "A New Neural Distinguisher Considering Features Derived From Multiple Ciphertext Pairs". The Computer Journal. 2023. DOI: 10.1093/comjnl/bxac019
9. b8: E Kaufmann, O Cappé, A Garivier. "On bayesian upper confidence bounds for bandit problems". Artificial intelligence and statistics. 2012
10. b9: Z Bao, J Guo, M Liu, L Ma, Y Tu. "Conditional differential-neural cryptanalysis". IACR Cryptol. 2021
