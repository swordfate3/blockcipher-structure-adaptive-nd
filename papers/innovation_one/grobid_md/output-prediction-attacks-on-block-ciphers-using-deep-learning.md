# Output Prediction Attacks on Block Ciphers using Deep Learning *

**Authors:** Hayato Kimura, Keita Emura, Takanori Isobe, Ryoma Ito, Kazuto Ogawa, Toshihiro Ohigashi

**Source PDF:** `2021_output_prediction_block_ciphers_deep_learning.pdf`

## Abstract

Cryptanalysis of symmetric-key ciphers, e.g., linear/differential cryptanalysis, requires an adversary to know the internal structures of the target ciphers. On the other hand, deep learningbased cryptanalysis has attracted significant attention because the adversary is not assumed to have knowledge about the target ciphers with the exception of the algorithm interfaces. Such cryptanalysis in a blackbox setting is extremely strong; thus, we must design symmetric-key ciphers that are secure against deep learning-based cryptanalysis. However, almost previous attacks do not clarify what features or internal structures affect success probabilities. Although Benamira et al. (Eurocrypt 2021) and Chen et al. ( ePrint 2021 ) analyzed Gohr's results (CRYPTO 2019), they did not find any deep learning specific characteristic where it affects the success probabilities of deep learning-based attacks but does not affect those of linear/differential cryptanalysis. Therefore, it is difficult to employ the results of such cryptanalysis to design deep learning-resistant symmetric-key ciphers. In this paper, we propose deep learning-based output prediction attacks in a blackbox setting. As preliminary experiments, we first focus on two toy SPN block ciphers (small PRESENT-[4] and small AES-[4]) and one toy Feistel block cipher (small TWINE-[4]). Due to its small internal structures with a block size of 16 bits, we can construct deep learning models by employing the maximum number of plaintext/ciphertext pairs, and we can precisely calculate the rounds in which full diffusion occurs. Next, based on the preliminary experiments, we explore whether the evaluation results obtained by our attacks against three toy block ciphers can be applied to block ciphers with large block sizes, e.g., 32 and 64 bits. As a result, we demonstrate the following results, specifically for the SPN block ciphers: First, our attacks work against a similar number of rounds that the linear/differential attacks can be successful. Next, our attacks realize output predictions (precisely ciphertext prediction and plaintext recovery) that are much stronger than distinguishing attacks. Then, swapping or replacing the internal components of the target block ciphers affects the average success probabilities of the proposed attacks. It is particularly worth noting that this is a deep learning specific characteristic because swapping/replacing does not affect the average success probabilities of the linear/differential attacks. Finally, by analyzing the influence of the differences in the characteristics of three S-boxes (i.e., the original PRESENT S-box and two known weak S-boxes) on deep learning specific characteristics, we clarify that the resistance * An extended abstract appears in the 4th International Workshop on Artificial Intelligence and Industrial Internetof-Things Security (AIoTS 2022) [26] . This work was done when the first author, Hayato Kimura, was a master student at the Tokai University, Japan, and was a research assistant at the National Institute of Information and Communications Technology (NICT), Japan.

of the target ciphers to differential/linear attacks can affect the success probability of deep learning-based attacks. We also confirm whether the proposed attacks work on the Feistel block cipher. We expect that our results will be an important stepping stone in the design of deep learning-resistant symmetric-key ciphers.

Reference

## Introduction

Unlike public-key cryptography, where security is reduced to mathematically difficult problems, the security of symmetric-key cryptography is evaluated based on resistance against classical attacks, e.g., differential, linear, and integral attacks. Specifically, the corresponding statistical characteristics, e.g., differential, linear, and integral characteristics, are searched using automatic evaluation programs and tools, e.g., SAT and MILP solvers. If there is a considerable security margin against these characteristics, the cipher can be considered to be secure against such attacks. Generally, these evaluations require extensive knowledge about the target algorithms and state-of-the-art cryptanalysis techniques because automatic evaluation programs and tools must be customized for different target algorithms and attacks.

Recently, deep learning-based cryptanalysis has received considerable attention in the symmetrickey cryptography field [1, 5-8, 10-14, 17, 21, 22, 25, 35, 39-41] . Remarkably, such attacks do not require knowledge about the target ciphers, except for the algorithm interfaces, i.e., these attacks are feasible even if the adversary does not know the algorithm of the target ciphers. In a blackbox setting, such cryptanalysis is extremely strong, i.e., the adversary can mount an attack with minimum knowledge about the target ciphers and cryptanalysis techniques. Thus, we must consider deep learning-based cryptanalysis when designing symmetric-key ciphers. However, previous studies have not clarified the features or internal structures that affect the success probabilities. Recently, Benamira et al. [8] and Chen et al. [12] confirmed that the characteristics explored by Gohr [17] can be employed in classical distinguishing attacks. These results may be used to design deep learning-resistant symmetric-key ciphers; however, this may be insufficient because they did not identify any deep learning specific characteristic in such a manner that it affects the success probabilities of deep learning-based attacks but does not affect those of classical attacks such as linear/differential attacks. Finding such a deep learning specific characteristic is important because exploiting such a characteristic can make the target cipher vulnerable to deep learning-based attacks. Thus, the usage of previous results of these attacks to design such deep learning-resistant symmetric-key ciphers is difficult.


## Our Contribution

In this study, we present new deep learning-based attacks on block ciphers in a blackbox setting where the adversary does not know the algorithm of target ciphers with the exception of the algorithm interfaces, e.g., the key and block sizes. In a blackbox setting, deep learning-based cryptanalysis enables the use of pre-obtained input/output pairs to construct deep learning models for the proposed attacks, e.g., ciphertext prediction and plaintext recovery, and then we can use these models to evaluate the proposed attacks. The next step is to examine the correlations between the evaluation results obtained by deep learning-based cryptanalysis and the characteristics of the target block ciphers. Here, we use a whitebox analysis technique in the evaluation phase using deep learning models. The whitebox analysis explores the relationship between the ability of deep learning-based attacks and classical attacks, e.g., linear/differential attacks; therefore, it may be possible to clarify the correlations between evaluation results obtained by deep learning-based cryptanalysis and the characteristics of the target block ciphers.

To obtain highly accurate results from the whitebox analysis in a blackbox setting, we perform comprehensive analyses using all input/output pairs, i.e., it is not appropriate to target reducedround block ciphers because they have the same block size as the original block ciphers (e.g., 64 or 128 bits). For this reason, we first focus on toy block ciphers with a small block size (e.g., 16 bits) and perform the whitebox analysis against these toy block ciphers as preliminary experiments. Based on the preliminary experiments, we apply the proposed attacks to block ciphers with large block sizes (e.g., 32 and 64 bits) and consider the whitebox analysis against the target block ciphers. The details of our contributions in this study are given as follows.


## New Deep Learning-based Output Prediction Attacks

To perform the whitebox analysis against block ciphers with large block sizes, we first focus on two toy SPN block ciphers (16-bit block variants of PRESENT [9] called small PRESENT- [4] and an AES-like cipher called small AES- [4] ) and one toy Feistel block cipher (a type-II generalized Feistel structure with 4 branches called small TWINE- [4] ). This allows us to accurately compare the effectiveness of the proposed deep learning-based attacks, which guess the ciphertext/plaintext from the corresponding plaintext/ciphertext without any knowledge of keys with that of classical attacks.

Because of its small internal structures with a block size of 16 bits, we can develop deep learning models by exploiting the maximum number of plaintext/ciphertext pairs, and we can precisely calculate linear/differential probability for each round. We demonstrate that the proposed attacks are effective against the similar number of rounds as linear/differential attacks. For small PRESENT- [4] , we successfully mount output prediction attacks on 4 rounds, while the number of rounds that the differential distinguisher can work is 5. For small AES- [4] and small TWINE- [4] , we can mount output prediction attacks on 1 and 3 rounds, while differential distinguishing attacks can reach 3 and 7 rounds, respectively. Note that our attacks realize output predictions (i.e., ciphertext prediction and plaintext recovery) that are considerably stronger than distinguishing attacks even without knowing the algorithm of the target ciphers. Nevertheless, for small TWINE- [4] , the number of rounds that the proposed attacks can be successful is significantly less than that of linear/differential attacks. To clarify this cause, additional studies will be required in future.

Next, based on evaluation results for toy block ciphers, we apply the proposed attacks to the target block ciphers with a block size of 64 bits, i.e., PRESENT [9] , AES-like, and TWINE-like ciphers. Consequently, we consider that by increasing the amount of training data, the whitebox analysis against block ciphers with large block sizes can be regarded as equal to or greater than the whitebox analysis against toy block ciphers with a block size of 16 bits; thus, the whitebox analysis against the target block ciphers with large block sizes can be summarized as follows:

• For PRESENT, the maximum number of rounds that the proposed attacks can be successful is at least equal to that of classical linear/differential attacks.

• For AES-like and TWINE-like ciphers, we conjecture that the maximum number of rounds that the proposed attacks can be successful also becomes equal to that of classical linear/differential attacks when the amount of training data increases more.

In addition, we conduct additional experiments with 10,000 trials (rather than 100 trials) to confirm the accuracy of the success probability calculated from the proposed attacks. Consequently, we demonstrate that the additional experiments with a small number of secret keys are sufficient to obtain the best success probability, and therefore the proposed attacks lead to reliable results.


## Extended Whitebox Analysis on Small PRESENT-[4]

We swap or replace internal components on the toy SPN block cipher, particularly on the 4-round small PRESENT- [4] , to investigate the relationship between the internal components and success probability of our deep learning-based attacks, and evaluate the impact of these modifications on the success probability of the prediction attacks. The toy Feistel block cipher, i.e., small TWINE- [4] , is excluded from this investigation because Feistel block ciphers generally use the same components for both encryption and decryption algorithms. Consequently, we find that swapping or replacing the internal components significantly affects the average success probabilities of the proposed attacks. It is particularly worth noting that this is a deep learning specific characteristic because component swapping and replacing that we did in this study did not affect success probabilities of linear/differential attacks. We expect that our results will be an important foundation in the design of deep learning-resistant symmetric-key ciphers.


## Deeper Look into Whitebox Analysis Using Weak S-boxes

We look deeper into deep learning specific characteristics and extend the whitebox analysis to explore clues to facilitate the design of symmetric-key cryptographic algorithms that are secure against deep learning-based attacks. To perform the extended whitebox analysis, we employ two weak variants of small PRESENT- [4] by replacing the original S-box with known weak S-boxes. We select the weak S-box1 shown in Fig. 6 .1 in the literature [28] . This is used in an example of differential cryptanalysis and is known to be vulnerable to differential attacks. We also select the weak S-box2 shown in Fig. 7 .1 in the literature [28] , which is used in an example of linear cryptanalysis and is known to be vulnerable to linear attacks. Thus, we aim to analyze the influence of the differences in the characteristics of three S-boxes (i.e., the original PRESENT S-box and two weak S-boxes) on deep learning specific characteristics. As a result, the whitebox analysis against small PRESENT- [4] with weak S-boxes can be summarized as follows:

• For the small PRESENT- [4] with weak S-box1, we successfully mount output prediction attacks on 11 rounds, and the number of rounds that the differential and linear distinguishing attacks can work is 11 and 9, respectively.

• For the small PRESENT- [4] with weak S-box2, we successfully mount output prediction attacks on 8 rounds, and the number of rounds that the differential and linear distinguishing attacks can work is 7 and 8, respectively.

From these results, we conclude that the resistance of the target ciphers to differential/linear attacks can affect the success probability of deep learning-based attacks.


## Comparison with Existing Studies

Table 1 compares the proposed and existing deep learning-based attacks [1, 5-8, 10-14, 17, 21-23, 25, 35, 39-41]. For comparison, we particularly focused on whether these attacks correspond to a deep learning-based attack in a blackbox setting and a deep learning-based attack with the whitebox analysis. When an adversary performs a deep learning-based attack in a non-blackbox setting, the adversary must be familiar with the target ciphers as well as state-of-the-art cryptanalysis techniques. This degrades the original function of a deep learning-based attack in such a way that it does not require any knowledge of target ciphers and state-of-the-art cryptanalysis techniques, except algorithm interfaces. In addition, even if an adversary uses the whitebox analysis in a non-blackbox setting to perform a deep learning-based attack, this should not result in accurate Table 1: Comparison of deep learning-based cryptanalysis. OP:=Output Prediction, PR:=Plaintext Recovery, KR:=Key Recovery, DD:=Differential Distinguisher, LD:=Linear Distinguisher, and DLD:=Differential-Linear Distinguisher.

evaluations of the attack. In summary, it is important to perform a deep learning-based attack with the whitebox analysis in a blackbox setting. As shown in Table 1 , the proposed attacks are the first deep learning-based output prediction attacks with whitebox analysis on both SPN and Feistel structures in a blackbox setting.

Regarding the whitebox analysis, Danziger et al. presented deep learning-based attacks that predict key bits of 2-round DES from a plaintext/ciphertext set, and analyze the relationship between these attacks and the differential probability [14] . They compared variants employing several types of S-boxes with different properties for differential attacks, and they concluded that there is a nontrivial relationship between the differential characteristics and success probability of their deep learning-based attacks. However, their results are extremely limited because they targeted a two-round Feistel construction, which is quite insecure even if the component is ideal function. It is unclear how much the property of internal components affects the security of the whole construction. In addition to improve Gohr's deep learning-based attack [17] , Benamira et al. [8] and Chen et al. [12] improved the success probability of traditional distinguishers using characteristics that are expected to be reacted by Gohr's attack. Their work confirms whether characteristics explored by Gohr can be employed in the traditional distinguishing attacks and they did not identify any deep learning specific characteristic. However, we compare the ability of classical attack with that of our deep learning-based attacks and investigate a relationship among them. Then, we identify deep learning specific characteristics of small PRESENT- [4] . To summarize, to the best of our knowledge, our results are the first ones that perform the whitebox analysis.

Alani and Hu reported plaintext recovery attacks on DES, 3-DES, and AES [2, 24] that guess plaintexts from given ciphertexts. They claimed that attacks on DES, 3-DES, and AES are feasible with 2 11 , 2 11 and 1741 (≃ 2 10.76 ) plaintext/ciphertext pairs, respectively. However, Xiao et al. doubted the correctness of their results [2, 24] because they could not be reproduced. Baek et al. also pointed this out in the literature [4] . Therefore, we exclude these results in Table 1 . Mishra et al. reported that they mounted output prediction attacks on full-round PRESENT; however, it did not work well [16] . In addition, certain results have yielded classical ciphers such as Caesar cipher, Vigenere, and Enigma ciphers [15, 18, 19, 32] .

Other machine learning-based analyses have also been reported, e.g., [30, 31] . Tan et al. demonstrated that deep learning can be used to distinguish ciphertexts encrypted by AES, Blowfish, DES, 3-DES, and RC5, respectively [37] , for detecting the encryption algorithm that the malware utilizes. Alshammari et al. attempted to classify encrypted Skype and SSH traffic [3] .

Organization. The remainder of this paper is organized as follows. Our target ciphers, i.e., two SPN block ciphers and one Feistel block cipher (and their toy ciphers), are introduced in Sect. 2. The proposed deep learning-based output prediction attacks in a blackbox setting are introduced in Sect. 3. Our whitebox analysis is presented in Sect. 4, which explores the evaluation results obtained by our attacks against three toy block ciphers can be applied to block ciphers with large block sizes. The extended whitebox analyses on small PRESENT- [4] are discussed in Sects. 5 and 6. Finally, the paper is concluded in Sect. 7.


## Preliminaries

In this section, we introduce two SPN block ciphers (PRESENT [9] and AES-like cipher), one Feistel block cipher (TWINE-like cipher), and their toy ciphers (small PRESENT-[n] [29] , small AES-[n], and small TWINE-[n]).

PRESENT and small PRESENT-[n]: PRESENT [9] is a lightweight SPN block cipher with a 64-bit block size, 31 rounds, and a key size of either 80 or 128 bits. To analyze PRESENT, a Table 2: Original S-box for PRESENT and small PRESENT-[n] 29] has been proposed. We show the round function of small PRESENT-[n] in Fig. 1 . Since the block size is 4n, small PRESENT- [16] is equivalent to the original PRESENT. The variant n, which specifies the block size and round key length, allows us to control the round of full diffusion. The S-box has 4-bit input and output. We provide the correspondence table in Table 2 that maps F 4 2 → F 4 2 . The pLayer is described as bit permutation P (i), which is defined as follows. Note that this is a generalization of that of PRESENT and is equivalent to that of PRESENT when n = 16. P (i) is used for encryption and P -1 (i) is used for decryption.

For key scheduling, the key scheduling algorithm of PRESENT-80, which is a variant of PRESENT with a key length of 80, is executed; furthermore, the 4n rightmost bits are used as round keys rk i .


## AES-like and small AES-[n]: We design AES-like cipher with a 64-bit block size, called AESlike for short.

To analyze AES-like, we design its toy model called small AES-[n]. The round function of small AES is shown in Fig. 1 . As with the case of PRESENT, small AES- [16] is equivalent to AES-like since the block size is 4n. The S-box and key scheduling are the same as those of PRESENT. The maximum distance separable (MDS) matrix (over GF (2 4 ) defined by the irreducible polynomial x 4 + x + 1) is the same as that of Piccolo [34] , which is expressed as follows. Table 3: Weak S-box1 which is known to be vulnerable to differential attack. x 0 1 2 3 4 5 6 7 8 9 A B C D E F S[x] 6 4 C 5 0 7 2 E 1 F 3 D 8 A 9 B


## 7 8 9 A B C D E F S[x] F E B C D 7 8 0 3 9 A 4 2 1 5

When a 16-bit input X (16) is given, the output is computed as t (y 0(4) , y 1(4) , y 2(4) , y 3(4) ) ← M • t (x 0(4) , x 1(4) , x 2(4) , x 3(4) ).


## TWINE-like and small TWINE-[n]:

We design TWINE-like cipher with a 64-bit block size, called TWINE-like for short. To analyze TWINE-like, we design its toy model called small TWINE-[n]. For our design, we adopt the type-II generalized Feistel structure with n branches and similar F function as TWINE, which comprises round key operation and 4-bit S-box, as shown in Fig. 2 . As with the case of PRESENT, small TWINE- [16] is equivalent to TWINE-like since the block size is 4n. The S-box and key scheduling are the same as those of PRESENT. The pLayer is described as round permutation RP , which is defined as follows: RP : (y 0 , y 1 , . . . , y n-2 , y n-1 ) ← (x 1 , x 2 , . . . , x n-1 , x 0 ). Two sub-round keys, rk s i for s ∈ {0, 1, . . . , n 2 -1}, are used in each round, which are generated from the round key rk i as follows:


## Weak S-boxes:

We provide additional S-boxes called weak S-box1 and weak S-box2 in Tables 3 and 4 , respectively. These S-boxes were introduced in the literature [28] . The weak S-box1 is known to be vulnerable to differential attacks, whereas the weak S-box2 is known to be vulnerable to linear attacks. We construct two weak variants of small PRESENT- [4] for our experiments by replacing the original S-box with these S-boxes.


## Methodology

In this section, we present the proposed deep learning-based output prediction attacks in a blackbox setting. To realize the proposed attacks, we construct deep learning models for ciphertext prediction and plaintext recovery, respectively. In the following, we first discuss the goals of these attacks and then explain the construction of deep learning models and their evaluation.


## Goals of Attack

To date, the relationship between the abilities classical attacks and deep learning-based ones has not been clarified. Here, we focus on clarifying this relationship. We then revisit the common sense in previous works using deep learning-based attacks. The targets of this work are summarized as follows:

1. We clarify the difference in capabilities between the classical and deep learning-based attacks.

Specifically, we compare the success probabilities of deep learning-based attacks with those of classical attacks.

2. Swapping or replacing the internal components in the target block ciphers does not affect the success probability of linear/differential cryptanalysis. We clarify how such modifications to cipher's algorithms affect the success probability of deep learning-based attacks.

3. We clarify which vulnerabilities in the cryptographic components affect the accuracy of deep learning-based attacks. Specifically, we apply the classical and deep learning-based attacks to two weak variants of small PRESENT- [4] , as described in Sect. 2, and observe the differences in the capabilities of these attacks by comparing the success probabilities.

We evaluate the success probabilities of attacks using the following settings.


## Known-plaintext attack setting:

In this setting, the adversary is given multiple plaintext/ciphertext pairs relating to a single secret key, and the pairs are used as training data to construct a deep learning model.


## Blackbox setting:

In this setting, the adversary does not have knowledge about the target block ciphers, except algorithm interfaces such as key and block sizes.

In both of these settings, the adversary is a very weak cryptographic attacker. The blackbox setting assumes that the adversary does not know the internal structures of the cipher. In addition, the adversary does not know the cipher is a permutation. The blackbox setting also assumes that the adversary only knows the input-output format and possesses deep learning knowledge.

Regarding attack settings, a ciphertext-only attack setting, which allows the adversary to obtain only the ciphertext, is the weakest setting. However, information-theoretically no information is provided to the adversary in the setting except for several special cases, e.g., the broadcast setting of RC4 [33] . In fact, the attack in this setting is practically impossible. The known-plaintext attack is the next weakest setting. In this setting, the adversary can obtain some information from the given plaintext/ciphertext pairs and use these pairs for the attacks. The other attack settings, e.g., chosen-plaintext attack setting, require the adversary to possess some knowledge about the ciphertext, and the adversary in this setting is stronger than the adversary in the known-plaintext attack setting. Thus, we employ the known-plaintext attack setting.

In these settings, we decide the adversary's goal to output predictions (i.e., ciphertext prediction and/or plaintext recovery), and we evaluate the success probabilities of these attacks. The ciphertext prediction and plaintext recovery attacks are summarized as follows:

Ciphertext prediction attack: In this attack, the adversary obtains multiple plaintext/ciphertext pairs regarding a secret key, where n is the block size. Then, the adversary predicts a ciphertext of a plaintext not included in the previously given pairs. Table 5 : Hyperparameters Hyperparameters Search ranges Number of hidden nodes 100, 200, 300, 400, 500 Initial value of learning rates 0.0001, 0.001, 0.01 Number of hidden layers 1, 2, 3, 4, 5, 6, 7 Optimizers SGD, Adam [27] , RMSprop [38] Plaintext recovery attack: In this attack, the adversary obtains multiple plaintext/ciphertext pairs regarding a secret key, and then the adversary recovers a plaintext of a ciphertext that is not included in the pairs given previously.

If the ciphertext prediction attack is possible, forgery of the Cipher-based Message Authentication Code (CMAC) is possible. If the plaintext recovery attack is possible, the adversary can obtain the plaintext of any ciphertext without possessing the secret key used for encryption.


## Neural Network and Hyperparameters

Deep learning allows us to automatically extract features unlike statistical machine learning techniques, e.g., Bayesian inference. Deep learning treats nonlinear separable problems; thus, it appears to work well for simulating cryptographic functions with nonlinearity. Hyperparameters such as the initial learning rate, number of hidden nodes (neurons), and optimizers, are defined prior to the learning phase and are used to construct models. These parameters affect model performance; thus, they are optimized using assessment metrics.

In this paper, we consider ciphertext prediction and plaintext recovery as regression problems with supervised learning where plaintext/ciphertext pairs are used as training data. To this end, we must extract numerous features from the plaintext/ciphertext pairs obtained under the knownplaintext attack; therefore, we employ long short-term memory (LSTM) which is a type of recurrent neural networks (RNN) [20] . The LSTM, which is a general technique for mapping sequences to sequences with neural networks, is used in the field of machine translation [36] . As the LSTM can realize the mapping between sequences in machine translation, we consider that it can also realize the mapping between sequences (i.e., between plaintexts and ciphertexts) in encryption/decryption of permutation-based block ciphers. In addition, we consider that numerous features can be extracted from plaintext/ciphertext pairs, i.e., the inputs to our deep learning models, by using the LSTM, which enables long-term memory of input sequences. In fact, we have confirmed that the use of the LSTM induces better experimental results than that of the convolutional neural network (CNN), as described in Appendix A for more details. We then optimize hyperparameters, e.g., number of hidden nodes, initial learning rates, number of hidden layers, and optimizers. Table 5 shows the search range for each hyperparameter. During the hyperparameter optimization, we use different secret keys from those used in the construction of deep learning models because we strictly evaluate the success probabilities of ciphertext prediction and plaintext recovery without depending on secret keys. In the following, the procedure to optimize hyperparameters is similar to constructing deep learning models, with the exception of the number of secret keys.


## Deep Learning Models and Their Evaluation

We construct and evaluate deep learning models for ciphertext prediction according to the following procedure. Note that we show the plaintext recovery case in parentheses.


## Step 1.

The adversary obtains multiple plaintext/ciphertext pairs under the known-plaintext attack. In our experiments, we randomly select multiple plaintexts and generate ciphertexts corresponding to the selected plaintexts.


## Step 2.

The adversary uses the obtained plaintext/ciphertext pairs as training data to construct deep learning models. Then, the adversary constructs a deep learning model for ciphertext prediction (plaintext recovery) using the plaintexts (ciphertexts) as inputs and the ciphertexts (plaintexts) as the correct outputs.


## Step 3.

The adversary uses all or part of the remaining plaintexts (ciphertexts), which were not used as training data, to evaluate the constructed deep learning models. The adversary uses these plaintexts (ciphertexts) as the input to the constructed deep learning models. Then, the adversary predicts the unknown ciphertext (plaintext) corresponding to each plaintext (ciphertext).


## Step 4.

The adversary calculates the percentage of exact match between the predicted ciphertext (plaintext) and the correct ciphertext (plaintext) as the predicted probability.

To evaluate the predicted probabilities, we use 2 x plaintext/ciphertext pairs as training data and 2 y plaintext/ciphertext of the remaining plaintext/ciphertext pairs as test data when applying the proposed attacks against the target block ciphers with a block size of 4n bits. It should be noted here that 2 x + 2 y ≤ 2 4n . In this case, if the predicted probability is greater than (2 4n -2 x ) - foot_0 , we consider the proposed attacks to be successful. This means that an attacker without knowledge of the target algorithms can predict the output value with a higher probability than a random probability.


## Whitebox Analysis

In this section, we perform the whitebox analysis to explore the relationship between the ability of deep learning-based attacks and the classical attacks such as linear/differential attacks against three block ciphers based on our methodology presented in Sect. 3. We first use three toy block ciphers with a block size of 16 bits as a testbed for the proposed attacks. Based on these preliminary experiments, we then apply the proposed attacks to block ciphers with large block sizes, such as 32 and 64 bits. Finally, we conduct additional experiments to ensure that our whitebox analysis is accurate.


## Application to Toy Block Ciphers

In this subsection, we apply the proposed attacks to three toy block ciphers, i.e., small PRESENT- [4] , small AES- [4] , and small TWINE- [4] , as preliminary experiments. We first explain the experimental procedure for our whitebox analysis and then demonstrate experimental results to compare the number of rounds that the proposed attacks can be successful to that of existing classical attacks.


## Experimental Procedure

In our experiments, we implement the proposed attacks using Keras 1 , which is a deep learning library, and we employ TensorFlow as the backend. The following is our experimental environment: 8 Linux machines with 14 NVIDIA GPUs (RTX 2080 SUPER, GeForce GTX 1080 Ti,

Table 6: Experimental hyperparameters Hyperparameters Values Number of input layer nodes (i.e., block sizes) 16, 32, 64 Number of output layer nodes (i.e., block sizes) 16, 32, 64 Batch size 250 Number of epochs 100

TITAN Xp, Tesla K40m, and Quadro P600 Mobile). For developing LSTM models by Keras, e.g., model.add(LSTM(...)), we specify only units, input shape, and return sequences as its arguments foot_1 . As an initial setting, we use common experimental hyperparameter values (see Table 6 ).

Our experiments involve the following two sub-experiments, i.e., Experiment 1 and Experiment 2.


## Experiment 1:

In each round, we optimize hyperparameters for the target block ciphers using the proposed attacks, as described in Sect. 3.2. For our hyperparameter optimization, we use Optuna foot_2 , which is an automatic optimization tool, and use its default search algorithm. The indication for our hyperparameter optimization is the success probability of ciphertext prediction or plaintext recovery. In our hyperparameter optimization, we obtain 100 hyperparameter candidates from the plaintext/ciphertext pairs generated by 20 secret keys. From these candidates, we select the optimized hyperparameter with the highest average success probabilities of ciphertext prediction or plaintext recovery. To this end, we use 2 15 plaintext/ciphertext pairs as training data and remaining 2 15 plaintext or ciphertext as testing data; thus, each average success probability is calculated from 2 15 randomly generated plaintext/ciphertext pairs. If the average success probabilities of ciphertext prediction or plaintext recovery with the optimized hyperparameter is greater than 2 -15 , then the number of rounds for finding the optimized hyperparameter is incremented by one; otherwise, the second sub-experiment is executed using the optimized hyperparameter.


## Experiment 2:

We use randomly generated 100 secret keys and the optimized hyperparameters obtained in Experiment 1 to execute the proposed attacks for ciphertext prediction or plaintext recovery; then, we compute the average success probabilities of ciphertext prediction or plaintext recovery. The secret keys used in Experiment 2 are not the same as those used in Experiment 1.

After clarifying the number of attacked rounds for target block ciphers by Experiment 2, we use experimental results and linear/differential probability of the target block ciphers to compare the proposed attacks to the classical linear/differential attacks.


## Experimental Results

Table 7 shows the experimental results of Experiment 2 using the optimized hyperparameter obtained in Experiment 1. Based on these experimental results, we discuss the whitebox analysis against three toy block ciphers, i.e., small PRESENT- [4] , small AES- [4] , and small TWINE- [4] . First, we compare the proposed and classical linear/differential attacks for small PRESENT- [4] . From the experimental results, the proposed attacks succeed up to 5 rounds for ciphertext prediction and up to 4 rounds for plaintext recovery against small PRESENT- [4] . Although the average success probability of ciphertext prediction for the 5-round small PRESENT-[4] is nearly 2 -15 , the average success probability of plaintext recovery for the 4-round small PRESENT- [4] is sufficiently greater than 2 -15 . In other words, we consider that the proposed attacks can be successful for a maximum of 4 rounds. On the other hand, from the precisely calculated differential probability of small PRESENT- [4] (see Table 8 ), the maximum number of rounds that the differential attack can be successful is 5. Similarly, based on the precisely calculated linear probability (see Table 9 ), the maximum number of rounds that a linear attack can be successful is 4. Therefore, for small PRESENT- [4] , the maximum number of rounds that the proposed attack can be successful is equivalent to that of classical linear/differential attacks. Next, we compare the proposed and classical linear/differential attacks for small AES- [4] . From Table 7 , we evaluate the maximum number of rounds that the proposed attacks can be successful is 1. From the precisely calculated linear/differential probabilities, the maximum number of rounds that the differential attack can be successful is 3 and that of the linear attack is also 3. Similarly, we compare the proposed attacks and classical linear/differential attacks for small TWINE- [4] . We discovered that the proposed attack can be successful for a maximum of 3 rounds with the differential attack lasting 7 rounds and the linear attack lasting 7 rounds. In summary, for small AES- [4] and Table 8 : Maximum differential probabilities of small PRESENT- [4] , small AES- [4] , and small TWINE- [4] .


## Round

Maximum differential probability small PRESENT- [4] small AES- [4] small TWINE-[4] 1 2 -2 2 -2 2 0 2 2 - foot_3 2 -10 2 -2 3 2 -8 2 -14 2 -4 4 2 -12 2 -20 2 -6 5 2 -14 -2 -8 6 2 -16 -2 -12 7 --2 -14 8 --2 -16

9 --small TWINE- [4] , the maximum number of rounds that the proposed attacks can be successful is less than that of the classical linear/differential attacks. It should be noted here that the proposed attacks realize much stronger ciphertext prediction and plaintext recovery than the distinguishing attacks of the classical linear/differential cryptanalysis. Nevertheless, for small TWINE- [4] , the maximum number of rounds that the proposed attacks can be successful is significantly smaller than that of the classical linear/differential attacks. This cause will be clarified in a future study.


## Whitebox Analysis with the Smaller Amount of Training Data

To perform the whitebox analysis with the smaller amount of training data against three toy block ciphers (i.e., 1-, 2-, 3-, 4-round small PRESENT-[4], 1-round small AES- [4] , and 1-, 2-, 3-round small TWINE-[4]), we conduct additional experiments in the same procedure described above, but we vary the amount of training data in the range of from 2 2 to 2 14 and use all the remaining plaintexts or ciphertexts as testing data. In these additional experiments, we use the optimized hyperparameters obtained in Experiment 1 (see Table 7 ). Table 10 shows the minimum amount of training data required for successful ciphertext prediction/plaintext recovery against three toy block ciphers. In addition, Table B .1 in Appendix B shows more detailed results regarding the average success probabilities of ciphertext prediction/plaintext recovery by the proposed attacks against three toy block ciphers with a block size of 16 bits. If the predicted probability is greater than 2 -15 , we consider the proposed attacks to be successful 4 . Consequently, we demonstrate successful ciphertext prediction/plaintext recovery with a smaller amount of training data than 2 15 against three toy block ciphers, with the exception of the 4-round small PRESENT- [4] .


## Application to Block Ciphers with Large Block Sizes

In this subsection, we apply the proposed attacks to three block ciphers with large block sizes based on the preliminary experiments as described in Sect. 4.1. To examine the evaluation results obtained by our whitebox analysis against three toy block ciphers can be applied to the target Table 9 : Maximum linear probabilities of small PRESENT- [4] , small AES- [4] , and small TWINE- [4] .


## Round

Maximum linear probability small PRESENT- [4] small AES- [4] block ciphers with large block sizes, we conduct Experiment 2 in the same procedure as described in Sect. 4.1.1, but we change the block sizes of the target block ciphers, e.g., 32 and 64 bits. In our experiments, we use the optimized hyperparameters obtained in Experiment 1 (see Table 7 ). Tables 11 and 12 show the minimum amount of training data required for successful ciphertext prediction/plaintext recovery against three block ciphers with block sizes of 32 and 64 bits, respectively. We vary the amount of training data in the range of from 2 8 to 2 17 or from 2 10 to 2 19 and use 2 16 of the remaining plaintexts or ciphertexts as testing data against three toy block ciphers with block sizes of 32 or 64 bits, respectively; thus, if the predicted probability is greater than the threshold derived by equation (2 4n -2 x ) -1 shown in Sect. 3.3, we consider the proposed attacks to be successful for both cases. In this case, those thresholds are (2 32 -2 8 ) -1 to (2 32 -2 17 ) -1 or from (2 64 -2 10 ) -1 to (2 64 -2 19 ) -1 . In addition, Tables C.1 and C.2 in Appendix C show more detailed results regarding the average success probabilities of ciphertext prediction/plaintext recovery by the proposed attacks against three block ciphers with block sizes of 32 and 64 bits. From Tables 11 and C .1, we report that the average success probabilities of ciphertext prediction/plaintext recovery by the proposed attacks against the target block ciphers with a block size of 32 bits are not zero, excluding the 4-round small PRESENT- [8] . Expressed differently, this fact should indicate that the proposed attacks against the target block ciphers with large block sizes can be successful by simply increasing the amount of training data; thus, we consider that the proposed attack against the target block ciphers with additional rounds could be successful by using more training data than 2 17 .

From Tables 12 and C .2, we can confirm that except for the 4-round small PRESENT- [16] and the 3-round small TWINE- [16] , the average success probabilities of ciphertext prediction/plaintext recovery by the proposed attacks against the target block ciphers with a block size of 64 bits are


## Accuracy of Experimental Results

In Sect. 4.1, we have presented the experimental results of Experiment 1 with 20 secret keys and Experiment 2 with 100 secret keys. These experimental results may appear to be correct. However, because of the small number of secret keys used in these experiments, we should have an additional discussion to ensure that the experimental results are accurate. To this end, this subsection shows two additional experimental results on the 3-round small TWINE- [4] with 100 secret keys for Experiment 1 and 10000 secret keys for Experiment 2, respectively. The following explains why we chose the 3-round small TWINE- [4] for confirming the accuracy: If we choose a target with a probability of 1 or 2 -15 , it appears difficult to see how the number of secret keys affects the accuracy. As shown in Table 7 , the average success probabilities of ciphertext prediction and plaintext recovery by the proposed attacks in the 3-round small TWINE-[4] are approximately 2 -10.46 and 2 -9.72 , respectively. We choose the 3-round small TWINE- [4] as the best target for additional experiments because these probabilities possibly vary significantly if the number of keys affects the accuracy.


## Experimental Procedure

We explain the following two additional experiments, i.e., Experiment 1' and Experiment 2'.


## Experiment 1':

We use the same procedures as in Experiment 1 to optimize the hyperparameters for the 3-round small TWINE- [4] . Unlike Experiment 1, we use plaintext/ciphertext pairs generated by 100 secret keys rather than 20 secret keys in this experiment. In the hyperparameter optimization, we examine the impact of the number of secret keys used in Experiment 1' on the experimental results.


## Experiment 2':

We obtain the average success probabilities of ciphertext prediction/plaintext recovery for the 3-round small TWINE- [4] in the same procedures of Experiment 2 using the hyperparameters optimized by Experiment 1 (see Table 7 ). Unlike Experiment 2, we use the plaintext/ciphertext pairs generated by 10000 secret keys rather than 100 secret keys. In the ciphertext prediction/plaintext recovery, we explore the influence of the number of secret keys used in Experiment 2' on the experimental results.


## Experimental Results.

Table 13 shows a comparison of the experimental results in Experiment 1 and Experiment 1' for the 3-round small TWINE- [4] . From the table, in the hyperparameter optimization for ciphertext prediction, the highest average success probabilities obtained from Experiment 1 and Experiment 1' are nearly equal, such as 2 -11.42 and 2 -11.26 . Conversely, in the hyperparameter optimization for the plaintext recovery, the highest average success probability obtained from Experiment 1 is much higher than that obtained from Experiment 1', such as 2 -7.80 and 2 -12.82 . As per these experimental results, optimizing the hyperparameters with a small number of secret keys is sufficient to obtain hyperparameters with the best average success probability; therefore, we consider that the hyperparameter optimization presented in Sect. 4.1 has led to reliable results.

Table 14 shows a comparison of experimental results in Experiment 2 and Experiment 2' for the 3-round small TWINE- [4] . We can see from the table that in both ciphertext prediction and plaintext recoveries, the average success probabilities obtained from Experiment 2 and Experiment 2' are nearly equal , such as 2 -10.46 and 2 -10.64 in the ciphertext prediction and 2 -9.72 and 2 -9.22 in the plaintext recovery. According to these experimental results, the additional experiments with a small number of secret keys are sufficient to obtain the best average success probability; therefore,


## Extended Whitebox Analysis on Small PRESENT-[4]

As shown in Table 7 , the average success probability of ciphertext prediction by the proposed attack on the 4-round small PRESENT-[4] is approximately 2 9 times greater than that of plaintext recovery. However, the security of the encryption and decryption is thought to be equivalent in terms of the linear/differential probabilities on small PRESENT- [4] ; thus, the experimental result of the proposed attacks on the 4-round small PRESENT- [4] seems contrary to intuition. We speculate that this can be a deep learning specific characteristic. In this section, we redesign the 4-round small PRESENT- [4] by swapping or replacing the internal components, e.g., S-box and bit permutation, and execute Experiment 1 and Experiment 2 against the new designs of the 4-round small PRESENT- [4] to reveal the relationship between the designs of block ciphers and average success probability of the proposed attacks.


## Experimental Procedure

We discuss two types of experiments to investigate the average success probabilities of ciphertext prediction and plaintext recovery by the proposed attacks under the conditions that (1) the substitution layer (sLayer) and its inverse function (sLayer-inv) are replaced, and (2) the order of the sLayer and permutation layer (pLayer) is swapped in the encryption and decryption algorithms. The target toy block ciphers are the 4-round small PRESENT-[4] and the 2-round small AES- [4] , and small TWINE- [4] is excluded from the target of these experiments. This is because the Feistel block ciphers generally use the same components for both encryption and decryption algorithms. The order of the sLayer and pLayer is the same in both the encryption and decryption algorithms, and sLayer-inv is not used in neither the encryption nor decryption algorithms. Rather than the experiments described in this section, we should compare the maximum number of rounds that the


## Conclusion

In this study, we first presented deep learning-based output prediction attacks on three block ciphers with a block size of 64 bits in a blackbox setting. We clarified the following results by examining the relationship between the ability of deep learning-based attacks and classical attacks such as linear/differential attacks:

• For PRESENT, the maximum number of rounds that the proposed attack can be successful is at least equal to that of classical linear/differential attacks.

• For AES-like and TWINE-like ciphers, we conjecture that the maximum number of rounds that the proposed attacks can be successful also becomes equal to that of classical linear/differential attacks when the amount of training data is increased more.

Next, we redesigned the 4-round small PRESENT- [4] by swapping or replacing the internal components, and we used the whitebox analysis technique to examine the relationship between the new target cipher designs and the success probability of the proposed attacks. Consequently, we clarified that swapping or replacing the internal components did not affect success probabilities of the classical linear/differential attacks, whereas it affects the average success probabilities of the proposed deep learning-based attacks; thus, we have obtained a deep learning specific characteristic. The obtained results are expected to be a foundation for designing deep learning-resistant symmetric-key ciphers.

Finally, to look deeper into deep learning specific characteristics, we employed two weak variants of small PRESENT- [4] , and we extended the whitebox analysis to explore clues to facilitate the design of symmetric-key cryptographic algorithms that are secure against deep learning-based attacks. We clarified the following results by examining the relationship between the ability of deep learning-based attacks and classical attacks, e.g., linear/differential attacks:

• Our deep learning-based whitebox analysis achieved the same attack capability as classical methods even when the S-box of the target cipher was changed to a weak one.

• We found that the success probability of our deep learning-based whitebox analysis tends to be affected by the success probability of classical cryptanalysis methods.

• We believe that output prediction attacks using deep learning will make it easier to estimate the resistance to differential and linear attacks, even without possessing knowledge about the target cryptographic algorithm or cryptanalysis methods.

We have the following future works:

• Clarify why the maximum number of rounds that the proposed attacks can be successful is significantly smaller than that of the linear/differential attacks for small TWINE- [4] .

• Clarify why swapping or replacing internal components affects the average success probabilities of our deep learning-based attacks, although it does not affect those of linear/differential attacks.

• Compare the maximum number of rounds that the proposed attacks can be successful against TWINE-like cipher (a type-II generalized Feistel cipher) to that of the other types of the Feistel block ciphers, such as classical, unbalanced, alternating, type-I and type-III generalized Feistel ciphers.

• Clarify whether the maximum number of rounds that the proposed attacks can be successful against AES-like and TWINE-like ciphers is equal to that of classical linear/differential attacks by conducting additional experiments with a larger amount of training data than 2 19 .

• Clarify why differences are observed in the average success probabilities regarding the underlying optimizer.

• Clarify how to feedback our results for designing deep learning-resistant symmetric-key ciphers.


## A Experimental Results Using the CNN

To confirm that the use of the LSTM induces better experimental results than that of the CNN, we conducted experiments using the CNN in the same procedure described in Sect. 4.1.1. In our experiments, we optimize activation functions in addition to the hyperparameters shown in Table 5 . The following is the search range for activation functions: Tanh, Sigmoid, and ReLU. For developing CNN models by Keras, e.g., model.add(Conv1D(...)), we specify only filters, kernel size, activation, and input shape as its arguments foot_4 . Table A .1 shows experimental results using the CNN. Consequently, we clarify the following facts by comparing the experimental results using the LSTM and CNN based on Tables 7 and A .1:

• For small PRESENT- [4] , the maximum number of rounds that the proposed attacks using the LSTM and CNN can be successful is 4 and 3, respectively.

• For small AES- [4] , the maximum number of rounds that the proposed attacks using the LSTM and CNN can be successful is 1 for each case. In addition, the average success probabilities of ciphertext prediction (plaintext recovery) by the proposed attacks against the 1-round small AES-[4] using the LSTM and CNN are 1 (1) and 2 -11.88 (2 -11.83 ), respectively.

• For small TWINE- [4] , the maximum number of rounds that the proposed attacks using the LSTM and CNN can be successful is 3 and 1, respectively.

To summarize the foregoing facts, we conclude that the use of the LSTM induces better experimental results of all the target block ciphers compared to the use of the CNN.


## B More Detailed Results in Sect. 4.1.3

Table B.1 details the experimental results shown in Table 10 (refer to Sect. 4.1.3 for more details). If the predicted probability is greater than 2 -15 , we consider the proposed attacks to be successful 6 .

> 1 Figure 1 : Figure 1: (a) Round Functions of small PRESENT-[n] and small AES-[n], (b) Last Round Function of small AES-[n].

> . x 0 1 2 3 4 5 6 7 8 9 A B C D E F S[x] C 5 6 B 9 0 A D 3 E F 8 4 7 1 2 toy model of PRESENT called small PRESENT-[n]

> [

> 2 Figure 2 : Figure 2: Round Function of small TWINE-[n]

> 0xF,where ≫ and & are bitwise right shift operation and bitwise AND operation, respectively.

> 4 Table 4 : Weak S-box2 which is known to be vulnerable to linear attack.

> 7 Table 7 : Average success probabilities of ciphertext prediction/plaintext recovery using the proposed attacks against three toy block ciphers with a block size of 16 bits. We use 215 training data and the remaining 215 testing data. CP:=Ciphertext Prediction and PR:=Plaintext Recovery.

> 10 Table 10 : Minimum amount of training data required for successful ciphertext prediction/plaintext recovery using the proposed attacks against three toy block ciphers with a block size of 16 bits. We use the optimized hyperparameters obtained in Experiment 1 (see Table7). CP:=Ciphertext Prediction and PR:=Plaintext Recovery.

> 11 Table 11 : Minimum amount of training data required for successful ciphertext prediction/plaintext recovery using the proposed attacks against three block ciphers with a block size of 32 bits. We use the optimized hyperparameters obtained in Experiment 1 (see Table7). CP:=Ciphertext Prediction and PR:=Plaintext Recovery.

> 13 Table 13 : Comparison of the experimental results in Experiment 1 and Experiment 1' for the 3round small TWINE- [4] .

> 14 Table 14 : Comparison of experimental results in Experiment 2 and Experiment 2' for the 3-round small TWINE- [4] . We use the optimized hyperparameters obtained in Experiment 1 (see Table7).

> 18 Table 18 : Maximum differential probabilities of small PRESENT- [4] with weak S-boxes.

> 19 Table 19 : Maximum linear probabilities of small PRESENT- [4] with weak S-boxes.

> 20 Table 20 : Maximum attackable round of small PRESENT- [4] with weak/original S-boxes. CP:=Ciphertext Prediction and PR:=Plaintext Recovery.

## Acknowledgements

This work was supported in part by the JSPS KAKENHI Grant Number 19K11971 .

## References

1. b0: M Khaled, Alaa H Alallayah, Waiel Alhamami, Mohamed Abdelwahed, Amin. "Applying Neural Networks for Simplified Data Encryption Standard (SDES) Cipher System Cryptanalysis". Int. Arab J. Inf. Technol. 2012
2. b1: M Mohammed, Alani. "Neuro-Cryptanalysis of DES and Triple-DES". ICONIP. 2012
3. b2: Riyad Alshammari, A Nur Zincir-Heywood. "Machine learning based encrypted traffic classification: Identifying SSH and Skype". 2009 IEEE Symposium on Computational Intelligence for Security and Defense Applications. 2009-07. DOI: 10.1109/cisda.2009.5356534
4. b3: Seunggeun Baek, Kwangjo Kim. "Integral Attacks on Some Lightweight Block Ciphers". KSII Transactions on Internet and Information Systems. 2020-11-30. DOI: 10.3837/tiis.2020.11.014
5. b4: Abbas Ghaemi Bafghi, Reza Safabakhsh, Babak Sadeghiyan. "Finding the differential characteristics of block ciphers with neural networks". Information Sciences. 2008
6. b5: Anubhab Baksi, Jakub Breier, Yi Chen, Xiaoyang Dong. "Machine Learning Assisted Differential Distinguishers For Lightweight Ciphers". 2021 Design, Automation & Test in Europe Conference & Exhibition (DATE). 2021-02-01. DOI: 10.23919/date51398.2021.9474092
7. b6: Zhenzhen Bao, Jian Guo, Meicheng Liu, Li Ma, Yi Tu. "Conditional Differential-Neural Cryptanalysis". IACR Cryptol. 2021
8. b7: Adrien Benamira, David Gerault, Thomas Peyrin, Quan Quan Tan. "A Deeper Look at Machine Learning-Based Cryptanalysis". Lecture Notes in Computer Science. 2021. DOI: 10.1007/978-3-030-77870-5_28
9. b8: Andrey Bogdanov, Lars R Knudsen, Gregor Leander, Christof Paar, Axel Poschmann, M J B Robshaw, et al.. "PRESENT: An Ultra-Lightweight Block Cipher". Lecture Notes in Computer Science. 2007. DOI: 10.1007/978-3-540-74735-2_31
10. b9: Yi Chen, Yantian Shen, Hongbo Yu. "Neural-Aided Statistical Attack for Cryptanalysis". The Computer Journal. 2020. DOI: 10.1093/comjnl/bxac099
11. b10: Yi Chen, Yantian Shen, Hongbo Yu, Sitong Yuan. "A New Neural Distinguisher Considering Features Derived From Multiple Ciphertext Pairs". The Computer Journal. 2021. DOI: 10.1093/comjnl/bxac019
12. b11: Yi Chen, Hongbo Yu. "Bridging Machine Learning and Cryptanalysis via EDLCT". IACR Cryptol. 2021
13. b12: Yi Chen, Yantian Shen, Hongbo Yu. "Neural-Aided Statistical Attack for Cryptanalysis". The Computer Journal. 2021. DOI: 10.1093/comjnl/bxac099
14. b13: Moises Danziger, Marco Aurelio Amaral Henriques. "Improved cryptanalysis combining differential and artificial neural network schemes". 2014 International Telecommunications Symposium (ITS). 2014-08. DOI: 10.1109/its.2014.6948008
15. b14: Riccardo Focardi, Flaminia L Luccio. "Neural Cryptanalysis of Classical Ciphers". ICTCS. 2018
16. b15: Girish Sk Pal, Mishra, Krishna Svssnvg, Murthy. "Neural Network Based Analysis of Lightweight Block Cipher PRESENT". Harmony Search and Nature Inspired Optimization Algorithms. 2019
17. b16: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
18. b17: Aidan N Gomez, Sicong Huang, Ivan Zhang, Bryan M Li, Muhammad Osama, Lukasz Kaiser. Unsupervised Cipher Cracking Using Discrete GANs. 2018
19. b18: Sam Greydanus. Learning the Enigma with Recurrent Neural Networks. 2017
20. b19: Sepp Hochreiter, Jürgen Schmidhuber. "Long Short-Term Memory". Neural Computation. 1997-11-01. DOI: 10.1162/neco.1997.9.8.1735
21. b20: Botao Hou, Yongqiang Li, Haoyue Zhao, Bin Wu. "Linear Attack on Round-Reduced DES Using Deep Learning". Lecture Notes in Computer Science. 2020. DOI: 10.1007/978-3-030-59013-0_7
22. b21: Zezhou Hou, Jiongjiong Ren, Shaozhen Chen. "Cryptanalysis of Round-Reduced SIMON32 Based on Deep Learning". IACR Cryptol. ePrint Arch. 2021
23. b22: Zezhou Hou, Jiongjiong Ren, Shaozhen Chen. "Improve Neural Distinguishers of SIMON and SPECK". Security and Communication Networks. 2021-12-31. DOI: 10.1155/2021/9288229
24. b23: Xinyi Hu, Yaqun Zhao. "Research on Plaintext Restoration of AES Based on Neural Network". Security and Communication Networks. 2018-11-18. DOI: 10.1155/2018/6868506
25. b24: Mohamed Fadl Idris, Je, Sen Teh, Jasy Liew, Suet Yan, Wei-Zhu Yeoh. "A Deep Learning Approach for Active S-Box Prediction of Lightweight Generalized Feistel Block Ciphers". IEEE Access. 2021
26. b25: Hayato Kimura, Keita Emura, Takanori Isobe, Ryoma Ito, Kazuto Ogawa, Toshihiro Ohigashi, et al.. "Applied Cryptography and Network Security Workshops". Applied Cryptography and Network Security Workshops -ACNS 2022 Satellite Workshops, AIBlock, AIHWS, AIoTS, CIMSS, Cloud S&P, SCI, SecMT. 2022. DOI: 10.1007/978-3-031-16815-4
27. b26: P Diederik, Jimmy Kingma, Ba. "Zunz, Leopold". Encyclopedia of Romantic Nationalism in Europe. 2015-04-15. DOI: 10.5117/9789462981188/ngfm4f56sgwxsqsaygobrmep
28. b27: Lars R Knudsen, Matthew J B Robshaw. "The Block Cipher Companion". Information Security and Cryptography. 2011. DOI: 10.1007/978-3-642-17342-4
29. b28: Gregor Leander, Shahram Rasoolzadeh. "Weak Tweak-Keys for the CRAFT Block Cipher". IACR Transactions on Symmetric Cryptology. 2010. DOI: 10.46586/tosc.v2022.i1.38-63
30. b29: Ting Rong Lee, Je Sen Teh, Norziana Jamil, Jasy Liew Suet Yan, Jiageng Chen. "Lightweight Block Cipher Security Evaluation Based on Machine Learning Classifiers and Active S-Boxes". IEEE Access. 2020. DOI: 10.1109/access.2021.3116468
31. b30: Je Ting Rong Lee, Sen Teh, Norziana Jamil, Jasy Liew, Suet Yan, Jiageng Chen. "Lightweight Block Cipher Security Evaluation Based on Machine Learning Classifiers and Active S-Boxes". IEEE Access. 2021
32. b31: Yu Liu, Jianshu Chen, Li Deng. "Unsupervised Sequence Classification using Sequential Output Statistics". NIPS. 2017
33. b32: Itsik Mantin, Adi Shamir. "A Practical Attack on Broadcast RC4". Lecture Notes in Computer Science. 2001. DOI: 10.1007/3-540-45473-x_13
34. b33: Kyoji Shibutani, Takanori Isobe, Harunaga Hiwatari, Atsushi Mitsuda, Toru Akishita, Taizo Shirai. "Piccolo: An Ultra-Lightweight Blockcipher". Lecture Notes in Computer Science. 2011. DOI: 10.1007/978-3-642-23951-9_23
35. b34: Jaewoo So. "Deep Learning-Based Cryptanalysis of Lightweight Block Ciphers". Security and Communication Networks. 2020-07-13. DOI: 10.1155/2020/3701067
36. b35: Ilya Sutskever, Oriol Vinyals, V Quoc, Le. "Sequence to Sequence Learning with Neural Networks". NIPS. 2014
37. b36: Cheng Tan, Qingbing Ji. "An approach to identifying cryptographic algorithm from ciphertext". 2016 8th IEEE International Conference on Communication Software and Networks (ICCSN). 2016-06. DOI: 10.1109/iccsn.2016.7586649
38. b37: Tijmen Tieleman, Geoffrey Hinton. "Geoffrey E. Hinton". Talking Nets. 2012. DOI: 10.7551/mitpress/6626.003.0017
39. b38: Gao Wang, Gaoli Wang. "Improved Differential-ML Distinguisher: Machine Learning Based Generic Extension for Differential Analysis". Lecture Notes in Computer Science. 2021. DOI: 10.1007/978-3-030-88052-1_2
40. b39: Ya Xiao, Qingying Hao, Danfeng Daphne Yao. "Neural Cryptanalysis: Metrics, Methodology, and Applications in CPS Ciphers". IEEE DSC. 2019
41. b40: Tarun Yadav, Manoj Kumar. "Differential-ML Distinguisher: Machine Learning Based Generic Extension for Differential Cryptanalysis". Lecture Notes in Computer Science. 2021. DOI: 10.1007/978-3-030-88238-9_10
