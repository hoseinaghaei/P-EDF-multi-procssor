# P-EDF (Partitioned Earliest Deadline First)

This project is a scheduler algorithm based on P-EDF on a multi-core system. You can change the processor count in the main.py file.

Here is a sample output using 10 tasks with dependencies as below.

<img src="pics/sample.png">
<img src="pics/result.png">

## main idea
###   We find the longest path in the tree and assign all those tasks in the path to a processor. then remove these tasks and continue with the remaining.
###   If there is no idle processor, we assign tasks to the processor with the least execution time. 
  
