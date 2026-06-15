# Improving Differential-Neural Distinguisher Model For DES, Chaskey and PRESENT

**Authors:** Liu Zhang, Zilong Wang

**Source PDF:** `2022_zhang_wang_improving_differential_neural_des_chaskey_present.pdf`

## Abstract

In CRYPTO'19, Gohr proposed a new cryptanalysis strategy using machine learning algorithms. Combining the differential-neural distinguisher with a differential path and integrating the advanced key recovery procedure, Gohr achieved a 12-round key recovery attack on Speck32/64. Chen and Yu improved prediction accuracy of differential-neural distinguisher considering derived features from multiple-ciphertext pairs instead of single-ciphertext pairs. By modifying the kernel size of initial convolutional layer to capture more dimensional information, the prediction accuracy of differential-neural distinguisher can be improved for for three reduced symmetric ciphers. For DES, we improve the prediction accuracy of (5-6)-round differential-neural distinguisher and train a new 7-round differential-neural distinguisher. For Chaskey, we improve the prediction accuracy of (3-4)-round differential-neural distinguisher. For PRESENT, we improve the prediction accuracy of (6-7)-round differential-neural distinguisher. 1

## Introduction

Classic differential cryptanalysis is a chosen-plaintext attack, which distinguishes ciphertext from random numbers by studying the probability propagation characteristics of specific plaintext differential values in the encryption process, then carries out the key recovery attacks based on differential distinguisher. The key to classic differential cryptanalysis is to search for a differential distinguisher with a high probability. Differential-neural cryptanalysis is proposed by Gohr [Goh19] based on classic differential cryptanalysis, using differential-neural distinguisher instead of differential distinguisher. The differentialneural distinguisher and differential distinguisher have the same role in distinguishing ciphertext from random numbers. A neural network trains the differential-neural distinguisher as the underlying differential distinguisher, and Bayesian search is used to speed up key recovery attacks. If the prediction accuracy of the differential-neural distinguisher is more significantly than 0.5, it is considered an effective distinguisher.

Gohr [Goh19] showed that the residual network (ResNet) [HZRS16] (previously applied in image recognition) could be trained to capture the non-randomness of the distribution of values of output pairs when the input pairs of round-reduced Speck32/64 are of specific difference. As a result, (5-8)-round (effective) differential-neural distinguishers are trained successfully, and (11-12)-round key recovery attacks for Speck32/64 were achieved by combining 2 rounds of the differential path. In order to launch more rounds of key recovery attacks, better differential-neural distinguishers were also studied recently.

Chen and Yu [CY21] proposed multiple-ciphertext pairs instead of single-ciphertext pairs (in Gohr's work) as the input of the neural network. They improved the prediction accuracy of the (5-7)-round differential-neural distinguisher of Speck32/64 to a certain extent. Bao et al. [BGL + 21] used Dense Network (DenseNet) [HLvdMW17] and Squeezeand-Excitation Network (SENet) [HSS18] with existing deep architectures to train neural network, and obtained (7-11)-round differential-neural distinguisher and devised a 16round key recovery attack for Simon32/64. Zhang et al. [zWW22] borrowed the idea of the Inception block of GoogLeNet to construct the new neural network architecture. Thus, they trained the differential-neural distinguisher for (5-9)-rounds Speck32/64 and (7-12)-rounds Simon32/64. In EUROCRYPT 2021, Benamira [BGPT21] indicated that Gohr's differential-neural distinguisher builds a good approximation of the differential distribution table of the cipher during the learning phase and learns additional information. Based on the principle that the purpose of the differential-neural distinguisher is to obtain the difference information in the ciphertext, we have done some tentative work to train a better differential-neural distinguisher on multiple ciphers in this paper. The main improvements for differential-neural distinguisher are listed as follows.

Our Contributions. We modify the network architecture to train differential-neural distinguisher for three reduced symmetric ciphers in this paper. Compared to Gohr's [Goh19] and Chen's distinguisher [CY21], we improve the prediction accuracy of differentialneural distinguisher for DES, Chaskey, and PRESENT and obtain a more round differentialneural distinguisher for DES under different group size m.

The rest of the paper is organized as follows. Section 2 introduces the network architecture and train process of our differential-neural distinguisher. Section 3 exhibits the prediction accuracy of our differential-neural distinguisher for three reduced symmetric ciphers. Our work is summarized in Section 4.


## Our Differential-Neural Distinguisher Model

Gohr [Goh19] proposed the method of differential-neural cryptanalysis based on classic differential cryptanalysis, where a differential-neural distinguisher is trained using a neural network. The differential-neural distinguisher is a one-to-many differential path compared to classic differential cryptanalysis. The input difference of plaintext is identical, but the output difference of ciphertext is different in differential-neural cryptanalysis. The role of the differential-neural distinguisher is to learn the differential information in the ciphertext.


## Theoretical Model Function

The differential-neural distinguisher is a supervised model to distinguish ciphertext and random numbers. Therefore, it is necessary to construct ciphertext and random numbers artificially, thereby assigning corresponding labels. Gohr Given m plaintext pairs {(P i,0 , P i,1 ), i ∈ [0, m -1]} and target cipher, the resulting ciphertext pairs {(C i,0 , C i,1 ), i ∈ [0, m -1]} is regarded as a sample. Each sample will be attached with a label Y :

If Y is 1, this sample is sampled from the target distribution and defined as a positive example. Otherwise, this sample is sampled from a uniform distribution and defined as a negative example. To guarantee the prediction accuracy of differential-neural distinguisher, a large number of samples need to be put into neural network training. If the neural network can obtain a stable prediction accuracy higher than 0.5 on a test set, it can effectively distinguish ciphertext and random numbers. The theoretical model function can be described as:

where f (X i ) represents the basic features of a ciphertext pair X i and ϕ(•) is the derived features obtained from f (X i ) and F (•) is the new posterior probability estimation function. In Gohr's model, the value of m is 1 [Goh19] . In Chen's model, the value of m is {2, 4, 8, 16} [CY21].


## Design the Network Architecture

The differential-neural distinguisher is a posterior probability estimation function that evaluates the quality of the distinguisher with prediction accuracy. Training a differentialneural distinguisher using a neural network is to capture differential information in the ciphertext and unknown information between multiple-ciphertext pairs. The network architecture of Gohr's [Goh19] and Chen's [CY21] model mainly includes an initial convolutional layer consisting of width-1 convolutional layers and multiple residual blocks. Zhang et al. [zWW22] modified the initial convolutional layer using the Inception block instead of the width-1 convolutional layer. According to theoretical derivation and experiment findings, the following network architecture can ensure the prediction accuracy of the distinguisher to the greatest extent. The network architecture contains several modules that are described in Figure 1 .

The network architecture of our differential-neural distinguisher model.


## Input Module: Data Format.

The neural network receives m ciphertext pairs {(C i,0 , C i,1 ) | i ∈ (0, m)} as input data. We convert a ciphertext pair into a two-dimensional matrix based on the word size of the target cipher. The input layer of the neural network consisting of multiple-ciphertext pairs is arranged in a m × ω × 2L ω array, where L represents the block size of the target cipher, and ω is the size of a basic unit. If the target cipher belongs to the Feistel structure, ω is usually 4. The generation method and arrangement structure of the input data are shown in Figure 2 .

The arrangement structure of input data Module 1: Initial Convolution. After converting the initial ciphertext data to a specific format, the train data enters the initial convolutional layer. The input layer is connected to the initial convolutional layer, which comprises three convolution layers with N f channels of different kernel sizes (k 1 , k 2 , k 3 ), where ideas come from the Inception block of GoogLeNet. The three convolution layers are concatenated at the channel dimension. Batch normalization is applied to the output of concatenate layers. Finally, rectifier nonlinearity is applied to the output of batch normalization, and the resulting [m, ω, 3 × N f ] matrix is passed to the Convolutional Blocks layer. The architecture of the initial convolutional layer can be seen in Figure 3 .


## Figure 3: The initial convolution layer

Module 2: Convolutional Blocks. Each convolutional block consists of two convolutional layers of 3 × N f filters. Each block applies first the convolution of kernel size k s , then a batch normalization, and finally a rectifier layer. At the end of the convolutional block, a skip connection is added to the output of the final rectifier layer of the block to the input of the convolutional block and passes the result to the next block. After each convolutional block, the kernel size increases by 2. The amount of convolutional blocks is determined by experiment. The architecture of convolutional blocks layer can be seen in Figure 4(a) .


## Output Module: Prediction Head.

The prediction head consists of a GlobalAverage-Pooling layer and an output unit using a Sigmoid activation function. We add a dropout layer (the drop rate is set to 0.8) before the Sigmoid activation function to prevent model overfitting. The structure of the prediction head is shown in Figure 4(b) .

Rationale. First, to make it easier for the neural network to capture the differential information of the ciphertext pair, we convert the ciphertext vector into matrices in the input module. Using multiple-ciphertext pairs with the same distribution as the input of the neural network can significantly reduce the influence of a single misjudgment on the


## GlobalAverageP ooling

Dropout Sigmod (b) The prediction head whole result. Second, the design idea for the initial convolutional layer comes mainly from the Inception block [SLJ + 15] in GoogLeNet to capture more dimensional information. In the initial convolutional layer, the size of kernel is k 1 , k 2 , k 3 separately. In general, we set k 1 to 1. Using the initial width-1 convolutional layer is intended to make learning simple bit-sliced functions easier, such as bitwise addition. To capture the features of the internal architecture of the cryptographic algorithm, we add the convolution operation of widths k 2 and k 3 to capture features under different dimensions, such as the circular shift operation, the modular addition operation. Third, to ensure that the cryptographic algorithm encrypts different rounds without modifying the network architecture, we use a residual network to let the network automatically adjust the model parameters. In order to capture information in a larger dimension, we modify the size of the residual network convolution kernel in Gohr's model to keep it incrementing 2. Finally, to prevent the problem of overfitting caused by too few sample sizes, we added a dropout layer. The essence of using a deep residual network to construct a differential distinguisher is to treat the cipher with a nonlinear round function as a complex function and use multiple residual blocks to fit the function.


## Model Training Process


## Data Generation.

Training and test data were generated by using the Linux random number generator to obtain uniformly distributed keys K i and plaintext pairs P i with the input difference ∆ as well as a vector of binary-valued real/random labels Y i . During producing training or test data for the target cipher, the plaintext pair P i was then encrypted for R rounds if Y i = 1, while otherwise, the second plaintext of the pairs was replaced with a freshly generated random plaintext and then encrypted for R rounds. In this way, training data set N = 10 7 and test data set M = 10 6 samples were generated for training and testing.


## Basic Training Scheme.

We run the training for 20 epochs (denoted by B s ) on the dataset of size 10 7 . In order to maximize GPU performance, the batch size (denoted by E s ) processed by the dataset is adjusted according to the parameter m. The last 10 6 sample was withheld for the test. Optimization was performed against mean square error loss plus a small penalty based on L2 weights regularization parameter λ = 10 -5 using the Adam algorithm [KB15] . A cyclic learning rate schedule was used, setting the learning rate l i for epoch i to l i = α + (n-i) mod (n+1) n .(βα) with α = 10 -4 , β = 2 × 10 -3 and n = 9. The networks obtained at the end of each epoch were stored, and the best network by validation loss was evaluated against a test set.


## Staged Train Method.

When the number of encryption rounds is large, the basic train-ing scheme described above fails, i.e., the model does not learn to approximate any helpful function. The staged train method divides the training process of the differential-neural distinguisher into multiple stages. In [Goh19] , Gohr trained an 8-round distinguisher of Speck32/64 by using the staged train method. For more detailed method details, refer to [Goh19] .


## The Experiment Result

The prediction accuracy is the essential indicator that reflects the performance of the differential-neural distinguisher. For a cipher reduced to R rounds, a specific plaintext differential is set firstly. Then a training set and test set are randomly generated. After sufficient training, we will obtain the testing accuracy of the obtained new differential-neural distinguisher. A key parameter of our differential-neural distinguisher is the number of ciphertext pairs: the group size m, which has four options {2, 4, 8, 16}. Other parameters related to the training and the network architecture of our differential-neural distinguisher are listed in Table 1 .

Table 1: Related parameter for training differential-neural distinguishers

The baseline distinguisher, abbreviated as BD, is reproduced by Chen et al. [CY21] according to the network architecture of Gohr [Goh19] . The differential-neural distinguisher of Chen, abbreviated as M CN D, is trained by using multiple-ciphertext pairs instead of single-ciphertext pairs as the input of the neural network in [CY21] . According to the network architecture in Section 2, we carried out two sets of experiments. The Case 1 is an experiment using N = 10 7 samples to train and M = 10 6 samples to test differentialneural distinguisher. Also, the Case 2 is an experiment using N = 10 7 × m samples to train and M = 10 6 × m samples to test differential-neural distinguisher. Meanwhile, we removed the Dropout layer in the Case 2 . According to the structure of the input module in the neural network, the number of multiple-ciphertext pairs in the training set ans test is N m and M m , respectively. In Case 1 , when the value of m is relatively large, the number of samples in the test set will be relatively small, resulting in overfitting, which is why experiment 2 is carried out.


## Experiments on DES

Differential-Neural Distinguishers for Reduced DES: DES [How87] is a block cipher that is built on a 6 × 4 Sbox. Based on the analysis of DES in [BS93], the plaintext difference adopted in this paper is α = (0x40080000, 0x04000000) and the baseline distinguishers were built for reduced DES firstly [Goh19] . Our differential-neural distinguishers are built for DES reduced to 5, 6, and 7 rounds. The parameter (k 1 , k 2 , k 3 ) in the initial convolutional layer are (1, 4, 6) . The penalty factor is increased to 8 × 10 -4 . Other related parameters are the same as Tabel 1. Corresponding distinguisher prediction accuracy is shown in Table 2 .

In Table 2 , we can see that the distinguisher BD has effectively distinguished ciphertext and random number when the reduced rounds R = 5. Compared to the prediction accuracy of the distinguisher M CN D [CY21], we cannot significantly improve the accuracy of the differential-neural distinguisher where R = 5. When R = 6, the distinguisher M CN D cannot significantly improve the prediction accuracy, even if the group size m is Training 7-round Distinguisher Using the Staged Training Method. For 7 rounds, the training scheme described above fails, i.e., the model does not learn to approximate any helpful function. We still succeeded in training a 7-round neural distinguisher of DES by using several stages of pre-training. First, we use our 6-round distinguisher to recognize 4-round DES with the input difference (0x04000000, 0x40080000) (the most likely difference to appear three rounds after the input difference (0x40080000,0x04000000). The training was done on 10 7 × m samples for twenty epochs with cyclic learning rates. Then we trained the distinguisher so obtained to recognize 7-round DES with the input difference (0x40080000, 0x04000000) by processing 10 7 × m freshly generated samples for ten epochs with a learning rate of 10 -4 . Finally, the learning rate was dropped to 10 -5 after processing another 10 7 × m fresh samples each.


## Experiments on Chaskey

Differential-Neural Distinguishers for Reduced Chaskey: Based on the best differential path searched in [MMH + 14], baseline distinguishers are built for reduced Chaskey firstly [Goh19] . Given the plaintext difference α = (0x8400,0x0400,0,0), the baseline distinguisher can distinguish Chaskey up to 4 rounds. Our differential-neural distinguishers are also built for Chaskey reduced to 3, 4 rounds. The parameter (k 1 , k 2 , k 3 ) in the initial convolutional layer are (1, 5, 8) . All related parameters are the same with Table 1 , except for the penalty factor λ is increased to 10 -4 . Corresponding distinguisher accuracy is present in Table 3 .


## Experiments on Present

Differential-Neural Distinguishers for Reduced Present64/80: Present [BKL + 07] is a block cipher that is based on a 4 × 4 Sbox. Based on the plaintext difference α = (0,0,0,0x9) provide in [Wan08], the baseline distinguisher were built for Present64/80 reduced up to 7 rounds [Goh19] . Our neural distinguishers are also built for Present64/80 reduced to 6, 7 rounds. The parameter (k 1 , k 2 , k 3 ) in the initial convolutional layer are (1, 2, 4). The concrete parameter of constructing neural distinguisher for Present64/80 are as follows. Corresponding distinguisher accuracy is present in Table 4 .


## Conclusions

In this article, we modify the network architecture to train differential-neural distinguisher for three reduced symmetric ciphers, which modify the size of three convolutional kernel in the initial convolutional layer depending on the round function of cipher. Thus, we improve the prediction accuracy of differential-neural distinguisher and obtained more rounds differential-neural distinguisher for DES, Chaskey, and PRESENT.

> [Goh19] took a single-ciphertext pair as input to the model function, and Chen et al. [CY21]generalized it, using multipleciphertext pairs as input to the model function. For brevity in the description, two model functions are represented by an expression.

> 2 Table 2 : Accuracy of differential-neural distinguisher for DES Both in the case of Case 1 and Case 2 , our differential-neural distinguisher significantly increase the prediction accuracy. Meanwhile, we trained successfully the 7-round distinguisher for DES when the group size m = 8 and 16.

> 3 Table 3 : Accuracy of differential-neural distinguisher for Chaskey

> 4 Table 4 : Accuracy of differential-neural distinguisher for PRESENT

## References

1. b0: Verónica Pousada Pardo. "Sumario BGL 53 (2º semestre 2018)". Boletín Galego de Literatura. 2018-12-31. DOI: 10.15304/bgl.53.5694
2. b1: Zhenzhen Bao, Jian Guo, Meicheng Liu, Li Ma, Yi Tu. "Conditional differential-neural cryptanalysis". IACR Cryptol. ePrint Arch. 2021
3. b2: Adrien Bgpt21, David Benamira, Thomas Gérault, Quan Peyrin, Tan Quan. "A deeper look at machine learning-based cryptanalysis". Lecture Notes in Computer Science. 2021
4. b3: Andrey Bogdanov, Lars R Knudsen, Gregor Leander, Christof Paar, Axel Poschmann, M J B Robshaw, et al.. "PRESENT: An Ultra-Lightweight Block Cipher". Lecture Notes in Computer Science. 2007. DOI: 10.1007/978-3-540-74735-2_31
5. b4: Eli Bs93, Adi Biham, Shamir. Differential Cryptanalysis of the Data Encryption Standard. 1993
6. b5: Chen Yi, Hongbo Yu. "A new neural distinguisher model considering derived features from multiple ciphertext pairs". IACR Cryptol. ePrint Arch. 2021
7. b6: Aron Goh19, Gohr. "Improving attacks on round-reduced speck32/64 using deep learning". CRYPTO (2. 2019
8. b7: Gao Hlvdmw17, Zhuang Huang, Laurens Liu, Kilian Q Van Der Maaten, Weinberger. Densely connected convolutional networks. 2017
9. b8: Ralph How, Howard. "Data Encryption Standard (DES) and Advanced Encryption Standard (AES)". Information age. 1987. DOI: 10.1007/springerreference_73130
10. b9: Jie Hss18, Li Hu, Gang Shen, Sun. Squeeze-and-excitation networks. 2018
11. b10: Xiangyu Hzrs ; Kaiming He, Shaoqing Zhang, Jian Ren, Sun. "Deep residual learning for image recognition". CVPR. 2016
12. b11: P Kb ; Diederik, Jimmy Kingma, Ba. "Adam: A method for stochastic optimization". ICLR (Poster). 2015
13. b12: "CrossMark Applying on MMH". MMH. null. DOI: 10.14710/mmh.crossmark
14. b13: Nicky Mouha, Bart Mennink, Anthony Van Herrewege, Dai Watanabe, Bart Preneel, Ingrid Verbauwhede. "Chaskey: An Efficient MAC Algorithm for 32-bit Microcontrollers". Lecture Notes in Computer Science. 2014. DOI: 10.1007/978-3-319-13051-4_19
15. b14: Eun Gi Lee. "Record of Incumbent Retrospection". Sogang Law Journal. 2020-02-29. DOI: 10.35505/slj.2020.02.9.1.11
16. b15: Christian Szegedy, Wei Liu, Yangqing Jia, Pierre Sermanet, Scott E Reed, Dragomir Anguelov, et al.. "Going deeper with convolutions". 2015 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2015-06. DOI: 10.1109/cvpr.2015.7298594
17. b16: Wang Wan08 Meiqin. "Differential cryptanalysis of reduced-round PRESENT". Lecture Notes in Computer Science. 2008
18. b17: Zilong Zww22 Liu Zhang, Boyang Wang, Wang. "Improving differential-neural cryptanalysis with inception blocks". IACR Cryptol. ePrint Arch. 2022
