# Deep Learning based Differential Distinguisher for Lightweight Block Ciphers

**Authors:** Aayush Jain, Varun Kohli, Girish Mishra

**Source PDF:** `2021_jain_kohli_mishra_present_simeck_neural_distinguisher.pdf`

## Abstract

Recent years have seen an increasing involvement of Deep Learning in the cryptanalysis of various ciphers. The present study is inspired by past works on differential distinguishers, to develop a Deep Neural Network-based differential distinguisher for round reduced lightweight block ciphers PRESENT and Simeck. We make improvements in the state-of-the-art approach and extend its use to the two structurally different block ciphers, PRESENT-80 and Simeck64/128. The obtained results suggest the universality of our cryptanalysis method. The proposed method can distinguish random data from the cipher data obtained until 6 rounds of PRESENT and 7 rounds of Simeck encryption with high accuracy. In addition to this, we explore a new approach to select good input differentials, which to the best of our knowledge has not been explored in the past. We also provide a minimum-security requirement for the discussed ciphers against our differential attack.

## Introduction

In the era of Internet of Things (IoT), security is one of the deciding factors for the viability of IoT systems [1] . These include smart homes [2] , medical and healthcare services [3, 4] , environment monitoring [5] , transportation [6] , vehicular networks [7] , and UAVs [8] to name a few. An IoT system comprises of four layers, namely application, middleware, network and sensing [1] , each of which may show vulnerability to a wide range of security threats [9] . Even seemingly secure systems have inherent flaws that can be exploited by attackers without the need of high computational resources [10] . One such flaw for example, may be biased encryption algorithms.

Various methods have been developed to exploit such flaws. Differential Cryptanalysis is a general cryptanalysis technique primarily used on block ciphers [11] , with some applications in stream ciphers [12] and hash functions [13] . It is the study of how input differences affect the differences in the output. In the case of block ciphers, the technique follows the transformation of the input through the cipher network, detecting areas of non-random behavior [2] . Such properties are exploited to recover the secret cryptographic key of the cipher. Biham and Shamir presented a novel differential cryptanalysis method [14] that could be applied to various DES-like substitution and permutation cryptosystems, such as FEAL-4 [15] . A classical differential attack follows the exhaustive approach of creating a difference distribution table. Aron Gohr proposed a novel neural network-based distinguisher in his recent work [16] , wherein a low-data, chosen-plaintext attack on round reduced SPECK 32/64 gave better results than past work by Dinur on SPECK [17] . Their proposed attack is an all-in-one approach with the Markov assumption which considers all output differences for a given input difference. He also presented a key recovery attack on 11 rounds of SPECK32/64 to recover the last two subkeys after 2 14.5 chosen-plaintext queries with a computational requirement of 2 38 SPECK encryptions, compared to past work by Dinur that achieved the complexity of 2 46 for 11 rounds. Following Gohr's work, Baksi et al proposed a deep learning-based approach for differential attacks on the non-Markov 8-round Gimli-Hash and Gimli-Cipher [18] . They used multiple models including multilayer perceptron (MLP), Long Short-Term Memory (LSTM) [19] , and Convolutional Neural Networks (CNN) [20] with varied width and number of neurons. We discuss their method in more detail in a later section.

PRESENT was developed in 2007 [21] at Orange Labs, France. It has become the criteria to measure the security of modern lightweight ciphers [22] . The Simeck family of lightweight block ciphers was developed in 2015 [23] and is a combination of the SIMON and SPECK block cipher families [24] , which are the smallest hardware and software block ciphers respectively. It has a smaller hardware footprint and software implementation than its parent families. An overview of the PRESENT and Simeck ciphers is discussed in a later section. These ciphers find practical application in IoT devices such as RFID tags [25] and sensors. Wang [26] in 2008, presented her differential cryptanalysis of 16-round reduced PRESENT. Her proposed differential characteristics for 14 and 15 rounds of encryption had a probability of 2 -62 and 2 -66 respectively. Wang also searched for iterative characteristics from the 2 nd to 7 th rounds which she claims to be more effective than the 2-round iterative characteristics. Wang's study proved the effectiveness of using select input differentials which have a higher probability over differentials with lower probability.

This study extends the work by Baksi and Wang for use in two structurally different lightweight block ciphers, PRESENT and Simeck. Our major contributions are as follows:

1. We improve the differential distinguisher algorithm proposed by Baksi et al by using Wang's high probability input differentials for PRESENT and Simeck. 2. We generate three good input differentials from one of Wang's high probability input differences by using left and right shift operators. 3. We propose a simpler deep learning architecture with a lower number of parameters as compared to Baksi's recommended architecture. 4. Our results provide a minimum-security requirement for the discussed ciphers to ensure safety against deep learning-based differential attacks.

Section-2 gives an overview of the lightweight block ciphers PRESENT and Simeck. This is followed by a discussion on the differential distinguisher algorithm in Section-3. We will then discuss our deep learning model followed by the results obtained during experimentation in Sections-4 and 5 respectively. Finally, we conclude the study in Section-6 and provide direction for future work based on our research.


## Lightweight Block Ciphers

Block ciphers are symmetric key ciphers employing deterministic algorithms to encrypt blocks of plaintext. Lightweight block ciphers are a subset of these, as they use algorithms that require less computing power. The following subsections discuss the two lightweight block ciphers used in our study, PRESENT and Simeck.


## PRESENT

The PRESENT cipher was developed by Bogdanov et al in 2007 [21] . It was included in the new international standard for lightweight cryptographic methods by the International Organization for Standardization (ISO) and the International Electrotechnical Commission (IEC) in 2019 [22] . Due to its bit-oriented permutations, PRESENT is a hardware cipher which can be implemented with simple wiring. It supports a block-length of 64 bits and key-lengths of 80 bits and 128 bits, which suffice the requirements of moderate-level security applications such as tag-based systems. The scope of this study is limited to the 80-bit key variant of PRESENT.


## 2.1.1


## Round Function

A complete-round PRESENT implementation consists of 31 rounds of encryption and each round includes the following layers:

Substitution Layer: The substitution layer contains 4×4 S-Boxes. These S-Boxes are used 16 times in parallel each round. The hexadecimal S-Box mapping is shown in Table -1 Where 1 ≤ 𝑖 ≤ 32, and 𝐾 𝑖 , 𝐵 𝑖 are the 𝑖 𝑡ℎ round key and block state respectively. Fig- 1 illustrates the general working of the PRESENT cipher.


## Key Scheduling Algorithm

The round keys to be used

in the addRoundKey step are generated using the Key Scheduling Algorithm (KSA) which takes the 80-bit key denoted as 𝐾 = 𝑘 79 𝑘 78 𝑘 77 … 𝑘 0 and stores it in the shift register. The key is rotated to the left by 61 bits positions. The most significant 4 bits are passed through the 4 × 4 PRESENT Sbox. Bits 15-19 of K are then XORed with the least significant bit of roundCounter on the right. The equations for the process are as follows: [𝑘 79 𝑘 78 … 𝑘 1 𝑘 0 ] = [𝑘 18 𝑘 17 … 𝑘 20 𝑘 19 ] [𝑘 79 𝑘 78 𝑘 77 𝑘 76 ] = 𝑆[𝑘 79 𝑘 78 𝑘 77 𝑘 76 ] [𝑘 19 𝑘 78 𝑘 17 𝑘 16 𝑘 15 ] = [𝑘 19 𝑘 18 𝑘 17 𝑘 16 𝑘 15 ]⨁ 𝑟𝑜𝑢𝑛𝑑𝐶𝑜𝑢𝑛𝑡𝑒𝑟 2.2 Simeck The Simeck lightweight block cipher was proposed by Yang et al in 2015 [23]. It is designed to be compact and moderately secure for resource constrained applications such as passive RFID tags and Wireless Sensor Network (WSN) nodes. It is a combination of the SIMON and SPECK cipher families which are a set of hardware and software lightweight block ciphers respectively. Simeck is smaller than SIMON due to the reduced size of the Round Function and KSA. It combines the best features of its parent cipher families, that are: a. A modified and compact version of SIMON's round function. b. A round function for key scheduling, similar to SPECK. c. A Linear Feedback Shift Register (LSFR)-based constant for simpler key schedule, in line with SIMON.

The Simeck family of ciphers is represented as Simeck2n/mn. Here n is the word size, equal to 16, 24 or 32 based on the family, and mn denotes the key size which may be 64, 96 or 128 bits long. Thus, the resulting ciphers are Simeck 32/64, 48/96, and 64/128. These size choices aim to fit various applications such as tag-based systems and are included in the specification of the SIMON and SPECK. The round function and key scheduling algorithm have a Feistel structure as shown in Fig- 2 and 3.


## Round Function

Fig- 2


## Key Scheduling Algorithm

The 𝑖 𝑡ℎ round key 𝑘 𝑖 is generated by dividing the master key 𝐾 into four words and loading them as the inital states (𝑡 2 , 𝑡 1 , 𝑡 0 , 𝑘 0 ). Here, 𝑡 2 is the most significant 𝑛 bits of 𝑘, and the least significant n bits are denoted by 𝑘 0 . These initial states are loaded into the LFSR. The FSR of the key scheduling algorithm are shown in Fig- 3 . The update of states is done as per the following equations: 𝑘 𝑖+1 = 𝑡 𝑖 , 𝑡 𝑖+3 = 𝑘 𝑖 ⨁𝑓(𝑡 𝑖 )⨁𝐶⨁(𝑧 𝑗 ) 𝑖 Where 𝑖 is the round number, 𝐶 = 2 𝑛 -4 (𝑛 is the word size) and (𝑧 𝑗 ) 𝑖 is the 𝑖 𝑡ℎ bit of sequence 𝑧 𝑗 in which 𝑗 = 0 for Simeck32/64 and Simeck48/96, and 𝑧 0 has period of 31. Similarly, for Simeck64/128, 𝑗 = 1 and 𝑧 1 has a period of 63.


## 3


## Differential Distinguisher

Following the work done by Baksi et. al. 18 on Machine Learning (ML) based differential distinguishers, we improve their differential method. This section discusses the in-depth approach of their algorithm and our suggested improvements. The algorithm for the deep learning based differential distinguisher is shown in Algorithm-1. In this differential method, the attacker chooses (𝑡 ≥ 2) input differentials. The four selected differentials are provided in Table-3, where the first differential is selected from Wang's study [26] for PRESENT. The remaining three differentials (numbered 2-4) are generated using left and right shifts. The same differences are used for Simeck64/128 as well. This selection is followed by two phases, OFFLINE and ONLINE. The OFFLINE or the Training Phase is for making the training-dataset of input-output differential pairs, and then training the DL model to learn the relationship between these input and output differences. The ONLINE or Testing Phase involves the creation of the test-dataset and then deciphering whether the given ORACLE is the CIPHER or RANDOM. For 𝑡 input differentials, if the training accuracy during the Offline phase comes out to be ≥

1 𝑡 , we proceed to the online phase. A testing accuracy ≥ 1 𝑡 in the online phase implies the ORACLE is the CIPHER, and otherwise, RANDOM.


## Dataset Collection:

For 10,000 different key-plaintext pairs, we have selected four input differential classes. These input differentials were either selected randomly (for 𝑀 1 and 𝑀 2 ) or were taken from Table-3 (for 𝑀 3 and 𝑀 4 ). For every key-plaintext pair, the plaintext, and its corresponding difference pair, calculated for each input difference class, is encrypted for r-round reduced PRESENT (3 ≤ 𝑟 ≤ 6) and Simeck (3 ≤ 𝑟 ≤ 7). The obtained ciphertext pairs XORed to get the output difference. This output difference, along with the input difference class, is stored in a training-dataset. The hyper-parameters for the training and testing of the models are given in Table -4 .


## Results

The previously discussed differential distinguisher models were trained and tested on random data, and data from PRESENT and Simeck. The minimum and maximum validation results of the study are presented in Table-5 in a very concise format. performed significantly better for both PRESENT and Simeck. This is because the selected input differentials have a high probability for differential cryptanalysis and remove the possibility of using low probability differentials, that would give poor results as seen for 𝑀 1 and 𝑀 2 . Although the selected differentials are for PRESENT, they give good results for Simeck as well as shown in the table. Fig- 5 and Fig- 6 show the average validation accuracies for PRESENT and Simeck respectively, round and model wise. It can be seen that 𝑀 3 and 𝑀 4 perform exceptionally well, with obtained average accuracies following a decreasing trend from lower to higher rounds.

Whereas the average accuracies for 𝑀 1 and 𝑀 2 are significantly lower in comparison, for reasons discussed earlier, with nearly constant values obtained after the third round. All four models reach the limiting average accuracies of nearly 25% by the 6 6 𝑡ℎ round for PRESENT, and the 7 𝑡ℎ round for Simeck. In addition to the above, our proposed MLP (used in 𝑀 2 and 𝑀 4 ) performs better than Baksi's recommended MLP (used in 𝑀 1 and 𝑀 3 ) for use on PRESENT and Simeck.


## Conclusion

In this study, we improved Baksi et al's differential distinguisher method by using one high probability input differential from Wang's study for PRESENT and generated three more differentials from it by shifting it left and right. This improvised method was extended to two structurally different lightweight block ciphers PRESENT and Simeck. The results obtained were significantly better than when randomly selected input differentials were used, and slightly better for our proposed deep learning architecture over the one recommended in the past work. The proposed method can differentiate random data from cipher data until 6 rounds of PRESENT and 7 rounds of Simeck encryption. This shows that using a higher number of encryption rounds for these ciphers can provide the necessary security for IoT devices against a deep learning based differential attack. Based on our study, future work in this area of research can be done on the suggestive universality of the method and input differences across structurally different ciphers. The suggested method for selecting input differentials by shifting an already established high probability input differential can also be explored. In addition to this, our approach does not include a key retrieval method, which can be developed in the future.

> 1 Fig. 1 . Fig. 1. Abstract view of PRESENT cipher.

> Fig-2shows the round function for Simeck. It involves the division of the plaintext into left and right words 𝑙 0 and 𝑟 0 respectively, where 𝑙 0 consists of the most significant 𝑛 bits, and 𝑟 0 contains the least significant 𝑛 bits. The round function processes these two words, followed by the concatenation of 𝑙 𝑇 and 𝑟 𝑇 , where 𝑇 is the total number of encryption rounds. The round function is as follows:𝑅 𝑘 𝑖 (𝑙 𝑖 , 𝑟 𝑖 ) = (𝑟 𝑖 ⨁𝑓(𝑙 𝑖 )⨁𝑘 𝑖 , 𝑙 𝑖 ) Where 𝑙 𝑖 and 𝑟 𝑖 are as discussed above and 𝑘 𝑖 is the 𝑖 𝑡ℎ round key. The function 𝑓(𝑧) is as follows:𝑓(𝑧) = (((𝑧)𝐴𝑁𝐷(𝑧 ⋘ 5))⨁(𝑧 ⋘ 1)) In the above equations, ⊕, ⋘ and 𝐴𝑁𝐷 represent the Exclusive OR, left rotation and bitwise AND operations respectively.

> 2 Fig. 2 . Fig. 2. Round function of Simeck.

> 3 Fig. 3 . Fig. 3. KSA of Simeck.

> 4 Fig. 4 . Fig. 4. Proposed DL Architecture.

> 5 Fig. 5 . Fig. 5. Average validation accuracies for PRESENT.

> 6 Fig. 6 . Fig. 6. Average validation accuracies for Simeck.

> 1 Table 1 . .Hexadecimal S-Box Mapping.Permutation Layer: Bit-wise permutation is performed on the data block in this layer. The permutation layer mapping is shown in Table-2.

> 2 Table 2 . Permutation Layer Mapping.

> 3 Table 3 . Differentials used in this study.

> 4 Table 4 . Hyper-parameters.

> 5 Table 5 . Comparison of Differential Distinguisher Models based on Validation Accuracy.

## References

1. b0: Vikas Hassija, Vinay Chamola, Vikas Saxena, Divyansh Jain, Pranav Goyal, Biplab Sikdar. "A Survey on IoT Security: Application Areas, Security Threats, and Solution Architectures". IEEE Access. 2019. DOI: 10.1109/access.2019.2924045
2. b1: Rodolfo R Rodrigues, Joel J P C Rodrigues, Mauro A A Da Cruz, Ashish Khanna, Deepak Gupta. "An IoT-based Automated Shower System for Smart Homes". 2018 International Conference on Advances in Computing, Communications and Informatics (ICACCI). 2018-09. DOI: 10.1109/icacci.2018.8554793
3. b2: Irina Valeryevna Pustokhina, Denis Alexandrovich Pustokhin, Deepak Gupta, Ashish Khanna, K Shankar, Gia Nhu Nguyen. "An Effective Training Scheme for Deep Neural Network in Edge Computing Enabled Internet of Medical Things (IoMT) Systems". IEEE Access. 2020. DOI: 10.1109/access.2020.3000322
4. b3: Ahmed Faeq Hussein, N Arun Kumar, Marlon Burbano-Fernandez, Gustavo Ramírez-González, Enas Abdulhay, Victor Hugo C De Albuquerque. "An Automated Remote Cloud-Based Heart Rate Variability Monitoring System". IEEE Access. 2018. DOI: 10.1109/access.2018.2831209
5. b4: Salman Khan, Khan Muhammad, Shahid Mumtaz, Sung Wook Baik, Victor Hugo C De Albuquerque. "Energy-Efficient Deep CNN for Smoke Detection in Foggy IoT Environment". IEEE Internet of Things Journal. 2019-12. DOI: 10.1109/jiot.2019.2896120
6. b5: Suresh Chavhan, Deepak Gupta, B N Chandana, Ashish Khanna, Joel J P C Rodrigues. "IoT-Based Context-Aware Intelligent Public Transport System in a Metropolitan Area". IEEE Internet of Things Journal. 2019. DOI: 10.1109/jiot.2019.2955102
7. b6: Gaurang Bansal, Naren Naren, Vinay Chamola, Biplab Sikdar, Neeraj Kumar, Mohsen Guizani. "Lightweight Mutual Authentication Protocol for V2G Using Physical Unclonable Function". IEEE Transactions on Vehicular Technology. 2020-07. DOI: 10.1109/tvt.2020.2976960
8. b7: Ashish Khanna, Joel J P C Rodrigues, Naman Gupta, Abhishek Swaroop, Deepak Gupta. "Local Mutual Exclusion algorithm using fuzzy logic for Flying Ad hoc Networks". Computer Communications. 2020-04. DOI: 10.1016/j.comcom.2020.03.036
9. b8: Tejasvi Alladi, Vinay Chamola, Biplab Sikdar, Kim-Kwang Raymond Choo. "Consumer IoT: Security Vulnerability Case Studies and Solutions". IEEE Consumer Electronics Magazine. 2020-03-01. DOI: 10.1109/mce.2019.2953740
10. b9: Tejasvi Alladi, Vinay Chamola, Sherali Zeadally. "Industrial Control Systems: Cyberattack trends and countermeasures". Computer Communications. 2020-04. DOI: 10.1016/j.comcom.2020.03.007
11. b10: D Coppersmith. "The Data Encryption Standard (DES) and its strength against attacks". IBM Journal of Research and Development. 1994-05. DOI: 10.1147/rd.383.0243
12. b11: Eli Biham, Orr Dunkelman. "Cryptanalysis of the A5/1 GSM Stream Cipher". Lecture Notes in Computer Science. 2007. DOI: 10.1007/3-540-44495-5_5
13. b12: Eli Biham, Adi Shamir. "Differential Cryptanalysis of Hash Functions". Differential Cryptanalysis of the Data Encryption Standard. 1993. DOI: 10.1007/978-1-4613-9314-6_8
14. b13: Eli Biham, Adi Shamir. "Differential cryptanalysis of DES-like cryptosystems". Journal of Cryptology. 1991-01. DOI: 10.1007/bf00630563
15. b14: K Aoki, K Ohta. "Differential-linear cryptanalysis of FEAL-8". IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences. 1996
16. b15: Aron Gohr. "Improving Attacks on Round-Reduced Speck32/64 Using Deep Learning". Lecture Notes in Computer Science. 2019. DOI: 10.1007/978-3-030-26951-7_6
17. b16: Itai Dinur. "Improved Differential Cryptanalysis of Round-Reduced Speck". Lecture Notes in Computer Science. 2014. DOI: 10.1007/978-3-319-13051-4_9
18. b17: Anubhab Baksi, Jakub Breier, Yi Chen, Xiaoyang Dong. "Machine Learning Assisted Differential Distinguishers For Lightweight Ciphers". 2021 Design, Automation & Test in Europe Conference & Exhibition (DATE). 2020. DOI: 10.23919/date51398.2021.9474092
19. b18: Amin Ullah, Khan Muhammad, Javier Del Ser, Sung Wook Baik, Victor Hugo C De Albuquerque. "Activity Recognition Using Temporal Optical Flow Convolutional Features and Multilayer LSTM". IEEE Transactions on Industrial Electronics. 2018. DOI: 10.1109/tie.2018.2881943
20. b19: Tanveer Hussain, Khan Muhammad, Amin Ullah, Zehong Cao, Sung Wook Baik, Victor Hugo C De Albuquerque. "Cloud-Assisted Multiview Video Summarization Using CNN and Bidirectional LSTM". IEEE Transactions on Industrial Informatics. 2019. DOI: 10.1109/tii.2019.2929228
21. b20: A Bogdanov, L R Knudsen, G Leander, C Paar, A Poschmann, M J B Robshaw, et al.. "PRESENT: An Ultra-Lightweight Block Cipher". Lecture Notes in Computer Science. 2007. DOI: 10.1007/978-3-540-74735-2_31
22. b21: Gangqiang Yang, Bo Zhu, Valentin Suder, Mark D Aagaard, Guang Gong. "The Simeck Family of Lightweight Block Ciphers". Lecture Notes in Computer Science. 2015. DOI: 10.1007/978-3-662-48324-4_16
23. b22: Ray Beaulieu, Douglas Shors, Jason Smith, Stefan Treatman-Clark, Bryan Weeks, Louis Wingers. "The SIMON and SPECK lightweight block ciphers". Proceedings of the 52nd Annual Design Automation Conference. 2013. DOI: 10.1145/2744769.2747946
24. b23: R Weinstein. "RFID: a technical overview and its application to the enterprise". IT Professional. 2005-05. DOI: 10.1109/mitp.2005.69
25. b24: Meiqin Wang. "Differential Cryptanalysis of Reduced-Round PRESENT". Lecture Notes in Computer Science. 2008. DOI: 10.1007/978-3-540-68164-9_4
