# Performance comparison between deep learning-based and conventional cryptographic distinguishers

**Authors:** Emanuele Bellini, Matteo Rossi

**Source PDF:** `2020_performance_comparison_deep_learning_conventional_distinguishers.pdf`

## Abstract

While many similarities between Machine Learning and cryptanalysis tasks exists, so far no major result in cryptanalysis has been reached with the aid of Machine Learning techniques. One exception is the recent work of Gohr, presented at Crypto 2019, where for the first time, conventional cryptanalysis was combined with the use of neural networks to build a more efficient distinguisher and, consequently, a key recovery attack on Speck32/64. On the same line, in this work we propose two Deep Learning (DL) based distinguishers against the Tiny Encryption Algorithm (TEA) and its evolution RAIDEN. Both ciphers have twice block and key size compared to Speck32/64. We show how these two distinguishers outperform a conventional statistical distinguisher, with no prior information on the cipher, and a differential distinguisher based on the differential trails presented by Biryukov and Velichkov at FSE 2014. We also present some variations of the DL-based distinguishers, discuss some of their extra features, and propose some directions for future research.

## Introduction

During an invited talk at Asiacrypt 1991 [41] , Rivest stated that, since the blossoming of computer science and due to the similarity of their notions and concerns, machine learning (ML) and cryptanalysis can be viewed as sister fields. However, in spite of this similarity, it is hard to find in the literature of the most successful cryptanalytical results the use of ML techniques. Several attempts have been made by researchers, using all range of tools that ML can offer, from genetic algorithms, to optimization techniques, neural networks, etc., both in the supervised and unsupervised setting, with the goal of improving or presenting new techniques for black box distinguishers, differential trail searches, or even plaintext or key recovery. So far, all positive results were only able to break particular instances of historical ciphers, simplified versions of modern ciphers, or ciphers for which a conventional attack already existed.

For the first time in 2019, standard differential cryptanalysis techniques and deep residual neural networks were successfully combined by Gohr [14] , to significantly improve an existing attack breaking a reduced version of the NSA cipher Speck32/64. While the reduction of the attack complexity obtained by Gohr was significant, and the adopted techniques not specific to Speck32/64, one might still wonder if the success of Gohr's experiment is due to the very small block and key size of the cipher. Indeed, Speck32/64 has a block size of 32 bits, and a key size of 64, which means the cipher can also be attacked by brute force.

Following the line of Gohr, in this work, we investigate how conventional distinguishers compare to deep learning based distinguisher, on a cipher with a similar (Feistel) structure to Speck32/64, but with twice its block and key size. For our experiments, we selected the Tiny Encryption Algorithm (TEA), and its variation RAIDEN.

The goal of this work, rather than improving existing results, is to compare conventional distinguishers with neural network based distinguishers, and to show weaknesses and strengths of one or the other.

The Tiny Encryption Algorithm (TEA) [49] is a block cipher with an extremely simple design, based only on the modular addition, bitwise exclusive or and shift operations. The cipher was designed by Wheeler and Needham of the Cambridge Computer Laboratory, and first presented during FSE 1994. Weaknesses of TEA are known, such as the existence of equivalent keys, reducing its security to 126 bits, and making the cipher not suited to be used as cryptographic hash function (use that led to the hack of Microsoft's Xbox game console [47] ). The full TEA is also susceptible to a related-key attack [20] . Because of these weaknesses, variations of TEA where presented as XTEA [32] and RAIDEN [40] . The latter was designed by means of genetic programming to be as quick as TEA and to be used in the same real world applications, but with stronger security properties.


## Our contribution

In this work, we compare conventional distinguishers with deep learning based distinguishers. We propose two different (but similar) network architectures to be used as distinguishers against round-reduced versions of the TEA and RAIDEN ciphers. In particular, one network is based on the multi-layer perceptron structure, while the other on a convolutional structure. Contrary to what Baksi et al. [7] stated, we show that Convolutional Neural Networks are suitable for the purpose of finding a distinguisher. We test the performances of all our deep learning based distinguishers, in terms of accuracy, against the conventional ones, then we propose a distinguishing task where conventional distinguisher cannot be applied. Finally, we analyze the limitations of our approach and we propose some directions for further research in the field. 3


## Outline of the paper

In section 2, we briefly overview the main results of ML applications to cryptanalysis. In section 3, devoted to the preliminaries, we describe the ciphers used in this work, we define cryptographic distinguishers and their properties, and we introduce the neural networks utilized during our analysis. In section 4, we describe two conventional distinguishers, one that can be used without any prior information on the cipher, and another that requires a preliminary cryptanalysis of the cipher. In section 5, we describe our neural network based distinguishers. Section 6 is devoted to the comparison and the experimental results, and finally, in section 7, we draw the conclusions.


## Related works


## Use of machine learning in cryptanalysis

We now give a brief (not exhaustive) overview of the literature concerning applications of machine learning techniques to cryptanalysis.

We already mentioned the brief invited talk by Rivest during Asiacrypt 1991 [41] on the relationship between cryptography and machine learning, where he discussed how each field has contributed ideas and techniques to the other. In 2017, a short survey on automated design and cryptanalysis of cipher systems was given [6] , showing that computational intelligence methods, such as genetic algorithms, genetic programming, Tabu search, and memetic computing, are effective tools to solve many cryptographic problems. In his master thesis [24] (2018), Lagerhjelm presents six experiments using long short-term memory networks to try to decipher encrypted text (with DES algorithm) and convolutional neural networks to perform classification tasks on encrypted MNIST images. Both tasks are unsuccessful, except when classifying images encrypted under DES-ECB mode.

ML has been applied with fair success to aid profiled side-channel analysis (e.g. [27, 38, 39] ). This is a technique in which the attacker has access to a clone device, which can be profiled for any chosen key. Afterwards, he can use that knowledge to extract a secret from a different device. Profiled attacks are conducted in two distinctive phases, where the first phase is known as the profiling (or sometimes learning/training) phase, while the second phase is known as the attack (test) phase. This very well resembles the same general profiled approach that is actually used in supervised machine learning. In 2019 the first non-profiled side-channel attack using neural networks with sensitivity analysis was presented [48] . The literature on this subject is somehow extended, and out of scope with respect to our work, where we only consider cryptanalysis methods which do not benefit from side channel information.

In 2007 [25] , the problem of finding some missing bits of the key that is used in a 4 and 6 rounds DES instance is tackled, with the optimization techniques of Particle Swarm Optimization (PSO) and Differential Evolution (DE). Experimental results for 4-round DES showed that the optimization methods considered located the solution efficiently, as they required a smaller number of function evaluations compared to the brute force approach. For 6 rounds DES the effectiveness of the proposed algorithms depends on the construction of the objective function. In the same work, also the factorization and discrete logarithm problem have been modeled as an optimization problem or by means of Artificial Neural Networks, but the experiments where run on 3 decimal digit numbers only.

A direct application of ML to distinguishing the output produced by modern ciphers was explored in [10] . The ML distinguisher had no prior information on the cipher structure, and the authors conclude that their technique was not successful in the task of extracting useful information from the ciphertexts when CBC mode was used and not even distinguish them from random data. Better results were obtained in ECB mode, as one may easily expect, due to the nonrandomization property of the mode. A similar experiment was also reproduced, with similar results, in [29] and in [24] , both in 2018.

Better success has been recently obtained with historical ciphers or to simplified version of modern ciphers. For example, in 2018, code-book recovery for short-period Vigenère cipher was obtained with the use of unsupervised learning using neural networks [15] or, in 2017, restricted version of Enigma cipher were simulated using restricted neural networks [16] . In 2014, in [11] , the authors successfully mapped the input/output behaviour of the Simplified Data Encryption Standard (S-DES), with the use of Multi-layer Perceptron (MLP) neural network. They also showed that the effectivness of the MLP network depends on the nonlinearity of the internal s-boxes of S-DES. Previous pioneering works on S-DES or other simplified ciphers are [36] , [46] , [2] , or [3] . A somehow singular case, in 2002, is that of a public-key scheme based on neural networks, who was broken by use of genetic algorithms (and also by other classical algorithms) [22] .

In [37] , the authors perform an extensive data analysis of the RC4 keystreams which allow them to extract the single-byte and double-byte distributions in the early portions of the keystream itself. This is used to then recover plaintext data.

In [17] , the authors use a genetic-algorithm to search for subsets of the input space that produces a high statistically significant deviation of the distribution of a given subset of the output produced by the Tiny Encryption Algorithm (TEA) encryption. They find 4 rounds trails using 2 11 random inputs.

In 2019, the work by Gohr [14] is the first that compares cryptanalysis performed by a deep neural network to solving the same problems with strong, well-understood conventional cryptanalytic tools. It is also the first paper to combine neural networks with strong conventional cryptanalysis techniques and the first paper to demonstrate a neural network based attack on a symmetric cryptographic primitive that improves upon the published state of the art. All this is applied to Speck32/64, a lightweight cipher designed by the NSA, with a 32 bit block input and a 64 bit key. At the time of writing this manuscript, other similar works followed Gohr approach. In particular, Baksi et al. [7] proposed a Deep Learning based distinguisher for up to 8-round reduced version of the Gimli-Hash and Gimli-Cipher using the all-in-one differential approach [4] . Jain et al. [19] analyze 3-6 round reduced PRESENT lightweight block cipher, by presenting a multi-layer perceptron network distinguisher Finally, Yadav and Kumar [51] derive a multi-layer perceptron distinguisher for 9 rounds SIMON and 6 rounds SPECK.


## Preliminaries


## Description of TEA and RAIDEN

In this work we are considering two block ciphers with a similar structure: RAIDEN and TEA. Precisely, they are Feistel networks of r rounds, in which the output of the nonlinear function F is injected into the network through a modular addition, see fig. 1 . Both ciphers input and output are b = 64 bit strings, and are represented as two words of w = 32 bits, to which we refer to as, respectively, (L 0 , R 0 ) and (L r , R r ). The key is k = 128 bits long, and split in four w-bit words, i.e. K = (K 0 , K 1 , K 2 , K 3 ). To perform the encryption and decryption, they only use the following types of operation: modular addition, bitwise exclusive or, and right or left shift. The cipher output is obtained by repeating r rounds as follows

where δ 0 = 0x9e3779b9, δ i = δ 0 • (r + 1)/2 mod 2 w (so that the same constant is used for two consecutive rounds), (k i0 , k i1 ) = (K 0 , K 1 ) for the even rounds, and (k i0 , k i1 ) = (K 2 , K 3 ) for the odd rounds. RAIDEN nonlinear function F RAIDEN is defined as

where k i is updated according to the following key schedule

), so that it is the same every other round.

Differential trails An additive differential difference ∆x is a n-bit string obtained as the modular difference of two other n-bit strings x 1 , x 2 , i.e. ∆x = x 1 x 2 .

Definition 1. Let ∆x, ∆y ∈ {0, 1} n be fixed n-bit strings, representing two additive differences. The Additive Differential Probability (ADP) of a function f (adp f ) is the probability with which ∆x propagates to ∆y through the function f , computed over all n-bit input x:

A differential trail for an iterated cipher is a sequence of triple (∆x i , ∆y i , p i ) representing the input/output i-th round differences and their associated ADP of the round function, where ∆x i+1 = ∆y i . Differential trails are usually found using standard techniques, such as the Matsui algorithm [28] , which require a manual analysis of the nonlinear layer of the cipher combined with a tree-search.

To build our classical and neural network based distinguisher, we use the differential trails found in the work of Biryukov and Velichkov [9] . These trails have been found using standard cryptanalysis techniques, with no aid from machine learning. A differential trail for TEA and RAIDEN are shown, respectively, in table 1 and table 2 of appendix A.

One fundamental difference among TEA and RAIDEN is that, due to the very simple key schedule, TEA cannot be modeled as a Markov ciphers, i.e. its round keys cannot be assumed to be independent. This means, for example, that a trail that has very good probability computed as an average over all keys, may in fact have zero probability for many or even all keys. This does not happen in RAIDEN. For this reason, the differential trail for TEA is only valid for a fixed key, and it cannot be used to mount a distinguishing attack (and, consequently, cannot be used for a key recovery). On the other hand, the probabilities of RAIDEN differential trail are computed as an average over all keys.


## Distinguishers

In what follows, a cryptographic distinguisher (or simply a distinguisher) A Oracle is a probabilistic algorithm, that takes as input an oracle Oracle secretly running either a random permutation Π, or a specific instantiation C k , indexed by the key k, of a family C of ciphers. The output of A Oracle is 1 if it believes that Oracle is executing C k , and 0 if it believes it is executing Π. Internally, the distinguisher might use specific information about C, as this is a public family of functions. In this case we speak about a tailored distinguisher (see e.g. section 4.2), or no information at all (except for the block size), in which case we speak about a generic distinguisher (see e.g. section 4.1).

In cryptography, a distinguisher is often called an adversary. The prp-cpaadvantage [8] , or simply advantage, of the adversary A in distinguishing the family C of permutations from the set of random permutations, using 2 λ resources, is, informally, a measure of how successfully A can distinguish C from the set of random permutation and, formally, is defined as

where E 1 is the event that A outputs 1 when Oracle contains C k , and E 0 is the event that A outputs 1 when Oracle contains Π.

If A is doing a good job at telling what function Oracle is running, it would return 1 more often when Oracle contains an instance of C, than when it contains a random permutation. Different adversaries have different advantages, depending on if the adversary is more "clever" in querying the oracle, or simply asks more questions and thus has more information. A block cipher algorithm is considered secure if no adversary has a non-negligible advantage. In this work, we will compare the performance of different distinguishers.

The concept of adversary advantage in machine learning, is usually referred to as accuracy of the distinguisher. This can be seen as the ability of recognizing true positives and negatives, or, in other words, the average of the probability of returning 1 while the oracle contains C k , and the probability of returning 0 while it contains Π. When this accuracy is close to 1 or to 0 we have a useful distinguisher, while when the accuracy is close to 0.5, we say the distinguisher is not able to distinguish C.

Two examples of bad distinguishers include the case where A always returns 1, or it flips a coin and returns 1 or 0 with equal probability. In this case its advantage/accuracy would be 0.5.

Single key and known key distinguishers In this work, we consider two scenarios. In the first case, called single secret-key scenario, the attacker sees some traffic, which he knows is coming either from a known cipher or a random permutation, and wants to determine from which of the two is coming. In the second case, called single known-key scenario, the attacker knows the cipher and the key, and wants to verify that the cipher with that specific key behaves as a random permutation or not. In other words, the adversary aims to find a structural property for the cipher under the known key, i.e. a property which an ideal cipher (a permutation drawn at random) would not have. The notion of known-key distinguisher was introduced in 2007, by Knudsen and Rijmen [23] , and subsequently vastly studied, e.g in [30, 42] , for AES-like ciphers, in [5, 43, 44] for Feistel-like ciphers, or in [12, 31, 33] for other constructions.


## Neural networks

In this section, we give a brief description of Deep Learning for Data Classification. Deep Learning is a branch of machine learning that uses Deep Neural Networks and which has been applied in many fields such as image classification, speech recognition and machine translation [13, 1, 52] . The goal is to classify some data x ∈ R n based on their labels y(x) ∈ S in some classes, where n is the dimension of the data and S is the set of classes that we are considering. For simplicity, we can consider S = {0, 1, ..., σ -1} as our classes and the so called one-hot encoding C : R n → S as the vector representation of y(x) in R σ , where C(x) is a vector of length σ with all components set to 0 except for the y(x)-th one, that is set to 1.

A Neural Network is a function F : R n → S which for an input x ∈ R n gives in output a score vector y ∈ R σ such that the i-th component of the vector is a positive real number that is proportional to our confidence that the input value x comes from the class i. To measure the performance of our network, we can define an error function, that is a measure on how far from the real data our previsions are. The most common choice for the error function is the Euclidean Distance E(x) = C(x) -F (x) 2 .

To quantify the error of the network to the whole dataset we define the so called loss function, that is simply the average of the error function on the entire set:

where L is the cardinality of the dataset. Together with the loss function we define another metric called the accuracy, that in our case is defined as the proportion of our dataset that is correctly classified, that is, the proportion of the x i 's for which y(x i ) = argmax F (x i ) holds.

The goal of a neural network is ideally to minimize the loss function L on every possible input dataset, and this is done by considering L as a function of some parameters θ called the trainable parameters of the network. The training phase of the neural network can be seen as a numerical optimization problem, where the function L(θ) is minimized using an iterative approach, called the optimizer of the network. The most famous and classical approach is called Gradient Descent where we iteratively update θ in this way:

where α is called the learning rate and it should be seen as the speed of the training procedure: bigger values of α in general will lead to faster trainings, while smaller ones will lead to slower but more precise trainings. Since Deep Neural Networks are usually made up by a lot of layers, doing Gradient Descent in practice is slow and, as the dimension of the dataset grows, can also be pretty unprecise. To avoid these problems a lot of techniques have been introduced that perform the parameters update over a small subset of the initial dataset; then the dataset is shuffled and the process is repeated on different subsets. The dimension of the subsets is called the batch size while the process of going through the entire dataset one time is called an epoch.


## Multilayer Perceptron

The most simple form of a neural network is the so called multilayer perceptron. We can define a perceptron as a function P : R n → R of the form

where a is a non linear function called the activation function of the perceptron, ω 0 is called the bias and ω i for 1 ≤ i ≤ n are the weights. Bias and weights put together form the set of trainable parameters of the perceptron.

A multilayer perceptron is the combination of several perceptrons organized in fully connected layers, in the sense that each perceptron output of a layer is used as an input for every perceptron in the next layer. The first layer is our input, while the last layer is a set of σ perceptrons representing each class of S.

Convolutional Neural Networks A convolutional neural network is a deep neural network composed of two types of layers: convolutional layers and pooling layers. This kind of network has shown a lot of success in the Image Recognition field [26, 35] because of its translation invariance property. Convolutional layers apply convolution operations to the target by sliding a set of filters on it, while pooling layers are non-linear layers that slide a window over the input data and output a local summary such as the maximum or the mean of the current portion of data.


## Classical distinguishers


## A classical generic distinguisher

In this section, we describe a generic (differential) distinguisher A 1 , which we call the bitflip distinguisher, that performs a simple statistical test on a set of outputs provided by the oracle when given a certain set of inputs. More precisely, the bitflip distinguisher A 1 works as follows. It takes as additional input the parameter τ , defining the threshold for the accuracy of the test. A message m is randomly selected and encrypted to c. Then a bit of m is flipped in a random bit position, and a new encryption c is computed. The distinguisher counts how many bits changed from c to c . If the number of bits that changed from c to c is about half the bit size b of c, the distinguisher concludes that the oracle is using a random permutation, otherwise a block cipher. The pseudo-code of the distinguisher is provided in fig. 2 .


## A classical tailored distinguisher

In this section, we describe a tailored distinguisher A 2 , which we call the differential distinguisher, which uses information about the family C of block ciphers. More precisely, the differential distinguisher A 2 works as follows. As an additional input, beside a threshold τ defining the accuracy of the distinguisher, it receives an additive differential triple, including an input difference ∆x ∈ {0, 1} b , an output difference ∆y ∈ {0, 1} b and the probability p that the input/output difference is preserved after applying the cipher to be distinguished. The probability p determines the number of sample messages the distinguisher needs to process. For each sample m the encryption c and c of m and m ∆x is computed, and if the difference between c and c is ∆y, then a counter is increased. If, at the end of the process, at least τ output differences matched ∆y, then the distinguisher concludes that the Oracle is using an instance from the family C of ciphers, otherwise that it is using a random permutation. The pseudo-code of the distinguisher is provided in fig. 2 .


## Neural network based distinguishers

In this section we present a distinguisher A 3 , that we will call neural distinguisher.

As the name suggests this is based on Neural Networks. Here we give a general structure of the distinguisher, then we will go into the details in the following sections. Recall that we defined a Neural Network as a function F that takes an input and tries to classify it in one of the given classes. Here the classes will be only 2: S = {random, cipher}, where the random class is the class in which random inputs will be classified, and the cipher one is the one for the inputs coming from the cipher. Our network is simply a function F : R 2 → S that takes in input a pair of integer numbers and classify it in one of the two classes. In the case of the random class, the input will simply be made up by two uniformly random integers with bit size equal to the block size of the cipher, while for the cipher class the input will be a pair of ciphertext coming from a fixed plaintext difference ∆x unknown to the network.

To build the distinguisher we first train the network using n input-output pairs coming half from the cipher and half from the random distribution (this is done one time, then the network is saved and reused for all the distinguisher calls) for e epochs, then we predict the classes for chunks of n input pairs coming all from the same source (random or cipher) and we go for a majority vote: we fix a threshold τ n and we check if at least τ n out of n samples are classified as coming from the cipher. If this is true, the chunk is classified as a cipher chunk, otherwise, it is classified as random. The general pseudo-code for the training phase and the one for the distinguisher can be seen, respectively, on the left and on the right of fig. 3 .


## Neural


## Time Distributed distinguisher

In this section, we describe the first of our network architectures for the neural distinguisher. We will refer to this as the Time Distributed distinguisher (TD distinguisher).

Input and Output Layers As we said before, our network takes in input a pair of bit size b integers, ideally representing two ciphertext coming from the same key and a known input difference. However we noticed that the network learns better if the inputs are given as bit vectors, so our input layer is made up by 2b neurons with binary values. For the output, we simply one-hot encode the two classes, so we have 2 output neurons that, during training, take the value (1, 0) for random inputs and (0, 1) for cipher inputs. In the classification phase we classify an observation for which the network output is a vector v to the class represented by arg max v.

Hidden Layers The network is structured as a multilayer perceptron. The hidden layers can be ideally splitted in two parts: the first part is what we call a time distributed network, while the second one is a multilayer perceptron in its classic definition. In the first part we split our input in four chunks of 32 bits, each representing one of the four words that make up the two ciphertexts, and we pass each chunk separatedly in 2 dense layers of 32 neurons (in our case, perceptrons) each. The name "time distributed" comes from the fact that this approach is common when dealing with temporal data, however in our case this can be simply seen as treating the chunk separatedly, without letting their values influence each other. The outputs are four vectors in R 32 that are now flattened, in the sense that they are joined to form a unique vector in R 128 that will be the input of the second part. The second part is made up by three fully connected layers of 64, 64 and 32 neurons, ending up in the output layers that is, as we said before, made up by two neurons.

Activations and Loss Function For the hidden layers we chose the Leaky ReLU activation function [50] , that can be defined as

with the value γ = 0.3. This solution has been found mainly with trial and error, but intuitively we expected it to work well since our problem has a strong vanishing gradient issue [18] . For the output layer, since we are using one-hot encoding, it comes natural to use the softmax activation function, defined as a(x) = (a 1 (x), ..., a n (x)) where

For the loss function we opted for the standard mean squared error, since we have not seen significant improvements using more sophisticated functions.


## Optimizer and Learning Rate

We chose the state of the art Adam algorithm as optimizer [21] . Since it slightly differs from the classical gradient descent we presented before, we give a brief explanation here. We define two sequences

where θ (t) represents as before our trainable parameters, L is our loss function and β 1 , β 2 are constants. Then the update rule is

, where is again a constant and α is the learning rate of our network. We fixed the constants to the values suggested by the authors, that are β 1 = 0.9, β 2 = 0.999, = 10 -7 . For the learning rate we followed a similar approach to the one described in [45] : we defined two values α max and α min and we fixed a small number of epochs (we used 3). We defined α max as the maximum value of the learning rate such that we still see some improvements for all the 3 epochs, and α min as the minimum value that gives a significant improvement in the loss at the end of the 3 epochs (ideally, this can be seen as an elbow in the graph of learning rate versus loss). We then set a cyclic learning rate as

where i refers to the current epoch in the training and c is the length of the cycle. Experimentally we found that for our problem α max = 0.015, α min = 0.0003 and c = 5 works well.


## Training and Testing

We ran our network on 10 6 training pairs and 10 4 validation pairs for e = 50 epochs. Based on the validation accuracy we selected the minimum number n of samples needed in each experiment to have a distinguisher with accuracy significantly far from 0.5 (where with significantly we mean that it deviates at least by 0.02 from 0.5) and the threshold τ n (see previous section).

We then evaluated 10 3 sets of dimension k to estimate the accuracy of the distinguisher.


## Convolutional distinguisher

Here we briefly outline a second neural distinguisher that we will include in the accuracy comparison in section 6. Since it is very similar to the TD distinguisher, we only talk about the main difference: hidden layers. We will refer to this distinguisher as the Convolutional distinguisher.

Hidden Layers As before, we can identify two splits of layers: in the first split, instead of perceptrons, we use two one-dimensional convolutional layers of size 32. The approach is very similar to the previous one: the input is split in four parts and passed through the filters. However, the main difference is that these filters can have dimensions greater than 1, allowing the network to learn different features. Then the output of these layers is flattened and passed to the prediction head, that is modeled as before as a multilayer perceptron with 3 layers of 32, 32 and 16 neurons.


## Experimental results and comparisons

In this section, we present the methodology we adopted to compare the performance of different distinguishers. We also present the results of this comparison, focusing in particular on the performance of the NN based distinguishers.


## Description of the experiment

In order to compare the distinguishers, we run the following experiments. We consider different reduced version of TEA and RAIDEN (with rounds ranging from 4 to 8). For each cipher family C, each distinguisher A i Oracle , and a fixed number of samples n, we compute the accuracy of the distinguisher. Precisely, we ran 1000 experiments. For half of the experiments we call the distinguisher A i Oracle with Oracle equal to an instance C k of the cipher family C, (with a fixed key for TEA, and with a randomly chosen key for RAIDEN). For the other half we fix Oracle to a random generator (using NumPy [34] random number generator). Then we measure the accuracy of the distinguisher by counting how many times it distinguishes correctly (i.e. it returns 1 in the first case, and 0 in the second), averaging the two cases.

The number n ranges from 2 0 to 2 20 in the case of TEA, and from 2 0 to 2 12 in the case of RAIDEN. These numbers have been chosen in order to have high success probability with the differential distinguisher up to a number of rounds where the bitflip distinguisher was failing (i.e. having accuracy 0.5). Precisely, the bitflip distinguisher becomes useless at round 7 for both TEA and RAIDEN. At round 7 and 8, TEA has a fixed key output difference of probability, respectively, 2 -20.77 and 2 -29.43 , while RAIDEN has a "true" output difference of probability, respectively, 2 -8 and 2 -10 . foot_1 Thus, for example, as far as it concern the differential distinguisher A 2 Oracle , we expect to have a success probability (accuracy) close to 1 with 2 8 samples at 7 rounds for RAIDEN, and with 2 21 samples at 7 rounds for TEA.

For both the bitflip distinguisher A 1 and the differential distinguisher A 2 we set the threshold value τ = 1. The choice of the threshold for the neural distinguishers was a bit more complicated: in general for n samples we set τ n = n 2 , though this is not always the optimal choice. We found out that sometimes, during the training phase, the network overfits one of the two classes, so it develops the tendency to predict better one class instead of the other. This happens especially with an high number of rounds, and we found out that it can be solved increasing a little bit the threshold. So, we set all the thresholds for the 8-rounds simulations to τ n = δn with 0.5 ≤ δ ≤ 0.7, depending on how it performed in the validation set. We stress that this is not a limitation of the distinguisher, since the value of δ is fixed during the training phase and remains fixed for all the calls to the distinguisher.


## Detailed results

The entire experiment was run in few days of computation with a fairly powerful personal laptop (2.9 GHz Quad-Core Intel Core i7 with 16 GB of RAM) and no excessive parallelization and optimization effort. Though, memory usage was significant during the training of the neural networks when targeting 7 and 8 rounds, and it seems that we need more computational power to increase the number of rounds (see section 6.5).

Both the bitflip and the differential distinguisher behaved as expected. In particular, the bitflip distinguisher started failing on both ciphers at round 7, and, in the case of RAIDEN, it was already showing some weaknesses at round 6, confirming the better diffusion properties compared to TEA.

In the case of TEA 4 rounds, we expect about 2 14 samples to reach accuracy 1 for the differential distinguisher. In practice, with 2 14 samples, we reached an accuracy of 0.92, and accuracy very close to 1 was reached with 2 16 samples. Similar results can be observed for all other rounds, and also for RAIDEN.

Both neural distinguishers performed a little worse than expected in some cases: for example for the 8-round experiment on TEA we obtained a validation accuracy of 0.545 when using the TD network; this would imply that, in theory, 2 8 samples should be enough to reach an accuracy of 1, while in practice we reached 0.982. This phenomena is worse in the Convolutional case, where, with a very similar validation accuracy, we reached a test accuracy of 0.916 with 2 8 samples. However, these results might be biased by the generation of the samples, since the validation set is relatively small and the NumPy random number generator does not yield a perfect uniform distribution, so the accuracy on the validation set can be slightly over or underestimated. In any case, the results (especially in the TD experiment) do not deviate significantly from what we expected.

A visualization of the performance of all distinguishers considered in our experiments, is given in fig. 4 , fig. 5 , fig. 6 . 0 1 2 3 4 5 6 7 8 9 1011121314151617181920 0.5 1 log 2 (#samples) Accuracy TEA 4-rounds Bitflip distinguisher Differential distinguisher TD distinguisher Convolutional distinguisher 0 1 2 3 4 5 6 7 8 9 1011121314151617181920 0.5 1 log 2 (#samples) Accuracy TEA 7-rounds Bitflip distinguisher Differential distinguisher TD distinguisher Convolutional distinguisher Fig. 5: Distinguishers applied to TEA 4 round (left) and 7 rounds (right), 1000 experiments. 0 1 2 3 4 5 6 7 8 9 10 11 12 0.5 1 log2(#samples) Accuracy RAIDEN 5-rounds Bitflip distinguisher Differential distinguisher TD distinguisher Conv. distinguisher 0 1 2 3 4 5 6 7 8 9 10 11 12 0.5 1 log2(#samples) Accuracy RAIDEN 6-rounds Bitflip distinguisher Differential distinguisher TD distinguisher Conv. distinguisher 0 1 2 3 4 5 6 7 8 9 10 11 12 0.5 1 log2(#samples) Accuracy RAIDEN 7-rounds Bitflip distinguisher Differential distinguisher TD distinguisher Conv. distinguisher


## Lowering the training

Although our models being quite small (compared to the common neural network models, especially in image classification), we asked ourselves if the training phase can be lowered without losing too much accuracy. In fig. 7 and fig. 8 we report the results of our two neural distinguishers on TEA with 6, 7 and 8 rounds, ranging the number of training samples from 10 3 to 10 6 . The results are pretty surprising: with 6 rounds 10 3 samples are enough to have a very good distinguisher, so with a negligible time in training (a few seconds) we can easily build this distinguisher. The most interesting case is the 8-rounds one: we can notice that in both network architectures the number of training samples can be lowered, but we can also see for the first time a significant difference between the two networks. In fact, we can see that with 10 4 samples a decent distinguisher can be build with the TD network, but not with the Convolutional one. Vice versa with 10 5 samples the Convolutional distinguisher seems a lot better than the TD one, that shows a lower accuracy. In general, fig. 7 and fig. 8 show that in the majority of the cases computations can be reduced significantly (from near 30 minutes for each model with 10 6 samples on our laptop to less than a minute with 10 4 and a couple of minutes with 10 5 ) with only a small performance loss.

0 1 2 3 4 5 6 7 8 9 10 11 12 0.5 1 log2(#samples) Accuracy TEA 6-rounds -TD distinguisher 10 3 training samples 10 4 training samples 10 5 training samples 10 6 training samples 0 1 2 3 4 5 6 7 8 9 10 11 12 0.5 1 log2(#samples) Accuracy TEA 7-rounds -TD distinguisher 10 3 training samples 10 4 training samples 10 5 training samples 10 6 training samples 0 1 2 3 4 5 6 7 8 9 10 11 12 0.5 1 log2(#samples) Accuracy TEA 8-rounds -TD distinguisher 10 3 training samples 10 4 training samples 10 5 training samples 10 6 training samples


## Further experiments

In this section we propose two more experiments, one on TEA and one on RAIDEN, using the TD distinguisher. All the trainings are done as before with 10 6 samples.

TEA: random key experiment Until now, we focused on distinguishing TEA with a fixed key and a given fixed input difference. We also wanted to test what happens if we only fix the input difference and select random keys, as we do on RAIDEN. Since the differential trail we used before for TEA was generated for a specific key, one can not use the same input difference of the trail for any 0 1 2 3 4 5 6 7 8 9 10 11 12 0.5 1 log2(#samples) Accuracy TEA 6-rounds -Convolutional Distinguisher 10 3 training samples 10 4 training samples 10 5 training samples 10 6 training samples 0 1 2 3 4 5 6 7 8 9 10 11 12 0.5 1 log2(#samples) Accuracy TEA 7-rounds -Convolutional Distinguisher 10 3 training samples 10 4 training samples 10 5 training samples 10 6 training samples 0 1 2 3 4 5 6 7 8 9 10 11 12 0.5 1 log2(#samples) Accuracy TEA 8-rounds -Convolutional Distinguisher 10 3 training samples 10 4 training samples 10 5 training samples 10 6 training samples other key. So, we decided to fix an input difference of low hamming weight and low integer value, i.e. 0x1. We ran the experiment on 6, 7, 8 rounds (see the left panel of fig. 9 of appendix B), observing that for 6 and 7 rounds the distinguisher seems identical to the previous ones, while for 8 rounds the distinguisher shows an accuracy of around 0.6. The results on 6 and 8 are somehow expected, since it is intuitive that this task is in general harder than the previous one (and this explains the lack of performance on 8 rounds), but also with 6 rounds the cipher has not reached the full diffusion yet, so it seems reasonable that the network is exploiting this property. The results on 7-rounds are a bit more unexpected: we think that the network is learning something that is neither only a diffusion property nor only a differential one, but probably a combination of them (with possibly some other properties). We leave a deep analysis of this result for future research.


## RAIDEN: ciphertext difference experiment

In this experiment we modified the network to take only a word of size b as input. The idea is to feed the network with ciphertext differences (rather than the ciphertext pairs generating the differences) generated from RAIDEN with random key and fixed input difference. The main point of this experiment is to verify if the network is actually learning only the differential properties of the cipher or something else. The results are shown in the right panel of fig. 9 . We can notice that the performances are pretty similar to the ones with the two ciphertexts as inputs, so there is no clear evidence of what is happening. However, since there is no significant improvement, we suspect that in the previous case the network was learning also some other properties of the data. As before, we leave further analysis of this experiment for future works.


## Limitations of NN based distinguishers

Even if, at run-time, the NN based distinguishers outperform the two conventional distinguishers considered in this work, one has to keep in mind that the accuracy of such distinguishers depends on the intensity of the training. Our experiments used at most 10 6 samples, with a memory cost of nearly 2.5GB during the training phase, so we expect the limit for a high level laptop to be somewhere near 10 7 samples, and this may not be enough to increase the number of rounds, especially in TEA case.


## Conclusion

In this work we introduced a simple network architecture to perform a distinguishing task on TEA and RAIDEN ciphers. We then showed that NN based distinguishers outperformed classical ones with quite high margin. We also showed that these results can be reached without excessive computational power on round-reduced versions of the ciphers. We leave for future research a more computationally extensive analysis of these results, in particular to see what happens for higher number of rounds, how the neural networks need to be trained, and how much memory they need. It would also be of interest to apply the same techniques to ciphers with 128 bit message block, and 256 bit keys, and to test different neural networks, or variation of the ones we used.

Round difference F TEA in/out differences Accumulated Round L R ∆x ∆y adp F TEA (∆x → ∆y) 0 0xfffffff1 0xffffffff ---1 0x00000000 0xffffffff 0xffffffff 0x0000000f 2 -3.62 2 0x00000000 0xffffffff 0x00000000 0x00000000 2 -3.62 3 0x0000000f 0xffffffff 0xffffffff 0x0000000f 2 -6.49 4 0x0000000f 0xffffffff 0x0000000f 0x00000000 2 -14.39 5 0x00000000 0xffffffff 0xffffffff 0xfffffff1 2 -17.99 6 0x00000000 0xffffffff 0x00000000 0x00000000 2 -17.99 7 0xfffffff1 0xffffffff 0xffffffff 0xfffffff1 2 -20.77 8 0xfffffff1 0x00000001 0xfffffff1 0x00000002 2 -29.43 9 0x00000000 0x00000001 0x00000001 0x0000000f 2 -33.00 10 0x00000000 0x00000001 0x00000000 0x00000000 2 -33.00 11 0xfffffff1 0x00000001 0x00000001 0xfffffff1 2 -35.87 12 0xfffffff1 0xffffffff 0xfffffff1 0xfffffffe 2 -43.77 13 0x00000000 0xffffffff 0xffffffff 0x0000000f 2 -47.36 14 0x00000000 0xffffffff 0x00000000 0x00000000 2 -47.36 15 0x00000011 0xffffffff 0xffffffff 0x00000011 2 -50.15 16 0x00000011 0xffffffff 0x00000011 0x00000000 2 -58.98 17 0x00000000 0xffffffff 0xffffffff 0xffffffef 2 -62.59 18 0x00000000 0xffffffff 0x00000000 0x00000000 2 -62.59

Table 1 . TEA 18-round additive differential trail, for the fixed key (0x11CAD84E, 0x96168E6B, 0x704A8B1C, 0x57BBE5D3).

Round difference F RAIDEN in/out differences Accumulated Round L R ∆x ∆y adp F RAIDEN (∆x → ∆y) 0 0x7fffff00 0x00000000 ---1 0x7fffff00 0x00000000 0x00000000 0x00000000 2 -0.00 2 0x7fffff00 0x7fffff00 0x7fffff00 0x7fffff00 2 -2.00 3 0x00000000 0x7fffff00 0x7fffff00 0x80000100 2 -4.00 4 0x00000000 0x7fffff00 0x00000000 0x00000000 2 -4.00 5 0x7fffff00 0x7fffff00 0x7fffff00 0x7fffff00 2 -6.00 6 0x7fffff00 0x00000000 0x7fffff00 0x80000100 2 -8.00 7 0x7fffff00 0x00000000 0x00000000 0x00000000 2 -8.00 8 0x7fffff00 0x7fffff00 0x7fffff00 0x7fffff00 2 -10.00 9 0x00000000 0x7fffff00 0x7fffff00 0x80000100 2 -12.00 10 0x00000000 0x7fffff00 0x00000000 0x00000000 2 -12.00 • • • 29 0x7fffff00 0x7fffff00 0x7fffff00 0x7fffff00 2 -38.00 30 0x7fffff00 0x00000000 0x7fffff00 0x80000100 2 -40.00 31 0x7fffff00 0x00000000 0x00000000 0x00000000 2 -40.00 32 0x7fffff00 0x7fffff00 0x7fffff00 0x7fffff00 2 -42.00

> 1 FFFig. 1 : Fig. 1: Two rounds of the Feistel structure of TEA and RAIDEN.

> 11612121102 Bitflip distinguisher: A 1 Oracle (τ ) 1 : 6 :7 : else return 1 Differential distinguisher: A 2 1 : h = 0 2 :← h + 1 8 : if h ≥ τ return 1 9 : else return 0 Fig. 2 : Fig. 2: Bitflip (left) and Differential (right) distinguisher.

> 1512311011203 15 : 1 : h = 0 2 : 3 : 1 9 : if h ≥ τn 10 : return 1 11 : else 12 : return 0 Fig. 3 : Fig. 3: Neural Network training (left) and Neural Distinguisher (right).

> 45 Fig. 4 :Fig. 5 : Fig. 4: Distinguisher comparison for TEA (left) and RAIDEN (right), 1000 experiments.

> 6 Fig. 6 : Fig. 6: Distinguishers applied to RAIDEN 5 round (left), 6 rounds (middle), and 7 rounds (right), 1000 experiments.

> 7 Fig. 7 : Fig. 7: Time Distributed distinguishers applied to TEA 6 (left), 7 (center) and 8 (right) rounds, with different size for the training set, 1000 experiments.

> 8 Fig. 8 : Fig. 8: Convolutional distinguishers applied to TEA 6, 7 and 8 rounds, with different size for the training set, 1000 experiments.

> 9 Fig. 9 : Fig.9: Results on TEA with 6, 7, 8 rounds and random key (left), results on RAIDEN 6, 7, 8 rounds letting the network learn only the output difference (right).

> 2 Table 2 . RAIDEN 32-round additive differential trail.

## References

1. b0: Ahmed Ali Mohammed Al-Saffar, Hai Tao, Mohammed Ahmed Talab. "Review of deep convolution neural network in image classification". 2017 International Conference on Radar, Antenna, Microwave, Electronics, and Telecommunications (ICRAMET). 2017-10. DOI: 10.1109/icramet.2017.8253139
2. b1: K M Alallayah, A H Alhamami, W Abdelwahed, M Amin. "Attack of Against Simplified Data Encryption Standard Cipher System Using Neural Networks". Journal of Computer Science. 2012. DOI: 10.3844/jcssp.2010.29.35
3. b2: K M Alallayah, W F El-Wahed, M Amin, A H Alhamami. "Attack of Against Simplified Data Encryption Standard Cipher System Using Neural Networks". Journal of Computer Science. 2010-01-01. DOI: 10.3844/jcssp.2010.29.35
4. b3: Martin R Albrecht, Gregor Leander. "An All-In-One Approach to Differential Cryptanalysis for Small Block Ciphers". Lecture Notes in Computer Science. 2013. DOI: 10.1007/978-3-642-35999-6_1
5. b4: Elena Andreeva, Andrey Bogdanov, Bart Mennink. "Towards Understanding the Known-Key Security of Block Ciphers". Lecture Notes in Computer Science. 2013. DOI: 10.1007/978-3-662-43933-3_18
6. b5: Wasan Shaker Awad, El-Sayed M. El-Alfy. "Computational Intelligence in Cryptology". Artificial Intelligence. 2017. DOI: 10.4018/978-1-5225-1759-7.ch065
7. b6: Anubhab Baksi, Jakub Breier, Yi Chen, Xiaoyang Dong. "Machine Learning Assisted Differential Distinguishers For Lightweight Ciphers". 2021 Design, Automation & Test in Europe Conference & Exhibition (DATE). 2020. DOI: 10.23919/date51398.2021.9474092
8. b7: M Bellare, P Rogaway. "Introduction to modern cryptography". Ucsd Cse. 2005
9. b8: Alex Biryukov, Arnab Roy, Vesselin Velichkov. "Differential Analysis of Block Ciphers SIMON and SPECK". Lecture Notes in Computer Science. 2014. DOI: 10.1007/978-3-662-46706-0_28
10. b9: Jung-Wei Chou, Shou-De Lin, Chen-Mou Cheng. "On the effectiveness of using state-of-the-art machine learning techniques to launch cryptographic distinguishing attacks". Proceedings of the 5th ACM workshop on Security and artificial intelligence. 2012-10-19. DOI: 10.1145/2381896.2381912
11. b10: Moises Danziger, Marco Aurelio Amaral Henriques. "Improved cryptanalysis combining differential and artificial neural network schemes". 2014 International Telecommunications Symposium (ITS). 2014-08. DOI: 10.1109/its.2014.6948008
12. b11: Le Dong, Wenling Wu, Shuang Wu, Jian Zou. "Known-Key Distinguisher on Round-Reduced 3D Block Cipher". Lecture Notes in Computer Science. 2011. DOI: 10.1007/978-3-642-27890-7_5
13. b12: Cristina España-Bonet, José A R Fonollosa. "Automatic Speech Recognition with Deep Neural Networks for Impaired Speech". Lecture Notes in Computer Science. 2016. DOI: 10.1007/978-3-319-49169-1_10
14. b13: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
15. b14: A N Gomez, S Huang, I Zhang, B M Li, M Osama, L Kaiser. Unsupervised cipher cracking using discrete gans. 2018
16. b15: S Greydanus. Learning the enigma with recurrent neural networks. 2017
17. b16: Julio C Hernandez, Pedro Isasi. "Finding Efficient Distinguishers for Cryptographic Mappings, with an Application to the Block Cipher TEA". Computational Intelligence. 2004-07-27. DOI: 10.1111/j.0824-7935.2004.00250.x
18. b17: Sepp Hochreiter. "The Vanishing Gradient Problem During Learning Recurrent Neural Nets and Problem Solutions". International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems. 1998-04. DOI: 10.1142/s0218488598000094
19. b18: A Jain, V Kohli, G Mishra. Deep learning based differential distinguisher for lightweight cipher present. 2020
20. b19: John Kelsey, Bruce Schneier, David Wagner. "Related-key cryptanalysis of 3-WAY, Biham-DES,CAST, DES-X, NewDES, RC2, and TEA". Lecture Notes in Computer Science. 1997. DOI: 10.1007/bfb0028479
21. b20: D Kingma, J Ba. "Adam: A method for stochastic optimization". International Conference on Learning Representations. 2014
22. b21: Alexander Klimov, Anton Mityagin, Adi Shamir. "Analysis of Neural Cryptography". Lecture Notes in Computer Science. 2002. DOI: 10.1007/3-540-36178-2_18
23. b22: Lars R Knudsen, Vincent Rijmen. "Known-Key Distinguishers for Some Block Ciphers". Lecture Notes in Computer Science. 2007. DOI: 10.1007/978-3-540-76900-2_19
24. b23: L Lagerhjelm. Extracting information from encrypted data using deep neural networks. 2018
25. b24: E C Laskari, G C Meletiou, Y C Stamatiou, M N Vrahatis. "Cryptography and Cryptanalysis Through Computational Intelligence". Studies in Computational Intelligence. 2007. DOI: 10.1007/978-3-540-71078-3_1
26. b25: Y Lecun, Y Bengio. Convolutional networks for images, speech, and time-series. The handbook of brain theory and neural networks. 1995
27. b26: Houssem Maghrebi, Thibault Portigliatti, Emmanuel Prouff. "Breaking Cryptographic Implementations Using Deep Learning Techniques". Lecture Notes in Computer Science. 2016. DOI: 10.1007/978-3-319-49445-6_1
28. b27: Mitsuru Matsui. "Linear Cryptanalysis Method for DES Cipher". Lecture Notes in Computer Science. 1993. DOI: 10.1007/3-540-48285-7_33
29. b28: F L De Mello, J A Xexéo. "Identifying encryption algorithms in ECB and CBC modes using computational intelligence". J. UCS. 2018
30. b29: Marine Minier, Null- W Phan, Benjamin Pousse. "Distinguishers for Ciphers and Known Key Attack against Rijndael with Large Blocks". Lecture Notes in Computer Science. 2009. DOI: 10.1007/978-3-642-02384-2_5
31. b30: Jorge Nakaharajr. "New Impossible Differential and Known-Key Distinguishers for the 3D Cipher". Lecture Notes in Computer Science. 2011. DOI: 10.1007/978-3-642-21031-0_16
32. b31: R M Needham, D J Wheeler. TEA extensions. 1997-10
33. b32: Ivica Nikolić, Josef Pieprzyk, Przemysław Sokołowski, Ron Steinfeld. "Known and Chosen Key Differential Distinguishers for Block Ciphers". Lecture Notes in Computer Science. 2010. DOI: 10.1007/978-3-642-24209-0_3
34. b33: T E Oliphant. "Annals of a Publishing House". A guide to NumPy. 2006. DOI: 10.1017/cbo9780511711114
35. b34: K O'shea, R Nash. "https://ikm.org.my/publications/malaysian-journal-of-chemistry/view-abstract.php?abs=J0051-aa0f72a". MALAYSIAN JOURNAL OF CHEMISTRY. 2015. DOI: 10.55373/mjchem.v26i4.88
36. b35: S Pandey, M Mishra. "Neural cryptanalysis of block cipher". International Journal. 2012
37. b36: Kenneth G Paterson, Bertram Poettering, Jacob C N Schuldt. "Big Bias Hunting in Amazonia: Large-Scale Computation and Exploitation of RC4 Biases (Invited Paper)". Lecture Notes in Computer Science. 2014. DOI: 10.1007/978-3-662-45611-8_21
38. b37: Stjepan Picek, Annelie Heuser, Sylvain Guilley. "Template attack versus Bayes classifier". Journal of Cryptographic Engineering. 2017-09-22. DOI: 10.1007/s13389-017-0172-7
39. b38: Stjepan Picek, Ioannis Petros Samiotis, Jaehun Kim, Annelie Heuser, Shivam Bhasin, Axel Legay. "On the Performance of Convolutional Neural Networks for Side-Channel Analysis". Lecture Notes in Computer Science. 2018. DOI: 10.1007/978-3-030-05072-6_10
40. b39: Javier Polimón, Julio C Hernández-Castro, Juan M Estévez-Tapiador, Arturo Ribagorda. "Automated design of a lightweight block cipher with Genetic Programming". International Journal of Knowledge-based and Intelligent Engineering Systems. 2008-03-12. DOI: 10.3233/kes-2008-12102
41. b40: Ronald L Rivest. "Cryptography and machine learning". Lecture Notes in Computer Science. 1991. DOI: 10.1007/3-540-57332-1_36
42. b41: Yu Sasaki. "Known-Key Attacks on Rijndael with Large Blocks and Strengthening ShiftRow Parameter". IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences. 2012. DOI: 10.1587/transfun.e95.a.21
43. b42: Yu Sasaki, Sareh Emami, Deukjo Hong, Ashish Kumar. "Improved Known-Key Distinguishers on Feistel-SP Ciphers and Application to Camellia". Lecture Notes in Computer Science. 2012. DOI: 10.1007/978-3-642-31448-3_7
44. b43: Yu Sasaki, Kan Yasuda. "Known-Key Distinguishers on 11-Round Feistel and Collision Attacks on Its Hashing Modes". Lecture Notes in Computer Science. 2011. DOI: 10.1007/978-3-642-21702-9_23
45. b44: L N Smith. "Puzzle Game". Encyclopedia of Computer Graphics and Games. 2015. DOI: 10.1007/978-3-031-23161-2_300967
46. b45: K Srinivasa Rao, M Rama Krishna, B Bujji. "Cryptanalysis of a feistel type block cipher by feed forward neural network using right sigmoidal signals". Int. J. of Soft Computing. 2009
47. b46: M Steil. "17 mistakes Microsoft made in the Xbox security system". 22nd Chaos Communication Congress. 2005
48. b47: B Timon. "Non-profiled deep learning-based side-channel attacks with sensitivity analysis". IACR Transactions on Cryptographic Hardware and Embedded Systems. 2019-02. DOI: 10.13154/tches.v2019.i2.107-131
49. b48: David J Wheeler, Roger M Needham. "TEA, a tiny encryption algorithm". Lecture Notes in Computer Science. 1994. DOI: 10.1007/3-540-60590-8_29
50. b49: B Xu, N Wang, T Chen, M Li. Empirical evaluation of rectified activations in convolutional network. 2015
51. b50: Tarun Yadav, Manoj Kumar. "Differential-ML Distinguisher: Machine Learning Based Generic Extension for Differential Cryptanalysis". Lecture Notes in Computer Science. 2020. DOI: 10.1007/978-3-030-88238-9_10
52. b51: Jiajun Zhang, Chengqing Zong. "Deep Neural Networks in Machine Translation: An Overview". IEEE Intelligent Systems. 2015-09. DOI: 10.1109/mis.2015.69
