# Python Setup & Environment Notes

---

## 1. Install Python 3.11+

1. Download from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
2. Verify installation:

```bash
python3 --version
# or
python --version


brew install python


# Create a virtual environment
python3 -m venv ai-env

# Activate the virtual environment
# macOS/Linux
source ai-env/bin/activate

# Windows (PowerShell)
.\ai-env\Scripts\activate

# Deactivate
deactivate


first_project/
├── ai-env/                 # Virtual environment
├── src/
│   └── main.py             # Main script
├── Day2/task/students.csv  # Data file
├── .gitignore              # Ignore env, IDE files
└── README.md               # Project documentation



# Install packages
pip install fastapi uvicorn pandas

# Verify installation
pip list

# Freeze dependencies
pip freeze > requirements.txt

# Install dependencies from requirements.txt
pip install -r requirements.txt
