# Neural differential distinguishers for GIFT-128 and ASCON

**Authors:** Dongsu Shen, Yijian Song, Yuan Lu, Saiqin Long, Shujuan Tian, School of Computer Science & School of Cyberspace Security , Xiangtan University , Xiangtan , 411105 , China. School of Computer Science School of Cyberspace Security Xiangtan University 411105 Xiangtan China

**Source PDF:** `2024_gift_ascon_score_distribution_mlp.pdf`

## Abstract

In CRYPTO 2019, Gohr first introduced a neural differential distinguisher for round-reduced SPECK32/64 to distinguish ciphertext pairs with a specific input difference from random data, indicating a promising approach to the cryptanalysis of lightweight ciphers. This paper proposes a new neural differential distinguisher model for GIFT and ASCON, both of them are the finalists of the NIST Lightweight Cryptography Competition with ASCON being announced as the winner in February 2023. In our model, we utilize the score distribution of multiple ciphertext differences instead of a single ciphertext pair for classification, which is different from Gohr's model. First, we construct neural distinguishers to evaluate the scores for ciphertext differences. Then we train neural networks to classify the distribution of scores, which is more efficient than the traditional statistical tests such as the Kolmogorov-Smirnov test. Based on the proposed model, we improve the prediction accuracy from 55.42% to 99.36% and from 50.69% to 69.25% for 7-round GIFT-128 and 4-round ASCON-PERMUTATION respectively. Compared with the previous neural distinguisher for ASCON, our distinguisher covers an additional round and attains higher accuracy. The experimental results show that better results can be obtained with the lower hamming weight input difference, and the method presented in this paper can improve the effectiveness of cryptanalysis with neural networks.

## Introduction

The Internet of Things (IoT) is rapidly developing and widely used in various fields. Since IoT devices are typically resource-constrained, such as sensors and RFIDs, the ciphers implemented on these devices must satisfy both security and performance requirements within this environment. This entails efficient design and implementation of ciphers [1] . To fulfill these requirements, lightweight ciphers have been introduced [2] [3] [4] [5] as a class of ciphers that have compact implementations for security. Due to their suitability for IoT devices, lightweight ciphers have gained prominence [6] .

Compared with traditional ciphers such as the AES [7] , lightweight ciphers are characterized by lower power consumption, smaller area requirement, less processing time, and cheaper cost [8] . Lightweight cryptography is a subcategory of cryptography that aims to provide customized solutions for constrained devices [9] . National Institute of Standards and Technology (NIST) [10] announced the first and second-round candidates for the Lightweight Cryptography Competition in April 2019 and August 2019, respectively. In March 2021, Recent research has increasingly considered applying machine learning to differential cryptanalysis, particularly in the context of lightweight ciphers. Gohr [21] proposed an 8-round distinguisher for 𝚂𝙿𝙴𝙲𝙺𝟹𝟸∕𝟼𝟺 constructed with a deep residual network at CRYPTO 2019, and performed efficient key recovery attacks with it. Subsequently, Benamira et al. [22] analyzed the underlying mechanisms of Gohr's distinguishers in detail from the perspectives of cryptanalysis and machine learning at EUROCRYPT in 2021, they pointed out that the network constructed a highly accurate approximated Difference Distribution Table (DDT), and proposed a method for improving Gohr's distinguishers. In another study, Su et al. [23] constructed a neural differential distinguisher for the 9-round lightweight cipher 𝚂𝚒𝚖𝚘𝚗𝟹𝟸∕𝟼𝟺 based on the polytopic differential attack and performed key recovery attacks on 11 rounds of 𝚂𝚒𝚖𝚘𝚗𝟹𝟸∕𝟼𝟺.

Baksi et al. proposed two training models for constructing machine learning-based differential distinguishers in [24] . They constructed distinguishers for four lightweight ciphers, including one for 3-round 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 using 2 19 training data, and compared the training effects of different machine learning models. In a related study, Rajan et al. [25] further developed Baksi's machine learning models of differential distinguisher and trained several distinguishers on 6-round 𝙶𝙸𝙵𝚃-𝙲𝙾𝙵𝙱 with Wang's input differences [26] .

Chen et al. [27] considered features derived from multiple ciphertext pairs to construct distinguishers and improved the accuracy of distinguishers for 𝚂𝙿𝙴𝙲𝙺𝟹𝟸∕𝟼𝟺 with their new model. Bao et al. [28] provided explicit rules that can be used alongside DDTs to improve full DDT-based distinguishers, and conducted a 14-round key recovery attack on 𝚂𝙿𝙴𝙲𝙺𝟹𝟸∕𝟼𝟺 successfully by introducing related-key differences to neural distinguishers.

Liu et al. [29] proposed two models of neural distinguishers utilizing a new input data generation method. With these new models, they constructed distinguishers for the Speck and Simon families, achieving enhanced performance compared to prior approaches. Teng et al. [30] pointed out that the distinguishing probability of neural distinguishers is significantly influenced by the designs of round functions, and presented some variants of that to compare their resistance against neural distinguishers.

Motivations: Some previous neural distinguishers take a pair of ciphertexts or the difference between the two ciphertexts as input, and then output a real-valued score representing the probability that the ciphertext pair is real. The limitation of these distinguishers is that the features among ciphertext pairs are not exploited, their distinguishing only depends on the features derived from a single ciphertext pair, which are not robust. Based on this, we will utilize the score distribution of multiple ciphertext differences instead of a single ciphertext difference for classification.

In this paper, we propose a new model to improve the accuracy of neural distinguishers and demonstrate our model on round-reduced 𝙶𝙸𝙵𝚃 and 𝙰𝚂𝙲𝙾𝙽. Both 𝙶𝙸𝙵𝚃 and 𝙰𝚂𝙲𝙾𝙽 are the finalists in the NIST Lightweight Cryptography (LWC) Competition, with 𝙰𝚂𝙲𝙾𝙽 emerging as the winner in the final round. The main contributions are listed as follows:

• A new method is proposed to distinguish ciphertext differences, by considering multiple ciphertext differences as a single input. We first train a neural distinguisher for the round-reduced cipher, which can output a score representing the probability that the ciphertext difference is real. Then we train another neural network to classify the score distributions of real and random differences. Thus, ciphertext differences can be distinguished by identifying the distribution of scores evaluated by the neural distinguisher. This method improves the accuracy of neural distinguishers that distinguish one ciphertext difference each time.

• Neural distinguishers learn the distribution of ciphertext differences instead of following a single differential trail, therefore the differential transition with the highest probability may not necessarily provide the best learning result. We conduct some experiments to compare the differences with hamming weights of 1 to 5, and the results suggest that starting with an input difference with hamming weight 1 is more likely to yield high accuracy.

• We compare the accuracy of the existing distinguishers model with ours on 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 and 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽. Although the existing model takes multiple ciphertext pairs as input, our new model achieves higher accuracy. Because our distinguishers do not overfit severely like the existing model as the group size increases.

This paper will be structured as follows. Section 2 briefly introduces the preliminaries of differential cryptanalysis, 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 and 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽. We propose our model of neural distinguishers in Section 3 and provide a comparison with previous neural distinguishers. In Section 4, we present our neural distinguishers for 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 and 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽, and discuss the influence of input differences with different hamming weights. Then we perform some experiments to compare the existing model with ours. Finally, Section 5 gives a summary of our work.


## Preliminaries


## Specification of differential cryptanalysis

Biham and Shamir [12] proposed differential cryptanalysis in 1991, which is a chosen-plaintext attack that studies the characteristics of the differential transition in the encryption process. It aims to recover part of the key bits by analyzing how the difference between plaintext pairs influences the difference between ciphertext pairs. Now let 𝐸 ∶ F 𝑛 {0,1} → F 𝑛 {0,1} be a cryptographic function and 𝑃 0 , 𝑃 1 are two inputs for 𝐸 with the input difference 𝛿 𝑎 = 𝑃 0 ⊕ 𝑃 1 . Let 𝐶 0 = 𝐸(𝑃 0 ), 𝐶 1 = 𝐸(𝑃 1 ) with the output difference 𝛿 𝑏 = 𝐶 0 ⊕𝐶 1 . We refer to 𝛿 𝑎 → 𝛿 𝑏 as the differential transition, and the differential transition probability Pr(𝛿 𝑎 → 𝛿 𝑏 ) is defined as

For random permutation on {0, 1} 𝑛 , if the difference transition 𝛿 𝑎 → 𝛿 𝑏 is given arbitrarily, its average probability 𝑃 = 1 2 𝑛 -1 ≈ 1 2 𝑛 . The Differential Distribution Table (DDT) is constructed by analyzing the differential transition characteristics of the nonlinear component in the encryption, which are usually S-boxes. This is because storing the DDT of an entire cipher with a large state (e.g. 128-bit) is impractical. After that, a 𝑟-round differential distinguisher can be obtained by identifying a high-probability differential characteristic with the chosen input difference. The key recovery attack can then be performed on 𝑟 + 1 round ciphertexts, wherein the last round key is hypothesized and employed to decrypt the ciphertext pairs. The differential distinguisher is used to evaluate the authenticity of the guessed key, and the key with the highest authenticity is selected for further key recovery attacks.


## Specification of 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾

𝙶𝙸𝙵𝚃 is a lightweight block cipher designed by Banik et al. [31] , based on the Substitution-Permutation Network (SPN) structure. It has two versions, namely 𝙶𝙸𝙵𝚃-𝟼𝟺 and 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾. In this article, we exclusively focus on the 128-bit version, where both the block size and key length are 128 bits. The round function is performed 40 times in 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾. The round function comprises three steps: SubCells, PermBits, and AddRoundKey. Before performing the first step, The cipher state 𝑆 is initialized with the 128-bit plaintext, which is segmented into four 32bit segments. Likewise, the key state 𝐾𝑆 is initialized with the 128-bit key, which is divided into eight 16-bit words.


## SubCells. This step uses an invertible 4-bit S-box 𝑆(𝑥). Table 1 shows a lookup table of the S-box represented in hexadecimal notation.

PermBits. Each cipher state 𝑆 𝑖 applies different 32-bit permutations as shown in Table 2 .

AddRoundKey. The addition of the round key and round constant is involved in this step. The round key is denoted as 𝑅𝐾 = 𝑈 ∥ 𝑉 , where 𝑈 , 𝑉 are extracted from the key state with 32 bits. More description about the key schedule can be found at [31] .

To add the round key, U and V are XORed to the state 𝑆 as follows,

To add the round constant, 𝑆 3 is updated as follows,

where the byte XY = 00𝑐 5 𝑐 4 𝑐 3 𝑐 2 𝑐 1 𝑐 0 .


## Specification of 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽

𝙰𝚂𝙲𝙾𝙽, designed by Dobraunig et al. [32] , is a permutation-based lightweight cipher. It is based on the monkeyDuplex [33] construction which is a classical sponge construction. 𝙰𝚂𝙲𝙾𝙽 operates on a state size of 320-bit (consisting of five 64-bit words 𝑥 0 , … , 𝑥 4 ), and the main component is a 320-bit permutation instantiated with different constants and the number of rounds. 𝙰𝚂𝙲𝙾𝙽 is the winner of the CAESAR competition and NIST competition.

We only consider the 320-bit permutation for training our neural distinguishers, providing a brief overview of the 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽. For a complete description of the cipher, we refer to [32] . Each round of the permutation consists of three steps: Addition of Constants, Substitution Layer, and Linear Diffusion Layer. These three are iteratively applied for 12 rounds in the 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 𝑝 12 .


## Addition of Constants.

In this step 𝑝 𝐶 , a round constant 𝑐 𝑟 is added to register word 𝑥 2 of the state 𝑆(𝑆 = 𝑥 0 ‖𝑥 1 ‖𝑥 2 ‖𝑥 3 ‖𝑥 4 ) in each round. The round constants are stated in Table 3 .


## Substitution Layer.

In this layer 𝑝 𝑆 , a 5-bit S-box is applied 64 times in parallel to update the state. Each bit of the five 64-bit words (𝑥0, … , 𝑥4) contributes one bit to each of the 64 S-boxes, where 𝑥 0 is the most significant bit. The lookup table of the S-box is shown in Table 4 .


## Linear Diffusion Layer.

In this layer 𝑝 𝐿 , each 64-bit register word 𝑥 𝑖 is diffused by the linear function 𝛴 𝑖 ( 𝑥 𝑖 ) , 𝑥 𝑖 ← 𝛴 𝑖 ( 𝑥 𝑖 ) for 𝑖 = 0, … , 4:

𝑥 ⋙ 𝑖 indicates right-rotation (circular shift) by 𝑖 bits of the 64-bit word 𝑥.


## New model of neural distinguishers

Differential distinguisher is a crucial component in the key recovery attack of differential cryptanalysis. The traditional differential distinguisher works with a differential characteristic that provides the highest probability transition from a chosen input difference to a ciphertext difference. Therefore, constructing a traditional differential distinguisher typically involves high data complexity. Neural distinguishers are trained to distinguish ciphertext differences with a fixed input difference from random ciphertext differences. They do not rely on the optimal differential characteristic, which reduces the data complexity of construction.

The proposed new model of neural distinguishers consists of two components: construction of neural distinguishers and prediction with multiple ciphertext differences. Both parts are implemented based on Multi-Layer Perceptron (MLP). The overall architecture of our new model is shown in Fig. 1 .


## Construction of neural distinguishers


## Data generation

The training and validation data for our neural distinguishers includes the differences between 𝑟-round ciphertext pairs encrypted from plaintext pairs with the chosen difference, as well as 𝑟-round ciphertext differences obtained from random plaintext pairs. The labels for these differences are binary, with values of 1 or 0. The generation of datasets can be found in Algorithm 1.


## Network architecture and training pipeline

Network Architecture: The MLP network takes ciphertext differences as input, with 128-bit for 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 and 320-bit for 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽. There are three hidden layers, with the same number of neurons as the input layer and ReLU activation function in each layer. The final layer outputs a real-valued score after a sigmoid activation function.


## Training Pipeline:

We take Binary Cross-Entropy Loss as the loss function since distinguishing differences can be seen as a binary classification task. Adam with default parameters in Keras is used as the optimizer. The training and validation of our neural distinguishers use the labeled datasets as described above. For each input ciphertext difference, the score between 0 and 1 calculated by the neural distinguisher representing the probability that the ciphertext difference is real. The distinguisher is built as follows:


## Table 3

The round constants 𝑐 𝑟 used in each round of 𝑝 12 .


## 𝑝 12

Constant 𝑐 𝑟 𝑝 12 Constant 𝑐 𝑟

0𝑥5a 5 0𝑥a5 11 0𝑥4b Step 3. If the validation accuracy is lower than or equal to 50%, the training has been overfitting. Return to Step 1 or refine the data generation process if necessary. Step 4. The neural network now is a valid neural distinguisher. Return the network with the lowest validation loss.

When testing the neural distinguisher with different sets, if the ciphertext differences in the set have the chosen input difference, the probability of classification as 1 (true positive rate) is expected to be lower than the validation accuracy. However, if the input differences of ciphertext differences are chosen randomly, the probability of classification as 0 (true negative rate) is likely to be higher than the validation accuracy. This is because the neural distinguisher can learn some significant features from the training data, but not all ciphertext differences have these features. Therefore, the neural distinguisher would classify ciphertext differences that do not conform to these features as random. In a word, distinguishing a specific input difference is generally more difficult than distinguishing random input differences.


## Prediction with multiple ciphertext differences 3.2.1. Motivations

When employing a neural distinguisher with validation accuracy slightly exceeding 50% for prediction, the classification accuracy for a set of real ciphertext differences will be equal to (or slightly lower than) 50%. It is hard to get convincing prediction results. However, we believe that this neural distinguisher has learned enough information to distinguish real differences from random differences.

We count the number of scores for ciphertext differences in each interval: [0, 0.1), [0.1, 0.2), …, [0.9, 1] for real and random sets. An example is shown in Fig. 2 . We chose the neural distinguisher of 6-round 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 with 77.06% validation accuracy to show the distribution of scores more clearly in the histogram. In fact, for all neural distinguishers with a validation accuracy higher than 50%, there exists a significant distinction in the score distribution of real and random sets. Classification can be done by identifying the distribution of scores. Neural networks learn features of ciphertext differences in the training data, and output highly similar scores for differences with identical features. In addition, the distribution of differences in different sets of the same size exhibits remarkable similarity. Therefore, the object of classification should be a set of differences rather than a single difference.


## Classification based on the score distribution

So we decide to classify multiple ciphertext differences at once based on the score distribution, and the accuracy in the training and validation is only seen as an indicator of whether the training is effective. On a theoretical level, a neural distinguisher with a validation accuracy higher than 50% can be improved to achieve higher prediction accuracy.

It can be implemented with statistical tests, such as the Kolmogorov-Smirnov (K-S) test, which quantifies the distance between the D. Shen et al.


## Table 4

The 5-bit S-box of 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽.

x 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 𝑆(𝑥) 4 11 31 20 26 21 9 2 27 5 8 18 29 3 6 28 x 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 𝑆(𝑥) 30 19 7 14 0 13 17 24 16 12 1 25 22 10 15 23

empirical distribution functions of two samples to check whether the two data samples come from the same distribution. A test set with multiple ciphertext differences is classified as follows: first, we generate a set of real differences and evaluate the scores of these differences with the neural distinguisher. This set of scores is seen as the stand score distribution of real differences. Then we compute the K-S test statistic and its 𝑝-value for scores of the test set and the stand distribution. If the 𝑝-value exceeds 0.05, the test set will be classified as real and random otherwise. We need a large set of differences to improve the accuracy of neural distinguishers with the K-S test. However, it would increase the data complexity of prediction. In terms of this issue, we use MLP to learn the distribution of scores and then classify a test set with the information learned by the neural network. We refer to the method of checking the score distribution with MLP as the MLP test. This helps us to perform classification more efficiently.


## MLP test

Network Architecture: Let 𝑠 denote the number of ciphertext differences in a sample. The input layer consists of 𝑠 units and receives scores evaluated by the neural distinguisher. There are two hidden layers, the number of neurons in each layer is 64 if 𝑠 ≤ 64, and 𝑠 if 𝑠 > 64. The activation function in hidden layers is ReLU. The final layer outputs a real-valued score after a sigmoid activation function.


## Training Pipeline:

The loss function is Binary Cross-Entropy Loss and the optimizer is Adam with default parameters in Keras. We train the MLP test by following steps:

1. Generate ciphertext differences with the chosen input difference and obtain their scores. Divide these scores into groups, each containing 𝑠 scores, and then sort the 𝑠 scores in ascending order (or descending order). Sorting aims to remove the positional relations of scores. Similarly, generate groups of scores for random ciphertext differences. 2. Generate training and validation dataset: half the data comes from score groups of real differences with label 1, and the other half is from score groups of random differences with label 0. 3. Train the neural network with training and validation dataset obtained as described above. If the validation accuracy is greater than that of the neural distinguisher, the MLP test is valid. If not, generate datasets with larger 𝑠 and retrain.

We apply the MLP test and K-S test to our neural distinguishers for round-reduced 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 and 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 in Sections 4.1 and 4.2. The results demonstrate the improvement of prediction with multiple differences to our neural distinguishers, and the MLP test is more efficient than the K-S test.


## Comparison with previous neural distinguishers

Gohr's Distinguishers. Gohr [21] proposed distinguishers for 𝚂𝙿𝙴𝙲𝙺𝟹𝟸∕𝟼𝟺 [34] constructed with a deep residual network. In a further study of Gohr's work, Benamira [22] pointed out that Gohr's neural distinguishers effectively approximated the Difference Distribution Table (DDT) by the training of neural networks, and classified ciphertext pairs with this information.

For the training of neural distinguishers, Gohr generated training and validation data with a single input difference of the highestprobability transition found by their model. Differently, our neural [24] chose 𝙶𝙸𝙼𝙻𝙸 [35] , 𝙰𝚂𝙲𝙾𝙽 [32] , 𝙺𝙽𝙾𝚃 [36] , and 𝙲𝙷𝙰𝚂𝙺𝙴𝚈 [37] with bigger state for differential cryptanalysis, all of which are non-Markov ciphers. They designed two models to construct neural distinguishers with different networks.

The first model uses multiple input differences, selecting 𝑡(𝑡 ≥ 2) input differences to generate the dataset, regardless of random differences. It uses the differences between the ciphertext pairs 𝐶 ⊕ 𝐶 ′ for training. The second model is similar to Gohr's distinguishers. We tried using the first model to train a neural distinguisher for 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾, but the results were inferior to those achieved with our single input difference neural distinguishers. As we discussed at the end of Section 3.1, the features of ciphertext differences with a fixed input difference that the neural distinguishers can learn are limited. The validation accuracy of a neural distinguisher with two given input differences will be lower than that with one given difference and random differences. Especially when the differential features from two given input differences have overlapping parts.


## Chen et al.'s Distinguishers.

Chen et al. [27] proposed a new distinguishers model considering features derived from multiple ciphertext pairs. Based on this model they improved the accuracy of distinguishers for 𝚂𝙿𝙴𝙲𝙺𝟹𝟸∕𝟼𝟺.

This new model can be seen as an improvement of Gohr's distinguishers, which take multiple ciphertext pairs as the input of the network. Their new distinguishers captured features derived from multiple ciphertext pairs, and similarly, our proposed model improves the accuracy of distinguishers with multiple ciphertext differences. In Section 4.4, we conduct some experiments to compare the results of Chen et al.'s model on 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 and 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 with ours.


## Experiments and analysis 1


## Neural distinguishers for round-reduced 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾

Using an improved MILP-based approach, Zhu et al. [38] presented some differential characteristics for reduced round 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾. A 12round differential characteristic is shown in Table 5 , and the data complexity of the 7-round classical differential distinguisher is 2 37 . We construct 7-round neural distinguishers with datasets of size 2 23.2 (10 7 ) in the training and validation based on the proposed model. Now, we present our neural distinguishers for 5 to 7 rounds of 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾.

Training: We assume that there is only one plaintext block for the data collection. Based on our data generation algorithm, we generate uniformly distributed 128-bit keys to compute 128-bit ciphertext differences with a difference of 1 in the 7th byte of plaintext pairs, along with 128-bit random differences. Training is run for 50 epochs.

The results on the validation data are given in Table 6 . Note that the validation accuracy only indicates the results of training, not the prediction accuracy. Prediction: We use the proposed method to improve the prediction accuracy of neural distinguishers for 6 to 7 rounds of 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 because the accuracy of the neural distinguisher for 5 rounds is high enough. Both the MLP test and K-S test are used here respectively.

We denote 𝑠 as the group size of a differences sample. For the K-S test, we first generate 𝑠(for 𝑠 ≤ 128 the number is 128) real ciphertext differences and evaluate their scores by our distinguishers. Then we randomly generate 50 000 real samples and 50 000 random samples for the evaluation.

For the MLP test, we generate 10 7 ∕s real and random samples for the training and 10 6 ∕s real and random samples for the validation. Table 7 shows the results of the experiment.


## Analysis:

We achieve high prediction accuracy with small samples using the MLP test for 6 rounds of 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾. For the K-S test, we need a larger 𝑠 to obtain an accuracy close to the MLP test. MLP test can detect the score distribution in smaller samples because it learns features of both real and random differences scores for classification. While the K-S test just uses scores of real differences as the stand score distribution to evaluate samples. Therefore MLP test requires a larger dataset for training. For the K-S test, a large real sample is not necessary, it is better to take a real sample that is close in size to 𝑠.

For the neural distinguisher of 7 rounds 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 with a low validation accuracy, both the MLP test and K-S test require larger samples to improve the prediction accuracy. MLP test achieves better overall accuracy than the K-S test with the same size of 𝑠.


## Neural distinguishers for round-reduced 𝙰𝚂𝙲𝙾𝙽

Using heuristic search tools, the authors of 𝙰𝚂𝙲𝙾𝙽 [39] presented an optimal differential transition with the differential probability of 2 -107 for 4-round 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽. Baksi et al. [24] presented machine learning-based differential distinguishers with a data complexity of 2 19 for up to 3 rounds of 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 based on their first model (two input differences), which can be found in Table 8(a) . Applying our new model, we obtain neural distinguishers for up to 4 rounds of 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 with a single input difference. The size of training and validation data is 2 19.9 (10 6 ) for 1 to 3 rounds, and 2 23.2 (10 7 ) for 4-round.

Training: Because the 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 does not require a key for computation, we only need to generate uniformly distributed 320bit states. The difference (0000 0001) is XOR to the last byte of the 64-bit register 𝑥 0 as the chosen input difference. Then we input 320bit differences to the MLP for training. Training is conducted for 20 epochs. Table 8 (b) shows our results.

It can be found that our neural distinguishers achieve higher validation accuracy than Baksi's for 1 to 3 rounds of 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 and cover one additional round.

Prediction: In order to know whether our new method improves the prediction accuracy of the neural distinguisher for 4 rounds of 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 with a validation accuracy slightly higher than 50%, Table 9 shows an experiment similar to that in Section 4.1. In addition to sorting the scores within the samples, we also perform Min-Max Normalization on the scores in each sample for the MLP test. We observe that the scores within the samples are densely distributed between 0.47 and 0.52. This normalization aids in better learning of the characteristics of the score distribution and ensures sufficient gradient for convergence.

Analysis: We need to generate differences samples with a minimum size of 2 8 to effectively improve the prediction accuracy using the MLP test, and for the K-S test the minimum size is 2 13 . The training for the MLP test with more than 2048 input units is hard to fit, so the highest accuracy is 69.25% with test sets of size 2048. But we can still achieve higher accuracy with the K-S test, despite the large size of 𝑠. The signal from this neural distinguisher is rather weak as the scores are densely distributed around 0.5. But the distinguisher has indeed learned certain features proved by the results of the K-S test.


## Discussion of the input differences

It can be determined that the accuracy of distinguishers is significantly influenced by the choice of input differences. (0𝑥0, 0𝑥0, 0𝑥0, 0𝑥0, 0𝑥0, 0𝑥0706, 0𝑥0, 0𝑥0) is the input difference of a high probability 14-round differential characteristic of 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 found in [38] , D. Shen et al. from which we only obtain a 6-round distinguisher with an accuracy of 50.77%. And our most effective distinguishers for 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 and 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 are obtained by using input differences with hamming weight 1. Therefore, we design an experiment to compare the effect of input differences with different hamming weights on the accuracy of distinguishers. The task of this experiment is training distinguishers for 6-round 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾, as we can observe the distribution of accuracy over a larger interval. We use the input differences with hamming weight of 1 to 5 for the training. We first generate all the input differences with hamming weight 1, totaling 128 differences. Then, for the experiments of input differences with hamming weight of 2 to 5, we randomly generate 128 differences for each without repeating. After training distinguishers with these input differences, we count the number of distinguishers' accuracies distributed in each interval. The results are shown in Table 10 . 2 It can be seen that as the hamming weight increases, more distinguishers achieve low accuracy. Hou et al. [40] proposed that the higher the Hamming weight of the input difference, the weaker the non-random feature of the ciphertext pair. This is partially confirmed by our experimental results. Therefore when choosing input difference for the training of distinguishers, starting with an input difference with hamming weight 1 is more likely to achieve high accuracy.


## Comparison with Chen et al.'s distinguisher model

To compare with the distinguisher model proposed by Chen et al. [27] with Residual Network, we train the distinguishers for 6 to 7 rounds of 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 and 4 rounds of 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 with their model. The code of network construction and training is from [27] . For convenience, we denote the distinguishers trained with Chen et al.'s model as   Res and ours as   MLP .

The size of a training set is 𝑁 = 10 7 , and the size of a validation set is 𝑀 = 10 6 . Each sample consists of 𝑠 ciphertext differences for   MLP and 𝑠 ciphertext pairs for   Res . A training set is composed of 𝑁∕2𝑠 real samples and 𝑁∕2𝑠 random samples, and a validation set is composed of 𝑀∕2𝑠 real samples and 𝑀∕2𝑠 random samples. Training is conducted for 50 epochs, and the best validation accuracy is recorded. The results are shown in the Table 11 .

For 6-round 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾: When 𝑠 = 1,   Res achieves a higher accuracy than   MLP due to the use of ciphertext pairs as input. As 2 The input differences we generate and the corresponding accuracy are given in our GitHub repository. 𝑠 increases to 2 and 4,   Res has an improved accuracy and   MLP brings a higher accuracy improvement. When 𝑠 = 8, the accuracy of   Res decreases because of the overfitting, whereas   MLP still can improve its accuracy.

For 7-round 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾:   Res achieves a similar accuracy to   MLP with 𝑠 = 1. When 𝑠 = 2,   Res is unable to improve the accuracy, and its accuracy decreases with 𝑠 ≥ 4 due to overfitting. Meanwhile,   MLP keeps improving the accuracy as 𝑠 increases.

For 4-round 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽:   MLP with 𝑠 = 1 performs similarly to   Res , 𝑠 = 1, 2. When 𝑠 ≥ 4,   Res cannot achieve a valid result because of the overfitting. We observe that with the increase in cipher state size,   Res overfits more severely when 𝑠 ≥ 2. This is also the reason why   MLP , which takes ciphertext differences as input, obtains higher accuracy than   Res on 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 and 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 when 𝑠 ≥ 2.

It is worth noticing that we do not perform Min-Max Normalization on the training and validation sets for our   MLP of 4-round 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 at 𝑠 = 2 to 𝑠 = 32, and instead achieve higher accuracy compared to the training with normalized sets. We initially suspect this might be an incidental occurrence on the current validation set, as the validation accuracy fluctuates between the highest accuracy and 0.5 during training. Therefore, we save the model with the highest accuracy for evaluation, and the obtained accuracy is very close to the previously observed one. What has the   MLP learned from these few scores closely distributed around 0.5? It is worth further investigation in future research.


## Conclusion

In this paper, we proposed a new model for the construction of neural differential distinguishers for lightweight ciphers, including a new method called the MLP test for the classification of ciphertext differences. This work improves the performance of the previous neural distinguishers for 4-round 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽 and constructs the neural distinguishers of 7-round 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 for the first time. The object of classification is changed from a single ciphertext difference to multiple ciphertext differences. We trained neural networks to classify the distribution of scores, and the K-S test is also used for prediction to show the comparison with the MLP test. Predicting based on the score distribution of ciphertext differences greatly improves the accuracy of prediction, with our new method the MLP test proving more efficient than the K-S test. By comparing with the existing distinguishers model using multiple ciphertext pairs, our new model is found to be more suitable for large state ciphers such as 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 and 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽.

Neural distinguishers do not rely on the optimal differential characteristic and they can reduce the data complexity by learning the distribution of ciphertext differences. Compared with the input difference of a highprobability differential transition, an input difference with hamming weight 1 is more likely to help neural distinguishers achieve higher accuracy.

As future work, we will continue optimizing the proposed model to cover further rounds and improve the distinguishing accuracy. Accordingly, we can give a more powerful illustration of the feasibility of applying neural networks to cryptanalysis.

> 152718291011 Algorithm 1 : 5 𝑃 2 = 7 𝐶 1 = 8 𝐶 2 = 9 Append 𝐷 with: 10 ( 11 ( Data generation for training and validationInput: Cipher 𝐸(⋅), Data Size 𝑁, Difference 𝛿 Output: Training or Validation Dataset 𝐷 1 𝐷 ← ∅; 2 𝐾 ← 𝑅𝑎𝑛𝑑𝑜𝑚; 3 for 𝑖 = 1 to 𝑁 do 4 𝑃 0 , 𝑃 1 ← 𝑅𝑎𝑛𝑑𝑜𝑚; 𝑃 1 ⊕ 𝛿; 6 𝐶 0 = 𝐸(𝑃 0 , 𝐾); 𝐸(𝑃 1 , 𝐾); 𝐸(𝑃 2 , 𝐾); 𝐶 0 ⊕ 𝐶 1 , 0) ; // class 0 𝐶 1 ⊕ 𝐶 2 , 1) ; // class 1 12 Return 𝐷

> 1 Step 1 . Train the neural network with the training dataset. Classify the sample as 1 if the output score exceeds 0.5; otherwise, classify it as 0. Then calculate the training accuracy.Step 2. Start validation on the validation dataset if the training accu-racy is higher than 50%. Or retrain a new neural network.

> 1 Fig. 1 . Fig. 1. The overall pipeline for the proposed model of neural distinguishers.

> 2 Fig. 2 . Fig. 2. Score distribution of real set and random set.

> 1 Table 1 The 4-bit S-box of 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾 as a lookup table.

> 2 Table 2 Bit permutation of 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾.

> 5 Table 5 Differential characteristic of 12-round 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾.′ while the input of Gohr's neural distinguishers takes a pair of ciphertext (𝐶, 𝐶 ′ ). The experiments with group size 𝑠 = 1 in Section 4.4 serve as a comparison with Gohr's distinguishers model.Baksi et al.'s Distinguishers.Baksi et al.

> 6 Table 6 Accuracy of neural distinguishers for round-reduced 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾.

> 7 Table 7 Prediction accuracy of improved neural distinguishers for round-reduced 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾.

> 8 Table 8 Accuracy of neural distinguishers for round-reduced 𝙰𝚂𝙲𝙾𝙽-𝙿𝙴𝚁𝙼𝚄𝚃𝙰𝚃𝙸𝙾𝙽.

> 10 Table 10 Experiment with Different Input Differences for 6-round 𝙶𝙸𝙵𝚃-𝟷𝟸𝟾.

## Acknowledgements

Acknowledgments This work was supported in part by the National Key R&D Program of China (Grant No. 2022YFB2701600 ); the Xiangtan University scientific research project (Grant No. 15XZX32 ); the National Natural Science Foundation of China (Grant No. 62172350 ); National Natural Science Foundation of China (Grant No. 62172349 ); National Natural Science Foundation of Hunan Province (Grant No. 2023JJ30597 ); the Research Foundation of Education Bureau of Hunan Province (Grant No. 21B0139 ); Open Project of the State Key Laboratory of Computer Science, Institute of Software, Chinese Academy of Sciences (Grant No. SYSKF2101 ).

## References

1. b0: Dinu Daniel, Corre Yann Le, Khovratovich Dmitry, Perrin Léo, Großschädl Johann, Alex Biryukov. "Triathlon of lightweight block ciphers for the internet of things". J Cryptogr Eng. 2019
2. b1: Mishra Bhasin Akshay, Girish. "Recent advances in lightweight stream ciphers". CSI Trans ICT. 2016
3. b2: Duy-Hieu Bui. "An innovative lightweight cryptography system for Internet-of-Things ULP applications". Sony Corp. 2008. DOI: 10.70675/1f44f620zf576z4d79zb57az256b7df60d33
4. b3: Manayankath Megha Mukundan Puliparambil, Srinivasan Sindhu, Sethumadhavan Chungath, Madathil. "Hash-one: a lightweight cryptographic hash function". IET Inf Secur. 2016
5. b4: Sankaran Sriram. "Lightweight security framework for IoTs using identity based cryptography". 2016 international conference on advances in computing, communications and informatics. ICACCI. 2016
6. b5: Singh Saurabh, Pradip Sharma, Moon Kumar, Park Jong Seo Yeon, Hyuk. "Advanced lightweight encryption algorithms for IoT devices: survey, challenges and solutions". J Ambient Intell Humaniz Comput. 2017
7. b6: Daemen Joan, Rijmen Vincent. The design of Rijndael. 2002
8. b7: Philip Merly, Annie. "A survey on lightweight ciphers for IoT devices". 2017 international conference on technological advancements in power and energy (TAP energy). 2017
9. b8: Mckay Kerry, Bassham Lawrence, Sönmez Turan Meltem, Mouha Nicky. Report on lightweight cryptography. 2016
10. b9: Turan Meltem Sönmez, Mckay Kerry, A, Çalik Çagdas, Chang Donghoon, Bassham Lawrence. Status report on the first round of the NIST lightweight cryptography standardization process. 2019
11. b10: Turan Meltem Sönmez, Mckay Kerry, Chang Donghoon, Calik Cagdas, Bassham Lawrence, Kang Jinkeon, et al.. "Status report on the second round of the NIST lightweight cryptography standardization process". and Technology Internal Report. 2021
12. b11: Biham Eli, Adi Shamir. "Differential cryptanalysis of DES-like cryptosystems". J Cryptol. 1991
13. b12: Matsui Mitsuru. "Linear cryptanalysis method for DES cipher". Advances in cryptology-EUROCRyPT'93: workshop on the theory and application of cryptographic techniques lofthus. 1993
14. b13: Mouha Nicky, Wang Qingju, Gu Dawu, Preneel Bart. "Differential and linear cryptanalysis using mixed-integer linear programming". Information security and cryptology: 7th international conference, inscrypt 2011. 2011-12-03
15. b14: Isola Phillip, Zhu Jun-Yan, Zhou Tinghui, Efros Alexei, A. "Image-to-image translation with conditional adversarial networks". Proceedings of the IEEE conference on computer vision and pattern recognition. 2017
16. b15: Strubell Emma, Ganesh Ananya, Mccallum Andrew. Energy and policy considerations for deep learning in NLP. 2019
17. b16: Chen Xiaozhi, Ma Huimin, Wan Ji, Li Bo, Xia Tian. "Multi-view 3d object detection network for autonomous driving". Proceedings of the IEEE conference on computer vision and pattern recognition. 2017
18. b17: Rivest Ronald, L. "Cryptography and machine learning". ASIACRyPT. 1991
19. b18: Maghrebi Houssem, Portigliatti Thibault, Prouff Emmanuel. "Breaking cryptographic implementations using deep learning techniques". Security, privacy, and applied cryptography engineering: 6th international conference, SPACE 2016. 2016
20. b19: Cagli Eleonora, Dumas Cécile, Prouff Emmanuel. "Convolutional neural networks with data augmentation against jitter-based countermeasures: Profiling attacks without pre-processing". Cryptographic hardware and embedded systems-CHES 2017: 19th international conference. 2017
21. b20: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
22. b21: Gerault Benamira Adrien, Peyrin David, Tan Thomas, Quan Quan. "A deeper look at machine learning-based cryptanalysis". Advances in cryptology-EUROCRyPT 2021: 40th annual international conference on the theory and applications of cryptographic techniques. 2021
23. b22: Su Heng-Chuan, Zhu Xuan-Yong, Ming Duan. "Polytopic attack on round-reduced simon32/64 using deep learning". Information security and cryptology: 16th international conference, inscrypt 2020. 2020
24. b23: Baksi Anubhab, Baksi Anubhab. "Machine learning-assisted differential distinguishers for lightweight ciphers". Class Phys Secur Symmetric Key Cryptogr Algorithms. 2022
25. b24: Rajan Reshma, Roy Rupam Kumar, Sen Diptakshi, Mishra Girish. "Deep learningbased differential distinguisher for lightweight cipher GIFT-cofb". Machine intelligence and smart systems: proceedings of MISS 2021. 2022
26. b25: Wang Meiqin. "Differential cryptanalysis of reduced-round PRESENT". Lecture Notes in Comput Sci. 2008
27. b26: Chen Yi, Shen Yantian, Yu Hongbo, Yuan Sitong. "A new neural distinguisher considering features derived from multiple ciphertext pairs". Comput J. 2023
28. b27: Bao Zhenzhen, Lu Jinyu, Zhang Yao Yiran, Liu. "More insight on deep learningaided cryptanalysis". International conference on the theory and application of cryptology and information security. 2023
29. b28: Liu Jiashuo, Ren Jiongjiong, Chen Shaozhen, Li Manman. "Improved neural distinguishers with multi-round and multi-splicing construction". J Inf Secur Appl. 2023
30. b29: Teng Wei Jian, Teh Je Sen, Jamil Norziana. "On the security of lightweight block ciphers against neural distinguishers: Observations on LBC-IoT and SLIM". J Inf Secur Appl. 2023
31. b30: Chakraborti Banik Subhadeep, Inoue Avik, Iwata Akiko, Minematsu Tetsu, Nandi Kazuhiko, Peyrin Mridul, et al.. "Gift-cofb". Cryptol ePrint Arch. 2020
32. b31: Dobraunig Christoph, Eichlseder Maria, Mendel Florian, Schläffer Martin. "Ascon v1. 2: lightweight authenticated encryption and hashing". Journal of Cryptology. 2021
33. b32: Bertoni Guido, Daemen Joan, Peeters Michaël, Assche Van, Gilles. "Duplexing the sponge: single-pass authenticated encryption and other applications". Selected areas in cryptography: 18th international workshop, SAC 2011. 2011
34. b33: Beaulieu Ray, Shors Douglas, Smith Jason, Treatman-Clark Stefan, Weeks Bryan, Wingers Louis. "The SIMON and SPECK lightweight block ciphers". Proceedings of the 52nd annual design automation conference. 2015
35. b34: Bernstein Daniel, J, Kölbl Stefan, Lucks Stefan, Pedro Maat Massolino, Mendel Costa, et al.. "Gimli: a cross-platform permutation". Cryptographic hardware and embedded systems-CHES 2017: 19th international conference. 2017
36. b35: Zhang Wentao, Ding Tianyou, Yang Bohan, Bao Zhenzhen, Xiang Zejun, Ji Fulei, et al.. "KNOT: algorithm specifications and supporting document". Submission to NIST lightweight cryptography project. 2019
37. b36: Mouha Nicky. "Chaskey: a MAC algorithm for microcontrollers-status update and proposal of chaskey-12". Cryptol ePrint Arch. 2015
38. b37: Zhu Baoyu, Dong Xiaoyang, Yu Hongbo. "MILP-based differential attack on roundreduced GIFT". Topics in cryptology-CT-RSA 2019: the cryptographers' track at the RSA conference 2019, san francisco. 2019
39. b38: Dobraunig Christoph, Eichlseder Maria, Mendel Florian, Schläffer Martin. "Cryptanalysis of ascon". Topics in cryptology-CT-RSA 2015: the cryptographer's track at the RSA conference 2015, san francisco. 2015
40. b39: Hou Zezhou, Ren Jiongjiong, Chen Shaozhen. "Improve neural distinguisher for cryptanalysis". Cryptol ePrint Arch. 2021
