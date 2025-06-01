import os
from box.exceptions import BoxValueError
import yaml
from textSummarizer.logging import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox object.
    
    Args:
        path_to_yaml (Path): The path to the YAML file.
        
    Returns:
        ConfigBox: A ConfigBox object containing the YAML data.
    """
    try:
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {path_to_yaml} loaded successfully.")
            return ConfigBox(content)
    except FileNotFoundError as e:
        logger.error(f"YAML file not found: {e}")
        raise
    except BoxValueError as e:
        logger.error(f"Error in YAML content: {e}")
        raise

@ensure_annotations
def create_directories(paths: list[Path]) -> None:
    """
    Creates directories if they do not exist.
    
    Args:
        paths (list[Path]): List of Path objects representing directories to create.
        
    Returns:
        None
    """
    for path in paths:
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory {path} created successfully.")
        except Exception as e:
            logger.error(f"Error creating directory {path}: {e}")
            raise

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Returns the size of a file or directory.
    
    Args:
        path (Path): The path to the file or directory.
        
    Returns:
        int: Size in KB.
    """
    if not path.exists():
        logger.error(f"Path {path} does not exist.")
        raise FileNotFoundError(f"Path {path} does not exist.")
    
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"
    # size = sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
    # logger.info(f"Size of {path} is {size} bytes.")
    # return size