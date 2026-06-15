# Machine Learning Assisted Differential Distinguishers For Lightweight Ciphers (Extended Version)

**Authors:** Anubhab Baksi, Jakub Breier, Yi Chen, Xiaoyang Dong

**Source PDF:** `2020_baksi_machine_learning_assisted_differential_distinguishers.pdf`

## Abstract

At CRYPTO 2019, Gohr first introduces the deep learning based cryptanalysis on round-reduced SPECK. Using a deep residual network, Gohr trains several neural network based distinguishers on 8-round SPECK-32/64. The analysis follows an 'all-in-one' differential cryptanalysis approach, which considers all the output differences effect under the same input difference. Usually, the all-in-one differential cryptanalysis is more effective compared to that using only one single differential trail. However, when the cipher is non-Markov or its block size is large, it is usually very hard to fully compute. Inspired by Gohr's work, we try to simulate the all-in-one differentials for non-Markov ciphers through machine learning. Our idea here is to reduce a distinguishing problem to a classification problem, so that it can be efficiently managed by machine learning. As a proof of concept, we show several distinguishers for four high profile ciphers, each of which works with trivial complexity. In particular, we show differential distinguishers for 8-round Gimli-Hash, Gimli-Cipher and Gimli-Permutation; 3-round Ascon-Permutation; 10-round Knot-256 permutation and 12-round Knot-512 permutation; and 4-round Chaskey-Permutation. Finally, we explore more on choosing an efficient machine learning model and observe that only a three layer neural network can be used. Our analysis shows the attacker is able to reduce the complexity of finding distinguishers by using machine learning techniques.

## Introduction

Machine Learning (ML) tools have made a great progress in the last decades. At present, these techniques are widely used in various fields, such as computer vision [35] , machine translation [4, 36] , autonomous driving [17] , to name a few. In the aspect of cryptography however, usage of ML is mainly confined in the context of side channel analysis, such as [16, 31] , to the best of our knowledge.

Therefore, the applicability of ML techniques in classical cryptanalysis is not much explored. It seems the community is rather skeptical regarding this approach. For example, the authors of [1] comment, "Neural networks are generally not meant to be great at cryptography. Famously, the simplest neural networks cannot even compute XOR, which is basic to many cryptographic algorithms".

Although ML techniques have been used against legacy ciphers, like the Enigma (the German cipher used during second world war) [24] , it was not until the work by Gohr [23] at CRYPTO'19 that this line of research finally got its exposure. The idea here is applied to key recovery attacks on round-reduced SPECK using ML.

This work focuses on extending the commonly used model of differential distinguisher by using ML techniques. In the case of differential distinguisher, the attacker Eve XORs a chosen input difference δ to the input of the state of the (reduced round) cipher and watches for a particular output difference ∆, with randomly chosen inputs. If the (δ, ∆) pair occurs with a probability significantly higher for the (reduced round) cipher than what it should be for a random case, the (reduced round) cipher can be distinguished from the random case. This probability distribution of δ → ∆ is modeled by differential branch number [18] or by automated tools like Mixed Integer Linear Programming (MILP) [34] . We extend the modeling for differential distinguisher by incorporating machine learning algorithms.

We argue that the usual modeling with branch number or MILP underestimates attacker's power. Having collected the output differences for the chosen input differences, the attacker can use any technique to distinguish the cipher from the random case. In such a situation, machine learning based techniques can reduce the search complexity estimated by existing methods. In fact, we observe that ML can reduce the search complexity to the cube root of the previously estimated bound.

The machine learning models we propose, can work with any number (say, t) of suitably chosen input differences. Our first model comes into play when t ≥ 2 (see Section 3.1). In order to work with only one input difference, we propose our second model (see Section 3.2).

Detailed discussion of machine learning is out of scope of this work, interested readers may refer to standard textbooks such as [25] for the same. We use TensorFlow foot_0 back-end with Keras foot_1 API. The optimizer function is based on Adam algorithm [26] .


## Our Contributions

In this work, we construct machine learning models to simulate the all-in-one differentials from [2] . We consider the classical distinguisher game: Given ORACLE $ ← {CIPHER, RANDOM}, the attacker is to identify whether ORACLE = CIPHER with probability significantly > 1 2 and with sufficiently small number of queries.

The core of our analysis lies in the actual problem of distinguishing the CIPHER from RANDOM into a classification problem. For this purpose, we propose two models (details are given in Section 3). We choose the most common ML tool, Multi-Layer Perceptron (MLP) as a starting point (we have also tested with other ML tools, as described in Section 5).

As for transforming the differential distinguisher to a classification problem, we propose two models here. We apply the first model (described in Section 3.1) to round-reduced GIMLI [12] , ASCON [19] and KNOT [37] . All of the ciphers are the 2 nd round candidates in the ongoing NIST Lightweight Cryptography (LWC) competition 3 . Further, we also show the effectiveness of the second model (described in Section 3.2) over the lightweight MAC CHASKEY [33] . Brief description of the ciphers is given in Appendix A.

Results are described in Section 4 and Section 5, which can be summarized as follows: • For GIMLI, we obtain 8-round practical distinguishers on GIMLI-HASH and GIMLI-CIPHER in nonce respecting case in Section 4.1. The distinguishing complexity is 2 17.6 offline data to train the model and 2 14.3 online data to distinguish the cipher. Note that the authors of GIMLI [12] proved that the optimal 8-round differential trail is with probability of 2 -52 . If we use this trail to distinguish 8-round GIMLI, we need at least 2 52 online data. Thus, we are able to perform a differential distinguisher in around cube root complexity.

• For the ciphers, ASCON [19] and KNOT [37] , we show practical distinguishers for reduced round versions of the underlying permutations in Section 4.2. For the 320-bit ASCON-PERMUTATION, we show two separate distinguishers that work until 3-rounds with 2 19 training data. For the 256-bit permutation of KNOT (KNOT-256), we show distinguishers for up to 10 rounds; and for the 512-bit permutation (KNOT-512), we show the same for up to 12-rounds. All results on KNOT are obtained with 2 19 training data.

• For CHASKEY [32, 33] , we present our results in Section 4.3. With trivial training/testing complexity (2 23 for training and 2 14.3 for testing), we show the existence of a 4-round distinguisher. This contradicts the authors' claim that no 4-round differential distinguisher of complexity 2 37 searches exists.

In Section 5, we discuss effects of choosing different neural network architectures with respect to 8-round GIMLI-PERMUTATION as the target cipher. We show that even a shallow three layer neural network works well for our purpose. We also report few differential distinguishers for 8-round GIMLI-PERMUTATION in the process.

With regard to our analysis, we emphasize on the following points:

• Generality and practicality. It is to be mentioned that our ML assisted model is generic in nature and can be adopted to any symmetric key setting. All the results presented are practical and can be carried out in around an hour on a modern computer.

• Compatibility with differential distinguisher. We would like to point out that we use the same attack model as that of the pre-existing differential distinguisher. The only distinction is made during the analysis, as ours is done by machine learning (instead of the branch number or automated tools like MILP). We do not fix any output difference a priori, instead all the differentials are fed to the ML.

• Effect of truncation. The results (Section 4.1) for GIMLI-HASH and GIMLI-CIPHER are with truncated versions of the state, whereas the results for GIMLI-PERMUTATION (Section 5) are with the full state. Moreover, we argue that the truncation of the state does not fall outside the perceived model. Having collected the differentials, the attacker can employ any method (including truncating a part) based on the attacker's preference for analysis. This is also noted (with an example) in [5] .

• Extensibility. The results presented in our work do not constitute the theoretical upper bound for the ML assisted distinguishers. By using a more sophisticated ML model and/or more training/testing data, it is likely that one can cover more rounds foot_3 .


## Background


## Markov Ciphers

Lai, Massey and Murphy [28] introduce the concept of Markov ciphers at Eurocrypt'91 which we describe here.

Definition 1 (Markov Chain [28] ). Given a sequence of discrete random variables v

If Pr(v i+1 = β|v i = α) is independent of i for all α and β, the Markov chain is called homogeneous. Given an r-round iterated cipher, the input of ith round is denoted as Y i (0 ≤ i ≤ r). Given a group operation ⊗, we define the corresponding input differences as ∆Y 0 , ∆Y 1 , . . . , ∆Y r , where ∆Y = Y ⊗ Y . Then, Lai et al. introduce the following definition of Markov cipher as given in Definition 2.

Definition 2 (Markov Cipher [28] ). An iterated cipher with round function Y = f (X, K) is a Markov cipher if there is a group operation ⊗ for defining differences such that, for all choices of α (α = 0) and β (β = 0), Pr(∆Y = β|∆X = α, X = γ) is independent of γ when the subkey K is uniformly random, or equivalently, if Pr(∆Y = β|∆X = α, X = γ) = Pr(∆Y (1) = β 1 |∆X = α) for all choices of γ when the sub-key K is uniformly random.


## Theorem 1.

If an r-round iterated cipher is a Markov cipher and the r round keys are independent and uniformly random, then the sequence of differences ∆X = (∆Y 0 ,∆Y 1 , . . . , ∆Y r ), is a homogeneous Markov chain. Moreover, this Markov chain is stationary if ∆X is uniformly distributed over the non-neutral elements of the group.

Theorem 1 is adopted from [28] . According to Theorem 1, one can compute the probability of an r-round differential characteristic as,

Pr(∆Y 1 = β i |∆X = β i-1 ).

(2) However, the above theory can not be applied to non-Markov ciphers, such as GIMLI [12] or ASCON [19] . One of the most important feature of those primitives is that there are no sub-keys in each iterated round. In this situation, the iterated cipher usually can not be regarded as a Markov cipher or a homogeneous a Markov chain. This is because, the differences in the former rounds usually have


## GIFT-64 SBox


## GIFT-64 SBox


## GIFT-64 SBox


## GIFT-64

SBox

Fig. 1 : One-round GIFT-128 (unkeyed) permutation significant effect on the the differences of the latter rounds, where Equation (1) does not hold any more. Hence, we can not use the Equation (2) to compute the probability of a characteristic any more. As shown in Figure 1 , we introduce a toy cipher to explain the dependence of the differences between a 2-round cipher without sub-keys. We use the 4-bit SBox of GIFT-64 [7] as an example. The Difference Distribution Table (DDT) SBox (1A4C6F392DB7508E) is omitted here for the interest of brevity and can be found in [7, Table 18 [1] are the input difference of the upper and lower SBox in Figure 1 , respectively. We try to compute the probability of a differential characteristic, where ∆Y 1 = (2, 3), ∆W 1 = (5, 8), ∆Y 2 = (6, 2), and ∆W 2 = (2, 5). From the DDT of the GIFT SBox, it is easy to know the probability of ∆Y 1 → ∆W 1 is 2 -5 . The valid tuples of (Y

) are (0, 1, 2, 4), (2, 4, 0, 1), (4, 6, 6, 3) and (6, 3, 4, 6). The valid tuples of (Y 1 [1] , W 1 [1] , Y 1 [1] , W 1 [1] ) is (d, 0, e, 8) and (e, 8, d, 0). Only input pairs with (Y 1 [0], Y 1 [1] ) = (0, d), (0, e), (2, d) and (2, e) are valid for the differential characteristic. Hence the probability of the characteristic is 2 -6 , instead of 2 -9 computed by Equation (2).


## Gohr's Work on SPECK (CRYPTO'19)

Using a deep residual neural networks, Gohr in [23] achieves better results than the best classical cryptanalysis on 11-round SPECK [8] . In this work, first several machine learned distinguishers for round-reduced SPECK based on an all-in-one differential cryptanalysis [2] are trained, where the attacker considers potentially all the output differences of a cipher for a given input difference and to combine the information derived from them. Under the Markov assumption, Gohr first computes the entire DDT of round-reduced SPECK with a fixed input difference, which can be achieved due to the small block size of SPECK-32/64. Hence, the all-in-one differentials for the 5-/6-/7-/8-round SPECK-32/64 following the Markov assumption are reported. After this, the same distinguishing task via the neural networks is performed.

Concretely, the following steps are used to train the model: 1. Collecting training data by generating uniformly distributed keys and plaintext pairs given a fixed input difference as well as the binary labels Y i . 2. If the binary label Y i = 1, then the plaintext pairs are encrypted by k-round SPECK to produce the ciphertext pairs. If other wise, the random ciphertext pairs are generated. 3. Pre-process ciphertext pairs to fit the format required by the neural network and start to train them.

Finally, the author gains several machine-learned distinguishers on round-reduced SPECK which are a little more efficient the the distinguishers derived by computing the entire difference distribution table. After that, Gohr uses the neural network based distinguishers to launch several key-recovery attacks on round-reduced SPECK.


## Motivation of Our Work.

Inspired from Gohr's work [23] , the following questions come to our mind, and subsequently we employ neural networks:

• As the all-in-one approach considers all the output differences with one input difference -it is more efficient to distinguish the ciphers than that using only one input difference and one output difference. However, computing the all-in-one distinguisher is infeasible when the state of the cipher is large, e.g. 128-bit state. However, as shown by Gohr's attack, the neural networks can match the all-in-one distinguisher well. Hence, we can take advantage of the neural networks to simulate the all-in-one distinguishers for larger state ciphers.

• As shown in Gohr's attack, under Markov assumption, one can compute the all-in-one distinguishers somehow. However, there are many ciphers which can not be assumed as Markov, such as some permutation-based ciphers or stream ciphers, where there are no sub-key in the iterated rounds (the justification is given in Section 2.1). In these situations, it is hard to compute the all-in-one distinguishers.

3 Machine Learning Based Distinguishers


## Model 1: Multiple Input Differences

Under this model, the attacker chooses t (≥ 2) input differences δ 0 , δ 1 , . . . , δ t-1 . In the training (offline) phase, the attacker tries to learn whether there is any pattern in the CIPHER outputs that the machine learning tool is capable of finding. To test that, Eve creates t differentials with those input differences and feeds all the data to the machine learning. If the accuracy (a) of ML training is higher than what it should be for random data (i.e., 1 t ), the attacker is able extract pattern from the CIPHER outputs and proceeds to the online phase. Otherwise (if the training accuracy is 1 t ), she aborts. During the testing (online) phase, the attacker would check if the sequence of classes predicted by the already-trained machine learning model matches the expected sequence (in which she has queried the ORACLE) with the same probability as training. Since she queries in a specific sequence to the ORACLE, the classes predicted by the machine learning would follow the specific sequence with the same probability as training if ORACLE = CIPHER; or would be arbitrary if ORACLE = RANDOM. Since the ORACLE can only choose between CIPHER and RANDOM, the machine learning produced sequence (of predicted classes) would either match the attacker's pre-perceived sequence with the same probability as she has observed during training (> 1 t ); or that sequence would be arbitrary and hence would match the attacker's pre-perceived sequence with probability 1 t . Therefore, if the accuracy of predicting the classes (a ) is same as a, we infer the chosen ORACLE = CIPHER. On the other hand, if a = 1 t , we conclude ORACLE = RANDOM.

Algorithm 1: Model 1 (multiple input differences) for differential distinguisher with machine learning

1: procedure Offline phase (Training) 2: T D ← (•) Training data 3: Choose random P 4: C ← CIPHER(P ) 5: for i = 0; i ≤ t -1; i ← i + 1 do 6: Pi ← P ⊕ δi 7: Ci ← CIPHER(Pi) 8: Append T D with (i, Ci ⊕ C) Ci ⊕ C is from class i 9: Repeat from Step 3 if required 10: Train ML model with T D 11: ML training reports accuracy a 12: if a > 1 t then 13: Proceed to Online phase 14: else a = 1 t 15: Abort 1: procedure Online phase (Testing) 2: T D ← (•) Testing data 3: Choose random P 4: C ← ORACLE(P ) 5:

Append T D with Ci ⊕ C 9:

Test ML model with T D to get C C is sequence of classes by ML 10: a = probability that C matches (0, 1, . . . , t -1) 11:

if a = a > 1 t then 12: ORACLE = CIPHER 13: else a = 1 t 14: ORACLE = RANDOM 15:


## Repeat from Step 3 if required

A top-level description of the model is given in Algorithm 1. Although we describe the algorithm in terms of the entire state of the permutation for the sake of simplicity. In actual experimentation, we often consider part of the state (such as the rate part) part to make the permutation compatible with the primitives that use it.

Discussion on ORACLE = RANDOM Given the RANDOM case, the machine learning tool will assign classes arbitrarily. Therefore, the accuracy for training will be (close to) 1 t . For example, if t = 2, then the expected training accuracy is 0.5; if t = 32, the expected training accuracy is 0.03125. This is confirmed through our experiments. In fact, for all the results reported (in Section 4), we note that the accuracy for training drops to this bound for higher rounds of the ciphers.

Training and Testing the Model Our distinguisher works on the (unkeyed) permutation with a suitably chosen number of rounds. For the sake of simplicity, we denote the (unkeyed) permutation with input P as CIPHER(P ). The basic work-flow is given next.


## Training (Offline).

1. Select t (≥ 2) non-zero input differences δ 0 , δ 1 , . . . , δ t-1 . 2. For each input difference δ i , generate (an arbitrary number of) input pairs (P, P i = P ⊕ δ i ). Run the (unkeyed) permutation the input pairs to get the output pairs: C ← CIPHER(P ), C i ← CIPHER(P i ) for all i. Then XOR the outputs within a pair to generate the output difference (C i ⊕ C). The output difference together with its label i (i.e., this sample belongs from class i) form a training sample. 3. Check if the training accuracy is > 1 t . Otherwise (i.e., if accuracy = 1 t ), the procedure is aborted.


## Testing (Online).

1. Generate the input pairs in the same way as training. In other words, randomly generate an input P . With the same input differences chosen during training δ 0 , δ 1 , . . . , δ t-1 ; generate new inputs P i = P ⊕ δ i for all i = 0(1)t -1. 2. Collect the outputs C and C i 's by querying ORACLE with input P and P i 's in order, for all i = 0(1)t -1. 3. Generate the testing data as C ⊕ C i for all i and in order. 4. Get the predicted classes from the trained model with the testing data. 5. Find the accuracy of class prediction. In other words, tally the classes returned by the trained ML with the sequence: (0, 1, . . . , t -1, 0, 1, . . . , t -1, . . . , 0, 1, . . . , t -1), and find the probability that both match. 6. (a) If ORACLE = CIPHER, the ML would predict the class for C ⊕ C i as i wtih the same probability as training.

Therefore in this case, the accuracy for class prediction (in Step 5) would be same (or, close to) the accuracy observed during training, i.e., > 1 t . (b) If ORACLE = RANDOM, the ML would arbitrarily predict the classes. Therefore the accuracy for predicting classes by the trained ML (in Step 5) would be equal to (or, close to) 1 t . Algorithm 2: Model 2 (one input difference) for differential distinguisher with machine learning 1: procedure Offline phase (Training) 2: T D ← (•) Training data 3: Choose random P0, P1 ( = P0 ⊕ δ) 4: P2 = P1 ⊕ δ 5: Ci ← CIPHER(Pi), for i = 0, 1, 2 6: Append T D with: (0, C0 C1), C0 C1 is from class 0 (1, C0 C2) C0 C2 is from class 1 7: Repeat from Step 3 if required 8: Train ML model with T D 9: ML training reports accuracy a 10: if a > 1 2 then 11: Proceed to Online phase 12: else a = 1 2 13: Abort 1: procedure Online phase (Testing) 2: T D ← (•) Testing data 3:

Choose random P0, P1 ( = P0 ⊕ δ) 4:

P2 = P1 ⊕ δ 5:

Ci ← ORACLE(Pi), for i = 0, 1, 2 6:

Append T D with C0 C1 and C0 C1 in order 7:

Test ML model with T D to get C C is sequence of classes by ML 8: a = probability that C matches (0, 1) 9:

if a = a >

1 2 then 10: ORACLE = CIPHER 11: else a = 1 2 12: ORACLE = RANDOM 13: Repeat from Step 3 if required


## Model 2: One Input Difference

While the first model (described earlier in Section 3.1) can work with an arbitrary number of input differences, t ≥ 2, here we propose a different model that can work with only one input difference. A top-level view can be found in Algorithm 2. As it can be seen, this model actually converts one input difference to a problem of classification with two classes. The case for ORACLE = RANDOM would result in training accuracy of 1 2 .

Training and Testing the Model With the backdrop already presented in the previous model, here we present the basic work-flow.


## Training (Offline).

1. Select the non-zero input difference, δ.

2. Generate (an arbitrary number of) pairs of inputs, P 0 , P 1 ( = P 0 ⊕ δ); and compute P 2 = P 1 ⊕ δ.

3. Run the (unkeyed) permutation the inputs to get the corresponding outputs: C i ← CIPHER(P i ), for i = 0, 1, 2. 4. Label C 0 C 1 as class 0 and C 0 C 2 as class 1. Run the machine learning model with the data. 5. Check if the training accuracy is > 1 2 . If the accuracy equals (or, close to) 1 2 , the procedure is aborted.


## Testing (Online).

1. Generate the input triplets P 0 , P 1 and P 2 in the same way as training. 2. Collect the outputs C 0 , C 1 and C 2 by querying ORACLE with input P 0 , P 1 and P 2 in order. 3. Feed the trained machine learning data C 0 C 1 and C 0 C 2 in order. 4. Get the predicted classes from the trained model with the testing data. 5. Find the accuracy of class prediction. More precisely, tally the classes returned by the trained ML with the sequence: (0, 1, 0, 1, . . . , 0, 1), and find the probability that both match. 6. (a) If ORACLE = CIPHER, the ML would predict the class for C 0 C 1 and C 0 C 2 as 0 and 1, respectively, wtih the same probability as training.

Therefore, the accuracy for class prediction (in Step 5) would be same (or, close to) the accuracy observed during training, i.e., > 1 2 . (b) If ORACLE = RANDOM, the ML would arbitrarily predict the classes. So the accuracy for predicting classes by the trained ML (in Step 5) would be equal to (or, close to) 1 2 .

As we can see for both the models, it is important to feed the machine learning (during the online phase) the queries returned by the ORACLE in a specific order. The ordering of the classes predicted by the trained machine learning is what determines the inference regarding the ORACLE. Also, this inference, in turn, is determined by the accuracy observed during the training phase.


## Comparison with Existing Models

All-in-one Differential Cryptanalysis All-in-one differential cryptanalysis [2] does not use the cases where the output difference is not same as the pre-determined output difference. Such cases are simply discarded. We make use of all the cases, and are able to obtain distinguishers with reduced search complexity in the process.


## Gohr's Model

Our analysis focuses on different direction from that of Gohr's [23] . Gohr tries to prove the ability of ML-based distinguishers, so he selects SPECK [8] with small state size. This way he is able computed the full DDT of round-reduced SPECK to compare with his neural distinguishers. We focus on other directions. More precisely, we consider ciphers with bigger state and non-Markov ciphers. Both of them are hard to compute the all-in-one distinguishers and we successfully to simulate them via machine learning. It can be stated that our algorithm is simpler to understand and implement.


## Results on Round-Reduced Ciphers


## GIMLI (Model 1)

Using a SAT/SMT-based approach, the authors of GIMLI present the optimal differential trails up to 8 rounds [12] , which are given in Table 1 . If we use the optimal 8-round differential trail to distinguish GIMLI-PERMUTATION, we need more than 2 52 input pairs. Now, based on the ML assisted model presented in Section 3.1 (the first model), we present differential distinguishers till 8 rounds of GIMLI-HASH and GIMLI-CIPHER, each with training data of 2 17.6 samples (and testing data of size 2 14.3 samples). In both the cases, we choose only two input differences, so t = 2. A summary of results can be found in Table 2 . We use the same MLP network for distinguishing 8-round GIMLI-HASH and GIMLI-CIPHER. The network has 5 middle layers with numbers of neurons as (296, 258, 207, 112, 160). The activation function is ReLU, and the number of epochs is set to 20. We observe that our ML model is able to train the data collected with accuracy > 0.5 till 8-rounds (the accuracy drops to 0.5 from 9 rounds onward) for both GIMLI-HASH and GIMLI-CIPHER.

GIMLI-HASH For GIMLI-HASH, we focus on the processes of absorbing the last block of message M and squeezing the first 128-bit hash value h. Suppose the full message M is just 127 bytes (denote the i th byte as M [i]), then after padded with a zero byte, the 128-bit block is absorbed into the sponge function. We generate the training data by flipping the least significant bit of byte M [4] and M [12] . In other words, we process the message pairs with difference 1 in the 4 th byte (as δ 0 ) and 12 th byte (as δ 1 ). Then we compute the first 128-bit hash values pairs accordingly and collect the difference of hash values as training samples.

GIMLI-CIPHER For GIMLI-CIPHER in Figure 3 , we assume there is only one associated data block, so at least 2 GIMLI permutations (48 rounds) are involved until the first output of the ciphertext block. Of 48 rounds, here we take the reduced version, namely up to 8 rounds to show our distinsguisher. For the data collection, we generate uniformly distributed 256-bit keys and 128-bit nonce pairs with difference 1 in the 4 th byte (as δ 0 ) or 12 th byte (as δ 1 ) of the nonces (similar to GIMLI-HASH). We set the associated data and the first message block m 0 to be zero. Then compute the ciphertext c 0 and the differences of it.


## ASCON and KNOT (Model 1)

To show genericness of our methodology, here we present differential distinguishers on ASCON foot_4 [19] and KNOT [37] , using the first model (Section 3.1) for this purpose.

ASCON-PERMUTATION works with 320-bit state; and we only take 256 and 512-bit versions of KNOT-PERMUTATION. Our results show existence of differential distinguishers for up to 3 rounds of ASCON-PERMUTATION; up to 10 rounds of KNOT-256, and up to 12 rounds KNOT-512 with trivial complexity. Table 3 shows results for ASCON with 1-3 reduced rounds. Here, we XOR a mask value to the 64-bit register x 0 to get δ 0 , and XOR the same mask value to the register x 1 to get δ 1 . The results with the mask value 1000 are presented in Table 3 (a), and the same for the mask value 10001 are presented in Table 3(b) . For both the variants of KNOT, the mask value 1 is XORed to the 0 th and 1 st bytes of the state to generate the input differences, respectively. Similarly, Table 4 shows the results for KNOT-PERMUTATION. In particular, Table 4 (a) shows the results for KNOT-256 with 6-10 reduced rounds, and Table 4(b) shows that of KNOT-512 with 8-12 reduced rounds.

The size of neurons for the middle layers of the MLP used for ASCON and KNOT-256 is (128, 1024, 1024, 1024), and for KNOT-512 it is (256, 1024, 1024, 1024). Activation function in the hidden layers is taken as ReLU. Training is run for 20 epochs with 2 19 training data (validation is done with testing data of equal size) samples in all the cases.


## CHASKEY (Model 2)

Using the Lipmaa-Moriai formula, the authors of CHASKEY present some differential trails up to 8 rounds [33] , which are given in Table 5 . Using the notion of pre-existing all-in-one differential, if we use the 4-round differential trail to distinguish CHASKEY, we need at least 2 37 input pairs. Here, we apply the second model of machine learning based differential distinguisher (described in Section 3.2) on 4-round CHASKEY-PERMUTATION. The ML model from Gohr's [23] is used here, except the number of epochs is set to 10.

First, we extend the 4-round differential given by the designers [33] to get a new 5-round trail presented in Table 6 , which shows the complexity for distinguishing 4-round CHASKEY-PERMUTATION would be at minimum 2 37 input pairs. Next for our analysis, first two inputs P 0 , P 1 are randomly generated. Thereafter, we obtain two pairs of samples: P 0 P 1 , and P 0 P 1 ⊕ (00008400 00000400 00000000 00000000). Then we follow the methodology as described in Section 3.2. With training data size of 2 23 , (validation is done with 2 14.3 data) we observe the accuracy of ML is 0.616 for 4-round CHASKEY-PERMUTATION.


## Choice of Machine Learning Model

For finding a distinguisher, we opt for machine learning techniques that can reveal the hidden structures in the data without explicit feature selection. Our problem is treated as a classification problem where one tries to check whether a particular differential is inserted at the input to the (round-reduced) cipher or not. Results in this section are obtained by taking the 8-round distinguisher of GIMLI-PERMUTATION as the benchmark. For training, we use 2 18 data samples. Number of epochs is set to 20 as for higher numbers the models tend to overfit. When using machine learning algorithms, one has to make a choice on hyperparameters that would perform the best on the given problem. These parameters are normally chosen in an empirical way, by testing various network architectures and following best practices. There are automated techniques to tune the hyperparameters [9, 10] ; however, these require significant resources which can be hard to emulate. Here, we report the outcome from the manual architecture search next. Results in this section are obtained by using Intel Xeon Silver 4215 processor with 256 GB of RAM.

We have tried several different neural network types, including the basic MLP, Convolutional Neural Network (CNN), and Long Short-Term Memory Network (LSTM). We have varied the width (number of neurons per layer) and the depth (number of layers) of these to find out the best accuracy and speed of learning. We have also tried several different types of activation functions.

Here, we choose our first model (Section 3.1), with two differences, δ 0 = 1 and δ 1 = 2 (i.e., the least significant and the second least significant bits are flipped, respectively). The input layer size of the model is 128 (first 128-bits are squeezed), and the output layer size, t = 2. Our findings, which contain several distinguishers for 8-round GIMLI-PERMUTATION (highlighted), are stated in Table 8 . Architecture denotes number of neurons per layer starting from the input layer. Activation function denotes the function that was used in the hidden layers, as the output layer always used softmax. A summary can be given as follows:

• CNNs are not suitable for the purpose of finding a distinguisher. We have tried several architectures, and the accuracy was always 0.5. This is expected result, as CNNs are aimed at recognizing patterns in input data, which helps in image recognition or natural language processing, but does not work for cipher input where the bits are not related in any way. In fact, we observe distinguisher for 8-round GIMLI-PERMUTATION only except these models. • LSTMs perform better than CNNs, but worse than fine-tuned MLP. The main drawback of LSTMs was the training speed -as they have recurrent layers, these have high memory requirements and more computations are required.

• MLPs provide the best accuracy, and can be tuned to train in very fast time. Our best result is achieved by MLP with 3 hidden layers and 1024 neurons per hidden layer (MLP VII in Table 8 ), respectively. One can notice that in some cases we used Leaky ReLU as activation function [30] , which allows a small, positive gradient when the unit is not active (e.g. input is negative), and therefore is considered more "balanced." This is an advantage for smaller networks compared to normal ReLU, but for the network with 1.2M parameters, its performance is slightly worse.


## Conclusion and Outlook

In this work, we propose two novel methods on finding distinguishers on symmetric key primitives by using machine learning. Our methods work with any number (non-zero) input differences. At the core, we use multiple differentials and convert the problem of distinguishing CIPHER from RANDOM into a classification problem, which is then tackled by a machine learning technique. Overall, we generalize the classical (all-in-one) differential distinguisher [2, 15] . Unlike the usual differential distinguisher that relies on a rigorous observation and specifics of the target cipher, both of our approaches are much simpler and only rely on analyzing a set of input difference-output difference by machine learning. Thus, we propose the first proof of concept on how machine learning can be used as a generic tool in symmetric key cryptanalysis.

Our methods are also efficient as they can be carried out in around an hour by a modern computer. On the non-Markov ciphers GIMLI [12] , ASCON [19] , KNOT [37] and CHASKEY [32, 33] ; we show drastic reduction of search complexity reported by the designers for the round-reduced versions (typically of the order of a cube root).

A summary of advantages and limitations of our work can be given as: + The attack model is simple. In terms of neural network, our method works with as simple as a three layer neural network. + For round-reduced ciphers, we show that the complexity of differential cryptanalysis can be reduced to around a cube root of the claimed complexity. For example, the designers of GIMLI [12] claim the complexity of mounting a differential distinguisher by existing modeling methods would be at least 2 52 data. However we are able to find the same with the complexity of around 2 17.6 data (details can be found in Section 4.1 and Section 5). + Our work is generic, and can be applied to any symmetric key primitive where differential cryptanalysis can be applied. Here we target non-Markov ciphers as these are typically more complicated to analyze. -So far, we are not able to extend our model to cover further rounds.

-For the time being, our model does not have a key recovery functionality.

That being said, we would like to emphasize that our work does not indicate the theoretical limit of the application of machine learning in symmetric key cryptography. Future works in this direction will likely cover more rounds with advanced ML modelling and/or more training/testing data. As noted in [5] , new functionalities like key recovery, higher order differential can be achieved by switching to a Support Vector Machine (SVM) 6 .

As this is the first research work of its kind, there are scopes to improve the coverage of our experiments in the future. For example, training with more data can be performed to see if a distinguisher for 9-round GIMLI-PERMUTATION is achieved. We only take two input differences with our experiments with the first model (Section 3.1), so one may also be interested in experimenting with more differences. Apart from that, one may look for optimal choices for the input differences so that the size of the training/testing data can be reduced.

We are optimistic that the same methodologies can be applied to Markov ciphers like GIFT [7] as well, which we leave as a future work. Since we use a classification problem, other machine learning techniques that specialize on classification can also be used instead of neural networks.


## A Basic Description of the Ciphers

A.1 GIMLI GIMLI [11] is a cross-platform permutation proposed by Bernstein, Kölbl, Lucks, Massolino, Mendel, Nawaz, Schneider, Schwabe, Standaert, Todo and Viguier at CHES'17. Based on GIMLI permutation, the authors of [12] introduce the lightweight hashing and authenticated encryption algorithms, i.e., GIMLI-HASH and GIMLI-CIPHER, which are included in the second round of NIST Lightweight Cryptography (LWC) competition. GIMLI is also used in the open source cryptographic library LibHydrogen 7 .


## GIMLI-PERMUTATION

works on a 384-bit state which can be represented as a 3 × 4 matrix of 32-bit words, namely:

where the j th column of s is s * ,j = s 0,j , s 1,j , s 2,j , the i th row of s is s i, * = s i,0 , s i,1 , s i,2 , s i,3 . The details of GIMLI-PERMUTATION is given in Algorithm 3, which is adopted from [11] .


## Algorithm 3: GIMLI-PERMUTATION

Input: s = (si,j) Output: GIMLI-PERMUTATION(s) 1: for r from 24 down to 1 inclusive do 2: for j from 0 to 3 inclusive do 3:

x ← s0,j ≪ 24 SP-box 4:

y ← s1,j ≪ 9 5: z ← s2,j 6: s2,j ← x ⊕ (z 1) ⊕ ((y ∧ z) 2) 7:

s1,j ← y ⊕ x ⊕ ((x ∨ z) 1) 8:

s0,j ← z ⊕ y ⊕ ((x ∧ y) 3) 9:

if r mod 4 = 0 then Linear layer 10:

s0,0, s0,1, s0,2, s0,3 ← s0,1, s0,0, s0,3, s0,2 Small-Swap 11:

else if r mod 4 = 2 then 12:

s0,0, s0,1, s0,2, s0,3 ← s0,2, s0,3, s0,0, s0,1 Big-Swap 13:

if r mod 4 = 0 then 14: GIMLI-HASH Taking advantage of GIMLI-PERMUTATION and the sponge construction [13], GIMLI-HASH is defined as shown in Figure 2. The message M is padded and divided into 128-bit blocks, i.e., m 0 , . . . , m t . They are XORed into the state in the absorb phase the state and output 256-bit digest in the squeeze phase. Here we omit some padding rules since they do not affect our attacks. Our neural distinguisher happens in the processing of the last message block m t . GIMLI-CIPHER Taking advantage of GIMLI-PERMUTATION and the Monkey-Duplex construction [14], GIMLI-CIPHER is defined as shown in Figure 3. Here σ 0 , . . . , σ t are the associated data and padded to 128-bit blocks. Here m 0 , . . . , m t and c 0 , . . . , c t are the plaintext and ciphertext blocks, respectively. Note that at least one block of associated data is processed. So at least two GIMLI-PERMUTATION's (48 rounds) are used until the first ciphertext block c 0 generated. In this paper, we target on the case where only one block of associated data is processed. f Nonce Key σ 0 • • • pad (σ t ) m 0 c 0 pad (m t ) Tag c t • • • • • • f f f f Fig. 3: Construction of GIMLI-CIPHER A.2 ASCON

ASCON is one of the winners of CAESAR foot_7 (first choice for lightweight application), and one of the 32 contestants in the second round of the ongoing NIST LWC competition [19] . The mode of operation is MonkeyDuplex [14] . It operates on a 320-bit state which are divided into five 64-bit words x 0 , . . . , x 4 , i.e., S = x 0 x 1 x 2 x 3 x 4 . Since for the machine learning assisted distinguisher we only consider the 320-bit ASCON-PERMUTATION, we give a concise description of it. For more information regarding the cipher, one may refer to [19] . ASCON-PERMUTATION iteratively applies a three-step round transformation for 12-rounds, which are (in order) denoted by p C (addition of constants), p S (substitution layer), p L (linear diffusion layer).

The constant addition, p C , adds an 8-bit round constant to the least significant 8-bits of x 2 at round i. The round constants are as follows: f0, e1, d2, c3, b4, a5, 96, 87, 78, 69, 5a, 4b.

The substitution layer, p S , updates the 320-bit state by applying a 5-bit SBox on it (the SBox is applied 64-times in parallel). The SBox in the look-up format is given as: 4, B, 1F, 14, 1A, 15, 9, 2, 1B, 5, 8, 12, 1D, 3, 6, 1C, 1E, 13, 7, E, 0, D, 11, 18, 10, C, 1, 19, 16, A, F, 17.

The linear diffusion layer, p L , is used to diffuse within each 64-bit register. It applies a linear function to each of the register, x i ← Σ i (x i ) for i = 0, . . . , 4. The linear functions, Σ i 's are given as given next. Here x ≫ i indicates right-rotation (circular shift) by i bits of 64-bit word x. As for the number of rounds, the designers recommend to use 28-rounds for b = 256 and 52-rounds for b = 512 [37, Table 2] . m 1 m 2 m ℓ K 1 K 1 K π π . . . π π right t τ (a) Case: |m ℓ | = n m 1 m 2 m ℓ ||10 K 2 K 2 K π π . . . π π right t τ (b) Case: 0 ≤ |m ℓ | < n Fig. 5: CHASKEY mode of operation

CHASKEY [32, 33] is a permutation based MAC which is designed for optimized performance for 32-bit microcontrollers. This permutation (π) is based on Modular Addition-Rotation-XOR (ARX) design methodology similar to SIPHASH [3] . It takes a 128-bit key K and processes a message m in 128-bit blocks using the 128-bit permutation π.

The permutation π (we denote it by CHASKEY-PERMUTATION) which processes 128 bits is as given in Figure 4 ; here,

). This round functions is iterated for r = 12 rounds [32] . The key operations are addition over modulo 2 32 ( ), XOR (⊕) and left rotation (≪). Here is the only non-linear operation. The permutation π is repeatedly applied in a mode of operation to implement the MAC (see Figure 5 ) and the whole process can be viewed as an Even-Mansour block cipher [21, 22] with a 2n-bit key and n-bit block size.

For the key schedule, CHASKEY takes a 128-bit key K; from which two 128-bit subkeys K 1 and K 2 are derived, each using a 128-bit shift and a 128-bit conditional XOR.

So far the most significant cryptanalysis that has been carried out on CHASKEY can be found in [29] . This attack was in fact on the older version [33] , where the number or rounds of the permutation π is set to r = 8. The author used differential-linear cryptanalysis and succeed to attack for r = 7. After this attack, CHASKEY is revised with r = 12 [32] .

To the best of our knowledge, the most advanced cryptanalysis of CHASKEY-PERMUTATION is reported in [20] , where the authors show a 4-round integral distinguisher. The authors also acknowledge that no such 5-round distinguisher exists. A recent work analyses CHASKEY in terms of weak key setting [27] .

> 23 Fig. 2 :Fig. 3 : Fig. 2: Construction of GIMLI-HASH

> 3 3 ⊕ (x 3 ≫ 10) ⊕ (x 3 ≫ 17) Σ 4 (x 4 ) = x 4 ⊕ (x 4 ≫ 7) ⊕ (x 4 ≫ 41) A.3 KNOT KNOT [37] is one of the 32 candidates currently competing in the second round of the NIST LWC project. Similar to ASCON, we only consider permutation of KNOT, therefore we only describe KNOT-PERMUTATION here. KNOT-PERMUTATION is parameterized by the width b, where b ∈ {256, 384, 512}, although we only use b = 256 and 512 for our experiment. KNOT-PERMUTATION has therefore a state size of b-bits, which is organized in a two dimensional matrix, as detailed in [37, Chapter 2.1]. At each round, an SPN round transformation (denoted by, p b ) is iteratively applied. Each p b consists of the following 3 steps (in order): AddRoundConstant b , SubColumn b , ShiftRow b . The AddRoundConstant b adds round constants (which are generated by a LFSR) to the state, more description can be found at [37, Chapter 2.2]. Next, the SubColumn b step updates the state by applying a 4-bit SBox in column-major fashion. The SBox chosen by the designers is: 40A7BE1D9F6852C3. Finally, the ShiftRow b step left-rotates the state in a row-major fashion. The 0 th is rotated c i bits, i = 0, 1, 2, 3; where c 0 = 0, c 1 = 1, c 3 = 25 for both b = 256, 512 and c 2 = 8 for b = 256, c 2 = 16 for b = 512.

> 45 Fig. 4 :Fig. 5 : Fig. 4: One round of CHASKEY-PERMUTATION (π)

> 1 Table 1 : Optimal differential trails for the round-reduced GIMLI-PERMUTATION

> 2 Table 2 : Accuracy of ML training on round-reduced GIMLI-HASH and GIMLI-CIPHER

> 3 Table 3 : Accuracy of ML training for reduced round ASCON-PERMUTATION(a) Mask: 1000

> 4 Table 4 : Accuracy of ML training for reduced round KNOT-256 and KNOT-512 (a) KNOT-256

> 5 Table 5 : Differential trails for the round-reduced CHASKEY-PERMUTATION

> 6 Table 6 : Differential trail for 5-round CHASKEY-PERMUTATION

> 7 Table 7 : Accuracy of ML training on reduced round CHASKEY-PERMUTATION

> 8 Table 8 : Results for architecture search with 8-round GIMLI-PERMUTATION

## References

1. b0: M Abadi, D G Andersen. Learning to protect communications with adversarial neural cryptography. 2016
2. b1: Martin R Albrecht, Gregor Leander. "An All-In-One Approach to Differential Cryptanalysis for Small Block Ciphers". Lecture Notes in Computer Science. 2012. DOI: 10.1007/978-3-642-35999-6_1
3. b2: Jean-Philippe Aumasson, Daniel J Bernstein. "SipHash: A Fast Short-Input PRF". Lecture Notes in Computer Science. 2012. DOI: 10.1007/978-3-642-34931-7_28
4. b3: D Bahdanau, K Cho, Y Bengio. Neural machine translation by jointly learning to align and translate. 2014
5. b4: Anubhab Baksi, Jakub Breier, Yi Chen, Xiaoyang Dong. "Machine Learning Assisted Differential Distinguishers For Lightweight Ciphers". 2021 Design, Automation & Test in Europe Conference & Exhibition (DATE). 2021-02-01. DOI: 10.23919/date51398.2021.9474092
6. b5: Anubhab Baksi, Jakub Breier, Yi Chen, Xiaoyang Dong. "Machine Learning Assisted Differential Distinguishers For Lightweight Ciphers". 2021 Design, Automation & Test in Europe Conference & Exhibition (DATE). 2020. DOI: 10.23919/date51398.2021.9474092
7. b6: Subhadeep Banik, Sumit Kumar Pandey, Thomas Peyrin, Yu Sasaki, Siang Meng Sim, Yosuke Todo. "GIFT: A Small Present". Lecture Notes in Computer Science. 2017. DOI: 10.1007/978-3-319-66787-4_16
8. b7: Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks, Louis Wingers. "The SIMON and SPECK lightweight block ciphers". Proceedings of the 52nd Annual Design Automation Conference. 2013. DOI: 10.1145/2744769.2747946
9. b8: Yoshua Bengio. "Gradient-Based Optimization of Hyperparameters". Neural Computation. 2000-08-01. DOI: 10.1162/089976600300015187
10. b9: J Bergstra, Y Bengio. "Random search for hyper-parameter optimization". Journal of Machine Learning Research. 2012-02
11. b10: Daniel J Bernstein, Stefan Kölbl, Stefan Lucks, Pedro Maat Costa Massolino, Florian Mendel, Kashif Nawaz, et al.. "Gimli : A Cross-Platform Permutation". Lecture Notes in Computer Science. 2017. DOI: 10.1007/978-3-319-66787-4_15
12. b11: Daniel J Bernstein, Stefan Kölbl, Stefan Lucks, Pedro Maat Costa Massolino, Florian Mendel, Kashif Nawaz, et al.. "Gimli : A Cross-Platform Permutation". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-319-66787-4_15
13. b12: Guido Bertoni, Joan Daemen, Michaël Peeters, Gilles Van Assche. "Sponge-Based Pseudo-Random Number Generators". Lecture Notes in Computer Science. 2007-05. DOI: 10.1007/978-3-642-15031-9_3
14. b13: Guido Bertoni, Joan Daemen, Michaël Peeters, Gilles Van Assche. "Duplexing the Sponge: Single-Pass Authenticated Encryption and Other Applications". Lecture Notes in Computer Science. 2011. DOI: 10.1007/978-3-642-28496-0_19
15. b14: Eli Biham, Adi Shamir. "Differential fault analysis of secret key cryptosystems". Lecture Notes in Computer Science. 1990. DOI: 10.1007/bfb0052259
16. b15: Eleonora Cagli, Cécile Dumas, Emmanuel Prouff. "Convolutional Neural Networks with Data Augmentation Against Jitter-Based Countermeasures". Lecture Notes in Computer Science. 2017. DOI: 10.1007/978-3-319-66787-4_3
17. b16: Chenyi Chen, Ari Seff, Alain Kornhauser, Jianxiong Xiao. "DeepDriving: Learning Affordance for Direct Perception in Autonomous Driving". 2015 IEEE International Conference on Computer Vision (ICCV). 2015-12. DOI: 10.1109/iccv.2015.312
18. b17: Joan Daemen, Vincent Rijmen. "Specification of Rijndael". Information Security and Cryptography. 2002. DOI: 10.1007/978-3-662-60769-5_3
19. b18: Christoph Dobraunig, Maria Eichlseder, Florian Mendel, Martin Schläffer. "Ascon v1.2: Lightweight Authenticated Encryption and Hashing". Journal of Cryptology. 2019. DOI: 10.1007/s00145-021-09398-9
20. b19: Zahra Eskandari, Andreas Brasen Kidmose, Stefan Kölbl, Tyge Tiessen. "Finding Integral Distinguishers with Ease". Lecture Notes in Computer Science. 2018. DOI: 10.1007/978-3-030-10970-7_6
21. b20: Shimon Even, Yishay Mansour. "A construction of a cipher from a single pseudorandom permutation". Lecture Notes in Computer Science. 1991. DOI: 10.1007/3-540-57332-1_17
22. b21: Shimon Even, Yishay Mansour. "A construction of a cipher from a single pseudorandom permutation". Journal of Cryptology. 1997-06. DOI: 10.1007/s001459900025
23. b22: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
24. b23: S Greydanus. Learning the enigma with recurrent neural networks. 2017
25. b24: S Haykin. Neural Networks and Learning Machines. 2008
26. b25: D P Kingma, J Ba. "Preprint repository arXiv achieves milestone million uploads". Physics Today. 2014-12-30. DOI: 10.1063/pt.5.028530
27. b26: Liliya Kraleva, Tomer Ashur, Vincent Rijmen. "Rotational Cryptanalysis on MAC Algorithm Chaskey". Lecture Notes in Computer Science. 2020. DOI: 10.1007/978-3-030-57808-4_8
28. b27: Xuejia Lai, James L Massey, Sean Murphy. "Markov Ciphers and Differential Cryptanalysis". Lecture Notes in Computer Science. 1991. DOI: 10.1007/3-540-46416-6_2
29. b28: Gaëtan Leurent. "Improved Differential-Linear Cryptanalysis of 7-Round Chaskey with Partitioning". Lecture Notes in Computer Science. 2016. DOI: 10.1007/978-3-662-49890-3_14
30. b29: Andrew L Maas, Peng Qi, Ziang Xie, Awni Y Hannun, Christopher T Lengerich, Daniel Jurafsky, et al.. "Building DNN acoustic models for large vocabulary speech recognition". Computer Speech & Language. 2013. DOI: 10.1016/j.csl.2016.06.007
31. b30: Houssem Maghrebi, Thibault Portigliatti, Emmanuel Prouff. "Breaking Cryptographic Implementations Using Deep Learning Techniques". Lecture Notes in Computer Science. 2016. DOI: 10.1007/978-3-319-49445-6_1
32. b31: Nicky Mouha, Bart Mennink, Anthony Van Herrewege, Dai Watanabe, Bart Preneel, Ingrid Verbauwhede. "Chaskey: An Efficient MAC Algorithm for 32-bit Microcontrollers". Lecture Notes in Computer Science. 2015. DOI: 10.1007/978-3-319-13051-4_19
33. b32: Nicky Mouha, Bart Mennink, Anthony Van Herrewege, Dai Watanabe, Bart Preneel, Ingrid Verbauwhede. "Chaskey: An Efficient MAC Algorithm for 32-bit Microcontrollers". Lecture Notes in Computer Science. 2014. DOI: 10.1007/978-3-319-13051-4_19
34. b33: Nicky Mouha, Qingju Wang, Dawu Gu, Bart Preneel. "Differential and Linear Cryptanalysis Using Mixed-Integer Linear Programming". Lecture Notes in Computer Science. 2011-12-03. DOI: 10.1007/978-3-642-34704-7_5
35. b34: Milan Sonka, Vaclav Hlavac, Roger Boyle. "Image Processing, Analysis and Machine Vision". Cengage Learning. 2014. DOI: 10.1007/978-1-4899-3216-7
36. b35: Y Wu, M Schuster, Z Chen, Q V Le, M Norouzi, W Macherey, et al.. Google's neural machine translation system: Bridging the gap between human and machine translation. 2016
37. b36: W Zhang, T Ding, B Yang, Z Bao, Z Xiang, F Ji, et al.. Knot: Algorithm specifications and supporting document. 2019
