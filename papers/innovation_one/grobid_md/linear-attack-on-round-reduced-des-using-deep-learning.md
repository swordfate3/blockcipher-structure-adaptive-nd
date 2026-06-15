# Linear Attack on Round-Reduced DES Using Deep Learning

**Authors:** Botao Hou, Yongqiang Li, Haoyue Zhao, Bin Wu

**Source PDF:** `2020_hou_linear_attack_des_deep_learning.pdf`

## Abstract

Linear attack is a powerful known-plaintext cryptanalysis method on block ciphers, which has been successfully applied in DES, KATAN, SPECK and other ciphers. In this paper, we use deep learning networks to achieve linear attack on DES with plain-cipher pairs. Comparing with traditional linear attack algorithm, our work requires less knowledge about complex cryptanalysis as neural network can work well by data-driven. Thus, this paper has three main contributions. First, a new linear attack architecture based on deep residual network was proposed to train discriminative neural networks with auto-generated plaincipher pair data. The results indicate that trained neural networks can effectively learn algorithmic representations of the XOR distributions of given linear expression on DES. Second, several novel neural networkbased algorithms were designed to efficiently enforce key recovery on round-reduced DES using trained networks with moderate full and partial bits of linear expression as inputs. Third, as far as we know, it is the first time that neural networks are used to achieve known-plaintext attack on complex block ciphers.

## Introduction

Linear cryptanalysis is one of the most powerful analysis techniques used in modern block ciphers. It can achieve key recovery attacks utilizing non-zero correlation with bits of plain-cipher text and key, which is expressed in a linear approximate equation. The first linear cryptanalysis [2] was presented to break Data Encryption Standard (DES) successfully in 1994. Since DES [1] was published in 1977, its security has been focused by all over the world. In that paper, Matsui provided some linear equations on round-reduced DES and proposed a key recovery algorithm for known-plaintext attack in 8-round and even only-plaintext attack in 8 rounds. And Matsui [3] proposed an improved version for linear cryptanalysis and its application to the full 16-round DES. Later, Hermelin et al. [4] improved linear cryptanalysis into multiple approximations and achieved a faster attack. Obviously, all of those traditional linear cryptanalysis works need amounts of mathematical knowledge and manual theory deduction.

Recently, some works have been explored to combine deep learning and applicable statistical cryptanalytic techniques [10, 12] . At first, Abadi and Andersen [5] trained two neural networks which allow them to communicate using given key without advanced cipher design, and another adversarial network was trained to prove that it cannot recover information without the key. However, their work did not explain what net construction is in cryptography. Soon, Coutinho et al. [11] improved simple adversarial network above with chosen-plaintext attack and obtained a unbreakable One-Time Pad algorithm in unsupervised condition which explored the effect of adversarial network in security. And then, some works tried to achieve cracking directly by simulating ciphers [13] . An unsupervised CycleGAN neural network [8] , named CipherGAN, was used to crack Shift and Vigenere ciphers. Their work showed that neural network can learn detail relationship about encrypt and decrypt processes, but it was limited to fixed key. Comparing with traditional encrypt algorithms, modern block cryptographical algorithms are more complex so that previous methods can't work well, and some works began to apply some mature cryptanalysis methods to improve availability of attacking using machine learning [14] . Recently, some works [9] explored the possibility of applying machine learning on side channel attack of Advance Encryption Standard (AES), but generally side channel is considered not to be cryptanalysis in the sense we discussed. And Gohr [6] tried to apply deep learning on Speck, a lightweight block encryption algorithm. They constructed a network to more accurately learn the distribution of output difference with a fixed input difference. However, they didn't give attacks on more complex ciphers.


## Our Contribution

First of all, we devise and train neural networks and expect that we can achieve efficient key recovery on DES using trained network models. Those network models should obtain the ability of distinguishing different distributions by observing given linear expression on round-reduced DES. Considering two different key recovery methods, one bit key recovery and multiple bits key recovery, we train corresponding network models in different ways.

For one bit key recovery on round-reduced DES, we propose a new neural network attack framework that can successfully distinguish two different binomial distributions. Those distributions perform two different situations of n-round linear approximation expression. Using the trained network models, we established corresponding one bit key recovery algorithm and achieved successful key recovering on 3, 4 and 5 rounds DES. In order to know the availability of our models, we calculate the expected efficiency for round-reduced DES that use Bayesian model. Experimental results indicate that the performance of our models is very closed to theoretical value.

In multiple bits key recovery, another neural network model is proposed to train as a discriminator for distributions produced by real and random effective key bits. And this model is used in proposed multiple bits key recovery algorithm. We tested the performance of this algorithm on 4 rounds DES and obtained effective key rank.


## Paper Organization

The rest of the paper is organized as follows. In Sect. 2, we present a brief description of the cryptographic modules employed in our linear cryptanalysis. In Sect. 3, we introduce our detail scheme of neural networks. The result of neural discriminators and corresponding key recovery attacks are in Sect. 4. Section 5 is the conclusion about our scheme in short.


## Preliminaries

Before introducing our architecture, we briefly review some cryptographic building modules deployed in linear cryptanalysis method on DES and two classical key recovery attack algorithms.


## DES

DES is a iterative cryptographic algorithm with Feistel structure, which has a profound impact on the design of later ciphers. DES uses 56 bits key to protect message with block divided into 64 bits. Omitting the initial permutation IP and the final permutation IP -1 in full DES, we call input and output of round iterations as plain text block P and cipher text block C. Each block will be divided into two 32 bits blocks (L, R), which will be encrypted by total 16 rounds. More details can be seen in [1] .

For rth round, the output L r and R r are computed as follows.

Where F(.) is the non-linear function called F function, it contains four operations which include extension operation E of R r , bitwise XOR operation between subkey and extended R r , S-box operation S and final permutation operation. F function is briefly expressed as:


## Linear Attack


## Linear Approximate Equation.

Linear attack has been widely used to break block cipher algorithms. Indeed, given plain text P , master key K and corresponding cipher text C, linear approximate equation L try to describe the linear relationship of bits in serval fixed locations like:

) Algorithm 1. ONE BIT KEY RECOVERY ALGORITHM Input: Ln, n-round linear approximate equation P rL n , the probability of Ln P air, plain-cipher text pairs generated by key K Output: output result 1: Npc ← the number of P air 2: NL ← 0 3: for pair in P air do 4: L l ← compare the left side of Ln 5: if L l == 0 then 6: NL+ = 1 7: if NL > Npc/2 then 8: if P rL > 1/2 then 9: return L r = 0 10: else 11: return L r = 1 12: else 13: if P rL > 1/2 then 14: return L r = 1 15: else 16: return L r = 0

Where α, β and γ are the bit location masks and α • P is the bitwise addition for bits in locations marked by α in P . There we name the value of left side in L as L l and the right side as L r . Generally, equation L holds with the probability P r L of 1/2. But if there is an obvious deviation with 1/2 and P r L , we call this expression L as a well linear approximate equation. The bigger this deviation is, the quicker this expression could be distinguished from other expressions. Moreover, key recovery mentioned in follows is relative with P r L closely.


## Key Recovery Attack.

There are two different linear attack algorithms divided by number of key bits can be recovered. First one is one bit key recovery attack, relying on a well linear expression. Multiple bits key recovery is another, it generally depend on the linear equation which expended by (n-1)-round expression. Both of those attacks can work well in DES, and many effective linear expressions can be found [2] .

One Bit Key Recovery. Given linear approximate equation L like Function 3, we can judge whether L r is 0 or 1 with probability P r L . If we have N pc plaincipher text pairs generated by fixed key, we count the number N L of those pairs that satisfy L l = 0. If N L has obvious difference with N pc /2, we can judge this one bit key L r depending on the symbol of difference with high success rate. The detailed recovery process is showed in Algorithm 1.


## Algorithm 2. MULTIPLE BITS CANDIDATE KEY RANK ALGORITHM

Input: Ln, n-round linear approximate equation P air, Plain-cipher text pairs generated by key K Output: output Rank key 1: Nt ← the number of effective text bits in left Ln 2: Tt ← {0} 2 N t 3: for pair in P air do 4:

e ← bits extracted from pair following Ln 5:

Tt[e]+ = 1 6: N k ← the number of effective key bits in left Ln 7:

for t in len(Tt) do 10:

L l ← compare the left side of Ln 11:

if L l == 0 then 12:

T k [k]+ = t 13: Npc ← the number of P air 14: for k in len(T k ) do 15:

T k [k] = T k [k] -Npc 16: Rank key ← sort T k by descending value order 17: return Rank key Multiple Bits Key Recovery. Generally, if we attack n rounds DES, we have to obtain a (n-1)-round linear approximate equation L n-i with P r L . Considering the effect of F function in first round and nth round, n-round expression L n is described as:

Since L n is expanded from L n-i , P r Ln should be almost same with P r Ln-i , which makes us knowing the distribution of L l n . Obviously, this value is totally determined by some bits of plain-cipher text and key, and we call those bits as effective text bits and effective key bits respectively. Based on known P r L , we can recover those effective key bits as follows.

First, we list all possible effective key bits as key candidates. Considering that the probability P r Ln would almost equal to P r Ln-i when K 1 and K n are correctly guessed, this leads us to use maximum likelihood method in regard to those key candidates.

There we get N pc plain-cipher text pairs generated with fixed key K. For each key candidate, compute L l n and add counter with 1 when it equals to 0. Sort all key candidates by the difference between counter and N pc /2 as key rank. Generally, correct key bits will be in higher rank. The candidate key rank processing is showed in Algorithm 2.


## Network Architectures

Our goal is to develop a learnable, end-to-end model for linear attack, and it should obtain statistical cryptanalytic characteristics. Thus, we proposed a new neural network architecture as a deep learning discriminator to distinguish different distributions. The diagram for our network is shown in Fig. 1 . Those networks comprise three main components: input layer, iteration layer and predict layer. The iteration layer is built by classical residual neural network [7] . This network has been successfully applied in many domains. It consists of some residual blocks which add input layer to output layer and produce new output, the output will been sent to next block. The most important advantage of residual networks is that it can effectively avoid gradient dispersion when the number of layer increases.

The input layer receives training data with fixed length and applies reshape layer into the data. We expect that our network should simulate XOR operation better and form some intermediate representation. For this reason, we transpose and apply convolution into input data so that we can expend the effect of each bit. After batch normalization layer, data will be sent into iteration layer. Each iteration layer has same structure with a convolution and normalization following. What' more, a skip connection is applied to add input layer and output layer and this operation may allow next layer can mix bits in block more like bitwise addition. Iteration layer will repeat 5 or 10 rounds in our experiments, and then the predict layer will be following. The predict layer provides a fully connect operation in order to combines all bits and a single linear layer to produce one bit predicted result.

In our key recovery experiments, this neural network will be fed with bit sequences and is expected to distinguish those input into two different distributions. For each sequence, it consists of 6 units and each unit will be padded with return right of Ln = 0 0 to fixed length, which is determined by max length of each mark in L n . Generally, this length is not longer than 8 and we will pad the sequence to 6 × 8 = 48. Input layer changes the size of this sequence into 8 × 48, and it will be trained in this size till predict layer. Pooling operation condenses it into 48 × 1 and output it with 1 bit by dense layer.

In each epoch, we will check networks by validation data, and we save and update the best model according to its accuracy.


## Attack Architecture

In this section, we will introduce two new linear attack architectures: one bit key recovery and multiple bits key recovery. We apply them in round-reduced DES, and both of them can distinguish different distributions well using deep learning net and realize expected key recovery.


## One Bit Key Recovery

Given n-round linear approximation expression L n as Function 3, and we know that it will hold with certain probability P r Ln in previous. There, we don't need to know exact value about P r Ln and more details, and we can also obtain one bit key information γ • K. For this, we propose one bit key recovery algorithm showed in Algorithm 3 to recover mentioned bit using deep learning networks.

Train and Recover. Supposed that P r Ln is the probability linear expression L n holds, if we ask that L r n is fixed to 0, the distribution of L r n will be almost binomial distribution which means 0 will appear with the probability equaling to P r Ln . While the binomial distribution will be inverse if L r n is fixed to 1. Thus, we mark those different distributions with corresponding labels and expect trained networks can effectively distinguish them by inputting some bit sequences.

In order to obtain those network models, we generate training and validation by several phases as follows:

1. Generate plain texts P and master keys K ordering uniformly distribution. 2. Encrypt P with K by n-round DES cipher and obtain cipher texts C. 3. Extract P -C pairs into bits sequence EX pc and K into EX k depending on linear equation L n . 4. Pad EX pc with 0 into X following the order of (α • P ||β • C). 5. Set label Y relying on XOR value distribution of each EX k .

After generating enough data, neural network discriminator Net Ln will be trained to predict right label Y . Obviously, if Net Ln is train well, its correct output will help us directly to recover corresponding one bit key information. Thus, we apply trained network into Algorithm 3 to recover this key bit.

Recovery phase need N pc plain-cipher pairs generated by fixed key K. Repetitively run Phase 3-4 above and we can obtain extracted text sequences of those pairs. Those text sequences are feed into Net Ln and output their prediction. Considering with the accuracy of Net Ln , the success rate of Algorithm 3 rely on N pc and performance of algorithm will be shown in following experiments.

Goal Model. After training mentioned above, we indeed obtain a deep learning discriminator. This discriminator would first learn the simulation of XOR operation, and then obtain the ability that distinguish the difference with different binomial distribution performance.

Our deep learning model didn't know any information about those distributions and even didn't know XOR operation before training, all they obtaining is input seems like random bit sequences. Obviously, if we can obtain those distribution information about linear expression L, we can estimate the best result of those networks using Bayesian rule.

As P r L is the possibility of linear approximation expression L holding and discriminator B L with Bayesian model obtains distribution features of L l fully, if L l of a bit sequence is 1, the accuracy of B L correctly judging that this sequence belongs into L r = 1 is shown following Function 5.

) Supposing that K is generated following uniform distribution, accuracy of B L will be equal to P r L .

This Bayesian model will be our goal model of deep learning network. We replace network discriminator Net L with this Bayesian discriminator B L in Algorithm 3 and can get one bit key recovery. After reducing, we find that the relationship between success rate of one bit key recovery and number of plain-cipher pairs required is same with Lemma 2 in [2] . Thus, we can measure key recovery effect which uses deep learning networks with this lemma.

Experiment. All of our experiments are run in a uniform environment, models are trained on a workstation with NVIDIA GeForce GTX 1080Ti and Intel(R) E5-2609 1.7 GHz CPU. P H [7, 18, 24, 29]⊕P L [15] ⊕ C H [7, 18, 24, 29] ⊕ C L [15] = K 1 [22] ⊕ K 3 [22] (6) P H [7, 18, 24, 29]⊕P L [15] ⊕ C H [15] ⊕ C L [7, 18, 24, 27, 28, 29, 30, 31] = K 1 [22] ⊕ K 3 [22] ⊕ K 4 [42, 43, 45, 46] (7) P H [15] ⊕ P L [7, 18, 24, 27, 28, 29, 30, 31] ⊕ C H [15] ⊕ C L [7, 18, 24, 27, 28, 29, 30, 31] = K 1 [42, 43, 45, 46] ⊕ K 2 [22] ⊕ K 4 [22] ⊕ K 5 [42, 43, 45, 46] (

First, we tested the performance of one bit key recovery algorithm on L 3 which can be seen in Function 6. Model was trained for 200 epochs using the Adam optimizer [15] with a batch size of 1000 against MSE loss with L2-regularization. And there were 10 5 train data and 10 4 validation data used. Figure 2a shows the learn history of Net L3 . The accuracy on validation data is 67.23% which is very closed to theoretical goal model which is 70%, same with P r L3 .

To be clear, our neural network knows nothing about XOR operation and detailed data distribution, but it can still perform well almost like goal model which knows all about knowledge. All of those show that the presented approach equips excellent learning capability of describing XOR distributions. What's more, we found that the increase of train data can significant improve the accuracy, and the network with 10 5 data is improved with 0.43% than 10 4 data.

Apply those models to recover key information and we found that the success rate of neural network models is only lower than theoretical Bayesian model slightly. The number of plain-cipher text pairs required in key recovery in different success rate based on those discriminators are shown in Fig. 2b . For each result, we run key recovery process for 2000 times to obtain moderate observations. We can see that our neural network can complete key recovery given small plain-cipher text set, and Net L3 trained by 10 5 training data even performs better than theoretical success rate. Thus, those network model showed their capacity to distinguish different distributions. (a) (b) Excepted 3-round one bit key recovery, we also ran 4 and 5-round key recovery based on linear expression in Function 7 and Function 8. Comparing with L 3 , the binomial distribution probability like P r L5 even decreases from 70% into 51.9% [2] . Obviously, the difficulty of distinguishing those two different distributions increases a lot. Table 1 shows the accuracy and key recovery of best models. There, B n is the discriminator of goal model using Bayes mentioned above. And we can find that almost all of them can recover required one bit key with limited plain-cipher text pairs number. For neural discriminators Net L5 , though it does not achieve success rate more than 95% with less than 20000 pairs plain-cipher text, it still performs its ability recovering key bit with success rate of even 90%.


## Algorithm 4 . MULTIPLE BITS DEEP LEARNING NETWORK CANDI-DATE KEY RANK ALGORITHM

Input: L n , n-round linear approximate equation Net L n , neural net discriminator trained by L n P air, Plain-cipher text pairs generated by key K Output: output Rank key 1: N k ← the number of effective subkey bits in left L n 2: T k ← {0} 2 N k 3: for key in len(T k ) do 4:

Ex ← bit sequences extracted from (P air, key) following L n 5:


## Multiple Bits Key Recovery

Like Function 4, we can apply (n-1)-round linear approximation expression L n-1 to consecutive F-functions from the first round to the (n-1)th round or from the second round to the nth round of n rounds DES, and obtain n-round linear equation L n with some bits in F-functions. Because K n is added in expression, we can try all possible effective bits in K n and test whether the value of left L n satisfies the similar distribution like L n-i , so that recover those effective bits. Thus, we propose new multiple bits key candidate recovery algorithm showed in Algorithm 4 to recover multiple bits using deep learning networks.

Train and Recover. Similar with one bit key recovery algorithm, we also utilize the ability of deep learning networks that can distinguish different distributions. Of course, we have to consider the interference produced by right side of Function 4. In order to simplify our models, we suppose that the value of γ • K is 0 which may be happened with the probability of 1/2. Then for once right guess of key, the distribution of L l n will still be almost binomial distribution which 0 will appear in the probability equal to P r L n , and we call it real distribution. While the distribution for one wrong guess of key will be uniform, and we name it random distribution. Those difference is what our networks should distinguish. If given bit sequences generated by correct fixed key, neural network discriminator Net L n should output label of real distribution as 1 with a big probability, otherwise, it should be random distribution as 0.

Also, we give the generation phases of training and validation data.

1. Generate plain texts P and label Y ordering uniformly distribution, and Num P is the number of those P . 2. Generate master key K ordering uniformly distribution, and filtrate out Num P K that satisfy γ • K = 0.

3. Encrypted P with K by n-round DES cipher and obtain cipher text C. 4. Extract P -C pairs into bits sequence EX pc and K into EX k with linear equation L n . 5. For each label Y , do.

-if Y = 1, Pad EX pc with 0 into X following the order of (α

with 0 into X following the order of (α • P ||β • C||Rand||Rand), which Rand is generated ordering uniformly distribution.

As we know, F 1 (P L , K 1 ) and F n (C L , K n ) are determined by effective text bits and effective key bits. Because the number of effective key bits are few enough, we can research those bit keys exhaustively and call those keys as key candidate. For each possible key candidate, we test this key candidate with some plaincipher text pairs and input corresponding bit sequences extracted following L n into network model Net L n . We count those output as the score which support that this key candidate is the right bits of master key required. Sort those key candidates with corresponding score in descending order and we call those as key rank. A well discriminator should have the ability ranking real right subkey higher.

Once we get a key rank, we can run an exhaustive key search for remaining several bits key. In each trying, we will choose a candidate bit key from key rank by order. Obviously, the higher the rank of right subkey is, the quicker whole key recovery will complete.


## Goal Model.

Also, our neural network discriminator Net L need distinguish two binomial distributions. However, different with distributions in one bit key recovery, these binomial distributions should be with p real = P r L and p ran = 1 2 . Use Function 5 and we can obtain the theory accuracy of B L with Bayesian model.


## Experiment.

We run our network models on the number of 10 5 training data and 10 4 validation data. And we tested the performance of multiple bits key recovery on L 4 showed in Function 9 extended from L 3 . Thus P r L 4 will almost equal to P r L3 if effective key bits in K 4 is right. P H [15] ⊕ P L [7, 18, 24, 29] ⊕ C H [7, 18, 24, 29] ⊕ C L [15]

We trained this neural network about 4-round with 200 epochs and each epoch is run in size of 5000. As no unit in L 4 is more than 4 bits, we set padding as 5. And we contain 6 × 5 bits sequence, where the sixth unit is F 4 and it don't appear in Function 9, we will pad it into {0} 5 . Real and random data determined by random label Y were sent to 5-depth residual network. And those two different distributions were separated with accuracy of 56.77%, while the accuracy of theoretical Bayesian model should be 58.3%.

Analysis the effective text and key bits in Function 9, we can easily ensure that the effective key bits effecting left side of L 4 are {K 1 We set a random master key K which holds γ •K = 1 asked by trained neural network Net L 4 above, and we obtained plain-cipher pairs P air with number of N pc encrypted by K. Then we extract each pair following L 4 and obtain bit sequence (α • P ||β • C). Up to now, we have no information about F 1 in L 4 . For each key candidate K can , we compute μ • F 1 (P L , K can ) and insert μ • F 1 into sequence. Record the prediction Net L 4 and get score of K can .

Count all score of key candidate K can , the rank of those key candidates with score is key rank. Research the rank of correct effective key bits, and we can test the performance of Net L 4 is showed in Table 2 . As key ranks using Net L 4 are no lower than 2 5 = 32 in those small number of plain-cipher pairs, all of those indicate that our neural network models can distinguish different distribution in multiple bits key recovery and are pretty effective for key ranking.


## Conclusion

In this paper, we used deep learning network achieving linear attack in roundreduced DES. We proposed the network structure to distinguish different performance of linear expressions. Our experiments indicated that those deep learning networks have the capacity of learning complex static characteristics like XOR and distinguishing different distributions. In order to make networks perform better, we also designed two linear attack algorithms which apply network in one bit and multiple bits key recovery. These end-to-end architectures need almost few knowledge about distribution of linear expressions and performs well in our experiments. And the representations of our results are also useful for cryptanalysis on other more complex block ciphers.

For further work, we will continue to test the performance using deep learning networks to research linear approximations with limited advanced knowledge.

What's more, we found a problem effecting performance of net when we trained our network. Limited by number N t of plain-cipher text bits, there are only 2 Nt text sequences in train text. However, training data is usually larger than this value and make some same input may have different label, and this may make network puzzled. The same situation also happened in [8] , and we will explore those further more.

> 1 Fig. 1 . Fig. 1. Model overview. An universal neural network architecture used in our experiments

> 3 Algorithm 3 . ONE BIT DEEP LEARNING NETWORK KEY RECOVERY ALGORITHM Input: Ln, n-round linear approximate equation NetL n , neural net discriminator trained by Ln P air, Plain-cipher text pairs generated by fixed key K Output: output 1: Npc ← the number of P air 2: G ← NetL n (P air) 3: if sum(G) > Npc/2 then 4: return right of Ln = 1 5: else 6:

> 2 Fig. 2 . Fig. 2. (a) shows accuracy and loss of Net3 in total train process data size of 10 5 respectively. Both valuation data and training data perform synchronously and indicate that network work well without over fitting. (b) shows key recovery performance of Bayesian model and our models. All of them will almost recover key information with success rate more than 99% when increase the number of plain-cipher pairs into 64. With same pair number, the success rate of neural network models only lower than theory Bayesian model slightly. And increasing the number of train data, neural networks will work better.

> [42], K 1 [43], K 1 [44], K 1 [45], K 1 [46], K 1 [47]}, all of them are related to S-box S 1 . Those 6 bits subkey are what we aim to recover. We list all possibility of 6 bits may take and get key candidate table with size of 2 6 = 64.

> 1 Table 1 . results of different models on corresponding linear expression Ln. Meanwhile, we show the average number of plain-cipher text pairs that can achieve key recovery success rate, each of them are test in 2000 times

> 2 Table 2 . Multiple bits key recovery on 4-round DES. We list the average key rank on different number of plain-cipher pairs. They are measured through 200 rounds in replicated test.Network Train data depth Accuracy Average key rank in number of P-C pairs 32 64 128 256

## Acknowledgements

The authors appreciate the anonymous reviewers valuable comments, which improved the paper greatly. This work was supported by National Nature Science Foundation of China under Grants No. 61941116 , No. 61772517 and No. U1936119 , and National Key R&D Program of China under Grant No. 2019QY (Y) 0602 .

## References

1. b0: "Federal Information Processing Standards Publication: dictionary for information processing". Federal Information Processing Standards. 1977. DOI: 10.6028/nbs.fips.11-1-sep30/1977
2. b1: M Matsui. "Linear cryptanalysis method for DES cipher". EUROCRYPT 1993. 1994. DOI: 10.1007/3-540-48285-733
3. b2: M Matsui. "The first experimental cryptanalysis of the data encryption standard". CRYPTO 1994. 1994. DOI: 10.1007/3-540-48658-51
4. b3: M Hermelin, K Nyberg. "Linear cryptanalysis using multiple linear approximations". IACR Cryptology ePrint Archive. 2011
5. b4: M Abadi, D G Andersen. "Learning to protect communications with adversarial neural cryptography". arXiv Cryptography and Security. 2017
6. b5: A Gohr. "Improving attacks on round-reduced Speck32/64 using deep learning". CRYPTO 2019. LNCS. 2019. DOI: 10.1007/978-3-030-26951-76
7. b6: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun. "Deep Residual Learning for Image Recognition". 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2016-06. DOI: 10.1109/cvpr.2016.90
8. b7: A N Gomez. Unsupervised cipher cracking using discrete GANs. 2018
9. b8: Aron Gohr, Friederike Laus, Werner Schindler. "Breaking Masked Implementations of the Clyde-Cipher by Means of Side-Channel Analysis". IACR Transactions on Cryptographic Hardware and Embedded Systems. 2019. DOI: 10.46586/tches.v2022.i4.397-437
10. b9: Vasyl Lytvyn, Ivan Peleshchak, Roman Peleshchak, Victoria Vysotska. "Information Encryption Based on the Synthesis of a Neural Network and AES Algorithm". 2019 3rd International Conference on Advanced Information and Communications Technologies (AICT). 2019-07. DOI: 10.1109/aiact.2019.8847896
11. b10: Murilo Coutinho, Robson De Oliveira Albuquerque, Fábio Borges, Luis García Villalba, Tai-Hoon Kim. "Learning Perfectly Secure Cryptography to Protect Communications with Adversarial Neural Cryptography". Sensors. 2018-04-24. DOI: 10.3390/s18051306
12. b11: Mario Preishuber, Thomas Hutter, Stefan Katzenbeisser, Andreas Uhl. "Depreciating Motivation and Empirical Security Analysis of Chaos-Based Image and Video Encryption". IEEE Transactions on Information Forensics and Security. 2018-09. DOI: 10.1109/tifs.2018.2812080
13. b12: S Greydanus. "Learning the enigma with recurrent neural networks". arXiv Neural and Evolutionary Computing. 2017
14. b13: K G Paterson, B Poettering, J C N Schuldt. "Big bias hunting in amazonia: large-scale computation and exploitation of rc4 biases (invited paper)". ASIACRYPT 2014. 2014. DOI: 10.1007/978-3-662-45611-821
15. b14: D P Kingma, J Ba. "Adam: a method for stochastic optimization". International Conference on Learning Representations. 2015
