# Chapter 03 Learnings
==
The book mentioned that: 
. There are two different types of learning
.. supervised learning
... Where you have a data set of clearly 'right' answers that your model can learn from
... Like a neural network
.. un-supervised learning
... Where no one piece of information is a "correct" example or can make predictions. The insight is generated holistically from the aggregate data. 
... Like data clustering in this chapter
. hierarchical clustering
.. It;s the continuous grouping of the two closest groups
. pearsons similarity will account for volume disparities in data while euclidian will not
.. for example in chapter 2 if a movie review tended to grade harsher then the another but still have similar tastes persons would match them and euclidian would not
.. here if a blogs have lots more words than others they would still match with blogs with less words on a pearsons scale