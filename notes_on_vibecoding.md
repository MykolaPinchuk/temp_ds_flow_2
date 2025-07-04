## LLM-based agentic tools used:

- windsurf.


### Windsurf best practices:

- SWE-1 model is no good. Using it is mostly waste of time.
- Gem 2.5 Pro is way better compared to SWE-1.
- If using agood model, give it more autonomy via /jdi at the end of each prompt.
- Keep each commit to larger than 4 prompts.
- Keep total number of prompts less than 8. After that, commit, push, and restart the chat.
- Always tell an agent at the very beginning not to overengineer stuff. E.g., Anthropic models tend to overengineer code by trying to fllow SWE best practices very rigorously. For DS purposes this is often an overkill. It leads to unnecessray complexity.
- Gem 2.5 can sometimes eneter some kind of loop, at least in terms of its printed thoughts. If this happens, restart it manually.


### Original prompt provided to the first gen of LLM agent to code this project from scratch:

I am a Data Scientist. My common pain point is messy codebase and data/source lineage. I have many steps of data preprocessing pipelines which I constantly change. I find it difficult to track which data files were created and when and by which notebook and how they are different from each other. I have similar challenges in tracking ML experiments. All my code so far is organized in jupyter notebooks.

I want to prototype a POC repo with such structure. I want to keep repo structure and code structure as simple as possible. I want to make minimum changes to how I write my data science notebooks. Please avoid OOP unless necessary.

Here are some thoughts on how to implement it. Please feel free to use different implementation if you think it is simpler and/or better than what I outline below.

There are only 4 dirs: src, notebooks, data, and logs. Logs contains logs from notebook runs which are created automatically. Data has raw and processes dirs. Each of data directories has data files (usually csv or pickle) and metadata dir. Metadata dir has a json corresponding to each created data file with identical name. Each json has only 4 keys: filename, timestamp (Incl seconds), path to notebook which wrote such data, and name of notebook file. Data files themselves should have timestamp in their suffix. E.g., raw_transactions_20250630_1913.csv.

Each notebook imports some logging module which logs main events: files read, files written, and output results. I want such logging to have no effect on the code in notebook. One way to do it is to implement logging start() and logging end() functions. The idea is that I should be able to just add these two to the beginning and end of existing notebooks, and it should work.

Each notebook will have notebook_description text object in its header. So notebook logging should include at least 5 things: notebook description, data files read, data files written, running time (start, end), and optional outputs. These outputs can e.g. be results of some ML experiment.

First, think about this task conceptually. Do not jump to coding before you fully thought through the big picture.


### Prompt to the LLM agent to continue working on this:

This repo is a project coded up by several generations of LLM agents. First, please read README, DOCUMENTATION and notes_on_videbcoding (especially Original prompt provided to the first gen of LLM agent to code this project from scratch section). Then, read and understand the entire codebase contained in this repo. 

If anything is unclear, please stop and ask questions. If everything is clear, then proceed to the following things from todo.md:
- 

- Please do not implement things from sections of todo file I have not asked for above.

/jdi






### General agent guidelines:
- Please do not implement things from sections of todo file I have not asked for above.
- Please do not use git. I will make commit myself after verifying that everything works.
If you want to document completion of these tasks, document it in tasks_done.md file. Do not touch todo.md. 
- Please do not ask me to copy-paste any text in jupyter notebooks. It is your job to edit code, not mine.
- If you figure out how to solve some task you have been stuck on for a while, feel free to document what you have learnt in lessons_for_future_agents.md. When documenting such lesson, specify exactly which kind of model you are. If you find that any lessons documented there by previous generations are not useful, feel free to edit/remove them.
- If unsure whether to ask for permission to do or run something, then do not. Go ahead and do it.
- Try maintaining consistency of the codebase. Adding temporary files for debugging and conversion is fine. But after validating that everything works, please remove them is they are no longer needed.

