#!/usr/bin/env python3
import os
import sys

def extract_files_content(root_dir, output_file):
    """
    Extract the content of all files in the given directory structure and write them to a single file.
    Each file's content is preceded by its title (filename) and followed by a separator.
    
    Args:
        root_dir (str): Root directory to start the search from
        output_file (str): Path to the output file
    """
    # Binary and object files to skip
    skip_extensions = {
        '.dll', '.exe', '.pdb', '.cache', '.json', '.endpoints.json',
        '.props', '.targets', '.dgspec.json', '.Up2Date'
    }
    
    # Compiled folders to skip
    skip_folders = {'bin', 'obj'}
    
    with open(output_file, 'w', encoding='utf-8') as outf:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip binary directories
            dirnames[:] = [d for d in dirnames if d not in skip_folders]
            
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                _, ext = os.path.splitext(filename)
                
                # Skip binary files and other non-text files
                if ext in skip_extensions or os.path.getsize(filepath) > 10 * 1024 * 1024:  # Skip files larger than 10MB
                    continue
                
                # Get relative path for cleaner output
                rel_path = os.path.relpath(filepath, root_dir)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Write file header
                    outf.write(f"\n{'='*80}\n")
                    outf.write(f"FILE: {rel_path}\n")
                    outf.write(f"{'='*80}\n\n")
                    
                    # Write file content
                    outf.write(content)
                    
                    # Write separator
                    outf.write(f"\n\n{'#'*80}\n\n")
                except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                    outf.write(f"\n{'='*80}\n")
                    outf.write(f"FILE: {rel_path} (SKIPPED - Binary or unreadable file)\n")
                    outf.write(f"{'='*80}\n\n")
                    outf.write(f"\n\n{'#'*80}\n\n")
                except Exception as e:
                    outf.write(f"\n{'='*80}\n")
                    outf.write(f"FILE: {rel_path} (ERROR: {str(e)})\n")
                    outf.write(f"{'='*80}\n\n")
                    outf.write(f"\n\n{'#'*80}\n\n")

if __name__ == "__main__":
    # Get current directory as default root directory
    root_dir = os.getcwd()
    
    # Default output file name
    output_file = "all_files_content.txt"
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    print(f"Extracting files from {root_dir} to {output_file}...")
    extract_files_content(root_dir, output_file)
    print(f"Done! All file contents have been written to {output_file}")