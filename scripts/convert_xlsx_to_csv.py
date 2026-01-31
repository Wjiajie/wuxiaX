import os
import glob
import sys
import subprocess

def install(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def convert_xlsx_to_csv(directory):
    # Try importing pandas and openpyxl, install if missing
    try:
        import pandas as pd
    except ImportError:
        print("Pandas not found. Installing pandas and openpyxl...")
        try:
            install("pandas")
            install("openpyxl")
            import pandas as pd
        except Exception as e:
            print(f"Failed to install dependencies: {e}")
            return

    try:
        import openpyxl
    except ImportError:
         print("Openpyxl not found. Installing...")
         install("openpyxl")

    # Search for xlsx files recursively? User said "put in same directory as source".
    # We will search in the given directory.
    xlsx_files = glob.glob(os.path.join(directory, "*.xlsx"))
    
    if not xlsx_files:
        print(f"No .xlsx files found in {directory}")
        return

    print(f"Found {len(xlsx_files)} files in {directory}. Starting conversion...")

    for file_path in xlsx_files:
        try:
            print(f"Processing {file_path}...")
            # Read excel
            # Using openpyxl engine explicitly
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # Construct csv path
            csv_path = os.path.splitext(file_path)[0] + ".csv"
            
            # Save to csv with utf-8-sig for Excel compatibility (Chinese characters)
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"Successfully converted to {csv_path}")
        except Exception as e:
            print(f"Failed to convert {file_path}: {e}")

if __name__ == "__main__":
    # Default target directory
    target_dir = r"c:\Users\jiaji\Documents\github-project\wuxiaX\河洛参考资料"
    
    # Allow overriding via command line argument
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    
    if os.path.exists(target_dir):
        convert_xlsx_to_csv(target_dir)
    else:
        print(f"Directory not found: {target_dir}")
