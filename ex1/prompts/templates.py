from string import Template
from typing import Any

class PromptTemplate:
    """
    템플릿 처리 및 반환
    """
    
    def __init__(self, template: str):
        self.template = Template(template)

    def generate(self, **kwargs: Any) -> str:
        return self.template.safe_substitute(**kwargs)
# End of PromptTemplate