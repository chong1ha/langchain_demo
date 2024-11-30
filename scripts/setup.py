from setuptools import setup, find_packages

setup(
    name="langchain_demo",
    version="1.0",
    description="test",
    author="chongha",
    author_email="",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "langchain==0.3.7", 
        "openai==1.54.0",   
        "streamlit==1.39.0",
        "python-dotenv==1.0.1"  
    ],
    entry_points={
        'console_scripts': [
            'run-langchain=app:main',
        ],
    },
    python_requires='>=3.9',
)
