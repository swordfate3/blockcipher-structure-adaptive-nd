# Enhanced related-key differential neural distinguishers for <tt>SIMON</tt> and <tt>SIMECK</tt> block ciphers

**Authors:** Gao Wang, Gaoli Wang

**Source PDF:** `2024_enhanced_related_key_simon_simeck.pdf`

## Abstract

At CRYPTO 2019, Gohr pioneered the application of deep learning to differential cryptanalysis and successfully attacked the 11-round NSA block cipher Speck32/64 with a 7-round and an 8-round single-key differential neural distinguisher. Subsequently, Lu et al. ( DOI 10.1093/comjnl/bxac195 ) presented the improved related-key differential neural distinguishers against the SIMON and SIMECK. Following this work, we provide a framework to construct the enhanced related-key differential neural distinguisher for SIMON and SIMECK. In order to select input differences efficiently, we introduce a method that leverages weighted bias scores to approximate the suitability of various input differences. Building on the principles of the basic related-key differential neural distinguisher, we further propose an improved scheme to construct the enhanced related-key differential neural distinguisher by utilizing two input differences, and obtain superior accuracy than Lu et al. for both SIMON and SIMECK. Specifically, our meticulous selection of input differences yields significant accuracy improvements of 3% and 1.9% for the 12round and 13-round basic related-key differential neural distinguishers of SIMON32/ 64. Moreover, our enhanced related-key differential neural distinguishers surpass the basic related-key differential neural distinguishers. For 13-round SIMON32/64, 13round SIMON48/96, and 14-round SIMON64/128, the accuracy of their related-key differential neural distinguishers increases from 0.545, 0.650, and 0.580 to 0.567, 0.696, and 0.618, respectively. For 15-round SIMECK32/64, 19-round SIMECK48/96, and 22-round SIMECK64/128, the accuracy of their neural distinguishers is improved from 0.547, 0.516, and 0.519 to 0.568, 0.523, and 0.526, respectively.

## INTRODUCTION

In recent years, with the wide application of wireless sensor networks (WSN) and radio frequency identification (RFID) technology in various industries, the data security problem of these resource-constrained devices have become more and more prominent. As a cryptographic solution that can achieve a good balance between security and performance under limited resources, lightweight block ciphers are widely used to protect data security in various resource-constrained devices. The security of block ciphers is closely related to the security of data. In this context, evaluating the security properties of these ciphers has become a popular research topic in the field of computer science and cryptography. Among many cryptanalysis techniques, differential cryptanalysis, proposed by Biham & Shamir (1991b) , is one of the most commonly used methods for evaluating the security of block ciphers. This technique focuses on the propagation of plaintext differences during the encryption.

In traditional differential cryptanalysis, the core task of differential cryptanalysis is to find a differential characteristic with high probability. Initially, this task was achieved by manual derivation, which required a lot of effort and time. At EUROCRYPT 1994 , Matsui (1994) presented a branch-and-bound method for this task, which replaced manual derivation with automated search techniques for the first time. However, for the block ciphers with large sizes, this method is insufficient to provide useful differential characteristics. This prompts cryptographers to adopt more efficient automated search tools for searching the differential characteristic with high probability, including mixed integer linear programming (MILP) (Sun et al., 2014; Bellini et al., 2023a; Mouha et al., 2012) , constraint programming (CP) (Gerault, Minier & Solnon, 2016; Sun et al., 2017) , and Boolean satisfiability problem or satisfiability modulo theories (SAT/SMT) (Sun et al., 2017; Lafitte, 2018) .

In recent years, with the rapid development of deep learning, cryptanalysts have begun to explore how to harness its power for differential cryptanalysis. At CRYPTO 2019, Gohr (2019) constructed an 8-round differential neural distinguishers by leveraging neural networks to learn the differential properties of block ciphers SPECK32/64 and successfully carried out an 11-round key recovery attack. This pioneering research significantly accelerated the integration of deep learning and differential cryptanalysis. Since this study, the differential neural distinguisher has been widely applied to various block ciphers in single-key and related-key scenarios, including but not limited to SIMON (Bao et al., 2022; Lu et al., 2024; Bellini et al., 2023b) , SIMECK (Zhang et al., 2023; Lu et al., 2024) , PRESENT (Jain, Kohli & Mishra, 2020; Bellini et al., 2023b; Zhang, Wang & Chen, 2023) , GIFT (Shen et al., 2024) , ASCON (Shen et al., 2024) , and others. In most of these works, the focus is only on the single-key neural distinguishers, while SIMON and SIMECK also focus on the relatedkey differential neural distinguishers. In this article, we continue to optimize the relatedkey differential neural distinguishers for SIMON and SIMECK.

So far, there are many studies exploring the differential neural distinguishers for SIMON and SIMECK ciphers, such as Bao et al. (2022) , Zhang et al. (2023) , Wang et al. (2022) , Seong et al. (2022) , Gohr, Leander & Neumann (2022) , Lyu, Tu & Zhang (2022) , Lu et al. (2024) . However, most of them focused on the single-key scenario, until the research of Lu et al. (2024) broke this trend. They not only improved the accuracy of their single-key differential neural distinguishers by using the enhanced data format ðD r L ; D r R ; C l ; C r ; C 0 l ; C 0 r ; D rÀ1 R ; pD rÀ2 R Þ (defined in Eq. ( 10 )), but also constructed the related-key differential neural distinguishers for them. The experimental results show that the related-key differential neural distinguishers outperforms the single-key differential neural distinguishers in terms of the number of analyzed rounds and accuracy. In the single-key scenario, Lu et al. (2024) exhaustively evaluated the input differences with Hamming weights of 1, 2, and 3 by training a differential neural distinguisher for each difference. However, for the related-key scenario, this task has not been explored in depth due to the huge number of input differences that need to be evaluated. Even for the smallest variants SIMON32/64 and SIMECK32/64, the number of input differences with Hamming weights of 1, 2, and 3 already reaches about 200 million. Therefore, it is impractical to train a neural distinguisher for each difference. In this article, we aim to further address this challenge.


## Our contributions

In this article, we first present a framework to construct the basic related-key differential neural distinguishers for SIMON and SIMECK. This framework is comprised of five components: differences selection, sample generation, network architecture, distinguisher training, and distinguisher evaluation. For comparison with the baseline work of Lu et al. (2024) , we keep sample generation, network architecture, distinguisher training, and distinguisher evaluation as in Lu et al. (2024) . Our attention is mainly on differences selection. We provide a method for approximately assessing the suitability of different input differences with weighted bias scores instead of training a neural distinguisher for every input difference as Lu et al. (2024) . This allows us to approximate the applicability of the different differences without training the model, which can significantly accelerates the process of differences selection. Our meticulous selection of the input difference can make the accuracy of the basic related-key differential neural distinguisher match or surpass previous results. In particular, the accuracy for the 12-round and 13-round distinguishers of SIMON32/64 is improved from 0.648 and 0.526 to 0.678 and 0.545, respectively, as shown in Table 1 .

Furthermore, based on the principles of the basic related-key differential neural distinguishers, we propose an enhanced scheme that harnesses two distinct input differences to construct a more powerful related-key differential neural distinguisher for SIMON and SIMECK instead of using only one difference in the phase of sample generation.

Specifically, for the 13-round SIMON32/64, 13-round SIMON48/96, and 14-round SIMON64/128, their accuracy is raised from 0.545, 0.650, and 0.580 to 0.567, 0.696, and 0.618, respectively. Similarly, the neural distinguishers for 15-round SIMECK32/64, 19round SIMECK48/96, and 22-round SIMECK64/128 also showed significant improvements in accuracy, rising from 0.547, 0.516, and 0.519 to 0.568, 0.523, and 0.526, respectively. All these results illustrate the effectiveness and robustness of our scheme.

Organization "Preliminaries" commences by introducing the foundational knowledge about the relatedkey differential neural distinguisher. Following this, "The Framework for Developing Related-Key Differential Neural Distinguishers to SIMON and SIMECK" comprehensively explores the construction of basic and enhanced neural distinguishers for SIMON and SIMECK. Building upon this framework, "Related-Key Differential Neural Distinguishers for Round Reduced SIMON and SIMECK" constructs the improved related-key differential neural distinguishers for SIMON and SIMECK. Finally, "Conclusions and Future Work" concludes this article.


## PRELIMINARIES

In this section, we first present the pivotal notations in Table 2 . Following this, we offer a succinct overview of the block ciphers SIMON and SIMECK, along with the basic concepts about related-key differential cryptanalysis and convolutional neural networks.


## Notations

Table 2 illustrates the notations utilized in this article.

A brief description of SIMON and SIMECK ciphers SIMON (Beaulieu et al., 2015) is a lightweight block cipher, designed by the National Security Agency (NSA) in 2013. It employs a Feistel structure, making it suitable for resource-constrained environments. In addition, it supports various block lengths and key Table 2 Notations. Notation Description <<<; >>> Circular left and right shift a; b; c Bits of cyclic shift C; Z j Predefined constants T Temporary variable È; Bit-wise XOR and AND operation jj Concatenation F 2 Binary field P; P 0 Plaintext C; C 0 Ciphertext K; K 0 Master key E, R Encryption algorithm and rounds P i ; K i ; C i Plaintext, key and ciphertext for round i t 2 ; t 1 ; t 0 ; k 0 Components of the K DP Plaintext difference DC Ciphertext difference DK Master key difference DP r The r-round input difference DC r The r-round ciphertext difference DK r The r-round key difference r Activation function x i Input of the i-th neuron w i Weight of the x i b Bias of the neuron F tr The transformation operation of SENet F sq ðÁÞ The squeeze operation of SENet F ex ðÁ; WÞ The excitation operation of SENet F scale ðÁ; ÁÞ The channel-wise multiplication of SENet b r Bias scores for r rounds bt r Approximate bias score calculated using t samples for r rounds S R R-rounds weighted bias score i i-th (1 i 8) ciphertext pair l i Cyclic learning rate for the i-th epoch a; b; n The parameter for calculating l i , defaulting to 0.0001, 0.003 and 29, respectively c The parameter for L2 regularization, default 0.00001 bl; kl block length and key length

where a, b and c represent the fixed rotation constants that are utilized in the circular left shift operation. For SIMON, the values of these constants are set to 1, 8, and 2, respectively. Given a master key K that comprises four key words, denoted as K ¼ ðK 3 ; …; K 1 ; K 0 Þ, the round key K rÀ1 is generated through a linear key schedule. This process incorporates predefined constants C and a series of constants ðZ j Þ i , the generation follows the scheme outlined below:

SIMON is designed to be highly efficient in terms of both hardware and software implementations. It processes the plaintext and ciphertext blocks in a symmetric manner. Its structure and the choice of operations contribute to its resistance against common attacks like differential cryptanalysis and linear cryptanalysis. Like many lightweight block ciphers, SIMON's simplicity may make it more susceptible to side-channel attacks, such as power analysis and timing attacks.

The SIMECK (Yang et al., 2015) cipher, presented at CHES in 2015, is a variant of the SIMON. It retains the same Feistel structure and round function as SIMON, but distinguishes itself through the values of a, b, and c, which are set to 0, 5, and 1, respectively. In addition, SIMECK uses the round function to generate the round keys K r for a given master key K ¼ ðt 2 ; t 1 ; t 0 ; k 0 Þ, as explained below:

(3) where C and ðZ j Þ i are the predefined constants. For more details, please refer to Yang et al. (2015) . SIMECK is a lightweight block cipher designed specifically for constrained environments. It boasts compact hardware implementations and low power consumption, making it suitable for embedded systems and IoT devices. SIMECK has fixed block size and key length, which facilitate consistent and predictable performance. SIMECK stands out for its efficiency in terms of both area and energy, as well as its resistance to common cryptographic attacks. However, it is worth noting that careful implementation is crucial to mitigate potential side-channel attack.


## Related-key differential cryptanalysis

In 1990, Biham & Shamir (1991b) introduced a groundbreaking attack strategy called differential cryptanalysis. This cryptanalysis technique can distinguish the block cipher from the random permutation by studying the propagation properties of the plaintext difference DP throughout the encryption. Due to its simple principle and excellent efficacy, this approach quickly attracted significant attention among the cryptography community (Biham & Shamir, 1991a , 1992; Biham & Dunkelman, 2007) .

In lightweight block ciphers, the key schedule holds paramount importance, as it is responsible for generating and updating the round keys. To delve into the security of this vital component, Biham (1994) proposed a pioneering related-key cryptanalysis method in 1994, which studies the security of block cipher under different keys. The related-key differential cryptanalysis method combines the principles of differential cryptanalysis and related-key cryptanalysis. It investigates differential propagation under different keys instead of the same key. The basic concepts related to block cipher and related-key differential cryptanalysis are summarized as follows.

Assuming E is the r-round encryption procedure employed by a block cipher with the block length bl and the key length kl, and the plaintext, ciphertext, and master key are denoted as P, C, and K, respectively. The formalized encryption process of this block cipher can be expressed as C ¼ E K ðPÞ, which indicates that the ciphertext C results from encrypting the plaintext P for r rounds using the master key K. For iterative block ciphers, their encryption process E K ðPÞ is derived by repeatedly applying the round function FðK i ; P i Þ, where K i represents the round key for the i-th iteration, whereas P i denotes the input to this iteration. Consequently, the encryption process of iterative block cipher is given in Eq. ( 4 ).

Definition 1 (Plaintext Difference, Ciphertext Difference, and Key Difference. Matsui (1994) ) For a block cipher, the plaintext difference DP of the plaintext pair ðP;

Similarly, the ciphertext difference DC of the ciphertext pair ðC; C 0 Þ is C È C 0 , and the key difference DK of the key pair ðK;

Given a plaintext pair (P; P 0 ) and a key pair (K; K 0 ) with the difference of DP and DK, let (C i ; C i 0 ) be the cipher pair obtained by encrypting the (P; P 0 ) with (K; K 0 ) for i rounds, the r-round related-key differential characteristic of the block cipher is (DP; DC 1 ; ……; DC rÀ1 ; DC r ), where

Definition 3 (Related-key Differential Probability. Jakimoski & Desmedt ( 2003 )) The related-key differential probability DPðDP; DK; DCÞ of the block cipher with the plaintext difference DP, master key difference DK, and ciphertext difference DC is

where x 2 F P j j 2 and k 2 F

2 , the hamming weight of is the number of non-zero bits within its binary representation. Mathematically, it can be formulated as P n i¼1 X i , where X i denotes the i-th bit in the binary of X.


## Convolutional neural network

Convolutional Neural Network (CNN), as a feed-forward neural network with convolutional structure, has been widely applied in numerous domains, including but not limited to image recognition (Chauhan, Ghanshala & Joshi, 2018) , video analysis (Ullah et al., 2017) , and natural language processing (Yin et al., 2017) , and among others. A convolutional neural network usually consists of the input layer, convolutional layer, pooling layer, fully connected layer, and output layer. The convolutional layer is used to extract features, the pooling layer is used to achieve data dimensionality reduction through subsampling, the fully connected layer integrates the previously extracted features for tasks such as classification or regression, and the output layer is responsible for producing the final results.

LeNet-5 is a convolutional neural network designed by LeCun et al. (1998) for handwritten digit recognition, and it is one of the most representative results of the early convolutional neural network. It consists of one input layer, one output layer, two convolutional layers, two pooling layers, and two fully connected layers, as shown in Fig. 2 . Its input is a image of 32 Â 32. After two convolution and subsampling operations, this input becomes a feature map of 16 Â 5 Â 5. The convolution kernels are all 5 Â 5 with stride 1. The subsampling function used for the pooling layers is maxpooling. Then it passes through two fully connected layers with sizes of 120 and 64 to reach the output layer.

Later, based on LeNet-5, many improved convolutional neural networks have been proposed, such as AlexNet (Krizhevsky, Sutskever & Hinton, 2017) , GoogleLeNet (Szegedy et al., 2015) , ResNet (He et al., 2016) , and so on. The main components used in this article are convolutional layers, activation functions, fully connected layers, as well as the advanced architectures including the Residual Network (ResNet) (He et al., 2016) and the Squeeze-and-Excitation Network (SENet) (Hu, Shen & Sun, 2018) .


## Convolution layer

Convolutional layers are the core component of convolutional neural networks. It is responsible for extracting features from input data through convolution operations. In a convolution operations, a convolutional kernel (also known as a filter) continuously slides over the input feature map. At each step, it calculates the sum of the product of the values at each position and takes it as the value in the corresponding position on the output feature map.


## Activation function

In neural networks and deep learning, the activation function plays a crucial role in introducing nonlinear properties that enable the neural network to learn complex patterns in the data. The activation functions Sigmoid (Little, 1974) and rectified linear unit (ReLU) (Nair & Hinton, 2010) are used in this article. The Sigmoid function can map any real value to an output between 0 and 1. Therefore, it is a common choice for the output layer in binary classification problems. The ReLU function returns the input value itself for the positive inputs and zero for the negative inputs. It performs well in many deep learning tasks because of its effectiveness in mitigating the gradient vanishing problem. Their mathematical formulations are as follows:

Fully connected layer

The fully connected layer (also known as dense layer) is a fundamental element of neural networks. In this layer, every neuron establishes a connection to each neuron in the preceding layer. This connection ensures that all the outputs from the previous layer are the inputs to every neuron in the current layer. This structure allows the fully connected layer to execute a weighted combination of input features, effectively capturing the intricate relationships between them. For a single neuron in the fully connected layer, its output can be represented as r P n i¼1 w i Á x i þ b À Á , where n is the total number of neurons, r represents the activation function, x i denotes the input of the i-th neuron, w i corresponds to the weight of the connection, and b is the bias of the neuron.


## Residual network

Gradient vanishing and explosion are issues in deep neural networks where gradients become extremely small or large during back-propagation, respectively, hindering effective training. The residual neural network (ResNet) (He et al., 2016) is an effective deep learning model that solves the problem of gradient vanishing and gradient explosion by introducing shortcut connections as shown in Fig. 3 . Shortcut connections can mitigate these problems by providing alternative paths for gradient flow, reducing the dependency on gradients passing through all intermediate layers and improving information flow through the network.


## Squeeze-and-excitation network (SENet)

The Squeeze-and-Excitation (SE) block (Hu, Shen & Sun, 2018 ) is a plug-and-play channel attention mechanism that can be integrated into any network, as shown in Fig. 4 . It can Full-size  DOI: 10.7717/peerj-cs.2566/fig-3

Figure 4 The squeeze-and-excitation block of SENet (Hu, Shen & Sun, 2018) .

Full-size  DOI: 10.7717/peerj-cs.2566/fig- 4 adjust the weights of each channel and improves the attention to important channels, which is particularly beneficial in deep residual architectures. In this article, the SE block is directly integrated with the residual network to form the SE-ResNet architecture. This integration allows SE-ResNet to achieve improved performance in differential cryptanalysis, by making the network more sensitive to informative features and more robust to variations in input data.


## THE FRAMEWORK FOR DEVELOPING RELATED-KEY DIFFERENTIAL NEURAL DISTINGUISHERS TO SIMON AND SIMECK

The development of related-key differential neural distinguisher consists of four steps: differences selection, sample generation, network architecture design, distinguisher training and distinguisher evaluation, as shown in Fig. 5 . In this section, we first introduce how to use a difference to construct the basic related-key differential neural distinguishers for SIMON and SIMECK from these steps. Subsequently, we introduce an advanced technique to construct the enhanced related-key differential neural distinguisher using a pair of distinct differences.


## Basic related-key differential neural distinguishers


## Differences selection

Selecting an appropriate plaintext difference DP and a master key difference DK for sample generation is a crucial step in the development of basic related-key differential neural distinguishers, since it significantly influences the features embodied within the samples.

The study of Gohr, Leander & Neumann (2022) , Bellini et al. (2023b) indicates that the differences that can yield the ciphertext differences with high bias scores b r may be more suitable for constructing neural distinguishers. In the related-key scenario, the r-round exact bias score of ciphertext difference is defined as follows.

Definition 5 (Exact bias score. Gohr, Leander & Neumann (2022) ) For a cipher primitive E : F n 2 Â F k 2 ! F n 2 , the r-round bias score b r ðDP; DKÞ of the plaintext difference DP 2 F n 2 and master key difference DK 2 F k 2 is the sum of the biases of each bit position in the resulting ciphertext differences, i.e., b r ðDP;

However, due to the immense computational demands posed by the exhaustive enumeration of all possible plaintexts and keys, computing the exact bias score is impractical. Therefore, we have to adopt more efficient methods to do this work. One promising approach is statistical sampling techniques, which is employed in Gohr, Leander & Neumann (2022) . By employing random sampling method, we could reduce the time and resources required for data collection and analysis while maintaining a high level of accuracy and reliability. By randomly selecting t samples from the plaintext and key space, we can obtain an approximate bias score e b t r ðDP; DKÞ as follow:

In addition, to mitigate the instance where certain differences have low bit bias in the initial few rounds but exhibit favorable bit bias in subsequent rounds, a practical strategy is to calculate the bias score from the initial round and adopt their weighted bias score as the final the final metric for evaluation. This approach can enhance the robustness of the differential evaluation. Specifically, the R-rounds weighted bias score S R ðDP; DKÞ for a given plaintext difference DP and master key difference DK is the sum of the product of the number of rounds and their bias score. The mathematical expression is as follows:


## Sample generation

The related-key differential neural distinguisher is a supervised binary classifier. Thus, its dataset consists of positive and negative samples, labeled as 1 and 0, respectively. The positive samples are obtained by encrypting the plaintext pairs using the key pairs that exhibit the plaintext difference DP and key difference DK. In contrast, the negative samples are derived from encrypting the random plaintext pairs using the random key pairs. Following the work of Lu et al. (2024) , we use eight ciphertext pairs with boosted data formats to train the related-key differential neural distinguishers for SIMON and SIMECK. Specifically, the i-th (1 i 8) r-round ciphertext pair ðC l ; C r ; C 0 l ; C 0 r Þ i , derived from the i-th plaintext pair ðP; P 0 Þ i and key pair ðK; K 0 Þ i , can be extended to ðD r L ; D r R ; C l ; C r ; C 0 l ; C 0 r ; D rÀ1 R ; pD rÀ2 R Þ i , denoted as i , where

The label Y of the sample ð 1 k 2 k…k s Þ can be expressed as


## Network architecture

We evaluate the various neural network architectures for the SIMON and SIMECK, such as neural network architectures used in Gohr (2019 . Input Layer: For the SIMON and SIMECK with a block length of bl, the input of neural network is a tensor with a shape of ð8 Â bl Â 4; 1Þ.

. Reshape Layer: This layer transforms the input tensor into a new shape of ð8; bl Â 8Þ to enhance the feature extraction for subsequent convolutional layers.

. Conv-1: A convolutional layer with bl convolutional kernels of size 1, followed by a batch normalization layer and a ReLU activation function.

. Dense bl Â 2: Two dense layers implemented sequentially to process the features extracted from the Conv-1. Each dense layer consists of bl neurons followed by a batch normalization layer and a ReLU activation function. . SE-ResNet Â 5: A sequence of five SE-ResNet layers. Each SE-ResNet integrates the ResNet and SENet architectures and contains two convolutional layers with 3 × 3 kernels for feature extraction, followed by a batch normalization layer, a ReLU activation function, and a Squeeze-and-Excitation module. The features from different layers are merged by Multiply and Add operations.

. Flatten: This layer flattens the multi-dimensional output from the SE-ResNet layer into a one-dimensional tensor.

. Dense-128 Â 2: Two fully connected layers with 128 neurons are used to connect all the features and send the output to the Sigmoid classifier in the subsequent layer.

. Output: The final layer of the neural network is responsible for generating the final prediction result.


## Training and evaluation

The training process of a related-key differential neural distinguisher can be divided into two phases: the offline phase and the online phase. During the offline phase, the attacker aims to train a neural network that can effectively distinguish between positive and negative samples. To achieve this, the attacker first generates training samples and validation samples using selected plaintext difference DP and master key difference DK.

The training samples are used to train the neural network, while the validation samples are used to evaluate the recognition ability of the neural network. Ultimately, we can determine whether we have successfully constructed an effective neural distinguisher based on whether its accuracy surpasses the threshold of 0.5. In the online phase, the neural distinguisher trained in the offline phase is employed to distinguish the ciphertext data generated by a block cipher or a random function. If the score of more than half of the samples exceeds 0.5, we consider the ciphertext data comes from the block cipher. Otherwise, these data are considered to originate from the random function.


## Parameter setting

The number of training samples and validation samples used in this article is 2 Â 10 7 and 2 Â 10 6 . In addition, we set the number of epochs to 120, and each epoch contains multiple batches, each containing 30,000 samples. In order to adjust the learning rate more efficiently, we adopt the cyclic learning rate. Specifically, for the i-th epoch, its learning rate l i is dynamically calculated by l i ¼ a þ ðnÀiÞ mod ðnþ1Þ n Â ðb À aÞ; where a ¼ 0:0001, b ¼ 0:003, and n ¼ 29. Moreover, we choose Adam (Kingma & Ba, 2014) as the optimizer and Mean Squared Error (MSE) as the loss function. To prevent the model from overfitting, we use L2 regularization with the parameter c of 0.00001. Benamira et al. (2021) found that Gohr's neural distinguisher showed a superior recognition ability for the ciphertext pairs exhibiting truncated differences with high probability in the last two rounds, suggesting a potential understanding and learning of differential-linear characteristics in the ciphertext pairs. Subsequently, Gohr, Leander & Neumann (2022) expanded their study to five different block, including SIMON, Speck (Beaulieu et al., 2015) , Skinny (Beierle et al., 2016) , PRESENT Bogdanov et al. (2007) , Katan (De Canniere, Dunkelman & Knežević, 2009) , and ChaCha (Bernstein, 2008) . Notably, their research highlights the close connection between the accuracy of the neural distinguisher and the mean absolute distance of the ciphertext differential distribution and the uniform distribution. In light of these investigations, we enhance the basic differential neural distinguisher by using two distinct non-zero plaintext differences and master key differences, symbolically represented as (DP; DP 0 ; DK; DK 0 ).


## Enhanced related-key differential neural distinguishers


## Motivation

The primary rationale behind selecting two input differences instead of one or more stems from the objective of minimizing conflicts among the output differences arising from positive and negative samples. When an input difference is chosen, as the number of rounds increases, some output differences will tend to be uniformly distributed due to the inherent confusion and diffusion properties of the block cipher. This poses a great challenge for the neural network to distinguish them from the uniformly distributed negative samples. However, if the negative samples are generated from another good difference, the mean absolute distance between the positive and negative samples may become more significant, which can allow the neural network to distinguish them more effectively. There are two reasons for limiting the number of input differences to two rather than more: firstly, the input differences that can maintain their unique distribution across several rounds are rare; secondly, an increase in the variety of ciphertext data may heighten the likelihood of collisions.


## Differences selection

To develop an efficient and enhanced neural distinguisher, (DP; DP 0 ; DK; DK 0 ) needs to satisfy two pivotal requirements. Firstly, they must exhibit a favorable weighted bias score after several rounds, ensuring that the resulting ciphertext data possess distinct and discernible features. This can be straightforwardly accomplished by adopting the differential evaluation scheme detailed in "Basic Related-Key Differential Neural Distinguishers". Second, the disparity between the ciphertext data derived from the input differences (DP; DK) and (DP 0 ; DK 0 ) should be maximized, thereby ensuring that there are sufficient features for the neural network to leverage during the learning process.

Inspired by the role of weighted bias scores, we try to directly utilize their relative weighted bias scores, denoted as S R ðDP; DP 0 ; DK; DK 0 Þ, as a rough metric to evaluate the suitability of ðDP; DP 0 ; DK; DK 0 Þ for building the enhanced neural distinguishers, where

However, the outcomes are disappointing, primarily due to the fact that the relative weighted bias scores among all combinations derived from two input differences with weighted high bias scores have a high degree of similarity.

Fortunately, the differences that have high weighted bias scores are generally scarce. For a set of m input differences, the total number of potential combinations is m Â ðmÀ1Þ 2 . Consequently, when m is small, the exhaustive approach that compares all potential combinations to identify the optimal one is feasible. Nonetheless, as the value of m increases, the number of combinations grows rapidly. Specifically, when m is 32, it is a daunting task to train 496 neural distinguishers. Given that the training of a single neural distinguisher takes about an hour and a half, the aggregate time required for this task approximating 31 days, which is impractical and and unacceptable for most researchers. Therefore, the adoption of a more efficient and targeted strategy for selecting promising combinations becomes imperative.

An available greedy strategy is to fix ðDP; DKÞ as the optimal or top-ranked input difference that can be used to construct the most effective basic neural distinguisher. Subsequently, ðDP 0 ; DK 0 Þ is chosen from the remaining differences with good weighted bias score. This strategy can ensure that the ciphertext data generated with ðDP; DKÞ have discernible and distinctive features. In this article, we adopt the exhaustive approach for SIMON32/64 and SIMON32/64. For the remaining variants, we adopt this greedy strategy to speed up the process of differences selection.


## Sample generation

The sample generation for enhanced neural distinguisher is different from method outlined for the basic neural distinguisher in "Basic Related-Key Differential Neural Distinguishers". For the enhanced neural distinguisher, the positive and negative samples are ciphertext data generated from the plaintext pairs and key pairs with the differences ðDP; ; DKÞ and ðDP 0 ; DK 0 Þ. The label of a sample ð 1 k 2 k…k s Þ is represented as

The neural network architecture and the process of training and evaluation remain consistent with that in "Basic Related-Key Differential Neural Distinguishers".


## RELATED-KEY DIFFERENTIAL NEURAL DISTINGUISHERS FOR ROUND-REDUCED SIMON AND SIMECK

In this section, we adopt the framework and strategies in "The Framework for Developing Related-Key Differential Neural Distinguishers to SIMON and SIMECK" to develop the basic and enhanced related-key differential neural distinguishers for SIMON and SIMECK.


## Differences selection for SIMON

The differences with Hamming weights of 1 and 2 For a block cipher with block length bl and key length kl, the number of input differences we need to evaluate is 2 blþkl . Even for the smallest variants, i.e., SIMON32/64 and SIMECK32/64, the number of differences that need to be evaluated reaches 2 96 , which would take a lot of time. Therefore, we first evaluate the weighted bias scores for all the differences with Hamming weights of 1 and 2.

For the 8-round SIMON32/64, there are 16 input differences with weighted bias scores around 11.0, which are DP ¼ ð0Â0; 0Â1 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â1 <<< iÞ; i 2 ½0; 15. This is followed by another 16 input differences with a weighted bias score of about 10.8, specified as DP ¼ ð0Â0; 0Â21 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â21 <<< iÞ; i 2 ½0; 15. The score for all remaining input differences with Hamming weights of 1 and 2 is less than 10.00. For the 8-round SIMON48/96, there are 24 input differences with a Hamming weight of 1 that have a weighted bias score between 15.3 and 14.4: DP ¼ ð0Â0; 0Â1 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â1 <<< iÞ; i 2 ½0; 23: For differences with a Hamming weight of 2, only 11 input differences yield weighted bias scores greater than 14.4. They are DP ¼ ð0Â0; 0Â41000 ( iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â41000 ( iÞ; i 2 ½0; 6, DP ¼ ð0Â0; 0Â21000 ( iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â21000 ( iÞ; i 2 ½0; 2, and DP ¼ ð0Â0; 0Â30000Þ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â30000Þ.

For the 8-round SIMON64/128, there are 32 differences with a Hamming weight of 1 that exhibit scores around 13.4. These differences are denoted as DP ¼ ð0Â0; 0Â1 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â1 <<< iÞ; i 2 ½0; 31. After that, there are 32 differences with Hamming weight 2 that have scores close to 12.6 or 12.5, which are DP ¼ ð0Â0; 0Â21 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â21 <<< iÞ; i 2 ½0; 31, and DP ¼ ð0Â0; 0 Â41 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â41 <<< iÞ; i 2 ½0; 31, respectively. The scores for all remaining differences are below 12.2.


## Structural features of SIMON

For SIMON32/64, SIMON48/96, and SIMON64/128, the input differences with high weighted bias scores are those with the structure DP ¼ ð0Â0; DXÞ and DK ¼ ð0Â0; 0Â0; 0Â0; DXÞ. By analyzing the propagation process of the difference in SIMON, we can find that the plaintext differences and key differences cancel each other out in the first round. In the next three rounds, both plaintext difference and key difference are zero. Only in the fifth round, the key difference DX is re-injected, and the plaintext difference is still zero. The detailed differential propagation process is given in Table 3 . This is easily verified by analyzing the transformations of the plaintext difference and the key difference in the round function and the round key.


## The differences with a Hamming weight greater than 2

Based on the structural feature of SIMON, for differences with a weight greater than 2, we only consider the differences with a structure of DP ¼ ð0Â0; DXÞ and DK ¼ ð0Â0; 0Â0; 0Â0; DXÞ. For 8-round SIMON32/64, there are only 32 differences with Hamming weights of 3 that have weighted bias scores greater than 10.0. Specifically, they are DP ¼ ð0Â0; 0Â43=0Â421 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â43=0Â421 <<< iÞ; i 2 ½0; 15, with scores between 10.7 and 10.3. For the 8-round SIMON48/96 and SIMON64/128, the weighted bias scores for all differences with a Hamming weight greater than two are less than 14.4 and 12.2, respectively.


## Differences selection for SIMECK

The differences with Hamming weights of 1 and 2

Following the experiments on SIMON, we first explore the applicability of the input differences with Hamming weights of 1 and 2 in constructing neural distinguishers for SIMECK. For 10-round SIMECK32/64, 16 differences with a Hamming weight of 1, denoted as DP ¼ ð0Â0; 0Â1 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â1 <<< iÞ; i 2 ½0; 15, achieve the optimal weighted bias score around 16.3. Then there are 32 differences with Hamming weight of 2, DP ¼ ð0Â0; 0Â3=0Â11 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â3=0Â 11 <<< iÞ; i 2 ½0; 15, with scores greater than 13.0. The rest of the differences are scored below 13.0.

For the 12-round SIMECK48/96, there are 24 differences with a Hamming weight of 1, DP ¼ ð0Â0; 0Â1 ( iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â1 ( iÞ; i 2 ½0; 23, that have a weighted bias score between 30.4 and 26.6. For differences with a Hamming weight of 2, there are 33 differences with scores greater than or equal to 26.6. They are DP ¼ ð0Â0; 0Â30 ( iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â30 ( iÞ; i 2 ½0; 12, DP ¼ ð0Â0; 0Â220 ( iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â220 ( iÞ; i 2 ½0; 8, DP ¼ ð0Â0; 0Â140 ( iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â140 ( iÞ; i 2 ½0; 6, and DP ¼ ð0Â0; 0Â480 ( iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â480 ( iÞ; i 2 ½0; 3. The scores of all remaining differences are all less than 26.5.

For the 15-round SIMECK64/128, the best weighted bias score around 30.1 is achieved by 32 differences with a Hamming weight of 1, which are DP ¼ ð0Â0; 0Â1 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â1 <<< iÞ; i 2 ½0; 31. Then there are 32 differences, DP ¼ ð0Â0; 0Â3 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â3 <<< iÞ; i in½0; 31, with scores close to 26.7. All the other differences have scores below 26.0.

Structural features of SIMECK Similar to SIMON, for all variants of SIMECK, the input differences that exhibit good weighted bias scores adhere to the format: DP ¼ ð0Â0; DXÞ and DK ¼ ð0Â0; 0Â0; 0Â0; DXÞ. This is also due to the fact, as shown in Table 4 , that the plaintext difference and key difference cancel each other out in the first round, and in the subsequent three rounds, both the plaintext difference and key difference are zero. It is not until the fifth round that the key difference DX 0 , resulting from the operation of DK r <<< a and DK r <<< b, is reintroduced.

The differences with a Hamming weight greater than 2

For the 10-round SIMECK32/64 and 15-round SIMECK64/128, none of the differences with a Hamming weight of more than two yields a weighted bias score above 12.5 and 24.5, respectively. For 12-round SIMECK48/96, there are only three differences with a Hamming weight of three that have a score of 26.8, which are DP ¼ ð0Â0; 0Â700=0xe00=0Â2300Þ, DK ¼ ð0Â0; 0Â0; 0Â0; 0Â700=0xe00=0Â2300Þ. The scores for all remaining differences with a Hamming weight of three or higher are all below 26.6.


## Basic related-key differential neural distinguishers

For the SIMON32/64, the 16 most effective 13-round related-key differential neural distinguishers are trained using the candidate differences DP ¼ ð0Â0; 0Â21 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â21 <<< iÞ where i ranges from 0 to 15. Their accuracy is 0:543 AE 0:002, while it is 0:525 AE 0:005 for the distinguishers built from the candidate differences DP ¼ ð0Â0; 0Â1 <<< iÞ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â1 <<< iÞ; i 2 ½0; 15. The best 13-round neural distinguisher is constructed by DP ¼ ð0Â0; 0Â2004Þ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â2004Þ with an accuracy of 0.545. Its 12-round neural distinguisher achieves an accuracy of 0.678. Compared with the related-key differential neural distinguisher in Lu et al. (2024) , our differential selection strategy enables us to yield the superior distinguisher, as shown in Table 1 .

For SIMON48/96, the best 13-round related-key differential neural distinguisher with an accuracy of 0.650 is constructed with DP ¼ ð0Â0; 0Â200000Þ and DK ¼ ð0Â0; 0Â0; 0Â0; 0Â200000Þ. Its 12-round neural distinguisher can achieve an accuracy of 0.993. For the remaining 23 candidate differences with a Hamming weight of 1, the accuracy of their 13-round neural distinguishers is between 0.640 to 0.650. In contrast, when the candidate differences with Hamming weight 2 in "Differences Selection for SIMON" is adopted, the highest accuracy is only 0.593, which is lower than that of 24 candidate differences with a Hamming weight of 1. Moreover, the three candidate differences with a Hamming weight of three could not construct an effective neural distinguisher for 13 rounds.

For SIMON64/128, the optimal 14-round related-key differential neural distinguisher is constructed using DP ¼ ð0Â0; 0Â100000Þ and DK ¼ ð0Â0; 0Â0; 0Â0; 0Â100000Þ with an accuracy of 0.580. The accuracy of its 13-round neural distinguisher is 0.840. In addition, the neural distinguishers built from the other 31 candidate differences with a Hamming weight of one exhibit accuracy between 0.577 and 0.580. There are no valid 14round neural distinguishers achieved when using the candidate differences with a Hamming weight of two in "Differences Selection for SIMON".

For SIMECK, the maximum number of rounds that can be constructed for related-key differential neural distinguishers is 15 for SIMECK32/64, 19 for SIMECK48/96, and 22 for SIMECK64/128. Their optimal neural distinguishers are constructed using DP ¼ ð0Â0; 0Â10=0Â2=0Â200000Þ and DK ¼ ð0Â0; 0Â0; 0Â0; 0Â10=0Â2=0Â200000Þ with an accuracy of 0.547, 0.516, and 0.519, respectively. The accuracies of these neural distinguishers from the previous round are 0.668, 0.551, and 0.552, respectively. The neural distinguishers constructed from other candidate differences with a Hamming weight of one have an accuracy very close to the best neural distinguisher above, with a maximum deviation of only 0.002. The candidate differences with Hamming weights greater than two fail to construct effective neural distinguishers with the maximum number of rounds.


## Enhanced related-key differential neural distinguishers

For the SIMON32/64 and SIMECK32/64, we use all possible combinations of the superior candidate differences DP ¼ ð0Â0; 0Â21=0Â1 <<< iÞ and DK ¼ ð0Â0; 0Â0; 0Â0; 0Â21=0Â1 <<< iÞ, i 2 ½0; 15, to construct the related-key differential neural distinguisher. For SIMON32/64, there are five different ðDP; DP 0 ; DK; DK 0 Þ that can yield the 13-round related-key differential neural distinguisher with an accuracy of 0.567. They are DP ¼ ð0Â0; 0Â801=0Â42=0Â2100=2004=2100Þ; DK ¼ ð0Â0; 0Â0; 0Â0; 0Â100000=0Â2=0Â200000Þ; DP 0 ¼ ð0Â0; 0Â1002=0Â84=0Â1080=1002=4200Þ; Dk 0 ¼ ð0Â0; 0Â0; 0Â0; 0Â400000=0Â80000=0Â200Þ: & For the first two instances, the accuracy of their 12-round neural distinguisher is 0.740, while it is 0.738 for the remaining three instances.

For SIMON48/96, SIMON64/128, SIMECK48/96, and SIMECK64/128, we consider combinations of the best differences in Table 5 and the remaining candidate differences of DP ¼ ð0Â0; 0Â1 <<< iÞ and DK ¼ ð0Â0; 0Â0; 0Â0; 0Â1 <<< iÞ, i 2 ½0; 15 to accelerate the construction of our enhanced neural distinguishers. Specifically, for SIMON48/96, there are three pairs of differences that can yield 12-round and 13-round related-key differential neural distinguishers with accuracies of 0.997 and 0.696, respectively. These pairs are DP ¼ ð0Â0; 0Â200000Þ and DK ¼ ð0Â0; 0Â0; 0Â0; 0Â2000Þ together with DP 0 ¼ ð0Â0; DÞ and DK 0 ¼ ð0Â0; 0Â0; 0Â0; DÞ, where D 2 ½0Â400000; 0Â100000; 0Â40. For SIMON64/128, SIMECK48/96, and SIMECK64/128, only one pair of differences can construct 14-round, 19-round, and 22-round related-key neural distinguishers with accuracies of 0.618, 0.523, and 0.526, respectively. They are DP ¼ ð0Â0; 0Â 100000=0Â2=0Â200000Þ, DK ¼ ð0Â0; 0Â0; 0Â0; 0Â100000=0Â2=0Â200000Þ, DP 0 ¼ ð0Â0; 0Â400000=0Â80000=0Â200Þ, and DK 0 ¼ ð0Â0; 0Â0; 0Â0; 0Â400000=0Â 80000=0Â200Þ. The accuracies of 13-round, 18-round, and 21-round neural distinguishers for these pairs are 0.916, 0.572, and 0.572, respectively, as shown in Table 6 .


## Comparison and discussion

In this section, we first evaluate the differences with Hamming weights of 1 and 2 for SIMON and SIMECK, using weight bias scores. Then, we further evaluate the differences with Hamming weights greater than two based on the structural features of SIMON and SIMECK. Compared with the exhaustive approach of training a neural distinguisher for each difference in Lu et al. (2024) , our scheme is more efficient.

Using these differences, we can obtain 13-round basic related-key differential neural distinguishers, exhibiting superior accuracy than that in Lu et al. (2024) , for SIMON32/64. The accuracy of this basic neural distinguisher can be improved from 0.526 to 0.545 due to the effectiveness of our difference selection strategy. For the remaining variants, we can also obtain the basic related-key differential neural distinguishers with the same accuracy as that in Lu et al. (2024) , as shown in Table 1 . In addition, we obtain multiple basic related-key differential neural distinguishers that have the same or similar accuracy as the best distinguisher. All these results illustrate the effectiveness and usability of our proposed strategy for difference selection.

When constructing the enhanced related-key differential neural distinguishers using our method, all the enhanced differential neural distinguishers achieve higher accuracy than the basic related-key differential neural distinguishers for both SIMON and SIMECK. Compared with the results in Lu et al. (2024) , our neural distinguishers all achieve different degrees of improvement in accuracy, as shown in Table 1 . Specifically, the accuracy of the 13-round SIMON32/64, 13-round SIMON48/96, and 14-round SIMON64/128 is increased from 0.545, 0.650, and 0.580 to 0.567, 0.696, and 0.618, respectively. Similarly, the neural distinguishers for the 15-round SIMECK32/64, 19-round SIMECK48/96, and 22-round SIMECK64/128 is also demonstrated notable improvements in accuracy, with increases from 0.547, 0.516, and 0.519 to 0.568, 0.523, and 0.526, respectively. These results collectively underscore the effectiveness and robustness of our proposed scheme for constructing the enhanced related-key differential neural distinguishers.


## CONCLUSIONS AND FUTURE WORK

In this article, we first establish a comprehensive framework to construct basic related-key differential neural distinguishers for the SIMON and SIMECK. To choose an appropriate difference to construct this distinguisher, we utilize weighted bias scores to assess the applicability of various differences, which speeds up the process of difference selection and evaluation.

Moreover, we introduce an innovative method that incorporates two distinct differences into the neural distinguisher instead of a differences, which can result in the more robust and effective neural distinguishers. Compared with the distinguishers in Lu et al. (2024) , we successfully improve the accuracy of the related-key differential neural distinguisher for both SIMON and SIMECK as shown in Table 1 .

Furthermore, we envision several promising directions for future research. Firstly, our framework can be easily extended to other block ciphers, which assists in evaluating the security of other block ciphers. Secondly, the integration of advanced neural network architectures and training techniques could yield even more powerful neural distinguishers.

> 1 Figure 1 Figure 1 The round function of SIMON and SIMECK. Full-size  DOI: 10.7717/peerj-cs.2566/fig-1

> 2 Figure 2 Figure2The architecture of LeNet-5 (LeCun et al., 1998) .Full-size  DOI: 10.7717/peerj-cs.2566/fig-2

> 3 Figure 3 Figure3The shortcut connections of ResNet (He et al., 2016) .Full-size  DOI: 10.7717/peerj-cs.2566/fig-3

> 5 Figure 5 Figure5The framework of basic and enhanced related-key differential neural distinguishers.Full-size  DOI: 10.7717/peerj-cs.2566/fig-5

> ), Bao et al. (2022) , Lu et al. (2024) and Zhang, Wang & Chen (2023) , the architecture shown in Fig.6can achieve best accuracy under the same conditions. It consists of the following components:

> 6 Figure 6 Figure 6 Overview of neural network architectures. BN, Batch Normalization; GAP, Global Average Pooling.Full-size  DOI: 10.7717/peerj-cs.2566/fig-6

> 1 Table 1 Summary of related-key neural distinguishers against SIMON32/64, SIMON48/96, SIMON64/128, SIMECK32/64, SIMECK48/96, and SIMECK64/128 using eight pairs of ciphertexts as a sample.

> 3 Table 3 The related-key differential characteristic of SIMON with four key words.

> 4 Table 4 The related-key differential characteristic of SIMECK.

> 5 Table 5 The basic related-key differential neural distinguishers for SIMON and SIMECK.

> 6 Table 6 The enhanced related-key differential neural distinguishers for SIMON and SIMECK.

## References

1. b0: Zhenzhen Bao, Jian Guo, Meicheng Liu, Li Ma, Yi Tu. "Enhancing Differential-Neural Cryptanalysis". Lecture Notes in Computer Science. 2022. DOI: 10.1007/978-3-031-22963-3_11
2. b1: Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks, Louis Wingers. "The SIMON and SPECK lightweight block ciphers". Proceedings of the 52nd Annual Design Automation Conference. 2015-06-07. DOI: 10.1145/2744769.2747946
3. b2: Christof Beierle, Jérémy Jean, Stefan Kölbl, Gregor Leander, Amir Moradi, Thomas Peyrin, et al.. "The SKINNY Family of Block Ciphers and Its Low-Latency Variant MANTIS". Lecture Notes in Computer Science. 2016-08-14. DOI: 10.1007/978-3-662-53008-5_5
4. b3: Emanuele Bellini, David Gerault, Juan Grados, Rusydi H Makarim, Thomas Peyrin. "Boosting Differential-Linear Cryptanalysis of ChaCha7 with MILP". IACR Transactions on Symmetric Cryptology. 2023-06-16. DOI: 10.46586/tosc.v2023.i2.189-223
5. b4: Emanuele Bellini, David Gerault, Anna Hambitzer, Matteo Rossi. "A Cipher-Agnostic Neural Training Pipeline with Automated Finding of Good Input Differences". IACR Transactions on Symmetric Cryptology. 2023-09-19. DOI: 10.46586/tosc.v2023.i3.184-212
6. b5: Adrien Benamira, David Gerault, Thomas Peyrin, Quan Quan Tan. "A Deeper Look at Machine Learning-Based Cryptanalysis". Lecture Notes in Computer Science. 2021. DOI: 10.1007/978-3-030-77870-5_28
7. b6: D J Bernstein. "Chacha, a variant of salsa20". Workshop Record of SASC. 2008
8. b7: Eli Biham. "New types of cryptanalytic attacks using related keys". Journal of Cryptology. 1994-12. DOI: 10.1007/bf00203965
9. b8: E Biham, O Dunkelman. "Differential cryptanalysis in stream ciphers". Cryptology ePrint Archive. 2007
10. b9: Eli Biham, Adi Shamir. "Differential Cryptanalysis of Snefru, Khafre, REDOC-II, LOKI and Lucifer". Lecture Notes in Computer Science. 1991. DOI: 10.1007/3-540-46766-1_11
11. b10: Eli Biham, Adi Shamir. "Differential cryptanalysis of DES-like cryptosystems". Journal of Cryptology. 1991-01. DOI: 10.1007/bf00630563
12. b11: Eli Biham, Adi Shamir. "Differential Cryptanalysis of the Full 16-round DES". Lecture Notes in Computer Science. 1992. DOI: 10.1007/3-540-48071-4_34
13. b12: A Bogdanov, L R Knudsen, G Leander, C Paar, A Poschmann, M J B Robshaw, et al.. "PRESENT: An Ultra-Lightweight Block Cipher". Lecture Notes in Computer Science. 2007-09-10. DOI: 10.1007/978-3-540-74735-2_31
14. b13: Rahul Chauhan, Kamal Kumar Ghanshala, R C Joshi. "Convolutional Neural Network (CNN) for Image Detection and Recognition". 2018 First International Conference on Secure Cyber Computing and Communication (ICSCCC). 2018-12. DOI: 10.1109/icsccc.2018.8703316
15. b14: Christophe De Cannière, Orr Dunkelman, Miroslav Knežević. "KATAN and KTANTAN — A Family of Small and Efficient Hardware-Oriented Block Ciphers". Lecture Notes in Computer Science. 2009. DOI: 10.1007/978-3-642-04138-9_20
16. b15: David Gerault, Marine Minier, Christine Solnon. "Constraint Programming Models for Chosen Key Differential Cryptanalysis". Lecture Notes in Computer Science. 2016. DOI: 10.1007/978-3-319-44953-1_37
17. b16: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
18. b17: A Gohr, G Leander, P Neumann. "An assessment of differential-neural distinguishers". Cryptology ePrint Archive. 2022. DOI: 10.1016/j.jisa.2024.103758
19. b18: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun. "Deep Residual Learning for Image Recognition". 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2016-06. DOI: 10.1109/cvpr.2016.90
20. b19: Jie Hu, Li Shen, Gang Sun. "Squeeze-and-Excitation Networks". 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2018-06. DOI: 10.1109/cvpr.2018.00745
21. b20: A Jain, V Kohli, G Mishra. "Deep learning based differential distinguisher for lightweight cipher present". Cryptology ePrint Archive. 2020. DOI: 10.48550/arXiv.2112.05061
22. b21: Goce Jakimoski, Yvo Desmedt. "Related-Key Differential Cryptanalysis of 192-bit Key AES Variants". Lecture Notes in Computer Science. 2003. DOI: 10.1007/978-3-540-24654-1_15
23. b22: D P Kingma, J Ba. Adam: a method for stochastic optimization. 2014. DOI: 10.48550/arXiv.1412.6980
24. b23: Alex Krizhevsky, Ilya Sutskever, Geoffrey E Hinton. "ImageNet classification with deep convolutional neural networks". Communications of the ACM. 2017-05-24. DOI: 10.1145/3065386
25. b24: Frédéric Lafitte. "CryptoSAT: a tool for SAT‐based cryptanalysis". IET Information Security. 2018-11. DOI: 10.1049/iet-ifs.2017.0176
26. b25: Y Lecun, L Bottou, Y Bengio, P Haffner. "Gradient-based learning applied to document recognition". Proceedings of the IEEE. 1998. DOI: 10.1109/5.726791
27. b26: W A Little. "The existence of persistent states in the brain". Mathematical Biosciences. 1974-02. DOI: 10.1016/0025-5564(74)90031-5
28. b27: Jinyu Lu, Guoqiang Liu, Bing Sun, Chao Li, Li Liu. "Improved (Related-Key) Differential-Based Neural Distinguishers for SIMON and SIMECK Block Ciphers". The Computer Journal. 2024. DOI: 10.1093/comjnl/bxac195
29. b28: Lijun Lyu, Yi Tu, Yingjie Zhang. "Improving the Deep-Learning-Based Differential Distinguisher and Applications to Simeck". 2022 IEEE 25th International Conference on Computer Supported Cooperative Work in Design (CSCWD). 2022-05-04. DOI: 10.1109/cscwd54268.2022.9776036
30. b29: Mitsuru Matsui. "On correlation between the order of S-boxes and the strength of DES". Lecture Notes in Computer Science. 1994. DOI: 10.1007/bfb0053451
31. b30: Nicky Mouha, Qingju Wang, Dawu Gu, Bart Preneel. "Differential and Linear Cryptanalysis Using Mixed-Integer Linear Programming". Lecture Notes in Computer Science. 2011-12-03. DOI: 10.1007/978-3-642-34704-7_5
32. b31: V Nair, G E Hinton. "Rectified linear units improve restricted Boltzmann machines". Proceedings of the 27th International Conference on Machine Learning (ICML-10). 2010
33. b32: H Seong, H Yoo, Y Yeom, J S Kang. "Analysis of Gohr's neural distinguisher on Speck32/64 and its application to Simon32/64". Journal of the Korea Institute of Information Security & Cryptology. 2022. DOI: 10.13089/JKIISC.2022.32.2.391
34. b33: Dongsu Shen, Yijian Song, Yuan Lu, Saiqin Long, Shujuan Tian. "Neural differential distinguishers for GIFT-128 and ASCON". Journal of Information Security and Applications. 2024-05. DOI: 10.1016/j.jisa.2024.103758
35. b34: Siwei Sun, David Gerault, Pascal Lafourcade, Qianqian Yang, Yosuke Todo, Kexin Qiao, et al.. "Analysis of AES, SKINNY, and Others with Constraint Programming". IACR Transactions on Symmetric Cryptology. 2017-03-08. DOI: 10.46586/tosc.v2017.i1.281-306
36. b35: Siwei Sun, Lei Hu, Peng Wang, Kexin Qiao, Xiaoshuang Ma, Ling Song. "Automatic Security Evaluation and (Related-key) Differential Characteristic Search: Application to SIMON, PRESENT, LBlock, DES(L) and Other Bit-Oriented Block Ciphers". Lecture Notes in Computer Science. 2014. DOI: 10.1007/978-3-662-45611-8_9
37. b36: Christian Szegedy, Wei Liu, Yangqing Jia, Pierre Sermanet, Scott Reed, Dragomir Anguelov, et al.. "Going deeper with convolutions". 2015 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2015-06. DOI: 10.1109/cvpr.2015.7298594
38. b37: Amin Ullah, Jamil Ahmad, Khan Muhammad, Muhammad Sajjad, Sung Wook Baik. "Action Recognition in Video Sequences using Deep Bi-Directional LSTM With CNN Features". IEEE Access. 2017. DOI: 10.1109/access.2017.2778011
39. b38: Huijiao Wang, Jiapeng Tian, Xin Zhang, Yongzhuang Wei, Hua Jiang. "Multiple Differential Distinguisher of SIMECK32/64 Based on Deep Learning". Security and Communication Networks. 2022-09-14. DOI: 10.1155/2022/7564678
40. b39: Gao Wang, Gaoli Wang, Yu He. "Improved Machine Learning Assisted (Related-key) Differential Distinguishers For Lightweight Ciphers". 2021 IEEE 20th International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom). 2021-10. DOI: 10.1109/trustcom53373.2021.00039
41. b40: Gangqiang Yang, Bo Zhu, Valentin Suder, Mark D Aagaard, Guang Gong. "The Simeck Family of Lightweight Block Ciphers". Lecture Notes in Computer Science. 2015. DOI: 10.1007/978-3-662-48324-4_16
42. b41: W Yin, K Kann, M Yu, H Schütze. Comparative study of CNN and RNN for natural language processing. 2017. DOI: 10.48550/arXiv.1702.01923
43. b42: Liu Zhang, Jinyu Lu, Zilong Wang, Chao Li. "Improved differential-neural cryptanalysis for round-reduced SIMECK32/64". Frontiers of Computer Science. 2023-12. DOI: 10.1007/s11704-023-3261-z
44. b43: Liu Zhang, Zilong Wang, Yindong Chen. "Improving the Accuracy of Differential-Neural Distinguisher for DES, Chaskey, and PRESENT". IEICE Transactions on Information and Systems. 2023-07-01. DOI: 10.1587/transinf.2022edl8094
