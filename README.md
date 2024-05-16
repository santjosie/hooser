# hooser

## introduction
hooser is a tool that can generate user stories for features that you are building, and create those user stories in JIRA as issues.

## how do i run this?
you can access the hosted version of the app at [hooser](https://hooser.streamlit.app)

if you want to run it locally, clone the repository in your local machine
```
git clone 
```
navigate into the project folder and execute the following command
```
streamlit run py/Home.py
```
## how does it work?
user journey
- you create a template specifying the writing style that and the sections that you want in your user stories.
- then you pick that template.
- enter a brief description for the feature that you want to build and hit Enter.
- hooser then magically writes a structured user story for you.
- you hit the Push to Jira button, to create an issue in JIRA.

what happens behind the scene?
- when you enter a brief prompt to describe a feature, hooser merges it with instructions from the template.
- this new combined set of instructions is sent to the north pole a.k.a snowflake arctic llm.
- this enterprise grade, llm trained on 17b active parameters generates a detailed user story.
- the user story generated is streamed back into the streamlit app, hooser.

## can it centre a div?
i'm afraid hooser can't help you with that.

## what's next for hooser?
- first and foremost, generate a lot of user stories.
- here's a feature roadmap
  - clean up template management crud operations
  - linear integration
  - change atlassian authentication to OAuth2.0
  - incorporate authentication and user accounts
  - incorporate RAG to ground user stories on custom user research and data insights
  - create tagging and storage mechanism for user research data set
  - workflows for creating new products and offerings and generating user stories in bulk
