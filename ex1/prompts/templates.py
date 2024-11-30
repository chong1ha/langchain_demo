from string import Template

class PromptTemplate:
    
    def __init__(self, template: str):
        self.template = Template(template)

    def generate(self, **kwargs):
        return self.template.safe_substitute(**kwargs)