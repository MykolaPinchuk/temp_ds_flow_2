### Simple things to fix/add

- Naming of data files. I do not need seconds in the suffix.
- Metadata of data files. Notebook path and notebook names are identical. I want path from repo name to the dir containing a notebook. These two should not duplicate each other.


### More complex things to fix/add

- Notebooks and data pipeline will change occasionally. There will be multiple runs on pipeline and multiple generations of data files produced by them. They will not always follow exactly the same pipeline DAG. Visualizing this is challenging. This is one of the reasons I need data/code lineage implemented. AI agent will have to think hard how to archieve this before implementing a solution.
