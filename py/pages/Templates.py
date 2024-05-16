import streamlit as st
import os
import json
from pages.utils import template as t


def update_section():
	with open(os.path.join(t.path_to_templates,filename),'r') as f:
		print("Save")

def template_selector():
	st.info("Editing and creating templates are currently disabled as the feature is being stabilized. Pick from one of the pre-defined templates for experimentation.")
	template = st.selectbox(label='Pick a template',
							options= t.list_templates(),
							index=0,
							help="Templates are pre-defined writing styles for user stories. Pick the style that you want the user story to be written in",
							label_visibility="collapsed")
	template_form(template)

def template_form(template):
	for filename in os.listdir(t.path_to_templates):
		if (filename.endswith(".json")):
			with open(os.path.join(t.path_to_templates,filename),'r') as f:
				file_content = f.read()
				if (json.loads(file_content)["name"] == template):
					template_name = json.loads(file_content)["name"]
					writing_guidelines = json.loads(file_content)["writing_guidelines"]
					section_names=[]
					section_instructions=[]
					for section in json.loads(file_content)['sections']:
						section_names.append(section['name'])
						section_instructions.append(section['instruction'])
					break

	main_col, section_col = st.columns(2)
	with main_col:
		with st.container(border=True):
			f_template_name = st.text_input(label="Template name", value=template_name, disabled=True)
			f_writing_guidelines = st.text_area("Writing style guidelines", value=writing_guidelines, disabled=True)
			submitted = st.button("Save", disabled=True)
			if submitted:
				st.write("Save")

	with section_col:
		with st.container(border=True):
			st.subheader("Sections")
			st.button(":orange-background[Add section :heavy_plus_sign:]", disabled=True)
			for section_name, section_instruction in zip(section_names, section_instructions):
				with st.expander(label=section_name):
					st.text_input(label="Enter a title for the section", value=section_name, disabled=True)
					st.text_area(label="Enter an instruction", value=section_instruction, disabled=True)
					spacer_col, del_col, save_col = st.columns([0.7, 0.15, 0.15])
					with del_col:
						st.button(key="del-" + section_name, label=":red-background[:wastebasket:]", disabled=True)

					with save_col:
						save = st.button(key="upd-" + section_name, label=":green-background[:floppy_disk:]", disabled=True)
						if save:
							st.write("Save hit")


def main():
	st.set_page_config(
		page_title='Hooser | Templates',
		page_icon=':material/home:',
		menu_items={
			'Get help': 'https://www.google.com',
			'About': '# Version: 2.2 #'
		},
		layout="wide")
	template_selector()

if __name__ == "__main__":
	main()

