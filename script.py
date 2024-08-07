import os

# Define the directory structure
structure = {
        'app': [
            '__init__.py',
            'main.py',
            'data_processing.py',
            'ner.py',
            'visualization.py',
            'utils.py'
        ],
        'models': [
            '__init__.py',
            'model_setup.py'
        ],
        'tests': [
            '__init__.py',
            'test_data_processing.py',
            'test_ner.py',
            'test_visualization.py'
        ],
        'static': {
            'css': [],
            'js': [],
            'images': []
        },
        'requirements.txt': None,
        'README.md': None,
        '.gitignore': None
    }

def create_structure(base_path, structure):
    for key, value in structure.items():
        path = os.path.join(base_path, key)
        if isinstance(value, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, value)
        elif isinstance(value, list):
            os.makedirs(path, exist_ok=True)
            for file_name in value:
                open(os.path.join(path, file_name), 'w').close()
        elif value is None:
            open(path, 'w').close()

# Create the directory structure
create_structure('.', structure)

print("Directory structure created successfully.")
