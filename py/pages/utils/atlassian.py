import requests
from requests.auth import HTTPBasicAuth
import json
import streamlit as st

def configure_atlassian():
    if 'ATLASSIAN_API_TOKEN' in st.secrets and 'ATLASSIAN_USER_NAME' in st.secrets and 'ATLASSIAN_DOMAIN' in st.secrets and 'ATLASSIAN_PROJECT_KEY' in st.secrets and 'ATLASSIAN_USER_ID' in st.secrets:
      st.session_state['atlassian_api_token'] = st.secrets['ATLASSIAN_API_TOKEN']
      st.session_state['atlassian_user_name'] = st.secrets['ATLASSIAN_USER_NAME']
      st.session_state['atlassian_domain'] = st.secrets['ATLASSIAN_DOMAIN']
      st.session_state['atlassian_project_key'] = st.secrets['ATLASSIAN_PROJECT_KEY']
      st.session_state['atlassian_user_id']  = st.secrets['ATLASSIAN_USER_ID']
    else:
        with st.expander("Atlassian JIRA configuration"):
            st.subheader("Atlassian JIRA configuration", help="For pushing user stories to JIRA, adding details of users for whom the requires Create Issue, Browse Projects and Modify Reporter permissions have been granted")
            st.session_state['atlassian_api_token'] = st.text_input(label="Enter your Atlassian API token")
            st.session_state['atlassian_user_name'] = st.text_input(label="Enter your Atlassian user name")
            st.session_state['atlassian_domain'] = st.text_input(label="Enter your Atlassian domain")
            st.session_state['atlassian_project_key'] = st.text_input(label="Enter your JIRA project key")
            st.session_state['atlassian_user_id'] = st.text_input(label="Enter the id of the user", help="Copy this from the URL when viewing the Atlassian profile page")

def invoke(summary, description):
    url = "https://" + st.session_state['atlassian_domain'] + ".atlassian.net/rest/api/3/issue"

    auth = HTTPBasicAuth(username=st.session_state['atlassian_user_name'], password=st.session_state['atlassian_api_token'])

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }

    payload = json.dumps( {
      "fields": {
        "project": {
          "key": st.session_state['atlassian_project_key']
        },
        "issuetype": {
          "name": "Story"
        },
        "reporter": {
            "id": st.session_state['atlassian_user_id']
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

    response = requests.request(
        method="POST",
        url=url,
        data=payload,
        headers=headers,
        auth=auth
    )
    if response.status_code == 201:
        jira_key = json.loads(response.text)['key']
        jira_url = "https://" + st.session_state['atlassian_domain'] + ".atlassian.net/jira/software/c/projects/" + \
                   st.session_state['atlassian_project_key'] + "/issues/" + jira_key
        st.success("A new issue has been created in JIRA with key " + jira_key)
        st.markdown("[Click here top open JIRA](" + jira_url + ")")
    else:
        st.error("Error while creating issue in JIRA")
        st.error(json.loads(response.text))

def push_to_jira(summary, description):
    if st.session_state['atlassian_api_token'] and st.session_state['atlassian_user_name'] and st.session_state['atlassian_domain'] and st.session_state['atlassian_project_key'] and st.session_state['atlassian_user_id']:
        invoke(summary, description)
    else:
        st.error("Atlassian integration not configured. Enter details in the sidebar")

if __name__ == "__main__":
    push_to_jira('Test ticket', 'This is the rhythm of the night')