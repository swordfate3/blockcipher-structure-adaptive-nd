# Improved polytopic differential neural distinguishers for SIMON, SIMECK, and SPECK block ciphers

**Authors:** Iman Mirzaali, Sadegh Sadeghi, Nasour Bagheri

**Source PDF:** `2026_polytopic_pdnd_simon_simeck_speck.pdf`

## Abstract

In recent years, the application of deep learning in cryptanalysis has gained significant attention, particularly with the emergence of neural network-based distinguishers. At CRYPTO'19, Gohr demonstrated that neural networks could develop differential distinguishers capable of producing highly competitive attacks against existing methods. Building on this foundation, we propose multiple input polytopic differential neural distinguishers (PDNDs) for the lightweight block ciphers SIMON, SIMECK, and SPECK. Our approach incorporates a novel data generation method that utilizes two polytope differences, resulting in more precise training data and enhanced model accuracy. Through extensive experiments in single-key and related-key scenarios, we evaluate and validate the intrinsic performance of our neural distinguishers. Our results show that PDNDs significantly outperform the baseline, polytopic, multiple, and mixture differential neural distinguishers, utilizing a single input difference, in accuracy across various cipher rounds. Notably, our PDNDs achieved 100% accuracy for up to 7 rounds of SIMON32 and SIMECK32, and 99.39% accuracy for 5 rounds of SPECK32 in the single-key scenario. Additionally, for extended rounds, we achieved accuracy levels of up to 12 rounds for SIMON32, 13 for SIMECK32, and 8 for SPECK32 without requiring staged training. In the related-key scenario, our method further improved performance, introducing 13-round and 15-round RK-PDNDs for SIMON32 and SIMECK32, respectively, underscoring the enhanced capabilities of our approach. Furthermore, we demonstrate the effectiveness of our neural distinguishers through a key recovery test, where they successfully distinguish between correct and incorrect keys, confirming the practical applicability of our approach in cryptanalysis.

## Introduction

The advancement of machine learning has profoundly impacted various aspects of people's lives. Among the various branches of machine learning, deep learning has excelled particularly in a wide range of tasks across numerous domains. Recently, deep learning has made significant contributions to challenging tasks, such as machine translation Klimova et al. (2023) and autonomous driving Lee and Liu (2023) . In cryptography, machine learning techniques have primarily been applied to practical works in side-channel analysis Masure et al. (2020) .

Block ciphers are commonly used in various information systems to ensure confidentiality. One type of cipher that is rapidly gaining popularity is the lightweight block cipher, which is widely employed in Internet of Things (IoT) devices. Lightweight block ciphers are fundamental components of cryptosystems, playing a critical role in ensuring data confidentiality in resource-constrained devices. In this context, the primary methods used to attack block ciphers are differential cryptanalysis Biham and Shamir (1991) and linear cryptanalysis Matsui (1993) .

Recent advancements in machine learning, especially deep learning, have introduced new paradigms in cryptanalysis. Using neural networks to develop distinguishers has shown promising results in identifying weaknesses in block ciphers. For the first time, at CRYPTO'19, Gohr proposed better results by using a neural network in differential cryptanalysis Gohr (2019) . That work focuses on applying deep learning techniques, such as ResNet He et al. (2016) , to extend the widely used differential distinguisher model.

In this paper, we extend Gohr's work by introducing a new method for differential neural cryptanalysis based on multiple input polytope differences. Our approach involves using two polytope differences as inputs instead of one. This method allows for distinguishing between the ciphertexts produced by different polytope differences, eliminating the need for random inputs. Furthermore, we utilize a ResNet architecture with dilated convolutional layers and a training method that loads the previous round's model weights at each new round, improving the accuracy of the baseline neural distinguishers for SPECK32, SIMON32 Beaulieu et al. (2015) , and SIMECK32 Yang et al. (2015) block ciphers.


## Related work

The main results of Gohr's work Gohr (2019) include training neural networks to use the differential features of the SPECK cipher with reduced rounds. For this purpose, neural networks were trained to distinguish SPECK ciphertexts with given input differences from random data. Neural networks have been developed to attack SPECK reduced to eight rounds, and it has been shown that key recovery attacks using neural distinguishers are more optimal than classical methods for nine and eleven rounds.

It is demonstrated that neural distinguishers exploit features of the distribution of ciphertext pairs that are hidden from all purely differential distinguishers, even with unlimited data. Different directions have been explored following the introduction of differential neural cryptanalysis. Su et al. (2021) proposed a novel approach combining polytope differences with neural networks to improve differential cryptanalysis on reduced-round SIMON32 block cipher. They introduced the Polytope Differential Neural Network Distinguisher, which enhanced the success rate of neural distinguishers from 0.76 to 0.92 on eight rounds of SIMON32. Furthermore, they developed a key recovery attack leveraging the probability of differential paths alongside their polytope distinguisher, achieving a computational complexity of 2 33.4 for 11-round SIMON32. The Bayesian Key Research with Error was another contribution, reducing the complexity to 2 30.9 . Benamira et al. (2021) investigated the superior performance of neural distinguishers in cryptanalysis, presenting their findings at Eurocrypt 2021. They analyzed Gohr's neural distinguishers and discovered their effectiveness stems from leveraging the differential distribution of ciphertext pairs and distributions in the penultimate and antepenultimate rounds. This dual reliance allows neural distinguishers to surpass traditional differential distinguishers in accuracy. Their study also showed that simplifying Gohr's neural network to basic machine learning tools can still achieve similar accuracy. This suggests that these neural distinguishers effectively approximate the Differential Distribution Table (DDT) during training to classify ciphertext pairs. This insight enhances the interpretability of deep neural networks in cryptanalysis. Wang et al. (2021) proposed an extended machine learning framework to construct related-key differential distinguishers for lightweight ciphers, such as SPECK32 and PRESENT64. They introduced exhaustive and greedy algorithms for optimizing input and key differences, demonstrating that low Hamming weight differences yield higher accuracy. Using Bayesian optimization, they identified suitable machine learning models, such as CNNs, to improve distinguisher performance. Their methods reduced the data complexity significantly, achieving, for instance, a 7-round related-key distinguisher for SPECK32 with a complexity of 2 8 , compared to 2 13.2 in Gohr (2019). Hou et al. (2021) proposed improvements to neural distinguishers for SIMON and SPECK by utilizing SATbased algorithms to optimize input differences and introducing a novel data format leveraging multiple output differences. Their approach significantly enhanced the accuracy and round coverage of neural distinguishers, achieving, for instance, effective 11-round distinguishers for SIMON64 and 8-round distinguishers for SPECK32. The study demonstrated that these advancements enable more efficient distinguishing attacks and reduce complexity in key recovery scenarios.

In Wang et al. (2022) , Wang et al. introduce novel multiple differential distinguishers for the round-reduced SIMECK32 cipher based on deep learning. They design two types of distinguishers using neural networks to simulate the multiple input and output differences of differential cryptanalysis. The study presents the general models of these distinguishers and their neural network structures, utilizing random and associated multiple ciphertext pairs as inputs. Experimental results show that these new distinguishers achieve higher accuracy and can handle more rounds than traditional single-difference distinguishes. The study highlights the efficiency and reduced complexity of deep learning-based differential cryptanalysis. Lyu et al. (2022a) improved deep-learning-based differential distinguishers by introducing repeated training and testing techniques, significantly enhancing the accuracy and round coverage of neural distinguishers applied to SIMECK32. They extended the NN-based distinguisher from 9 to 10 rounds and the differential-NN distinguisher to 15 rounds. Building on this work, Lyu et al. (2022b) further advanced deep-learning-assisted key recovery attacks for SIMECK32 by focusing on selecting neural distinguishers optimized for Bayesian key search rather than solely prioritizing accuracy. Their approach incorporated precomputed wrong-key response profiles and classical differential transitions with high probabilities and neutral bits, enabling successful key recovery for 13, 14, and 15 rounds of SIMECK32 with reduced data and time complexity compared to prior methods, achieving a success rate of up to 88%. Bao et al. (2022) enhanced differential-neural cryptanalysis by introducing advanced techniques to extend attacks on round-reduced ciphers like SPECK32 and SIMON32. Their study devised the first practical 13-round key-recovery attack on SPECK32 and improved 12-round attacks by leveraging generalized neutral bits and Bayesian optimization. Additionally, they introduced innovative approaches, including paired and switching differentials, which enabled efficient data reuse and reduced complexity. Experimental results demonstrated significant improvements in both time and data efficiency. Hambitzer et al. (2023) introduced NNBits, a deep learning ensemble designed for bit-level profiling in cryptographic randomness tests. This tool generalizes neural distinguishers, such as Gohr's, and extends their application to datasets, including avalanche effects from ciphers like SPECK and AES. Their results demonstrate that NNBits match or surpass the performance of traditional statistical tools, such as NIST STS, while providing deeper cryptanalytic insights, including the identification of specific weak bits and an understanding of bias propagation. Chen et al. (2023) proposed a new neural distinguisher model that leverages derived features from multiple ciphertext pairs for enhanced differential cryptanalysis. Unlike traditional models that rely on single ciphertext pairs, their approach processes groups of k > 2 cipher- text pairs, capturing additional features that emerge from the non-uniform distribution of multiple samples. Experimental results demonstrated improved distinguishing accuracy across five reduced symmetric ciphers, including SPECK32, with significant performance gains over baseline models. Additionally, the proposed model reduced the time complexity of key recovery attacks. Gohr et al. (2022) assessed various differential-neural distinguishers for multiple ciphers, including SIMON and SPECK, to evaluate their generality and optimization potential. They demonstrated that neural distinguishers can be automatically optimized for improved performance across six ciphers, highlighting a correlation between distinguisher accuracy and distribution skewness. Furthermore, the study rectified misconceptions regarding multi-pair ciphertext distinguishers, showing that claimed improvements were often marginal. Their findings reaffirm the utility of neural distinguishers in cryptanalysis, particularly for scenarios where classical methods are computationally infeasible. However, they emphasize their limitations in leveraging non-differential features.

In Bellini et al. (2023) , Bellini et al. develop a general framework for neural cryptanalysis capable of automatically finding suitable input differences and providing general neural distinguishers without human adjustment. Their research comprises two main components: an evolutionary algorithm for searching suitable input differences and the DBitNet architecture, agnostic to the cipher structure. This fully automated pipeline has demonstrated competitive performance with specialized approaches, especially for SPECK32 and SIMON32, and introduced new neural distinguishers for various ciphers (e.g., XTEA, LEA, HIGHT, SIMON128, SPECK128). It also improves the state-of-the-art for PRESENT, KATAN, TEA, and GIMLI. This work lays the groundwork for future research, making it easier to apply neural cryptanalysis to a wider range of ciphers without manual tuning.

In Baksi et al. (2023) , Baksi et al. present new advancements in machine learning-based distinguishers, focusing on round-reduced versions of ciphers such as SPECK32, SPECK128, ASCON, SIMECK32, SIMECK64, and SKINNY128. They explore the use of neural networks and support vector machines in various configurations, including different activation functions and multiple input difference tuples. Their results demonstrate the effectiveness of machine learning in cryptanalysis, achieving notable distinguishers for up to 8-round SPECK32 and improved performance for other ciphers. This research highlights the potential of machine learning to enhance classical differential methods, providing a foundation for future studies to further optimize and generalize neural cryptanalysis techniques. Seok et al. (2024) proposed an innovative method for constructing high-quality differential datasets to enhance the performance of differential neural cryptanalysis. Utilizing Principal Component Analysis (PCA) and K-means clustering, the authors identified input differences that significantly improve the training accuracy of neural distinguishers. Their experiments on lightweight block ciphers SPECK and SIMON demonstrated that datasets optimized using their methodology achieved superior performance compared to traditional approaches, such as Gohr's neural difference search algorithm. The proposed algorithm reduced execution time by 30% while identify- ing more effective input differences. This study highlights the importance of dataset quality in cryptanalysis and proposes a scalable approach for generating optimized datasets within the context of machine learning-based cryptanalytic techniques.

In Wu et al. (2024) , Wu et al. explore the properties of mixture differentials and propose a mixture differential neural network distinguisher using ResNet to improve accuracy in cryptanalysis. Their research focuses on the SIMON32 cipher, demonstrating that the 8-round mixture differential neural network distinguisher achieves an accuracy improvement of 74.7% to 92.3% compared to previous methods. The mixture differential distinguisher is shown to be less sensitive to input differences and offers greater robustness. Additionally, by combining probabilistic expansion and neutral bit techniques, they extend the distinguisher to 11 rounds and perform a successful 12-round key recovery attack on SIMON32 with a key recovery accuracy of 55% , outperforming traditional differential neural network distinguishers.


## Contributions

We aim to improve upon the results of Wu et al. (2024) , Su et al. (2021) , Wang et al. (2022) as well as the baseline differential neural distinguishers. Results are described in Sect. 5, which can be summarized as follows:

• We introduce a data generation method based on multiple input polytope differences and polytopic differential analysis. This method reduces the sensitivity of distinguishers to input differences and eliminates the need for random differences for one of the labels.

• We enhance the accuracy of polytopic, mixture, and multiple differential neural distinguishers for the SIMON32 and introduce the first polytopic differential neural distinguishers for the 32-bit versions of the SIMECK and SPECK ciphers, both in the single-key and related-key scenarios. For SPECK32, our approach achieves 99.39% accuracy for 5 rounds, 91.22% for 6 rounds, 62.01% for 7 rounds, and 50.80% for 8 rounds. For SIMON32, our method improves the accuracy to 100% for 7 rounds, 98.47% for 8 rounds, and remains effective up to 12 rounds with an accuracy of 50.50%. For SIMECK32, we obtain 100% accuracy for 7 rounds, 98.97% for 8 rounds, and maintain effectiveness up to 12 rounds with an accuracy of 50.55%. These results are further improved in the related-key scenario for SIMON32 and SIMECK32, achieving up to 13 rounds with 50.59% accuracy and 15 rounds with 54.44% accuracy, respectively.

• We conduct a series of experiments to understand the intrinsic performance of neural distinguishers based on polytopic differential analysis. The results of these experiments indicate that the polytopic differential neural distinguisher learns and bases its distinctions on information beyond just the polytopic differential distribution and simple XOR operations. Additionally, ciphertexts provide more details to the distinguisher model than their differences. Furthermore, our distinguishers effectively differentiate between real polytopic differences and randomized differences.

We propose a framework for performing multiple-input polytopic differential neural cryptanalysis of several block ciphers. Our code and trained models are available on GitHub at https:// github. com/ Neura lDist ingui sher/ Multi ple-PDND. git .


## Organization

In Sect. 2, we discuss the necessary preliminary concepts, including the structure of the block ciphers under consideration, differential-neural distinguishers, and the idea of polytopic differential analysis. In Sect. 3, we describe our data generation method, which is based on the differences between multiple input polytopes. In Sect. 4, we describe the model architecture used for constructing the distinguishers, along with the training methodology and parameters. In Sect. 5, we present and compare the obtained results with previous works. Additionally, we describe the method for selecting input polytope differences. We also demonstrate the effectiveness of our method through a key recovery test. In Sect. 6, we present the experiments and additional findings. Finally, in Sect. 7, we summarize the paper.


## Preliminaries

This section provides an overview of the fundamental terms used in this paper. It includes an introduction to the block ciphers SIMON, SPECK, and SIMECK examined in this work, an explanation of the use of neural networks in differential cryptanalysis, and an overview of polytopic differential analysis.

Short description of SIMON, SPECK, and SIMECK Lightweight block ciphers SIMON and SPECK, proposed by the U.S. National Security Agency in 2013 Beaulieu et al. (2015), support block sizes ranging from 32 to 128 bits and key sizes from 64 to 256 bits. SIMON employs a Feistel structure with the bitwise AND function as the non-linear operation, while SPECK uses a traditional ARX structure (Addition, Rotation, XOR). SIMON is notable for its simplicity and efficiency in hardware implementations, whereas SPECK, due to its ARX operations, is optimized for software performance on modern processors. SIMECK, introduced at CHES 2015 Yang et al. ( 2015 ), is a family of lightweight block ciphers whose round function and key schedule were inspired by both SIMON and SPECK. Compared to these two ciphers, SIMECK achieves a more compact hardware implementation.

For the 32-bit versions of these ciphers, the round function takes as input two 16-bit words, (x i , y i ) , and a 16-bit round key, k i , derived from a 64-bit master key using a key schedule. The next-round state, (x i+1 , y i+1 ) , for SPECK, SIMON, and SIMECK, is computed using the following equations ( 1 ), (2), and (3), respectively. Here, ⊕ represents the bitwise XOR operation, & denotes the bitwise AND operation, ⊞ signifies modular addition, and the symbols ≫ and ≪ denote circular right and left shifts, respectively.

SIMON uses a linear key schedule, whereas SPECK and SIMECK employ their respective non-linear round functions to derive the round keys.


## Differential-neural distinguishers

Gohr introduced a neural differential distinguisher for round-reduced SPECK to distinguish ciphertext pairs with a specific input difference from random data Gohr (2019) . The model is trained using the following procedures:

• Collecting training data by generating N uniformly distributed keys and plaintext pairs given a fixed input difference and the binary labels Y i , where i ranges from 0 to N -1.

• If the binary label Y i = 1 , then the plaintext pairs are encrypted by r-round SPECK to produce the ciphertext pairs. Otherwise, random ciphertext pairs are generated.

(1)

• Pre-process ciphertext pairs to fit the format required by the neural network and start training.

Gohr's work shows that neural networks can be effectively trained to capture the non-randomness of target ciphers.

Given a particular input difference in and a target cipher, the neural network is trained to distinguish ciphertext pairs using in from random differences. These ciphertext pairs using in are labeled by 1, and those using random differences are labeled by 0.

Given enough training samples, a deep residual network (ResNet) is trained to distinguish between ciphertext data and random data. The neural network, acting as a distinguisher, outputs a value v ranging from 0 to 1. If v > 0.5 , the pair of ciphertexts is considered to use in ; otherwise, it is supposed to use a random difference. This trained neural network is referred to as a neural distinguisher (ND).

The effectiveness of neural distinguishers is further demonstrated by their ability to outperform classical differential cryptanalysis methods. For example, Gohr achieved better results than the best classical cryptanalysis on 11-round SPECK, showing the potential of machine learning in cryptanalysis.


## Overview of (related-key) polytopic cryptanalysis

Differential cryptanalysis examines how round function iterations transfer plaintext differences to ciphertext differences. Polytopic cryptanalysis Tiessen (2016) is a generalized framework extending traditional differential cryptanalysis by incorporating the interdependencies among larger sets of texts (polytopes) traversing through a cipher. Introduced formally in block cipher security analysis, this method evaluates the statistical relationships of multiple plaintext and ciphertext differences beyond pairwise dependencies. Polytopic transitions enable cryptanalysts to exploit higher-order differential structures and uncover subtle non-random features in cryptographic algorithms that traditional methods might overlook.

A transition involving a (d + 1)-polytope, denoted as (m 0 , m 1 , . . . , m d ) , is described as an s-tuple of values in F n 2 , where differences between texts in the polytope are analyzed relative to a reference text. These differences form the foundation of d-differences:

where m 0 is the anchor or reference text.

Similar to differential cryptanalysis, polytopic trails trace transitions over multiple rounds: with probabilities calculated over all possible intermediate transitions.

Related-key differential cryptanalysis, introduced by Biham in 1991 Biham (1994) , extends classical differential cryptanalysis by incorporating differences in the plaintexts and the master keys. In this approach, a pair of plaintexts P and P ′ is encrypted using a pair of related keys K and K ′ , respectively, where K ⊕ key = K ′ . The analysis focuses on exploiting differential propagation while encrypting these plaintexts with distinct keys, even if they are identical.

In polytopic differential analysis, this concept is extended to related-key settings by considering d + 1 polytopes in both the plaintext and key domains. A related-key polytopic distinguisher uses a (d + 1)-polytope (m 0 , m 1 , . . . , m d ) for the plaintexts and a corre- sponding (d + 1)-polytope for the keys (k 0 , k 1 , . . . , k d ) , where

The relative differences between these texts and keys form the foundation of d-differences:

This framework analyzes the propagation of polytopic differences through the cipher, represented as an r-round related-key polytopic differential transition. The formal representation of such a transition can be expressed as: where P and K denote the input plaintext and key differences, and ′ P and ′ K represent their corresponding output differences after r rounds.


## Dataset generation

The dataset generation process is crucial in training neural network distinguishers for cryptanalysis. This process ensures the model learns to identify non-random characteristics in ciphertext distributions by leveraging structured input differences.

We adopt the multiple input differences method, first introduced by Baksi and Baksi (2022) , to construct training data for single-key and related-key scenarios. This method generates plaintext and ciphertext quadruples with specific polytope differences, creating distinguishable patterns for the neural network.

In the single-key scenario, all plaintexts in a quadruple are encrypted with the same random key. In contrast, in the related-key scenario, the plaintexts are encrypted with related keys derived using predefined key differences. Both scenarios use distinct polytope differences for the positive (label 1) and negative (label 0) classes, ensuring structured output distributions that enhance

the neural network's distinguishing capabilities. The dataset generation process comprises the following steps:

1. Random selection of plaintexts and keys. 2. Application of polytope differences to create plaintext quadruples for both label classes. 3. Encryption of the plaintext quadruples using single or related keys to generate ciphertext quadruples. 4. Assignment of labels and storage of the generated data for training purposes.

The following subsections provide a detailed explanation of the dataset generation process for both single-key and related-key scenarios. Subsequently, a structured algorithm is presented to encapsulate the entire procedure.


## Single-key scenario

In the single-key scenario, all plaintexts within a quadruple are encrypted using the same randomly selected key, ensuring that the differences in the ciphertext quadruples are determined solely by the differences in the plaintexts. The generated ciphertext quadruples (C 0 , C 1 , C 2 , C 3 ) and their respective labels Y serve as the input for training the neural network distinguisher.

To construct the dataset, we generate a random plaintext P 0 and apply predefined polytope differences. For label 0, the polytope differences � = (� 1 , � 2 , � 3 ) are applied to P 0 , resulting in the plaintext quadruple: Similarly, for label 1, the polytope differences δ = (δ 1 , δ 2 , δ 3 ) are applied to generate: Each plaintext quadruple is then encrypted using the same randomly selected key K to produce the corresponding ciphertext quadruple: where: and:

The ciphertext quadruples, alongside their labels, form the training dataset for the neural network. The network learns to distinguish between label 0 and label 1 by identifying the statistical differences in the ciphertext

distributions resulting from the input plaintext differences and δ.

The detailed steps for generating the dataset in the single-key scenario are summarized in Algorithm 1.


## Algorithm 1 Dataset Generation for Single-Key Scenario


## Related-key scenario

In the related-key scenario, the plaintext quadruples, and the corresponding encryption keys are structured using predefined polytope differences. This enables a more comprehensive examination of the cipher's behavior under related-key settings, where the encryption keys are not independent but are derived from a master key through specific differences.

Given the input polytope differences � = (� 1 , � 2 , � 3 ) for label 0 and δ = (δ 1 , δ 2 , δ 3 ) for label 1, along with key differences � key = (α 1 , α 2 , α 3 ) for label 0 and δ key = (β 1 , β 2 , β 3 ) for label 1, the ciphertext quadruples (C 0 , C 1 , C 2 , C 3 ) and their associated labels Y are gener- ated for training.


## Key and Plaintext Generation

A random 32-bit plaintext P 0 and a random 64-bit key K are generated. The key K is then split into four parts: K = {l 0 , l 1 , l 2 , l 3 } . Related keys are derived as follows:

• For label 0:

• For label 1:

A plaintext quadruple is generated for each label:

• For label 0:

• For label 1:

Ciphertext Generation Each plaintext in the quadruple is encrypted using the corresponding related keys:

• For label 0:

• For label 1:

The resulting ciphertext quadruples (C 0 , C 1 , C 2 , C 3 ) , along with their labels, are used as input for the neural network. This structured approach leverages plaintext and key differences to enhance the neural network's ability to identify distinguishing characteristics in ciphertext distributions.

Algorithm 2 Dataset Generation for Related-Key Scenario C 0 = encrypt(P 0 , K ), C j = encrypt(P j , K j 0 ), j = 1, 2, 3.


## Network architecture

To effectively capture the complex patterns in polytopic differential cryptanalysis, we employ a deep learning model based on the architecture proposed by Bellini et al. (2023) . This section outlines the structure of the neural network, which utilizes dilated convolutional layers to enhance feature extraction and to improve model performance. The overall architecture of this model is illustrated in Fig. 1 .


## Input and Normalization

The input to our model consists of N samples, where the format and structure of each sample is a quadruple of ciphertexts along with their corresponding label, represented as (C 0 , C 1 , C 2 , C 3 , Y ) . In the main model, each sample from the dataset has four features, each 32 bits in length, and the processing is performed on this input format. The model begins with an input layer where the data is normalized to a range of [-1, 1] . This normalization step helps stabilize the training process and enhances the model's convergence. The input size is denoted by 4 × block size , which in this case is 128 bits (since the block size is 32 bits). Using dilated convolutional layers eliminates the need to reshape the input, allowing us to perform bit-oriented analysis directly. This is particularly beneficial for cryptographic analysis, where maintaining the data's bit-level structure is crucial.

Block 1 Block 1 consists of two dilated convolutional layers. The first convolutional layer uses a kernel size of 2, a stride of 1, 'valid' padding, and a dilation rate based on the input size. The second convolutional layer uses a kernel size of 2, a stride of 1, 'causal' padding, and a dilation rate of 1. Both convolutional layers are followed by batch normalization (BN) and ReLU activation functions. After each pair of convolutional layers, the number of filters is increased by 16. The dilation rates are calculated as follows:

where ⌊•⌋ represents the floor function, which returns the greatest integer less than or equal to the input value, dilation_rate(i) represents the dilation rate for the i-th layer, and 128 is the input size in bits. Dilated convolutions enable an exponential increase in the receptive field without compromising resolution or coverage, making them particularly useful for capturing long-range dependencies in data while maintaining computational efficiency.

Block 2 Block 2 consists of three fully connected (FC) layers, followed by batch normalization (BN) and ReLU activation functions. The first and second dense layers each have 256 neurons, while the third dense layer has 64 neurons. Additionally, an l 2 regularization with a param- eter of 10 -5 is applied to the dense layers to prevent overfitting.

Prediction Head The prediction head's final layer is a fully connected layer followed by a sigmoid activation function. This layer produces a binary decision, indicating whether the input data conforms to the expected differential pattern.

Despite the inherently random nature of cryptographic algorithms, deep learning models can identify subtle features and patterns that are not directly observable through traditional methods. The model can learn complex representations of the input data by leveraging the power of dilated convolutions and dense layers. These representations capture the underlying relationships between the input differences and the resulting ciphertexts, enabling the model to act effectively. The combination of advanced feature extraction techniques and extensive training on large datasets allows the neural network to detect non-randomness and differentiate between conforming and non-conforming data with high accuracy.


## Training distinguishers

The training strategy utilized in this paper adopts a progressive approach. First, a distinguisher for r rounds is trained. The trained weights are then used to initialize the model for the subsequent (r + 1) rounds. This incre- mental method enhances the model's capability to learn complex patterns effectively across different rounds.

The training continues until the validation accuracy falls below a specified threshold, ten times the standard deviation ( 10σ ) above the random baseline of 50% accuracy. The standard deviation for the accuracy is determined by the size of the dataset, N, and is given by: This criterion ensures that a distinguisher is deemed effective only if its performance exceeds random guessing by a statistically significant margin. During training, the accuracy is carefully monitored for both the training and testing datasets to ensure the reliability and generalization of the distinguisher. The detailed training process is described in Algorithm 3. The same method is used for training and evaluating RK-PDNDs in the related-key scenario.

The training process utilizes the Adam optimizer, which features a cyclic learning rate that ranges from 0.001 to 0.0002 over ten epochs. The model is trained for several epochs with early stopping based on validation accuracy. We chose a training set size of 10 7 sam- ples and a validation set size of 10 6 . We ran 120 epochs for each training, with a batch size of 10,000. The loss function used was Mean Squared Error (MSE). Additionally, each model was run 5 times, and the average accuracy of these five runs is reported.

The model training was performed using two Nvidia RTX 3060 Ti GPUs. The programming language used for data generation, model construction, and model training was Python 3.10. The training was executed on a machine with the following specifications: Intel i9-12900K CPU, 16 GB RAM, and Ubuntu LTS 22.04.4 operating system. The machine learning framework utilized was TensorFlow 2, with additional libraries such as NumPy and Pandas.

Algorithm 3 Training PDNDs


## Testing process

The trained model is evaluated by making predictions on unseen ciphertext quadruples. For each quadruple, the model outputs a prediction score v ∈ (0, 1) , which indicates the likelihood that the ciphertext quadruple is derived from a plaintext quadruple conforming to the input polytopic pattern. The testing process is conducted on a separate test dataset of 10 6 samples to measure the model's perfor- mance. The dataset is composed of ciphertext quadruples generated using two distinct polytopic differences:

• Polytopic Difference : Corresponding to label 0.

• Polytopic Difference δ : Corresponding to label 1.

For each input quadruple, the model determines whether it was generated using or δ . A higher value of v (closer to 1) indicates the model's confidence in distinguishing between the distributions associated with these two polytopic differences.

Additionally, the model can differentiate between genuine data-ciphertext quadruples generated by encrypting plaintexts using the target block cipher-and random data, which does not conform to any structured polytopic pattern. This demonstrates the model's robustness in identifying structured patterns within ciphertext distributions.


## Results

This section presents the results obtained for our distinguishers on the SPECK32, SIMON32, and SIMECK32 ciphers in two scenarios: single-key and related-key. We analyze the performance and accuracy of the neural distinguishers in both settings to evaluate their effectiveness and robustness. In addition, we describe the method for selecting input polytope differences, which significantly improves the accuracy of our neural distinguishers. Furthermore, we demonstrate the applicability of our approach through a key recovery test, where the distinguishers effectively distinguish between correct and incorrect keys.


## Single key polytopic differential neural distinguishers

This section compares the neural distinguishers obtained in this work and those from previous research. The results are shown in Table 1 .

For our experiments, we used specific polytope differences for each cipher as follows:

For SPECK32, we used the polytope differences and � = ((0x40, 0x0), (0x0, 0x8000), (0x60, 0x0)) δ = ((0x20, 0x0), (0x40, 0x8000), (0x10, 0x2000)).

For SIMON32 and SIMECK32, we used the polytope differences and The neural distinguishers were trained using the method described in SubSect. 4.1. The Table 1 summarizes the accuracy of the single key distinguishers for different rounds of SPECK32, SIMON32, and SIMECK32. The results show improvements in accuracy compared to previous works. For a fair comparison, we used papers with � = ((0x0, 0x1), (0x0, 0x4), (0x0, 0x8)) δ = ((0x0, 0x2), (0x0, 0x10), (0x0, 0x40)).

similar features, a comparable number of samples, and no staged training or advanced feature engineering. These results demonstrate that our method, which utilizes two polytope differences and a ResNet-based neural network architecture, significantly improves the accuracy of baseline neural distinguishers for multiple rounds of SPECK32, SIMON32, and SIMECK32 compared to previous methods. Polytope differences reduce the distinguisher model's sensitivity to the specific input difference, making it more robust. Additionally, employing two distinct sets of differences for the positive and negative classes (instead of random differences for the negative class) enhances the separability of the output distributions for both labels, thereby improving the model's ability to distinguish between them.


## Related-key polytopic differential neural distinguishers

This subsection presents the results for the related-key polytopic differential neural distinguishers (RK-PDNDs) for SPECK32, SIMON32, and SIMECK32. The analysis was conducted similarly to the single-key scenario, using the same parameters but with related keys. The results are summarized in Table 2 . For SPECK32, the input key differences used were For SIMON32, the input key differences were For SIMECK32, the input key differences were

The input polytope difference values and δ for the plaintexts are the same as the values mentioned in SubSect. 5.1.

The results in Table 2 show that for SPECK32, the number of rounds distinguished by the RK-PDND is similar to that of the PDND. Still, the accuracy in the related-key scenario is generally lower. This indicates the resistance of SPECK's key schedule algorithm to this analysis, which does not provide additional features or information to the model in the related-key scenario. However, for SIMON32 and SIMECK32, the number of rounds distinguished by the RK-PDND is higher than that of the PDND, and the accuracy for all rounds in the related-key scenario is significantly better.

� key = (0x0040, 0x8000, 0x0060), δ key = (0x0020, 0x8000, 0x2000).

� key = (0x0, 0x8000, 0x0), δ key = (0x0, 0x8000, 0x2000).

� key = (0x1, 0x4, 0x8), δ key = (0x0020, 0x0010, 0x0040).

When the number of rounds distinguished for SIMON32 and SIMECK32 is compared, we observe that the number of rounds and accuracy in the single key scenario are almost similar. However, in the related-key scenario, SIMECK32 shows more distinguishable rounds and better accuracy than SIMON32. This suggests that SIMON32's linear key schedule provides more resistance against related-key polytope differential neural analysis compared to the non-linear key schedule of SIMECK32, which uses its round function for key distribution.


## On the choice of polytope input differences

The selection of polytope input differences plays a crucial role in the effectiveness of our neural distinguishers. A well-chosen polytope difference can significantly enhance the performance of the distinguisher by optimizing its ability to identify distinguishing features across cipher rounds. In this section, we discuss the importance of polytope input differences, the criteria for selecting suitable differences, the methodology used in this study, and the impact of these choices compared to previous work, particularly Baksi and Baksi (2022) .

The primary factor influencing the selection of polytope input differences is minimizing the Hamming weight of the differences. Lower Hamming weight differences reduce the dispersion of the difference across the cipher rounds, making it easier for the neural distinguisher to identify and classify the distribution of differences. This is because differences with high Hamming weights tend to spread more widely, making them less predictable and more challenging to track through the rounds of the cipher. By keeping the Hamming weight SPECK32 6 ((0x40, 0x0), (0x0, 0x8000), (0x60, 0x0)) ((0x20, 0x0), (0x40, 0x8000), (0x10, 0x2000)) 91.33 ((0x40, 0x0), (0x8000, 0x0), (0x20, 0x0)) ((0x100, 0x0), (0x40, 0x0), (0x1, 0x0)) 91.00 ((0x0, 0x1), (0x0, 0x4), (0x0, 0x8)) ((0x0, 0x20), (0x0, 0x10), (0x0, 0x40)) 89.40 ((0x0, 0x10), (0x0, 0x8000), (0x0, 0x400)) ((0x100, 0x0), (0x40, 0x0), (0x2, 0x0)) 88.99 ((0x0, 0x10), (0x0, 0x6000), (0x0, 0x400)) ((0x100, 0x8), (0x40, 0x0), (0x2, 0x0)) 83.34 ((0x0, 0x10), (0x0, 0x8), (0x10, 0x0)) ((0x100, 0x40), (0x40, 0x8), (0x1, 0x2000)) 54.30 ((0x0, 0x40), (0x3000, 0x0), (0x0, 0x6)) ((0x100, 0x6), (0x40, 0x8), (0x2, 0x3)) 50.00 SIMON32 8 ((0x0, 0x1), (0x0, 0x4), (0x0, 0x8)) ((0x0, 0x2), (0x0, 0x10), (0x0, 0x40)) 98.47 ((0x0, 0x1), (0x0, 0x3), (0x0, 0x6)) ((0x0, 0x2), (0x8, 0x10), (0x1, 0x40)) 94.71 ((0x20, 0x1), (0x0, 0x4), (0x0, 0x100)) ((0x2, 0x0), (0x0, 0x80), (0x0, 0x10)) 93.80 ((0x0, 0x80), (0x0, 0x100), (0x0, 0x8)) ((0x0, 0x20), (0x0, 0x40), (0x0, 0x10)) 93.71 ((0x1, 0x0), (0x4, 0x0), (0x8, 0x0)) ((0x0, 0x2), (0x0, 0x10), (0x0, 0x40)) 86.80 ((0x0, 0x4002), (0x0, 0x4001), (0x0, 0x2001)) ((0x3, 0x0), (0x2, 0x0), (0x1, 0x0)) 60.99 ((0x1, 0x8000), (0x4000, 0x2), (0x200, 0x8)) ((0x40, 0x80), (0x200, 0x4), (0x1000, 0x20)) 59.61 low, the propagation of the difference across rounds is more concentrated, which leads to a more effective distinguisher. Moreover, the placement of the active bit in the input difference is also critical. For SIMON-like ciphers (SIMON and SIMECK), placing the active bit in the right word (i.e., in the form (0, e i ) ) was found to yield better results. For the SPECK cipher, the placement of the active bit in either of the two words can yield effective results; however, typically placing it in the left word produces better outcomes for the neural distinguisher. This strategic placement of active bits ensures that the differences propagate efficiently, optimizing the distinguisher's ability to detect them.

In this work, the polytope input differences were selected through an extensive experimental evaluation of various potential differences. We tested several polytope differences, adjusting their Hamming weights and the placement of active bits, and selected the differences that provided the best performance for each cipher. This process allowed us to identify the most effective polytope differences for SPECK32, SIMON32, and SIMECK32. It is essential to note that the differences chosen in this study differ from those used in previous work, particularly Baksi and Baksi (2022) . While the method presented in Baksi and Baksi (2022) relies on pure differential analysis, our approach employs polytopic differential analysis, which allows for greater flexibility in selecting input differences and thus enables better optimization of the neural distinguisher's performance. For example, the best neural distinguisher reported in Baksi et al. (2023) as an extension of the work in Baksi and Baksi (2022) for the SIMECK32 cipher was achieved for 9 rounds, whereas we extend the analysis to 13 and 15 rounds, demonstrating the robustness of our method in handling more complex cases.

In this study, various polytope input differences were evaluated to determine their impact on the performance of the neural distinguisher. Based on the findings and discussions provided in this section, Table 3 presents a comparison of the performance and effect of several polytope input differences on the neural distinguishers for 6-round SPECK32 and 8-round SIMON32. The table highlights the influence of different input differences on the accuracy of the distinguisher.

In conclusion, the choice of polytope input differences is a critical factor in optimizing the performance of neural distinguishers. By minimizing the Hamming weight and carefully selecting the placement of active bits, we improved the effectiveness of the distinguisher for SIMON-like and SPECK ciphers. The flexibility in choosing polytope differences, combined with polytopic differential analysis, has enabled better performance compared to previous approaches, as demonstrated by our experiments and the results presented in this paper.


## Key recovery test

This section presents a key recovery test to evaluate the ability of our neural distinguishers to distinguish between correct and incorrect subkeys. The primary goal is to assess the potential of our distinguishers in recovering the correct subkey through partial decryption and to demonstrate their applicability in cryptanalysis.

To show the effectiveness of the proposed neural distinguishers as research tools, we developed a partial key recovery attack utilizing the r-round distinguishers for the lightweight block ciphers SIMON32, SIMECK32, and SPECK32. In this approach, we focus on evaluating the performance of the neural network model trained using an r-round distinguisher for each of the target encryption algorithms. The model is tested to see how accurately it can predict the correct subkey as compared to incorrect ones when extended to r + 1 rounds.

The key recovery test is performed as follows:

1. After training the neural network model, we select 10 6 plaintext quadruple samples. A fixed key is applied to all these samples. 2. The corresponding ciphertext quadruples are generated using r + 1 rounds of the encryption algorithm. 3. These r + 1 round ciphertext quadruples are then partially decrypted using both the correct key and a set of random incorrect keys, with one round of decryption applied in each case. 4. For each resulting ciphertext quadruple, input features for the neural network model are generated as described in Sect. 3. 5. The accuracy of the model is then evaluated based on its ability to distinguish the correct key from incorrect ones.

This process is repeated across 100 different random keys, and the average accuracy is calculated. The expected result is that, for the correct key, the model's accuracy should closely match the accuracy achieved with the r-round distinguisher. For incorrect keys, the accuracy should be approximately 0.5, which is close to random guessing. For the single key experiments involving SIMON32, SIMECK32, and SPECK32, we applied the key recovery test for r + 1 rounds ranging from r = 5 to r = 8 for SPECK32 and r = 8 to r = 11 for SIMECK32 and SIMON32, based on the distinguishers and their accuracies presented in Table 1 . Additionally, we extended this key recovery test to related-key scenarios for r + 1 rounds, using related-key distinguishers for SIMON32, SIMECK32, and SPECK32. Notably, these included distinguishers for up to 12 rounds of SIMON32, and up to 12 to 15 rounds of SIMECK32, as shown in Table 2 . The results for distinguishers with accuracy below 51% were excluded due to their proximity to random guessing.

Figures 2 , 3 , and 4 present the model's accuracy in distinguishing between correct and incorrect subkeys for both single-key and related-key scenarios. The left columns of the figures show the accuracy when the correct keys are used, while the right columns illustrate the performance with random keys. Specifically, Fig. 2 focuses on the 6 to 9 rounds of SPECK32 in the singlekey scenario, Fig. 3 covers 10 to 13 rounds of SIMON32 for both single-key and related-key and Fig. 4 demonstrates the results for 13 to 16 rounds of SIMECK32 in the related-key scenario. As demonstrated in these figures, our proposed neural network model effectively distinguishes between correct and incorrect keys for r + 1 rounds, showcasing its capability in key recovery tasks. As illustrated in the corresponding figures, we observe that as the number of rounds increases, the accuracy of the distinguisher in differentiating between the correct key and incorrect keys tends to decrease. This trend is expected, since the cryptographic structure becomes more complex and the statistical differences between correct and incorrect keys become less pronounced in higher rounds. However, this reduction in accuracy can be partially compensated by increasing the number of samples and utilizing larger, more diverse datasets for both training and evaluation. Additionally, as the number of samples increases, the average score assigned by the distinguisher to the correct key becomes closer to the neural distinguisher's accuracy. In practical key recovery attacks as well, the lower accuracy of the distinguisher can generally be compensated by increasing the data complexity Chen et al. (2023) . Conversely, reducing the number of dataset samples leads to a decrease in the distinguisher's accuracy, and consequently, a lower neural distinguisher score for the correct key.

In comparison to the key recovery results for 11-round and 12-round SIMON32 presented in Su et al. (2021) and Wu et al. (2024) , our distinguishers, without the complexity of adding additional rounds, have been extended to 12 rounds in the single-key scenario and 13 rounds in the related-key scenario, as explained above. Furthermore, the key recovery presented in Wang et al. (2022) for SIMECK32 was for 11 rounds, but in this section, using our PDND distinguishers, it has been extended to 12 rounds in the single-key scenario and up to 16 rounds in the related-key scenario.

In addition, leveraging the first subkey addition after the initial nonlinearity application, all distinguishers discussed in this paper can be extended by one additional round at no extra cost. In a chosen-plaintext scenario, an adversary can easily introduce plaintext polytope differences into the output of the first round of SIMON, SIMECK, or SPECK, making it possible to apply the key recovery attack for 1 + r + 1 rounds with the PDNDs.

Based on this, Table 4 provides a comparative analysis of deep learning-based attacks on SPECK32, SIMON32, and SIMECK32. Rows highlighted in Bold indicate distinguishers with higher data complexity, which are not directly comparable. Works that did not perform key recovery are marked with "-", and certain studies (e.g., Lu et al. 2024; Ebrahimi et al. 2023; Wang et al. 2024 ) are excluded due to their incomparable complexity and lack of key recovery evaluation.

Table 4 demonstrates that our proposed neural distinguishers not only achieve high accuracy in distinguishing correct and incorrect keys but also enable competitive or improved attacks compared to prior works. Additionally, by identifying a suitable s-round polytopic differential characteristic with a high probability (where its output difference matches the input difference of the r-round neural distinguisher) and leveraging neutral bits Bao et al. (2022) to generate ciphertext structures, this characteristic can be prepended to the neural distinguisher. This extends the total attack rounds to 1 + s + r + 1 , fur- ther enhancing the cryptanalytic reach.

Computational complexity in key recovery attacks is typically measured by the number of required encryption (and decryption) operations. In contrast, data complexity refers to the number of plaintext samples utilized during the attack. In practical attacks, when the neural distinguisher achieves high accuracy, the correct key is often recovered rapidly, and not all theoretically required data is necessarily used Zhang et al. (2024) . The success rate (SR) in key recovery experiments can be defined based on different criteria. For example, in Zhang et al. (2023) , the success rate is defined as the ratio of successfully recovered subkeys to the total number of experiments. An experiment is considered successful when the overall SR reaches 99%, i.e., for an experiment count n e that sat- isfies 1 -(1 -SR) n e = 0.99.

In our key recovery tests, the SR can be defined as the fraction of times the neural distinguisher distinguishes the correct key from incorrect keys, or as the fraction of times the mean distinguisher score for the correct key matches the accuracy of the neural distinguisher. Using the first metric, we observed an SR of 100%; using the second metric, and with a standard deviation of 0.03, the SR remains at 100%. Moreover, as the difference between the mean output scores for the correct and incorrect keys increases, the SR also improves. In general, increasing computational complexity will further enhance the SR in practical attacks Chen et al. (2023) . In contrast to traditional differential cryptanalysis, neural network-based methods require only the input difference, allowing them to capture a wider spectrum of output differences and thereby enabling more effective key recovery attacks Hou et al. (2021) .

On another note, based on the findings in Baksi et al. (2021) , it may also be feasible to recover (part of ) the round key using the linear inequality generated by the Support Vector Machine (SVM), instead of the neural network. In summary, this section highlights that our PDNDs are valuable tools for cipher designers to evaluate security margins and empower attackers to mount key recovery attacks. The results underscore the dual utility of neural distinguishers in both defensive and offensive cryptographic research.


## Experiments

In this section, we conduct experiments to evaluate the intrinsic performance and learning mechanisms of neural distinguishers based on polytopic differential analysis. Additionally, we explore methods to improve their accuracy. The experiments are conducted in a single-key scenario.


## Training with output polytope differences

In the first set of experiments, we modify the training data to use output polytope differences instead of ciphertexts. Specifically, we calculate the polytope differences of the ciphertexts and use these differences as input to the neural distinguishers. The input data format for the model becomes (C 0 ⊕ C 1 , C 0 ⊕ C 2 , C 0 ⊕ C 3 ) along with their corresponding labels, where ⊕ denotes the XOR operation. This approach allows the model to focus on the polytopic differential properties of the ciphertexts.

For each sample, we generate four plaintexts (P 0 , P 1 , P 2 , P 3 ) and encrypt them to obtain the cipher- texts (C 0 , C 1 , C 2 , C 3 ) based on Algorithm 2. The input polytope differences are similar to those in SubSect. 5.1. The output polytope differences are then calculated as (C 0 ⊕ C 1 , C 0 ⊕ C 2 , C 0 ⊕ C 3 ).

The results of this experiment are summarized in Table 5 . Based on the results in Table 1 and the comparison with using ciphertext inputs, it is evident that the accuracy of neural distinguishers decreases when the input is limited to the output polytope differences rather than the full ciphertexts.

For the SPECK32 cipher, the accuracy of distinguishers trained on output polytope differences shows a significant decrease compared to those trained on ciphertexts. For instance, the 7-round accuracy drops from 62.01% to 61.02%. Similarly, for the SIMON32 cipher, the accuracy for nine rounds drops from 83.93% to 65.15%. For the SIMECK32 cipher, the 9-round accuracy drops from 86.13% to 67.51%.

This reduction in accuracy indicates that when the model is restricted to the polytope differences of the four ciphertexts and does not have access to the full ciphertexts, its ability to distinguish between samples decreases. The number of rounds that can be accurately distinguished also decreases by at least one round for SIMON32 and SIMECK32 ciphers.

These findings suggest that the ciphertext quadruples give the model more features and information than the output polytope differences. Similar to differential neural distinguishers, the PDND can extract more valuable features from the ciphertexts, which are not limited to the differential properties but also include relationships between the bits of the ciphertexts and linear approximations of them, as well as information from the penultimate and antepenultimate rounds of the encryption algorithm Benamira et al. (2021) . This additional information allows the model to achieve higher accuracy and distinguish more rounds than using only the polytope differences.


## Applying input differences from classical mixture differential characteristics

To investigate whether the neural distinguisher can achieve better accuracy using the input difference from the r-round mixture differential path, we compare its performance with classical mixture input differences used in previous research. Specifically, we utilize the characteristic from the paper Qiao et al. (2024) for the SIMON32 cipher.

According to Table 10 in Qiao et al. (2024) , the input mixture difference determined for the 17-round distinguisher of SIMON32 is: In this experiment, we use this value as the input polytope difference for our neural distinguisher and generate the corresponding ciphertexts for label 1 using this input difference. The ciphertexts corresponding to label 0 will have random differences. Table 6 compares the results obtained from this experiment with those from Wu et al. (2024) and the single-key distinguishers obtained in our study. As shown in Table 6 , the results for the neural distinguishers trained with the input difference from Qiao et al. (2024) appear to be less satisfactory, with significantly lower accuracy and performance compared to the differential neural distinguishers trained with the input differences from Wu et al. (2024) and our study.

Based on the test results, it seems that the polytope differential neural distinguisher does not perform as well using the input difference from the r-round mixture differential path. However, it is important to note that the classical characteristic may not be the most suitable for this task, and other factors might contribute to the observed performance.

Additionally, while one of the advantages of PDNDs is their lower sensitivity to input differences compared to differential neural distinguishers, it remains essential to choose appropriate differences. It appears that the selected differences, such as those in differential neural distinguishers, should have a Hamming weight of 1 to ensure effective results. Despite the inherent robustness of PDNDs, arbitrary differences may not yield satisfactory performance.


## Real polytope differences experiment

Inspired by Aaron Gohr's experiments on neural differential distinguishers, we will perform a similar experiment to investigate how well our neural distinguishers can differentiate between real and randomized polytope differences.

Previous work has shown that neural distinguishers trained on differential properties can effectively recognize reduced-round versions of block ciphers. These experiments generated a set of ciphertext pairs, and half of them were randomized by applying a blinding value. � = ((0x0001, 0x1150), (0x0100, 0x0444), (0x0101, 0x4104)).

The neural distinguishers were then tasked with distinguishing between the real and randomized pairs. The results demonstrated that the neural distinguishers could identify real differences without explicit training for this task, leveraging inherent features within the data Gohr (2019) . We aim to replicate and extend this experiment using our polytopic differential analysis approach. We will generate a set of ciphertext quadruples (C 0 , C 1 , C 2 , C 3 ) and then randomize half using a random blinding value R. The neural distinguishers will be tasked with classifying these quadruples as either real or random. This experiment will help us determine whether our polytopic differential neural distinguishers can extract additional information from the ciphertexts, achieving similar or better distinguishing accuracy compared to the baseline differential neural distinguishers.


## Experimental steps

• Data Generation: Generate 10 6 samples of ciphertext quadruples (C 0 , C 1 , C 2 , C 3 ) using the polytopic dif- ferential method described earlier (Algorithm 1). The input polytope differences are aligned with those presented in SubSect. 5.1.

• Randomization: Apply a random blinding value R to half of the samples to produce randomized ciphertext quadruples (C 0 ⊕ R, C 1 ⊕ R, C 2 ⊕ R, C 3 ⊕ R).

• Classification: Use pre-trained neural distinguishers to classify the ciphertext quadruples as real or random based on the polytope differences.

• Evaluation: Measure the accuracy of the neural distinguishers in distinguishing between real and randomized samples.

By conducting this experiment, we aim to validate whether the neural distinguishers based on polytopic differential analysis can effectively identify real differences and leverage additional features from the ciphertexts, similar to the findings in Gohr (2019) . Given the similar behavior of distinguishers for the SIMON and SIMECK ciphers, we will conduct this experiment on the 5-round SPECK and 7-round SIMON ciphers. The results of this experiment indicate that, despite not being specifically trained for this task, the polytopic differential neural distinguishers can effectively distinguish between the generated samples. This demonstrates that the distinguishers can learn information beyond a simple XOR and identify more complex patterns. The results of this experiment are also shown in Table 7 .


## Discussion on utilizing advanced methods for further enhancing PDNDs

This subsection discusses various methods for transforming our basic neural distinguishers into advanced models with improved performance and accuracy. These methods are primarily based on selecting an optimal neural network, optimizing its parameters, and feature engineering.

The first method for enhancing the performance of distinguishers involves selecting and employing a better, often more complex, neural network. The most crucial aspect of this task is optimizing the hyperparameters of the network according to the specific task assigned to the model. In addition, choosing a more sophisticated training method, such as staged training Gohr (2019) , can also lead to higher accuracy for the neural distinguishers.

The second category of methods for improving the performance of neural distinguishers is related to data generation and feature engineering techniques. Among these, the most critical aspect is the input data format to the model and its features. The more these features include information about the structure of the target cipher algorithm, the better the performance of the neural distinguisher. These features can include, for instance, information from the penultimate rounds of the cipher algorithm, which can be added to the input samples. For example, one can compute the right-branch input differences of the last round of the SPECK cipher without involving the subkey and provide this to the model.

Multiple ciphertexts per sample can further enrich the input data and improve model performance. In Chen et al. (2023), Chen and Yu developed neural distinguisher models for cryptanalysis that utilize features derived from multiple pairs of ciphertexts. This new model utilizes non-uniform distributions to generate derived features that are absent in single ciphertext pairs. The neural distinguishers achieve higher distinguishing accuracy by incorporating these derived features than baseline models. Experiments demonstrate that this approach significantly enhances distinguishing capability and improves key recovery attacks.

Therefore, the performance of basic neural distinguishers can generally be significantly improved by employing different models and optimizing their parameters following cryptanalysis and feature engineering, considering the structure of the cipher algorithm and the analysis method.


## Conclusion

In this paper, we introduced Multiple Input Polytopic Differential Neural Distinguishers (PDNDs) for the SIMON, SIMECK, and SPECK block ciphers, leveraging deep learning techniques and the ResNet architecture to enhance the effectiveness of neural distinguishers. By utilizing multiple polytope differences for data generation, our approach significantly improved the ability of the distinguishers to detect specific differential patterns in ciphertexts. Experimental results in both single-key and related-key scenarios demonstrated that PDNDs consistently outperformed baseline differential neural distinguishers in terms of accuracy.

Furthermore, through extensive experimentation, we examined the intrinsic behaviors and performance characteristics of our neural distinguishers. These investigations allowed us to address various aspects, including enhancing previous results, extending the attack to previously untested ciphers, and analyzing the underlying mechanisms of the distinguishers.

Our findings underscore the potential of advanced neural network architectures combined with multiple input polytope differences as powerful tools in cryptanalysis. Future research could explore the application of these techniques to other cryptographic primitives, develop more sophisticated models, automate the search for optimal polytope differences, and extend the use of deep learning to classical cryptanalytic attacks, thereby unlocking further opportunities in this domain.

> 1 Fig. 1 Fig. 1 Architecture of the model

> 2 Fig. 2 Fig.2PDND scores for single-key key recovery tests across 6 to 9 rounds of SPECK32

> 3 Fig. 3 Fig.3PDND scores for single-key key recovery tests across 10 to 12 rounds of SIMON32 and 13 rounds for related-key

> 4 Fig. 4 Fig.4PDND scores for related-key key recovery tests across 13 to 16 rounds of SIMECK32

> 1 Table 1 Comparison of our single-key polytopic differential neural distinguishers for SPECK32, SIMON32 and SIMECK32 with previous research

> 3 Table 3 Comparison of the performance of different polytope input differences for 6-round SPECK32 and 8-round SIMON32

> 4 Table 4 Summary of deep learning-based attacks on target algorithms† Reported values are obtained from the execution of the key recovery test presented in SubSect. 5.4. ⋆ The staged training method is used to train the ND model (higher data complexity).N, training data complexity; N ′ , testing data complexity; SR, success rate for key recovery; Time, time (computational) complexity; Data, data complexity; DND, differential neural distinguisher; NASA, neural-aided statistical attack; PDND, polytopic differential neural distinguisher; RK-PDND, related-key polytopic differential neural distinguisher; MDND, mixture differential neural distinguisher; MDND*, multiple differential neural distinguisher; -, key recovery not attempted or not reported

> 5 Table 5 Accuracy of neural distinguishers trained with output polytope differences (C 0 ⊕ C 1 , C 0 ⊕ C 2 , C 0 ⊕ C 3 )

> 6 Table 6 Comparison of neural distinguishers' performance with different input differences

> 7 Table 7 Results of neural distinguishers on real polytope differences for 5-round SPECK and 7-round SIMON

## Acknowledgements

We would like to thank the anonymous reviewers for their valuable comments and suggestions, which have greatly improved the content and presentation of this paper.

## References

1. b0: Blanka Klimova, Marcel Pikhart, Alice Delorme Benites, Caroline Lehr, Christina Sanchez-Stockhammer. "Neural machine translation in foreign language teaching and learning: a systematic review". Education and Information Technologies. 2023. DOI: 10.1007/s10639-022-11194-2
2. b1: Der-Hau Lee, Jinn-Liang Liu. "End-to-end deep learning of lane detection and path prediction for real-time autonomous driving". Signal, Image and Video Processing. 2023. DOI: 10.1007/s11760-022-02222-2
3. b2: Loïc Masure, Cécile Dumas, Emmanuel Prouff. "A Comprehensive Study of Deep Learning for Side-Channel Analysis". IACR Transactions on Cryptographic Hardware and Embedded Systems. 2020. DOI: 10.46586/tches.v2020.i1.348-375
4. b3: Eli Biham, Adi Shamir. "Differential cryptanalysis of DES-like cryptosystems". Journal of Cryptology. 1991-01. DOI: 10.1007/bf00630563
5. b4: Mitsuru Matsui. "Linear Cryptanalysis Method for DES Cipher". Lecture Notes in Computer Science. 1993. DOI: 10.1007/3-540-48285-7_33
6. b5: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019-08-18. DOI: 10.1007/978-3-030-26951-7_6
7. b6: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun. "Deep Residual Learning for Image Recognition". 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2016-06. DOI: 10.1109/cvpr.2016.90
8. b7: Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks, Louis Wingers. "The SIMON and SPECK lightweight block ciphers". Proceedings of the 52nd Annual Design Automation Conference. 2015-06-07. DOI: 10.1145/2744769.2747946
9. b8: Gangqiang Yang, Bo Zhu, Valentin Suder, Mark D Aagaard, Guang Gong. "The Simeck Family of Lightweight Block Ciphers". Lecture Notes in Computer Science. 2015. DOI: 10.1007/978-3-662-48324-4_16
10. b9: Heng-Chuan Su, Xuan-Yong Zhu, Duan Ming. "Polytopic Attack on Round-Reduced Simon32/64 Using Deep Learning". Lecture Notes in Computer Science. 2020. DOI: 10.1007/978-3-030-71852-7_1
11. b10: Adrien Benamira, David Gerault, Thomas Peyrin, Quan Quan Tan. "A Deeper Look at Machine Learning-Based Cryptanalysis". Lecture Notes in Computer Science. 2021-10-17. DOI: 10.1007/978-3-030-77870-5_28
12. b11: Gao Wang, Gaoli Wang, Yu He. "Improved Machine Learning Assisted (Related-key) Differential Distinguishers For Lightweight Ciphers". 2021 IEEE 20th International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom). 2021-10. DOI: 10.1109/trustcom53373.2021.00039
13. b12: Zezhou Hou, Jiongjiong Ren, Shaozhen Chen. "Improve Neural Distinguishers of SIMON and SPECK". Security and Communication Networks. 2021-12-31. DOI: 10.1155/2021/9288229
14. b13: Huijiao Wang, Jiapeng Tian, Xin Zhang, Yongzhuang Wei, Hua Jiang. "Multiple Differential Distinguisher of SIMECK32/64 Based on Deep Learning". Security and Communication Networks. 2022-09-14. DOI: 10.1155/2022/7564678
15. b14: Lijun Lyu, Yi Tu, Yingjie Zhang. "Improving the Deep-Learning-Based Differential Distinguisher and Applications to Simeck". 2022 IEEE 25th International Conference on Computer Supported Cooperative Work in Design (CSCWD). 2022-05-04. DOI: 10.1109/cscwd54268.2022.9776036
16. b15: Lijun Lyu, Yi Tu, Yingjie Zhang. "Deep Learning Assisted Key Recovery Attack for Round-Reduced Simeck32/64". Lecture Notes in Computer Science. 2022. DOI: 10.1007/978-3-031-22390-7_26
17. b16: Zhenzhen Bao, Jian Guo, Meicheng Liu, Li Ma, Yi Tu. "Enhancing Differential-Neural Cryptanalysis". Lecture Notes in Computer Science. 2022. DOI: 10.1007/978-3-031-22963-3_11
18. b17: Anna Hambitzer, David Gerault, Yun Ju Huang, Najwa Aaraj, Emanuele Bellini. "NNBits: Bit Profiling with a Deep Learning Ensemble Based Distinguisher". Lecture Notes in Computer Science. 2023. DOI: 10.1007/978-3-031-30872-7_19
19. b18: Yi Chen, Yantian Shen, Hongbo Yu, Sitong Yuan. "A New Neural Distinguisher Considering Features Derived From Multiple Ciphertext Pairs". The Computer Journal. 2023. DOI: 10.1093/comjnl/bxac019
20. b19: A Gohr, G Leander, P Neumann. "Figure 5: The framework of basic and enhanced related-key differential neural distinguishers.". Cryptology ePrint Archive. 2022. DOI: 10.7717/peerj-cs.2566/fig-5
21. b20: Emanuele Bellini, David Gerault, Anna Hambitzer, Matteo Rossi. "A Cipher-Agnostic Neural Training Pipeline with Automated Finding of Good Input Differences". IACR Transactions on Symmetric Cryptology. 2023-09-19. DOI: 10.46586/tosc.v2023.i3.184-212
22. b21: Anubhab Baksi, Jakub Breier, Vishnu Asutosh Dasu, Xiaolu Hou, Hyunji Kim, Hwajeong Seo. "New Results on Machine Learning-Based Distinguishers". IEEE Access. 2023. DOI: 10.1109/access.2023.3270396
23. b22: Byoungjin Seok, Changhoon Lee. "A Novel Approach to Construct a Good Dataset for Differential-Neural Cryptanalysis". IEEE Transactions on Dependable and Secure Computing. 2024. DOI: 10.1109/tdsc.2024.3387662
24. b23: Zehan Wu, Kexin Qiao, Zhaoyang Wang, Junjie Cheng, Liehuang Zhu. "Mixture Differential Cryptanalysis on Round-Reduced SIMON32/64 Using Machine Learning". Mathematics. 2024-05-03. DOI: 10.3390/math12091401
25. b24: Tyge Tiessen. "Polytopic Cryptanalysis". Lecture Notes in Computer Science. 2016-05-08. DOI: 10.1007/978-3-662-49890-3_9
26. b25: Eli Biham. "New types of cryptanalytic attacks using related keys". Journal of Cryptology. 1994-12. DOI: 10.1007/bf00203965
27. b26: Anubhab Baksi, Anubhab Baksi. "Machine Learning-Assisted Differential Distinguishers for Lightweight Ciphers". Computer Architecture and Design Methodologies. 2022. DOI: 10.1007/978-981-16-6522-6_6
28. b27: Yi Chen, Yantian Shen, Hongbo Yu. "Neural-Aided Statistical Attack for Cryptanalysis". The Computer Journal. 2023. DOI: 10.1093/comjnl/bxac099
29. b28: Jinyu Lu, Guoqiang Liu, Bing Sun, Chao Li, Li Liu. "Improved (Related-Key) Differential-Based Neural Distinguishers for SIMON and SIMECK Block Ciphers". The Computer Journal. 2024. DOI: 10.1093/comjnl/bxac195
30. b29: Amirhossein Ebrahimi, David Gerault, Paolo Palmieri. "Deep Learning-Based Rotational-XOR Distinguishers for AND-RX Block Ciphers: Evaluations on Simeck and Simon". Lecture Notes in Computer Science. 2023. DOI: 10.1007/978-3-031-53368-6_21
31. b30: Gao Wang, Gaoli Wang, Siwei Sun. "Investigating and Enhancing the Neural Distinguisher for Differential Cryptanalysis". IEICE Transactions on Information and Systems. 2024-08-01. DOI: 10.1587/transinf.2024edp7011
32. b31: Liu Zhang, Zilong Wang, Baocang Wang. "Improving Differential-Neural Cryptanalysis". IACR Communications in Cryptology. 2024-10-07. DOI: 10.62056/ay11wa3y6
33. b32: Liu Zhang, Jinyu Lu, Zilong Wang, Chao Li. "Improved differential-neural cryptanalysis for round-reduced SIMECK32/64". Frontiers of Computer Science. 2023-12. DOI: 10.1007/s11704-023-3261-z
34. b33: Z Hou, J Ren, S Chen. "Cryptanalysis of round-reduced simon32 based on deep learning". Cryptology ePrint Archive. 2021
35. b34: Anubhab Baksi, Jakub Breier, Yi Chen, Xiaoyang Dong. "Machine Learning Assisted Differential Distinguishers For Lightweight Ciphers". 2021 Design, Automation & Test in Europe Conference & Exhibition (DATE). 2021-02-01. DOI: 10.23919/date51398.2021.9474092
36. b35: Tarun Yadav, Manoj Kumar. "Differential-ML Distinguisher: Machine Learning Based Generic Extension for Differential Cryptanalysis". Lecture Notes in Computer Science. 2021. DOI: 10.1007/978-3-030-88238-9_10
37. b36: Amirhossein Ebrahimi, Francesco Regazzoni, Paolo Palmieri. "Reducing the Cost of Machine Learning Differential Attacks Using Bit Selection and a Partial ML-Distinguisher". Lecture Notes in Computer Science. 2022. DOI: 10.1007/978-3-031-30122-3_8
38. b37: Xiaoteng Yue, Wanqing Wu. "Improved Neural Differential Distinguisher Model for Lightweight Cipher Speck". Applied Sciences. 2023-06-09. DOI: 10.3390/app13126994
39. b38: Jiashuo Liu, Jiongjiong Ren, Shaozhen Chen, Manman Li. "Improved neural distinguishers with multi-round and multi-splicing construction". Journal of Information Security and Applications. 2023-05. DOI: 10.1016/j.jisa.2023.103461
40. b39: W Tian, B Hu. "Deep Learning Assisted Differential Cryptanalysis for the Lightweight Cipher SIMON". KSII Transactions on Internet and Information Systems. 2021-02-28. DOI: 10.3837/tiis.2021.02.012
41. b40: A Jain, V Kohli, G Mishra. Deep learning based differential distinguisher for lightweight block ciphers. 2021
42. b41: Kexin Qiao, Zehan Wu, Junjie Cheng, Changhai Ou, An Wang, Liehuang Zhu. "Bitwise Mixture Differential Cryptanalysis and Its Application to SIMON". IEEE Internet of Things Journal. 2024-07-01. DOI: 10.1109/jiot.2024.3384668
