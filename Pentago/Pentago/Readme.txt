Minmax-
   Expands approximately 16 thousand nodes every time the tree is generated (which is pretty much every time it is the AI's turn), 
 though that number fluctuates as the game goes on. The time and space complexity of the algorithm is O(b^d), although the coefficient is much lower than if i had
 generated every possible state (i did some repeat/redundant state checking to reduce tree size). Nodes expanded at first depth level is usually about 80-100 
 (depending on game state), while second level is closer to 100 to 130 a node (~16k total).

Minmax w/pruning-
   Expands the same number of nodes, and has the same time/space complexity. However, the coefficients on time/space complexity are much lower than regular minmax, as
 the pruning usually removes about half (or more) of the nodes in the tree. Nodes expanded at each level are still the same, but many of those expanded nodes end up getting
 pruned off