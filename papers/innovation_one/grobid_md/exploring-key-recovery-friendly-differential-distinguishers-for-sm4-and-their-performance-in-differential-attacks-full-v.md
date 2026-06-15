# Exploring Key-Recovery-Friendly Differential Distinguishers for SM4 and Their Performance in Differential Attacks (Full Version)

**Authors:** Bingqing Li, Ling Sun

**Source PDF:** `2025_li_sun_key_recovery_friendly_sm4_differential_distinguishers.pdf`

## Abstract

In this paper, we focus on SM4, a widely used and standardized Chinese block cipher. After revisiting the previously proposed optimal 19-round differential characteristic, we observe that its applicability in differential attacks is limited by a reduced pre-sieving probability, causing the time complexity to exceed that of brute force. To overcome this issue, we employ an automated search approach to identify more promising optimal 19-round differential characteristics. By translating key properties relevant to key recovery into Boolean expressions, we uncover three structural properties common to all optimal 19-round characteristics. While these properties dictate the overall probability of the resulting 19-round distinguishers, their varying pre-sieving probabilities influence their practical effectiveness in differential attacks. Using Boolean encodings, we identify four representative key-recovery-friendly differential characteristics. We then conduct an in-depth analysis of one such characteristic and demonstrate that, when evaluated under both the hypothesis testing paradigm and the key ranking paradigm, the proposed attack requires slightly more data than existing 23-round attacks. Nonetheless, it achieves lower time and memory complexities and ensures a higher success probability, offering a valuable new avenue for differential cryptanalysis of SM4. We believe our findings enhance the understanding of SM4's differential structure and provide a solid foundation for future research on advanced key-recovery techniques that leverage these newly identified structural properties and differential characteristics.

## Introduction

SM4 [7] is a block cipher standard widely used in China to safeguard sensitive data. Developed by the Chinese government, it forms a core component of the nation's cryptographic standards. Originally introduced as SMS4, the algorithm was standardized by the Chinese State Cryptography Administration and later renamed SM4, aligning it with the SM series of cryptographic algorithms. Since its inception, SM4 has been subjected to extensive cryptanalysis, with researchers examining its resilience against a wide range of attacks most notably differential attacks [9, 24, 25, 19] , as well as linear [8, 9] and integral attacks [12] , among other advanced techniques.

Like many modern block ciphers, SM4 is designed to resist differential cryptanalysis a powerful method introduced by Biham and Shamir [3, 4] . Nevertheless, researchers continue to investigate differential characteristics in pursuit of potential vulnerabilities. Notably, Su et al. [19] identified a family of 19-round differential characteristics for SM4, including one with a maximal probability of 2 -124 . By exploiting this distinguisher, they launched the first 23-round differential attack on SM4.

For nearly a decade, the probability bound of 19-round differential characteristics in SM4 remained unchallenged. In 2019, Liu et al. [13, 14] leveraged an automated approach based on the Simple Theorem Prover (STP) to search for differential and linear characteristics in S-box-based ciphers. Through this method, they claimed to discover a 19-round SM4 differential characteristic with a probability of 2 -123 , although they did not provide detailed information about the characteristic or confirm whether 2 -123 is indeed the tightest bound.

More recently, Li and Sun [10] used a Boolean Satisfiability (SAT) based automated search to address the gap left by Liu et al. They confirmed that 2 -123 is indeed the upper bound for 19-round differential characteristics in SM4 and publicly released the first known optimal 19-round characteristic. However, this newly identified characteristic has not yet been employed in any differential attack on SM4. Consequently, the primary motivation for this work was to determine whether this optimal 19-round differential characteristic could be leveraged to improve differential attacks on SM4.

In this paper, we begin by analyzing the optimal differential characteristic proposed in [10] . Our findings reveal that the output difference of this characteristic reduces the pre-sieving probability in the differential attack, resulting in a time complexity that exceeds that of brute force. Since the existing differential characteristic does not yield an improvement in the differential attack on SM4, we shift our focus to identifying other 19-round differential characteristics with the same probability of 2 -123 that are more conducive to key recovery.

In view of the SAT-based method's outstanding performance in searching for optimal differential characteristics in SM4, we also adopt an automated SATbased search strategy to discover new differential characteristics. Given the vast number of 19-round optimal differential characteristics with a probability of 2 -123 in SM4 and considering the lengthy runtime required by SAT solvers for multi-solution searches it is not feasible to enumerate all such characteristics in order to identify those best suited for key-recovery attacks. Instead, we explore the properties these optimal 19-round differential characteristics share, as well as those that set them apart.

By translating the characteristic properties that influence key recovery into Boolean expressions, we successfully identified three structural properties common to all optimal 19-round differential characteristics.

• The total number of active S-boxes cannot be fewer than 19.

• Each round must contain at least one active S-box.

• The number of active S-boxes is exactly 19, with precisely one active S-box present in every round.

Based on these properties, we find that the 19-round differential distinguisher derived from any optimal characteristic has a probability of 2 -123. 99 . Although all 19-round distinguishers from the optimal characteristics share this overall probability, their respective pre-sieving probabilities differ, influencing their practical utility in differential attacks. Using Boolean encodings, we confirm the existence of key-recovery-friendly characteristics among the optimal 19-round differential characteristics of SM4. Furthermore, we identify four representative differential characteristics that are particularly favorable for keyrecovery attacks.

We conduct an in-depth analysis of one of the four differential characteristics in the context of key-recovery attacks. To comprehensively evaluate its performance, we employ both the hypothesis testing paradigm and the key ranking paradigm, with the resulting performance metrics summarized in Table 1 . Under the hypothesis testing paradigm, our attack requires slightly more data than the 23-round attack proposed by Su et al. [19] , yet it achieves lower time and memory complexities while ensuring at least a 90% success probability. Under the key ranking paradigm, our attack also requires more data than the 23-round attack by Zhao et al. [26] , but it offers lower time complexity and a higher success probability. The remainder of this paper is organized as follows. Section 2 presents an overview of differential cryptanalysis and summarizes essential information on SM4. Section 3 describes our methodology for identifying key-recovery-friendly optimal 19-round differential characteristics of SM4. In Section 4, we evaluate the attack performance using one of these newly identified 19-round characteristics. Finally, Section 5 concludes the paper.


## Preliminary


## Differential Cryptanalysis

Differential cryptanalysis [3, 4] is a cryptanalytic method primarily applied to symmetric-key algorithms, especially block ciphers. It leverages the nonlinear components of a cipher to identify cases where certain input differences ∆ in yield specific output differences ∆ out with a higher probability than would occur by chance. The pair (∆ in , ∆ out ) is called a differential. The probability of this differential, for an n-bit primitive E K , is defined as

The weight of the differential is given by

Determining the probability of a valid differential in a multi-round cryptographic algorithm can be quite challenging. Typically, differential characteristics are constructed to trace internal differences after each round. Let (∆ in = ∆ 0 , ∆ 1 , . . . , ∆ R = ∆ out ) represent an R-round differential characteristic. Suppose the R-round encryption function E K is composed of R round functions, i.e.,

Under the assumption that the round keys K 0 , K 1 , . . ., K R-1 are uniformly random and independent, the probability of this differential characteristic is the product of the differential transition probabilities at each round:

When determining differential characteristics for round functions, S-boxes often present the greatest complexity. To simplify their analysis, one typically constructs a Differential Distribution Table (DDT). For an s-bit S-box, the DDT is a 2 s × 2 s table, with the entry in the i-th row and j-th column indicating the number of input-output pairs that satisfy the differential (i, j). An S-box is considered active if its differential corresponds to a DDT entry that is nonzero yet strictly less than 2 s .


## Data Complexity and Success Probability in Differential Attack

Once an effective differential characteristic for the target cipher is identified, a differential attack can be mounted. Let p 0 denote the probability of the R-round differential characteristic, and let N be the number of plaintext pairs used in the attack. As a form of statistical cryptanalysis, we define the statistic Σ (used in the differential attack) as the number of pairs that satisfy the differential characteristic. Under the correct key guess, Σ follows a binomial distribution with parameters (N, p 0 ). Conversely, if the probability that a pair satisfies the differential characteristic under an incorrect key guess is p (where p < p 0 ), then Σ follows a binomial distribution with parameters (N, p).

Once the observed value of Σ is obtained from the sample, we construct a list L of the most likely keys among all κ possible keys. As shown by Blondeau et al. [5] , two paradigms can be adopted for this process. In both paradigms, the success probability P S is defined as the probability that the correct key is included in L.

Hypothesis Testing Paradigm. Hypothesis testing begins by setting a threshold τ . Any key whose statistic Σ is at least τ is included in the list L. Two types of errors can arise. 1. Non-detection error probability (α): This error occurs if the correct key k 0 is not included in L (i.e., k 0 / ∈ L). From its definition,

In this situation, the success probability P S is 1α. 2. False alarm error probability (β): This error occurs if an incorrect key k is included in L (i.e., k ∈ L). In this case,

The following theorem can be used to estimate α and β.

Theorem 1 (Blondeau et al. [5] ). Let p 0 and p be real numbers such that 0 < p < p 0 < 1, and let τ satisfy p < τ /N < p 0 . Define Σ 0 and Σ k as binomial random variables with parameters (N, p 0 ) and (N, p), respectively. Then,

is the Kullback-Leibler divergence between two Bernoulli distributions with parameters q 1 and q 2 . Remark 1. As noted in [5] , when p and p 0 are not extremely small, the approximation formulas from Theorem 1 can reliably estimate both types of error probabilities. However, when p and p 0 are exceedingly small, directly applying these approximations to compute α and β may cause substantial errors. For instance, in our evaluation of the SM4 differential attack, if we set p = 2 -128 and p 0 = 2 -123.99 with N ranging from 2 123 to 2 126 , using (3) sometimes produces negative values or values greater than 1 both of which are invalid probabilities. As a result, in the subsequent analysis, we do not use the approximation formulas from Theorem 1. Instead, we revert to the original definitions of the error probabilities and employ formulas (1) and (2) to evaluate α and β. Key Ranking Paradigm. Key ranking fixes the size of the candidate key list L to an integer ℓ, retaining the ℓ most probable keys. By leveraging properties of the Beta distribution, the success probability can be evaluated using the following theorem.

Theorem 2 (Blondeau et al. [5] ). Let F be the cumulative distribution function of a binomial distribution with parameters (N, p), i.e., F(x)

Denote by f 0 (i) the probability that the statistic Σ for the correct key takes the value i:

If λ ⩽ 0.25, then the success probability P S satisfies

where

f 0 (i) and C λ = p p 0 p 0 (N + 1) -F -1 (1λ) F -1 (1λ)p(N + 1) .


## Through experimental verification, Blondeau et al.

showed that when N takes the form

the success probability P S depends primarily on the constant c.


## Description of SM4

SM4 [7] operates on 128-bit blocks, consistent with other modern block ciphers such as the Advanced Encryption Standard (AES) [16] . The cipher uses a 128bit key K, providing a symmetric encryption scheme in which the same key is employed for both encryption and decryption. SM4 consists of 32 rounds of encryption. Let (X i , X i+1 , X i+2 , X i+3 ) ∈ (F 32 2 ) 4 denote the 128-bit input to the i-th round, where 0 ⩽ i < 32. Denote the round keys by RK i .

In each round, the internal state is updated using the function T . The encryption process for the i-th round is given by

The function T is composed of a nonlinear transformation S and a linear transformation L, i.e., T = L • S. An illustration for the round function of SM4 can be found in Figure 1 . Nonlinear transformation S. SM4 applies the same 8 × 8 S-box S four times in parallel to a 32-bit input. Let Y = (Y [0], Y [1], Y [2], Y [3]) ∈ (F 8 2 ) 4 represent the input to S, and Z = (Z[0], Z[1], Z[2], Z[3]) ∈ (F 8

2 ) 4 denote the corresponding output. The transformation S is defined by


## Linear transformation L.

The linear transformation L is a simple linear function that takes the output of S as its input. Given Z as the input to L, its output is computed as

A key property of the SM4 S-box, often exploited in its cryptanalysis, is the following.

Property 1. For any nonzero input difference, the SM4 S-box produces 127 possible output differences. Among these, one specific output difference appears with probability 2 -6 , while each of the remaining 126 output differences occurs with probability 2 -7 .

As illustrated in Figure 1 , the SM4 key schedule operates similarly to its encryption function. The function T ′ , used in the key schedule, closely resembles T except for the linear transformation: it uses

instead of L. The round key RK i for the i-th round is then computed as

where KC i are certain constants. Moreover, (KS 0 , KS 1 , KS 2 , KS 3 ) is obtained by XORing the master key K with a fixed system parameter. Additional details on the cipher can be found in [7] .


## Previous Most Effective Differential Attacks on SM4

The most effective differential attacks on SM4 so far target 23 rounds. Both known 23-round differential attacks on SM4 [19, 26] are based on the 127 2 19round differential characteristics first introduced by Su et al. [19] . These characteristics share the same output difference foot_0 :

(3f0000cf, ccf300fc, f3f30033, f3f30033), while their input differences vary. The input differences take the form (a 0 , f3f30033, f3f30033, f3000030), where a 0 ∈ {x ⊕ 00f30003 | Pr T (f3000030, x) > 0}. Among these 127 2 differential characteristics, one has a probability of 2 -124 , 254 have a probability of 2 -125 , and the remaining characteristics have a probability of 2 -126 . The average probability of these differential characteristics is 2 -125.98 , representing the probability for the 19-round distinguisher.

In the 23-round differential attacks, this 19-round distinguisher is placed at the beginning (rounds 0 to 18), followed by four additional rounds. As illustrated in Figure 2 (a), only the second and third bytes of ∆X 0 are fixed, enabling structures to be constructed at the distinguisher input so that more plaintext pairs can be generated from a fixed number of plaintexts. At the output of the distinguisher, ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 = ccf300fc, which matches the input difference of the function T in the nineteenth round. Since

which contains 127 3 elements. Because ∆X 23 is part of the ciphertext difference, the condition ∆X 23 ∈ Λ filters out ciphertext pairs with probability 2 -11.03 prior to key enumeration. This probability is called the pre-sieving probability. As the initial number of pairs heavily impacts the time complexity of subsequent key enumeration, the magnitude of this pre-sieving probability is critically important.

(a) Key-recovery procedure using the distinguisher proposed by Su et al.


## ∆X0 = a0

∆X1 = f3f30033 ∆X2 = f3f30033 ∆X3 = f3000030

19-round distinguisher with a probability of 2 -125.98 19-round distinguisher with a probability of 2 -123.99

Fig. 2 . 23-round key-recovery procedures with different distinguishers.


## Automated Search for Optimal Differential Characteristics

Several studies [23, 11, 13, 14, 10] have employed automated techniques to explore the differential properties of SM4. Among these, the method based on Boolean satisfiability problems (SAT) has delivered the best performance to date. In a SAT problem, one seeks an assignment of truth values to variables that satisfies a given Boolean formula making it evaluate to true. SAT problems are widely utilized in areas such as cryptography, hardware and software verification, and automated theorem proving. Due to their importance, many advanced algorithms and tools, known as SAT solvers, have been developed to efficiently handle large-scale and complex SAT instances. When given to SAT solvers, SAT problems are generally expressed in Conjunctive Normal Form (CNF), where the formula is a conjunction (AND, ∧) of clauses, each clause being a disjunction (OR, ∨) of literals. A literal is defined as a variable or its negation (NOT, •).

By formulating the search for differential characteristics in SM4 as SAT problems, Li and Sun [10] introduced the first publicly available optimal 19-round differential characteristic with a probability of 2 -123 . Its input difference is (4703d247, 263b8b26, 479ad247, 61835961), and its output difference is (26168b26, 4703d247, 61ae5961, 479ad247).


## Explorations of Key-Recovery-Friendly Distinguishers

In this section, we first demonstrate that the previously discovered optimal differential characteristic does not yield a stronger differential attack on SM4. Subsequently, we succeed in identifying alternative 19-round differential characteristics that are more conducive to key recovery.


## Main Problem of Employing Differential Characteristic in [10]

Although Li and Sun [10] presented an optimal 19-round differential characteristic for SM4, its potential to strengthen differential attacks has not been examined. In this work, we show that the 19-round distinguisher derived from their characteristic offers no advantage when used to launch 23-round differential attacks on SM4.

As illustrated in Figure 2 (b), since ∆X 1 ⊕ ∆X 2 ⊕ ∆X 3 = 00220000 serves as the input difference for the function T in the zeroth round, we can derive a set of 127 differential characteristics based on the original characteristic from [10] (see Section 2.5). These differential characteristics share the same output difference as the optimal one but differ in their input differences, which are of the form (a ′ 0 , 263b8b26, 479ad247, 61835961), where a ′ 0 ∈ {x ⊕ 263b8b26 | Pr T (00220000, x) > 0}. Among these 127 characteristics, one achieves the highest probability of 2 -123 , while the remaining 126 have a probability of 2 -124 . Consequently, the new 19-round distinguisher has an average probability of 2 -123.99 .

To mount a 23-round attack, we append four rounds to the new 19-round distinguisher. Since ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 = 61375961, the possible values of ∆X 23 belong to

which contains 127 4 elements. When applying the condition ∆X 23 ∈ Λ ′ to filter ciphertext pairs, the pre-sieving probability is 2 -4.05 . Given the large number of pairs advancing to the key enumeration phase, the time complexity of the attack will be difficult to manage.

Given that even the 19-round distinguisher with higher differential probability does not yield a more efficient differential attack, we must also consider whether other 19-round differential characteristics with probability 2 -123 might facilitate stronger attacks. We aim to use a SAT-based automated approach 6 to investigate the existence of more effective differential characteristics. Before presenting our method, we first review the automated techniques from [10] for searching differential characteristics of SM4.


## Methods for Finding Differential Characteristics of SM4

To find differential characteristics of SM4, one can translate differential propagation through the cipher's components into Boolean formulas in CNF. This SAT formulation, geared toward identifying SM4 differential characteristics, naturally divides into three parts: SAT models for the linear components, the nonlinear components, and the objective function.

SAT Models for Linear Components. As discussed in [10] , characterizing differential propagation over the linear components of SM4 only requires a SAT model for multi-input XOR operations. Because Kissat does not natively support Boolean formulas involving XOR, the SAT model from [21] is employed instead. Throughout this work, for an n-bit vector ∆X, we use ∆X (i) to denote the i-th bit of ∆X, where 0 ⩽ i < n.

Model 1 (l-Input XOR, [21] ) Consider the n-bit XOR operation Y = X 0 ⊕ X 1 ⊕ • • • ⊕ X l-1 , whose input and output differences are ∆X 0 , ∆X 1 , . . ., ∆X l-1 and ∆Y , respectively. The differential propagation is valid if and only if ∆X 0 , ∆X 1 , . . ., ∆X l-1 , and ∆Y satisfy the following equations for every (l + 1)-bit vector (θ (0) , θ (1) , . . . , θ (l) ) such that θ (0


## SAT Models for Nonlinear Components.

In SM4, the S-box S is the sole nonlinear component. The SAT model for S, which aims to capture differential probabilities, follows the approach in [20] . Specifically, each S-box is characterized by sixteen Boolean variables, ∆X = (∆X (0) , ∆X (1) , . . . , ∆X (7) ) and ∆Y = (∆Y (0) , ∆Y (1) , . . . , ∆Y (7) ), representing the input and output differences. The probability of differential propagation through S can take one of three values: 1, 2 -6 , or 2 -7 . To encode these probabilities, two additional Boolean variables w = (w (0) , w (1) ) are introduced, and the corresponding weight is computed as w (0) + 6w (1) . Hence, the 18-bit vector (∆X, ∆Y, w) must belong to the set

To enforce this, the model introduces a clause

for every 18-bit vector θ / ∈ Θ, thus forming a baseline SAT description of the S-box. However, because F 18 2 \Θ has 229758 elements, encoding all such clauses directly would produce an intractably large SAT problem. To mitigate this complexity, the ESPRESSO logic minimizer [6] is applied, reducing the model to 8599 clauses. This streamlined SAT model effectively captures the S-box's differential probability properties.

SAT Models for the Objective Function. Since the goal of the automatic search is to identify differential characteristics with high probabilities, the objective function in the SAT problem can be represented by a cardinality inequality:

γ-1 i=0 w i ⩽ ϖ, where w i are Boolean variables encoding the weights of possible differential propagations through S-boxes, and ϖ is a predefined upper bound on the characteristic's total weight. A common technique for translating this cardinality constraint into Boolean logic is the sequential encoding method [17] .

Wang et al. [22] demonstrated that when the upper and lower bounds of each partial sum

information can be integrated into the sequential encoding method to construct a more effective objective function model. The enhanced model significantly improves the efficiency of SAT-based searches. Due to space limitations, the two SAT models for the objective function are provided in Appendix A.


## Structural Properties of 19-Round Optimal Characteristics

Theoretically, confirming whether other 19-round differential characteristics with a probability of 2 -123 exist requires only a multi-solution SAT solver such as CryptoMiniSat [18] to enumerate these characteristics in SM4. However, our experiments with CryptoMiniSat suggest that there may be a very large number of such characteristics, and exhaustively exploring them is extremely time-consuming. In one instance, we ran the solver for 15 days and discovered only 77491 characteristics, yet the search remained incomplete.

Although we can select some of these 77491 characteristics that potentially facilitate more efficient key-recovery attacks than the one presented in [10] , this approach does not guarantee finding the truly optimal distinguisher. Consequently, rather than enumerating all 19-round optimal differential characteristics of SM4, we focus on analyzing both their shared and distinct properties. These properties closely tied to the probability of the derived distinguisher and the pre-sieving probability allow us to estimate an upper limit on the effectiveness of 19-round optimal differential characteristics for key-recovery attacks.

Maximum Number of Derived Characteristics from a Single Optimal Characteristic. As discussed in Sections 2.4 and 3.1, the probability of a distinguisher depends not only on the probability of its optimal characteristic but also on the number of differential characteristics derivable from that characteristic. Although the optimal characteristic in [10] achieves a probability of 2 -123 , it yields only 127 associated differential characteristics. In contrast, the distinguisher in [19] encompasses 127 2 characteristics. Because a greater number of characteristics can boost the probability of the distinguisher, we first investigate whether it is possible to find a 19-round characteristic with probability 2 -123 that generates at least 127 2 characteristics.

To explore this question, we revisit the differential characteristics presented in [19] and [10] . We observe that the characteristic proposed in [10] achieves a higher probability but involves 19 active S-boxes, whereas the best characteristic from [19] contains only 18 active S-boxes. Both works [19, 10] confirm that 18 is the minimum number of active S-boxes possible for a 19-round differential characteristic in SM4. Thus, we aim to determine whether a 19-round differential characteristic exists in SM4 that offers a probability of 2 -123 while maintaining exactly 18 active S-boxes.

We address this problem via automated searches. Because we must constrain both the probability of the characteristic and the number of active S-boxes, we employ a dual-objective SAT problem. In particular, we use Model 6 to limit the differential characteristic's weight to 123 and Model 5 to fix the number of active S-boxes at 18. Leveraging the SAT solver Kissat under these constraints yields the following property.

Property 2. The number of active S-boxes in any 19-round differential characteristic of SM4 with a probability of 2 -123 cannot be fewer than 19.

Because the minimum number of active S-boxes in a 19-round optimal differential characteristic is 19, the arrangement of these active S-boxes directly affects how many differential characteristics can be derived from the optimal one. For example, in the differential characteristic analyzed in Section 2.4 of [19] , there are two active S-boxes in the first round; consequently, under fixed output differences, the 127 2 choices of input differences yield 127 2 possible differential characteristics. This observation prompts the question of whether a 19-round differential characteristic with probability 2 -123 could also feature two active S-boxes in its first round.

To investigate the positions of active S-boxes in a 19-round optimal characteristic more comprehensively, we reformulate the problem into a SAT-based check. Specifically, we test whether a 19-round optimal differential characteristic can feature a round with no active S-boxes. Let w r,i be the 2-bit Boolean variable encoding the weight of the i-th S-box in the r-th round. We then incorporate the following model into our SAT problem to determine if the r-th round can indeed contain zero active S-boxes.


## Model 2

The r-th round of the differential characteristic contains no active Sboxes if and only if the variables w Our test results indicate that, when these conditions are successively introduced into the SAT problem, none of the 19 resulting SAT instances is solvable. Hence, we arrive at the following conclusion.

Property 3. In SM4, any 19-round differential characteristic with probability 2 -123 must have at least one active S-box in each round.

Since the maximum differential propagation probability of SM4's S-box is 2 -6 , and the probability of the optimal 19-round characteristic is 2 -123 , the number of active S-boxes in the optimal characteristic cannot exceed 20. By Property 3, this implies that the optimal 19-round differential characteristic may contain at most one round with two active S-boxes, with each of the remaining rounds featuring exactly one active S-box. To determine whether the r-th round of the optimal 19-round differential characteristic can accommodate two active S-boxes, we incorporate the following model into our SAT problem.


## Model 3

The r-th round of the SM4 differential characteristic has at least two active S-boxes if and only if the variables w

r,2 , and w (1) r,3 satisfy the following equations.

The test results show that, when these conditions are successively included in the SAT problem, all 19 instances become unsatisfiable. Therefore, we arrive at the following conclusion. Property 4. In every optimal 19-round differential characteristic of SM4, there are exactly 19 active S-boxes one in each round.

According to Property 4, the first round of an optimal 19-round differential characteristic must contain exactly one active S-box. As a result, the total number of differential characteristics derivable from a single optimal characteristic is capped at 127. Furthermore, the probability of any 19-round differential distinguisher constructed from an optimal characteristic is 2 -123.99 , matching the probability of the distinguisher discussed in Section 3.1.


## Maximum Pre-Sieving Probability for Optimal Characteristics.

As discussed in Sections 2.4 and 3.1, the pre-sieving probability is influenced by the XOR of the last three branches of the output difference, ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 .

A smaller number of nonzero bytes in ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 reduces the range of possible values for ∆X 23 in the first branch of the ciphertext pair, thereby decreasing the pre-sieving probability. In the distinguisher from [19] , ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 contains three nonzero bytes, whereas in the distinguisher from [10] , it contains four. Since our goal is to identify optimal 19-round differential characteristics for key-recovery attacks, we focus on whether a 19-round characteristic with a probability of 2 -123 can be found such that ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 has exactly three nonzero bytes. This condition is equivalent to asking whether there exists one zero byte in ∆X 20 ⊕∆X 21 ⊕∆X 22 . To test this, we integrate the following model into the SAT problem, enabling the solver to analyze whether the i-th byte of ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 is zero.

Model 4 In SM4's 19-round optimal differential characteristic, the i-th byte of ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 is zero if and only if, for every 0 ⩽ j < 8, the variables ∆X

, and ∆X (8i+j) 22 satisfy the following equations.

Test results indicate that each of the four bytes in ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 can independently be zero. Naturally, this raises the question of whether two of these bytes can be zero simultaneously. To explore this, we adapt the constraints from Model 4 and integrate them into the SAT problem. The solver's outcome reveals that, in SM4, no 19-round differential characteristic with probability 2 -123 has two zero bytes in the XOR of the last three branches of the output difference. Consequently, the minimum number of nonzero bytes in ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 is three. This finding also establishes the upper bound on the presieving probability for optimal differential characteristics in key-recovery attacks, consistent with the pre-sieving probability of 2 -11.03 reported in [19] . The four 19-round optimal differential characteristics identified via Model 4 are provided in Table 2 . In the next section, we examine the effectiveness of employing the fourth characteristic in differential key-recovery attacks.


## Attack Performance with the New Distinguisher

In this section, we present differential attacks on 23-round SM4 using a 19-round distinguisher derived from the fourth differential characteristic in Table 2 . To ensure fair comparisons with previously proposed distinguishers, we reimplement the attacks in [19, 26] using our new 19-round distinguisher. By applying the two paradigms introduced in Section 2.2, we accurately determine the complexities of these attacks in each scenario.

19-round distinguisher with a probability of 2 -123.99

Fig. 3 . Key-recovery attack on 23-round SM4 using the new distinguisher.

As depicted in Figure 3 , the 19-round distinguisher is applied to the first nineteen rounds of the cipher in both attacks. Its input difference has the form To generate plaintext pairs, we construct two pools, M 1 and M 2 , each containing 2 32 plaintexts:

where c 1 , c 2 , and c 3 are fixed constants in F 32 2 . We refer to the pair (M 1 , M 2 ) as a structure. Each structure contains 2 33 distinct plaintexts and can generate approximately 2 32 × 127 ≈ 2 38.99 plaintext pairs.


## Key-Recovery Attack Using the Method from [19]

Following the approach in [19] , the attack proceeds as follows. (1) For each remaining ciphertext pair (C, Ĉ), where C = (C 0 , C 1 , C 2 , C 3 ) and Ĉ = ( Ĉ0 , Ĉ1 , Ĉ2 , Ĉ3 ), partially decrypt to obtain the output difference of the zeroth S-box in the 22-nd round

and compute c 22 [0] = (L -1 (C 3 ⊕ Ĉ3 ⊕ ∆X 22 ))[0]. If RK 22 [0] is guessed correctly, then for all correct ciphertext pairs, we must have d 22 [0] = c 22 [0]. Discard any pairs that do not satisfy this condition. After this sieving, approximately m × 2 27.96 × 2 -8 = m × 2 19.96 ciphertext pairs remain. Next, repeat this guessing procedure for each of the other three bytes of RK 22 . Compute the corresponding S-box output and input differences d 22 [i] and c 22 [i] for i = 1 to 3. At each step, discard pairs whenever d 22 [i] ̸ = c 22 [i]. After these tests, the expected number of surviving pairs is m × 2 19.96 × 2 -24 = m × 2 -4.04 . (2) For each of the four bytes of RK 21 , guess its value and perform similar sieving steps on the remaining ciphertext pairs, as in Step 3(1). After applying these tests, the number of surviving ciphertext pairs becomes m × 2 -4.04 × 2 -32 = m × 2 -36.04 . (3) Similarly, guess each of the four bytes of RK 20 and apply the same sieving process. After these tests, the expected number of remaining ciphertext pairs is m × 2 -36.04 × 2 -32 = m × 2 -68.04 . (4) Next, guess RK 19 [0] and perform sieving similar to Step 3(1). Because of the chosen set Λ ′′ , the number of surviving pairs is m × 2 -68.04 × 1 127 = m×2 -75.03 . For each of RK 19 [1] and RK 19 [2] , guess its value and perform the same sieving as in Step 3(1) . Each guess further reduces the number of pairs by a factor of 1 127 . After both guesses, the expected number of remaining pairs is m × 2 -75.03 × 1 127 2 = m × 2 -89.01 . Since the last S-box in the 19-th round is inactive, there is no information available to recover RK 19 [3] .

Step 4. After completing the sieving steps, any 120-bit subkey guess (RK 19 [0-2], RK 20 , RK 21 , RK 22 ) that leaves at least a threshold τ number of ciphertext pairs is considered a candidate key. For each candidate key, guess the missing byte RK 19 [3] . Then, use at most two plaintext-ciphertext pairs to verify each fully reconstructed key by encrypting or decrypting with the guessed subkey values. Finally, the correct key is uniquely determined as the one that reproduces the observed ciphertexts or plaintexts upon encryption or decryption.

Analysis of the Attack Using the Hypothesis Testing Paradigm. Since the probability of the distinguisher is 2 -123.99 , the number of remaining pairs for the correct key follows a binomial distribution with parameters (N, p 0 ), where N = m × 2 38.99 and p 0 = 2 -123.99 . For incorrect keys, the number of remaining pairs follows a binomial distribution with parameters (N, p), where p = 2 -128 . We set the threshold τ to 3 and the success probability to 90%. By applying formulas (1) and (2) for numerical approximation, we obtain N = 2 126.40 and β = 2 -7.74 . Consequently, the number of structures used in the attack is m = 2 87.41 , leading to a data complexity of 2 120.41 chosen plaintexts.

The overall time complexity can be divided into three parts. T 1 = m × 2 33 is the cost of generating ciphertexts from the m × 2 33 plaintexts.

accounts for enumerating 120 bits of the round keys. T 3 = 2 128 ×β is the exhaustive search over the remaining key candidates plus the unguessed 8-bit subkey. Summing these yields T 1 + T 2 + T 3 = 2 122.77 23-round encryptions. The memory required for the attack is primarily used to store the remaining m × 2 27.96 ciphertext pairs in the second step. Therefore, the memory complexity of the attack is approximately m × 2 28.96 = 2 116.37 blocks.

As summarized in Table 1 , although our attack uses slightly more data than the 23-round attack of Su et al. [19] , it achieves lower time and memory complexities while ensuring at least a 90% success probability.


## Key-Recovery Attack Using the Method from [26]

In the attack described in [26] , the differential key recovery framework for partial substitution-permutation networks proposed in [1] is employed. Instead of performing exhaustive key enumeration, the primary idea is to generate key suggestions for each ciphertext pair. During the preprocessing phase, two matrices are constructed. The method for constructing matrices A and B is detailed in Appendix B. With these matrices prepared, the key-recovery process proceeds as follows.

Step I. By selecting m structures, we generate approximately m × 2

38.99 plaintext pairs from m × 2 33 plaintexts. Step II. For each pair (P, P ), compute the difference of the corresponding ciphertexts (C, Ĉ) and check whether the first word of the ciphertext difference is in Λ ′′ . If it is not, discard the pair. After this filtering, around m × 2 38.99 × 2 -11.03 = m × 2 27.96 pairs are expected to remain. Step III. For each remaining pair (C, Ĉ), perform the following steps. (1) Calculate (∆Z 19 , ∆Z 20 , ∆Z 21 , ∆Z 22 ) using matrix A from equation (6), which enables the computation of the input differences ∆Y i and output differences ∆Z i of the nonlinear transformation S in rounds 19 to 22. (2) For each of the 12 active S-boxes in rounds 20 to 22, check whether the differential transitions are possible according to the DDT; if any transition is impossible, discard this pair and return to Step III to analyze the next pair. In view of Property 1, the sieving probability for each active S-box is 127 256 , so after these checks, the expected number of surviving ciphertext pairs becomes m × 2 27.96 × 127 256 12 = m × 2 15.82 . (3) Based on the DDT, construct a list List of vectors containing all possible values for (Y 19 [0-2], Y 20 , Y 21 , Y 22 , Z 19 [0-2], Z 20 , Z 21 , Z 22 ), representing the inputs and outputs of all 15 active S-boxes in rounds 19 to 22. Since each S-box input and output occupies 16 bits, each of these vectors comprises 240 bits. (4) For each 240-bit vector in List, combine it with the known ciphertext C, apply matrix B (see equation (7)), and derive a candidate 120-bit key (RK 19 [0-2], RK 20 , RK 21 , RK 22 ). Then guess the missing byte RK 19 [3]. Verify each candidate by testing at most two plaintext-ciphertext pairs; if the correct ciphertexts are reproduced, output the 128-bit key.

Analysis of the Attack Using the Key Ranking Paradigm. In the keyranking framework, let p = 2 -128 , p 0 = 2 -123.99 , and the total number of possible keys be κ = 2 120 . Since each possible differential transition of the S-box yields an average of 2×126+4 127 = 2 1.01 correct pairs, the number of remaining key candidates is ℓ = m × 2 15.82 × 2 1.01×15 = m × 2 30.97 . By setting N = 2 122.83 and applying formula (5), we determine that the attack's success probability is approximately P S = 99.99%. From N = m × 2 38.99 , we obtain m = 2 83.84 , giving a data complexity of 2 116.84 chosen plaintexts.

The overall time complexity can be divided into four parts. T 1 = m × 2 33 is the time required to encrypt m × 2 33 plaintexts. T 2 is the time required to use matrix A to derive input and output differences for the nonlinear transformation S. Following the approach in [26] , we treat one computation of expression (6) as a single round of SM4 encryption. Thus, T 2 = m × 2 27.96 × 1 23 23-round encryptions. T 3 is the time needed to use matrix B to obtain 120-bit round-key candidates. We treat one computation of expression (7) as four rounds of SM4 encryption. Hence, T 3 = m × 2 30.97 × 4 23 23-round encryptions. T 4 is the time for brute-forcing the correct key, giving T 4 = m × 2 30.97 × 2 8 23-round encryptions. Summing these contributions, we obtain T 1 + T 2 + T 3 + T 4 = 2 122.84 23-round encryptions. The memory complexity is below 2 10 words of 128 bits, primarily for storing matrices A and B, since elements of List can be generated on-the-fly.

As summarized in Table 1 , although our attack uses more data than the 23round attack of Zhao et al. [26] , it achieves lower time complexity and a higher success probability.


## Conclusion

In this work, we revisit the 19-round differential characteristics of SM4, motivated by the observation that previously published optimal characteristics do not necessarily yield practical efficiency in key-recovery attacks. To address this shortcoming, we employ an automated search method to examine the properties of all optimal 19-round differential characteristics of SM4. Through Boolean encodings and comprehensive exploration, we identify three structural properties common to all such optimal characteristics and highlight four representative characteristics that are particularly well-suited for key recovery. Our detailed analysis of one such characteristic reveals that although it requires slightly more data compared to certain existing 23-round attacks, it achieves lower time and memory complexities under both the hypothesis testing and key ranking paradigms. These findings not only deepen our understanding of SM4's differential structure but also offer a strong foundation for future research. the ciphertext differences it is possible to calculate ∆Z 19 , ∆Z 20 , ∆Z 21 , and ∆Z 22 via the equation

where L -1 is the matrix representation of the inverse of L. Consequently, the matrix A that we seek to construct is the block diagonal matrix in expression (6), where each diagonal element is L -1 .

The second matrix B is used to generate key suggestions based on the ciphertexts and the differential transitions. Let ∆Y i denote the input difference to the nonlinear transformation S in the i-th round, and let Y i and Z i be the input and output values of S in the i-th round, respectively. After determining the differential transitions (∆Y i , ∆Z i ) for all rounds 19 ⩽ i < 23, the values of Y i and Z i become almost uniquely determined (ignoring the ciphertext order within each pair). Referring to the cipher structure in Figure 3 , we have the following equations for 0 ⩽ i < 4:

By combining these equations, we can derive expressions for RK 19 , RK 20 , RK 21 , and

The matrix B we construct is the block matrix in expression (7) .

> 13231 ≪ 13 ≪ 23 SFig. 1 . Fig. 1. Round function and key schedule of SM4.

> b) Key-recovery procedure using the distinguisher proposed by Li and Sun. ∆X0 = a ′ 0 ∆X1 = 263b8b26 ∆X2 = 479ad247 ∆X3 = 61835961

> = 1, 0 ⩽ i < 4.

> (a ′′ 0 , e793932d, 6fb9b98f, 882a2a9e), where a ′′ 0 ∈ {x ⊕ e79393d6 | Pr T (0000003c, x) > 0}. The probability of this 19round distinguisher is 2 -123.99 . Because the input difference for the nineteenth T function is ∆X 20 ⊕ ∆X 21 ⊕ ∆X 22 = 882a2a00, the difference ∆X 23 can only take values from Λ ′′ = {x ⊕ e7939348 | Pr T (882a2a00, x) > 0} , which contains 127 3 possible elements.

> 1 Step 1 . Select m structures to obtain approximately m × 2 38.99 plaintext pairs, generated from m × 2 33 plaintexts. Step 2. For each plaintext pair (P, P ), compute the difference of the corresponding ciphertexts (C, Ĉ). Check whether the first word of the ciphertext difference belongs to the set Λ ′′ . If not, discard the pair. After this filtering process, the expected number of surviving pairs is m × 2 38.99 × 2 -11.03 = m × 2 27.96 . Step 3. For each guess of RK 22 [0], perform the following steps.

> 1 Table 1 . Comparison of differential attacks on SM4.

> 2 Table 2 . Four optimal 19-round differential characteristics enabling effective differential attacks on SM4.

## Acknowledgements

The research leading to these results has received funding from the Shan-dong Key Research and Development Program (Grant No. 2024ZLGX05 ), the National Natural Science Foundation of China (Grant No. 62272273 , Grant No. 62002201 , Grant No. 62032014 ), and the National Cryptologic Science Fund of China (Grant No. 2025NCSF02006 ). Ling Sun gratefully acknowledges the support by the Program of TaiShan Scholars Special Fund for young scholars (Grant No. tsqn202306043 ) and Xiaomi Young Talents Program .

## References

1. b0: Achiya Bar-On, Itai Dinur, Orr Dunkelman, Virginie Lallemand, Nathan Keller, Boaz Tsaban. "Cryptanalysis of SP Networks with Partial Non-Linear Layers". Lecture Notes in Computer Science. 2015. DOI: 10.1007/978-3-662-46800-5_13
2. b1: A Biere, T Faller, K Fazekas, M Fleury, N Froleyks, F Pollitt. "CaDiCaL, Gimsatul, IsaSAT and Kissat entering the SAT Competition". Proc. of SAT Competition 2024 -Solver, Benchmark and Proof Checker Descriptions. 2024
3. b2: Eli Biham, Adi Shamir. "Differential Cryptanalysis of DES-like Cryptosystems". Lecture Notes in Computer Science. 1991-08. DOI: 10.1007/3-540-38424-3_1
4. b3: Eli Biham, Adi Shamir. "Differential Cryptanalysis of the Full 16-round DES". Lecture Notes in Computer Science. 1993-08. DOI: 10.1007/3-540-48071-4_34
5. b4: Céline Blondeau, Benoît Gérard, Jean-Pierre Tillich. "Accurate estimates of the data complexity and success probability for various cryptanalyses". Designs, Codes and Cryptography. 2011. DOI: 10.1007/s10623-010-9452-2
6. b5: Robert K Brayton, Gary D Hachtel, Curtis T Mcmullen, Alberto L Sangiovanni-Vincentelli. "Logic Minimization Algorithms for VLSI Synthesis". The Kluwer International Series in Engineering and Computer Science. 1984. DOI: 10.1007/978-1-4613-2821-6
7. b6: W Diffie, G L. "Index". ZigBee Wireless Networks and Transceivers. 2008. DOI: 10.1016/b978-0-7506-8393-7.00023-6
8. b7: Jonathan Etrog, Matt J B Robshaw. "The Cryptanalysis of Reduced-Round SMS4". Lecture Notes in Computer Science. 2009-08. DOI: 10.1007/978-3-642-04159-4_4
9. b8: Jongsung Kim, Seokhie Hong, Jaechul Sung, Sangjin Lee, Jongin Lim, Soohak Sung. "Impossible Differential Cryptanalysis for Block Cipher Structures". Lecture Notes in Computer Science. 2008. DOI: 10.1007/978-3-540-24582-7_6
10. b9: Bingqing Li, Ling Sun. "Exploring the Optimal Differential Characteristics of SM4". Lecture Notes in Computer Science. 2024. DOI: 10.1007/978-981-96-5566-3_1
11. b10: Ling‐chen Li, Wen‐ling Wu, Lei Zhang, Ya‐fei Zheng. "New method to describe the differential distribution table for large S‐boxes in MILP and its application". IET Information Security. 2019-09. DOI: 10.1049/iet-ifs.2018.5284
12. b11: Fen Liu, Wen Ji, Lei Hu, Jintai Ding, Shuwang Lv, Andrei Pyshkin, et al.. "Analysis of the SMS4 Block Cipher". Lecture Notes in Computer Science. 2007-07. DOI: 10.1007/978-3-540-73458-1_13
13. b12: Yu Liu, Huicong Liang, Muzhou Li, Luning Huang, Kai Hu, Chenhe Yang, et al.. "STP models of optimal differential and linear trail for S-box based ciphers". Science China Information Sciences. 2019. DOI: 10.1007/s11432-018-9772-0
14. b13: Yu Liu, Huicong Liang, Muzhou Li, Luning Huang, Kai Hu, Chenhe Yang, et al.. "STP models of optimal differential and linear trail for S-box based ciphers". Science China Information Sciences. 2021-03-23. DOI: 10.1007/s11432-018-9772-0
15. b14: Mitsuru Matsui. "On correlation between the order of S-boxes and the strength of DES". Lecture Notes in Computer Science. 1994. DOI: 10.1007/bfb0053451
16. b15: V Rijmen, J Daemen. "Advanced Encryption Standard (AES)". Proceedings of federal information processing standards publications. 2001. DOI: 10.6028/nist.fips.197
17. b16: C Sinz. "Towards an optimal CNF encoding of boolean cardinality constraints". Principles and Practice of Constraint Programming -CP 2005, 11th International Conference, CP 2005. 2005. DOI: 10.1007/11564751_73
18. b17: Mate Soos, Karsten Nohl, Claude Castelluccia. "Extending SAT Solvers to Cryptographic Problems". Lecture Notes in Computer Science. 2009-07-03. DOI: 10.1007/978-3-642-02777-2_24
19. b18: B Su, W Wu, W Zhang. "Differential cryptanalysis of SMS4 block cipher". Cryptology ePrint Archive. 2010
20. b19: Ling Sun, Meiqin Wang. "SoK: Modeling for Large S-boxes Oriented to Differential Probabilities and Linear Correlations". IACR Transactions on Symmetric Cryptology. 2023-03-10. DOI: 10.46586/tosc.v2023.i1.111-151
21. b20: Ling Sun, Wei Wang, Meiqin Wang. "Accelerating the Search of Differential and Linear Characteristics with the SAT Method". IACR Transactions on Symmetric Cryptology. 2021-03-19. DOI: 10.46586/tosc.v2021.i1.269-315
22. b21: Senpeng Wang, Dengguo Feng, Bin Hu, Jie Guan, Kai Zhang, Tairong Shi. "New method for combining Matsui’s bounding conditions with sequential encoding method". Designs, Codes and Cryptography. 2023-07-07. DOI: 10.1007/s10623-023-01259-9
23. b22: Jian Zhang, Wenling Wu, Yafei Zheng. "Security of SM4 Against (Related-Key) Differential Cryptanalysis". Lecture Notes in Computer Science. 2016. DOI: 10.1007/978-3-319-49151-6_5
24. b23: Lei Zhang, Wentao Zhang, Wenling Wu. "Cryptanalysis of Reduced-Round SMS4 Block Cipher". Lecture Notes in Computer Science. 2008-07. DOI: 10.1007/978-3-540-70500-0_16
25. b24: Wentao Zhang, Wenling Wu, Dengguo Feng, Bozhan Su. "Some New Observations on the SMS4 Block Cipher in the Chinese WAPI Standard". Lecture Notes in Computer Science. 2009. DOI: 10.1007/978-3-642-00843-6_28
26. b25: L Y Zhao Yan-Min, W Mei-Qin. "Improved differential attack on 23-round SMS4". Journal of Software. 2018. DOI: 10.13328/j.cnki.jos.005271
