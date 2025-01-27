## Human-Centered Machine Intelligence Lab with Dr. Michael Goodrich 
*April 2024 - Present*

### BT_Sim 🐜 : Grammatical Evolution in a Virtual Swarm Environment

#### *What Learned*
This project further developed my understanding of the concept of grammatical evolution through rigorous trial and error. I perused many an academic research paper in search of ideas and/or methods that I could implement to improve my simulation while also familiarizing myself with the field. A project of this size taught me a lot about good coding practices to implement in future projects. I became more familiar with the benefits of git, learned useful debugging practices, the importance of CLEAN and readable/understandable code with inlaid comment explanations, and even strengthened effective communication skills with my team members as we all individually tried our hand at the project.

#### *More Information About the Project*

The goal of the project was to familiarize our team with grammatical evolution, a type of genetic algorithm, and to develop a simulation that would enable us to see in a virtual environment the benefits of such a method of solution-finding, specifically in a biologically-inspired random environment where a correct solution is not necessarily known. Many decisions regarding the implementation of the algorithm as well as the agent and environment classes were left to me to decide. The grammar used to determine the behavior trees that our agents would use in the simulation was also developed personally.

The environment was to resemble a population of "ants" or other biological gatherer searching for food. Food was to be randomly distributed around the environment and the agents (or ants) were to search for food and return it to the den. Each agent had a particular genome that would be used to parse a grammar and provide the ant with a behaviour tree to implement in the simulation. Agents would then "share" genomes with each other when they "bumped" into each other, thereby sharing their genomes with an attached "score" based on how well they had been doing at finding, picking up, and returning food to the den. After a certain threshold of "poor activity" was met, agents would decide to "evolve" and perform genetic operations on their dictionary of collected genome and genome_score pairs to hopefully implement a behavior better capable of accomplishing the task at hand. With every agent acting in accordance with their own respective behavior tree, we hoped to see a population-wide behavior (or behaviors) emerge that maximized the agents' potential to find and gather food.

<!--
Add more about the specific decisions you made, what each file does, what you learned from each decision, the two types of grammatical evolution? What you want to continue working on, where did it end? Struggles/overcome them?
-->
