import os
from box.exceptions import BoxValueError
import yaml
from textsummarizer.logging import logger
from ensure import ensure_annotations   
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations 

def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads yaml file and returns
    Args:
        path_to_yaml (Path): path to the yaml file
    Raises:
        ValueError: if the yaml file is empty
    Returns:
        ConfigBox: ConfigBox object containing the yaml file data
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"Yaml file: {path_to_yaml} loaded successfully.")
            return ConfigBox(content)   
    except FileNotFoundError:
        raise ValueError("yaml file is empty ")
    except BoxValueError as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list,  verbose = True):

    """create listt of directories
    Args:
        path_to_directories (list): list of directories
        ignore (bool),optional: ignore if multiple dirs is  to be created. dafult is fasle
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in kb
    Args:
        path (Path): path to the file
    Returns:
        str: size in kb
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~{size_in_kb} kb"