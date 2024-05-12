import requests
from requests.auth import HTTPBasicAuth
import json
import streamlit as st

def invoke(atlassian_user_name, atlassian_api_token, atlassian_domain, atlassian_project_key, atlassian_user_id, summary, description):
    url = "https://" + atlassian_domain + ".atlassian.net/rest/api/3/issue"

    auth = HTTPBasicAuth(username=atlassian_user_name, password=atlassian_api_token)

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }

    payload = json.dumps( {
      "fields": {
        "project": {
          "key": atlassian_project_key
        },
        "issuetype": {
          "name": "Story"
        },
        "reporter": {
            "id": atlassian_user_id
        },
        "description": {
          "content": [
            {
              "content": [
                {
                  "text": description,
                  "type": "text"
                }
              ],
              "type": "paragraph"
            }
          ],
          "type": "doc",
          "version": 1
        },
        "summary": summary,
      },
      "update": {}
    })
    print(auth)
    response = requests.request(
      method="POST",
      url=url,
      data=payload,
      headers=headers,
        auth=auth
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    jira_key = json.loads(response.text)['key']
    jira_url = "https://"+atlassian_domain+".atlassian.net/jira/software/c/projects/"+atlassian_project_key+"/issues/"+jira_key
    st.success("A new issue has been created in JIRA with key " + jira_key)
    st.markdown("[Click here top open JIRA]("+jira_url+")")

def push_to_jira(summary, description):
    if 'ATLASSIAN_API_TOKEN' in st.secrets and 'ATLASSIAN_USER_NAME' in st.secrets and 'ATLASSIAN_DOMAIN' in st.secrets and 'ATLASSIAN_PROJECT_KEY' in st.secrets and 'ATLASSIAN_USER_ID' in st.secrets:
      atlassian_api_token = st.secrets['ATLASSIAN_API_TOKEN']
      atlassian_user_name = st.secrets['ATLASSIAN_USER_NAME']
      atlassian_domain = st.secrets['ATLASSIAN_DOMAIN']
      atlassian_project_key = st.secrets['ATLASSIAN_PROJECT_KEY']
      atlassian_user_id  = st.secrets['ATLASSIAN_USER_ID']
      invoke(atlassian_user_name, atlassian_api_token, atlassian_domain, atlassian_project_key, atlassian_user_id, summary, description)
    else:
        st.error("Atlassian access configuration missing. Update secrets.toml in utilities/.streamlit")
        st.error("Required keys: ATLASSIAN_API_TOKEN, ATLASSIAN_USER_NAME, ATLASSIAN_DOMAIN, ATLASSIAN_PROJECT_KEY, ATLASSIAN_USER_ID")

if __name__ == "__main__":
    push_to_jira('Test ticket', 'This is the rhythm of the night')