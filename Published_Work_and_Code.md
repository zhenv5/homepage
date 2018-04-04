### Published Work & Code


* Homepage: [Jiankai Sun](http://web.cse.ohio-state.edu/~sun.1306/)
* Last Updated Date: 2018.03.25

<span id="home"></span>
Works categorized by year: 

* [View All Paper](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/)
* [2018](#2018)
*  [2017](#2017)
*  [Visualization of Work before 2016](#visualization2016)
*  [2014](#2014)
*  [2012](#2012)


### 2018

#### QDEE: Question Difficulty and Expertise Estimation in Community Question Answering Sites

> In this paper, we present a framework for Question Difficulty and Expertise Estimation (QDEE) in Community Question Answering sites (CQAs) such as Yahoo! Answers and Stack Overflow, which tackles a fundamental challenge in crowdsourcing: how to appropriately route and assign questions to users with the suitable expertise. This problem domain has been the subject of much research and includes both language-agnostic as well as language conscious solutions. We bring to bear a key language-agnostic insight: that users gain expertise and therefore tend to ask as well as answer more difficult questions over time. We use this insight within the popular competition (directed) graph model to estimate question difficulty and user expertise by identifying key hierarchical structure within said model. An important and novel contribution here is the application of "social agony" to this problem domain. Difficulty levels of newly posted questions (the cold-start problem) are estimated by using our QDEE framework and additional textual features. We also propose a model to route newly posted questions to appropriate users based on the difficulty level of the question and the expertise of the user. Extensive experiments on real world CQAs such as Yahoo! Answers and Stack Overflow data demonstrate the improved efficacy of our approach over contemporary state-of-the-art models. The QDEE framework also allows us to characterize user expertise in novel ways by identifying interesting patterns and roles played by different users in such CQAs.

* The 12th International AAAI Conference on Web and Social Media (ICWSM 2018)
* [arXiv](https://arxiv.org/abs/1804.00109)
* [Code](https://github.com/zhenv5/QDEE)
* Acceptance Rate: $48/295 = 16\%$
* [Back To Top](#home)

#### SEANO: Semi-supervised Embedding in Attributed Networks with Outliers [6]

> In this paper, we propose a novel framework, called Semi-supervised Embedding in Attributed Networks with Outliers (SEANO), to learn a low-dimensional vector
representation that systematically captures the topological proximity, attribute affinity and label similarity of vertices in a partially labeled attributed network
(PLAN). Our method is designed to work in both transductive and inductive settings while explicitly alleviating noise effects from outliers. Experimental results on
various datasets drawn from the web, text and image domains demonstrate the advantages of SEANO over the state-of-the-art methods in semi-supervised classification
under transductive as well as inductive settings. We also show that a subset of parameters in SEANO are interpretable as outlier scores and can significantly outperform
baseline methods when applied for detecting network outliers. Finally, we present the use of SEANO in a challenging real-world setting – flood mapping of
satellite images and show that it is able to outperform modern remote sensing algorithms for this task.

* SDM'2018
* [Project Homepage (Code and Dataset)](http://jiongqianliang.com/SEANO/)
* [PDF Download](https://arxiv.org/pdf/1703.08100.pdf) [bib](http://jiongqianliang.com/publications/SDM18.txt)

### 2017

#### Breaking Cycles in Noisy Hierarchies [5]

> Taxonomy graphs that capture hyponymy or meronymy relationships through directed edges are expected to be acyclic. However, in practice, they may have thousands of cycles, as they are often created in a crowd-sourced way. Since these cycles represent logical fallacies, they need to be removed for many web applications. In this paper, we address the problem of breaking cycles while preserving the logical structure (hierarchy) of a directed graph as much as possible. Existing approaches for this problem either need manual intervention or use heuristics that can critically alter the taxonomy structure. In contrast, our approach infers graph hierarchy using a range of features, including a Bayesian skill rating system and a social agony metric. We also devise several strategies to leverage the inferred hierarchy for removing a small subset of edges to make the graph acyclic. Extensive experiments demonstrate the effectiveness of our approach.

>  **Keywords**:  _Directed Acyclic Graph_, _Graph Hierarchy_, _TrueSkill_, _Social Agony_, _Cycle Edges_

* WebSci'2017
* Internship work with [Deepak Ajwani](https://www.bell-labs.com/usr/deepak.ajwani), [Patrick Nicholson](https://www.bell-labs.com/usr/pat.nicholson), and [Alessandra Sala](https://www.bell-labs.com/usr/alessandra.sala)  @Bell Labs, Nokia, Ireland, May - Aug, 2016
*  [Slides Download](https://github.com/zhenv5/homepage/blob/master/documents/Slides_WebSci_17_Breaking_Cycles_in_Noisy_Hierarchies.pdf)
* [Breaking cycles in noisy hierarchies](https://github.com/zhenv5/breaking_cycles_in_noisy_hierarchies/blob/master/paper/Paper_WebSci_17_Breaking_Cycles_in_Noisy_Hierarchies.pdf) [Paper Download](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/WebSci_17_Remove_Cycle_Edges.pdf)
* Code is available on [Github](https://github.com/zhenv5/breaking_cycles_in_noisy_hierarchies.git)
* [BibTex Download](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/Bib_WebSci_17_Breaking_Cycles_in_Noisy_Hierarchies.bib)
* [ACM Link](http://dl.acm.org/citation.cfm?id=3091495)
* Acceptance Rate: $30/127 = 23.6\%$
* [Back To Top](#home)

#### Learning to Recommend Accurate and Diverse Items [4]

> In this study, we investigate diversified recommendation problem by supervised learning, seeking significant improvement in diversity while maintaining accuracy. In particular, we regard each user as a training instance, and heuristically choose a subset of accurate and diverse items as ground-truth for each user. We then represent each user or item as a vector resulted from the factorization of the user-item rating matrix. In our paper, we try to discover a factorization for matching the following supervised learning task. In doing this, we define two coupled optimization problems, parameterized matrix factorization and structural learning, to formulate our task. And we propose a diversified collaborative filtering algorithm (DCF) to solve the coupled problems. We also introduce a new pairwise accuracy metric and a normalized topic coverage diversity metric to measure the performance of accuracy and diversity respectively. Extensive experiments on benchmark datasets show the performance gains of DCF in comparison with the state-of-the-art algorithms.

* WWW'2017
* [PDF Download](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/WWW_2017_Learning_to_Recommend_Accurate_and_Diverse_Items.pdf)
* [BibTex Download](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/WWW_2017_Learning_to_Recommend_Accurate_and_Diverse_Items.bib)
* [ACM Link](http://dl.acm.org/citation.cfm?id=3052585)
* Acceptance Rate: $164/966 = 17\%$
* [Back To Top](#home)

<span id="visualization2016"> </span>

#### Keyword Cloud to Visualize My Work before 2016

* ![Word Cloud](http://web.cse.ohio-state.edu/~sun.1306/pic/cloud_word_2017.png)

*  **This keyword cloud figure is generated based on abstracts of my papers published/accepted before 2016**
* [Back To Top](#home)


### 2014

#### VSRank: A Novel Framework for Ranking-Based Collaborative Filtering [3]

> Collaborative filtering (CF) is an effective technique addressing the information overload problem. CF approaches generally fall into two categories: rating based and ranking based. The former makes recommendations based on historical rating scores of items and the latter based on their rankings. Ranking-based CF has demonstrated advantages in recommendation accuracy, being able to capture the preference similarity between users even if their rating scores differ significantly. In this study, we propose VSRank, a novel framework that seeks accuracy improvement of ranking-based CF through adaptation of the vector space model. In VSRank, we consider each user as a document and his or her pairwise relative preferences as terms. We then use a novel degree-specialty weighting scheme resembling TF-IDF to weight the terms. Extensive experiments on benchmarks in comparison with the state-of-the-art approaches demonstrate the promise of our approach.

* ACM-TIST'2014
* [PDF Download](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/TIST_2014_VSRank-A_Novel_Framework_for_Ranking-Based_Collaborative_Filtering.pdf)
* [BibTex Download](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/TIST_2014_VSRank-A_Novel_Framework_for_Ranking-Based_Collaborative_Filtering.bib)
* [ACM Link](http://dl.acm.org/citation.cfm?id=2542048)
* [Back To Top](#home)

### 2012

####  Learning to rank for hybrid recommendation [2]

> Most existing recommender systems can be classified into two categories: collaborative filtering and content-based filtering. Hybrid recommender systems combine the advantages of the two for improved recommendation performance. Traditional recommender systems are rating-based. However, predicting ratings is an intermediate step towards their ultimate goal of generating rankings or recommendation lists. Learning to rank is an established means of predicting rankings and has recently demonstrated high promise in improving quality of recommendations. In this paper, we propose LRHR, the first attempt that adapts learning to rank to hybrid recommender systems. LRHR first defines novel representations for both users and items so that they can be content-comparable. Then, LRHR identifies a set of novel meta-level features for learning purposes. Finally, LRHR adopts RankSVM, a pairwise learning to rank algorithm, to generate recommendation lists of items for users. Extensive experiments on benchmarks in comparison with the state-of-the-art algorithms demonstrate the performance gain of our approach.

* CIKM'2012
* [PDF Download](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/CIKM_12_Learning_to_Rank_for_Hybrid_Recommendation.pdf)
* [BibTex Download](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/CIKM_12_Learning_to_Rank_for_Hybrid_Recommendation.bib)
* [ACM Link](http://dl.acm.org/citation.cfm?id=2398610)
* [Back To Top](#home)

#### Adapting vector space model to ranking-based collaborative filtering [1]

> Collaborative filtering (CF) is an effective technique addressing the information overload problem. Recently ranking-based CF methods have shown advantages in recommendation accuracy, being able to capture the preference similarity between users even if their rating scores differ significantly. In this study, we seek accuracy improvement of ranking-based CF through adaptation of the vector space model, where we consider each user as a document and her pairwise relative preferences as terms. We then use a novel degree-specialty weighting scheme resembling TF-IDF to weight the terms. Then we use cosine similarity to select a neighborhood of users for the target user to make recommendations. Experiments on benchmarks in comparison with the state-of-the-art methods demonstrate the promise of our approach.

* CIKM'2012
* [PDF Download](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/CIKM_12_Adapting_Vector_Space_Model_to_Raanking-based_Collaborative_Filtering.pdf)
* [BibTex Download](http://web.cse.ohio-state.edu/~sun.1306/Published_Works/CIKM_12_Adapting_Vector_Space_Model_to_Raanking-based_Collaborative_Filtering.bib)
* [ACM Link](http://dl.acm.org/citation.cfm?id=2398458)
* [Back To Top](#home)



