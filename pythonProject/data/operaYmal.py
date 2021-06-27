import yaml
import os

def readYaml():
    with open("login.yaml","r") as f:
        return yaml.safe_load(f)
print(readYaml())