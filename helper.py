# machinelearne.ar

import os
from os.path import exists as path_exists

import gradio as gr


class HFSpaces:
    def __init__(self, hf_spaces_url):
        self.url = hf_spaces_url
        self.local_folder = self.url.split('/')[-1]
        self.check_repo_exists_or_git_clone()
        self.readme = self.retrieve_readme(f'{self.local_folder}/README.md')
    
    def __str__(self):
        return f"{self.readme}"
    
    def check_repo_exists_or_git_clone(self):
        if not path_exists(self.local_folder):
            os.system(f'git clone {self.url}')
            os.system(f'pip install -r {self.local_folder}/requirements.txt')
        
    def retrieve_readme(self, filename):
        readme = {}
        if path_exists(filename):
            with open(filename) as f:
                for line in f:
                    if not line.find(':') > 0 or 'Check' in line: continue
                    (k,v) = line.split(':')
                    readme[(k)] = v.strip().replace('\n','')
        else:
            print('No "README.md" file')
            
        return readme
    
    def launch_demo(self, domain, region):
        '''
        Runs Gradio/Streamlit application on port 6006/80/8080 (open by default)        
        '''
        print('\033[1m' + f'Demo: {self.readme["title"]}\n' + '\033[0m')
        print(f'Wait a few seconds, then click the link below to open your application')
        print(f'https://{domain}.studio.{region}.sagemaker.aws/studiolab/default/jupyter/proxy/6006/')
        
        if self.readme["sdk"] == 'gradio':
            gr.close_all()
            os.system(f'export GRADIO_SERVER_PORT=6006 && cd {self.local_folder} && python {self.readme["app_file"]}')
        elif readme["title"] == 'streamlit':
            os.system(f'cd {self.local_folder} && streamlit run {self.readme["app_file"]} --server.port 6006')
        else:
            print('This notebook will not work with static apps hosted on `Spaces`')