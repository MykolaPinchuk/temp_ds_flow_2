## LLM-based agentic tools used:

- windsurf.


### Windsurf best practices:

- SWE-1 model is no good. Using it is mostly waste of time.
- Gem 2.5 Pro is way better compared to SWE-1.
- If using agood model, give it more autonomy via /jdi at the end of each prompt.
- Keep each commit to larger than 4 prompts.
- Keep total number of prompts less than 8. After that, commit, push, and restart the chat.
- Always tell an agent at the very beginning not to overengineer stuff. E.g., Anthropic models tend to overengineer code by trying to fllow SWE best practices very rigorously. For DS purposes this is often an overkill. It leads to unnecessray complexity.










### Original prompt provided to the first gen of LLM agent to code this project from scratch:

I am a Data Scientist. My common pain point is messy codebase and data/source lineage. I have many steps of data preprocessing pipelines which I constantly change. I find it difficult to track which data files were created and when and by which notebook and how they are different from each other. I have similar challenges in tracking ML experiments. All my code so far is organized in jupyter notebooks.

I want to prototype a POC repo with such structure. I want to keep repo structure and code structure as simple as possible. I want to make minimum changes to how I write my data science notebooks. Please avoid OOP unless necessary.

Here are some thoughts on how to implement it. Please feel free to use different implementation if you think it is simpler and/or better than what I outline below.

There are only 4 dirs: src, notebooks, data, and logs. Logs contains logs from notebook runs which are created automatically. Data has raw and processes dirs. Each of data directories has data files (usually csv or pickle) and metadata dir. Metadata dir has a json corresponding to each created data file with identical name. Each json has only 4 keys: filename, timestamp (Incl seconds), path to notebook which wrote such data, and name of notebook file. Data files themselves should have timestamp in their suffix. E.g., raw_transactions_20250630_1913.csv.

Each notebook imports some logging module which logs main events: files read, files written, and output results. I want such logging to have no effect on the code in notebook. One way to do it is to implement logging start() and logging end() functions. The idea is that I should be able to just add these two to the beginning and end of existing notebooks, and it should work.

Each notebook will have notebook_description text object in its header. So notebook logging should include at least 5 things: notebook description, data files read, data files written, running time (start, end), and optional outputs. These outputs can e.g. be results of some ML experiment.

First, think about this task conceptually. Do not jump to coding before you fully thought through the big picture.