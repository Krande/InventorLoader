import argparse
import os
import sys
import shutil
import traceback

# Adjust path to allow imports if run directly, though -m is preferred
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from acis import Acis
from acis import Acis2Step
from acis import importerUtils

def detect_binary(file_path):
    """
    Detects if the ACIS file is binary or text.
    Binary files usually start with 'ACIS Binary'.
    Text files usually start with version number (e.g., '400 0 1 0').
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(15)
            if b'ACIS Binary' in header:
                return True
            
            # Heuristic: try to decode as ASCII and check for digits/space
            try:
                text = header.decode('ascii')
                # Check if starts with digit (version number) or space
                if text and (text[0].isdigit() or text[0].isspace()):
                    return False
            except UnicodeDecodeError:
                pass
            
            return True # Default to binary if not clear text
    except Exception as e:
        print(f"Warning: Could not detect file type: {e}. Defaulting to Binary.")
        return True

def resolve_nodes(reader):
    """
    Iterates through records in the reader and extracts Body entities.
    """
    bodies = []
    Acis.init() # Clears entities cache
    Acis.setReader(reader)
    
    # Ensure reader has records
    records = reader.getRecords()
    if not records:
        print("No records found in ACIS file.")
        return []

    for record in records:
        if record is None: continue # Handle gaps or None entries
        
        # Stop at history section or end of data
        if record.name in ['Begin-of-ACIS-History-Data', 'End-of-ACIS-History-Section', 'End-of-ACIS-data']:
            break
        
        try:
            entity = Acis.createEntity(record)
            if record.name == 'body':
                bodies.append(entity)
        except Exception as e:
            # Log error but continue processing other records
            print(f"Error creating entity for record index {getattr(record, 'index', '?')}: {e}")
            # traceback.print_exc()
    
    return bodies

def main():
    parser = argparse.ArgumentParser(description='Convert ACIS (.sat) file to STEP (.stp) file.')
    parser.add_argument('input', help='Input ACIS file path')
    parser.add_argument('output', help='Output STEP file path')
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)

    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    # Initialize utilities (sets dump folder based on input)
    importerUtils.setInventorFile(input_path)
    
    # Read ACIS file
    reader = None
    is_binary = detect_binary(input_path)
    
    try:
        if is_binary:
            print(f"Reading '{input_path}' as Binary ACIS...")
            with open(input_path, 'rb') as f:
                reader = Acis.AcisReader(f)
                reader.name = os.path.basename(input_path)
                if not reader.readBinary():
                    print("Failed to read binary ACIS file.")
                    sys.exit(1)
        else:
            print(f"Reading '{input_path}' as Text ACIS...")
            # Use latin-1 to avoid decoding errors, as ACIS text is mostly ASCII but can have extended chars
            with open(input_path, 'r', encoding='latin-1') as f:
                reader = Acis.AcisReader(f)
                reader.name = os.path.basename(input_path)
                if not reader.readText():
                    print("Failed to read text ACIS file.")
                    sys.exit(1)

    except Exception as e:
        print(f"Error reading ACIS file: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    # Extract bodies
    print("Extracting bodies...")
    bodies = resolve_nodes(reader)
    print(f"Found {len(bodies)} bodies.")
    
    if not bodies:
        print("No bodies to export.")
        sys.exit(0)

    # Export to STEP
    print("Converting to STEP...")
    try:
        # Acis2Step.export generates file in dump folder
        generated_step = Acis2Step.export(os.path.basename(input_path), reader.header, bodies)
        
        if generated_step and os.path.exists(generated_step):
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Move to requested output path
            if os.path.exists(output_path):
                os.remove(output_path)
            shutil.move(generated_step, output_path)
            print(f"Successfully created '{output_path}'")
            
            # Optional: Cleanup dump folder
            dump_folder = importerUtils.getDumpFolder()
            if dump_folder and os.path.exists(dump_folder):
                 try:
                     shutil.rmtree(dump_folder)
                 except Exception as e:
                     print(f"Warning: Could not clean up dump folder '{dump_folder}': {e}")
        else:
            print("Error: STEP file was not generated.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error during export: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
