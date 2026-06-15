# Improving deep learning-based neural distinguisher with multiple ciphertext pairs for speck and Simon

**Authors:** Yufei Hou, Jie Liu, Shouxu Han, Zhongjun Ma, Xi Ye, Xuan Nie

**Source PDF:** `2025_speck_simon_multi_pair_multiscale.pdf`

## Abstract

The neural network-based differential distinguisher has attracted significant interest from researchers due to its high efficiency in cryptanalysis since its introduction by Gohr in 2019. However, the accuracy of existing neural distinguishers remains limited for high-round-reduced cryptosystems. In this work, we explore the design principles of neural networks and propose a novel neural distinguisher based on a multi-scale convolutional block and dense residual connections. Two different ablation schemes are designed to verify the efficiency of the proposed neural distinguisher. Additionally, the concept of a linear attack is introduced to optimize the input dataset for the neural distinguisher. By combining ciphertext pairs, the differences between ciphertext pairs, the keys, and the differences between the keys, a novel dataset model is designed. The results show that the accuracy of the proposed neural distinguisher, utilizing the novel neural network and dataset, is 0.15-0.45% higher than Gohr's distinguisher for Speck 32/64 when using a single ciphertext pair as input. When using multiple ciphertext pairs as input, it is 1.24-3.5% higher than the best distinguishers for Speck 32/64 and 0.32-1.83% higher than the best distinguishers for Simon 32/64. Finally, a key recovery attack based on the proposed neural distinguisher using a single ciphertext pair is implemented, achieving a success rate of 61.8%, which is 9.7% higher than the distinguisher proposed by Gohr. Therefore, the proposed neural distinguisher demonstrates significant advantages in both accuracy and key recovery rate.

## Motivation

Neural distinguisher-based key recovery attacks have been widely studied for various block ciphers and have achieved higher key recovery rates. However, there is still much work to be done, such as optimizing the input data model, improving the neural network, enhancing interpretability, and advancing the key recovery attack. In this work, we explore the construction of input data, the optimization of the neural network, and their performance in key recovery attacks.


## Our contributions

This paper focuses on the accuracy of the neural distinguisher, which influences the success rate of key recovery attacks while addressing security aspects. The main contributions of this work are as follows:

(i) We design three novel neural networks based on ResNeXt and DenseNet, in which both the residual block and the convolutional layers are improved. Then derive rules of thumb for optimizing the neural network modules: increase the number of convolution layers in the residual block from 2 to 5. Start with a convolution kernel size of 1 and increase it by 2 for each successive convolution layer. Increase the convolution kernel size between different residual blocks by 2 with each step. (ii) We combine the ciphertext pairs and their differences, the keys and the difference of the keys to the dataset.

This approach highlights that the number of ciphertext pairs, the number of decrypted rounds, and the order in which these data are combined significantly affect accuracy. Finally, construct the dataset with highest accuracy by using the ciphertext pairs of different rounds, the differences of the ciphertext pairs of different rounds, and the differences of the keys used to decrypt the ciphertexts of different rounds. (iii) A key recovery attack based on the proposed neural distinguisher is designed and implemented for the Speck 32/64 and Simon 32/64. This attack shows a 9.7% improvement in key recovery rate compared to the state-of-the-art methods for Speck 32/64.

The organization is as follows: The paper is organized as follows. Section 2 provides an introduction to deep learning-based differential cryptanalysis and introduces the Speck cipher. The proposed neural networks and the rules for optimizing them are described in Sect. 3. In Sect. 4, we design two efficient data models and explore the construction of the input dataset using different cipher materials and orders. In Sect. 5, the accuracy of the proposed neural distinguisher for Speck 32/64 and Simon 32/64 is tested. Additionally, we verify the key recovery rate of the proposed neural distinguisher using single ciphertext pairs as input. Finally, the work is concluded in Sect. 6.


## Preliminaries

Let (x, x * ) denotes a plaintext pair with difference ∆ x. The corresponding ciphertext pair is (c, c * ), and the i -th round's ciphertext pair is (xi, x * i ). The notations used in this work are defined as follows:

Definition 1 (Difference). For any plaintext x, x * ∈ {0,1} n , the difference between x and x * is defined as

Definition 2 (Difference of the ciphertext pair). For any plaintext x, x * ∈ {0,1} n with a difference ∆ x = x ⊕ x * , their i-th round's ciphertext are xi and x * i , respectively. Then ∆ xi = xi ⊕ x * i is the difference of the ciphertext pair.

Definition 3 (Neutral bit). Let {e0, e1, . . . , ei , . . . , en-1} ∈ F n 2 be the standard basis, where i ≥ 0 is the index. Suppose that any plaintexts x, x * ∈ {0,1} n have an input difference ∆ x, and their i-th round's ciphertext difference is ∆ xi. If the difference of i-th round's ciphertext of x + ei and x * + ei also equals ∆ xi, then the i-th bit is the neutral bit of the difference (∆ x → ∆ xi).


## The speck 32/64 cipher

The Speck cryptosystem is a lightweight block cipher with an ARX (Addition, Rotation, and XOR) construction. It is proposed by Beaulier et al. 11 for the NSA, aimed at achieving high efficiency for IoT devices. Different rotation constants and the number of rounds are designed for various block and key sizes. A general description of Speck is Speck B/A, where B denotes the block size and A denotes the key size. This work focuses on Speck 32/64 with 22 rounds. The round function is shown in Fig. 1 .

As shown in Fig. 1 , the plaintext is split into two subblocks (Li, Ri) with each length of 16 bits, where i denotes the i-th round. ki is the 16 bits key for the i-th round, generated by the round key schedule algorithm using mast key K. The round function follows a classical Feistel structure, combining XOR, addition modulo, and bitwise operations, which are denoted by ⊕, ⊞ and ⊙, respectively. The bitwise left and bitwise right rotations are denoted by <<< and >>>, respectively. In the round function of Speck 32/64, α = 7 and β = 3.


## The Simon 32/64 cipher

Simon 11 is a lightweight block cipher proposed by the NSA to meet the need for secure, flexible, and analyzable encryption. Its block sizes are 32, 48, 64, 96, and 128 bits, which can be expressed in units of word lengths as 16, 24, 32, 48, and 64, respectively. The round function of Simon is shown in Fig. 2 .


## Scientific Reports | 2025 15:13696

As shown in Fig. 2 , the key-dependent Simon (2

round function is the map R sk i : GF (2) n × GF (2) n → GF (2) n × GF (2) n , defined by formula (1), where n is the block size in word length unit, and l is the number of the key word length.

Where

is the bitwise AND operation, and ski ∈ GF (2) n is the round key.


## Structure of the Gohr' neural network

The structure of the neural network used for differential analysis was first proposed by Gohr in 10 . Its network is shown in Fig. 3 : In 10 , the ciphertext pair (x, x * ) is generated by encrypting two plaintext pair with a specified difference ∆ x , for example ∆ x = (0 × 0040/0000). The ciphertext pair (x, x * ) encrypted by Speck 32/64 is first split into two words. Then, it goes through the initial convolutional (IC) model, where a convolution with a filter size of 1 and 32 filters is applied. Batch normalization and a Rectified Linear Unit (ReLU) activation layer follow the convolutional layer. Next, 10 Convolutional Block (CB) models are applied, each consisting of two iterations of convolutional layers with a filter size of 3 and 32 filters, followed by batch normalization and ReLU activation. The input of each CB model is added to its output. Finally, the output of the last CB model is processed by the prediction head (PH) model, which consists of two iterations of a densely connected layer (using 64 neurons), batch normalization, and ReLU activation. The output of the PH model is processed by a densely connected layer in the output model, which uses a sigmoid activation function and a single neuron.


## The differential analysis

Differential analysis is a commonly used method for data analysis, which extracts significant features and correlations between two or more data sets. It is a form of chosen plaintext attack. This method distinguishes ciphertext pairs of a given difference from random ciphertext pairs based on the probability propagation property of the plaintext pair with the given difference during encryption. Given an encryption function E :

2 , where np denotes the number of the plaintext bits, n k denotes the number of the key bits, and nc denotes the number of the ciphertext bits. Let the input of plaintext pair be (x, x * ), the difference of x and x * is denoted by

and its difference is denoted by

After n rounds of encryption, we obtain a differential sequence Ω = (∆ x, ∆ x1, • • • , ∆ xn), which is called the differential path of the n-rounds of encryption. This path represents the differential propagation characteristics of the encryption. Let ND be the number of the plaintext pair. The probability that all these plaintext pair have a differential path Ω is given by formula (2):

where m is the length of the plaintext. The Differential Distribution Table (DDT) is widely used to analyze cryptosystems, listing the probability of each differential path. In 10 , Gohr constructed a neural distinguisher (ND) for Speck 32/64 reduced to 8 rounds and recovered the key for Speck 32/64 reduced to 11 rounds. First, Gohr extended the 7-round distinguisher to a 9-round distinguisher by prepending a two-round differential transition ∆ x = δ → ∆ x2 = (0x0040,0000), passing as desired with a probability of about 1/64. For example, ∆ x = δ = (0x0211,0x0a04). Then, the 9-round distinguisher was extended by another round with no additional cost, requiring encryptions of ciphertext pairs (x0, x * 0 ) that encrypt to the desired input difference δ after one round of Speck encryption. This creates a 10-round distinguisher, which can be easily achieved since no key addition happens in Speck before the first nonlinear operation. Finally, the ciphertext pair (x11, x * 11 ) is decrypted by a random key, and recovery the key by the 10-round distinguisher and Bayesian optimization. Scientific Reports | 2025 15:13696


## Design of the neural network

Inspired by the pyramid convolutional structure and the residual network, we introduce multi-scale convolution and multi-character studies into the convolutional layer to propose a novel distinguisher (ND). Furthermore, different convolutional block models are designed to enhance the accuracy of the proposed ND. Additionally, three different convolutional block models are designed to use as the ablation schemes and validate the efficiencies of the proposed ND.


## The distinguisher using pyramid convolutional structure

Since the pyramid convolutional structure can capture both global and local features, it is employed to optimize the convolutional module of Gohr's neural network and construct eleven different distinguishers. We test the accuracy of these distinguishers using different number of convolutional blocks NCB, convolutional layers NCL, first convolutional kernel size of each CB model NCK, and the increasement of convolutional kernel size Nstep in each CB block. The results of these distinguishers against 5 round-reduced Speck 32/64 cipher are shown and compared with that of Gohr's distinguisher in Table 1 : As shown in Table 1 , the distinguisher with the highest accuracy is ND_G8, which has five CB models, each with five convolutional layers. The convolutional kernel sizes for the first CB model are 1, 3, 5, 7, and 9 for each convolutional layer, with the corresponding convolutional kernel size of each subsequent CB model increasing by a step of 2. The accuracy of all the improved distinguishers is higher than that of Gohr's, which implies that the pyramid convolutional structure can improve the accuracy of the ND.

From above, we derive the structure optimization criteria of neural discriminator network based on ResNet as follows:

Proposition 1 The accuracy of the neural distinguisher can be enhanced by increasing the number of convolutional layers in the residual block from 2 to 5.


## Proposition 2

The accuracy of the neural distinguisher can be enhanced by increasing the convolutional kernel size in the residual block from 1, with a step of 2.

Proposition 3 The accuracy of the neural distinguisher can be enhanced by increasing the initial convolutional kernel size in different residual blocks with a step of 2.


## New distinguisher base on multiple scale convolution and denser residual connection

Based on the above propositions, we introduce the denser residual connection in 37 and construct a novel CB model. Then, present a new neural distinguisher ND1 with five proposed CB models, while the other models remain the same as Gohr's. The network structure is shown in Fig. 4 .

In Fig. 4 , ks denotes the initial convolutional kernel size, and i denotes the i-th convolutional block. The operation ⊕ denotes addition. In the new convolutional block, a denser residual connection is added from the input to all the convolutional layers. The n-th convolutional layer is defined by formula (3).

where x is the input of the n-th layer, F i (x) is the output of the i-th layer. The final output of the convolutional block model is F N CL (x). Additionally, a skip connection is added from the output of each convolutional layer to the input of all subsequent convolutional layers, while the convolutional kernel size of the residual block increases by 2. These skip connections allow the use of features from lower layers, and the addition operation preserves the shape of the feature matrix, preventing the data dimension from exploding.

The ciphertext pairs are first reshaped into a two-dimensional array with 16 columns. Then, they are processed by a convolution operation with a kernel size of 1, followed by Batch Normalization and the ReLU function. In the convolutional block model, the data is processed through five convolutional blocks, each containing different convolutional layers. In each convolutional block, there are five convolutional layers with an increasing convolutional kernel size, incrementing by 2, enabling feature extraction at different scales. The output of the convolutional block model is processed by two dense blocks, each containing a dense layer of size 64, a Batch Normalization operation, and a ReLU function. Finally, the features are mapped into the target space by a dense layer of size 1 and passed through the Sigmoid function. By using the multi-scale convolution operation in the convolutional block model, more features of the ciphertext pairs can be captured, allowing the new neural distinguisher to achieve higher accuracy.


## Design of the ablation schemes

In the proposed distinguisher ND1, the input of each convolutional layer is the output of its previous convolutional layer, except for the first convolutional layer. To verify whether this design may lead to the loss of some features from the original input, we consider using convolutional layers with different kernel sizes simultaneously to process the original input. We replace the CB model of ND1 with five parallel CB blocks, each containing different convolutional layers, to obtain a new neural distinguisher ND2. The structure of the CB model of ND2 is shown in Fig. 5 .

Here, the parameters ks represents the initial convolutional kernel size. As shown in Fig. 5 , there are five convolutional blocks, each consisting of two identical convolutional layers. The convolutional operation of each identical layer can be defined as a function F (x) . The convolutional kernel size of the convolutional layers increases with a step of 2. Multiple groups of convolutional layers with different kernel sizes can study features in parallel, thereby enhancing the model's expressive power. This approach also reduces the number of parameters and computational cost.

Additionally, the initial convolutional model of ND1 uses a single convolutional layer with a kernel size of 1 to capture the features of the ciphertext pairs. To verify whether multiple convolutional layers with different kernel sizes can capture more nonlinear features that are widely present in ciphertext pairs, we replace the initial convolutional model of ND1 with a new initial convolutional model containing multiple convolutional layers with different kernel sizes. The resulting neural distinguisher is denoted as ND3. The structure of the new initial convolutional model is shown in Fig. 6 .


## Scientific Reports | 2025 15:13696

In Fig. 6 , the input is processed simultaneously by three convolutional layers at the first depth, each with a kernel size of 1 and denoted as F 1,1 (x), F 1,2 (x) and F 1,3 (x), respectively. Then, the outputs of F 1,1 (x) and F 1,3 (x) are concatenated and used as the input for the first convolutional layer at the second depth, defined as F 2,1 (x) = F (F 1,1 (x) , F 1,3 (x)). The second convolutional layer at the second depth is defined as F 2,2 (x) = F (F 1,2 (x) , F 1,3 (x)). Following the same method, the convolutional layer at the third depth is defined as F 3,1 (x) = F (F 2,1 (x) , F 2,2 (x)). Finally, the three outputs are added together to generate the output of the initial convolutional model.


## Best parameters and network structure for the proposed neural distinguisher

To verify the effectiveness of the proposed neural distinguisher, the accuracy of the neural distinguishers ND1 , ND2, and ND3 is tested. The simulation environment is set up as follows:


## Hyperparameters

We set the number of epochs to 200 and the batch size to 5000. The default parameters of the Adam algorithm in Keras 38 are used to optimize the mean squared error (MSE) loss, with a small penalty based on L2 weights regularization, and a regularization parameter c = 10 -5 . The learning rate for epoch i is defined as formula (4).

where α = 10 -4 , β = 2 • 10 -3 , and n = 9.


## Data generation

The random number generator in Linux, using a fixed random seed, is used to generate the keys, training dataset, and test dataset. The size of the training set is 10 7 , while the size of the test set is 10 6 . Half of the dataset is generated by encrypting the plaintext pairs with an input difference ∆ x = (0x0040,0x0000), which is labeled by 1. The other half of the dataset is generated by encrypting random plaintext pairs, which are labeled as 0.

Considering the improvements to Gohr's NDs in Table 1 , which achieve higher accuracy when NCK = (3,5, 7,9) and NCK = (1,3, 5,7, 9), we test the accuracy of ND1 and ND2 against 5 round-reduced Speck 32/64 for different NCK in Table 2 :

From Table 3 , we can see that the accuracy of the proposed distinguishers ND1 is approximately equal to the ablation scheme ND2. Therefore, applying parallel convolutional layers with different kernel sizes to the original input has a limited effect on the neural distinguisher. Furthermore, ND2 requires more training time and computational resources, as it requires copying multiple inputs to the CB model and uses more convolutional layers. Therefore, ND1 is more suitable for large input datasets. Although the accuracy of another ablation scheme ND3 is higher than that of the other distinguishers for both 5-round and 6-round reduced Speck 32/64, it is lower than the distinguishers in 10, 30 for the 7-round reduced Speck. Moreover, its accuracy is significantly lower than that of ND1, suggests that multi-scale convolution in the initial convolutional model fails to capture additional nonlinear features effectively. The accuracy of ND1 is higher than that of the traditional distinguisher and the ND models in 10, 29 , and 30 . The advantage ranges from 0.2 to 0.5%, which is significant according to Gohr's evaluation criteria for neural distinguishers.

Additionally, the training time, inference speed, memory usage, and number of parameters of the different neural distinguishers are tested on an Intel(R) Xeon(R) Silver 4216 CPU @ 2.10 GHz platform with an RTX 3090 GPU. The results are shown in Table 4 . Scientific Reports | 2025 15:13696

Table 4 shows that, the proposed ND1 requires less time than ND2. Although the efficiency of ND1 is lower than ND3, its accuracy is higher. Since accuracy is more critical for key recovery than slightly increased resource consumption, the proposed ND1 represents the best compromise between accuracy and efficiency.

To verify the validity of the above optimization criteria (Propositions 1-3) for ND1, we conduct an ablation experiment with different combinations of the criteria. The details are shown in Table 5 .

Table 5 demonstrates that the combination of different improved components in ND1 contributes to a 0.46% improvement in accuracy.

Thus, we can conclude that the three propositions in Sect. 3.1 are applicable to the proposed neural distinguisher ND1, ND2 and ND3. The denser residual connection and the multi-scale convolutional layers in the convolutional block module can significantly improve the accuracy of the neural distinguisher. Among them, ND1 achieves the best balance between efficiency and accuracy compared to ND2 and ND3. Table 3. Comparison of accuracy of different neural distinguishers. *D denotes the traditional distinguisher. *Ghor denotes the neural distinguisher that uses knowledge distillation for the 7 round-reduced Speck 32/64. Table 2. The accuracy of the NDs using improved CB model with different NCK From Table 2, we can see that the accuracy of ND1 and ND2 obtains the maximum advantage of 0.34-0.43% compared to Gohr's when NCK = (1,3, 5,7, 9) . Therefore, we adopt NCK = (1, 3, 5, 7, 9) for the proposed ND1 in the following work. Furthermore, we validate the efficiency of ND1 and the ablation schemes, and compare them with other distinguishers in Table 3 :


## Mathematical analysis of feature extraction improvement

The convolutional kernel size in 10 remains constant at 3, which results in a limited and small receptive field. In this work, the convolutional kernel size within the residual block and between residual blocks increases by a step of 2, leading to a richer convolutional receptive field and an extended feature range. The computation of the receptive field is defined by formula (5):

where RF i+1 denotes the receptive field of the (i + 1)-th layer, ks represents the convolutional kernel size, and Si denotes the product of the all the steps from the first layer to the i-th layer. Since the convolutional step of both ND1 and the neural distinguisher in 10 is 1, the receptive field can be denoted by RF i+1 = RF i + (ks -1) . Therefore, the receptive field of ND1 becomes larger than that of the neural distinguisher in 10 from the third convolutional layer. Furthermore, the receptive field of ND1 increases at each convolutional layer and convolutional block, allowing it to capture multi-scale features. Additionally, based on the definition of the neural network in formula (3), we analyze the process of each convolutional layer in the proposed ND1 and Gohr's neural distinguisher in 10 . Let x l denotes the input of the neural distinguisher, l denotes the l-th convolutional block. The output of each convolutional layer is presented in Table 6 : Here, Conv 1D (a, b, c) denote a 1D convolution operation using convolutional layer weight a, convolutional kernel size b, and input c. W l i denotes the weight of the i-th convolutional layer in the l-th convolutional block. Table 6 shows that the final output of ND1 integrates all the features captured by different convolutional layers, whereas the final output of the neural distinguisher in 10 only contains the features captured by the current convolutional layer. Therefore, the modifications introduced in this work significantly enhance the performance of the distinguisher.


## Constructing of dataset using multiple ciphertext pairs

Besides the improvement of the neural network structure, the construction of the dataset is another important way to improve the accuracy of the neural distinguisher. In this section, we propose two methods to construct the dataset using different rounds of ciphertext pairs, decryption keys, and ciphertext pair differences. Then obtain two optimal combinations of these elements and test their accuracy.


## Two novel models of dataset construction

Since the input data can provide different features for the ND, we construct two new datasets by combining ciphertext pairs, decryption keys, and ciphertext pair differences from different decryption rounds. These datasets are denoted as follows: multi-round multi-splicing ciphertext-pair and keys (MRMSCPK), and multiround multi-splicing ciphertext-pairs and differences (MRMSCPD).

In MRMSCPK, the ciphertext pair (xi, x * i ) is decrypted by a random key to obtain the ciphertext pair (xi-1, x * i-1 ) and (xi-j, x * i-j ) is obtained by decrypting j times with j different keys. The dataset is denoted by {(xi,

) N d , key}, where (xi, x * i ) l denotes the l-th ciphertext pair of i-round's encryption, key = {key 1 , • • • , key j }, and N d is the number of the ciphertext pairs. The structure is shown in Fig. 7 .

Here, ND is the number of ciphertext pairs. xi-j denotes the ciphertext obtained by decrypting a i-round's ciphertext j times. The size of the dataset is (2m

In MRMSCPD, the dataset consists of the ciphertext pairs and the difference of the ciphertext pairs, which is denoted as

. Here, (xi, x * i ) l denotes the l-th ciphertext pair of i-round's encryption, and (∆ xi) l denotes the difference of the l-th ciphertext pair. The detail is shown in Fig. 8 .


## Index of the convolutional layer


## Output of the convolutional layer


## ND1

ND in [10]

Table 6 . The output of each convolutional layer for different neural distinguishers.


## Scientific Reports | 2025 15:13696


## Construction of dataset with different decryption rounds

Although the decrypted ciphertext pairs are useful for capturing features, the error propagation introduced by decryption with random keys may mislead the neural distinguisher. Therefore, we explore efficient decryption rounds to construct the datasets for MRMSCPK and MRMSCPD, where the decryption rounds j are varied from 1 to 2. When j = 1, the datasets are denoted by DRMSCPK and DRMSCPD, respectively. We use the ciphertext pairs and their differences from the i-th and (i -1)-th rounds, along with the keys used to decrypt the ciphertext of the i-th round, to construct double-round multiple splicing ciphertext pairs with differences and keys (denoted as DRMSCPDK). The structure of the DRMSCPDK is shown in Fig. 9 .

) and (xi-2, x * i-2 ) using the same random key. All these ciphertext pairs and their differences are used to construct triple-round multiple splicing ciphertext pairs and differences (denoted as TRMSCPD), as shown in Fig. 10 .

Furthermore, we use two different keys to decrypt (xi, x * i ) and add the differences of the keys at the end of the data in Fig. 10 which is denoted as TRMSCPDKD (triple-round multiple splicing ciphertext pairs, differences, and key differences).

Since the dataset is reshaped to a 4 × B 2 matrix for each ciphertext pair and input into the initial convolutional layer, the order of the ciphertext pairs and their differences may affect the accuracy. Therefore, we change the order of DRMSCPDK to

. This dataset is denoted as DRMSCPDK* and shown in Fig. 11 .


## Scientific Reports | 2025 15:13696

Then, we change the order of TRMSCPDKD to

. This is denoted as TRMSCPDKD* and shown in Fig. 12 .


## Test of accuracy and key recovery

To validate the efficiency of the different datasets, we train the neural distinguisher ND1 using the proposed datasets and compare the accuracy of the different neural distinguishers. Additionally, we test key recovery using the proposed ND1 for Speck 32/64 and Simon 32/64. The details are as follows.


## Testing the proposed distinguisher with a new dataset format for speck 32/64

Since the neural distinguisher ND1 achieves the best accuracy and training speed for a single ciphertext pair, we fine-tune the structure and reduce the number of convolutional layers in each convolutional block to 4 for handling multiple ciphertext pairs. The size of the training dataset and prediction dataset is 10 6 and 10 5 , respectively. The epoch is set to 100, and the batch size is set to 1000. The learning rate of epoch i is defined as li = α + (n-i) mod (n+1) n • (βα ), where, α = 10 -4 , β = 2 • 10 -3 , and n = 9. The number of ciphertext pairs is set to ND = 32, as used in 33 . The accuracy of the proposed ND1 for Speck 32/64 is test and compared in Table 7 .

From Table 7 , we can see that the accuracy of all the proposed datasets using ND1 is higher that of the neural distinguisher in 33 , where the accuracy in 33 is the highest so far. The datasets DRMSCPDK* and TRMSCPDKD* achieve the highest accuracy for 8-round-reduced Speck 32/64 and 7-round-reduced Speck 32/64, respectively.


## Scientific Reports | 2025 15:13696

Both datasets show an advantage of 2.1-2.16% for 7-round-reduced Speck 32/64, and 0.48-0.69% for 8-roundreduced Speck 32/64. The improvement in accuracy is significant.

We analyzed the reason that these particular data organizations capture more distinguishing features from the perspective of theoretical cryptography. As shown in Fig. 2 , the (i + 1)-th ciphertext can be obtained by formula (6).

That is, the (i + 1)-th ciphertext contains information about the bit shift and XOR operations between the i-th ciphertext and the i-th key. The difference of the ciphertext pair can be defined by formula (7):

We have

and

In the left-hand side of the difference equation, the i-th key is eliminated. While the right-hand side contains only the bit shift operation of

. Therefore, the difference of the ciphertext pair removes the confusion introduced by the XOR operation and the i-th key, making the ciphertext features more distinguishable. In this section, keys are added to the dataset DRMSCPDK*, and key differences are included in the dataset TRMSCPDAK*. This enables the neural distinguisher to study them independently, allowing it to extract more features. These theoretical analyses also demonstrate that the proposed datasets help capture more distinguishing features.

Additionally, we test the accuracy of the proposed neural distinguisher using ND1 with different number of ciphertext pairs ncp, which help us explore the optimal number of ciphertext pairs. The results are shown in Table 8 .

In Table 8 , the symbol "×" denotes that the accuracy of the neural distinguisher is smaller than 50.5%, which indicates that it cannot make an efficient distinction. The accuracy of the proposed scheme is higher than that

Round ND Number of ciphertext pairs ncp 2 4 8 16 32 64 128 256 7 ND of [33] 63.33% 68.51% 75.82% 84.48% 94.11% 95.51% 98.12% 98.62% CSYY [29] 64.99% 69.17% 72.93% 71.34% 69.52% 58.46% 59.91% × DRMSCPDK*/ ND1 (Ours) 64.62% 70.00% 79.26% 88.92% 96.21% 99.01% 99.39% 99.86% TRMSCPDKD*/ ND1 (Ours) 64.24% 70.78% 79.29% 88.84% 96.27% 99.03% 99.67% 99.86% 8 ND of [33] 52.96% 54.45% 56.91% 56.91% 65.02% 55.32% 52.79% 57.34% CSYY [29] × × × × × × × × DRMSCPDK*/ ND1 (Ours) × 54.53% 57.45% 61.11% 65.71% 69.52% 74.30% 71.58% TRMSCPDKD*/ ND1 (Ours) 51.93% 53.78% 57.03% 57.03% 65.5% 69.41% 73.13% 72.40% 9 ND of [33] × × × × × 50.46% 50.54% 50.65% CSYY [29] × × × × × × × × DRMSCPDK*/ ND1 (Ours) × × × × × 50.52% 51.01% 50.91% TRMSCPDKD*/ ND1 (Ours) × × × × × 50.64% 50.79% 50.67% of 29] and [33 for all round-reduced Speck32/64 variants. The accuracy of the proposed neural distinguisher using the DRMSCPDK* dataset and the ND1 network is 3.5% higher than that of 29 when ncp = 64. Its accuracy reaches 99.86% when ncp = 256, which is 1.24% higher than 29 . For the 9-round-reduced Speck32/64, the accuracy of the proposed neural distinguisher is 51.01% when ncp = 128, which is 0.47% higher than 29 and can make an efficient distinguish. Additionally, the accuracy of the neural distinguisher increases as ncp increases, reaching its highest accuracy when ncp = 128. This trend is particularly evident for 8-and 9-round-reduced Speck 32/64.


## Testing the proposed distinguisher with a new dataset format for Simon 32/64

To validate the generalization of the proposed neural distinguisher and dataset, we test the accuracy of the proposed ND1 with the dataset TRMSCPDKD* for different round-reduced Simon 32/64 ciphers. The number of the ciphertext pairs is set to 32 to compare with other literatures. The results are shown in Table 9 .

In Table 9 , the neural distinguishers proposed in 33 and our paper can distinguish ciphertext pairs with fixed input differences from those with random input differences with a probability higher than 60%. The accuracy of the proposed ND1 with the TRMSCPDKD* dataset is 0.32%, 1.83%, and 0.44% higher than that of the neural distinguisher in 33 for 9, 10, and 11 round-reduced Simon 32/64 ciphers, respectively.

Therefore, the proposed neural distinguisher demonstrates a significant advantage over other neural distinguishers. Additionally, it achieves high accuracy for both the Speck 32/64 and Simon 32/64 ciphers when using the TRMSCPDKD* dataset. We also evaluate the accuracy of the proposed neural distinguisher on a 4-round reduced GIFT-64 cipher, achieving 97% accuracy. This suggests that the proposed neural distinguisher exhibits strong generalization capabilities for lightweight ciphers, which is consistent with the findings of other studies, such as 29] and [31 .


## Key recovery attack based on the neural distinguisher

The key recovery attack on 11-round Speck32/64 is proposed in 11 , which combines the 2-round classical differential (0x0211,0x0a04) → (0x0040,0x0000) with the 7-round and 6-round neural distinguishers. Since there is no key addition operation before the first nonlinear operation in Speck 32/64, this method can be extended to 10 rounds for the 7-round distinguisher. All the 10-round ciphertext pairs (x10, x * 10 ) i are obtained by decrypting (x11, x * 11 ) i with all possible keys k10,j, where j ∈ {1,2, • • • , 2 16 -1}. All (x10, x * 10 ) i are input into the 7-round distinguisher to obtain a score S k 10,j for each possible key, as defined as formula (8):

where N is the number of the ciphertext pairs, Z k 10,j i is the score of k10,j used to decrypt the ciphertext pair (x11, x * 11 ) i . When S k 10,j exceeds the threshold Ci, k10,j is returned as a candidate key. The same operation is applied to obtain k9,j. Since this method is probabilistic, it may not return the correct keys when only one round of trial decryption is performed. Bayesian optimization is used to reduce the number of trial decryptions and improve the probability of finding the correct keys. Additionally, the upper confidence bound (UCB) is employed to prioritize the ciphertext structures with the highest scores during the last-key search process, thus reducing the time spent searching for less promising ciphertext structures. It can be calculated by formula (9):

Here, w i max is the highest distinguisher score obtained so far for the i-th ciphertext structure, nsi is the number of previous iterations in which the i-th ciphertext structure has been selected, j is the number of the current iteration, and α = √ N , where N is the total number of ciphertext structure available.


## Key recovery test for speck 32/64

In this work, the key recovery attack is implemented through the following four steps:

Step 1: Generate the incorrect key response profile for our neural distinguisher ND1 by encrypting 3000 plaintext pairs (x0, x * 0 ) for each key difference δ ∈ {1,2, • • • , 2 16 -1} over 11 rounds to obtain the ciphertext pairs (x11, x * 11 ).


## Step 2: Decrypt the ciphertext pairs using E -1 k+δ (x 11

) and E -1 k+δ (x * 11 ), then distinguish them using the proposed ND1 to compute the empirical mean µ δ and standard deviation σ δ of these trials. Here, k is the final subkey of each encryption operation.


## ND Accuracy Round 9 Round 10 Round 11

ND of [20] 82.27% 61.09% × MRMSP [33] 96.30% 78.72% 56.16% MRMSD [33] 99.08% 83.02% 60.81% TRMSCPDKD*/ ND1 (Ours) 99.4% 84.85% 61.25% Step 3: Randomly select 100 plaintext pairs with an input difference of (0x11, 0xa04) and decrypt them using all-zero key. Then, extend each of these by modifying the neutral bits {20,21,22,14,15,23} to create 64 plaintext pairs, and calculate the 11-round ciphertext pairs (x11, x 1 and 6-round distinguisher ND 6 1 , respectively. We set N ucb = 500 , N kc = 5, N = 100, m = 64, and n k = 32. The key recovery attack test is implemented 1000 times and divided in to 10 groups. The results are shown in Table 10 .

From Table 10 , we can see that the total number of successful key recoveries in our attack reaches 618, resulting in a success rate of 61.8%. This is 9.7% higher than the success rate reported in 10 . The success rate can be further improved by increasing the number of neutral bits. In this experiment, the neutral bits were chosen solely to enable a fair comparison with 10 . The computational complexity of the key recovery attack consists of two rounds of key recovery operations. The (i -1)-th round of key recovery is performed only when the score of the guessed key in the i-th round of key recovery exceeds the predefined threshold. Consequently, it is difficult to precisely estimate the computational complexity of the (i -1)-th round of key recovery. The computational . Suppose the predicted score is improved to 0.513, then we obtain w k ′ = 4.8024. For the 7 round-reduced Speck 32/64, if w i,ka is improved from 0.788 to 0.7904, the total score w k increases from 121.2244 to 122.5564. The larger the w k , the higher the success rate of the key recovery attack. Therefore, improving the accuracy of the neural distinguisher can significantly enhance the success rate of the key recovery attack.

Additionally, we used the method described in 11 to train an 8-round distinguisher for Speck32/64. During the training process, we first utilized 10 7 ciphertext pairs (x5, x * 5 ) of 5-round Speck32/64 with an input difference of (0x8000,0x840a) to retrain the 7-round distinguisher ND 7 1 for 10 epochs with a batch size of 500 and a learning rate of 10 -4 . Here, (0x8000,0x840a) is the most likely difference to appear three rounds after the input difference (0x4000,0x0000). Subsequently, we train the distinguisher ND 8 1 using 2 × 10 7 ciphertext pairs (x8, x * 8 ) of 8-round Speck32/64 with an input difference of (0x4000,0x0000) for 10 epochs with a batch size of 10,000 and a learning rate of 10 -4 . Finally, we retrain the distinguisher ND 8 1 using another 2 × 10 7 ciphertext pairs (x8, x * 8 ), this time with a reduced learning rate of 10 -5 . The accuracy of the new distinguisher ND 8 1 is test, yielding a result of 51.38%. Base on the distinguishers ND 8 1 and ND 7 1 , we implement the same key recovery attack for 13-round Speck32/64 with neutral bits {20,13,22, {12,19} , {14,21} , {6,29} , 30, {0,8, 31} , {5,28} , {15,24} , {6,11,12,18} , {4,27,29}, } and number of ciphertext structures of N = 2 11 . Each ciphertext structure consists of 2 12 ciphertext pairs. The key recovery attack is only tested 20 times and the result is shown in Table 11 .

From Table 11 , we can see that the success rate of the key recovery attack against the 13-round reduced Speck32/64 using the proposed neural distinguisher is 65%. In contrast, this attack cannot be implemented by the methods described in 10, 20, 33 . Therefore, the proposed neural distinguisher demonstrates significant advantages in key recovery attacks.


## Conclusion

To improve the accuracy of the neural distinguisher based on deep learning, we explore neural distinguishers using different convolutional block models. A neural distinguisher based on dense residual connections and multiple convolutional layers is proposed. The convolutional block module with parallel convolutional layers and an initial convolutional module using multi-scale convolutional kernel sizes are designed to validate the efficiency of the proposed neural distinguisher. The experiments show that adding incremental convolutional layers and adjusting the convolutional kernel sizes within and between the residual blocks (with a step of 2) can significantly improve accuracy. However, the initial convolutional module using multi-scale convolutional kernel sizes does not improve accuracy. Additionally, we constructed two new datasets, which suggest that the combination of ciphertext pairs, decryption keys, and the differences between ciphertext pairs from different decryption rounds can significantly improve the accuracy of the neural distinguisher. The key recovery attack results show that the proposed neural distinguisher has a significant advantage.

Although the proposed neural distinguisher using 256 ciphertext pairs achieves higher accuracy, it cannot yet be used to recover the key directly. The reason is that, to ensure the generated correct ciphertext structure follows the same distribution for the two rounds of differential paths (0x211,0xa04) → (0x40,0), log 2 256 = 8 neutral bits are required to extend a ciphertext pair structure. However, there are only 12 neutral and probabilistic neutral bits available, which can generate only 16 ciphertext pair structures, significantly reducing the success rate of the key recovery attack. This issue will be the focus of future work. Finding more neutral and probabilistic neutral bits may help mitigate this problem.

Sequence number of key recoveries 1 2 3 4 5 6 7 8 9 10 Result Y Y N Y N Y N N Y Y Number of used iterations 7956 7778 8192 1203 8192 8192 8192 8192 2490 1755 Sequence number of key recoveries 11 12 13 14 15 16 17 18 19 20 Result Y N Y Y Y Y N N Y Y Number of used iterations 1722 8192 4165 648 6177 8192 8192 8192 1689 692

Table 11. The key recovery attack against 13-round Speck32/64. Scientific Reports | 2025 15:13696

> 2 Fig. 2 . Fig. 2. The round function of Simon cipher.

> 1 Fig. 1 . Fig. 1. The round function and key schedule algorithm of Speck 32/64.

> 3 Fig. 3 . Fig.3. The structure of Gohr's neural network.

> 5 Fig. 5 . Fig. 5. The structure of the convolutional block model with parallel convolutional blocks.

> 4 Fig. 4 . Fig. 4. The network structure of the proposed neural distinguisher.

> 6 Fig. 6 . Fig.6. The structure of the initial convolutional model with multi-scale layers.

> 5 The number of the convolutional layers of the residual block equals to 5 The

> 5 Round ND Accuracy 5 ND1 with N CK = (3,5, 7,9)93.29%ND2 with N CK = (3,5, 7,9) 93.38% ND1 with N CK = (1,3, 5,7, 9) 93.35% ND2 with N CK = (1,3, 5,7, 9)

> 9 Fig. 9 . Fig. 9. The data set structure of DRMSCPDK.

> 8 Fig. 8 . Fig. 8. The data set structure of MRMSCPD.

> 7 Fig. 7 . Fig. 7. The data set structure of MRMSCPK.

> 12 Fig. 12 . Fig. 12. The data set structure of TRMSCPDAK*.

> 11 Fig. 11 . Fig. 11. The data set structure of DRMSCPDK*.

> 10 Fig. 10 . Fig. 10. The data set structure of TRMSCPD.

> 111 * 11 )Algorithm 1 . i of each. Step 4: Use UCB method and the optimized Bayesian approach to recover the key of Speck 32/64. The details of the key recovery process for the 11-round case are shown in Algorithm 1: Key recovery process. In Algorithm 1, the variable N ucb denotes the iteration number of the UCB, N kc denotes the iteration number of the Bayesian-based key search, n k denotes the number of candidate keys, and c1 denotes the threshold of the key's score. The function E -1 ka (Xi) denotes the decryption of the ciphertext pair Ci by key ka , and ND (P i,ka ) denotes distinguishing the plaintext pair P i,ka using the neural distinguisher. In this work, we use the 7-round distinguisher ND

> 7 7

> 10 Group 1 2 3 4 5 6 7 8 9 10 Number of successes 68 63 64 63 64 64 55 59 59 59

> 1 Table 1 . The

> 5 Table 5 . The accuracy of the ND1 with different ablation experiments

> 4 Table 4 . Comparison of the efficiency of the proposed neural distinguishers.

> 8 Table 8 . The accuracy of different neural distinguishers using different numbers of ciphertext pairs for speck 32/64.

> 7 Table 7 . Comparison of the accuracy of different neural distinguisher for speck 32/64.

> 9 Table 9 . Comparison of the accuracy of different neural distinguisher for Simon 32/64.

> 10 Table 10 . The key recovery attack against 11-round Speck32/64. complexity of the i-th round of key recovery is approximately O (N ucb * N kc * n k * O( ND ( ) )). Thus, the primary difference between the proposed method and Gohr's method lies in the inference complexity of the neural distinguisher. The execution time of a single attack was tested, showing that the proposed scheme requires 1500 s, whereas the method in 10 takes 500 s. Although the proposed key recovery attack requires more time, it remains acceptable and offers a significant advantage in terms of success rate.Furthermore, we analyze the impact of ND1's accuracy on the success rate of the key recovery attack. As shown in Algorithm 1, scoring the decrypted ciphertextE -1 ka (Xi)is the core operation in key recovery. The score for each possible key is defined in formula(8), where each key's score is obtained using ND1. For example, in the 11 round-reduced Speck 32/64, if ND1 outputs a predicted score 0.512 for all 64 ciphertext pairs with a fixed input difference, its final score is w i,ka = log 2

## Acknowledgements

This work was supported by the following projects and foundations: 2024 Shaanxi Province key research and development plan project (No. 2024GX-ZDCYL-01-13 ), the Special Funds for Basic scientific Research of the

## References

1. b0: M Baritha Begum, N R Nagarajan, P Rajalakshmi. "Dynamic network security leveraging efficient CoviNet with granger causality-inspired graph neural networks for data compression in cloud IoT Devices". Knowledge-Based Systems. 2025-01. DOI: 10.1016/j.knosys.2024.112859
2. b1: M Baritha Begum, B Suganthi, P Sivagamasundhari, S A Arunmozhi, S J Muhamed Suhail. "An Enhanced Heterogeneous Local Directed Acyclic Graph Blockchain With Recalling Enhanced Recurrent Neural Networks for Routing in Secure MANET‐IOT Environments in 6G". International Journal of Communication Systems. 2025-01-23. DOI: 10.1002/dac.6110
3. b2: M Baritha Begum, Karthikeyan Kaliyaperumal. "Integration of BWT scrambling and data compression in an innovative system enhances protection and versatile management of sensor feeds (SEC)". Heliyon. 2024-10. DOI: 10.1016/j.heliyon.2024.e39254
4. b3: M B Begum. Review of Marochov et al.: Image Classification of Marine-Terminating Outlet Glaciers using Deep Learning Methods. 2020-12-22. DOI: 10.5194/tc-2020-310-rc3
5. b4: M Baritha Begum, G Sivakannu, J Eindhumathy, J Sangeetha Priya, M Mahendran, R Ranjith Kumar. "Enhancing Agricultural Productivity with Data-Driven Crop Recommendations". 2023 Second International Conference on Augmented Intelligence and Sustainable Systems (ICAISS). 2023-08-23. DOI: 10.1109/icaiss58487.2023.10250657
6. b5: Yanfeng Wang, Pengke Su, Zicheng Wang, Junwei Sun. "FN-HNN Coupled With Tunable Multistable Memristors and Encryption by Arnold Mapping and Diagonal Diffusion Algorithm". IEEE Transactions on Circuits and Systems I: Regular Papers. 2024. DOI: 10.1109/tcsi.2024.3516722
7. b6: Gang Dou, Wenhai Guo, Lingtong Kong, Junwei Sun, Mei Guo, Shiping Wen. "Operant Conditioning Neuromorphic Circuit With Addictiveness and Time Memory for Automatic Learning". IEEE Transactions on Biomedical Circuits and Systems. 2024-10. DOI: 10.1109/tbcas.2024.3388673
8. b7: Junwei Sun, Yuhan Cao, Yi Yue, Shiping Wen, Yanfeng Wang. "Memristor-Based Parallel Computing Circuit Optimization for LSTM Network Fault Diagnosis". IEEE Transactions on Circuits and Systems I: Regular Papers. 2024. DOI: 10.1109/tcsi.2024.3516325
9. b8: Hongjian Xia, Yi Zhang, Minyou Chen, Dan Luo, Wei Lai, Huai Wang. "Capacitor Parameter Estimation Based on Wavelet Transform and Convolution Neural Network". IEEE Transactions on Power Electronics. 2024-11. DOI: 10.1109/tpel.2024.3409534
10. b9: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
11. b10: Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks, Louis Wingers. "The SIMON and SPECK lightweight block ciphers". Proceedings of the 52nd Annual Design Automation Conference. 2015-06-07. DOI: 10.1145/2744769.2747946
12. b11: Adrien Benamira, David Gerault, Thomas Peyrin, Quan Quan Tan. "A Deeper Look at Machine Learning-Based Cryptanalysis". Lecture Notes in Computer Science. 2021. DOI: 10.1007/978-3-030-77870-5_28
13. b12: Emanuele Bellini, Matteo Rossi. "Performance Comparison Between Deep Learning-Based and Conventional Cryptographic Distinguishers". Lecture Notes in Networks and Systems. 2021. DOI: 10.1007/978-3-030-80129-8_48
14. b13: W Tian, B Hu. "Deep Learning Assisted Differential Cryptanalysis for the Lightweight Cipher SIMON". KSII Transactions on Internet and Information Systems. 2021-02-28. DOI: 10.3837/tiis.2021.02.012
15. b14: Z Hou, J Ren, S Chen. "Improve Neural Distinguisher for Cryptanalysis". Cryptology ePrint Archive. 2021
16. b15: Z Hou, J Ren, S Chen. "Cryptanalysis of Round-Reduced SIMON32 Based on Deep Learning". Cryptology ePrint Archive. 2021
17. b16: Heng-Chuan Su, Xuan-Yong Zhu, Duan Ming. "Polytopic Attack on Round-Reduced Simon32/64 Using Deep Learning". Lecture Notes in Computer Science. 2020. DOI: 10.1007/978-3-030-71852-7_1
18. b17: Gao Wang, Gaoli Wang, Yu He. "Improved Machine Learning Assisted (Related-key) Differential Distinguishers For Lightweight Ciphers". 2021 IEEE 20th International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom). 2021-10. DOI: 10.1109/trustcom53373.2021.00039
19. b18: Runlian Zhang, Mi Zhang, Jiaxu Yan, Yixing Li, Xiaonian Wu, Lingchen Li. "Differential Cryptanalysis of TweGIFT-128 Based on Neural Network". 2021 IEEE Sixth International Conference on Data Science in Cyberspace (DSC). 2021-10. DOI: 10.1109/dsc53577.2021.00084
20. b19: Lijun Lyu, Yi Tu, Yingjie Zhang. "Improving the Deep-Learning-Based Differential Distinguisher and Applications to Simeck". 2022 IEEE 25th International Conference on Computer Supported Cooperative Work in Design (CSCWD). 2022-05-04. DOI: 10.1109/cscwd54268.2022.9776036
21. b20: Reshma Rajan, Rupam Kumar Roy, Diptakshi Sen, Girish Mishra. "Deep Learning-Based Differential Distinguisher for Lightweight Cipher GIFT-COFB". Algorithms for Intelligent Systems. 2022. DOI: 10.1007/978-981-16-9650-3_31
22. b21: Girish Mishra, S K Pal, S V S S N V G Krishna Murthy, Ishan Prakash, Anshul Kumar. "Deep Learning-Based Differential Distinguisher for Lightweight Ciphers GIFT-64 and PRIDE". Algorithms for Intelligent Systems. 2022. DOI: 10.1007/978-981-16-9650-3_19
23. b22: Anubhab Baksi, Anubhab Baksi. "Machine Learning-Assisted Differential Distinguishers for Lightweight Ciphers". Computer Architecture and Design Methodologies. 2022. DOI: 10.1007/978-981-16-6522-6_6
24. b23: Zhenzhen Bao, Jian Guo, Meicheng Liu, Li Ma, Yi Tu. "Enhancing Differential-Neural Cryptanalysis". Lecture Notes in Computer Science. 2022. DOI: 10.1007/978-3-031-22963-3_11
25. b24: Liu Zhang, Zilong Wang, Yindong Chen. "Improving the Accuracy of Differential-Neural Distinguisher for DES, Chaskey, and PRESENT". IEICE Transactions on Information and Systems. 2022. DOI: 10.1587/transinf.2022edl8094
26. b25: Yi Chen, Yantian Shen, Hongbo Yu, Sitong Yuan. "A New Neural Distinguisher Considering Features Derived From Multiple Ciphertext Pairs". The Computer Journal. 2021. DOI: 10.1093/comjnl/bxac019
27. b26: Yi Chen, Yantian Shen, Hongbo Yu. "Neural-Aided Statistical Attack for Cryptanalysis". The Computer Journal. 2023. DOI: 10.1093/comjnl/bxac099
28. b27: Liu Zhang, Zilong Wang, Baocang Wang. "Improving Differential-Neural Cryptanalysis". IACR Communications in Cryptology. 2022. DOI: 10.62056/ay11wa3y6
29. b28: Yi Chen, Yantian Shen, Hongbo Yu, Sitong Yuan. "A New Neural Distinguisher Considering Features Derived From Multiple Ciphertext Pairs". The Computer Journal. 2023. DOI: 10.1093/comjnl/bxac019
30. b29: A Gohr, G Leander, P Neumann. "Figure 5: The framework of basic and enhanced related-key differential neural distinguishers.". Cryptology ePrint Archive. 2022. DOI: 10.7717/peerj-cs.2566/fig-5
31. b30: Zezhou Hou, Jiongjiong Ren, Shaozhen Chen. "Practical Attacks of Round-Reduced SIMON Based on Deep Learning". The Computer Journal. 2023. DOI: 10.1093/comjnl/bxac102
32. b31: Zhenzhen Bao, Jinyu Lu, Yiran Yao, Liu Zhang. "More Insight on Deep Learning-Aided Cryptanalysis". Lecture Notes in Computer Science. 2023. DOI: 10.1007/978-981-99-8727-6_15
33. b32: Jiashuo Liu, Jiongjiong Ren, Shaozhen Chen, Manman Li. "Improved neural distinguishers with multi-round and multi-splicing construction". Journal of Information Security and Applications. 2023-05. DOI: 10.1016/j.jisa.2023.103461
34. b33: Jinyu Lu, Guoqiang Liu, Bing Sun, Chao Li, Li Liu. "Improved (Related-Key) Differential-Based Neural Distinguishers for SIMON and SIMECK Block Ciphers". The Computer Journal. 2024. DOI: 10.1093/comjnl/bxac195
35. b34: Byoungjin Seok, Changhoon Lee. "A Novel Approach to Construct a Good Dataset for Differential-Neural Cryptanalysis". IEEE Transactions on Dependable and Secure Computing. 2024. DOI: 10.1109/tdsc.2024.3387662
36. b35: Gao Wang, Gaoli Wang, Siwei Sun. "Investigating and Enhancing the Neural Distinguisher for Differential Cryptanalysis". IEICE Transactions on Information and Systems. 2024-08-01. DOI: 10.1587/transinf.2024edp7011
37. b36: Gao Huang, Zhuang Liu, Laurens Van Der Maaten, Kilian Q Weinberger. "Densely Connected Convolutional Networks". 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2017-07. DOI: 10.1109/cvpr.2017.243
38. b37: F Chollet. 2015
