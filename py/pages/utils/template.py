import os
import json
import streamlit as st

path_to_templates = os.path.join(os.getcwd(),'templates')

def parse_json(file_content):
    try:
        template_instructions = ["I want you to create a user story for a feature that I will describe below. I will specify the format in which it has to be written."]
        template_json = json.loads(file_content)
        template_instructions.append(template_json["writing_guidelines"])
        template_instructions.append("The user story has the following sections. The output should be in markdown format with each section title in Heading 1")
        for section in template_json["sections"]:
            template_instructions.append(section["name"])
            template_instructions.append(section["instruction"])
        template_instructions.append("Create a user story for the following feature in the above specified format.")

    except KeyError as e:
        print("Template is corrupt. Could not find value for attribute " + str(e))
        #TODO notify session state
    else:
        template_instructions_str = ('\n').join(template_instructions)
        return template_instructions_str

def set_template_instrutions(template_name):
    template_file = os.path.join(path_to_templates, template_name.lower().replace(' ','_')) + '.json'
    try:
        with open(template_file,'r') as f:
            file_content = f.read()
    except FileNotFoundError as e:
        st.error("Template not found.")
    else:
        template_instructions_str = parse_json(file_content)
        return template_instructions_str

def list_templates():
    template_files = []
    for filename in os.listdir(path_to_templates):
        if filename.endswith(".json"):
            with open(os.path.join(path_to_templates,filename)) as f:
                template_files.append(json.loads(f.read())["name"])
    return template_files

if __name__ == "__main__":
    set_template_instrutions("Krispy")