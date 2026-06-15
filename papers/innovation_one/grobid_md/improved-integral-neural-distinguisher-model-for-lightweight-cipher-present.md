# Improved integral neural distinguisher model for lightweight cipher PRESENT

**Authors:** Wanqing Wu, Mingyu Guo

**Source PDF:** `2024_wu_guo_improved_integral_neural_distinguisher_present.pdf`

## Abstract

PRESENT is a lightweight block cipher, which has attracted many scholars to research its security. In 2022, Zahednejad et al. proposed the integral neural distinguisher on round-reduced PRESENT. In this paper, a new integral neural distinguisher for PRESENT is constructed. In contrast to Zahednejad's works, the proposed integral neural distinguisher can improve the number of attack rounds in one round. This paper proposes a new data format ( invP n 0 , invP n 1 , . . . , invP n 15 , invS n 0 , invS n 1 , . . . , invS n 15 ), which can exposes more features of PRESENT previous round ciphertext. Simultaneously, this paper incorporates MBConv module into the convolutional layers of DenseNet, which enable the neural network to identify a greater variety of features in ciphertext. The data format of the paper is analysed. The results of the analysis show that the data format in this paper is able to identify more features compared to Zahednejad's data format. Further to this, experiments are performed on PRESENT using the integral neural distinguisher in this paper. The experimental results show that the changes make to the neural network and data format have improved the accuracy of distinguishers. Finally, key recovery attacks are conducted on the integral neural distinguishers of SmallPresent-(8) to demonstrate the efficacy of the distinguisher proposed in this paper. The results demonstrate that the key recovery success rates for 5-round and 6-round are 98% and 90%, considering error bits within a range of two bits.

## Introduction

With the widely application of devices such as sensors and RFID, the Internet of Things (IoT) is increasingly becoming a part of daily life. However, the pursuit of enhanced productivity and convenience leads to the compression of storage and computing resources, which makes traditional ciphers (e.g. AES) ineffective in ensuring the data security and privacy of IoT devices. In order to ensure data security and privacy in resourceconstrained environments, PRESENT was proposed by Bogdanov (2007) , which is designed to have low power consumption, low throughput and high efficiency. Since PRESENT was proposed, several cryptanalysis methods such as differential analysis, linear attacks, integral analysis, algebraic analysis, bypass cube analysis, have been employed to scrutinize its security (Bogdanov 2007; Wu and Wang 2013; Xiang et al. 2016; Z'aba et al. 2008; Jain et al. 2020; Nakahara et al. 2009; Yang et al. 2009; Cho 2010; Wang 2008; Collard and Standaert 2009) .

Integral attack (Knudsen and Wagner 2002) was proposed by Knudsen et al., which borrows from square attack (Daemen et al. 1997) , saturation attack (Lucks 2001 ) and multiset attack (Biryukov and Shamir 2001) . Initially, the integral attack was mainly applied to the byte-based ciphers. However, at FSE 2008, bit-based integral attack was proposed and applied to analyse Noekeon, Serpent and PRESENT by Z'aba et al. (2008) . This improvement solve the problem that integral cryptanalysis cannot be applied to bit-based ciphers. In 2013, Wu and Wang (2013) used the properties of PRE-SENT's Sbox to evaluate algebraic degrees and found a 7-round integral distinguisher. In 2016, both Xiang et al. (2016) and Todo and Morii (2016) found a 9-round integral distinguisher by bit-based division property (Todo 2015) , and 12-round PRESENT-80 and 13-round PRE-SENT-128 were attacked by Todo and Morii (2016) via using the 9-round integral distinguisher. In 2018, Wang et al. (2018) proposed an algebraic method and used it to attack 10-round PRESENT-80 and 12-round PRE-SENT-80. At the same time, they proposed a key partition technique to attack 11-round PRESENT-80 and 13-round PRESENT-80.

In recent years, the widely application of deep learning has provided many new approaches to cryptanalysis. At CRYPTO 2019, the great potential of machine learning in cipher identification was demonstrated for the first time by Gohr (2019) . Ghor designed a differential neural distinguisher for the SPECK using ResNet (He et al. 2016) and performed key recovery experiments. This result has led many researchers to investigate neural network assisted cryptanalysis. In 2021, Chen and Yu (2021) improved Ghor's neural distinguisher using multiple ciphertext pairs as the neural network input. They improved the neural network accuracy using different output differences. Inspired by Ghor's work, in 2020, Jain et al. (2020) developed a differential neural distinguisher and applied it to round-reduced PRESENT, which identified 3-5 rounds of PRESENT data from random data with a high probability. Hou et al. (2020) proposed a combination of neural networks and linear cryptanalysis to identify 3-5 rounds of DES, which allow the neural networks gaining the ability to distinguish the linear expressions between the DES and random data. In 2022, Zahednejad and Lyu (2022) firstly proposed combining integral attacks with neural networks. They proved that neural network can capture the integral features of ciphertexts, and their integral neural distinguisher can improve the number of identify rounds by 1-2 rounds compared to the classical integral distinguisher in a variety of cipher structures (e.g. SPN, Feistel, ARX, etc.). In the case of PRESENT, they achieve a 7-round integral neural distinguisher using a 5-round classic integral distinguisher. But as the number of rounds increases, the accuracy of the neural distinguisher decreases from 99% in 5 rounds to 58.1% in 7 rounds. Notably, the 8-round PRESENT integral neural distinguisher transitioned into a process of random guessing. In order to increase the number of rounds identified by the neural network, this paper designs a new data preprocessing method based on the characteristics of the PRESENT and the integral attack.


## Our contributions

In this paper, according to the characteristics of PRE-SENT and integral attack, a new data preprocessing method is adopted. It not only ignores the effects of permutation and subkey addition, but also identifies more features of the previous round ciphertexts. Simultaneously, this paper improves the number of distinguish rounds to 8 rounds with accuracy of 57.32% via using multi-multiset data format, and the convolutional layer of DenseNet is modified by using the MBConv module, which reduces the training time successfully and improves the accuracy of the neural network. The accuracy for rounds 5-7 are 99.58%, 99.13% and 82.03%, respectively. Finally, key recovery attacks are performed on the integral neural distinguishers of SmallPresent-(8). The results demonstrate that the key recovery success rates of the 5-round and 6-round neural distinguishers are 98% and 90% respectively, considering error bits within a range of two bits.


## Preliminaries


## Brief description of PRESENT and SmallPresent-(size) PRESENT

PRESENT (Bogdanov 2007 ) is an SPN block cipher for the resource-constrained environments. It is a 31-round ultra-light block cipher with a block size of 64 bits. The underlying structure of PRESENT has three layers in every round: AddRoundKey layer, SBoxLayer and PLayer. In the AddRoundKey layer, the current state is XORed to the round key. Then, one 4-bit Sbox is applied by the SBoxLayer repeatedly. Finally, all bits are shifted in the PLayer. At the end of the last round, the current state is XORed to the round key to get the ciphertext. The encryption flow of the whole algorithm is shown in Fig. 1 .

According to Fig. 1 , if we take the result of the plaintext passing through the addRoundKey layer as the initial encryption state. Then, the order of the three layers can be changed from AddRoundKey layer, SBoxLayer, PLayer to SBoxLayer, PLayer, AddRoundKey layer. Let Y and Z denote the n th round input and output of the initial encryption state. Then the encryption and decryption process can be expressed in the equations:

(1) Z = P(S(Y ))⊕k n .

(2

Where P, S denote the permutation and substitution in the encryption process. P -1 and S -1 denote the inverse- permutation and inverse-substitution in the decryption process. And k n denote the subkey of the n th round.


## Key schedule

This paper uses PRESENT with a key of 80 bits. The key is represented as k 79 k 78 k 77 . . . k 0 and stored in the key register. The subkey for each round is consisted of the leftmost 64 bits of the key register. After each round of encryption, k 79 k 78 k 77 . . . k 0 in the key register is updated as follows:

Where round_counter represents the current encryption round.

Step 1: The key register is rotated by 61 bit positions to the left.

Step 2: The leftmost 4 bits of the key register are passed through the S-box.

Step 3: The value of round_counter is XORed to the k 19 k 18 k 17 k 16 k 15 .


## SmallPresent-(size)

In order to clearly describe the time complexity of attacking the PRESENT (Cho 2010; Collard and Standaert 2009) , Leander (2010) designed its general variant SmallPresent-(size)(0 < size <= 16 , indicates the size of the PRESENT variant used by the user) based on PRE-SENT-80. SmallPresent-(size) represents a PRESENT

variant with a block size of 4 × size . The overall encryp- tion process of SmallPresent-(size) is the same as that of PRESENT. The differences are as follows:

Player The permutation utilized in SmallPresent-(size) is defined by the following function, which shifts the bit state of state to the bit position P(state).

Inverse permutation can be described as: Key schedule SmallPresent's key scheduling is similar to that of PRESENT-80, with the exception that the subkey consists of the 4 × size rightmost bits of PRESENT-80's subkey.


## Classical intergral distinguisher

Integral analysis was proposed by Daemen et al. when analysing the security of SQUARE (Daemen et al. 1997) . Subsequently, Knudsen et al. formalized it based on the Square attack (Daemen et al. 1997) , Saturation attack (Lucks 2001 ) and Multiset attack (Biryukov and Shamir 2001) . It is a chosen-plaintext attack in which the adversary selects 2 N plaintexts (known as multiset) for a block cipher of size H bits. These plaintexts are binary strings consisting of active bits with different N (N ≤ H ) bit arrangements and constant bits with same H -N bit arrangements. Then the plaintexts are encrypted to obtain the corresponding ciphertexts. If the corresponding ciphertexts contains certain bits, whose XOR is always equal to 0, these bits are called balance bits. Further it claims that the integral distinguisher with 2 N selected plaintexts (or a data complexity of 2 N ) is found. The XOR of the bal- ance bits is the integral feature on which the integral attack relies.

Taking the PRESENT as an example, Xiang et al. (2016) proposed a 5-round integral distinguisher in which the rightmost 4 bits of the ciphertext are balance bits. The distinguisher fixes the rightmost 4 bits of the plaintext as active bits and the leftmost 60 bits of the plaintext as constant bits. The formats of plaintext and its associated ciphertext is shown in Fig. 2 . Encrypt the selected plaintexts for 5 rounds to obtain a multiset containing 16 ciphertexts. Then, apply XOR to the ciphertexts:

The XOR of the balance bits in Eq. 3 is equal to 0. The adversary can decrypt the ciphertexts with their guess of the last-round key. If the XOR of the balance bits from the ciphertexts is equal to 0, the adversary has found the correct subkey.


## DenseNet

DenseNet (Huang et al. 2017) was specially developed to improve accuracy caused by the vanishing gradient in neural networks. Unlike other networks (such as ResNet He et al. 2016 and ResNeXt Xie et al. 2017 ) establish short-circuited connections among layers. DenseNet introduces the concept of dense connectivity, which directly connects all layers in the network.

Assume that the output equation of the neural network is:

Where y l represents the mapping output of the F l to the previous layer y l-1 . F l usually includes BN, RelU, Pooling, Conv and other operations.

For efficient communication among layers, DenseNet uses cross-channel connections to merge the outputs of previous layers into the current layer's mapping. The equation for each layer of DenseNet is as follows.

Where y l denotes the mapping output of the F l to all pre- vious layers. The network structure of DenseNet is shown in Fig. 3 .

(3)

y l = F l (y l-1 ).


## MBConv

MBConv module is an inverted linear bottleneck layer with deeply separable convolution, which is commonly used for lightweight network structures(e.g., Efficientnet Tan and Le 2019, MobileNetV3 Howard et al. 2019 , Mnasnet Tan et al. 2019) . MBConv uses a lightweight depthwise separable convolution (Chollet 2017) to divide the standard convolution into channel-by-channel convolution and point-by-point convolution, thereby reduces the convolutional parameters while maintaining the same input parameters.

Figure 4 shows the main operations of MBConv: Firstly, a 1 × 1 kernel-size convolution is employed to increase the number of input channels. Secondly, a 3 × 3 kernel- size depth-separated convolution is employed to conduct channel-by-channel and point-by-point convolutional operations. Subsequently, a 1 × 1 kernel-size convolution is utilized to adjust the number of channels to the specified filter size. Finally, the inputs and outputs are added together.


## Build 8-round integral neural distinguisher


## Data format

Encrypting the plaintexts from Xiang et al. ( 2016 )'s 5-round integral distinguisher for n ( 5 ≤ n ≤ 8 ) rounds: Where C n j denotes the result of encrypt the j th plaintext for n rounds.

C n j is decrypted using Eq. 2, where the k n is C n 0 . The following result is:

(4) C n 0 , C n 1 , C n 2 , C n 3 , . . . , C n 12 , C n 13 , C n 14 , C n 15 . Fig. 3 DenseNet network structure Based on Eq. 2, split the decryption process of C n j into inverse permutation and inverse substitution:

Where invP n j denotes the inverse permutation result after applying XOR to C n j and C n 0 . invS n j represents the inverse of S-Box.

Finally, the data format of this paper is:

Figure 5 shows the data generation process. The specific data format generation process is as follows: Firstly, we generate the set M randomly, which includes r multisets conforming to the 5-round integral distinguisher.

Where M r_i denotes the i th plaintext in the r th multiset. Secondly, The plaintext set M is encrypted for n rounds. We generate the master key K and binary sample label Y randomly. When Y = 1 , the M is encrypted with K. When Y = 0 , All plaintexts in the set M are replaced with unrestricted plaintexts. K is used to encrypt the replaced set M.

Where C n r_i denotes the result of encrypt the M r_i for n rounds.

Finally, Eq. 6 converts the ciphertexts into the data format required by the neural network:

. Where invP n r_i denotes the inverse permutation result after applying XOR to C n r_i and C n r_0 . invS n r_i denotes the inverse S-Box result for invP n r_i .


## Analysis of the data format

Zahednejad et al. used Eq. 4 as the input data format for the neural distinguisher. We propose a data format in "Data format" section based on Zahednejad's data format.

Here, we compare the data format proposed in "Data format" section with Zahednejad's data format. After analyzing the data format proposed in this paper, as well as the S-Boxes and the ciphertexts of the previous round, we find some underlying relations between them. These relations enable our method to improve the number of rounds and its accuracy compared to the work of Zahednejad and Lyu (2022). The reasons are as follows.

Proposition 1 5-round integral features can be obtained by invP 5 0 , invP 5 1 , . . . , invP 5 15 in Eq. 6.

Proof The invP 5 0 , invP 5 1 , . . . , invP 5 15 in round 5 is denoted by the ciphertexts: P -1 , P and C 5 0 are eliminated to obtain:

Apply XOR to the above results:

S(C 4 0 )⊕S(C 4 0 ), S(C 4 0 )⊕S(C 4 1 ), . . . , S(C 4 0 )⊕S(C 4 15 ).

S(C 4 0 )⊕S(C 4 1 )⊕S(C 4 2 )⊕S(C 4 3 )⊕ • • • ⊕S(C 4 15 ).

The value of the bit is not changed by the operations of P or P -1 , so P -1 does not affect the extraction of integral features:

It follows that the 5-round PRESENT integral features extracted by invP 5 0 , invP 5 1 , . . . , invP 5 15 .

The 5-round PRESENT integral distinguisher is improved to 7 rounds by Zahednejad using a neural network. In order to improve the number of attack rounds, we use Eq. 6 as a new data format. Proposition 1 shows that in the case of 5 rounds, the features extracted by invP 5 0 , invP 5 1 , . . . , invP 5 15 in Eq. 6 are equivalent to C 5 0 , C 5 1 , C 5 2 , . . . , C 5 15 of Zahednejad. However, the number of identification rounds can be improved to 8 rounds by using Eq. 6 as a new data format, the reasons are given in Proposition 2 and Proposition 3. P -1 (C 5 0 ⊕C 5 1 ⊕ • • • ⊕C 5 15 ) = P -1 (P(S(C 4 0 ))⊕k 5 ⊕ • • • ⊕P(S(C 4 15 ))⊕k 5 ) = S(C 4 0 )⊕S(C 4 1 )⊕S(C 4 2 )⊕S(C 4 3 )⊕ • • • ⊕S(C 4 15 ).

Proof It is well-known that a secure cipher has strong randomness. PRESENT is a block cipher designed based on Shannon's (1948) principles of diffusion, confusion, and product iteration. As a result, it possesses strong randomness. In order to facilitate a comparison of the differences between our data format and Zahednejad's data format, we impose a security assumption that each round of encryption for PRESENT exhibits strong randomness. In other words, the probability of the output value being equal to the input value is 0.5. Take PRESENT as an example and apply XOR to 7 rounds of ciphertexts in Zahednejad's data format: Eq. 12 is equal to: Meanwhile, C 7 j obtains information of C 6 j with a probability of 0.5, so each C 7 0 ⊕C 7 j in Eq. 13 obtains information about C 6 0 ⊕C 6 j with a probability of 0.5. The calculation is as follows:

Whereas the data format ( invS 7 0 , . . . , invS 7 15 ) for the 7 rounds in this paper:

j is defined by C 7 0 and the ciphertexts of the 6 rounds, eliminating P -1 , P and C 7 0 yields the following result:

Apply XOR to all invS 7 j :

(12)

p(C 7 0 ⊕C 7 j = C 6 0 ⊕C 6 j ) = p(C 7 0 = C 6 0 , C 7 j = C 6 j ) + p(C 7 0 � = C 6 0 , C 7 j � = C 6 j ) = 0.25 + 0.25 = 0.5.

Proposition 2 demonstrates that the probability of S -1 (S(C 6 0 )⊕S(C 6 j )) in Eq. 14 obtaining information about C 6 0 ⊕C 6 j is higher than 1/2 and cannot be neglected. In other words, the probability of S -1 (S(C 6 0 )⊕S(C 6 j )) in Eq. 14 obtaining information about C 6 0 ⊕C 6 j is 0.625 or 0.53125, where there are more data with a probability of 0.625, whereas the probability of Eq. 13 is close to 0.5. Therefore, Eq. 14 yields more information about C 6 0 ⊕C 6 j .

The above analysis clearly shows that the data format in this paper will have a higher opportunity to learn the XOR information of the previous round than Zahednejad's data format. Thus, the number of attack rounds can be increased at least one round using the data format in this paper. The experiments in "Comparison of different data formats" section further support this point.


## Designing the network structure

Our network is built upon DenseNet and incorporates MBConv to modify the convolutional layers of DenseNet.

Compared to other modules, MBConv can reduce the convolution parameters with the same input parameters, which allows us to create deeper network models with the same amount of computation. Simultaneously, MBConv connects the input and output of the convolutional block through skip connections, which gives the network the opportunity to access the unmodified state in the convolutional block. Therefore, we modified the convolutional layers of DenseNet using the MBConv. This alteration is expected to decrease training time and attain a level of accuracy that is unattainable by other models.

The network is composed of four components: an input layer containing the multisets, an initial convolutional layer composed of a single convolution, a Dense layer modified by the MBConv, and finally, Multiple Fully Connected Layers make up the prediction header. Figure 6 shows the different layers.


## Input layer

We use the Reshape operation in Ten-sorFlow to transform the initial data from Eq. 6 into a three-dimensional [w, 2LM sw , s] . [w, 2LM sw ] represents the characteristic information of each two-dimensional convolution channel operation, where s is the number of channels, w is the width of the channel, 2LM sw is the height of the channel, L is the size of the cipher, and M is the size of the multiset, and s = 8 , L = 64 , w = 16 , M = 16 for PRESENT.


## Initial convolutional layer

The data inflow from the input layer is expanded into N f channels using convolu- tion with a kernel size of 1. Then, Batch normalization and rectifier nonlinearities are applied to the output of these convolutions. Finally, the result is passed to the Dense layer.

Dense layer Each convolutional block contains the MBConv module. In the MBConv module, N f is expanded to 2N f using a 1 × 1 convolutional layer. Sub- sequently, a 3 × 3 depth separable convolutional layer is executed, and a DropOut operation is employed to prevent overfitting. Further to this, a 1 × 1 convolutional layer adjusts the number of channels to the specified size, and the inputs of the MBConv are summed with the outputs. Finally, a 1 × 1 convolutional layer is applied, and the inputs of the Dense layer are connected to the final outputs.

Prediction header The prediction header comprises a Flatten layer, three Fully Connected Layers (FC), and a single output unit. Flatten operations are applied to spread out the inflow of data. Then the three Fully Connected Layers are utilized to process the data from the Flatten layer. Batch normalization and rectifier nonlinearities are performed on the output of the Fully Connected Layers. The final layer utilizes the Sigmoid activation function to output a single output unit. Figure 7 shows the details of the network structure.


## Network training scheme

In this paper, a 2 21 sample training dataset and a 2 17 sample validation dataset are used. In order to test the accuracy, a test dataset with 2 17 samples is generated. The datasets are processed in batches of 2000. In order to optimise the results, we use a mean square error loss function with L2 weight regularization (regularization parameter reg_param = 10 -5 ) and the Adam algo- rithm. During the training process, this paper employs a decreasing learning rate schedule. The update algorithm for the decreasing learning rate is given by the Algorithm 1.

The training was conducted using Python 3.9 and Tensorflow 2.12.0 on Ubuntu 20.04 OS. Our device is a server with an Intel(R) Xeon(R) Platinum 8255C CPU at 2.50 GHz, 80GB of RAM,, and two RTXA4500 20GB GPUs. Each model was repeated 10 times with each training session taking 5 h approximately. Ultimately, the model with the highest accuracy was selected as the final distinguisher. Algorithm 1 Learning rate decline algorithm


## Experimental results


## Experiments on PRESENT

The encrypted data of PRESENT is processed by the method proposed in "Data format" section, and the number of multisets in M is 2. The processed data is fed into the neural network proposed by "Designing the network structure" section for training, and the data used for neural network training, validation and testing are randomly generated with sample sizes of 2 21 , 2 17 and 2 17 , respectively.

In Fig. 8 , the line chart shows the change in accuracy and loss rate for rounds 6-8. The horizontal axis represents the training batch, and the vertical axis represents the loss rate and accuracy of the neural network. From Fig. 8 , it is easy to notice that for 6 rounds the accuracy is 99.13% and the loss rate is 0.84%, for 7-8 rounds the accuracy is 82.03%, 57.32% and the loss rate is 11.51% and 24.35%. Increasing the accuracy of 8 rounds to 57.32% has differentiated the process from random guess, which is unattainable by Zahednejad's distinguisher.


## Comparison of different data formats

Zahednejad used ciphertext (Eq. 4) as the input data format. The data format (Eq. 6) of this paper is given in "Data format" section.

In order to demonstrate the superiority of the data format in this paper, a comparison experiment is designed which fixes all other parameters and only changes the data format. The neural network is trained using the model in "Designing the network structure" section.

Table 1 demonstrates that our data format (the number of multisets in M is 1) achieved an accuracy of 98.16% in 6 rounds. For the 7-round integral neural distinguisher, the accuracy of the data format proposed in this paper surpasses Zahednejad's data format by 14.18%. And to our surprise, it extends the number of identification rounds to 8 rounds when invS n 0 , invS n 1 , . . . , invS n 15 is included in the data format.


## Algorithm 2 Key recovery attack on SmallPresent-(8).


## Comparison of different neural network

Zahednejad trained the distinguishers of three different neural networks (ResNet, ResNeXt, DenseNet) and obtained similar results in terms of accuracy for the three networks.

By only changing the neural network model and using Eq. 6 as the data format (the number of multisets in M is 1). In order to ensure the fairness of the experiment, the same input data is used by different networks and the input data is generated randomly. A comparison is made between the neural network in this paper and that of Zahednejad.

In Table 2 , the accuracy of our network for rounds 6, 7, and 8 are reported as 98.16%, 77.31%, and 53.23%, respectively. Among the four networks, our network improved accuracy by 1.90%, 4.40% and 1.31% in rounds 6-8, respectively. This indicates that the modifications in our network contribute to the effective identification of features. Due to the channel expansion in the MBConv module within our network for extracting additional features, the training time is longer compared to ResNet. Nevertheless, it still remains lower than the training times of DenseNet and ResNeXt. Therefore, when prioritizing accuracy, our neural network proves to be effective.


## Key recovery attack on SmallPresent-(8)

Due to the limitations of the device, in 2011, Blondeau and Gérard (2011) perform key recovery on PRESENT. Consequently, we refer to their work for conducting key recovery attacks on SmallPresent-(8). We believe that the key recovery attacks on the 32-bit SmallPresent-(8) can be extended to higher bits. The active bits selection of SmallPresent-( 8 ) is the same as that of the 5-round PRESENT integral distinguisher which is used to simplify the attack. The integral neural distinguishers for SmallPresent-(8) are trained for 5-7 rounds with accuracies of 99.32%, 72.13%, and 55.62%, respectively.

During the key recovery attacks, the ciphertexts are decrypted by all possible candidate subkeys. Then, the decrypted results are fed into integral neural distinguishers. The outputs of the integral neural distinguishers are used as the scores of the candidate subkeys. The topranked candidate subkey is regarded as the correct subkey suggested by the distinguisher. The specific operation procedure is shown in Algorithm 2.

(1) Generate r plaintexts randomly. Each plaintext is expanded to a mutilset based on active bits. Encrypt these mutilset to obtain the corresponding ciphertext multisets. (2) Decrypt the ciphertext multisets with candidate subkeys.

(3) The score x k i for each candidate subkey is obtained using the integral neural distinguisher. (4) For each subkey k, the scores x k i are merged into the score x k , x k is the score of k and sorts k in descend- ing order.

In this paper, we perform key recovery attacks on the integral neural distinguishers of SmallPresent-(8). Each integral neural distinguisher repeats the key recovery attack 50 times with different keys and each attack uses 8 random plaintexts. Among these attacks, the first suggested subkey of the 5-round integral distinguisher is the correct subkey 45 times. Consequently, the 5-round integral distinguisher achieved a key recovery success rate of 90%. Key recovery success rates for 6-round and 7-round are 62% and 8%. The rank of the candidate subkeys is shown in Table 3 . According to Table 3 , it is not difficult to see that as the accuracy of the distinguisher decreases, it becomes more and more difficult to recover the subkey. Even the 7-round distinguisher only had 4 successful attacks.

. Table 5 Percentage of correct guesses for subkey bits

Subkey bits 1 (%) 2 (%) 3 (%) 4 (%) 5 (%) 6 (%) 7 (%) 8 (%) 9 (%) 10 (%) 11 (%) 12 (%) Percentage of correct guesses 5r 100 100 100 100 100 100 100 100 100 100 100 100 6r 100 100 100 100 100 100 100 100 100 100 100 100 7r 100 100 100 100 100 100 100 100 100 100 98 98 Subkey bits 13 (%) 14 (%) 15 (%) 16 (%) 17 (%) 18 (%) 19 (%) 20 (%) 21 (%) 22 (%) 23 (%) 24 (%) Percentage of correct guesses 5r 100 100 100 100 98 100 96 100 100 100 96 96 6r 100 100 100 98 94 98 92 96 94 96 92 96 7r 96 92 90 81 66 56 68 60 56 60 64 64 Subkey bits 25 (%) 26 (%) 27 (%) 28 (%) 29 (%) 30 (%) 31 (%) 32 (%) Percentage of correct guesses 5r 94 94 96 100 100 100 100 100 6r 90 98 88 96 94 98 86 98 7r 58 66 50 60 56 58 68 52

Additionally, our aim is to ensure correctness for each bit during key recovery attacks. In this paper, a successful guess is defined as the scenario where the subkey guessed by the neural dstinguisher differs from the correct subkey within two bits. Then the incorrect bits can be eliminated by using the exhaustive method. The results of the experiments can be found in Tables 4 and 5 .

The success rate of the 5-round neural distinguisher for SmallPresent-(8) in Table 4 is 98%, with 45 attacks having completely accurate subkey guesses. Among the experiments with incorrect guesses, 3 attacks have only 1 bit errors, and 1 attack have 2 bits guessed incorrectly. Only 1 attack fail to meet the criteria established, and none of them have more than 3 bits of incorrect guesses. Simultaneously, the success rate of the 6-round neural distinguisher for SmallPresent-( 8 ) is 90%, which has 5 attacks with more than 2 bits of error bits. However, the key recovery accuracy of the 7-round distinguisher drops to 18% and there are 36 attacks with more than 4 incorrect bits.

Table 5 statistics the success rate of recovery for each bit. Although the 5-round neural distinguisher incorrectly identifies the key bits, all of these key bits have a success rate of over 90%. For the 6-round distinguisher, only bits 27 and 31 have success rates of less than 90%. But it is still very successful to get such a high bit recovery success rate using the classical 5-round integral distinguisher. Surprisingly, although the neural distinguishers are different, the success rate of the top 10 bits are all 100%.


## Conclusions

This paper improves the integral neural distinguisher of PRESENT and performs key recovery attacks on SmallPresent-(8). Firstly, this paper obtains more derived features by adopting the data format ( invP n 0 , invP n 1 , . . . , invP n 15 , invS n 0 , invS n 1 , . . . , invS n 15 ). Additionally, we implement the ideas from the MBConv module to enhance the convolutional layers of DenseNet. As a result, this paper improves the accuracy of the 6-round and 7-round PRESENT integral neural distinguisher to 99.13% and 82.03%, respectively. And this improvement result in an accuracy of 57.32% for PRESENT's 8-round integral neural distinguisher, which is unattainable by Zahednejad's distinguisher. In order to confirm the effectiveness of the modifications to the neural network, we perform experiments with 4 different neural networks, and the results show that there are some advantages of our network structure in pursuit of accuracy. Finally, we perform key recovery attacks on SmallPresent-(8). The results demonstrate that the key recovery success rates for 5-round and 6-round are 98% and 90%, considering error bits within a range of two bits.

In this paper, the modifications to the data format led to an improvement in accuracy. It shows that the derived features exposed by the data format have a significant effect on the neural network. Simultaneously, we observe subtle differences in the results among different neural networks. Therefore, in the future, we will explore the enhancement possibilities by combining Zahednejad's data format with the data format of this paper and try to find a better data format. Simultaneously, we will attempt to identify the reasons for variations in neural network results, aiming to design an integral neural distinguisher with higher accuracy. We will also attempt to extend the methods to other block ciphers.

> 1 Fig. 1 Fig. 1 PRESENT encryption flowchart

> 2 Fig. 2 Fig. 2 PRESENT's 5-round classic integral distinguisher

> 4 Fig. 4 Fig. 4 MBConv module

> 5 Fig. 5 Fig. 5 Data generation process

> 1 Definition 1 Denote S m_inv as the S -1 of S(A)⊕S(B) ,where S(A), S(B) denote two S-Boxes. S m_inv has a form as: Proposition 2 The XOR of the two S-Boxes inputs is acquired by S m_inv with a non-negligible probability greater than 1/2. Proof Denote x, y as the input value and output value of the i th bit in the S-Box, respectively. The algebraic normal form (ANF) of PRESENT inverse S-Box: Assuming that there are two four-bit S-Boxes, A = [A 0 , A 1 , A 2 , A 3 ], B = [B 0 , B 1 , B 2 , B 3 ] as inputs to the two S-Boxes, a = [a 0 , a 1 , a 2 , a 3 ] and b = [b 0 , b 1 , b 2 , b 3 ] as the corresponding output to the two S-Boxes. Equation 9 is used to calculate S m_inv = S -1 (S(A)⊕S(B)) . Where S i m_inv represents the value of the i th bit of S m_inv .

> 6 Fig. 6 Fig. 6 Neural network architecture

> 7 Fig. 7 Fig. 7 Neural network structure

> 8 Fig. 8 Fig.8PRESENT's loss and accuracy

> 1 Table 1 Comparison of different data formats

> 2 Table 2 Comparison of different neural network

> 3 Table 3 The rank of the candidate subkeys

> 4 Table 4 Total number of incorrect guesses for subkey bits

## Acknowledgements

Not applicable.

## References

1. b0: Alex Biryukov, Adi Shamir. "Structural Cryptanalysis of SASAS". Lecture Notes in Computer Science. 2001. DOI: 10.1007/3-540-44987-6_24
2. b1: Céline Blondeau, Benoît Gérard. "Multiple Differential Cryptanalysis: Theory and Practice". Lecture Notes in Computer Science. 2011. DOI: 10.1007/978-3-642-21702-9_3
3. b2: A Bogdanov, L R Knudsen, G Leander, C Paar, A Poschmann, M J B Robshaw, et al.. "PRESENT: An Ultra-Lightweight Block Cipher". Lecture Notes in Computer Science. 2007. DOI: 10.1007/978-3-540-74735-2_31
4. b3: Yi Chen, Yantian Shen, Hongbo Yu, Sitong Yuan. "A New Neural Distinguisher Considering Features Derived From Multiple Ciphertext Pairs". The Computer Journal. 2021. DOI: 10.1093/comjnl/bxac019
5. b4: Joo Y Cho. "Linear Cryptanalysis of Reduced-Round PRESENT". Lecture Notes in Computer Science. 2010. DOI: 10.1007/978-3-642-11925-5_21
6. b5: Francois Chollet. "Xception: Deep Learning with Depthwise Separable Convolutions". 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2017-07. DOI: 10.1109/cvpr.2017.195
7. b6: B Collard, F-X Standaert. "A Statistical Saturation Attack against the Block Cipher PRESENT". Lecture Notes in Computer Science. 2009. DOI: 10.1007/978-3-642-00862-7_13
8. b7: Joan Daemen, Lars Knudsen, Vincent Rijmen. "The block cipher Square". Lecture Notes in Computer Science. 1997. DOI: 10.1007/bfb0052343
9. b8: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
10. b9: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun. "Deep Residual Learning for Image Recognition". 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2016-06. DOI: 10.1109/cvpr.2016.90
11. b10: Botao Hou, Yongqiang Li, Haoyue Zhao, Bin Wu. "Linear Attack on Round-Reduced DES Using Deep Learning". Lecture Notes in Computer Science. 2020. DOI: 10.1007/978-3-030-59013-0_7
12. b11: Andrew Howard, Mark Sandler, Bo Chen, Weijun Wang, Liang-Chieh Chen, Mingxing Tan, et al.. "Searching for MobileNetV3". 2019 IEEE/CVF International Conference on Computer Vision (ICCV). 2019-10. DOI: 10.1109/iccv.2019.00140
13. b12: Gao Huang, Zhuang Liu, Laurens Van Der Maaten, Kilian Q Weinberger. "Densely Connected Convolutional Networks". 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2017-07. DOI: 10.1109/cvpr.2017.243
14. b13: A Jain, V Kohli, G Mishra. "Deep learning based differential distinguisher for lightweight cipher present". Cryptology ePrint Archive. 2020
15. b14: Hayato Kimura, Keita Emura, Takanori Isobe, Ryoma Ito, Kazuto Ogawa, Toshihiro Ohigashi. "Output Prediction Attacks on Block Ciphers Using Deep Learning". Lecture Notes in Computer Science. 2022. DOI: 10.1007/978-3-031-16815-4_15
16. b15: Lars Knudsen, David Wagner. "Integral Cryptanalysis". Lecture Notes in Computer Science. 2002. DOI: 10.1007/3-540-45661-9_9
17. b16: Gregor Leander, Shahram Rasoolzadeh. "Weak Tweak-Keys for the CRAFT Block Cipher". IACR Transactions on Symmetric Cryptology. 2010. DOI: 10.46586/tosc.v2022.i1.38-63
18. b17: Stefan Lucks. "The Saturation Attack — A Bait for Twofish". Lecture Notes in Computer Science. 2001. DOI: 10.1007/3-540-45473-x_1
19. b18: Jorge Nakahara, Pouyan Sepehrdad, Bingsheng Zhang, Meiqin Wang. "Linear (Hull) and Algebraic Cryptanalysis of the Block Cipher PRESENT". Lecture Notes in Computer Science. 2009. DOI: 10.1007/978-3-642-10433-6_5
20. b19: C E Shannon. "A Mathematical Theory of Communication". Bell System Technical Journal. 1948-07. DOI: 10.1002/j.1538-7305.1948.tb01338.x
21. b20: M Tan, Q Le. Efficientnet: rethinking model scaling for convolutional neural networks. 2019
22. b21: Mingxing Tan, Bo Chen, Ruoming Pang, Vijay Vasudevan, Mark Sandler, Andrew Howard, et al.. "MnasNet: Platform-Aware Neural Architecture Search for Mobile". 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 2019-06. DOI: 10.1109/cvpr.2019.00293
23. b22: Yosuke Todo. "Structural Evaluation by Generalized Integral Property". Lecture Notes in Computer Science. 2015. DOI: 10.1007/978-3-662-46800-5_12
24. b23: Yosuke Todo, Masakatu Morii. "Compact Representation for Division Property". Lecture Notes in Computer Science. 2016. DOI: 10.1007/978-3-319-48965-0_2
25. b24: Meiqin Wang. "Differential Cryptanalysis of Reduced-Round PRESENT". Lecture Notes in Computer Science. 2008. DOI: 10.1007/978-3-540-68164-9_4
26. b25: Shi Wang, Zejun Xiang, Xiangyong Zeng, Shasha Zhang. "Improved Integral Attacks on PRESENT-80". Lecture Notes in Computer Science. 2018. DOI: 10.1007/978-3-030-14234-6_9
27. b26: Shengbao Wu, Mingsheng Wang. "Integral Attacks on Reduced-Round PRESENT". Lecture Notes in Computer Science. 2013. DOI: 10.1007/978-3-319-02726-5_24
28. b27: Zejun Xiang, Wentao Zhang, Zhenzhen Bao, Dongdai Lin. "Applying MILP Method to Searching Integral Distinguishers Based on Division Property for 6 Lightweight Block Ciphers". Lecture Notes in Computer Science. 2016. DOI: 10.1007/978-3-662-53887-6_24
29. b28: Saining Xie, Ross Girshick, Piotr Dollar, Zhuowen Tu, Kaiming He. "Aggregated Residual Transformations for Deep Neural Networks". 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2017-07. DOI: 10.1109/cvpr.2017.634
30. b29: Lin Yang, Meiqin Wang, Siyuan Qiao. "Side Channel Cube Attack on PRESENT". Lecture Notes in Computer Science. 2009. DOI: 10.1007/978-3-642-10433-6_25
31. b30: Mr, H Raddum, M Henricksen, Dawson E. Bit-pattern based integral attack. 2008
32. b31: Behnam Zahednejad, Lijun Lyu. "An improved integral distinguisher scheme based on neural networks". International Journal of Intelligent Systems. 2022-05-09. DOI: 10.1002/int.22895
