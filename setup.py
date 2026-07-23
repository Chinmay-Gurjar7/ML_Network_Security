'''
The setup.py file is used for packaging and distributing Python projects. It contains metadata about the project, such as its name, version, author, and dependencies.
This file is essential for creating a distributable package that can be installed using tools like pip.

'''

from setuptools import setup, find_packages
from typing import List


def get_requirements(file_path:str) -> List[str]:
    '''
    This function reads the requirements.txt file and returns a list of dependencies.
    It ignores any lines that are comments or empty.

    :param file_path: Path to the requirements.txt file
    :return: List of dependencies
    '''
    
    requirement_lst: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            ## read lines from the file
            lines = file.readlines()
            ## Process each line 
            for line in lines:
                requirement = line.strip() # Remove leading/trailing whitespace
                ## Ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists in the project directory.")
        
    return requirement_lst

setup(
    name = 'NetworkSecurity',
    version = '0.0.1',
    author = 'Chinmay Gurjar',
    author_email = 'gurjarchinmay01@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)