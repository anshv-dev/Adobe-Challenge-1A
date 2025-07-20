import json
import jsonschema
from typing import Dict, Any, Tuple
from pathlib import Path

class SchemaValidator:
    """
    Validates JSON output against the required schema for Adobe Hackathon Challenge 1a
    """
    
    def __init__(self, schema_path: str = "output_schema.json"):
        self.schema_path = schema_path
        self._schema = None
        self._load_schema()
    
    def _load_schema(self):
        """Load the JSON schema from file"""
        try:
            with open(self.schema_path, 'r') as f:
                self._schema = json.load(f)
        except FileNotFoundError:
            # If schema file doesn't exist, create a default one
            self._create_default_schema()
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in schema file: {str(e)}")
    
    def _create_default_schema(self):
        """Create a default schema if none exists"""
        self._schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "PDF Processing Output Schema",
            "description": "Schema for structured data extracted from PDF documents",
            "type": "object",
            "required": ["document_info", "content", "extraction_summary"],
            "properties": {
                "document_info": {
                    "type": "object",
                    "required": ["filename", "page_count", "processing_timestamp"],
                    "properties": {
                        "filename": {"type": "string"},
                        "page_count": {"type": "integer", "minimum": 0},
                        "total_pages": {"type": "integer", "minimum": 0},
                        "processing_timestamp": {"type": "string"},
                        "metadata": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "author": {"type": "string"},
                                "subject": {"type": "string"},
                                "creator": {"type": "string"},
                                "producer": {"type": "string"},
                                "creation_date": {"type": "string"},
                                "modification_date": {"type": "string"}
                            }
                        }
                    }
                },
                "content": {
                    "type": "object",
                    "required": ["text_blocks", "images", "tables", "page_structure"],
                    "properties": {
                        "text_blocks": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["page", "block_id", "type", "text"],
                                "properties": {
                                    "page": {"type": "integer", "minimum": 1},
                                    "block_id": {"type": "string"},
                                    "type": {
                                        "type": "string",
                                        "enum": ["header", "paragraph", "list", "table_text", "caption", "unknown"]
                                    },
                                    "text": {"type": "string"},
                                    "position": {
                                        "type": "object",
                                        "properties": {
                                            "x0": {"type": "number"},
                                            "y0": {"type": "number"},
                                            "x1": {"type": "number"},
                                            "y1": {"type": "number"}
                                        }
                                    },
                                    "fonts": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "font_sizes": {
                                        "type": "array",
                                        "items": {"type": "number"}
                                    }
                                }
                            }
                        },
                        "images": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["page", "image_id"],
                                "properties": {
                                    "page": {"type": "integer", "minimum": 1},
                                    "image_id": {"type": "string"},
                                    "width": {"type": "integer"},
                                    "height": {"type": "integer"},
                                    "colorspace": {"type": "string"},
                                    "format": {"type": "string"}
                                }
                            }
                        },
                        "tables": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["page", "table_id", "type"],
                                "properties": {
                                    "page": {"type": "integer", "minimum": 1},
                                    "table_id": {"type": "string"},
                                    "type": {"type": "string"},
                                    "rows": {"type": "integer", "minimum": 0},
                                    "columns": {"type": "integer", "minimum": 0},
                                    "position": {"type": "object"},
                                    "data": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "page_structure": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["page"],
                                "properties": {
                                    "page": {"type": "integer", "minimum": 1},
                                    "dimensions": {
                                        "type": "object",
                                        "properties": {
                                            "width": {"type": "number"},
                                            "height": {"type": "number"}
                                        }
                                    },
                                    "text_coverage": {"type": "number"},
                                    "element_counts": {
                                        "type": "object",
                                        "properties": {
                                            "text_blocks": {"type": "integer"},
                                            "images": {"type": "integer"}
                                        }
                                    },
                                    "layout_type": {
                                        "type": "string",
                                        "enum": ["text_heavy", "image_heavy", "mixed", "standard", "empty"]
                                    }
                                }
                            }
                        }
                    }
                },
                "extraction_summary": {
                    "type": "object",
                    "required": ["processing_complete"],
                    "properties": {
                        "total_text_blocks": {"type": "integer", "minimum": 0},
                        "total_images": {"type": "integer", "minimum": 0},
                        "total_tables": {"type": "integer", "minimum": 0},
                        "processing_complete": {"type": "boolean"}
                    }
                }
            }
        }
        
        # Save the default schema
        self._save_schema()
    
    def _save_schema(self):
        """Save the schema to file"""
        try:
            with open(self.schema_path, 'w') as f:
                json.dump(self._schema, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save schema file: {str(e)}")
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the current schema"""
        return self._schema
    
    def validate(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate data against the schema
        
        Args:
            data: The data to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            jsonschema.validate(instance=data, schema=self._schema)
            return True, ""
        except jsonschema.ValidationError as e:
            return False, str(e)
        except jsonschema.SchemaError as e:
            return False, f"Schema error: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def validate_partial(self, data: Dict[str, Any], path: str = "") -> Tuple[bool, list]:
        """
        Validate data and return detailed validation results
        
        Args:
            data: The data to validate
            path: The JSON path being validated
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            jsonschema.validate(instance=data, schema=self._schema)
            return True, []
        except jsonschema.ValidationError as e:
            # Collect all validation errors
            validator = jsonschema.Draft7Validator(self._schema)
            for error in validator.iter_errors(data):
                error_path = ".".join(str(p) for p in error.absolute_path)
                errors.append({
                    "path": error_path,
                    "message": error.message,
                    "invalid_value": error.instance
                })
            
            return False, errors
        except Exception as e:
            errors.append({
                "path": path,
                "message": str(e),
                "invalid_value": None
            })
            return False, errors
    
    def get_schema_summary(self) -> Dict[str, Any]:
        """Get a summary of the schema requirements"""
        def extract_properties(obj, path=""):
            """Recursively extract property information"""
            if not isinstance(obj, dict):
                return {}
            
            properties = {}
            
            if "properties" in obj:
                for prop_name, prop_def in obj["properties"].items():
                    prop_path = f"{path}.{prop_name}" if path else prop_name
                    prop_info = {
                        "type": prop_def.get("type", "unknown"),
                        "required": prop_name in obj.get("required", []),
                        "path": prop_path
                    }
                    
                    if "enum" in prop_def:
                        prop_info["allowed_values"] = prop_def["enum"]
                    
                    properties[prop_path] = prop_info
                    
                    # Recursively process nested objects
                    if prop_def.get("type") == "object":
                        nested = extract_properties(prop_def, prop_path)
                        properties.update(nested)
                    elif prop_def.get("type") == "array" and "items" in prop_def:
                        if prop_def["items"].get("type") == "object":
                            nested = extract_properties(prop_def["items"], f"{prop_path}[]")
                            properties.update(nested)
            
            return properties
        
        return {
            "title": self._schema.get("title", ""),
            "description": self._schema.get("description", ""),
            "required_sections": self._schema.get("required", []),
            "properties": extract_properties(self._schema)
        }
