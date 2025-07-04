### More complex things to fix/add

- Notebooks and data pipeline will change occasionally. There will be multiple runs on pipeline and multiple generations of data files produced by them. They will not always follow exactly the same pipeline DAG. Visualizing this is challenging. This is one of the reasons I need data/code lineage implemented. AI agent will have to think hard how to archieve this before implementing a solution. 
- [x] Example 1: build an alternative model, e.g., random forest. Store hyperparameters of both models. Store metrics of both models. Store both models. Visualize this (on that DAG?) in a way which shows that I tried two model types and their performance.
- [x] Example 2: lets simulate getting more raw data. Suppose that we get more data which increased out sample size by 50%. Simulate it by updating raw data in whatever way you want. Then we need to run the whole pipeline. And then it should be reflected in the lineage graph in a meaningfull way. 
- [] Example 2 clean-up and verification. Is everything working as intended? What if I want to run original data pipeline?
- [] Example 3: lets simulate gettin new data similarly to the Example 2. Now add 100% more data. And add some randomization in order to make training models more challenging.

- automating notebook runs.