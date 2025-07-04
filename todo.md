### More complex things to fix/add

- Preprocessing/modeling logic and data pipeline will change occasionally. There will be multiple runs on pipeline and multiple generations of data files produced by them. They will not always follow exactly the same pipeline DAG. Visualizing this is challenging. This is one of the reasons I need data/code lineage implemented. AI agent will have to think hard how to archieve this before implementing a solution.
- [x] Example 1: build an alternative model, e.g., random forest. Store hyperparameters of both models. Store metrics of both models. Store both models. Visualize this (on that DAG?) in a way which shows that I tried two model types and their performance.
- [x] Example 2a: lets simulate getting more raw data. Suppose that we get more data which increased out sample size by 50%. Simulate it by updating raw data in whatever way you want. Then we need to run the whole pipeline. And then it should be reflected in the lineage graph in a meaningfull way.


- [] It appears that LLM agents struggle with writing and editing jupyter notebooks. Having jupyter notebook rather then .py script is slightly more convenient for me, but it is not a big deal. So I guess it is better for progress of this project to remobe notebooks dir and to move main logic into py scripts which correpond to these notebooks.




- [] Example 2b clean-up and verification. Is everything working as intended? What if I want to run original data pipeline?
- [] Example 3: lets simulate gettin new data similarly to the Example 2. Now add 100% more data. And add some randomization in order to make training models more challenging.
- [] Example 4: add categorical variable (e.g., a, b, c, d, e) which has complex and noisy relation to the target. Then adjust the whole pipeline to deal with it.
- [] Example 5: add interaction variables (e.g., a*b, a*c, a*d, a*e, b*c, b*d, b*e, c*d, c*e, d*e) which have complex and noisy relation to the target. Then adjust the whole pipeline to deal with it.


- automating notebook runs.