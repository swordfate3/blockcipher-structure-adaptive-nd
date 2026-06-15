# Survey: 6 Years of Neural Differential Cryptanalysis

**Authors:** David Gerault, Anna Hambitzer, Moritz Huppert, Stjepan Picek

**Source PDF:** `2024_sok_neural_differential_cryptanalysis.pdf`

**Extraction:** `pdftotext -layout` fallback because GROBID timed out on this PDF.

## Extracted Text

```text
1




                   Survey: 6 Years of Neural Differential Cryptanalysis
                            David Gerault∗ , Anna Hambitzer∗ , Moritz Huppert† , and Stjepan Picek‡
                                             ∗ Technology Innovation Institute, UAE

                                                   {name}.{lastname}@tii.ae
                                        † Technical University of Darmstadt, Germany

                                                 moritz.huppert@tu-darmstadt.de
                                             ‡ Radboud University, The Netherlands

                                                       stjepan.picek@ru.nl




   Abstract—At CRYPTO 2019, A. Gohr introduced Neural                                                   I. I NTRODUCTION
Differential Cryptanalysis and used deep learning to improve
the state-of-the-art cryptanalysis of 11-round SPECK32. As of
February 2025, according to Google Scholar, Gohr’s article has
been cited 229 times. The variety of targeted cryptographic
                                                                                 T      HE security of most digital applications relies on cryptog-
                                                                                        raphy, the science of protecting the integrity, authenticity,
                                                                                 and confidentiality of data. Confidentiality is about ensuring
primitives, techniques, settings, and evaluation methodologies
that appear in these follow-up works grants a careful survey,                    that only intended parties can read exchanged data. Typically,
which we provide in this paper. More specifically, we propose a                  an encryption key is used in a secure cipher algorithm to
taxonomy of these 229 publications and systematically review the                 encrypt the plaintext into a ciphertext. The recipient, knowing
66 papers focusing on neural differential distinguishers, pointing               the decryption key, can easily retrieve the plaintext from this
out promising directions. We then highlight future challenges in
the field, particularly the need for improved comparability of
                                                                                 ciphertext. On the other hand, it is computationally intractable
neural distinguishers and advancements in scaling. This survey                   for an adversary who does not know the key.
helps researchers and engineers to identify the leading neural                      The cornerstone of symmetric cryptography, where the
differential attacks, compare their performance, and highlight                   encryption and decryption keys are the same, is block ciphers,
the outstanding open problems in AI-assisted cryptanalysis.                      which encrypt fixed-size messages, usually through iterations
  Index Terms—Neural Differential Cryptanalysis, Survey                          of a simple round function. Block ciphers play an important
                                                                                 role in confidentiality but can also serve as building blocks to
Glossary -—Key Concepts for Non-Cryptographers
                                                                                 construct other primitives [1], such as hash functions and MAC
Block Cipher                                                                     schemes. Therefore, the security analysis of block ciphers (or
   A symmetric-key algorithm in which the same secret key is used for both       cryptanalysis) is a crucially important field.
   encryption and decryption. It transforms an n-bit plaintext block into an
   n-bit ciphertext block through several rounds of non-linear substitution         In the classical security notion, Pseudo Random Permutation
   and linear permutation—effectively “scrambling” a bit sequence such as        (PRP) security, an adversary algorithm is assumed to have
   01001... into a key-dependent sequence like 01110.... Formally,               black-box access to an oracle function, implementing either
   it is a keyed bijection
                                                                                 (A) the studied block cipher (with a hidden, random key)
                         Ek : {0, 1} n −→ {0, 1} n .                             or (B) a random permutation. A block cipher is considered
PRP Security                                                                     secure under this notion if no such adversary can distinguish
   The indistinguishability game in which an adversary receives black-box        between situation A and B faster than using the trivial strategy
   access to either the real cipher oracle Ek ( · ) or a uniform random          of enumerating all possible keys to find one that matches the
   permutation on n-bit blocks and must decide which oracle it is.
Differential Cryptanalysis                                                       oracle’s output (A) or be convinced that no such key exists (B).
   An analytical technique that encrypts input pairs differing by a chosen       On the other hand, if a distinguisher exists, the block cipher
   difference ∆, traces how ∆ propagates through the rounds, and exploits        is considered broken, as a good distinguisher can usually be
   the resulting output-difference statistics to infer information about the
   secret key.                                                                   used to retrieve the key. The performance of a distinguisher
Neural Differential Cryptanalysis                                                is usually expressed in terms of time complexity (number of
   Differential cryptanalysis augmented with a neural network that learns        operations to be performed by the attacker), data complexity
   to distinguish ciphertext data produced by the cipher from data produced
   by a random permutation.                                                      (number of queries to the oracle), and memory complexity.
Neural Distinguisher                                                                The main goal of cryptanalysis is to estimate how many
   A trained network that outputs “cipher” or “random” for a ciphertext
   (or ciphertext pair). Accuracy strictly better than 50% constitutes a
                                                                                 iterations of the round functions (or rounds) are needed for
   successful distinguisher under the relevant security notion.                  security. This is an iterative process, and new results continue
Neutral Bits (NBs)                                                               to be published regularly years after the release of a cipher.
   Input-bit positions that can be flipped in both texts of a pair without
   breaking the targeted differential trail, yielding 2|N B| additional usable
                                                                                 Therefore, cryptographers are eager to build and improve tools
   pairs at negligible cost.                                                     that help with this tedious task. Differential cryptanalysis,
Wrong-Key Randomization                                                          first introduced by Biham and Shamir in 1991 [2], examines
   The working assumption that statistic(s) generated under an incorrect
   key follow the same distribution as those obtained from a truly random
                                                                                 how input differences (δ) propagate through block ciphers,
   permutation, enabling efficient pruning of wrong key guesses.                 seeking high-probability differentials where specific plaintext
                                                                                 differences yield predictable ciphertext differences (∆). Tradi-
                                                                                                                                                        2




Fig. 1. Neural Differential Distinguisher: Basic Training Pipeline. Start with two plaintext P0 , P1 , where P0 ⊕ P1 = δ or P0 ⊕ P1 = rand. Encrypt
them using a symmetric key K to obtain ciphertexts C0 , C1 . Concatenate the ciphertexts C0 |C1 and input them into a neural distinguisher N D. The neural
distinguisher’s output is a neuron with a sigmoid activation function. The sigmoid curve indicates a binary decision output to answer if P0 ⊕ P1 = δ.



tional approaches rely on mathematical analysis of difference                 networks could serve as superior distinguishers in what is now
propagation through cipher rounds, calculating probabilities                  termed neural differential cryptanalysis. Despite their black-
that given input differences produce specific output differ-                  box nature, these networks consistently outperformed tradi-
ences to create distinguishers. While this technique proved                   tional methods by learning to identify subtle patterns in cipher-
devastatingly effective against early ciphers, modern designs                 text pairs that indicate whether they originated from structured
incorporate specific countermeasures that make conventional                   versus random input differences, as illustrated in Figure 1.
differential analysis increasingly challenging and computation-               Gohr’s approach proved particularly effective against the NSA-
ally intensive, requiring extensive manual analysis of cipher                 designed SPECK32 [18] cipher, demonstrating superior ac-
structure and often yielding suboptimal distinguishers for                    curacy on 8-round variants while significantly reducing time
complex round functions. Deep learning, due to its strength                   complexity for 11-round key recovery attacks. Once trained,
at detecting and distinguishing patterns, has long been seen as               these neural distinguishers serve as critical components in
a potential candidate to assist the task of cryptanalysis.                    practical recovery attacks, as illustrated in Figure 2, funda-
   Deep learning has experienced significant advancements in                  mentally challenging conventional cryptanalysis assumptions
recent years, leading to remarkable achievements in various                   and enabling automated analysis of cipher variants without
domains. Initially, Frank Rosenblatt introduced Multi-Layer                   extensive manual mathematical investigation.
Perceptrons (MLPs) in his 1958 book Perceptron and laid the                      Since Gohr’s seminal paper, researchers have explored every
foundation for modern neural networks. The introduction of                    part of the basic Neural Differential Cryptanalysis pipeline.
Convolutional Neural Networks (CNNs) in the 1980s [3] led                     A majority of the works citing Gohr that focus on neural
to a breakthrough in computer vision in the form of LeNet,                    differential distinguishers have attempted to apply the scheme
which achieved human-level performance in digit recognition                   to 24 different symmetric-key primitives (with SPECK and
in 1998 [4]. Through advancements in Monte Carlo Tree                         SIMON families receiving the most attention at 38 and 36
Search (MCTS) and reinforcement learning, further leaps were                  experiments respectively), improve the distinguishing advan-
enabled, such as Google’s AlphaGo surpassing human capa-                      tage by developing 15+ distinct network architectures (from
bilities [5], [6], [7]. More recently, transformer-based Large                the dominant N DGohr to specialized approaches like DBit-
Language Models (LLMs) [8], such as GPT, have revolution-                     Net, SE-ResNet, and even quantum neural networks), scaling
ized natural language processing, demonstrating near-human                    training data from 20K to 32.48 billion samples (though
capabilities in tasks like machine translation and language                   20M remains the de facto standard), or innovating sample
generation.                                                                   formats (including advanced feature engineering techniques
   Despite the long-standing recognition of the intersection                  that have been shown to improve distinguishing accuracy).
between cryptography and machine learning [9], [10], [11],                    Finally, we also observe emerging research directions aimed
the use of computational intelligence in cryptanalytic tasks                  at enhancing neural distinguishers across multiple dimensions:
has remained limited. Early approaches typically relied on                    increasing automation of the attack pipeline (exemplified by
extensive precomputation [12], exploited implementation flaws                 DBitNet’s cipher-agnostic approach and AutoND flags in 21
(e.g., side-channel attacks) [13], targeted inherently weak                   experiments), improving transparency through explainability
cryptographic schemes [14], [15], or generally proved ineffec-                techniques that reveal the cryptographic features being learned
tive [16]. It was not until Gohr’s seminal work [17], presented               (as seen in ensemble approaches), and boosting effectiveness
at CRYPTO 2019, that a breakthrough was achieved by com-                      of the obtained neural distinguishers in practical key recovery
bining deep learning with traditional cryptanalytic techniques.               attacks.
Gohr’s work was the first to demonstrate that neural networks                    The explosive growth of neural cryptanalysis literature has
could be successfully leveraged in cryptanalysis, producing                   created an increasingly fragmented landscape that poses sig-
attacks that improved upon state-of-the-art techniques against                nificant barriers to systematic knowledge synthesis. This rapid
a round-reduced version of a modern block cipher.                             expansion has outpaced efforts to establish coherent theoretical
  Gohr’s groundbreaking work [17] established a new                           foundations and standardized methodologies, creating partic-
paradigm in cryptanalysis by demonstrating that deep neural                   ular challenges for interdisciplinary researchers who must
                                                                                                                                                          3




                     Encryption Oracle
                                             C0 = Ekr+1 (P0 )
                       P0 ⊕ P1 = δ                                           C0 ||C1
                                             C1 = Ekr+1 (P1 )


                                                              Adversary
                                                                               −1
                                                                        C0′ = Drk (C0 )
                                                                          ′    −1               rk ← {0, 1}m
                                                                        C1 = Drk  (C1 )


                                                                p≪1          C0′ ||C1′


                                                                                                      p≈1
                                                                              N Dr                                             rk



Fig. 2. Neural Differential Distinguisher: Basic Key Recovery Pipeline. An encryption oracle generates an (r + 1)-round ciphertext pair with input
difference δ. The adversary decrypts one round using a key guess rk and feeds the result to a neural distinguisher trained on the r-round distribution. Keys
producing prediction scores near 1 are output as candidates, following the wrong-key randomization hypothesis [17].



navigate both cryptographic principles and machine learning                         atically classify and compare peer-reviewed research out-
techniques. The absence of systematic knowledge organization                        comes on neural differential distinguishers (section VIII),
has fostered several critical problems: redundant research                          across various techniques, architectures, and primitives.
efforts where teams independently investigate nearly identical                      We also identify promising research directions and severe
questions while remaining unaware of parallel work, leading                         methodological issues in some peer-reviewed papers and
to duplicated findings and contradictory claims such as [19]’s                      challenge their results.
erroneous assertion of developing the first truncated neural                     4) Best Practice Recommendations: Evaluating research
distinguisher; fundamental disagreements on core methodolog-                        involving the training of neural networks presents sig-
ical questions, exemplified by the conflicting assessments of                       nificant challenges. We have developed a comprehen-
neural architecture suitability among [20], [21], and [22]; and                     sive set of best-practice guidelines specifically tailored
persistent misinterpretations of foundational concepts, partic-                     for reviewers of Neural Differential Cryptanalysis re-
ularly regarding the proper aggregation of multiple ciphertext                      search (section IX).
pair predictions – an issue that Gohr explicitly addressed                       5) Future Challenges: Finally, we identify and discuss two
in [23] yet continues to be misunderstood in subsequent work.                       major challenges set to shape the next six years of neural
As this field’s rapid expansion shows no signs of abating,                          cryptanalysis (section X).
these structural problems will inevitably intensify without
intervention, underscoring the urgent need for a comprehensive                                          II. R ELATED W ORK
survey that can establish coherent theoretical frameworks and
                                                                                  While a substantial body of literature has focused on devel-
standardized practices in Neural Differential Cryptanalysis.
                                                                               oping and analyzing effective neural differential distinguishers,
      a) Our Contributions.: In our survey, we have achieved                   this paper is, to the best of our knowledge, the first to
the following:                                                                 systematically organize a large collection of research (229
  1) Comprehensive Field Review: We conducted an exhaus-                       papers) and highlight promising directions and challenges in
     tive survey of the follow-up work (section V). In this pro-               this area. Recent surveys [24], [25], [26], [27], [28] do not
     cess, we have identified the full body of research in the                 claim a systematic approach, cover a significantly smaller body
     field of Neural Differential Cryptanalysis. We analyzed                   of work, and most lack a specific focus on machine learning-
     the directions of the field, resulting in a detailed taxon-               based cryptanalysis.
     omy of Neural Differential Cryptanalysis (section V).                        Bellini et al. in [24] examine machine learning-based
  2) Explainability and Key Recovery Overview: We pro-                         black-box and white-box cryptanalysis. Regarding white-box
     vide a comprehensive overview of recent advancements                      cryptanalysis, they reference Gohr’s work [17] along with
     in explainability techniques using neural differential dis-               15 related follow-up studies, though these were not selected
     tinguishers (section VI). Since analyzing neural distin-                  systematically and include preprints. Nitaj and Richidi, in [25],
     guishers constitutes the core contribution of our work,                   explore various cryptographic areas that could benefit from the
     we provide a comprehensive overview of advancements                       application of artificial intelligence (AI). While they briefly
     in neural-aided key recovery (section VII) as a contextual                mention the potential of machine learning to enhance side-
     application of our findings.                                              channel and cryptanalytic attacks on symmetric block ciphers,
  3) Rigorous Classification and Comparison: We system-                        they neither provide a systematic analysis of existing work in
                                                                                                                                                  4



this area nor delve into the specific methodologies involved.          In 2002, Castro et al. used evolutionary algorithms to con-
Awad and El-Alfy, in [29], conduct a survey on computational        struct a cryptanalytic tool that can distinguish between the two-
intelligence applications in cryptography, with a focus on          round TEA algorithm and random permutations [35]. In 2007,
the automated design and cryptanalysis of ciphers. However,         Laskari et al. considered the application of diverse computa-
their work predates Gohr’s introduction of differential machine     tional intelligence techniques to the cryptanalysis of known
learning-based cryptanalysis in [17], and as a result, it does      cryptosystems, including public key cryptosystems and Feistel
not include a comprehensive review of neural distinguishers         ciphers [36]. In the same year, Tapiador et al. used heuristics to
found in more recent literature. Singh et al. [28] investigate      conduct nonlinear cryptanalysis and applied it to the MARS
various machine learning and optimization techniques, includ-       cipher S-box [37]. In 2012, Chou et al. experimented with
ing Hill Climbing and Particle Swarm Optimization, applied          machine learning techniques to mount distinguishing attacks
to cryptanalysis. They also reference Gohr’s research [17]          and concluded it is not possible to extract useful information
along with 12 subsequent studies that build upon it. However,       from ciphertexts produced by modern ciphers operating in
the selection of these papers is not based on a systematic          secure modes, nor to distinguish them from random data [26].
methodology. The work by Martinez et al. [27] is the most           On the other hand, Svenda et al. in 2014 used evolutionary
comparable to ours. Although it does not follow a systematic        algorithms to construct empirical tests for randomness [38].
paper selection process, it aims to capture the state-of-the-art       Finally, in 2017, Awad and El-Alfy surveyed computational
and categorizes 10 works, including Gohr’s, based on their          intelligence applications in cryptography, focusing on the
architectures and the cryptographic schemes they target.            automated design and cryptanalysis of ciphers [29].

      III. AI AND C RYPTOGRAPHY IN THE B EGINNINGS                                       IV. P RELIMINARIES
The popularity and widespread adoption of neural differential       This section introduces key concepts in machine learning-
distinguishers (more precisely, deep learning-based cryptanal-      assisted differential cryptanalysis: conventional differential
ysis) can be credited to the seminal work of A. Gohr [17].          cryptanalysis (subsection IV-A), deep learning applications
However, even in that work, the author mentioned a number           (subsection IV-B), and neural network-aided key recovery
of related works at the intersection between cryptanalysis and      (subsection IV-C).
AI. What distinguishes Gohr’s work from previous ones is that
it considers relevant (modern) ciphers and manages to obtain        A. Differential Cryptanalysis
results that surpass state-of-the-art conventional cryptanalysis    Differential cryptanalysis [2] is a chosen plaintext attack
techniques. The following section is not meant to provide           analyzing how plaintext perturbations propagate through ci-
an exhaustive list of works connecting AI and cryptology            phers. While typically using bitwise XOR differences, some
but rather provide a brief historical overview of various           approaches employ modular addition or rotations. For a map
approaches.                                                         F : {0, 1}b → {0, 1}b , a differential transition is a pair
   Already in 1947, researchers started considering connec-         (δ, ∆) ∈ {0, 1}b × {0, 1}b with probability:
tions between cryptography and artificial intelligence [9].
                                                                                          ({x ∈ {0, 1}b : F (x) ⊕ F (x ⊕ δ) = ∆})
While this attempt was devoid of any technical details, it            P (δ → ∆) =                                                 .
still showcases the interest of the scientific community in                                                   2b
combining these two domains. In 1984, L. Valiant discussed          B. Training Neural Differential Distinguishers
learnable Boolean functions and mentioned the evidence from
                                                                    For plaintexts p1 , p2 ∈ {0, 1}b with ciphertexts ci = F (pi ) ∈
cryptography that the whole class of functions computable by
                                                                    {0, 1}b , neural distinguishers approximate the function for
polynomial-size circuits is not learnable [10]. Shortly after, in
                                                                    fixed difference δ ∈ {0, 1}b :
1988, Minsky and Papert showed that every Boolean function                                       (
can be realized by an MLP neural network [30]. In 1994, R.                                         1, if p1 ⊕ p2 = δ,
Rivest wrote a paper on connections between cryptography                          Y (c1 ||c2 ) =
                                                                                                   0, else.
and machine learning [11]. Already there, he mentioned the
possibility of using machine learning for cryptanalysis.              Success requires identifying nonrandom properties in out-
   In 2002, Klimov et al. analyzed the security of a key            put distributions resulting from input difference δ. Training
exchange protocol based on mutually learning neural net-            typically uses balanced datasets: 50% samples (c1 , c2 , 0) with
works [31]. While the authors experimentally verify that it         random p1 , p2 , and 50% samples (c1 , c2 , 1) where p2 = p1 ⊕δ.
is unlikely for a particular attacker using a similar neural        Networks are trained via stochastic gradient descent [39]1
network to converge to the same key, they still break the           using loss functions such as mean squared error.
protocol using more advanced cryptanalytic techniques. Simi-          1 We introduce essential machine learning terminology needed to understand
larly, in 2016, Abadi and Andersen employed neural networks         the techniques used in neural differential cryptanalysis: Stochastic gradient
in a framework inspired by generative adversarial networks          descent is an iterative optimization method that updates the weights of a neural
                                                                    network by calculating error gradients on small random subsets (”batches”)
(GANs) to develop an encryption scheme [32]. Although this          of the training data rather than the entire dataset. The ”loss function” (e.g.,
early research did not show any formal security, Coutinho et        mean squared error) quantifies prediction error, while an ”epoch” represents
al. demonstrated in 2018 [33] that, with certain architectural      one complete pass through the training dataset. The Adam optimizer is an
                                                                    advanced gradient descent variant that adapts learning rates individually for
modifications, the network could be trained to learn the One-       each weight. L2 regularization prevents overfitting by penalizing large weight
Time Pad [34].                                                      values, essentially constraining the model’s complexity.
                                                                                                                                           5



   Following Gohr [17], effective implementations use approx-         an r-round neural distinguisher, yielding an (s + r)-round
imately 107 training samples, 106 testing samples, batch sizes        distinguisher. This combination introduces a fundamental com-
around 5000, and up to 200 training epochs. Performance               plexity tradeoff inherent to differential cryptanalysis. In Gohr’s
enhancements often include Adam optimizer [40], L2 regu-              implementation [17], the selected 2-round differential transi-
                                                                                                   1
larization [41], and cipher-specific architectures [23], [42].        tion exhibits probability 64   , necessitating an average increase
                                                                      of 64-fold in data complexity while extending the 7-round
C. Neural-aided Key Recovery                                          neural distinguisher to achieve 9-round coverage.
                                                                         The integration of classical and neural techniques presents
Neural distinguishers N D that approximate Y (c1 ||c2 ) enable
                                                                      a significant challenge in score aggregation. When prepending
practical key recovery attacks on block ciphers, demonstrating
                                                                      classical differentials, the aggregation of scores across multiple
their concrete cryptanalytic value. This section outlines the
                                                                      ciphertext pairs becomes problematic due to non-conforming
attack methodology based on Gohr’s seminal approach [17],
                                                                      pairs that introduce stochastic noise, degrading distinguisher
which has become the standard framework in subsequent
                                                                      performance. This limitation is addressed through the strategic
research. We denote the r-round reduced block cipher with
                       r                                              deployment of (Probabilistic) Neutral Bits (PNBs), which en-
secret key K as FK       .
                                                                      hance the signal-to-noise ratio. For a neutral bit i, pairs (p1 , p2 )
     a) The Basic Attack: The attack leverages a pre-trained
                                                          r+1         satisfying differential δ → ∆ ensure that (p1 ⊕ (1 ≪ i), p2 ⊕
neural distinguisher N Dr for F r to compromise FK             with
                                                                      (1 ≪ i)) also conform to the differential with probability 1
secret key K. For example, a 5-round SPECK32/64 distin-
                                                                      (or high probability for PNBs). Consequently, utilizing j PNBs
guisher enables attacks on 6-round SPECK32/64.
                                                                      enables the construction of plaintext structures containing 2j
   The attack targets the last round key kr+1 in round-based
                                                                      pairs where conformance to the prepended differential exhibits
ciphers that use function fk with keys k1 , . . . , kr+1 derived
                                                                r+1   binary behavior: either all pairs within the structure satisfy the
from master key K and begins by querying the oracle FK
                                                                      differential or none do, thereby ensuring consistent scoring
with a conforming pair p1 and p2 = p1 ⊕δ, obtaining ciphertext
                                                                      mechanisms. This methodology was subsequently extended
pair (c1 , c2 ). Next, for some random key guess k ′ , the attacker
                                                                      to incorporate conditional simultaneous neutral bit-sets and
computes c′i = fk−1                                     ′   ′
                       ′ (ci ) and evaluates R = Dr (c1 , c2 ). We
                                                                      switching bits for adjacent differentials [43].
rank key candidates by prediction score, as the correct key
                                                                            c) Reducing Computational Cost.: Gohr’s approach
yields R ≈ 1 (the distribution matches what N Dr was trained
                                                                      achieves significant computational complexity reduction
to recognize), while incorrect keys produce R < 1, following
                                                                      through the application of Bayesian optimization to key search
the wrong-key randomization hypothesis [17].
                                                                      procedures [17]. This methodology represents a departure
   For SPECK32, where round keys (16 bits) are smaller
                                                                      from exhaustive key enumeration toward statistically informed
than the master key (64 bits), we can feasibly enumerate all
                                                                      search strategies. The technique initiates by constructing a
candidates. After identifying the last round key, the process
                                                                      Wrong Key Response Profile (WKRP) that characterizes the
can be repeated to recover earlier round keys until the entire
                                                                      distributional properties of neural distinguisher responses un-
sequence is reconstructed.
                                                                      der incorrect key hypotheses.
   Our simplified attack explanation omitted that prediction
                                                                         For a ciphertext pair (c1 , c2 ) derived from plaintexts p and
scores exhibit variance, which can be mitigated by aggregating
                                                                      p⊕δ, with correct r-round key k and candidate key k ′ = k⊕γ,
scores across multiple ciphertext pairs for each key candidate,
                                                                      the distinguisher response is modeled as:
thereby enhancing the statistical reliability of the distinguisher.
In [17], the responses for a given key guess k ′ are aggregated                    RD,γ (c1 , c2 ) = D fk−1          −1
                                                                                                                              
                                                                                                           ′ (c1 ), fk ′ (c2 )
into a single score by the equation:
                              n             ′
                                                !                     where D represents the neural distinguisher and fk−1      ′  denotes
                           X            Rik                           single-round decryption. The response variable RD,γ is char-
                    sk′ =       log2          ′   ,
                            i=1
                                      1 − Rik                         acterized by a normal distribution with parameters µγ and σγ
                                                                      that depend functionally on the key difference γ.
where Rik represents the distinguisher’s response for the i-th           The key search algorithm operates iteratively, employing
ciphertext pair.                                                      an acquisition function derived from the WKRP to optimize
      b) Extending the Rounds Covered by the Distinguisher.:          candidate selection. Given observed responses R1 , . . . , Rn
Neural distinguishers can effectively extend their coverage by        corresponding to key candidates k1′ , . . . , kn′ , the optimization
exploiting structural properties of ARX ciphers. For ciphers          procedure selects subsequent candidates k by minimizing:
such as Speck and Simon, where initial subkey addition occurs
                                                                                             n−1
after the first nonlinear operation, neural distinguishers gain                              X    (Ri − µk⊕ki′ )2
an additional round without computational overhead. This                                               2
                                                                                                      σk⊕k
                                                                                              i=0          i
extension is achieved by constructing plaintext pairs that
deterministically yield ciphertext differences corresponding to       This formulation aligns the precomputed wrong key response
the neural distinguisher’s trained input difference δ following       profile optimally with empirically observed values, typically
the first round transformation.                                       converging within a limited number of iterations compared to
   Furthermore, neural distinguishers can be combined with            exhaustive round key enumeration.
classical differential cryptanalysis through a hybrid approach          To mitigate computational overhead from unpromising
that prepends an s-round classical differential transition to         search directions, Upper Confidence Bounds (UCB) serve as
                                                                                                                                        6



algorithmic stopping criteria. For t independent encryption           the proposal of a new cipher [129], [130], [131], [132], neural
         r+1
oracles FK   , the attack prioritizes instances according to:         output prediction attacks [133], [134], [135], [136], neural
                                    s                                 integral distinguishers [137], [138], [139], neural attacks on
                         i             log2 (j)                       protocols [140], [141], post-quantum schemes [142], [143],
                  sk = wmax  +α·
                                          ni                          pseudorandom number generators [144], [145], or other un-
          i                                                           related topics [146], [147], [148], [149], [150], [151], [152],
where wmax     represents the maximum distinguisher score
                                                                      [153], [154], [155], [156], [157], [158], [159], [160], [161],
achieved for instance i, ni denotes the computational iterations
                                                                      [162], [163], [164], which leaves us with a total of 66
allocated to instance i, j corresponds to the current global
                                                                      peer-reviewed publications in the field of Neural Differential
iteration, and α = 10. This formulation implements an
                                                                      Cryptanalysis.
exploration-exploitation tradeoff that concentrates computa-
tional resources on instances demonstrating either insufficient          The Body of Peer-Reviewed Research in Neural
exploration or elevated key candidate scores.                            Differential Cryptanalysis
      d) Additional Verification.: The verification phase ad-
dresses the challenge of near-correct key candidates producing           The full body of peer-reviewed publications that focus
high neural distinguisher scores. Candidates differing by 1-             specifically on advancing research of Neural Differential
2 bits from the correct key often generate elevated scores,              Cryptanalysis is [20], [165], [22], [166], [167], [168],
requiring localized search within the Hamming neighborhood               [169], [42], [170], [171], [172], [173], [174], [175],
of promising candidates to identify the correct key with                 [176], [177], [178], [179], [180], [181], [182], [183],
marginally superior scores.                                              [184], [185], [186], [187], [188], [189], [190], [191],
   Gohr implements joint recovery of (r + 1)-round and r-                [192], [193], [194], [195], [196], [197], [198], [199],
round keys by combining distinguishers Dr and Dr−1 . The                 [200], [201], [21], [202], [203], [204], [205], [19], [206],
protocol triggers r-round key search using Dr−1 when an (r+              [207], [208], [209], [210], [211], [212], [213], [214],
1)-round candidate exceeds threshold t1 , returning both keys            [215], [216], [217], [218], [219], [220], [221], [222],
only when an r-round candidate surpasses threshold t2 . This             [223], [224], [225]
cascaded approach provides verification, as incorrect (r + 1)-
round keys rarely generate elevated scores for corresponding          B. Taxonomy of Research Directions
r-round hypotheses, reducing false positives.
                                                                      We found contributions to the explainability (or interpretabil-
      V. N EURAL D IFFERENTIAL C RYPTANALYSIS : A                     ity) of neural distinguishers in the following 17 works [165],
         TAXONOMY OF R ESEARCH D IRECTIONS                            [167], [169], [173], [175], [176], [17], [178], [180], [182],
                                                                      [190], [193], [194], [203], [19], [217], [225], and will discuss
A. Selected Literature                                                their respective contributions in section VI.
As of February 03, 2025, a total of 229 works cite Gohr’s             We found contributions to neural-aided key recovery attacks in
work [17] on Google Scholar. Among these, we discarded                the following 22 works [166], [169], [173], [174], [17], [181],
4 references that were either redundant or not linked to a            [182], [187], [186], [189], [193], [194], [201], [19], [206],
paper, and 33 that were not available in English. Additionally,       [207], [212], [217], [224], [222], [219], [225], and will give
34 references are not peer-reviewed, and only available as            an overview of these works in section VII.
preprints [44], [45], [46], [43], [47], [48], [49], [23], [50],          Most (62/66) of peer-reviewed research on Neural Differen-
[51], [52], [53], [54], [55], [56], [57], [58], [59], [60], [61],     tial Cryptanalysis involves training neural differential distin-
[62], [63], [64], [65], [66], [67], [68], [69], [70], [71], [72],     guishers. More precisely, neural differential distinguishers are
[73], [74], [75]. After excluding these, we are left with 158         trained in [165], [20], [22], [166], [167], [42], [168], [169],
peer-reviewed references, which we systematically categorize          [171], [172], [173], [174], [175], [176], [177], [179], [181],
as shown in Figure 3.                                                 [180], [182], [183], [184], [185], [187], [186], [188], [190],
   We consider the following references outside the field of          [191], [189], [192], [193], [194], [195], [197], [199], [200],
research on Neural Differential Cryptanalysis as they are             [201], [21], [202], [204], [203], [19], [205], [206], [207],
surveys, overviews, theses, or book chapters that treat the use       [208], [209], [210], [211], [212], [213], [214], [215], [216],
of “ML in cryptography” [24], [76], [77], [27], [78], [25],           [217], [218], [220], [221], [222], [224], [223], [219], [225].
[79], [80], [81], [82], [83], [84], [85], or their research focuses      A comparative review of the peer-reviewed neural differen-
on other topics such as: classical cryptanalysis [86], [87],          tial distinguishers from 55 papers (including Gohrs’ seminal
[88], [89], [90], [91], [92], [93], [94], [95], [96], [97], the       work [17]) is provided in subsection VIII-C. We excluded pa-
theory of Neural Differential Cryptanalysis [98], cryptanalysis       pers that were inaccessible [170], [198], focused primarily on
of historic or toy ciphers [99], [100], [101], [102], [103],          explainability [203], lacked concrete accuracy measurements
[104], deep learning-supported design of cryptographic algo-          [181], utilized leakage models outside conventional security
rithms [105], [106], [107], [108], [109], [110], [111], neural        assumptions [205], [183], or prioritized input difference com-
side-channel attacks [112], [113], [114], [115], distinguishers       patibility over distinguisher performance in hybrid approaches
between different ciphers [116], [117], [118], [119], neural          [216], [213].
preimage attacks [120], [121], [122], the introduction of a              Two recent papers [182], [193] investigating neural dif-
new tool or library [123], [124], [125], [126], [127], [128],         ferential attacks on large-state block ciphers predominantly
                                                                                                                                                                        7




                                               Neural Attacks on PRGs 1%
                                 Neural Attacks on Post-Quantum 1%
                                   Neural Attacks on Protocols 1%
                              Neural Integral Distinguishers 2%
                                                                                                                                    Neural Differential Cryptanalysis
                              Neural Output Prediction 3%                                                                                         42%

                                  Cipher Proposal 3%


                            New Tool or Library 4%


                     Neural Preimage Attacks 2%

                       Cipher Distinguishers 3%


                 Neural Side-Channel Attacks 3%




                                 Unrelated Topics 12%



                                                                                                                              Surveys, Book Chapters, or Theses
                                  Theory of Neural Cryptanalysis 1%                                                                          8%
                                             Deep Learning-Supported Design
                                                           4%
                                                                                                 Classical Cryptanalysis 8%
                                                                    Historic or Toy Ciphers 4%



Fig. 3. Our taxonomy of the peer-reviewed English-language publications that cite Gohr’s seminal work [17].



emphasize key recovery methodologies while providing lim-                                        in various ways to add some explainability to a neural network,
ited insights into their neural network training processes. This                                 e.g., by pruning, ablation studies, or visualization techniques.
methodological opacity presents significant challenges for our                                         a) Understanding the learned cryptanalytic features: A.
comparative review. However, Huang et al. [182] provide their                                    Gohr investigated the capabilities of provided neural networks
implementation, enabling a more comprehensive evaluation                                         by introducing a differential cryptanalytic task called the
of their approach despite the initial presentation’s technical                                   real differences experiment [17]. This experiment involved
brevity.                                                                                         applying a uniform random mask to both ciphertexts in a
   Gohr’s analysis was performed within the secret key chosen-                                   candidate pair, thereby preserving the differential relationship
plaintext attack (SK/CPA) model. We do not consider the work                                     (the XOR difference pattern between encrypted pairs) while
of Phan et al. [196] as it operates under a fundamentally                                        mathematically obscuring the actual bitwise difference from
different adversary model, where generative AI techniques                                        the neural network. Statistical analysis of the neural distin-
are trained in an adaptively chosen ciphertext or known key                                      guisher’s performance demonstrated that it maintained classi-
scenario to distinguish 10-round SPECK32/64, making direct                                       fication accuracy exceeding that of random guessing. This em-
comparison inappropriate.                                                                        pirical evidence suggests that such neural architectures exploit
                                                                                                 cryptographically relevant features beyond those captured in
VI. OVERVIEW: N EURAL D IFFERENTIAL D ISTINGUISHER                                               conventional difference distribution tables (DDTs, which are
                 E XPLAINABILITY                                                                 lookup tables storing how input differences propagate through
Neural distinguishers (neural networks that can identify non-                                    a cipher).
random patterns in encrypted data), enabling new cryptanalytic                                      In [165], Benamira et al. studied the properties of pairs
attacks, potentially better than manual cryptanalysis, motivated                                 that were correctly classified and proposed that Gohr’s neural
researchers to try to understand what made these attacks so                                      distinguishers learn differential-linear features (a combination
powerful and to learn new properties from them. The lack                                         of differential cryptanalysis, which tracks difference propaga-
of explainability is the “machine’s inability to explain its                                     tion, and linear cryptanalysis, which exploits linear approx-
decisions and actions to human users” [226]. One of the                                          imations). In particular, the authors observed that the pairs
major efforts in research on explainability was the 4-year pro-                                  for which the score of the neural distinguisher at round 5 is
gram (2017-2021)“ XAI” by the Defense Advanced Research                                          high often follow a specific truncated differential pattern (a
Projects Agency (DARPA) of the United States Department of                                       partial difference pattern affecting only some bits) at round 3;
Defense “DARPA’s Explainable Artificial Intelligence (XAI)                                       a similar observation is made for rounds 6 and 4, leading to
Program” [227]. A more recent review of the research in                                          the authors proposing that the features learned by the neural
XAI is given in “Interpreting Black-Box Models: A Review                                         distinguisher are differential-linear in nature. Later, the trun-
on Explainable Artificial Intelligence” [228]. To this day,                                      cated differential observations from [165] were used by [42]
explainability is an active research field in AI and has resulted                                to identify good input differences for neural distinguishers
                                                                                                                                                  8



automatically.                                                                   approximations obtainable within hours on consumer hard-
    The authors further modified the convolutional neural net-                   ware.
work to use a Heaviside activation function in the first layer,                     Bao et al. developed explicit rules to be used alongside a
which binarizes the associated intermediate values, allowing                     differential distinguisher to enhance its effectiveness and more
them to analyze the linear transformation that the network                       closely match the performance of advanced neural distinguish-
learned for SPECK. Their findings demonstrate that this first                    ers [169]. The rules are based on strong correlations between
convolutional layer primarily extracts sophisticated features                    bit values in the right pairs of XOR-differential propagation
following the pattern (C1 , C2 ) = (l1 ||r1 , l2 ||r2 ) → (l1 ⊕                  through addition modulo 2n (how XOR differences behave
l2 , l1 ⊕ r1 ⊕ l2 ⊕ r2 , l1 ⊕ r1 , l2 ⊕ r2 ), where l and r represent            when processed through modular addition operations). The
left and right halves of ciphertext blocks. Further experi-                      authors also showed that those rules can be closely linked to
mentation revealed that replacing Gohr’s network’s initial 1D                    the previous studies of the multi-bit constraints and the fixed-
convolutions with a static feature extractor maintained com-                     key differential probability. Finally, the authors concluded that
parable accuracy levels, suggesting the importance of these                      leveraging the value-dependent differential probability makes
specific transformations. The researchers further revealed that                  it possible to add additional knowledge to purely differential
subsequent convolutional layers effectively learn to encode                      distinguishers. In contrast, they demonstrate that neural differ-
a compressed (generalized) representation of the differential                    ential distinguishers inherently utilize these rules. Building on
distribution table. Additionally, they demonstrated that the                     this observation, Lv et al. [194] trained a neural distinguisher
prediction head could be replaced with various alternative                       on differential-linear cryptanalysis.
ensemble classifiers without significant degradation in perfor-                     The collective research trajectory from Gohr’s initial exper-
mance, maintaining nearly identical accuracy levels.                             iments through subsequent investigations by Benamira et al.,
    Gohr et al. demonstrated that the accuracy of a (classical)                  Bellini et al., Gohr et al., and Bao et al. reveals a progressive
differential distinguisher is equivalent (up to constants) to                    refinement in understanding how neural networks operate in
the mean absolute distance between the ciphertext-difference                     cryptanalysis. This research demonstrates a clear evolution
distribution and the uniform distribution. They further estab-                   from observing that neural distinguishers for some class of
lished that for ciphers where a key-independent transformation                   ciphers exploit non-differential (key-independent) features to
can represent (intermediary) ciphertexts in the form c′ ⊕ k ′                    identifying specific differential-linear patterns they recognize,
(with k ′ being independent key bits), the encryption distri-                    and finally to formalizing these insights into explicit rules
bution and ciphertext-difference distribution contain identical                  based on bit-value correlations and value-dependent differen-
information [23]. This theoretical framework applies to major                    tial probability.
cipher classes: Substitution-Permutation Networks (SPNs, like                          b) Understanding the network architecture: In [167],
Present, which alternate substitution and permutation opera-                     Bacuieti et al. investigated the structure of the neural network
tions) and Feistel ciphers (like Simon, which split data and                     itself. In particular, the authors used the lottery ticket hypoth-
apply functions to one half) both satisfy these conditions                       esis (the idea that sparse subnetworks within larger networks
under the assumption of independent round keys (separate                         can achieve comparable performance) to prune Gohr’s neural
keys used in each encryption round)2 . Consequently, neural                      network to a minimal working version, on which they used
distinguishers for these ciphers are fundamentally limited to                    feature visualization techniques to obtain a visual representa-
learning differential features and can at best approximate                       tion of the neural network’s behavior. They additionally show
the Difference Distribution Table (DDT). This limitation was                     that, for the case of SPECK32, there is no significant accuracy
empirically confirmed: Simon’s neural distinguisher achieved                     difference between the depth 1 neural network and the depth
virtually identical accuracy to a DDT-based distinguisher, and                   10 version for Speck reduced to 7 and 8 rounds.
the Real-Difference Experiment showed Simon’s accuracy                                 c) Understanding the influence of the input data on
dropped to exactly 0.5 (random guessing level), confirming                       the distinguisher performance: Ablation studies are routinely
exclusive reliance on differential features. Speck presents a                    performed for neural networks to understand their sensitivity
contrasting case: its use of modular addition rather than XOR                    and fidelity under small perturbations on either the network
operations means it does not satisfy the theoretical constraints.                itself or its input data. Ablation studies can give insights into
Empirically, Speck’s neural distinguisher consistently outper-                   the explainability of neural network models, as detailed, for
formed purely differential approaches and maintained signifi-                    example, in “BASED-XAI: Breaking Ablation Studies Down
cant accuracy (above 0.5) in the Real-Difference Experiment,                     for Explainable Artificial Intelligence” [229], or “Logic Rule
demonstrating its ability to exploit non-differential features.                  Guided Attribution with Dynamic Ablation” [230]. In [217],
Despite these theoretical limitations, neural differential distin-               Yue et al. performed a data ablation study to observe trade-
guishers remain valuable tools for cryptanalysis. Computing                      offs between improved accuracy and overfitting when using
the DDT is computationally expensive or infeasible for large                     multiple ciphertext pairs per sample for neural differential
block sizes, while neural distinguishers provide fast, accurate                  distinguishers. Empirical evidence consistently demonstrates
                                                                                 that training on limited sample sizes significantly increases
   2 This assumption is empirically validated: The authors’ experiments across   the risk of overfitting, mostly independent of the number of
six ciphers demonstrated that key schedule algorithms (methods for generating    pairs per sample.
round keys from the main key) have negligible impact on distinguisher perfor-
mance, as replacing cipher-specific round keys with independent, identically        Seok et al. [203] investigated the use of Principal Compo-
distributed keys produced no significant accuracy changes.                       nent Analysis (PCA) and K-means clustering to define metrics
                                                                                                                                      9



for evaluating the quality of datasets in differential-neural       et al. [182] train partial neural distinguishers through extended
cryptanalysis. Their findings reveal that the datasets associated   encryption and strategic decryption with zero-set subkey bits,
with input differences leading to successful distinguishers,        and Li et al. [193] develop a sophisticated ensemble approach
which can effectively separate cipher outputs from random           combining multiple student distinguishers, each strategically
data, tend to have more axes that effectively represent the         trained on input differences producing mostly distinct infor-
data compared to other datasets. Similarly, these datasets          mative ciphertext bits.
form multiple high-density clusters compared to only a single          Deng et al. introduced the attention mechanism [8] into the
cluster in the shape of a sphere. They introduce an input dif-      differential cryptanalysis on SPECK [175]. The authors used a
ference search method based on PCA and K-means clustering           visualization algorithm to demonstrate the effectiveness of the
that surpasses the efficiency and effectiveness of the greedy       attention mechanism and further analyze the features extracted
approach proposed in [17].                                          from the ciphertext by deep learning. With this visualization
      d) Understanding the importance of bits: Recent ad-           technique, the authors evaluate which bits the attention mech-
vances in neural distinguishers [176], [178], [182], [193],         anism focuses on most, providing interpretability results.
[190], [180], [173], [19], [225], [175] have demonstrated              This extensive body of research demonstrates that neural
remarkable efficiency by operating on partial ciphertext in-        distinguishers can achieve remarkable efficiency and inter-
formation rather than complete outputs. These approaches            pretability by identifying and focusing on the most informative
have simultaneously advanced cryptographic interpretability         ciphertext bits. By systematically isolating critical bit positions
methods through systematic identification of the most influen-      through techniques like bit sensitivity testing, advantage bit
tial ciphertext bits. Chen et al. [173] introduced “Informative     search, and attention mechanisms, researchers have drastically
Bits” and Bit Sensitivity Testing, formally defining informative    reduced computational requirements for key recovery attacks
bits as ciphertext bits that effectively distinguish between a      (attacks that aim to find the secret encryption key). These
cipher and a pseudo-random permutation. They successfully           approaches not only improve attack efficiency but also provide
maintained high distinguisher performance for SPECK32/64            valuable insights into cipher vulnerabilities at the bit level,
while omitting 16 of 32 ciphertext bits through their novel         establishing a foundation for more targeted (neural) cryptanal-
testing methodology.                                                ysis.
   Hambitzer et al.’s [180] deep learning ensemble (NNBits)
provided bit-profiling capabilities specifically designed for
                                                                        VII. OVERVIEW: N EURAL A IDED K EY R ECOVERY
evaluating cryptographic (pseudo) random bit sequences. Their
                                                                                          ATTACKS
work notably contributed to explaining the accuracy ob-
tained by Gohr’s depth-1 neural distinguisher in round 6            Gohr’s work [17] marked a breakthrough in ML-based crypt-
for SPECK32/64 by providing a detailed bit-level analysis.          analysis, achieving high-accuracy neural distinguishers for
Liu et al. [190] performed a comprehensive interpretability         7-round SPECK32/64 and developing key recovery attacks
analysis exploring the relationship between neural distin-          (cryptanalytic attacks that aim to find the secret encryption
guishers, truncated differentials, and advantage bits (the most     key) for 11 and 12 rounds that rivaled or surpassed state-of-
informative bits for cryptanalysis). Their advantage bit search     the-art manual techniques.
algorithm successfully truncated ciphertexts to just 8 bits while      Since then, research has progressed in multiple directions,
leveraging XOR differences to reduce training sample size           including applying the proposed key recovery algorithm to
requirements significantly.                                         various cryptographic primitives [206], [212], [207], [217],
   Similarly, Ebrahimi et al. [176] presented a Partial Differen-   [219], [224], proposing enhancements to the original algorithm
tial (PD) ML-distinguisher for SPECK32/64, achieving nearly         [187], [173], [166], [222], [201], [181], [174], [194], exploring
identical accuracy with only 8 bits compared to full 32-bit         key recovery in alternative adversarial settings [186], [189],
distinguishers for six rounds of the cipher. Goi et al. [178]       [169], and reducing the complexity of the attack by truncating
employed explainable AI techniques (LIME and SHAP, which            the ciphertexts observed by the distinguishers [173], [182],
are model explanation methods) to examine Gohr’s neural             [193], [19], [225]. We specifically highlight (†) papers that
distinguisher, revealing significant methodological differences:    implement a (full) Bayesian attack (probabilistic key search
LIME effectively captures individual bit significance, while        methods) compared to those employing a simplified basic
SHAP uniquely identifies important bit pairings in the cipher-      attack.
text.                                                                  1) Key Recovery on Different Cryptographic Primitives:
   Seok [19] developed a specialized neural distinguisher for       While the first neural-aided key recovery was performed on
HIGHT that focuses exclusively on ciphertext bits produced          SPECK32/64, subsequent works applied the same or a sim-
by one of the two independent operations in the round func-         plified version of the attack to SPECK [224], SIMON [206],
tion, demonstrating the viability of operation-specific analysis.   [212], [224], LBC-IoT [207], SLIM [207], SPECK [217], and
Zhang et al. [225] extended neural cryptanalysis to AES-128,        PRESENT [219].
training distinguishers for the 2-round reduced cipher and             Zhang et al. [224]† achieved significant breakthroughs in
additionally examining specific intermediate states between         differential-neural cryptanalysis by performing key recovery
rounds 2 and 3. Their approach replaced full 16-byte state          attacks on 13- and 14-round SPECK32/64, with the 14-
processing with specialized networks operating on just 2-byte       round attack exhaustively searching through the final round’s
segments while maintaining nearly identical accuracy. Huang         subkey. They also executed the first 17-round key recovery
                                                                                                                                    10



attack on SIMON32/64. Building upon Gohr’s foundational              neutral bits, and a Bayesian algorithm in the lines of [17],
work [17], the authors implemented knowledge distillation (a         their method reduces both computational and data complexity
technique to create smaller, efficient neural networks from          compared to the original key recovery in [17].
larger ones) to create dramatically smaller student networks            Bao et al. introduced generalized neutral bits techniques
featuring fixed-size convolutions and GlobalAveragePooling           and conditional neural differential cryptanalysis [166]† . They
layers. These streamlined architectures substantially reduced        improved the success rate of deep learning-assisted key re-
computational demands during key recovery while maintaining          covery attacks by considering neural distinguisher accuracies,
attack effectiveness.                                                round numbers, and classical differential paths spliced in front
   Tian and Hu [206] developed 7-9 round neural distinguish-         of neural distinguishers. They also explored data complexity
ers for SIMON32/64 and achieved 15-round key recovery us-            aspects and achieved successful key recovery attacks on 13-
ing a prepended differential, which is a probabilistic transition    round SPECK32/64 and 16-round SIMON32/64.
from an input difference to an output difference, combined              In [222]† , the authors improved SIMECK-32 attacks, en-
with probabilistic neutral bits that represent specific bit po-      hancing the 15-round attack and launching the first practical
sitions that can be varied without affecting the differential        16- and 17-round key recovery attacks for SIMECK32/64.
pattern, followed by an exhaustive subkey search.                    They extended their 12-round neural distinguisher with a 3-
   Teng et al. [207] demonstrated practical 8-round key re-          round differential and associated 14 deterministic NBs (neutral
covery attacks on LBC-IoT using their 6-round neural distin-         bits with deterministic behavior) and 2 SNBSs (sets of neu-
guisher.                                                             tral bits that can be simultaneously complemented) identified
   Wu et al. [212]† introduced a mixed-neural differential           through exhaustive search.
network for 12-round SIMON32/64 key recovery, achieving                 In [201]† , the authors implemented full key recovery on
higher accuracy with increased complexity.                           Simon32/64 using a distinguisher trained for polytopic dif-
   Yue and Wu [217] improved upon Gohr’s work with a                 ferences (differences with multiple possible patterns). Unlike
novel data format exploiting SPECK32/64’s round function             Gohr’s attack [17], their approach doesn’t rely on neutral bits
structure, enabling 8-round key recovery.                            but instead filters (r + 1)-round ciphertext pairs conforming
   Zhu et al. [219] successfully executed an 8-round key             to the initial differential using an (r + 1)-round neural distin-
recovery attack on PRESENT by extracting non-linear S-               guisher, selecting pairs producing the highest scores.
box features (characteristics of the cipher’s substitution boxes,       Hou et al. in [181]† leveraged key response profile peri-
which are key nonlinear components) using randomly gener-            odicity (repeating patterns in how keys behave) to achieve
ated subkeys, demonstrating that neural networks trained on          key recovery using only a partial profile. This approach is
ciphertext differences substantially outperform those trained        particularly necessary for block ciphers with round key sizes
on raw ciphertext pairs for distinguishing and key recovery          significantly larger than 16 bits, such as SIMON64/128,
tasks.                                                               ensuring feasible key response profile generation.
   2) Advancements of the Key Recovery: Several studies                 In [174], the authors proposed a data reuse strategy for
aimed to advance neural-aided key recovery by focusing on            distinguishers processing input sets of n > 2 ciphertext pairs.
parameter selection [187], [173], [166], exploring variants of       Their approach generates a large ciphertext set and forms
neutral bits in the prepended classical differential [166], [222],   subsets where each ciphertext pair appears in a limited number
[201], and reducing data complexity (the amount of encrypted         of subsets while maintaining sufficient distinction between
data needed for the attack) through precomputation [181],            subsets. Using this strategy, they applied neural distinguish-
[194] and reducing encryption queries [174].                         ers to perform 10-rounds and 11-rounds key recovery on
   Lyu et al. exhaustively explored neural distinguishers            Speck32/64 using NASA [173] and Bayesian Key Recovery,
for Bayesian key search and applied them to                          respectively.
SIMECK32/64 [187]† . They obtained 8/9/10-round neural                  Lv et al. [194]† used super-neutral bits (enhanced neutral
differential distinguishers and recovered penultimate and last       bits with stronger properties) to decrease attack data complex-
round subkeys for 13/14/15-round SIMECK32/64 with low                ity and a lookup table strategy to eliminate real-time neural
data and time complexity. Their findings revealed that key           distinguisher invocations, performing a practical 13-round key
response profile regularity, which measures how consistently         recovery on Speck using their novel differential-linear neural
a neural distinguisher’s output changes when decrypting              distinguishers.
with systematically varied incorrect keys, plays a crucial              3) Bit-Level Ciphertext Analysis: Recent work on neural
role and varies greatly among distinguishers, as does the            distinguishers [173], [182], [193], [19], [225] offers promising
number of neutral bits available for the distinguisher’s             approaches for reducing both computational and data require-
prepended differential. Interestingly, the most accurate neural      ments in key recovery attacks. These distinguishers can operate
distinguisher did not necessarily achieve the best key recovery      on partial ciphertext bits, suggesting that complete decryption
performance.                                                         may not be necessary for successful key recovery. For detailed
   Chen et al. proposed a Neural-Aided Statistical Attack            explanations of approaches involving distinguishers on partial
(NASA) with experiments on reduced-round SPECK32/64,                 ciphertexts, see section VI on interpretability. Here, we focus
DES, and Speck96/96 [173]† . Their theoretical estimates             specifically on key recovery applications.
suggest breaking 10-round DES, surpassing Gohr’s 8-round                Chen et al. [173]† trained student distinguishers (smaller,
attack. When combined with a novel early stopping technique,         specialized neural networks) using only subsets of ciphertext
                                                                                                                                   11



bits for DES and SPECK while maintaining high accuracy.             classical cryptanalysis, this approach has extended key recov-
For SPECK32/64, they omitted 6 of the 32 ciphertext bits,           ery attacks in the related-key setting for SPECK [169] and in
identified through their novel Bit Sensitivity Test. These          conditional and related-key settings for KATAN [186], [189].
optimized distinguishers enabled subkey recovery in smaller           Lin et al. demonstrated practical key recovery attacks on
subspaces (reduced search spaces for key bits), reducing attack     KATAN ciphers [186]† by combining conditional and related-
complexity. The authors demonstrated a practical attack on          key differential cryptanalysis. They successfully attacked
SPECK32/64 and provided theoretical estimates for attacking         125-round KATAN32, 106-round KATAN48, and 95-round
10-round DES and 14-round Speck96/96.                               KATAN64, while proposing parallelization of the Wrong Key
   Li et al. [193] extended this work by developing an              Response Profile (a measure of how incorrect key guesses
ensemble of student distinguishers, each trained on distinct        behave) calculation to enhance efficiency.
input differences and ciphertext bit combinations. Their key
insight revealed that varying input differences cause different        In subsequent work, Lin et al. developed attacks target-
ciphertext bits to become critical for distinction, affecting       ing 97-round KATAN32, 82-round KATAN48, and 70-round
relevant key bits. Through their novel key sensitivity test, they   KATAN64 [189]† . Their method integrates neural distinguish-
partitioned the subkey space into independently solvable com-       ers with conditional prepended differentials that constrain spe-
ponents, enabling practical key recovery against previously         cific plaintext and key bits. By identifying optimal conditions
resistant large-state block ciphers: 18-round SIMON128, 14-         and neutral bit sets, they improved the attack effectiveness.
round SIMON96, 14-round SIMON64, 12-round SPECK128,                    Bao et al. [169] successfully executed a 14-round key
10-round SPECK96, and 9-round SPECK64.                              recovery attack on SPECK32/64 in the related-key setting.
   Huang et al. [182] introduce a novel neural differential
cryptanalysis framework that substantially mitigates compu-            5) Limitations of Hybrid Distinguisher Models for Key
tational complexity in large-state block cipher key recov-          Recovery: Recent works [216], [214], [213] have explored
ery. By implementing a parallelizable multi-stage approach          hybrid approaches combining classical differential transitions
with strategically trained neural distinguishers, the researchers   with neural distinguishers. Rather than optimizing standalone
demonstrate improvements in attacking SPECK. The proposed           s-round neural distinguishers, these models are constrained
methodology leverages partial neural distinguishers (PNDs,          to input differences matching the output difference of a
networks trained on subsets of the cipher state) executed           classical r-round differential transition. This hybridization
in parallel, followed by a full neural distinguisher (FND)          aims to achieve near-perfect distinction for (r + s)-encrypted
for key selection. The partial distinguishers are trained to        ciphertexts with minimal data complexity.
recover independent key bits through an innovative whitening           A significant limitation of these hybrid approaches stems
key decryption technique (a method to isolate specific key          from their dependence on extended classical differential paths.
bits during analysis). Experimental validation on 10-round          This dependence precludes the use of neutral bits, making it
SPECK64 and 10-round SPECK96 reveals computational ef-              impossible to construct the plaintext structures (see section IV)
ficiency gains. Their SPECK64 attack employed a customized          necessary for key recovery methods like those in [17]. While
ResNet architecture using multiple ciphertext pairs generated       some studies, including [216], have claimed breakthrough
via neutral bits and an advanced staged training protocol.          results in key recovery, these claims lack experimental val-
   Seok et al. [19] attempted partial key recovery in the final     idation.
transformation of 15-round HIGHT, claiming to recover por-            In a different approach, Yadav et al. [218] constructed
tions of the last round key. However, their analysis relied on an   high-accuracy neural distinguishers from low-accuracy ones
assumed differential characteristic with probability 2−31 with-     without prepending classical differentials, though at the cost
out addressing practical implementation details, particularly       of increased data complexity.
regarding the use of this prepended differential characteristic
without neutral bits. While they theorized about a divide-and-
conquer strategy, the proposal lacked concrete implementation
details.
   Zhang et al. [225] developed neural distinguishers targeting
                                                                      VIII. C OMPARATIVE R EVIEW: N EURAL D IFFERENTIAL
a 2-round reduced version of AES-128, specifically analyzing
                                                                                      D ISTINGUISHERS
pairs of bytes from the ciphertext. These byte-wise distinguish-
ers were leveraged to mount key recovery attacks on 3-round
AES-128 using a divide-and-conquer strategy where different
key segments were recovered independently.                          In the following, we provide a comparative review of all
   4) Key Recovery for Related-Key and Conditional Adver-           trained neural differential distinguishers as of February 2025.
saries: Conditional and related-key differential cryptanalysis      First, all investigated neural network architectures are re-
enhances adversarial capabilities by slowing the diffusion of       viewed (subsection VIII-A), then we detail the classification
differences, enabling attacks on additional rounds of ciphers.      scheme (subsection VIII-B) and conclude with a comparative
Related-key attacks assume the attacker can observe encryp-         review of the best neural differential distinguishers for each
tion under multiple related keys, while conditional attacks         symmetric primitive (subsection VIII-C), followed by a dis-
constrain specific plaintext or key bits. Following trends in       cussion of the review (subsection VIII-D).
                                                                                                                                               12



A. Architectures                                                                  layers as reusable feature extractors while updating only the
                                                                             3    classification layers for new rounds [169].
In this section, we review the neural network architectures
                                                                                        d) MLP: MLP (Multi-Layer Perceptron) employs
employed in Neural Differential Cryptanalysis.
                                                                                  densely connected layers where each neuron connects to all
   1) Core Architectures:                                                         neurons in subsequent layers. Due to their computational effi-
      a) N DGohr : N DGohr is the foundational neural net-                        ciency, MLPs have been investigated on 11 of 24 primitives.
work architecture introduced by Gohr [17]. The architecture                          Other classical machine learning methods (AdaBoost, Ran-
consists of four key components: (1) input reshaping that mir-                    dom Forest, Decision Trees) generally achieve accuracy rates
rors the cipher’s word-oriented structure, (2) a single bit-sliced                at least 20% lower than CNNs [221]. Classical ML methods
convolution enabling effective learning of XOR relationships                      like SVM are occasionally competitive and included when
between components [165], (3) a residual convolutional tower                      relevant [168].
of varying depths (commonly depth-1, 5, or 10), and (4) a                               e) SE-Networks: SENet (Squeeze-and-Excitation Net-
fully connected prediction head. The bit-sliced convolution is                    work) introduces attention mechanisms that adaptively recali-
particularly crucial, as other architectures struggle without di-                 brate channel-wise feature responses [166]. The core squeeze-
rect XOR inputs [22], [179], [216]. Initially requiring elaborate                 and-excitation blocks perform: (1) squeeze operations using
staged training for 8-round SPECK (Table III) distinguishers,                     global average pooling to create channel descriptors, (2) exci-
subsequent work demonstrated that freezing all layers except                      tation operations with fully connected layers learning channel
the prediction head enables rapid training [169]. N DGohr has                     dependencies, and (3) scale operations multiplying features by
been applied to the majority (14/24) of primitives and serves                     attention weights. This enables focus on discriminative crypto-
as the baseline for most cryptanalytic applications.                              graphic features with minimal overhead, proving particularly
   Several variants extend the original design: N Dpruned  Gohr                   effective for longer encryption rounds on SIMECK (Table II)
reduces model complexity for SPECK (Table III) [167];                             and SIMON (Table I).
  N Dattntn.
       Gohr     adds attention mechanisms to SPECK (Ta-                              SE-ResNet combines ResNet’s residual connections with
ble III) [175]; N Densmbl.
                       Gohr    combines multiple networks for                     SENet’s attention mechanism, leveraging both gradient flow
enhanced explainability on SPECK (Table III) [180]; and                           improvement and adaptive feature recalibration [192]. Applied
N Dsep.conv.
     Gohr      employs separable convolutions to reduce train-                    to SIMON (Table I) and SIMECK (Table II), this hybrid
ing costs for SPECK (Table III) [190].                                            approach demonstrates the effectiveness of combining com-
      b) DBitNet: DBitNet was designed as a “cipher-                              plementary architectural innovations.
agnostic” alternative to N DGohr [42]. Built on dilated con-                         2) Additional Architectures:
volutional layers that learn dependencies between distant                               a) LSTM and Transformer: LSTM s (Long Short-Term
rather than neighboring neurons, DBitNet eliminates the need                      Memory) process sequential data using memory cells to cap-
for input reshaping and bit-slicing convolution. This design                      ture long-term dependencies in cryptographic patterns. Ap-
enables automatic distinguisher generation across multiple                        plied to GIMLI (Table XI), TinyJAMBU (Table XXIV), and
primitives while achieving comparable accuracy to Gohr’s                          GIFT (Table X) [22], [21], LSTMs treat ciphertext pairs as
method through simple staged training. The architecture                           sequential data. Transformer architectures, based on atten-
successfully generated distinguishers for eight primitives:                       tion mechanisms, process ciphertext pairs through encoder
SPECK (Table III), SIMON (Table I), HIGHT (Table XIII),                           networks with positional encoding. Both architectures have
PRESENT (Table XVIII), GIMLI (Table XI), KATAN (Ta-                               been applied to LEA (Table XVII), PRESENT (Table XVIII),
ble XIV), TEA (Table XXIII), and LEA (Table XVII).                                and HIGHT (Table XIII), offering alternative approaches to
      c) Inception: The INC architecture incorporates                             traditional convolutional methods [172].
GoogLeNet’s Inception modules, which process inputs through                             b) UNet: UNet employs an encoding-decoding architec-
multiple parallel convolutional layers with various kernel sizes.                 ture typically used for image segmentation. The encoder com-
This parallel processing enables feature extraction capabilities                  presses input features while the decoder reconstructs relevant
that single kernel sizes cannot achieve, though at increased                      patterns, connected by skip connections that preserve spatial
computational cost [23]. First proposed in [224], INC has                         information. Applied to GIFT (Table X) and PRESENT (Ta-
been applied to SIMECK (Table II), PRESENT (Table XVIII),                         ble XVIII) [219], UNet offers a different perspective on fea-
CHASKEY (Table VII), DES (Table VIII), SIMON (Table I),                           ture extraction by explicitly modeling the encoding-decoding
and SPECK (Table III). A variant (INCfreeze ) employs staged                      process inherent in cryptographic analysis.
training with partially frozen networks, treating convolutional                         c) Quantum Neural Networks: Quantum Neural Net-
                                                                                  works leverage quantum computing principles, including su-
    3 We introduce key vocabulary for Neural Differential Cryptanalysis archi-    perposition (qubits existing in multiple states simultaneously)
tectures: MLPs use densely connected layers with full connectivity between        and entanglement (correlated qubit interactions). Unlike clas-
neurons, resulting in many parameters. Convolutional layers (CNNs) apply          sical networks processing binary information, quantum net-
filters to detect spatial patterns, requiring more computation but better cap-
turing hierarchical features. Inception modules combine parallel convolutions     works can theoretically explore multiple solution paths si-
with various kernel sizes for enhanced feature extraction. Residual connections   multaneously. The first simulated quantum neural network
(RESNets) create bypass paths to improve information flow during training.        distinguisher was demonstrated on SPECK (Table III) [184],
LSTM (a type of RNN) processes sequential data using memory cells to
capture long-term dependencies. Attention mechanisms dynamically focus on         though practical quantum implementations remain limited by
relevant input portions, forming the basis of transformer networks.               current hardware constraints.
                                                                                                                                  13



     d) DenseNet: DenseNet implements dense connectivity               From a statistical perspective, using multiple independent
where each layer receives inputs from all preceding layers          samples to classify between two distributions is fundamen-
through concatenation: xℓ = Hℓ ([x0 , x1 , . . . , xℓ−1 ]). Orga-   tal to hypothesis testing theory. When observing samples
nized into dense blocks connected by transition layers (1 × 1       X1 , X2 , . . . , Xn from either distribution f0 (null hypothe-
convolutions and average pooling), the architecture employs a       sis) orQ f1 (alternative hypothesis), the likelihood ratio test
growth rate parameter k controlling feature map production.         Λ = i f1 (Xi )/f0 (Xi ) provides optimal classification. Per-
This design enables extensive feature reuse and improved            formance improves exponentially with sample size n, as both
gradient flow, which is beneficial for capturing multi-level        Type I and Type II error probabilities decay exponentially
cryptographic patterns. Applied to SPECK-32 (Table III),            when distributions differ, a classical result established by
DenseNet showed marginal improvements over ResNet for               Neyman and Pearson (1933).
shorter rounds but struggled with complex 8-round encryp-              Instead of combining prediction scores using systematic
tion [202]. While investigated in [166], it was surpassed by        formulas, Shen et al. [204] replaced traditional score ag-
SENet for longer rounds and therefore does not appear in the        gregation with multilayer perceptrons (MLPs) that directly
following compilation of best neural distinguishers.                classify from multiple pair scores. Further, researchers have
                                                                    moved beyond post-hoc score combination to architectures
                                                                    that process multiple ciphertext pairs jointly during inference.
B. Classification Scheme n-m-T -E for Neural Distinguishers         This approach was pioneered by Benamira et al. [165], whose
The proliferation of diverse training configurations for neural     distinguisher directly accepted multiple pairs as input, and has
distinguishers often complicates the comparison of results          since been adopted across numerous subsequent works.
across studies. Bellini et al. [42] addressed this challenge by        The benefits of combining multiple pairs during inference
proposing a systematic classification framework based on four       remain contentious. While joint processing could, in theory,
key parameters: n, m, T , and E. We adopt this classifica-          allow neural distinguishers to exploit key schedule biases
tion scheme throughout our review due to its demonstrated           or plaintext correlation patterns, empirical evidence suggests
robustness in organizing the extensive cryptographic literature,    limited advantages.
extending it with additional taxonomic symbols to enable               Key schedule influence appears minimal, as Gohr et al. [23]
more nuanced categorization. We note that [42] is a technical       showed that replacing round keys with uniform random values
contribution paper focused on developing automated neural           negligibly affects distinguishing accuracy. Similarly, Chen et
cryptanalysis tools, not a survey paper, and makes no claims        al. [174] explored two critical scenarios: samples where all
regarding a systematic or comprehensive collection of research      pairs of a multi-pair distinguisher share the same encryption
literature.                                                         key versus samples with independent keys per pair. Key reuse
   To illustrate this framework, consider Gohr’s foundational       patterns showed minimal impact on distinguisher performance,
approach, which exemplifies the 2-1-CT-R configuration: the         suggesting neural networks learn features independent of key
distinguisher processes pairs of ciphertexts (n = 2), considers     correlations.
only a single input difference (m = 1), receives raw ciphertext        In general, multi-pair architectures historically show min-
pairs without preprocessing (T = CT), and performs binary           imal practical gains over classical score aggregation [23],
classification to detect the usage of the input difference (E =     [174], while increasing computational costs by processing x-
R).                                                                 fold more bits. Further, Zhang et al. [223] identified critical
                                                                    training trade-offs when using more samples. Comparing fixed
   Parameter Overview of n-m-T -E Classification                    total pairs (107 ) versus fixed multi-pair samples revealed that
                                                                    maintaining pair count led to overfitting, validation fluctua-
      • n: Number of ciphertexts per training sample                tions, and slow convergence due to reduced sample diversity.
      • m: Number of input differences per training sample          This finding, confirmed by Zhang et al. [224], emphasizes that
      • T : Feature engineering on training sample                  the number of samples has to be significantly increased for the
      • E: Type of distinguishing experiment performed              training of multi-pair distinguishers.
                                                                       2) Number of Input Differences: m: Traditional differential
   1) Number of Ciphertexts per Sample: n: This section             cryptanalysis focuses on single input differences, but advanced
focuses on multiple samples (n > 2) for a single input              approaches can leverage multiple differences simultaneously,
difference (m = 1). The next section examines multiple input        as formalized in multiple differential cryptanalysis [231]. It
differences (m > 1).                                                has been shown that multiple differential cryptanalysis, which
The foundational work by Gohr [17] already demonstrated             simultaneously exploits differentials with different input dif-
that, using multiple independent ciphertext pairs (generated        ferences, reduces data complexity by approximately a factor
from the same input difference δ), predictions from a single-       of |∆0 | compared to single-difference attacks, where |∆0 |
pair distinguishers could be effectively combined during key        represents the number of distinct input differences used. Blon-
recovery, amplifying signal strength and improving classifi-        deau and Gérard’s theoretical framework demonstrates that
cation accuracy. This score aggregation approach was later          combining multiple differential paths extracts more statistical
formalized by Gohr et al. [23], who noted its rediscovery           information per sample, enabling practical improvements such
across multiple studies and proposed systematic combining           as extending differential attacks on PRESENT from 16 to 18
formulas.                                                           rounds while maintaining reasonable data requirements.
                                                                                                                                        14



   Mirroring this trend in Neural Differential Cryptanalysis, re-       For Partial Decryption With Key Assumption, Yue et
                                                                                                               ′
cent advances in neural differential cryptanalysis have system-      al. [217] developed the format (Rr−1 , Rr−1    , dl , C0 , C1 ) where
atically explored multiple input difference techniques across        dl estimates the left-half difference at round r − 1 through
various approaches and primitives. Baksi et al. [22] demon-          ((Lr ⊟ Rr−1 ) ⊕ (L′r ⊟ Rr−1
                                                                                               ′
                                                                                                   )), equivalent to partial decryption
strated the effectiveness of multi-difference settings with m =      with a null key. Lu et al. [192] extended this by incorporating
2 across permutations including KNOT, ASCON, CHASKEY,                two-round prior information using subkey 0 for partial decryp-
and GIMLI, while two works ([201], [21]) adapted polytopic           tion, an approach also used in [215], [222]. The MRMSD/M-
cryptanalysis to develop neural differential networks that main-     RMSP Approaches by Liu et al. [191] introduced MRMSD
tain a fixed plaintext anchor while using multiple differences       (Multiple Rounds Multiple Splicing Differences), combining
(P, P ⊕ δ0 , P ⊕ δ1 , . . .) to generate k differential pairs from   output differences with estimated previous-round differences
k + 1 plaintexts. Similarly, Wu et al. [212] explored the            using random-key partial decryption, and MRMSP (Multi-
combination of mixture differential techniques and machine           ple Rounds Multiple Splicing Pairs), providing correspond-
learning. In [211], the authors investigated two variations of       ing ciphertext pairs instead of differences. Finally, Zhu et
a multiple-input differences scenario, where the samples are         al. [219] modified traditional approaches by performing partial
the concatenations of pairs with differences δi . In NDrm , a        encryption to intermediate round states, targeting input/output
sample is the concatenation of a pair of ciphertexts for each        relationships of substitution box operations to extract nonlinear
difference (resulting in n = 2m); in NDam , the first ciphertext     transformation features.
is the encryption of a random plaintext P0 , each subsequent
ciphertext Ci is the encryption of Pi−1 ⊕ ∆i−1 so that                  Feature Engeneering T Overview
n = m + 1. Multiple works ([215], [22], [168], [199], [210])
trained neural distinguishers to differentiate between different           • CT: Unprocessed ciphertext pair handed to N D
output difference distributions (see subsubsection VIII-B4).               • δ: Ciphertext XOR handed to N D
                                                                           • δtr : Reduced-bit XOR differences handed to N D
   3) Feature Engineering Type: T :
                                                                           • A: Advanced processing, such as partial decryption
      a) Raw Ciphertext Processing (T = CT): The most
straightforward feature engineering type passes the raw ci-
phertext pairs directly to the neural distinguisher. While this         4) Type of Distinguishing Experiment: E:
preserves maximum information content, it requires networks                a) Standard Differential Detection (E = R):
to learn differential patterns implicitly, potentially increasing    Gohr’s [17] foundational experiment uses samples of the form
training and architectural complexity [165].                         EK (P0 )∥EK (P0 ⊕ x) where the network determines whether
      b) XOR Difference Features (T = δ): Multiple works,            x equals a target difference δ. This binary classification task
such as Baksi et al. [22], Hou et al. [179], Yadav et al. [216],     directly mirrors classical differential cryptanalysis objectives.
have demonstrated that replacing ciphertext pairs with their               b) Real Ciphertext Masking (E = RM ): Gohr’s [17]
XOR differences can speed up training while maintaining              “real ciphertext” experiment creates samples EK (P0 ) ⊕
comparable performance. This transformation reduces input            x∥EK (P0 ⊕ δ) ⊕ x where the network identifies whether
dimensionality and provides a more direct representation of          x = 0 (unmasked) or x is random (masked). Success in
differential characteristics.                                        this experiment demonstrates that neural distinguishers learn
   Truncated Variants (T = CTtr /δtr ): Huang et al. [182]           information beyond simple XOR differences, capturing more
and Yhang et al. [225] reduced training requirements by trun-        subtle structural patterns.
cating ciphertexts to a few bits before handing them to the dis-           c) Alternative Difference Operations (E = R+ ):
tinguisher, significantly decreasing sample size requirements        Modular Addition Differences: Bellini et al. [20] adapted
at the cost of information loss. Liu et al. [190], Ebrahimi et       the framework for ciphers using modular addition (TEA,
al. [176], and Seok [19] further reduced training requirements       RAIDEN) by replacing XOR with modular addition differ-
by truncating ciphertexts to a few bits before computing XOR         ences, demonstrating the framework’s flexibility across differ-
differences, decreasing sample size requirements at the cost of      ent algebraic structures.
information loss.                                                       Rotational-XOR Differences: Ebrahimi et al. [177] ex-
   Advanced Variants (T = A): In [170], the authors append           plored rotational-XOR differences rather than standard XOR
the individual ciphertext pairs and the ciphertext difference.       operations, targeting ciphers with rotational components.
   For Partial Decryption Without Key Knowledge, re-                       d) Multi-Difference Classification (E = D): Several
searchers demonstrated that XORing cipher halves and ap-             works, including Baksi et al.’s [22], including Baksi et
plying rotation operations reveals structural information that       al.’s [22], Wang et al.’s [210], and Wang et al.’s [214],
improves distinguisher accuracy for SPECK32 [165], [182],            transform the binary classification problem into multi-class
[224], with similar feature engineering applied to SIMON-            classification. Samples are formed as (EK (P ), EK (P ⊕ δi ))
like ciphers by Bao et al. [166]. However, Gohr et al. [23]          for i ∈ [0, m − 1], with the network identifying which specific
showed that neural distinguishers can learn these feature trans-     difference i was used. This approach enables simultaneous
forms automatically when provided with raw ciphertext pairs,         analysis of multiple differential characteristics.
though this requires extensive hyperparameter optimization,                e) Differential-Linear Hybrid Approaches (E = DL)):
demonstrating how the cipher structure influences the optimal        Lv et al. [194] developed a hybrid methodology that com-
architecture choice of the neural distinguisher.                     bines differential and linear (neural) cryptanalysis. For each
                                                                                                                                                    15



ciphertext pair (c, c′ ), they apply N distinct output masks              list of primitives analyzed to date is as follows: AES (Ta-
(Γ1 , Γ′1 ), . . . , (ΓN , Γ′N ) to generate N -bit input vectors where   ble IV), ARADI (Table V), ASCON (Table VI), CHASKEY
each bit computes xi = Γi · C1 ⊕ Γ̃i · C2 . This approach                 (Table VII), DES (Table VIII), FF (Table IX), GIFT (Ta-
effectively implements differential-linear cryptanalysis within           ble X), GIMLI (Table XI), GOST (Table XII), HIGHT (Ta-
the neural framework, leveraging both differential properties             ble XIII), KATAN (Table XIV), KNOT (Table XV), LBCIoT
and linear approximations.                                                (Table XVI), LEA (Table XVII), PRESENT (Table XVIII),
                                                                          PRIDE (Table XIX), SHA3 (Table XX), SIMECK (Table II),
   Experiment Type E Overview                                             SIMON (Table I), SKINNY (Table XXI), SLIM (Table XXII),
                                                                          SPECK (Table III), TEA and XTEA (Table XXIII), and
                                                    ?
      • R: EK (P )∥EK (P ⊕ x), Classify x = δ                             TinyJAMBU (Table XXIV).
                                                         ?                   In addition, Bose et al. claimed statistically significant
      • RM : EK (P0 )⊕x∥EK (P0 ⊕δ)⊕x, Classify x = 0
         +                                       ?                        distinguishers for 6-round SPARX and 8-round PICCOLO-80.
      • R : EK (P )∥EK (P ⊛ x), Classify x = δ, where
                                                                          As theirs is the only work targeting these ciphers and their
        ⊛ ∈ {⊞, ≫}
                                                                          reported improvements for other ciphers challenge fundamen-
      • D: (EK (P )∥EK (P ⊕ δi )), Identify i ∈ [0, m − 1]
                                                                          tal cryptographic principles, we omitted dedicated tables that
      • DL: EK (P )∥EK (P ⊕x), Extract b = b1 ∥ · · · ∥bN
                                                        ?                 would lack contextual comparison. Instead, we included their
        where bi = Γi · C0 ⊕ Γ̄i · C1 , then classify x = δ               distinguishers for LEA, PRESENT, and HIGHT with a critical
                                                                          discussion.
                                                                             1) SIMON: SIMON is a family of AND-RX block ciphers,
This classification framework provides a systematic founda-               denoted SIMON-B/K, that encrypt blocks of size B with a key
tion for comparing neural distinguisher approaches across the             of size K. SIMON-32/64, SIMON-48/96, SIMON-64/128, and
literature. The parameter space defined by n-m-T -E enables               SIMON-128/256 have 32, 36, 44, and 72 rounds, respectively.
researchers to precisely characterize their methodologies and             Neural differential distinguishers have been developed for all
identify gaps for future exploration.                                     versions of SIMON.
                                                                             Table I provides an overview of the differential neural dis-
                                                                          tinguishers developed for the SIMON family of block ciphers.
C. Comparative Review
                                                                          The most extensively studied variant is SIMON-32, with var-
Based on the whole body of research in Neural Differ-                     ious neural network architectures and settings explored across
ential Cryptanalysis (subsection V-A), this section provides              multiple works. In the standard setting ( 2-1-CT-R ), the best
a comparative review of all best published neural distin-                 distinguisher achieves round 11 through an automated pipeline
guishers, classified according to the previously introduced               and a generic, convolutional architecture [42]. In general,
scheme, together with their neural network architecture (sub-             convolutional architectures consistently achieve the highest
section VIII-A).                                                          accuracy among the neural network distinguishers obtained for
   The neural differential distinguishers of each publication             SIMON. By using multiple ciphertext pairs (n = 16, 32, 64)
were selected as follows: i) We present the best result of each           and employing advanced feature engineering techniques, as
work, either the standard setting (2-1-CT-R or 2-1-δ-R) or                in [191], [192], [224], the distinguisher performance surpasses
an alternative setting (n-m-T -E). If, additionally, a result in          this result, extending the analysis to round 12 [192]. Similarly,
the standard setting is given, we will also present it. ii) In            switching to the related-key setting, distinguishers can be
most works, no error margins on the results are provided,                 trained for 13 rounds, as in [192]. The classification task
preventing us from displaying them. Ideally, the accuracies               becomes significantly easier when distinguishing between two
shown should be test accuracies on sets of several fresh sam-             ciphertext distributions rather than distinguishing a single
ples. However, in many works, only the validation accuracy is             distribution from uniform4 . This approach yields substantially
reported. iii) Note that from a machine learning and statistical          higher accuracies in the related-key setting and enables attacks
perspective, the number of training and validation samples is             on one additional round using just a single ciphertext pair in
very important. However, from a cryptographic perspective,                the standard setting [215].
the number of needed encryptions, i.e., ciphertexts, is more                 For the case of SIMON, some authors experimented with
relevant. Accordingly, the numbers reported in the following              a vast amount of data: [179] used k · 107 for k = 32, 48, 64
under Trn. (training data) and Val. (validation data) are the             (maximum of 640M) samples for training, and [166] obtained
number of ciphertexts.                                                    an 11-round distinguisher for SIMON32 at the cost of staged
   To date, neural distinguishers have been applied to analyze            trained in four steps, with respectively 107 , 228 , 2·230 (2426M
24 symmetric primitives. This comparative review provides a               pairs). In [42], the authors proposed a polishing step, retraining
foundation for integrating new research into the existing body            a neural distinguisher initially trained with 107 pairs with an
of work. While comprehensive tables compiling these analyses              additional 109 pairs: 107 , 109 (1010M pairs). This polishing
are provided in the appendices, we focus here on the most                 step was also used by Wang et al. [214]. Similarly, Zhang
extensively studied primitives where distinguishers have been             et al. [224] used a staged training approach: 4 · 107 samples,
developed by 9 or more works (namely SIMECK, SIMON, and                      4 This approach is aimed to maximize the average absolute distance between
SPECK), as only these provide sufficient data for meaningful              two ciphertext distributions, a key metric for distinguisher performance, as
comparative analysis of optimal approaches. The complete                  established by Gohr [23]
                                                                                                                                                     16



                                                                  TABLE I
                                     OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR SIMON.

   Primitive                     Arch.             Class               Trn.          Val.        AutoND          Rounds        Acc.          Ref.
   SIMON-32/64                   N DGohr           2-1-A-R             20M           2M             -            8             0.834         [165]
                                 N DGohr           2-1-CT-R            20M           2M             -            9             0.5907        [179]
                                 N DGohr           2-1-CT-R            20M           2M             -            9             0.6277        [201]
                                 N DGohr           2-1-CT-R            /             /              -            9             0.6320        [206]†
                                 N DGohr           4-3-CT-R            40M           4M             -            9             0.6373        [201]
                                 N DGohr           4-3-CT-R            40M           4M             -            8             0.923         [212]
                                 N DGohr           64-1-δ-R            640M          6.4M           -            10            0.6109        [179]
                                 SENet             2-1-A-R             4852M         537M           -            11            0.517         [166]
                                 DBitNet           2-1-CT-R            2020M         2M            ✓             11            0.518         [42]
                                 N DGohr           64-1-A-R            640M          64M            -            11            0.6081        [191]
                                 DenseNet          2-2-CT-D            2020M         2M            ✓             12            0.505         [214]
                                 SE-ResNet         16-1-A-R            320M          32M            -            12            0.5152        [192]
                                 INC               32-1-A-R            1280M         2M             -            12            0.5218        [224]
   SIMON-32/64RK                 N DGohr           2-1-CT-R+           20M           2M             -            11            0.5445        [177]
                                 SE-ResNet         16-1-A-R            320M          32M            -            13            0.5262        [192]
                                 SE-ResNet         16-2-A-D            320M          32M           ✓             13            0.567         [215]
   SIMON-48/96                   N DGohr           2-1-CT-R            20M           2M             -            10            0.5789        [179]
                                 N DGohr           96-1-δ-R            960M          9.6M           -            11            0.6143        [179]
                                 DenseNet          2-2-CT-D            20M           2M            ✓             12            0.515         [214]
                                 N DGohr           96-1-A-R            960M          96M            -            12            0.6159        [191]
   SIMON-48/96RK                 SE-ResNet         16-2-A-D            320M          32M           ✓             13            0.696         [215]
   SIMON-64/128                  N DGohr           2-1-CT-R            20M           2M             -            11            0.5972        [179]
                                 N DGohr           128-1-δ-R           1280M         12.8M          -            12            0.6957        [179]
                                 DBitNet           2-1-CT-R            20M           2M            ✓             13            0.518         [42]
                                 N DGohr           128-1-A-R           1280M         128M           -            13            0.701         [191]
                                 DenseNet          2-2-CT-D            20M           2M            ✓             14            0.506         [214]
                                 SE-ResNet         16-1-A-R            1394M         134M           -            14            0.5185        [192]
   SIMON-64/128RK                N DGohr           2-1-CT-R+           20M           2M             -            13            0.5151        [177]
                                 SE-ResNet         16-1-A-R            320M          32M            -            14            0.5788        [192]
                                 SE-ResNet         16-2-A-D            320M          32M           ✓             14            0.618         [215]
   SIMON-128/256                 DBitNet           2-1-CT-R            20M           2M              ✓           20            0.507         [42]
   SIMON-128/256RK               N DGohr           2-1-CT-R+           20M           2M              -           16            0.5062        [177]
   Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out
   settings n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an
   elaborate, manually designed training procedure (-).
 / Unknown quantity.
 † A critical discussion of these results is provided in the text.
  RK
      Related key setting.



each sample with 16 pairs (640M pairs). Lu et al. [192] use                 tectures consistently achieve the highest accuracy among the
different training strategies depending on the scenario. In some            neural network distinguishers obtained for SIMECK. By using
cases, they employ a staged approach with 8 · (2 · 107 + 2 · 225 )          multiple ciphertext pairs (n = 16) and employing advanced
pairs, while in others they use 2 · 107 · 8 pairs directly.                 feature engineering techniques, as in [192], [222], [215],
   We end this section on SIMECK with a critical discussion                 the distinguisher performance surpasses this result, extending
of [206]. Tian et al. [206]† do not specify the size of their               the analysis to round 12 [192]. In the related-key setting,
training or validation sets, making it impossible to assess the             distinguishers can be trained for up to 15 rounds, a substantial
statistical reliability of their reported accuracy.                         improvement over the single additional round achieved for
                                                                            SIMON [192]. The task becomes easier when distinguishing
   2) SIMECK: SIMECK is a variant of SIMON using a
                                                                            between two ciphertext distributions rather than distinguishing
key schedule similar to that of SPECK. SIMECK-32/64,
                                                                            a single distribution from uniform. This approach enables
SIMECK 48/96, and SIMECK-64/128 have 32, 36, and 44
                                                                            attacks on one additional round using just a single ciphertext
rounds, respectively. Neural differential distinguishers have
                                                                            pair in the standard setting [215].
been developed for all versions of SIMECK.
   Table II provides an overview of the differential neural                    For the case of SIMECK, some authors experimented with
distinguishers developed for the SIMECK family of block                     a vast amount of data: In [222], the authors used the staged
ciphers. The most extensively studied variant is SIMECK-                    training approach proposed by Gohr in [17]: 2 · 107 , 2 · 109
32, with various neural network architectures explored across               samples with 8 pairs each (16160M pairs). In [42], the authors
multiple works. In the standard setting ( 2-1-CT-R ), the best              proposed a polishing step, retraining a neural distinguisher
distinguisher achieves round 10 through the original convo-                 initially trained with 107 pairs with an additional 109 pairs:
lutional architecture [187]. In general, convolutional archi-               107 , 109 (1010M pairs). This polishing step was also used
                                                                                                                                                               17



                                                                   TABLE II
                                      OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR SIMECK.

  Primitive                        Arch.              Class                 Trn.           Val.         AutoND          Rounds          Acc.          Ref.
  SIMECK-32                        N DGohr            2-1-CT-R              20M            2M               -           10              0.5407        [188]†
                                   N DGohr            2-1-CT-R              20M            2M               -           10              0.5438        [187]
                                   N DGohr            4-3-CT-R              67M            1M               -           11              0.5042        [211]
                                   DenseNet           2-2-CT-D              2020M          2M               ✓           12              0.505         [214]
                                   SE-ResNet          16-1-A-R              1394M          134M             -           12              0.5146        [192]
                                   INC                16-1-A-R              32320M         32M              -           12              0.5161        [222]
  SIMECK-32/64RK                   N DGohr            2-1-CT-R+             20M            2M               -           15              0.5134        [177]
                                   SE-ResNet          16-1-A-R              320M           32M              -           15              0.5467        [192]
                                   SE-ResNet          16-2-A-D              320M           32M              ✓           15              0.568         [215]
  SIMECK-32Unkeyed                 MLP                2-2-δ-D               66K            66K              -           9               0.526         [168]‡
  SIMECK-48/96                     DenseNet           2-2-CT-D              20M            2M               ✓           15              0.505         [214]
  SIMECK-48/96RK                   N DGohr            2-1-CT-R+             20M            2M               -           17              0.5206        [177]
                                   SE-ResNet          16-2-A-D              320M           32M              ✓           19              0.523         [215]
  SIMECK-64/128                    DenseNet           2-2-CT-D              20M            2M               ✓           18              0.507         [214]
                                   SE-ResNet          16-1-A-R              1394M          134M             -           18              0.5218        [192]
                                   N DGohr            2-1-CT-R+             20M            2M               -           20              0.5212        [177]
  SIMECK-64/128RK                  SE-ResNet          16-1-A-R              320M           32M              -           22              0.5180        [192]
                                   SE-ResNet          16-2-A-D              320M           32M              ✓           22              0.526         [215]
  SIMECK-64Unkeyed                 MLP                2-2-δ-D               66K            66K              -           14              0.55          [168]‡
   Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out
   settings n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an
   elaborate, manually designed training procedure (-).
 † A critical discussion of these results is provided in the text.
 RK
      Related key setting.
 ‡ The use of a small validation set raises concerns about the statistical robustness, reproducibility, and generalizability of the results, as such datasets are
   prone to high variance and may not reliably reflect model performance.



by Wang et al. [214] Lu et al. [192] use different training                      not specifically tailored to SPECK5 and lacks the complex
strategies depending on the scenario. In some cases, they                        training scheme essential for high accuracy on 8 rounds. More
employ a staged approach with 8 · (2 · 107 + 2 · 225 ) pairs,                    precisely, the authors proposed a polishing step, retraining a
while in others they use 2 · 107 · 8 pairs directly.                             neural distinguisher initially trained with 107 pairs with an
                                                                                 additional 109 pairs (1010M pairs in total). Zhang et al. and
                                                                                 Huang et al. [224], [182] used a staged training approach:
   We end this section on SIMECK with a critical discussion                      4·107 samples, each sample with 16 pairs (640M pairs). Wang
of [188]. In [188]† , the authors proposed training a neural                     and Wang [214] built upon the staged training proposed in
distinguisher multiple times independently and selecting the                     [42]. As the size of the validation set has not been explicitly
model with the highest test accuracy. Notably, they reported                     mentioned by the authors, we assume that they follow the size
successfully obtaining a single 10-round Simeck distinguisher                    in [42].
in only one out of 20 independent training attempts.                                Enhanced accuracy over Gohr’s results on ≥ 8-round
                                                                                 SPECK-32 can be achieved by employing advanced feature
                                                                                 engineering and multiple ciphertext pairs (e.g., n > 2). Indeed,
                                                                                 for 8-round SPECK-32, a higher accuracy is reported when
   3) SPECK: SPECK is a family of ARX block ciphers,                             using multiple ciphertext pairs for: [191] uses n = 128, and
denoted as SPECK-B/K, designed to encrypt blocks of size B                       [194] uses n = 512. For 9-round SPECK-32, [224] presents
with a key of size K. The variants SPECK-32/64, SPECK-                           the first distinguisher using 16 ciphertext pairs and advanced
48/96, SPECK-64/128, SPECK-96/96, and SPECK-128/256                              feature engineering.
consist of 22, 23, 27, 29, and 34 rounds, respectively. SPECK
                                                                                    The classification task becomes significantly easier when
is the cipher with the most published neural distinguishers to
                                                                                 distinguishing between two ciphertext distributions rather than
date. Neural differential distinguishers have been developed for
                                                                                 distinguishing a single distribution from uniform. This ap-
all SPECK versions, with a comprehensive overview presented
                                                                                 proach enables attacks on 8-round SPECK-32 with slightly
in Table III.
                                                                                 higher accuracy in the standard setting [214].
                                                                                    5 We note that [169] stated that “the simple training pipeline [of [42]] did
   In the standard setting (2-1-CT-R ) for SPECK-32, Gohr’s                      not produce N Ds with the same accuracy as Gohr’s on 8-round Speck32/64;
original analysis on 8 rounds [17] remains unmatched, in                         it needs a further polishing step to achieve similar accuracy, demanding more
which the author applied a staged training: 2 · 107 , 2 · 109                    time and data” which is not entirely correct. While in [42], a polishing step
                                                                                 is indeed needed to achieve the same accuracy, the polishing step is a highly
(2020M pairs). However, [42] achieved comparable accu-                           simplified and automated version of the 8-round training scheme used by
racy to [17] using an automated, generic pipeline that is                        Gohr (in conclusion, it does not demand more time or data).
                                                                                                                                                               18



                                                                   TABLE III
                                       OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR SPECK.

  Primitive                    Arch.                 Class                   Trn.          Val.         AutoND           Rounds         Acc.          Ref.
  SPECK-32                     Quantum               2-1-CT-R                60K           2K              -             5              0.53          [184]†
                               N Dsep.conv.
                                   Gohr              2-1-δtr -R              10M           1M              -             6              0.673         [190]
                               MLP                   2-1-δtr -R              20M           2M              -             6              0.688         [176]
                               MLP                   2-1-δ-R                 20M           2M              -             6              0.72          [176]
                               N Densmbl.
                                   Gohr              2-1-CT-R                20M           2M              -             6              0.781         [180]
                               N DGohr               100-1-A-R               20M           2M              -             6              1             [165]
                               DenseNet              2-1-CT-R                2M            2M              -             7              0.531         [202]†
                               N Dpruned
                                   Gohr              2-1-CT-R                20M           2M              -             7              0.596         [167]†
                               N DGohr               2-1-δ-R                 20M           2M              -             7              0.583         [165]
                               N DGohr               2-2-δ-D                 20M           2M              -             7              0.599         [210]
                               N DGohr               2-1-CT-R                2M            /              ✓              7              0.614         [209]
                               N Dattntn.
                                   Gohr              2-1-CT-R                20M           2M              -             7              0.6169        [175]
                               N Dsep.conv.
                                   Gohr              8-1-CT-R                80M           8M              -             7              0.6939        [190]
                               N DGohr               16-1-CT-R               20M           2M              -             7              0.7009        [174]
                               N Dattntn.
                                   Gohr              16-1-CT-R               160M          16M             -             7              0.728         [175]
                               INC                   64-1-A-R                64M           6.4M            -             7              0.9713        [217]
                               INCfreeze             2-1-CT-R                20M           2M              -             8              0.5135        [169]
                               N DGohr               2-1-CT-R                4040M         2M              -             8              0.514         [232]
                               DBitNet               2-1-CT-R                2020M         2M             ✓              8              0.514         [42]
                               DenseNet              2-2-CT-D                2020M         2M             ✓              8              0.519         [214]
                               MLP                   2-1-CT-DL               20M           2M              -             8              0.5208        [194]
                               N DGohr               128-1-A-R               1280M         128M            -             8              0.6502        [191]
                               MLP                   512-1-CT-DL             20M           2M              -             8              0.8866        [194]
                               INC                   32-1-A-R                1280M         2M              -             9              0.5045        [224]
  SPECK-32 RK                  N DGohr               2-2-δ-D                 20M           2M              -             7              0.559         [210]
                               N DGohr               2-2-CT-R                20M           2M              -             7              0.576         [210]
                               N DGohr               2-1-CT-R                2M            200K            -             9              0.5932        [208]
                               INCfreeze             2-1-CT-R                20M           2M              -             10             0.5562        [169]
  SPECK-32Unkeyed              MLP                   2-2-δ-D                 66K           66K             -             8              0.515         [168]‡
  SPECK-48                     N DGohr               2-1-CT-R                2M            /              ✓              6              0.726         [209]
                               DenseNet              2-2-CT-D                20M           2M             ✓              8              0.506         [214]
                               N DGohr               128-1-A-R               1280M         128M            -             8              0.5462        [191]
  SPECK-64                     N DGohr               2-1-CTtr -R             20M           2M              -             6              0.662         [182]
                               N DGohr               2-1-CT-R                20M           2M              -             6              0.754         [182]
                               N DGohr               2-1-CT-R                20M           2M              -             7              0.623         [182]
                               N DGohr               2-1-CT-R                2M            /              ✓              7              0.632         [209]
                               INC                   32-1-A-R                1280M         2M              -             7              0.641         [182]
                               DBitNet               2-1-CT-R                20M           2M             ✓              8              0.537         [42]
                               DenseNet              2-2-CT-D                20M           2M             ✓              8              0.559         [214]
                               N DGohr               128-1-δ-R               1280M         12.8M           -             8              0.632         [179]
                               N DGohr               128-1-A-R               1280M         128M            -             8              0.7181        [191]
  SPECK-96                     N DGohr               2-1-CTtr -R             20M           2M              -             7              0.681         [182]
                               N DGohr               2-1-CT-R                20M           2M              -             7              0.832         [182]
                               N DGohr               2-1-CT-R                20M           2M              -             7              0.850‡        [173]
  SPECK-128                    DBitNet               2-1-CT-R                20M           2M             ✓              10             0.593         [42]
   Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out
   settings n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an
   elaborate, manually designed training procedure (-).
 / Unknown quantity.
 † A critical discussion of these results is provided in the text.
  RK
      Related key setting.
 ‡ The use of a small validation set raises concerns about the statistical robustness, reproducibility, and generalizability of the results, as such datasets are
   prone to high variance and may not reliably reflect model performance.
 ‡ In [173], the accuracy of the teacher network for SPECK-96 was not given, but we were able to retrieve it by running the model from the authors’
   repository; we give the average of 10 runs, each with 106 samples.
 † In [167], the authors evaluated several pruned neural distinguishers; we report the smallest one, Gohr’s N D
                                                                                                                 Gohr with depth 1, 7 channels removed from
   C1, 21 from C2, 25 from C3, 46 neurons from D1, and 36 from D2.


   For 8-round SPECK-32, Lv et al. [194] demonstrated that                       volved an exhaustive search over differential-linear approxi-
differential-linear cryptanalysis can produce neural distin-                     mations with low Hamming weights, filtering out the most
guishers surpassing the state-of-the-art distinguishers based                    influential approximations using importance metrics from the
solely on differential cryptanalysis. Their methodology in-                      Light Gradient Boosting Machine (LGBM) classification al-
                                                                                                                                   19



gorithm. However, the authors incorrectly asserted that multi-      al. [21] found LSTMs superior to MLPs on TinyJAMBU and
pair neural differential distinguishers necessitate architectural   GIFT. Tcydenova et al. [208] evaluated various architectures
modifications. This assertion directly contradicts the work of      but found no significant improvements over ResNet, though
Gohr [23], which explicitly presented a concrete methodol-          they noted overfitting issues. Lv et al. [194] comprehensively
ogy for constructing multi-pair distinguishers from single-pair     compared multiple techniques for differential-linear crypt-
architectures without requiring structural changes. Notably,        analysis, with MLPs consistently outperforming alternatives,
the input difference employed in their 8-round distinguisher        including ELLR, Logistic Regression, and LightGBM.
exhibits significant divergence from conventional patterns es-         Convolutional neural networks, pioneered as the original
tablished in current literature, raising interesting questions      distinguisher architecture in [17], consistently demonstrate ex-
about optimal difference selection in neural cryptanalysis.         cellent performance in neural cryptanalysis, with convolutional
   In general, convolutional architectures consistently achieve     architectures ranking among the most effective distinguishers
the highest accuracy among neural network distinguishers for        across virtually all cryptographic primitives with a substan-
SPECK, with the exception of results in [194]. However, since       tial body of neural cryptanalytic research. This is expected
only MLPs have been trained for neural differential-linear          as DCNNs have demonstrated remarkable feature extraction
cryptanalysis, it remains unclear whether convolutional neural      capabilities across various disciplines, particularly in image
networks would be superior in this setting as well.                 recognition. Once the relevant features have been identified,
   Several studies demonstrate that neural distinguishers can       classical or simpler neural models can often achieve perfor-
achieve comparable performance using significantly truncated        mance comparable to their complex neural counterparts [165],
ciphertext data. Liu et al. [190] conducted interpretability        [169]. However, meaningful comparison between concrete
analysis linking neural distinguishers to truncated differentials   approaches remains challenging due to numerous influential
and advantage bits, developing an algorithm that success-           factors beyond architecture alone, including the number of
fully reduced ciphertexts to 8 bits while exploiting XOR            ciphertext samples and input differences, the sophistication of
differences to minimize training requirements. Ebrahimi et          feature engineering techniques, and the experimental design
al. [176] presented a Partial Differential ML-distinguisher for     variations. This complexity underscores the critical need for
SPECK32/64, achieving similar accuracy with 8-bit across six        comprehensive benchmarking studies to establish definitive
rounds. Huang et al. [182] similarly trained partial neural         conclusions about optimal approaches, a challenge we address
distinguishers on 11 ciphertext bits.                               in detail in subsection X-A.
   We end this section on SPECK with a critical discussion             Unlike natural language processing, neural cryptanalysis has
of [202] and [184]. Sajwan et al. [202]† reported an accuracy       not consistently benefited from the ”bigger is better” scaling
of 53.1% (round 7) on 2M training, respectively validation          paradigm described by Kaplan et al. [233]. Research has not
samples, and provides a comparison in which DenseNet out-           conclusively demonstrated that deeper or wider neural archi-
performs N DGohr . At such a small number of training sam-          tectures reliably improve distinguishing capability in cryp-
ples, both networks show heavy overfitting ([202, Table 2]),        tographic contexts. Notably, Gohr [17] employed shallower
and the authors themselves called the result only “marginal.”       architectures for distinguishers targeting near-uniform cipher-
In [184]† , the author reported an accuracy of 53% (round 5)        text distributions (specifically for 7 and 8 rounds of SPECK
on only 1,000 validation samples. The experimental mean or          encryption). Differential ciphertext distributions contain subtle
standard deviation was not given. The statistically expected        non-uniform statistical properties that remain challenging to
standard                                                            capture. This underscores a fundamental challenge in devel-
     √ deviation for a binomial experiment on 1k samples is
1/(2 n) = 1.6%. Therefore, the reported result is only 1.9σ         oping neural networks capable of effectively learning these
away from random and is likely not statistically significant.       cryptographic statistics – a problem requiring sophisticated
                                                                    modeling approaches, which we examine thoroughly in sub-
                                                                    section X-B.
D. Discussion                                                             b) Multi-Pair Distinguishers (n > 2): Neural distin-
Based on our comprehensive assessment of research in neural         guishers that process multiple ciphertext pairs simultaneously
differential cryptanalysis (subsection V-A), we identify several    have historically shown minimal practical advantages over
promising directions and critical challenges that merit further     simpler approaches [23], [174]. While these complex multi-
investigation. Our analysis focuses primarily on thoroughly         pair architectures typically performed equivalently or worse
vetted cryptographic primitives – those subjected to sub-           than single-pair distinguishers with basic score aggregation, re-
stantial cryptanalytic scrutiny, specifically SIMON (Table I),      cent evidence suggests this paradigm is shifting – particularly
SIMECK (Table II), SPECK (Table III).                               for lightweight block ciphers. Our comprehensive analysis
     a) Network Architectures (N): Findings on optimal neu-         reveals that for SPECK, SIMON, and SIMECK, multi-pair
ral network architectures for cryptanalysis remain contra-          distinguishers have successfully broken more rounds than their
dictory. While Baksi et al. [22] concluded CNNs were                single-pair counterparts. This development closely matches
unsuitable for distinguishers and found MLPs superior on            common notions in differential cryptanalysis: as the number
GIMLI-PERMUTATION, Bellini et al. [20] and Wang et al.              of rounds increases, the differential probability decreases, and
[210] demonstrated effective CNN-based distinguishers for           more data is needed to observe a bias; grouping multiple
PRESENT and SPECK. Mishra et al. [195] reported MLPs                pairs into a sample artificially increases the chance that a rare
outperforming CNNs on GIFT and PRIDE, whereas Sun et                but relevant differential propagation will occur within each
                                                                                                                                    20



sample.                                                              tion and combining ciphertext values with difference-related
   Interestingly, similar ideas have been widely studied in the      features. Interestingly, virtually all multi-pair distinguishers
machine learning community, in particular under the name of          obtaining state-of-the-art results utilize advanced feature en-
Multiple Instance Learning [234] (MIL), but the corresponding        gineering. Nevertheless, well-designed network architectures
techniques have so far not been applied at all in the context        can autonomously learn optimal feature representations, as
of neural distinguishers. A typical benchmark for MIL is the         demonstrated by Gohr et al. [23] for SIMON, which achieved
Elephant dataset, introduced in [235], where the samples are         comparable results to the feature engineering of Bao et
groups of images, with a positive label if the group contains an     al. [166].
elephant, and a negative label otherwise. This problem mirrors          The explainability analyses in [165] demonstrate that Gohr’s
the case of high rounds neural distinguishers, where most pairs      architecture NGohr effectively utilizes information beyond mere
are not helpful, but rare pairs that follow a ‘good’ differential    ciphertext differences (C1 ⊕ C2 ). Consequently, architectures
pattern (the elephants) determine the label. Recent approaches       incapable of efficiently extracting XOR differences from ci-
to the MIL problem, such as [236], seem to be promising              phertexts and feature engineering limited to solely ciphertext
directions to explore in order to improve multi-pair classifiers.    differences (F = δ) exhibit fundamental constraints, failing to
Similarly, the problem of anomaly detection has received             capture the full spectrum of cryptanalytically relevant features.
considerable attention in the machine learning community; if            The extent to which hand-crafted features enhance neural
we choose to treat the ‘elephant pair’ as an anomaly to an           network learning capabilities remains an open research ques-
otherwise unremarkable distribution, adapting approaches such        tion. Establishing comprehensive benchmarking frameworks
as Deep One-Class Classification [237] could yield interesting       would provide valuable insights into the relative merits of au-
results. Finally, the Deep Set framework [238] considers             tomated versus engineered feature extraction for cryptanalytic
functions of sets, and addresses issues such as permutation          applications (subsection X-A).
invariance, which are relevant to multiple pair classification,            e) Alternative Adversarial Models (E): Paralleling clas-
for which the order of the pairs has no importance.                  sical cryptanalysis, adversarial models with expanded ca-
   This evolving effectiveness of multi-pair architectures rep-      pabilities consistently outperform against increased cipher
resents a significant development and offers a promising             rounds, as demonstrated by related-key and conditional ap-
direction for future cryptanalytic research; however, this line      proaches extending several rounds beyond chosen plaintext
of work has so far largely ignored the significant body of work      counterparts. Rotational cryptanalysis and other specialized
available in the deep learning community, and we believe there       techniques have also shown promising results when adapted
is significant room for improvement through incorporating            to neural frameworks, exploiting structural weaknesses that
these techniques.                                                    conventional differential approaches might miss.
      c) Using Multiple Input Differences (m > 1): The                  The critical research question is what additional adversarial
effectiveness of differential cryptanalysis using multiple in-       models remain unexplored. Classical cryptanalysis offers nu-
put differences has been demonstrated across several cipher          merous attack vectors yet to be fully adapted to neural network
families, including SIMON, SIMECK, and SPECK. Gohr et                distinguishers. Systematically mapping these techniques to
al. [23] established a crucial relationship: neural differential     their neural counterparts could reveal new attack classes.
distinguisher accuracy correlates with the statistical distance
between the separated ciphertext-difference distributions (par-
                                                                           IX. N EURAL D ISTINGUISHER T RAINING : B EST
ticularly when distinguishing from a uniform distribution E =
                                                                                           P RACTICES
R). Distinguishers naturally perform better when targeting
input differences that produce more distinguishable output           Neural network training is not a deterministic process: it
distributions.                                                       is subject to significant variations in the outcome that are
   Despite this advantage, integrating multiple-difference ap-       caused, for example, by the (random) network parameter ini-
proaches into practical key recovery attacks presents sig-           tialization process, and the batch process of training data and
nificant challenges. The current attack framework pioneered          corresponding differing movement through the optimization
by Gohr [17] fundamentally relies on distinguishing real             plane. Further, the chosen hyperparameters and neural network
ciphertext distributions from uniform distributions as its core      architectures heavily influence the training outcome.
mechanism. Adapting this framework to leverage the statistical          To interpret the success of neural network training correctly,
power of multiple input differences would require substantial        it is important to distinguish between training, validation, and
modifications to the underlying cryptanalytic methodology.           test data carefully. Each dataset has an important role: The
   One promising research direction is exploiting structural re-     training data is used to calculate the loss of the model and
lationships between differential characteristics through switch-     to update the model parameters. However, the goal of neural
ing bits for adjoining differentials (SBfADs) [166]. For multi       network training is not good performance (low loss) on known
difference distinguishers, requirements could be relaxed to          data, but instead, generalization to previously unseen data. To
conformance with any one output difference, rather than              monitor the model’s performance on previously unseen data
requiring all differentials to share identical output differences.   during training, validation data is used.
      d) Feature Engineering (T ): Feature engineering has              A commonly observed phenomenon during neural network
demonstrated a significant impact on distinguisher perfor-           training is overfitting. At some point during the training, the
mance [192], with notable examples including partial decryp-         model does not learn new generalizable features of the training
                                                                                                                                              21



data but instead uses its parameters to learn the training                     of standard problems and compare them in a leaderboard.
dataset “by heart”. This leads to an increasing validation loss.               This objective is, however, not straightforward, and we discuss
Instead of using the model that has been trained for the                       some friction points below.
maximum number of epochs, in this case, one better uses the                          a) Defining Problems: A problem can be defined as an
model with the minimum validation data loss. However, the                      n-M -T -E configuration, a primitive, a training pipeline, and a
validation data has now been used in model optimization and                    dataset size. A logical first step would be evaluating all models
can no longer be used to characterize performance based on                     on the initial SPECK32 problem in the 2-1-CT-R setting to
previously unseen data. Fresh test data should be used for the                 identify top-performing architectures.
final characterization instead.                                                   Training regimes are critical: Gohr’s work [17] required
   The number of parameters of a deep neural network does                      an advanced pipeline with pre-training on likely differences
not relate to its computational training cost straightforwardly.               followed by re-training with 100× more samples to reach
Instead, it depends on the computations required by the                        8 rounds. Subsequent research often employs similar pol-
particular layers used in the network model. The computational                 ishing techniques. This creates a distinction between raw
training cost should be measured in terms of the required num-                 performance (training from scratch under consistent condi-
ber of FLOPs (floating point operations) or MACs (multiply-                    tions) and enhanced accuracy (using pretraining [232], layer
accumulate operations). Popular deep learning libraries such                   freezing [23], previous-round distinguisher retraining [20], or
as TensorFlow and PyTorch provide routines to obtain neural                    increased final-round samples). A standardized pipeline for
network parameter counts as well as FLOPs.6 For exam-                          comparing enhanced distinguishers would be beneficial.
ple, FLOPs can be evaluated with the TensorFlow Keras                             Sample quantity also matters. Many works follow Gohr’s
module keras-flops, and the TensorFlow native routine                          approach [17] (107 training, 106 test samples), as reduction
model.count_params() provides the parameter count.                             significantly impacts performance. Multiple-pair sample ap-
                                                                               proaches [44] present comparison challenges: fixing sample
   Commonly Overlooked Best Practices for Neural                               count gives unfair advantages to models seeing more pairs,
   Distinguisher Training                                                      while fixing pair count may disadvantage models trained on
                                                                               fewer samples (extreme case: 107 pairs per sample would
     1) Results Reporting I: Clearly indicate the results
                                                                               mean training on a single sample). Despite some works
        obtained on training, validation, and test datasets
                                                                               using over 1 billion ciphertexts, little research explores this
        and the size of each dataset.
                                                                               data magnitude in the 2-1-CT-R scenario versus multiple-pair
     2) Results Reporting II: Denote accuracy (or any
                                                                               approaches – an axis worth including in benchmarking studies.
        other metrics) with error margins on multiple sets
                                                                                     b) Metrics: The first challenge to comparing different
        of freshly generated test data.
                                                                               models is to define what is to be compared. As of now,
     3) Neural Network Reporting: Indicate the net-
                                                                               the main metrics used to compare neural distinguishers are
        work’s memory requirements using FLOPs and the
                                                                               accuracy, true positive rate, true negative rate, and more re-
        number of neural network parameters, and training
                                                                               cently [42], the number of floating point operations (FLOPS),
        time per epoch on the specific computational envi-
                                                                               which impacts the training time and quantifies the time com-
        ronment (e.g., number and type of GPUs or CPUs).
                                                                               plexity of the inference part in a key recovery attack. In the
     4) Open Reproducibility: Publish the code and
                                                                               Deep Learning community, the EfficientNet framework [239],
        trained model parameters to enable review, repli-
                                                                               which proposes techniques to scale a neural network based
        cation, and future comparisons.
                                                                               on inference speed or parameter count constraints, is often
                                                                               used as a baseline comparison for new models. For neural
   Though not unique to neural differential cryptanalysis, these               distinguishers, we could similarly use the number of parame-
best practices were frequently overlooked in papers during our                 ters and FLOPs ratio with the original architecture from Gohr,
literature review, underscoring the importance of emphasizing                  providing context to the obtained accuracy. However, we also
these standards.                                                               need dedicated metrics adapted to the specific use cases of
                                                                               neural cryptanalysis. In particular, the current metrics do not
                     X. F UTURE C HALLENGES                                    provide much information on the key recovery complexity,
A. The Benchmarking Challenge                                                  which largely depends on the wrong key response profile
As the field of neural cryptanalysis grows, it is becoming                     (see subsection IV-C), prepended differentials, and neutral bits.
more difficult to compare different works on a given primitive
due to significant variability in the architectures used, training             B. The AI-N D Challenge
regimes, distinguishing experiments, or feature engineering. To
                                                                               The neural network architectures currently employed in Neural
gain a better understanding of neural distinguisher, we see the
                                                                               Differential Cryptanalysis have origins that trace back sev-
creation of a benchmarking platform as an important challenge
                                                                               eral years. For instance, the Inception Module by Google
in the medium term. The goal of such a platform would be
                                                                               researchers was introduced in a seminal paper in 2014 [241].
to compare neural architectures submitted by authors on sets
                                                                               Similarly, Kaiming He et al. [242] won the ILSVRC (Ima-
  6 The performance of libraries for training neural distinguishers has been   geNet Large Scale Visual Recognition Challenge) 2015 using
compared in [168].                                                             ResNet. Attention was introduced in “Attention is all you
                                                                                                                                                   22




Fig. 4. Adapted from [240] with added data for Gohr’s N DGohr on Table III, and DBitNet on Table XI from [42, Table 5].



need” at NeurIPS 2017 [8], and Squeeze-and-Excitation Net-                 use more advanced AI technologies, but also at (ii) motivating
works at CVPR 2018 [243].                                                  cryptographers to establish an AI-competition7 to allow AI
   In recent years, deeper and more complex models have led                researchers and engineers to apply state-of-the-art methods to
to a larger parameter count. Figure 4 illustrates the general              Neural Differential Cryptanalysis.
trend of the increasing parameter count in deep learning
models. This is particularly evident in the case of Large Lan-                                      XI. C ONCLUSIONS
guage Models (LLMs), such as GPT, which contain billions                      In this paper, we perform a systematic review of the follow-
of parameters. The deep learning models used to date in                    ups to Gohr’s seminal paper on neural distinguishers. In the
Neural Differential Cryptanalysis have low parameter counts                process, we identify and classify works focusing on training
compared to more modern “Deep Learning Era” models. Chal-                  neural distinguishers. This systematic review uncovered a
lenges when increasing the model parameter count are higher                young yet vast body of research and a need for common
computational load, longer training times, and overfitting.                methodological guidelines to grow the field, which we attempt
   However, the advancement of AI technologies such as trans-              to provide. We also identified two challenges, namely compar-
formers and reinforcement learning, coupled with increased                 ing neural distinguisher results and scaling up to much larger
computational power, holds significant potential for enhancing             and more ambitious architectures.
cryptographic neural differential distinguishers. Transformers,               Over the past 6 years, multiple new settings have been
with their capability to handle long-range dependencies and                explored for differential cryptanalysis, using multiple pairs
their effectiveness in capturing complex patterns, offer a robust          per sample or polytopic differences, with the same or varied
framework for analyzing cryptographic data. Reinforcement                  keys across samples. In addition, various types of feature
learning, on the other hand, provides a powerful approach                  engineering, particularly through partial inversion, have been
for optimizing neural network performance through iterative                explored. These address the question of what clues we can
feedback and learning from interactions. These advanced AI                 give the neural distinguisher, and multiple avenues are left
methodologies, when applied to cryptographic neural dif-                   to explore in that direction. But more fundamentally, what
ferential distinguishers, can lead to more accurate models.                matters perhaps more is what question we ask the neural
The increased computational power available today allows                   distinguisher, given this clue, or said differently, what task
for training deeper and more complex networks, which can                   we ask the neural network to perform. So far, a large portion
explore a larger hypothesis space and uncover subtle crypto-               of the literature has focused on differential-based property for
graphic weaknesses that simpler models might miss.                         one pair and one input difference, but many variations could be
   Up until now, cryptographers have mainly attempted to                   built, as well as tasks related to different types of cryptanalysis
apply AI models. As illustrated in subsection X-A, a leader-               or entirely new distinguishing experiments.
board with cryptographically meaningful metrics should be                     7 Small AI-competitions are hosted on platforms such as Kaggle, while
established. Based on the existence of transparent metrics, the            large AI-competitions include the “Makrikadis” time series forecasting com-
AI-N D Challenge aims at (i) motivating cryptographers to                  petition [244], or ILSVRC [245].
                                                                                                                                                          23



                             R EFERENCES                                        [21] T. Sun, D. Shen, S. Long, Q. Deng, and S. Wang, “Neural distinguishers
                                                                                     on tinyjambu-128 and gift-64,” in International Conference on Neural
                                                                                     Information Processing. Springer, 2022, pp. 419–431.
 [1] J. Katz and Y. Lindell, Introduction to modern cryptography: principles
                                                                                [22] A. Baksi, J. Breier, Y. Chen, and X. Dong, “Machine learning-
     and protocols. Chapman and hall/CRC, 2007.
                                                                                     assisted differential distinguishers for lightweight ciphers,” Classical
 [2] E. Biham and A. Shamir, “Differential cryptanalysis of des-like cryp-           and Physical Security of Symmetric Key Cryptographic Algorithms,
     tosystems,” J. Cryptology, vol. 4, pp. 3–72, 1991.                              pp. 141–162, 2022.
 [3] K. Fukushima, “Neocognitron: A self-organizing neural network model        [23] A. Gohr, G. Leander, and P. Neumann, “An assessment of differential-
     for a mechanism of pattern recognition unaffected by shift in position,”        neural distinguishers,” Cryptology ePrint Archive, 2022.
     Biological cybernetics, vol. 36, no. 4, pp. 193–202, 1980.                 [24] E. Bellini, A. Hambitzer, M. Rossi et al., “A survey on machine
 [4] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based                 learning applied to symmetric cryptanalysis,” RENDICONTI DEL
     learning applied to document recognition,” Proceedings of the IEEE,             SEMINARIO MATEMATICO, vol. 80, pp. 107–122, 2022.
     vol. 86, no. 11, pp. 2278–2324, 1998.                                      [25] A. Nitaj and T. Rachidi, “Applications of neural network-based ai in
 [5] D. Silver, A. Huang, C. J. Maddison, A. Guez, L. Sifre, G. Van                  cryptography,” Cryptography, vol. 7, p. 39, 2023.
     Den Driessche, J. Schrittwieser, I. Antonoglou, V. Panneershelvam,         [26] J.-W. Chou, S.-D. Lin, and C.-M. Cheng, “On the effectiveness of using
     M. Lanctot et al., “Mastering the game of go with deep neural networks          state-of-the-art machine learning techniques to launch cryptographic
     and tree search,” nature, vol. 529, no. 7587, pp. 484–489, 2016.                distinguishing attacks,” in Proceedings of the 5th ACM Workshop
 [6] D. Silver, T. Hubert, J. Schrittwieser, I. Antonoglou, M. Lai, A. Guez,         on Security and Artificial Intelligence, ser. AISec ’12. New York,
     M. Lanctot, L. Sifre, D. Kumaran, T. Graepel et al., “A general                 NY, USA: Association for Computing Machinery, 2012, p. 105–110.
     reinforcement learning algorithm that masters chess, shogi, and go              [Online]. Available: https://doi.org/10.1145/2381896.2381912
     through self-play,” Science, vol. 362, no. 6419, pp. 1140–1144, 2018.      [27] I. Martı́nez, V. López, D. Rambaut, G. Obando, V. Gauthier-Umaña,
 [7] J. Schrittwieser, I. Antonoglou, T. Hubert, K. Simonyan, L. Sifre,              and J. F. Pérez, “Recent advances in machine learning for differential
     S. Schmitt, A. Guez, E. Lockhart, D. Hassabis, T. Graepel et al.,               cryptanalysis,” in Colombian Conference on Computing. Springer,
     “Mastering atari, go, chess and shogi by planning with a learned                2023, pp. 45–56.
     model,” Nature, vol. 588, no. 7839, pp. 604–609, 2020.                     [28] A. Singh, K. B. Sivangi, and A. N. Tentu, “Machine learning and
 [8] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N.                cryptanalysis: An in-depth exploration of current practices and future
     Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,”               potential,” Journal of Computing Theories and Applications, vol. 1,
     Advances in neural information processing systems, vol. 30, 2017.               no. 3, pp. 257–272, 2024.
 [9] W. Weaver, “Letter to norbert wiener,” 4 March 1947, https:                [29] W. S. Awad and E.-S. M. El-Alfy, Computational Intelligence in
     //aclanthology.org/1952.earlymt-1.1.pdf. [Online]. Available: https:            Cryptology. IGI Global, 2017, p. 1636–1652. [Online]. Available:
     //aclanthology.org/1952.earlymt-1.1.pdf                                         http://dx.doi.org/10.4018/978-1-5225-1759-7.ch065
[10] L. G. Valiant, “A theory of the learnable,” Commun. ACM,                   [30] M. L. Minsky and S. A. Papert, “Perceptrons: expanded edition,” 1988.
     vol. 27, no. 11, p. 1134–1142, nov 1984. [Online]. Available:              [31] A. Klimov, A. Mityagin, and A. Shamir, Analysis of Neural
     https://doi.org/10.1145/1968.1972                                               Cryptography. Springer Berlin Heidelberg, 2002, p. 288–298.
[11] R. L. Rivest, “Cryptography and machine learning,” in Proceedings               [Online]. Available: http://dx.doi.org/10.1007/3-540-36178-2 18
     of the International Conference on the Theory and Applications of          [32] M. Coutinho, R. de Oliveira Albuquerque, F. Borges, L. J. Garcı́a-
     Cryptology: Advances in Cryptology, ser. ASIACRYPT ’91. Berlin,                 Villalba, and T. Kim, “Learning perfectly secure cryptography to
     Heidelberg: Springer-Verlag, 1991, p. 427–439.                                  protect communications with adversarial neural cryptography,” Sensors,
[12] K. G. Paterson, B. Poettering, and J. C. N. Schuldt, “Big bias hunting          vol. 18, no. 5, p. 1306, 2018.
     in amazonia: Large-scale computation and exploitation of RC4 biases        [33] ——, “Learning perfectly secure cryptography to protect communica-
     (invited paper),” in Advances in Cryptology - ASIACRYPT 2014 - 20th             tions with adversarial neural cryptography,” Sensors, vol. 18, no. 5, p.
     International Conference on the Theory and Application of Cryptology            1306, 2018.
     and Information Security, Kaoshiung, Taiwan, R.O.C., December 7-11,        [34] C. E. Shannon, “Communication theory of secrecy systems,” Bell Syst.
     2014. Proceedings, Part I, ser. Lecture Notes in Computer Science,              Tech. J., vol. 28, no. 4, pp. 656–715, 1949.
     P. Sarkar and T. Iwata, Eds., vol. 8873. Springer, 2014, pp. 398–419.      [35] J. C. H. Castro, J. M. Sierra, P. Isasi, and A. Ribagorda, “Genetic
                                                                                     cryptoanalysis of two rounds TEA,” in Computational Science - ICCS
[13] M. Randolph and W. Diehl, “Power side-channel attack analysis: A
                                                                                     2002, International Conference, Amsterdam, The Netherlands, April
     review of 20 years of study for the layman,” Cryptogr., vol. 4, no. 2,
                                                                                     21-24, 2002. Proceedings, Part III, ser. Lecture Notes in Computer
     p. 15, 2020.
                                                                                     Science, P. M. A. Sloot, C. J. K. Tan, J. J. Dongarra, and A. G.
[14] S. Greydanus, “Learning the enigma with recurrent neural networks,”
                                                                                     Hoekstra, Eds., vol. 2331. Springer, 2002, pp. 1024–1031. [Online].
     CoRR, vol. abs/1708.07576, 2017. [Online]. Available: http://arxiv.
                                                                                     Available: https://doi.org/10.1007/3-540-47789-6 108
     org/abs/1708.07576
                                                                                [36] E. C. Laskari, G. C. Meletiou, Y. C. Stamatiou, and M. N. Vrahatis,
[15] A. N. Gomez, S. Huang, I. Zhang, B. M. Li, M. Osama, and L. Kaiser,             Cryptography and Cryptanalysis Through Computational Intelligence.
     “Unsupervised cipher cracking using discrete gans,” in 6th Interna-             Springer Berlin Heidelberg, 2007, p. 1–49. [Online]. Available:
     tional Conference on Learning Representations, ICLR 2018, Vancouver,            http://dx.doi.org/10.1007/978-3-540-71078-3 1
     BC, Canada, April 30 - May 3, 2018, Conference Track Proceedings.          [37] J. M. E. Tapiador, J. A. Clark, and J. C. Hernandez-Castro, Non-linear
     OpenReview.net, 2018.                                                           Cryptanalysis Revisited: Heuristic Search for Approximations to
[16] J. Chou, S. Lin, and C. Cheng, “On the effectiveness of using                   S-Boxes. Springer Berlin Heidelberg, 2007, p. 99–117. [Online].
     state-of-the-art machine learning techniques to launch cryptographic            Available: http://dx.doi.org/10.1007/978-3-540-77272-9 7
     distinguishing attacks,” in Proceedings of the 5th ACM Workshop on         [38] M. Sys, P. Svenda, M. Ukrop, and V. Matyas, “Constructing empirical
     Security and Artificial Intelligence, AISec 2012, Raleigh, NC, USA,             tests of randomness,” in Proceedings of the 11th International
     October 19, 2012, T. Yu, V. N. Venkatakrishan, and A. Kapadia, Eds.             Conference on Security and Cryptography. SCITEPRESS - Science
     ACM, 2012, pp. 105–110.                                                         and Technology Publications, 2014. [Online]. Available: http:
[17] A. Gohr, “Improving attacks on round-reduced speck32/64 using deep              //dx.doi.org/10.5220/0005023902290237
     learning,” in Advances in Cryptology–CRYPTO 2019: 39th Annual              [39] H. Robbins and S. Monro, “A stochastic approximation method,” The
     International Cryptology Conference, Santa Barbara, CA, USA, August             annals of mathematical statistics, pp. 400–407, 1951.
     18–22, 2019, Proceedings, Part II 39. Springer, 2019, pp. 150–179.         [40] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimiza-
[18] R. Beaulieu, S. Treatman-Clark, D. Shors, B. Weeks, J. Smith, and               tion,” in 3rd International Conference on Learning Representations,
     L. Wingers, “The simon and speck lightweight block ciphers,” in 2015            ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track
     52nd ACM/EDAC/IEEE Design Automation Conference (DAC), 2015,                    Proceedings, Y. Bengio and Y. LeCun, Eds., 2015.
     pp. 1–6.                                                                   [41] A. E. Hoerl and R. W. Kennard, “Ridge regression: Biased estimation
[19] B. Seok, “Truncated differential-neural key recovery attacks on round-          for nonorthogonal problems,” Technometrics, vol. 42, no. 1, pp. 80–86,
     reduced hight,” Electronics, vol. 13, no. 20, p. 4053, 2024.                    2000.
[20] E. Bellini and M. Rossi, “Performance comparison between deep              [42] E. Bellini, D. Gerault, A. Hambitzer, M. Rossi et al., “A cipher-
     learning-based and conventional cryptographic distinguishers,” in In-           agnostic neural training pipeline with automated finding of good input
     telligent Computing: Proceedings of the 2021 Computing Conference,              differences,” IACR TRANSACTION ON SYMMETRIC CRYPTOLOGY,
     Volume 3. Springer, 2021, pp. 681–701.                                          vol. 2023, no. 3, pp. 184–212, 2023.
                                                                                                                                                            24



[43] Z. Bao, J. Guo, M. Liu, L. Ma, and Y. Tu, “Conditional differential-        [71] B. Zahednejad and J. Li, “An improved integral distinguisher scheme
     neural cryptanalysis.” IACR Cryptol. ePrint Arch., vol. 2021, p. 719,            based on deep learning,” EasyChair, Technical report, Tech. Rep., 2020.
     2021.                                                                       [72] ——, “An improved integral distinguisher scheme based on deep
[44] A. Baksi, J. Breier, Y. Chen, and X. Dong, “Machine learning assisted            learning,” 2020.
     differential distinguishers for lightweight ciphers (extended version),”    [73] L. Zhang and Z. Wang, “Improving differential-neural distinguisher
     Cryptology ePrint Archive, 2020.                                                 model for des, chaskey, and present,” arXiv preprint arXiv:2204.06341,
[45] A. Baksi, J. Breier, V. A. Dasu, and X. Hou, “Machine learning attacks           2022.
     on speck,” Security and Implementation of Lightweight Cryptography          [74] W. Zheng, L. Zhang, and Z. Wang, “Theoretical explanation and
     (SILC), pp. 1–6, 2021.                                                           improvement of deep learning-aided cryptanalysis,” Cryptology ePrint
[46] A. Baksi, J. Breier, A. Chattopadhyay, T. Gerlich, S. Guilley, N. Gupta,         Archive, 2024.
     T. Isobe, A. Jati, P. Jedlicka, H. Kim et al., “Baksheesh: Similar yet      [75] R. Zhou, M. Duan, Q. Wang, Q. Wu, S. Guo, L. Guo, and Z. Gong,
     different from gift,” Cryptology ePrint Archive, 2023.                           “Neural-linear attack based on distribution data and its application on
[47] J. Dani, K. Nakka, and N. Saxena, “Breaking indistinguishability                 des,” Cryptology ePrint Archive, 2023.
     with transfer learning: A first look at SPECK32/64 lightweight              [76] C. Brunetta, “Cryptographic tools for privacy preservation,” Ph.D. dis-
     block ciphers,” CoRR, vol. abs/2405.19683, 2024. [Online]. Available:            sertation, Department of Computer Science & Engineering, Chalmers
     https://doi.org/10.48550/arXiv.2405.19683                                        University of Technology, Gothenburg, Sweden, 2021.
[48] M. ElSheikh, “Milp-aided cryptanalysis of some block ciphers,” Ph.D.        [77] L. Cardoso Dos Santos, “Design, cryptanalysis and protection of
     dissertation, Concordia University, 2021.                                        symmetric encryption algorithms,” Ph.D. dissertation, Universite Du
[49] A. Gohr, S. Jacob, and W. Schindler, “Efficient solutions of the ches            Luxembourg, The Faculty of Science, Technology and Medicine, 2022.
     2018 aes challenge using deep residual neural networks and knowledge        [78] M. S. Naik, M. Mallam, and C. S. Nataraju, “Machine learning-based
     distillation on adversarial examples february 12, 2020,” challenge,              lightweight block ciphers for resource-constrained internet of things
     vol. 2, p. 2, 2020.                                                              networks: a review.” International Journal of Electrical & Computer
[50] A. Gohr, “Brute force cryptanalysis,” Cryptology ePrint Archive, 2022.           Engineering (2088-8708), vol. 14, no. 3, 2024.
[51] Z. Hou, J. Ren, and S. Chen, “Cryptanalysis of round-reduced simon32        [79] S. Picek and D. Jakobovic, “Evolutionary computation and machine
     based on deep learning,” Cryptology ePrint Archive, 2021.                        learning in cryptology,” in Proceedings of the Genetic and Evolutionary
[52] ——, “Improve neural distinguisher for cryptanalysis,” Cryptology                 Computation Conference Companion, 2021, pp. 1089–1118.
     ePrint Archive, 2021.                                                       [80] ——, “Evolutionary computation and machine learning in security,” in
[53] ——, “Sat-based method to improve neural distinguisher and applica-               Proceedings of the Genetic and Evolutionary Computation Conference
     tions to simon,” Cryptology ePrint Archive, 2021.                                Companion, 2022, pp. 1572–1601.
[54] A. Jain, V. Kohli, and G. Mishra, “Deep learning based differential dis-
                                                                                 [81] M. Rossi, “Automatic differential cryptanalysis of symmetric ciphers,”
     tinguisher for lightweight cipher present,” Cryptology ePrint Archive,
                                                                                      Ph.D. dissertation, Polytechnic University of Turin, Italy, 2024.
     2020.
                                                                                      [Online]. Available: https://hdl.handle.net/11583/2993918
[55] ——, “Deep learning based differential distinguisher for lightweight
                                                                                 [82] Å. Å. Sommervoll, “Machine learning for offensive cyber operations,”
     block ciphers,” arXiv preprint arXiv:2112.05061, 2021.
                                                                                      Ph.D. dissertation, Institute for Informatics, University of Oslo, 2023.
[56] P. Junod, “Statistical cryptanalysis of block ciphers,” EPFL, Tech. Rep.,
                                                                                 [83] Q. Q. Tan, “Cryptanalysis of lightweight symmetric-key cryptographic
     2005.
                                                                                      algorithms,” Ph.D. dissertation, Nanyang Technical University, Singa-
[57] H. Kim, K. Jang, S. Lim, Y. Kang, W. Kim, and H. Seo, “Quantum
                                                                                      pore, 2023.
     neural network based distinguisher for differential cryptanalysis on
     simplified block ciphers,” Cryptology ePrint Archive, 2022.                 [84] Y. Tu, “Machine learning-aided and sat-aided cryptanalysis of
[58] B. D. Kim, V. A. Vasudevan, R. G. D’Oliveira, A. Cohen, T. Stahlbuhk,            symmetric-key primitives,” Ph.D. dissertation, Nanyang Technical Uni-
     and M. Médard, “Cryptanalysis via machine learning based information            versity, Singapore, 2022.
     theoretic metrics,” arXiv preprint arXiv:2501.15076, 2025.                  [85] Y. Zhong and J. Gu, “Lightweight block ciphers for resource-
[59] J. Lu, G. Liu, Y. Liu, B. Sun, C. Li, and L. Liu, “Improved neural               constrained environments: A comprehensive survey,” Future Genera-
     distinguishers with (related-key) differentials: Applications in SIMON           tion Computer Systems, 2024.
     and SIMECK,” CoRR, vol. abs/2201.03767, 2022. [Online]. Available:          [86] A. Baksi, “Classical and physical security of symmetric key crypto-
     https://arxiv.org/abs/2201.03767                                                 graphic algorithms,” in 2021 IFIP/IEEE 29th International Conference
[60] T. R. Lee, J. S. Teh, N. Jamil, J. L. S. Yan, and J. Chen, “Assessing            on Very Large Scale Integration (VLSI-SoC). IEEE, 2021, pp. 1–2.
     lightweight block cipher security using linear and nonlinear machine        [87] A. Biryukov, L. Cardoso dos Santos, J. S. Teh, A. Udovenko, and
     learning classifiers,” Cryptology ePrint Archive, 2020.                          V. Velichkov, “Meet-in-the-filter and dynamic counting with applica-
[61] C. Li, J. Sotakova, E. Wenger, Z. Allen-Zhu, F. Charton, and K. Lauter,          tions to speck,” in International Conference on Applied Cryptography
     “Salsa verde: a machine learning attack on learning with errors with             and Network Security. Springer, 2023, pp. 149–177.
     sparse small secrets,” arXiv preprint arXiv:2306.11641, 2023.               [88] M. Eichlseder, G. Leander, and S. Rasoolzadeh, “Computing expected
[62] J. Liu, J. Ren, and S. Chen, “Effective network parameter reduction              differential probability of (truncated) differentials and expected linear
     schemes for neural distinguisher,” Cryptology ePrint Archive, 2022.              potential of (multidimensional) linear hulls in spn block ciphers,” in
[63] D. Pal, U. Mandal, M. Chaudhury, A. Das, and D. R. Chowdhury,                    Progress in Cryptology–INDOCRYPT 2020: 21st International Con-
     “A deep neural differential distinguisher for arx based block cipher,”           ference on Cryptology in India, Bangalore, India, December 13–16,
     Cryptology ePrint Archive, 2022.                                                 2020, Proceedings 21. Springer, 2020, pp. 345–369.
[64] M. Pareek, G. Mishra, and V. Kohli, “Deep learning based analysis of        [89] Z. Feng, Y. Luo, C. Wang, Q. Yang, Z. Liu, and L. Song, “Improved
     key scheduling algorithm of present cipher,” Cryptology ePrint Archive,          differential cryptanalysis on speck using plaintext structures,” in Aus-
     2020.                                                                            tralasian Conference on Information Security and Privacy. Springer,
[65] A. Sajwan and G. Mishra, “Comparative analysis of resnet and densenet            2023, pp. 3–24.
     for differential cryptanalysis of speck 32/64 lightweight block cipher,”    [90] D. Gerault, T. Peyrin, and Q. Q. Tan, “Exploring differential-based dis-
     Cryptology ePrint Archive, 2023.                                                 tinguishers and forgeries for ascon,” IACR Transactions on Symmetric
[66] S. Stevens and Y. Su, “Memorization for good: Encryption with                    Cryptology, 2021.
     autoregressive language models,” CoRR, vol. abs/2305.10445, 2023.           [91] S. Karthika and K. Singh, “Theoretical and deep learning based
     [Online]. Available: https://doi.org/10.48550/arXiv.2305.10445                   analysis of biases in salsa 128 bits,” in International Symposium on
[67] S. Stevens, E. Wenger, C. Li, N. Nolte, E. Saxena, F. Charton, and               Mobile Internet Security. Springer, 2022, pp. 147–164.
     K. Lauter, “Salsa fresca: Angular embeddings and pre-training for           [92] M. Kumar and T. Yadav, “Milp based differential attack on round
     ml attacks on learning with errors,” arXiv preprint arXiv:2402.01082,            reduced warp,” in International Conference on Security, Privacy, and
     2024.                                                                            Applied Cryptography Engineering. Springer, 2021, pp. 42–59.
[68] N. Sugio, “Implementation of cryptanalytic programs using chatgpt,”         [93] T. Prantl, M. Lauer, L. Horn, S. Engel, D. Dingel, A. Bauer,
     Cryptology ePrint Archive, 2024.                                                 C. Krupitzer, and S. Kounev, “Security analysis of a decentralized,
[69] P. Wang, S. Nagaraja, A. Bourquard, H. Gao, and J. Yan, “Sok:                    revocable and verifiable attribute-based encryption scheme,” in
     Acoustic side channels,” arXiv preprint arXiv:2308.03806, 2023.                  Proceedings of the 19th International Conference on Availability,
[70] X. Yuan and Q. Wang, “Improving differential-neural distinguisher for            Reliability and Security, ARES 2024, Vienna, Austria, 30 July 2024
     simeck family,” IACR Cryptol. ePrint Arch., p. 2002, 2024. [Online].             - 2 August 2024. ACM, 2024, pp. 24:1–24:11. [Online]. Available:
     Available: https://eprint.iacr.org/2024/2002                                     https://doi.org/10.1145/3664476.3664487
                                                                                                                                                              25



 [94] J. Shi, C. Li, and G. Liu, “Differential attack with constants on µ2        [113] Z. Tolba, M. Derdour, and N. E. H. Dehimi, “Machine learning
      block cipher,” The Computer Journal, vol. 67, pp. 195–209, 2024.                  based cryptanalysis techniques: perspectives, challenges and future
 [95] F. Wang and G. Wang, “Improved differential-linear attack with ap-                directions,” in 2022 4th International Conference on Pattern Analysis
      plication to round-reduced speck32/64,” in International Conference               and Intelligent Systems (PAIS). IEEE, 2022, pp. 1–7.
      on Applied Cryptography and Network Security. Springer, 2022, pp.           [114] T. Yap, A. Benamira, S. Bhasin, and T. Peyrin, “Peek into the
      792–808.                                                                          black-box: Interpretable neural network using sat equations in side-
 [96] T. Yadav and M. Kumar, “Miles: Modeling large s-box in milp based                 channel analysis,” IACR Transactions on Cryptographic Hardware and
      differential characteristic search.” IACR Cryptol. ePrint Arch., vol.             Embedded Systems, pp. 24–53, 2023.
      2021, p. 1388, 2021.                                                        [115] Q. Zhang, H. Zhang, X. Cui, X. Fang, and X. Wang, “Side channel
 [97] ——, “Modeling large s-box in milp and a (related-key) differential                analysis of speck based on transfer learning,” Sensors, vol. 22, p. 4671,
      attack on full round pipo-64/128,” in International Conference on                 2022.
      Security, Privacy, and Applied Cryptography Engineering. Springer,          [116] C. Brunetta and P. Picazo-Sanchez, “Modelling cryptographic distin-
      2022, pp. 3–27.                                                                   guishers using machine learning,” Journal of Cryptographic Engineer-
 [98] A. Shafran, E. Malach, T. Ristenpart, G. Segev, and S. Tessaro, “Is               ing, vol. 12, pp. 123–135, 2022.
      ml-based cryptanalysis inherently limited? simulating cryptographic         [117] S. K. Dadhwal and G. Mishra, “Machine learning-based classification
      adversaries via gradient-based methods,” in Advances in Cryptology                between block cipher and stream cipher,” in Inventive Computation
      - CRYPTO 2024 - 44th Annual International Cryptology Conference,                  and Information Technologies: Proceedings of ICICIT 2022. Springer,
      Santa Barbara, CA, USA, August 18-22, 2024, Proceedings, Part VI,                 2023, pp. 531–542.
      ser. Lecture Notes in Computer Science, L. Reyzin and D. Stebila,           [118] G. Mishra, S. Pal, S. K. Murthy, K. Vats, and R. Raina, “Distinguish-
      Eds., vol. 14925. Springer, 2024, pp. 37–71.                                      ing lightweight block ciphers in encrypted images,” Defence Science
 [99] H. Grari, K. Zine-Dine, A. Azouaoui, and S. Lamzabi, “Deep learning-              Journal, vol. 71, pp. 647–655, 2021.
      based cryptanalysis of a simplified aes cipher,” International Journal      [119] R. Xia, M. Li, S. Chen et al., “Cryptographic algorithms identification
      of Information Security and Privacy (IJISP), vol. 16, pp. 1–16, 2022.             based on deep learning,” in CS & IT Conference Proceedings, vol. 12.
[100] H.-J. Kim, G.-J. Song, K.-B. Jang, and H.-J. Seo, “Cryptanalysis                  CS & IT Conference Proceedings, 2022.
      of caesar using quantum support vector machine,” in 2021 IEEE               [120] D. Jankovikj, H. Mihajloska Trpceska, and V. Dimitrova, “Cryptanaly-
      International Conference on Consumer Electronics-Asia (ICCE-Asia).
                                                                                        sis of round-reduced ascon powered by ml,” in The 19th International
      IEEE, 2021, pp. 1–5.                                                              Conference on Informatics and Information Technologies – CIIT, 2022.
[101] H. Kim, S. Lim, Y. Kang, W. Kim, D. Kim, S. Yoon, and H. Seo,
                                                                                  [121] G. Liu, J. Lu, H. Li, P. Tang, and W. Qiu, “Preimage attacks against
      “Deep-learning-based cryptanalysis of lightweight block ciphers revis-
                                                                                        lightweight scheme xoodyak based on deep learning,” in Advances
      ited,” Entropy, vol. 25, p. 986, 2023.
                                                                                        in Information and Communication: Proceedings of the 2021 Future
[102] E. Leierzopf, V. Mikhalev, N. Kopal, B. Esslinger, H. Lampesberger,               of Information and Communication Conference (FICC), Volume 2.
      and E. Hermann, “Detection of classical cipher types with feature-                Springer, 2021, pp. 637–648.
      learning approaches,” in Data Mining: 19th Australasian Conference
      on Data Mining, AusDM 2021, Brisbane, QLD, Australia, December              [122] M. G. Perusheska, H. M. Trpceska, and V. Dimitrova, “Deep learning-
      14-15, 2021, Proceedings 19. Springer, 2021, pp. 152–164.                         based cryptanalysis of different aes modes of operation,” in Future
                                                                                        of Information and Communication Conference. Springer, 2022, pp.
[103] S. Park, H. Kim, and I. Moon, “Automated classical cipher emula-
                                                                                        675–693.
      tion attacks via unified unsupervised generative adversarial networks,”
      Cryptography, vol. 7, p. 35, 2023.                                          [123] E. Bellini, D. Gerault, J. Grados, Y. J. Huang, R. Makarim, M. Rachidi,
[104] D. Pal, U. Mandal, A. Das, and D. R. Chowdhury, “Deep learning based              and S. Tiwari, “Claasp: a cryptographic library for the automated
      differential classifier of pride and rc5,” in International Conference on         analysis of symmetric primitives,” in International Conference on
      Applications and Techniques in Information Security. Springer, 2022,              Selected Areas in Cryptography. Springer, 2023, pp. 387–408.
      pp. 46–58.                                                                  [124] B. Esslinger, Learning and Experiencing Cryptography with CrypTool
[105] I. Aishwarya, L. Koduvayur Viswanathan, C. Srinivasan, G. Mishra,                 and SageMath. Artech House, 2023.
      S. K. Pal, and M. Sethumadhavan, “Improving the security of the lcb         [125] R. A. Hallman, “Poster evegan: Using generative deep learning for
      block cipher against deep learning-based attacks,” Cryptography, vol. 8,          cryptanalysis,” in Proceedings of the 2022 ACM SIGSAC Conference
      no. 4, p. 55, 2024.                                                               on Computer and Communications Security, 2022, pp. 3355–3357.
[106] B. Y. Chong and I. Salam, “Investigating deep learning approaches           [126] M. F. Idris, J. S. Teh, and M. N. Yusoff, “Diffgen: a data-
      on the security analysis of cryptographic algorithms,” Cryptography,              driven framework for generating truncated differentials,” Appl.
      vol. 5, p. 30, 2021.                                                              Intell., vol. 55, no. 5, p. 329, 2025. [Online]. Available: https:
[107] Y. Huang, L. Li, Y. Guo, Y. Ou, and X. Huang, “An efficient differential          //doi.org/10.1007/s10489-025-06248-0
      analysis method based on deep learning,” Computer Networks, vol. 224,       [127] G. Lv, C. Jin, Z. Shi, and T. Cui, “Unveiling the neutral difference
      p. 109622, 2023.                                                                  and its automated search,” IET Inf. Secur., vol. 2024, pp. 1–15, 2024.
[108] M. F. Idris, J. S. Teh, J. L. S. Yan, and W.-Z. Yeoh, “A deep learning            [Online]. Available: https://doi.org/10.1049/2024/2939486
      approach for active s-box prediction of lightweight generalized feistel     [128] M. Paravisi, A. Visconti, and D. Malchiodi, “Security analysis
      block ciphers,” IEEE Access, vol. 9, pp. 104 205–104 216, 2021.                   of cryptographic algorithms: Hints from machine learning,” in
[109] T. R. Lee, J. S. Teh, N. Jamil, J. L. S. Yan, and J. Chen, “Lightweight           Engineering Applications of Neural Networks - 25th International
      block cipher security evaluation based on machine learning classifiers            Conference, EANN 2024, Corfu, Greece, June 27-30, 2024,
      and active s-boxes,” IEEE Access, vol. 9, pp. 134 052–134 064, 2021.              Proceedings, ser. Communications in Computer and Information
[110] L. Mariot, D. Jakobovic, T. Bäck, and J. Hernandez-Castro, “Artificial           Science, L. S. Iliadis, I. Maglogiannis, A. Papaleonidas, E. Pimenidis,
      intelligence for the design of symmetric cryptographic primitives,”               and C. Jayne, Eds., vol. 2141. Springer, 2024, pp. 569–580. [Online].
      in Security and Artificial Intelligence: A Crossdisciplinary Approach.            Available: https://doi.org/10.1007/978-3-031-62495-7 43
      Springer, 2022, pp. 3–24.                                                   [129] K. Bhargavi, C. Srinivasan, and K. Lakshmy, “Panther: a sponge
[111] H. Watanabe, R. Ito, and T. Ohigashi, “On the effects of neural                   based lightweight authenticated encryption scheme,” in Progress in
      network-based output prediction attacks on the design of symmetric-               Cryptology–INDOCRYPT 2021: 22nd International Conference on
      key ciphers,” in Cyber Security, Cryptology, and Machine Learning                 Cryptology in India, Jaipur, India, December 12–15, 2021, Proceedings
      - 8th International Symposium, CSCML 2024, Be’er Sheva, Israel,                   22. Springer, 2021, pp. 49–70.
      December 19-20, 2024, Proceedings, ser. Lecture Notes in Computer           [130] A. Chakraborti, N. Datta, A. Jha, C. Mancillas-López, and M. Nandi,
      Science, S. Dolev, M. Elhadad, M. Kutylowski, and G. Persiano,                    “thyena: Making hyena even smaller,” in Progress in Cryptology -
      Eds., vol. 15349. Springer, 2024, pp. 201–218. [Online]. Available:               INDOCRYPT 2021 - 22nd International Conference on Cryptology in
      https://doi.org/10.1007/978-3-031-76934-4 13                                      India, Jaipur, India, December 12-15, 2021, Proceedings, ser. Lecture
[112] A. Gohr, S. Jacob, and W. Schindler, “Subsampling and knowledge                   Notes in Computer Science, A. Adhikari, R. Küsters, and B. Preneel,
      distillation on adversarial examples: New techniques for deep learning            Eds., vol. 13143. Springer, 2021, pp. 26–48. [Online]. Available:
      based side channel evaluations,” in Selected Areas in Cryptography:               https://doi.org/10.1007/978-3-030-92518-5 2
      27th International Conference, Halifax, NS, Canada (Virtual Event),         [131] Y. Deng, J. Chen, and J. Wang, “An image compression encryption
      October 21-23, 2020, Revised Selected Papers 27. Springer, 2021,                  based on the semi-tensor product and the dft measurement matrix,”
      pp. 567–592.                                                                      Optik, vol. 288, p. 171175, 2023.
                                                                                                                                                             26



[132] A. Fanfakh, N. Abduljalil, and A. K. M. Al-Qurabat, “Parallel multi-              of Information and Communication Conference. Springer, 2022, pp.
      core implementation of the optimized speck cipher.” International                 675–693.
      Journal of Safety & Security Engineering, vol. 14, no. 3, 2024.             [152] B. Hou, Y. Li, H. Zhao, and B. Wu, “Linear attack on round-reduced
[133] O. Jeong and I. Moon, “Deep learning-based hash function                          des using deep learning,” in Computer Security–ESORICS 2020: 25th
      cryptanalysis,” in 15th International Conference on Information and               European Symposium on Research in Computer Security, ESORICS
      Communication Technology Convergence, ICTC 2024, Jeju Island,                     2020, Guildford, UK, September 14–18, 2020, Proceedings, Part II 25.
      Republic of Korea, October 16-18, 2024. IEEE, 2024, pp. 1302–                     Springer, 2020, pp. 131–145.
      1303. [Online]. Available: https://doi.org/10.1109/ICTC62082.2024.          [153] M. Kang, Y. Li, L. Jiao, and M. Wang, “Differential analysis of
      10826852                                                                          arx block ciphers based on an improved genetic algorithm,” Chinese
[134] H. Kimura, K. Emura, T. Isobe, R. Ito, K. Ogawa, and T. Ohigashi,                 Journal of Electronics, vol. 32, pp. 225–236, 2023.
      “Output prediction attacks on block ciphers using deep learning,”           [154] S. Karthika, “Check for theoretical and deep learning based analysis
      in International Conference on Applied Cryptography and Network                   of biases in salsa 128 bits sk karthika) and kunwar singh department
      Security. Springer, 2022, pp. 248–276.                                            of of computer science and engineering, national institute of,” in
[135] ——, “A deeper look into deep learning-based output prediction attacks             Mobile Internet Security: 6th International Symposium, MobiSec 2022,
      using weak spn block ciphers,” Journal of Information Processing,                 Jeju, South Korea, December 15–17, 2022, Revised Selected Papers.
      vol. 31, pp. 550–561, 2023.                                                       Springer Nature, 2023, p. 147.
[136] R. D. Labio and E. Festijo, “Neural network–based cryptanalysis of          [155] G. Mishra, I. Gupta, S. Krishna Murthy, and S. Pal, “Deep learning
      present and d-present block ciphers,” in Cryptology and Information               based cryptanalysis of stream ciphers.” Defence Science Journal,
      Security Conference 2024, 2024, p. 110.                                           vol. 71, 2021.
[137] Y. Huang, L. Li, D. Li, and Y. Li, “Iabc: A neural integral distinguisher   [156] G. Mishra, S. Krishna Murthy, and S. Pal, “Dependency of lightweight
      for and-rx ciphers,” Journal of Intelligent & Fuzzy Systems, no.                  block ciphers over s-boxes: A deep learning based analysis,” Journal
      Preprint, pp. 1–15.                                                               of Discrete Mathematical Sciences and Cryptography, pp. 1–21, 2021.
[138] W. Wu and M. Guo, “Improved integral neural distinguisher model for         [157] P. Ma, Z. Liu, Y. Yuan, and S. Wang, “Neurald: Detecting indistin-
      lightweight cipher PRESENT,” Cybersecur., vol. 7, no. 1, p. 65, 2024.             guishability violations of oblivious ram with neural distinguishers,”
      [Online]. Available: https://doi.org/10.1186/s42400-024-00258-0                   IEEE Transactions on Information Forensics and Security, vol. 17, pp.
[139] B. Zahednejad and L. Lyu, “An improved integral distinguisher scheme              982–997, 2022.
      based on neural networks,” International Journal of Intelligent Systems,    [158] Q. Pang, Y. Yuan, and S. Wang, “Mpcdiff: Testing and repairing mpc-
      vol. 37, pp. 7584–7613, 2022.                                                     hardened deep learning models,” in Network and Distributed System
[140] Z. Tolba and M. Derdour, “Deep learning for cryptanalysis attack on               Security (NDSS) Symposium. NDSS, 2024.
      iomt wireless communications via smart eavesdropping,” in 2021 Inter-       [159] R. Rajan, R. K. Roy, D. Sen, and G. Mishra, “Gift-cofb,” Machine
      national Conference on Networking and Advanced Systems (ICNAS).                   Intelligence and Smart Systems: Proceedings of MISS 2021, p. 397,
      IEEE, 2021, pp. 1–6.                                                              2022.
[141] B. Zahednejad, L. Ke, and J. Li, “A novel machine learning-based            [160] J. So, “Deep learning-based cryptanalysis of lightweight block ciphers,”
      approach for security analysis of authentication and key agreement                Security and Communication Networks, vol. 2020, pp. 1–11, 2020.
      protocols,” Security and Communication Networks, vol. 2020, pp. 1–          [161] N. Sugio, “Implementation of cryptanalytic program for ASCON
      15, 2020.                                                                         using chatgpt,” in Twelfth International Symposium on Computing and
[142] C. Li, E. Wenger, Z. Allen-Zhu, F. Charton, and K. E. Lauter, “Salsa              Networking, CANDAR 2024 - Workshops, Naha, Japan, November
      verde: a machine learning attack on lwe with sparse small secrets,”               26-29, 2024. IEEE, 2024, pp. 307–313. [Online]. Available:
      Advances in Neural Information Processing Systems, vol. 36, 2024.                 https://doi.org/10.1109/CANDARW64572.2024.00057
[143] E. Wenger, M. Chen, F. Charton, and K. E. Lauter, “Salsa: Attacking         [162] Z. Tolba, M. Derdour, M. A. Ferrag, S. Muyeen, and M. Benbouzid,
      lattice cryptography with transformers,” Advances in Neural Informa-              “Automated deep learning black-box attack for multimedia p-box
      tion Processing Systems, vol. 35, pp. 34 981–34 994, 2022.                        security assessment,” IEEE Access, vol. 10, pp. 94 019–94 039, 2022.
[144] S. Boancă, “Exploring patterns and assessing the security of pseudo-       [163] Z. Zhang, W. Zhang, and H. Shi, “Genetic algorithm assisted state-
      random number generators with machine learning,” in Proceedings of                recovery attack on round-reduced xoodyak,” in Computer Security–
      the 16th International Conference on Agents and Artificial Intelligence           ESORICS 2021: 26th European Symposium on Research in Computer
      - Volume 3: ICAART, INSTICC. SciTePress, 2024, pp. 186–193.                       Security, Darmstadt, Germany, October 4–8, 2021, Proceedings, Part
[145] Z. Ebadi Ansaroudi, R. Zaccagnino, and P. Dâ C™Arco, “On pseudo-                 II 26. Springer, 2021, pp. 257–274.
      randomness and deep learning: A case study,” Applied Sciences, vol. 13,     [164] X. Zheng, Y. Li, C. Fan, H. Wu, X. Song, and J. Yan, “Learning
      p. 3372, 2023.                                                                    plaintext-ciphertext cryptographic problems via anf-based sat instance
[146] A. F. Al-Aboosi, M. Broner, and F. Y. Al-Aboosi, “Bingo: A semi-                  representation,” in The Thirty-eighth Annual Conference on Neural
      centralized password storage system,” Journal of Cybersecurity and                Information Processing Systems, 2024.
      Privacy, vol. 2, pp. 444–465, 2022.                                         [165] A. Benamira, D. Gerault, T. Peyrin, and Q. Q. Tan, “A deeper look
[147] H. T. Alaoui, A. Azouaoui, and J. El Kafi, “Artificial neural networks            at machine learning-based cryptanalysis,” in Advances in Cryptology–
      cryptanalysis of merkle-hellman knapsack cryptosystem,” in Interna-               EUROCRYPT 2021: 40th Annual International Conference on the The-
      tional Conference on Advanced Intelligent Systems for Sustainable                 ory and Applications of Cryptographic Techniques, Zagreb, Croatia,
      Development. Springer, 2022, pp. 196–205.                                         October 17–21, 2021, Proceedings, Part I 40. Springer, 2021, pp.
[148] S. Boanca, “Optimizations for learning from linear feedback shift                 805–835.
      register variations with artificial neural networks,” in Artificial         [166] Z. Bao, J. Guo, M. Liu, L. Ma, and Y. Tu, “Enhancing differential-
      Intelligence Applications and Innovations - 20th IFIP WG 12.5                     neural cryptanalysis,” in International Conference on the Theory and
      International Conference, AIAI 2024, Corfu, Greece, June 27-30,                   Application of Cryptology and Information Security. Springer, 2022,
      2024, Proceedings, Part IV, ser. IFIP Advances in Information                     pp. 318–347.
      and Communication Technology, I. Maglogiannis, L. S. Iliadis,               [167] N. Bacuieti, L. Batina, and S. Picek, “Deep neural networks aiding
      J. MacIntyre, M. Avlonitis, and A. Papaleonidas, Eds., vol.                       cryptanalysis: A case study of the speck distinguisher,” in Applied
      714. Springer, 2024, pp. 197–210. [Online]. Available: https:                     Cryptography and Network Security - 20th International Conference,
      //doi.org/10.1007/978-3-031-63223-5 15                                            ACNS 2022, Rome, Italy, June 20-23, 2022, Proceedings, ser. Lecture
[149] I. Dinur, O. Dunkelman, N. Keller, E. Ronen, and A. Shamir, “Efficient            Notes in Computer Science, G. Ateniese and D. Venturi, Eds.,
      detection of high probability statistical properties of cryptosystems via         vol. 13269. Springer, 2022, pp. 809–829. [Online]. Available:
      surrogate differentiation,” in Annual International Conference on the             https://doi.org/10.1007/978-3-031-09234-3 40
      Theory and Applications of Cryptographic Techniques. Springer, 2023,        [168] A. Baksi, J. Breier, V. A. Dasu, X. Hou, H. Kim, and H. Seo, “New
      pp. 98–127.                                                                       results on machine learning-based distinguishers,” IEEE Access, 2023.
[150] M. Duan, R. Zhou, C. Fu, S. Guo, and Q. Wu, “Vulnerability testing          [169] Z. Bao, J. Lu, Y. Yao, and L. Zhang, “More insight on deep learning-
      on the key scheduling algorithm of present using deep learning,” in               aided cryptanalysis,” in International Conference on the Theory and
      International Conference on Security and Privacy in New Computing                 Application of Cryptology and Information Security. Springer, 2023,
      Environments. Springer, 2021, pp. 307–318.                                        pp. 436–467.
[151] M. G. Perusheska, H. M. Trpceska, and V. Dimitrova, “Deep learning-         [170] A. Bose, D. Pal, and D. Roy Chowdhury, “Cryptographic distinguishers
      based cryptanalysis of different aes modes of operation,” in Future               through deep learning for lightweight block ciphers,” in International
                                                                                                                                                               27



      Conference on Applications and Techniques in Information Security.           [189] D. Lin, M. Li, Z. Hou, and S. Chen, “Conditional differential analysis
      Springer, 2024, pp. 47–63.                                                         on the katan ciphers based on deep learning,” IET Information Security,
[171] E. Bellini, M. Formenti, D. Gérault, J. Grados, A. Hambitzer, Y. J.               vol. 17, pp. 347–359, 2023.
      Huang, P. Huynh, M. Rachidi, R. Rohit, and S. K. Tiwari, “Claasp-            [190] J. Liu, J. Ren, and S. Chen, “A deep learning aided differential
      ing ARADI: automated analysis of the ARADI block cipher,” in                       distinguisher improvement framework with more lightweight and uni-
      Progress in Cryptology - INDOCRYPT 2024 - 25th International                       versality,” Cybersecurity, vol. 6, p. 47, 2023.
      Conference on Cryptology in India, Chennai, India, December 18-21,           [191] J. Liu, J. Ren, S. Chen, and M. Li, “Improved neural distinguishers with
      2024, Proceedings, Part II, ser. Lecture Notes in Computer Science,                multi-round and multi-splicing construction,” Journal of Information
      S. Mukhopadhyay and P. Stanica, Eds., vol. 15496. Springer, 2024,                  Security and Applications, vol. 74, p. 103461, 2023.
      pp. 90–113.                                                                  [192] J. Lu, G. Liu, B. Sun, C. Li, and L. Liu, “Improved (related-key)
[172] A. Bose, D. Pal, and D. R. Chowdhury, “Deep learning-based                         differential-based neural distinguishers for simon and simeck block
      differential distinguishers for cryptographic sequences,” in Progress              ciphers,” The Computer Journal, vol. 67, no. 2, pp. 537–547, 2024.
      in Cryptology - INDOCRYPT 2024 - 25th International Conference               [193] X. Li, J. Ren, and S. Chen, “Improved deep learning aided
      on Cryptology in India, Chennai, India, December 18-21, 2024,                      key recovery framework: applications to large-state block ciphers,”
      Proceedings, Part II, ser. Lecture Notes in Computer Science,                      Frontiers Inf. Technol. Electron. Eng., vol. 25, no. 10, pp. 1406–1420,
      S. Mukhopadhyay and P. Stanica, Eds., vol. 15496. Springer,                        2024. [Online]. Available: https://doi.org/10.1631/FITEE.2300848
      2024, pp. 114–133. [Online]. Available: https://doi.org/10.1007/             [194] G. Lv, C. Jin, Z. Shi, and T. Cui, “Approximating neural
      978-3-031-80311-6 6                                                                distinguishers using differential-linear imbalance,” J. Supercomput.,
[173] Y. Chen, Y. Shen, and H. Yu, “Neural-aided statistical attack for                  vol. 80, no. 19, pp. 26 865–26 889, 2024. [Online]. Available:
      cryptanalysis,” The Computer Journal, vol. 66, pp. 2480–2498, 2023.                https://doi.org/10.1007/s11227-024-06375-4
[174] Y. Chen, Y. Shen, H. Yu, and S. Yuan, “A new neural distinguisher            [195] G. Mishra, S. Pal, S. Krishna Murthy, I. Prakash, and A. Kumar, “Deep
      considering features derived from multiple ciphertext pairs,” The Com-             learning-based differential distinguisher for lightweight ciphers gift-64
      puter Journal, vol. 66, pp. 1419–1433, 2023.                                       and pride,” in Machine Intelligence and Smart Systems: Proceedings
[175] H. Deng, X. Cao, and Y. Cheng, “Attention in differential cryptanalysis            of MISS 2021. Springer, 2022, pp. 245–257.
      on lightweight block cipher speck,” in 2023 20th Annual International        [196] R. C.-W. Phan, A. Pal, K. Wong, and S. Rajanala, “CηιDAE: Cryp-
      Conference on Privacy, Security and Trust (PST). IEEE, 2023, pp.                   tographically distinguishing autoencoder for cipher cryptanalysis,” in
      1–9.                                                                               GLOBECOM 2023-2023 IEEE Global Communications Conference.
[176] A. Ebrahimi, F. Regazzoni, and P. Palmieri, “Reducing the cost of                  IEEE, 2023, pp. 4467–4472.
      machine learning differential attacks using bit selection and a partial      [197] Pooja, Shantanu, and G. Mishra, “Related-key neural distinguisher
      ml-distinguisher,” in International Symposium on Foundations and                   for round-reduced present cipher,” in International Conference on
      Practice of Security. Springer, 2022, pp. 123–141.                                 Advances in Data-driven Computing and Intelligent Systems. Springer,
[177] A. Ebrahimi, D. Gerault, and P. Palmieri, “Deep learning-based                     2023, pp. 393–405.
      rotational-xor distinguishers for and-rx block ciphers: Evaluations on       [198] D. Pal, M. Chaudhury, A. Das, and D. R. Chowdhury, “Deep learning-
      simeck and simon,” in International Conference on Selected Areas in                based differential distinguishers for nist standard authenticated encryp-
      Cryptography. Springer, 2023, pp. 429–450.                                         tion and permutations,” in International Conference on Mathematics
                                                                                         and Computing. Springer, 2024, pp. 1–13.
[178] Y.-T. Goi, S.-M. Leong, R. C.-W. Phan, S. Lai, and A. Sălăgean,
      “Unveiling the black box: Neural cryptanalysis with xai,” in 2024 IEEE       [199] R. Rajan, R. K. Roy, D. Sen, and G. Mishra, “Deep learning-based
      International Conference on Systems, Man, and Cybernetics (SMC).                   differential distinguisher for lightweight cipher gift-cofb,” in Machine
                                                                                         Intelligence and Smart Systems: Proceedings of MISS 2021. Springer,
      IEEE, 2024, pp. 1951–1956.
                                                                                         2022, pp. 397–406.
[179] Z. Hou, J. Ren, and S. Chen, “Improve neural distinguishers of simon
                                                                                   [200] V. Rajakumar, K. Lakshmy, and C. Srinivasan, “Deep learning based
      and speck,” Security and Communication Networks, vol. 2021, pp. 1–
                                                                                         cryptanalysis on slim cipher,” in 2023 3rd International Conference on
      11, 2021.
                                                                                         Innovative Sustainable Computational Technologies (CISCT). IEEE,
[180] A. Hambitzer, D. Gerault, Y. J. Huang, N. Aaraj, and E. Bellini,                   2023, pp. 1–6.
      “Nnbits: Bit profiling with a deep learning ensemble based dis-              [201] H.-C. Su, X.-Y. Zhu, and D. Ming, “Polytopic attack on round-
      tinguisher,” in CryptographersâC™ Track at the RSA Conference.                    reduced simon32/64 using deep learning,” in Information Security and
      Springer, 2023, pp. 493–523.                                                       Cryptology: 16th International Conference, Inscrypt 2020, Guangzhou,
[181] Z. Hou, J. Ren, and S. Chen, “Practical attacks of round-reduced simon             China, December 11–14, 2020, Revised Selected Papers. Springer,
      based on deep learning,” The Computer Journal, vol. 66, pp. 2517–                  2021, pp. 3–20.
      2534, 2023.                                                                  [202] A. Sajwan and G. Mishra, “Comparative analysis of resnet and densenet
[182] T. Huang, Y. Li, Q. Fu, Y. Chen, and L. Song, “Improving differential-             for differential cryptanalysis of speck 32/64 lightweight block cipher,”
      neural cryptanalysis for large-state SPECK,” in Information and                    in International Conference on Cryptology & Network Security with
      Communications Security - 26th International Conference, ICICS 2024,               Machine Learning. Springer, 2023, pp. 495–504.
      Mytilene, Greece, August 26-28, 2024, Proceedings, Part I, ser. Lecture      [203] B. Seok, D. Chang, and C. Lee, “A novel approach to construct a
      Notes in Computer Science, S. K. Katsikas, C. Xenakis, C. Kalloniatis,             good dataset for differential-neural cryptanalysis,” IEEE Transactions
      and C. Lambrinoudakis, Eds., vol. 15056. Springer, 2024, pp. 40–57.                on Dependable and Secure Computing, 2024.
      [Online]. Available: https://doi.org/10.1007/978-981-97-8798-2 3             [204] D. Shen, Y. Song, Y. Lu, S. Long, and S. Tian, “Neural differential
[183] Y. Hu, L. Li, S. Zhu, and Z. Hu, “Enhancing neural distinguishers with             distinguishers for gift-128 and ascon,” Journal of Information Security
      partial difference bits leakage,” Internet Things, vol. 29, p. 101438,             and Applications, vol. 82, p. 103758, 2024.
      2025. [Online]. Available: https://doi.org/10.1016/j.iot.2024.101438         [205] A. Sarkar, M. Bhattacharyya, U. Garain, S. K. Pal, S. Shantanu,
[184] H. Kim, K. Jang, S. Lim, Y. Kang, W. Kim, and H. Seo, “Quantum                     S. Bandyopadhyay, and N. R. Pal, “Leveraging synergy to design
      neural network based distinguisher on speck-32/64,” Sensors, vol. 23,              neural differential distinguishers for lightweight block ciphers,” IEEE
      p. 5683, 2023.                                                                     Transactions on Emerging Topics in Computational Intelligence, 2024.
[185] D. Kim, H. Kim, K. Jang, S. Yoon, and H. Seo, “Deep-learning-based           [206] W. Tian and B. Hu, “Deep learning assisted differential cryptanalysis
      neural distinguisher for format-preserving encryption schemes ff1 and              for the lightweight cipher simon.” KSII Transactions on Internet &
      ff3,” Electronics, vol. 13, no. 7, p. 1196, 2024.                                  Information Systems, vol. 15, 2021.
[186] D. Lin, S. Chen, M. Li, and Z. Hou, “The construction and application        [207] W. J. Teng, J. S. Teh, and N. Jamil, “On the security of lightweight
      of (related-key) conditional differential neural distinguishers on katan,”         block ciphers against neural distinguishers: Observations on lbc-iot and
      in International Conference on Cryptology and Network Security.                    slim,” Journal of Information Security and Applications, vol. 76, p.
      Springer, 2022, pp. 203–224.                                                       103531, 2023.
[187] L. Lyu, Y. Tu, and Y. Zhang, “Deep learning assisted key recovery            [208] E. Tcydenova, B. Seok, and C. Lee, “Related-key neural distinguisher
      attack for round-reduced simeck32/64,” in International Conference                 on block ciphers speck-32/64, hight and gost,” Journal of Platform
      on Information Security. Springer, 2022, pp. 443–463.                              Technology, vol. 11, no. 1, pp. 72–84, 2023.
[188] ——, “Improving the deep-learning-based differential distinguisher and        [209] G. Wang and G. Wang, “Improved differential-ml distinguisher: ma-
      applications to simeck,” in 2022 IEEE 25th International Conference                chine learning based generic extension for differential analysis,” in In-
      on Computer Supported Cooperative Work in Design (CSCWD). IEEE,                    ternational Conference on Information and Communications Security.
      2022, pp. 465–470.                                                                 Springer, 2021, pp. 21–38.
                                                                                                                                                            28



[210] G. Wang, G. Wang, and Y. He, “Improved machine learning assisted           [231] C. Blondeau and B. Gérard, “Multiple differential cryptanalysis: theory
      (related-key) differential distinguishers for lightweight ciphers,” in           and practice,” in International Workshop on Fast Software Encryption.
      2021 IEEE 20th International Conference on Trust, Security and                   Springer, 2011, pp. 35–54.
      Privacy in Computing and Communications (TrustCom). IEEE, 2021,            [232] A. Gohr, “Improving attacks on round-reduced speck32/64 using deep
      pp. 164–171.                                                                     learning,” in Advances in Cryptology – CRYPTO 2019, A. Boldyreva
[211] H. Wang, J. Tian, X. Zhang, Y. Wei, and H. Jiang, “Multiple differential         and D. Micciancio, Eds. Cham: Springer International Publishing,
      distinguisher of simeck32/64 based on deep learning.” Security &                 2019, pp. 150–179.
      Communication Networks, 2022.                                              [233] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess,
[212] Z. Wu, K. Qiao, Z. Wang, J. Cheng, and L. Zhu, “Mixture differential             R. Child, S. Gray, A. Radford, J. Wu, and D. Amodei, “Scaling laws
      cryptanalysis on round-reduced simon32/64 using machine learning,”               for neural language models,” arXiv preprint arXiv:2001.08361, 2020.
      Mathematics, vol. 12, no. 9, p. 1401, 2024.                                [234] T. G. Dietterich, R. H. Lathrop, and T. Lozano-Pérez, “Solving the
[213] G. Wang and G. Wang, “Keeping classical distinguisher and neural                 multiple instance problem with axis-parallel rectangles,” Artificial
      distinguisher in balance,” J. Inf. Secur. Appl., vol. 84, p. 103816,             Intelligence, vol. 89, no. 1, pp. 31–71, 1997. [Online]. Available:
      2024. [Online]. Available: https://doi.org/10.1016/j.jisa.2024.103816            https://www.sciencedirect.com/science/article/pii/S0004370296000343
[214] G. Wang, G. Wang, and S. Sun, “A new (related-key) neural                  [235] S. Andrews, I. Tsochantaridis, and T. Hofmann, “Support vector ma-
      distinguisher using two differences for differential cryptanalysis,”             chines for multiple-instance learning,” Advances in Neural Information
      IET Inf. Secur., vol. 2024, no. 1, 2024. [Online]. Available:                    Processing Systems, vol. 15, pp. 561–568, 01 2002.
      https://doi.org/10.1049/2024/4097586                                       [236] M. Ilse, J. Tomczak, and M. Welling, “Attention-based deep multiple
[215] G. Wang and G. Wang, “Enhanced related-key differential neural                   instance learning,” in Proceedings of the 35th International Conference
      distinguishers for SIMON and SIMECK block ciphers,” PeerJ                        on Machine Learning, ser. Proceedings of Machine Learning Research,
      Comput. Sci., vol. 10, p. e2566, 2024. [Online]. Available:                      J. Dy and A. Krause, Eds., vol. 80. PMLR, 10–15 Jul 2018,
      https://doi.org/10.7717/peerj-cs.2566                                            pp. 2127–2136. [Online]. Available: https://proceedings.mlr.press/v80/
[216] T. Yadav and M. Kumar, “Differential-ml distinguisher: Machine                   ilse18a.html
      learning based generic extension for differential cryptanalysis,” in       [237] L. Ruff, R. Vandermeulen, N. Goernitz, L. Deecke, S. A. Siddiqui,
      International Conference on Cryptology and Information Security in               A. Binder, E. Müller, and M. Kloft, “Deep one-class classification,”
      Latin America. Springer, 2021, pp. 191–212.                                      in Proceedings of the 35th International Conference on Machine
[217] X. Yue and W. Wu, “Improved neural differential distinguisher model              Learning, ser. Proceedings of Machine Learning Research, J. Dy and
      for lightweight cipher speck,” Applied Sciences, vol. 13, p. 6994, 2023.         A. Krause, Eds., vol. 80. PMLR, 10–15 Jul 2018, pp. 4393–4402.
[218] T. Yadav and M. Kumar, “ML based improved differential distinguisher             [Online]. Available: https://proceedings.mlr.press/v80/ruff18a.html
      with high accuracy: Application to GIFT-128 and ASCON,”                    [238] S. Kalra, M. Adnan, G. Taylor, and H. R. Tizhoosh, “Learning permu-
      in Security, Privacy, and Applied Cryptography Engineering -                     tation invariant representations using memory networks,” in Computer
      14th International Conference, SPACE 2024, Kottayam, India,                      Vision – ECCV 2020, A. Vedaldi, H. Bischof, T. Brox, and J.-M. Frahm,
      December 14-17, 2024, Proceedings, ser. Lecture Notes in Computer                Eds. Cham: Springer International Publishing, 2020, pp. 677–693.
      Science, J. Knechtel, U. Chatterjee, and D. Forte, Eds., vol.              [239] M. Tan and Q. V. Le, “Efficientnet: Rethinking model scaling
      15351. Springer, 2024, pp. 287–316. [Online]. Available: https:                  for convolutional neural networks,” in Proceedings of the 36th
      //doi.org/10.1007/978-3-031-80408-3 18                                           International Conference on Machine Learning, ICML 2019, 9-15
[219] S. Zhu, L. Li, Z. Hu, and Y. Hu, “Bcs: A neural distinguisher method             June 2019, Long Beach, California, USA, ser. Proceedings of
      based on differential propagation uncertainty of nonlinear components            Machine Learning Research, K. Chaudhuri and R. Salakhutdinov,
      and network adaptability,” Physica Scripta, 2025.                                Eds., vol. 97. PMLR, 2019, pp. 6105–6114. [Online]. Available:
                                                                                       http://proceedings.mlr.press/v97/tan19a.html
[220] R. Zhang, M. Zhang, J. Yan, Y. Li, X. Wu, and L. Li, “Differential
                                                                                 [240] Epoch AI, “Parameter, compute and data trends in machine
      cryptanalysis of twegift-128 based on neural network,” in 2021 IEEE
                                                                                       learning,” 2024, accessed: 2024-05-31. [Online]. Available: https:
      Sixth International Conference on Data Science in Cyberspace (DSC).
                                                                                       //epochai.org/data/epochdb/visualization
      IEEE, 2021, pp. 529–534.
                                                                                 [241] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. Reed, D. Anguelov,
[221] W. Zhang and Y. Zhao, “Ensemble learning-based differential dis-
                                                                                       D. Erhan, V. Vanhoucke, and A. Rabinovich, “Going deeper with
      tinguishers for lightweight cipher,” in Proceedings of the 2021 5th
                                                                                       convolutions,” in Proceedings of the IEEE conference on computer
      International Conference on Electronic Information Technology and
                                                                                       vision and pattern recognition, 2015, pp. 1–9.
      Computer Engineering, 2021, pp. 28–34.
                                                                                 [242] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image
[222] L. Zhang, J. Lu, Z. Wang, and C. Li, “Improved differential-neural               recognition,” in Proceedings of the IEEE conference on computer vision
      cryptanalysis for round-reduced simeck32/64,” Frontiers of Computer              and pattern recognition, 2016, pp. 770–778.
      Science, vol. 17, no. 6, p. 176817, 2023.                                  [243] J. Hu, L. Shen, and G. Sun, “Squeeze-and-excitation networks,” in
[223] L. Zhang, Z. Wang, and Y. Chen, “Improving the accuracy of                       Proceedings of the IEEE conference on computer vision and pattern
      differential-neural distinguisher for des, chaskey, and present,” IEICE          recognition, 2018, pp. 7132–7141.
      TRANSACTIONS on Information and Systems, vol. 106, pp. 1240–               [244] S. Makridakis, E. Spiliotis, and V. Assimakopoulos, “The M4 Compe-
      1243, 2023.                                                                      tition: 100,000 time series and 61 forecasting methods,” International
[224] L. Zhang, Z. Wang, and B. Wang, “Improving differential-neural                   Journal of Forecasting, vol. 36, no. 1, pp. 54–74, 2020.
      cryptanalysis,” IACR Commun. Cryptol., vol. 1, no. 3, p. 13, 2024.         [245] O. Russakovsky, J. Deng, H. Su, J. Krause, S. Satheesh, S. Ma,
      [Online]. Available: https://doi.org/10.62056/ay11wa3y6                          Z. Huang, A. Karpathy, A. Khosla, M. Bernstein, A. C. Berg, and
[225] L. Zhang, Z. Wang, and J. Lu, “Differential-neural cryptanalysis on              L. Fei-Fei, “ImageNet Large Scale Visual Recognition Challenge,”
      AES,” IEICE Trans. Inf. Syst., vol. 107, no. 10, pp. 1372–1375, 2024.            International Journal of Computer Vision (IJCV), vol. 115, no. 3, pp.
      [Online]. Available: https://doi.org/10.1587/transinf.2024edl8044                211–252, 2015.
[226] D. Gunning, E. Vorm, Y. Wang, and M. Turek, “Darpa’s explainable           [246] D. Hong, J.-K. Lee, D.-C. Kim, D. Kwon, K. H. Ryu, and D.-G.
      ai (xai) program: A retrospective,” Authorea Preprints, 2021.                    Lee, “Lea: A 128-bit block cipher for fast encryption on common
[227] D. Gunning and D. Aha, “Darpa’s explainable artificial intelligence              processors,” in Information Security Applications, Y. Kim, H. Lee, and
      (xai) program,” AI Magazine, vol. 40, no. 2, pp. 44–58, Jun.                     A. Perrig, Eds. Cham: Springer International Publishing, 2014, pp.
      2019. [Online]. Available: https://ojs.aaai.org/aimagazine/index.php/            3–27.
      aimagazine/article/view/2850                                               [247] M. Wang, “Differential cryptanalysis of present,” IACR Cryptol. ePrint
[228] V. Hassija, V. Chamola, A. Mahapatra, A. Singal, D. Goel, K. Huang,              Arch., vol. 2007, p. 408, 2007.
      S. Scardapane, I. Spinelli, M. Mahmud, and A. Hussain, “Interpreting
      black-box models: a review on explainable artificial intelligence,”
      Cognitive Computation, vol. 16, no. 1, pp. 45–74, 2024.                                                    A PPENDIX
[229] I. Hameed, S. Sharpe, D. Barcklow, J. Au-Yeung, S. Verma, J. Huang,
      B. Barr, and C. B. Bruss, “Based-xai: Breaking ablation studies down       A. Comparative Review of the remaining Neural Differential
      for explainable artificial intelligence,” 2022.                            Distinguishers
[230] J. An, Y. Lai, and Y. Han, “Logic rule guided attribution with
      dynamic ablation,” in Proceedings of the AAAI Conference on Artificial       1) AES: AES is a widely used block cipher standardized
      Intelligence, vol. 36, no. 1, 2022, pp. 77–85.                             by NIST in 2001, designed for general-purpose encryption
                                                                                                                                                       29



                                                                 TABLE IV
                                       OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR AES.

    Primitive         Arch.                   Class                 Trn.         Val.        AutoND            Rounds          Acc.            Ref.
    AES-128           N D Gohr                2-1-CTtr -R           20M          2M               -            2               0.9981          [225]
                      N D Gohr                2-1-CT-R              20M          2M               -            2               1               [225]
 Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
 n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
 manually designed training procedure (-).
 RK
    Related key setting.



applications. It operates on 128-bit blocks and supports key                  block sizes of 32 and 128 bits and key sizes of 128 bits. We
sizes of 128, 192, or 256 bits. The cipher’s structure com-                   use the notations FFX-D when the domain is digits and FFX-L
prises 10, 12, or 14 rounds (depending on the key size),                      when the domain is lowercase characters.
each involving four transformations: SubBytes (substitution),                     In [185]† , the authors performed neural cryptanalysis of FF1
ShiftRows (permutation), MixColumns (linear mixing), and                      and FF3 for digits (FFX-D) and lowercase letters (FFX-L). We
AddRoundKey. Notably, AES’s SubBytes transformation uses                      report the best results in the 2-1-CT-R setting, but note that
a single 8-bit S-box followed by an affine transformation.                    the authors additionally performed experiments in the m-2-
   Zhang et al. [225] developed neural distinguishers targeting               CT-D setting with similar, yet not directly comparable, results.
a 2-round reduced version of AES-128, specifically using only                 Experiments were conducted for the classification of up to 15
one pair of bytes from the ciphertext.                                        input differences. However, it is not immediately clear which
   2) ARADI: ARADI is a low-latency block cipher intro-                       results are the best. The number of samples for training and
duced by the NSA in 2024, specifically designed for memory                    testing was not specified, nor is the source code available.
encryption applications. It operates on 128-bit blocks and                        7) GIFT: GIFT is a PRESENT-inspired SPN cipher, using
utilizes a 256-bit key. The cipher’s structure comprises 16                   128-bit keys to encrypt 64-bit (GIFT64) or 128-bit (GIFT128)
rounds, each involving a combination of substitution and                      blocks for 28 and 40 rounds, respectively. GIFT was one of the
permutation operations. Notably, ARADI’s round function                       finalists of the NIST Lightweight Cryptography Competition.
employs a unique S-box, a linear layer, and a key addition                        In [220]† , the authors claimed a distinguisher on 7 rounds
layer.                                                                        because the training accuracy was 0.6487, despite the valida-
   3) ASCON: ASCON is an SPN-based permutation with an                        tion accuracy being non-significant (0.5002); in the table, we
input size of 320 bits. It can be used within a sponge con-                   report this 7 rounds distinguisher as it is the best one claimed
struction to build the authenticated ciphers ASCON-128 and                    by the authors, but also their 6-round distinguisher, which has
ASCON-128a, both using 128-bit keys and 12 rounds in the                      a significant validation accuracy.
initialization, and respectively 64 and 128-bit messages, and                     In [195]† , the authors claimed a full round distinguisher
6 and 8 rounds in the encryption process. The hash function                   on GIFT-64 with over 90% accuracy, using 220 samples
ASCON-hash, also based on sponge construction, hashes 64-                     in total, of which 15% are kept for validation, respectively
bit messages over 12 rounds. ASCON was announced as the                       testing, and a MLP architecture; they also claimed a full
winner of the NIST Lightweight Cryptography Competition in                    round distinguisher on PRIDE with 100% accuracy. Full-round
February 2023.                                                                attacks on modern and reputable ciphers are an extraordinary
                                                                              claim and require extraordinary evidence, which the author’s
   Shen et al. [204] trained neural differential distinguishers
                                                                              manuscript does not provide.
for the 4-round ASCON with an accuracy of 0.5069 in the
                                                                                  In [199]† , only 10K samples were used for training and
standard setting and were able to improve the accuracy to
                                                                              testing; as a result, the distinguishers exhibit significant over-
0.6925 by training another neural network to classify based
                                                                              fitting (e.g., 92% training accuracy and 25% test accuracy for
on the distribution of multiple scores. We do not include
                                                                              M1 on 6 rounds).
this result in the table, as it is a system where the neural
                                                                                  8) GIMLI: GIMLI is a 24-round permutation acting on
distinguisher part is run separately on single pairs rather than
                                                                              384 bits, from which a hash function GIMLI-HASH and an
a neural distinguisher accepting multiple pairs.
                                                                              authenticated cipher GIMLI-CIPHER are derived.
   4) CHASKEY: CHASKEY is an ARX-based permutation                                9) GOST: GOST is a block cipher developed by the Soviet
with an input size of 128 bits. It operates through 8 rounds of               Union. It operates on 64-bit blocks with a 256-bit key and
Addition, Rotation, and XOR operations on four 32-bit words                   follows a Feistel network structure with 32 rounds. Each
   5) DES: DES (Data Encryption Standard) is a 16-round                       round applies a key-dependent substitution using fixed S-
SPN block cipher working with 56-bit keys and 64-bit blocks.                  boxes, followed by modular addition and bitwise rotations to
   Zhang et al. [223] used a staged training approach to obtain               ensure diffusion and security.
a distinguisher for 7-round DES: 4·107 samples, 16 pairs each                     10) HIGHT: HIGHT is a 32-round ARX-based block ci-
(640M ciphertext pairs).                                                      pher operating on 64-bit blocks and 128-bit keys.
   6) FF1 and FF3: FF1 and FF3 are format-preserving                              Seok et al. [19] achieved a distinguishing accuracy of 0.5707
encryption algorithms, with 10 and 8 rounds, respectively, with               on 10-round HEIGHT by analyzing only half of the ciphertext
                                                                                                                                                               30



                                                                    TABLE V
                                        OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR ARADI.

    Primitive               Arch.                   Class                 Trn.         Val.        AutoND            Rounds           Acc.            Ref.
    ARADI                   N D Gohr                2-1-CT-R              20M          2M              ✓             5                0.5954          [123]
    ARADI RK                N D Gohr                2-1-CT-R              20M          2M              ✓             6                0.5631          [123]
 Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
 n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
 manually designed training procedure (-).
 RK
    Related key setting.

                                                                    TABLE VI
                                        OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR ASCON.

    Primitive                      Arch.                  Class            Trn.         Val.          AutoND          Rounds          Acc.           Ref.
    ASCON                          MLP                    3-2-δ-D          1.1M         1.1M                -         3               0.9861         [22]
                                   MLP                    2-1-δ-R          17M          2M                  -         4               0.502          [218]
                                   MLP                    2-1-δ-R          20M          20M                 -         4               0.5069         [204]
    ASCONUnkeyed                   Classical ML           2-2-δ-D          64K          16K                 -         3               0.916          [168]‡
  Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
  n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
  manually designed training procedure (-).
 ‡ The use of a small validation set raises concerns about the statistical robustness, reproducibility, and generalizability of the results, as such datasets are
  prone to high variance and may not reliably reflect model performance.

                                                                   TABLE VII
                                      OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR CHASKEY.

   Primitive                                 Arch.              Class               Trn.       Val.         AutoND        Rounds         Acc.          Ref.
   CHASKEY-PERMUTATION                       N D Gohr           2-1-CT-R            17M        40K              -         4              0.6161        [22]‡
                                             N D Gohr           32-1-CT-R           20M        2M               -         4              0.7712        [174]
                                             INC                16-1-CT-R           60M        2M               -         5              0.5181        [223]
   Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out
   settings n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an
   elaborate, manually designed training procedure (-).
 ‡ The use of a small validation set raises concerns about the statistical robustness, reproducibility, and generalizability of the results, as such datasets are
   prone to high variance and may not reliably reflect model performance.

                                                                   TABLE VIII
                                          OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR DES.

    Primitive          Arch.                   Class                  Trn.            Val.         AutoND            Rounds            Acc.           Ref.
    DES                N D Gohr                2-1-CT-R               20M             2M                -            5                 0.58           [173]
                       N D Gohr                4-1-CT-R               20M             2M                -            6                 0.5653         [174]
                       INC                     32-1-CT-R              1280M           32M               -            7                 0.5114         [223]
  Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
  n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
  manually designed training procedure (-).



difference (4 out of 8 bytes). These specific bytes were selected                 inconsistencies, independent verification is necessary before
through their analysis of the HIGHT round function.                               accepting these anomalous results. We report the best distin-
                                                                                  guishers with statistical significance at the 95% confidence
   Bose et al. [172]† claimed advancements in distinguishing                      level (z-scores > 1.96, p < 0.05), corresponding to accuracies
additional encryption rounds through sequential model training                    above 0.5011 on a test set of 5 × 106 samples.
on ciphertext pairs. However, these findings contradict estab-
lished cryptographic theory, which shows distinguishability                          11) KATAN: KATAN is a family of FSR-based block
decreases monotonically with increasing rounds; a pattern                         ciphers with block sizes 32, 48, or 64, key size 80, and 254
absent in their results. Notably, Bellini et al. [42] reported                    rounds.
superior distinguishers for rounds 9 and 10 of HIGHT, chal-                          For KATAN32, [42] reached statistically significant accu-
lenging the purported architecture’s effectiveness in detecting                   racies up to 69 rounds in an automatically generated distin-
differential patterns. Given these theoretical and empirical                      guisher, and noted that this can be improved to a 71-round
                                                                                                                                                        31



                                                                  TABLE IX
                                         OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR FF.


    Primitive             Arch.          Class                Trn.          Val.          AutoND             Rounds             Acc.           Ref.

    FF1-D                 MLP            2-1-CT-R             /             /                  -             10                 0.855          [185]†
    FF1-L                 MLP            2-1-CT-R             /             /                  -             2                  0.522          [185]†

    FF3-D                 MLP            2-1-CT-R             /             /                  -             8                  0.977          [185]†
    FF3-L                 MLP            2-1-CT-R             /             /                  -             2                  0.554          [185]†
   Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
   n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
   manually designed training procedure (-).
 † A critical discussion of these results is provided in the text.
 / Unknown quantity.



                                                                   TABLE X
                                        OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR GIFT.

    Primitive               Arch.           Class                 Trn.          Val.          AutoND             Rounds          Acc.           Ref.

    GIFT-64                 UNet            12-1-A-R              /             /                  -             4               0.725          [219]†
                            LSTM            3-2-CT-R              17M           4M                 -             6               0.5754         [21]
                            MLP             2-1-δ-R               2.1M          300K               -             FULL            0.96           [195]†
    GIFT-128                MLP             2-1-δ-R               17M           2M                 -             7               0.55           [218]
                            MLP             2-1-δ-R               20M           2M                 -             7               0.5542         [204]
    TweGIFT-128             MLP             2-1-CT-R              2M            200K               -             6               0.5675         [220]
                            MLP             2-1-CT-R              2M            200K               -             7               0.5002         [220]†

    GIFT-COFB               MLP             2-4-δ-D               20K           20K                -             4               0.615          [199]†
   Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
   n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
   manually designed training procedure (-).
 / Unknown quantity.
 † A critical discussion of these results is provided in the text.




distinguisher with 0.5034±0.0002 accuracy using their simple                    characteristic with probability 2−98 for 11 rounds, and 2−128
polishing step. In contrast, [186] reached 51 rounds in the                     for 12 rounds.
standard setting and 59 when using 64 pairs.                                       Bose et al. [172]† claimed advancements in distinguishing
   In [186], practical key recoveries were obtained for 125, 106                additional encryption rounds through sequential model training
and 95 rounds respectively, in the related key scenario. Single-                on ciphertext pairs. However, these findings contradict estab-
key conditional neural distinguishers were also mentioned                       lished cryptographic theory, which shows distinguishability
in [186] for 85, 72 and 61 rounds respectively, but the r + s                   decreases monotonically with increasing rounds – a pattern
decomposition was not explicitly mentioned so we omit them                      absent in their results. Notably, Bellini et al. [42] reported
in the table.                                                                   superior distinguishers for rounds 9 and 10 of HIGHT, chal-
   12) KNOT: KNOT is an SPN-based permutation acting on                         lenging the purported architecture’s effectiveness in detecting
a 256, 384, or 512-bit state; when used in a MonkeyDuplex                       differential patterns. Given these theoretical and empirical
construction to build a cipher, it uses 28 to 52 rounds,                        inconsistencies, independent verification is necessary before
depending on the version.                                                       accepting these anomalous results. We report the best distin-
   13) LBCIoT: LBCIoT is a 32-round block cipher encrypt-                       guishers with statistical significance at the 95% confidence
ing 32-bit plaintexts with an 80-bit key. In [207], the authors                 level (z-scores > 1.96, p < 0.05), corresponding to accuracies
propose a neural distinguisher on 7 rounds and build a practical                above 0.5011 on a test set of 5 × 106 samples.
key recovery attack for 8 rounds.                                                  15) PRESENT: PRESENT is an SPN-based block cipher,
   14) LEA: LEA is an ARX-based block cipher, encrypting                        encrypting 64-bit blocks with 80 (PRESENT-80) or 128-bit
128-bit plaintexts with 128-, 192-, or 256-bit keys for 24, 28,                 keys (PRESENT-128) for 31 rounds.
or 32 rounds, respectively.                                                        In [42], a 9-round distinguisher with an accuracy of 0.5092
   For LEA, [42] proposes the first neural differential distin-                 was given, which favorably compares to the 7-round distin-
guisher, reaching 11 rounds with accuracy 0.5109. In com-                       guishers of [174], despite [174] using four pairs per sample.
parison, the proposal of LEA [246] presents a differential                      On the other hand, [73] obtained a slightly higher accuracy
                                                                                                                                                             32



                                                                   TABLE XI
                                       OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR GIMLI.

   Primitive                   Arch.             Class                 Trn.          Val.        AutoND             Rounds           Acc.            Ref.
   GIMLI                       DBitNet           2-1-CT-R              20M           2M              ✓              11               0.524           [42]

   GIMLI-HASH                  MLP               3-2-δ-D               400K          40K              -             8                0.5219          [22]‡

   GIMLI-CIPHER                MLP               3-2-δ-D               400K          40K              -             8                0.5099          [22]‡
 Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
 n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
 manually designed training procedure (-).
‡ The use of a small validation set raises concerns about the statistical robustness, reproducibility, and generalizability of the results, as such datasets are
 prone to high variance and may not reliably reflect model performance.

                                                                   TABLE XII
                                        OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR GOST.

   Primitive             Arch.                    Class                Trn.         Val.          AutoND            Rounds           Acc.            Ref.
   GOST                  N D Gohr                 2-1-CT-R             2M           200K               -            9                0.5430          [208]
   GOST RK               N D Gohr                 2-1-CT-R             2M           200K               -            14               0.7134          [208]
 Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
 n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
 manually designed training procedure (-).
 RK
    Related key setting.

                                                                  TABLE XIII
                                       OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR HIGHT.

   Primitive              Arch.                   Class                Trn.         Val.          AutoND            Rounds           Acc.           Ref.
   HIGHT                  N D Gohr                2-1-CT-R             2M           200K              -             9                0.7472         [208]
                          N D Gohr                2-1-δtr -R           20M          2M                -             10               0.5707         [19]
                          DBitNet                 2-1-CT-R             20M          2M                ✓             10               0.751          [42]
                          N D Gohr                2-1-CT-R             2M           200K              -             11               0.7472         [208]
                          LSTM                    2-1-A-R              10M          500K              -             15               0.5015         [172] †
   HIGHT RK               DBitNet                 2-1-CT-R             20M          2M                ✓             14               0.563          [42]
                          DenseNet                2-2-CT-D             20M          2M                ✓             14               0.640          [214]
 Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
 n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
 manually designed training procedure (-).
RK
    Related key setting.
† A critical discussion of these results is provided in the text.




at the cost of using 32 ciphertexts per sample. In comparison,                   above 0.5011 on a test set of 5 × 106 samples.
the best differential characteristic for PRESENT reduced to 9                       16) PRIDE: PRIDE is a 20-round SPN cipher using 64-bit
rounds has probability 2−36 [247].                                               blocks and 128-bit keys.
                                                                                 In [195], the authors claimed a full-round distinguisher on the
   Bose et al. [172]† claimed advancements in distinguishing
                                                                                 cipher with 100% accuracy, which seems likely to be attributed
additional encryption rounds through sequential model training
                                                                                 to a methodology issue rather than an actual break, as perfect
on ciphertext pairs. However, these findings contradict estab-
                                                                                 accuracy is often a sign of overfitting, especially considering
lished cryptographic theory, which shows distinguishability
                                                                                 the lack of evidence provided in the paper.
decreases monotonically with increasing rounds – a pattern
absent in their results. Notably, Bellini et al. [42] reported                      17) SHA3: SHA3-256 is a 24-round sponge-based hash
superior distinguishers for rounds 9 and 10 of HIGHT, chal-                      function with an output size of 256.
lenging the purported architecture’s effectiveness in detecting                     18) SKINNY: SKINNY is an SPN-based block cipher;
differential patterns. Given these theoretical and empirical                     SKINNY128 processes 128-bit plaintexts with 128, 256, and
inconsistencies, independent verification is necessary before                    384-bit keys for 40, 48, and 56 rounds, respectively.
accepting these anomalous results. We report the best distin-
guishers with statistical significance at the 95% confidence                        19) SLIM: SLIM is a 32-round block cipher encrypting 32-
level (z-scores > 1.96, p < 0.05), corresponding to accuracies                   bit plaintexts with an 80-bit key.
                                                                                                                                                              33



                                                                   TABLE XIV
                                        OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR KATAN.

   Primitive                     Arch.               Class               Trn.             Val.         AutoND           Rounds           Acc.         Ref.
   KATAN32                       N D Gohr            2-1-δ-R             20M              2M              -             51               0.533        [186]
                                 N D Gohr            128-1-δ-R           1280M            128M            -             59               0.575        [186]
                                 DBitNet             2-1-CT-R            20M              2M             ✓              69               0.505        [42]
   KATAN32 C                     N D Gohr            64-1-δ-R            64M              6.4M            -             58               0.602        [189]
                                 N D Gohr            128-1-δ-R           1280M            128M            -             85               0.570        [186]
   KATAN32 RK,C                  N D Gohr            128-1-δ-R           1280M            128M            -             112              0.647        [186]
   KATAN48                       N D Gohr            2-1-δ-R             20M              2M                -           40               0.58         [186]
                                 N D Gohr            96-1-δ-R            960M             96M               -           50               0.54         [186]
   KATAN48 C                     N D Gohr            64-1-δ-R            64M              6.4M              -           47               0.582        [189]
                                 N D Gohr            96-1-δ-R            960M             96M               -           72               0.582        [186]
   KATAN48 RK,C                  N D Gohr            48-1-δ-R            960M             96M               -           96               0.625        [186]
   KATAN64                       N D Gohr            2-1-δ-R             20M              2M                -           31               0.718        [186]
                                 N D Gohr            128-1-δ-R           1280M            128M              -           36               0.548        [186]
   KATAN64 C                     N D Gohr            64-1-δ-R            64M              6.4M              -           26               0.613        [189]
                                 N D Gohr            128-1-δ-R           1280M            128M              -           61               0.613        [186]
   KATAN64 RK,C                  N D Gohr            128-1-δ-R           1280M            128M              -           86               0.728        [186]
  Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out
  settings n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an
  elaborate, manually designed training procedure (-).
 RK
     Related key setting.
 C
   Conditional setting.

                                                                   TABLE XV
                                        OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR KNOT.

    Primitive               Arch.           Class              Trn.            Val.           AutoND              Rounds             Acc.              Ref.
    KNOT-256                MLP             3-2-δ-D            1.6M            1.6M                -              10                 0.5912            [22]
    KNOT-512                MLP             3-2-δ-D            1.6M            1.6M                -              12                 0.6032            [22]
  Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
  n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
  manually designed training procedure (-).

                                                                   TABLE XVI
                                       OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR LBCI OT.

    Primitive           Arch.                   Class                 Trn.         Val.          AutoND            Rounds           Acc.            Ref.

    LBC-IoT             N D Gohr                2-1-CT-R              2M           200K                -           7                0.6408          [207]‡
  Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
  n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
  manually designed training procedure (-).
 ‡ The use of a small validation set raises concerns about the statistical robustness, reproducibility, and generalizability of the results, as such datasets are
  prone to high variance and may not reliably reflect model performance.



In [200], the authors performed experiments with low key                             20) TEA and XTEA: TEA and its successor XTEA are 64-
entropy (10 and 100 keys, respectively, for 1M samples), as                       round block ciphers encrypting 64-bit plaintexts with a 128-bit
well as with one random key per sample. We report the last                        key.
one for comparability and note that the results were very close                      In [20], the authors considered modular addition-based
in the 3 cases.                                                                   differentials, where the input difference is injected by modular
   In [207]† , the reported accuracy is 0.5036 on 105 samples,                    addition, which we denote by R+ in the experiment. [42]
which corresponds to less than 3 standard deviations and has                      automatically found distinguishers for both TEA and XTEA
a probability over 1% of occurring for distinguisher making                       for 5 cycles (10 rounds), respectively, with accuracies 0.5634
predictions at random; we question the relevance of this                          and 0.5984; the authors noted that they interestingly share the
result, as testing on more data is required to prove statistical                  same input difference. For TEA, [42] reached two more rounds
significance.                                                                     than [20].
                                                                                                                                                              34



                                                                 TABLE XVII
                                         OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR LEA.

    Primitive           Arch.                  Class                 Trn.          Val.          AutoND             Rounds            Acc.            Ref.
    LEA-128             DBitNet                2-1-CT-R              20M           2M                  ✓            11                0.512           [42]
                        Transformer            2-1-A-R               10M           500K                -            13                0.5012          [172]†
  Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
  n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
  manually designed training procedure (-).

                                                                  TABLE XVIII
                                      OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR PRESENT.

   Primitive                        Arch.              Class                Trn.          Val.         AutoND          Rounds            Acc.        Ref.
   PRESENT-64/80                    N D Gohr           8-1-CT-R             20M           2M              -            7                 0.5853      [174]
                                    UNet               12-1-A-R             /             /               -            7                 0.664       [219]‡
                                    DBitNet            2-1-CT-R             20M           2M             ✓             8                 0.512       [42]
                                    N D Gohr           2-2-δ-D              20M           2M              -            8                 0.515       [210]
                                    INC                32-1-CT-R            960M          32M             -            8                 0.5416      [223]
                                    LSTM               2-1-A-R              10M           500K            -            12                0.5014      [172] †
   PRESENT-64/80 RK                 MLP                6-1-δ-R              4.2M∗         1.9M∗           -            5                 0.614       [197]
                                    N D Gohr           2-2-δ-D              20M           2M              -            10                0.517       [210]
   Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out
   settings n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an
   elaborate, manually designed training procedure (-).
 RK
      Related key setting.
 ‡ The use of a small validation set raises concerns about the statistical robustness, reproducibility, and generalizability of the results, as such datasets are
   prone to high variance and may not reliably reflect model performance.

                                                                   TABLE XIX
                                        OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR PRIDE.

     Primitive            Arch.           Class               Trn.           Val.            AutoND              Rounds              Acc.          Ref.

     PRIDE                MLP             2-1-δ-R             2.1M           300K                  -             20                  1             [195]‡
  Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
  n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
  manually designed training procedure (-).
 ‡ The use of a small validation set raises concerns about the statistical robustness, reproducibility, and generalizability of the results, as such datasets are
  prone to high variance and may not reliably reflect model performance.



   21) TinyJAMBU: TinyJambu-128 is an authenticated en-
cryption algorithm based on a 640-round NLFSR-based per-
mutation, which encrypts 128-bit blocks. TinyJambu-128 was
among the ten NIST’s lightweight cryptography finalists.
   In [21]† , the authors claimed a full-round distinguisher on
TinyJambu, which we challenge. In the provided code, the
ciphertexts in a sample use the same key, nonce, and associated
data, which would provide a trivial distinguisher. As noted
by the designers of TinyJambu8 : ’When nonce is reused,
an attacker can decrypt the ciphertext since the encryption
of TinyJAMBU is somehow similar to the Cipher Feedback
mode.’.




  8 https://csrc.nist.gov/CSRC/media/Projects/lightweight-cryptography/
documents/finalist-round/updated-spec-doc/tinyjambu-spec-final.pdf
                                                                                                                                                             35




                                                                   TABLE XX
                                        OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR SHA3.

   Primitive            Arch.                    Class                 Trn.          Val.          AutoND          Rounds            Acc.            Ref.
   SHA3-256             N D Gohr                 2-1-CT-R              2M            2M               -            3                 0.9904          [174]
 Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
 n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
 manually designed training procedure (-).



                                                                  TABLE XXI
                                      OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR SKINNY.

   Primitive                           Arch.                 Class            Trn.          Val.     AutoND            Rounds         Acc.          Ref.

   SKINNY128Unkeyed                    Classical ML          2-2-δ-D          32K           32K           -            6              0.9912        [168]‡
                                       Classical ML          2-2-δ-D          2M            2M            -            7              0.5456        [168]
 Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
 n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
 manually designed training procedure (-).
‡ The use of a small validation set raises concerns about the statistical robustness, reproducibility, and generalizability of the results, as such datasets are
 prone to high variance and may not reliably reflect model performance.



                                                                 TABLE XXII
                                        OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR SLIM.

   Primitive           Arch.                    Class                Trn.           Val.           AutoND          Rounds            Acc.            Ref.

   SLIM                N D Gohr                 2-1-CT-R             2M             200K              -            3                 0.5036          [207]†
                       N D Gohr                 2-1-CT-R             2M             /                 -            5                 0.814           [200]
  Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
  n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
  manually designed training procedure (-).
/ Unknown quantity.
† A critical discussion of these results is provided in the text.




                                                                TABLE XXIII
                                  OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR TEA AND XTEA.

   Primitive            Arch.              Class                     Trn.           Val.           AutoND          Rounds            Acc.           Ref.

   TEA                  MLP                2-1-CT-R+                 2M             20K              -             8                 0.545          [20]‡
                        DBitNet            2-1-CT-R                  20M            2M               ✓             10                0.563          [42]
   XTEA                 DBitNet            2-1-CT-R                  20M            2M               ✓             10                0.598          [42]
 Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
 n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
 manually designed training procedure (-).
‡ The use of a small validation set raises concerns about the statistical robustness, reproducibility, and generalizability of the results, as such datasets are
 prone to high variance and may not reliably reflect model performance.



                                                                 TABLE XXIV
                                    OVERVIEW OF THE N EURAL D IFFERENTIAL D ISTINGUISHERS FOR T INY JAMBU.

   Primitive                    Arch.          Class             Trn.             Val.             AutoND          Rounds            Acc.            Ref.

   TinyJAMBU-128                MLP            2-1-δ-R           2.097M           262K                -            FULL              0.9958          [21]†
 Class: n-m-T -E, from subsection VIII-B. Under this convention, Gohr’s initial experiments are 2-1-CT-R, and the results obtained in greyed out settings
 n-m-T -E are not directly comparable. AutoND: indicates if the neural distinguisher was automatically generated (✓) or is the result of an elaborate,
 manually designed training procedure (-).
† A critical discussion of these results is provided in the text.
```
