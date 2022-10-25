from setuptools import setup,find_packages
from typing import List

# Declaring variables for setup function
PROJECTING_NAME = 'kafka'
VERSION = '0.0.3'
AUTHOR = 'Shivaraj Bevoor'
DESCRIPTION = "This is a sample project for kafka producer and consumer"

REQUIRMENT_FILE_NAME = 'requirements.txt'

HYPEN_E_DOT = "-e ."

def get_requirements_list() -> List[str]:
    """
    Description : This function is going to return list of requirements...
    ...mentioned in the requirments.txt file.
    Return in this function going to return list which contains...
    ...name of libraries mentioned in the requirements.txt file
    """

    with open(REQUIRMENT_FILE_NAME) as requirements_file:
        #This line reads all the lines in the requirements.txt file
        requirement_list = requirements_file.readlines()
        # This line removes \n from list of requirments
        requirement_list = [requirement_name.replace('\n', '') for requirement_name in requirement_list]
        if HYPEN_E_DOT in requirement_list:
            requirement_list.remove(HYPEN_E_DOT)
        return requirement_list

setup(
name= PROJECTING_NAME,
version= VERSION,
author= AUTHOR,
description= DESCRIPTION,
packages = find_packages(),
install_requires = get_requirements_list()
)


