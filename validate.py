#!/usr/bin/env python3
"""
Simple validation script to check Python syntax and basic issues
"""
import ast
import sys
import os

def validate_python_file(filepath):
    """Validate a Python file for syntax errors"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check for syntax errors
        ast.parse(content)
        print(f"✅ {filepath}: Syntax OK")
        return True
        
    except SyntaxError as e:
        print(f"❌ {filepath}: Syntax Error on line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ {filepath}: Error - {e}")
        return False

def main():
    """Main validation function"""
    print("🔍 Running code validation...")
    
    # Find all Python files in the project
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and common build/cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', 'env', 'node_modules']]
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    if not python_files:
        print("⚠️  No Python files found in the project")
        return 1
    
    print(f"Found {len(python_files)} Python files to validate:")
    for file in python_files:
        print(f"  - {file}")
    print()
    
    all_good = True
    
    for file in python_files:
        if not validate_python_file(file):
            all_good = False
    
    if all_good:
        print("\n🎉 All files passed validation!")
        return 0
    else:
        print("\n💥 Some files have issues!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
