### More complex things to fix/add

- Preprocessing/modeling logic and data pipeline will change occasionally. There will be multiple runs on pipeline and multiple generations of data files produced by them. They will not always follow exactly the same pipeline DAG. Visualizing this is challenging. This is one of the reasons I need data/code lineage implemented. AI agent will have to think hard how to archieve this before implementing a solution.
- [x] Example 1: build an alternative model, e.g., random forest. Store hyperparameters of both models. Store metrics of both models. Store both models. Visualize this (on that DAG?) in a way which shows that I tried two model types and their performance.
- [x] Example 2a: lets simulate getting more raw data. Suppose that we get more data which increased out sample size by 50%. Simulate it by updating raw data in whatever way you want. Then we need to run the whole pipeline. And then it should be reflected in the lineage graph in a meaningfull way.


- [x] Refactor 1a: It appears that LLM agents struggle with writing and editing jupyter notebooks. I needed to do multiple rollbacks due to this issue. Having jupyter notebook rather then .py script is slightly more convenient for me, but it is not a big deal. So I guess it is better for progress of this project to remove notebooks dir and to move main logic into py scripts which correspond to these notebooks.
- [x] Refactor 1b: Add back notebooks dir. It will be used for EDA notebooks only. LLM agent will create .py scripts with all the logic for such EDA notebooks abd convert them into notebook with the same name. Huma developer will then run and edit such notebooks. This will allow each agentic entity to focus on what it does best.
- [x] Refactor 1c: Add capability to run the whole pipeline of .py sscripts with a single click. Do not overengineer.

- [x] Refactor 2: Data files naming. How to do it to have them play nicely in a pipeline and extensive experimentation, frequent reruns of the same pipeline etc? Having timing suffix for each file is very convenient but creates clutter. Having a single file for experiemnt will work better in a pipeline, look cleaner in a dir, but destroys information in the older data files. And lineage DAG should contain some information about time as well. Need to think how to achieve our desired functionaly...


- [x] Refactor 3: For transparecy, I need ability to run each pipeline step separately. I want it to report important metrics to help me better track how it processes data. Things like shapes of df, column names, engineered features, performance etc.


- [x] Enhancement 1: I need more detailed model performance evaluation. There exist many metrics for classification problems. I need performance report returned and stored for each experiment. 


- [x] Experiment 3: lets simulate getting new data similarly to the Example 2. Now add 100% more data. And add some randomization in order to make training models more challenging.


- [x] Experiment 4: add categorical variable (e.g., a, b, c, d, e) which has complex and noisy relation to the target. Then adjust the whole pipeline to deal with it.
- [x] Experiment 5: add interaction variables (e.g., a*b, a*c, a*d, a*e, b*c, b*d, b*e, c*d, c*e, d*e) which have complex and noisy relation to the target. Then adjust the whole pipeline to deal with it.

- Enhancement 2: I need to see model hyperparaemters stored somewhere. If there are there already, then I cannot find, so make their location more intuitive. And then I want to run several models with different hyperparaemters to see whether model with looser hyperparameters can learn the classification better. Train 3 versions of RF and 2 versions of XGB. Feel free to call these runs as experiments if needed.

Agent, DO NOT DO tasks below yet!
