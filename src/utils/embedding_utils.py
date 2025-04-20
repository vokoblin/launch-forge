"""
Utilities for embedding configuration data in launcher executables.
"""

import os
import json
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

# Markers to locate embedded configuration in executable files
CONFIG_MARKER_START = b"<<<LAUNCHFORGE_CONFIG_START>>>"
CONFIG_MARKER_END = b"<<<LAUNCHFORGE_CONFIG_END>>>"


def embed_config(
    template_path: str, 
    output_path: str, 
    config_data: Dict
) -> Tuple[bool, str]:
    """
    Embed configuration data in an executable file.
    
    Args:
        template_path: Path to the template executable
        output_path: Path where the customized executable should be saved
        config_data: Configuration data to embed
        
    Returns:
        Tuple containing:
        - bool: True if embedding was successful
        - str: Error message if embedding failed, otherwise empty string
    """
    try:
        logger.info(f"Embedding configuration in executable: {output_path}")
        
        # Ensure template file exists
        if not os.path.exists(template_path):
            logger.error(f"Template executable not found: {template_path}")
            return False, f"Template executable not found: {template_path}"
        
        # Convert config data to JSON
        config_json = json.dumps(config_data, indent=2)
        config_bytes = config_json.encode('utf-8')
        
        # Create the full data block with markers
        data_block = CONFIG_MARKER_START + config_bytes + CONFIG_MARKER_END
        
        # Read the template file
        with open(template_path, 'rb') as f:
            template_data = f.read()
        
        # Check if the template already has configuration data
        start_idx = template_data.find(CONFIG_MARKER_START)
        if start_idx != -1:
            # If markers exist, replace the existing configuration
            end_idx = template_data.find(CONFIG_MARKER_END, start_idx)
            if end_idx == -1:
                logger.error(f"Template has start marker but no end marker: {template_path}")
                return False, "Template has invalid configuration markers"
                
            # Calculate the end position (including the end marker)
            end_pos = end_idx + len(CONFIG_MARKER_END)
            
            # Replace the existing configuration
            output_data = template_data[:start_idx] + data_block + template_data[end_pos:]
        else:
            # If no markers exist, append configuration to the end of the file
            output_data = template_data + data_block
        
        # Write the output file
        with open(output_path, 'wb') as f:
            f.write(output_data)
        
        # Make the output file executable on Unix-like systems
        if os.name == 'posix':
            os.chmod(output_path, 0o755)
            
        logger.info(f"Configuration successfully embedded in {output_path}")
        return True, ""
        
    except Exception as e:
        logger.exception(f"Failed to embed configuration in executable: {e}")
        return False, f"Failed to embed configuration: {str(e)}"


def extract_config(executable_path: str) -> Optional[Dict]:
    """
    Extract configuration data embedded in an executable file.
    
    Args:
        executable_path: Path to the executable file
        
    Returns:
        Dict: Extracted configuration data, or None if not found
    """
    try:
        logger.debug(f"Extracting configuration from: {executable_path}")
        
        # Ensure file exists
        if not os.path.exists(executable_path):
            logger.error(f"Executable not found: {executable_path}")
            return None
        
        # Read the executable file
        with open(executable_path, 'rb') as f:
            file_data = f.read()
        
        # Find the markers
        start_idx = file_data.find(CONFIG_MARKER_START)
        if start_idx == -1:
            logger.debug(f"Configuration start marker not found in: {executable_path}")
            return None
            
        end_idx = file_data.find(CONFIG_MARKER_END, start_idx)
        if end_idx == -1:
            logger.debug(f"Configuration end marker not found in: {executable_path}")
            return None
        
        # Extract the configuration data
        start_data_idx = start_idx + len(CONFIG_MARKER_START)
        config_json = file_data[start_data_idx:end_idx].decode('utf-8')
        
        # Parse the JSON data
        config_data = json.loads(config_json)
        logger.debug(f"Successfully extracted configuration from: {executable_path}")
        
        return config_data
        
    except Exception as e:
        logger.error(f"Failed to extract configuration from executable: {e}")
        return None


def verify_embedding(executable_path: str, expected_config: Dict) -> bool:
    """
    Verify that the configuration was correctly embedded in the executable.
    
    Args:
        executable_path: Path to the executable file
        expected_config: Expected configuration data
        
    Returns:
        bool: True if the embedded configuration matches the expected configuration
    """
    try:
        # Extract the configuration
        extracted_config = extract_config(executable_path)
        
        if extracted_config is None:
            logger.error(f"No configuration found in: {executable_path}")
            return False
        
        # Compare with expected configuration
        # This is a simple comparison that ignores whitespace and formatting differences
        return json.dumps(extracted_config, sort_keys=True) == json.dumps(expected_config, sort_keys=True)
        
    except Exception as e:
        logger.error(f"Failed to verify configuration in executable: {e}")
        return False