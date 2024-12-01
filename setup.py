from setuptools import setup, find_packages


try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Detailed description not available."

setup(
    name="langchain_demo",
    version="1.0",
    description="demo",
    author="chong1ha",
    author_email="",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "langchain>=0.3.9", 
        "openai>=1.55.3",   
        "streamlit>=1.40.2",
        "python-dotenv>=1.0.1"  
    ],
    entry_points={
        'console_scripts': [
            'run-langchain=app:main',
        ],
    },
    python_requires='>=3.9',
)
