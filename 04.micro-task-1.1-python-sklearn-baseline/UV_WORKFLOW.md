# UV Quick Workflow Guide

> **Quick Reference** - For first-time setup, see [README.md](README.md)

This is a quick reference guide for daily workflow with `uv`. For complete setup instructions including direnv configuration and Windows support, see the main README.

## 🚀 Basic Workflow

### 1. **Create and activate virtual environment**

**Mac/Linux/WSL:**
```bash
# Create venv
uv venv

# Activate the environment
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
uv venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
uv venv
.venv\Scripts\activate.bat
```

### 2. **Install dependencies from requirements.txt**
```bash
# Install all packages from requirements.txt
uv pip install -r requirements.txt

# Or install packages directly
uv pip install scikit-learn joblib
```

### 3. **Run your scripts**
```bash
# With venv activated, just run normally
python train.py
python predict.py
```

### 4. **Add new dependencies**
```bash
# Install a new package
uv pip install pandas

# Update requirements.txt
uv pip freeze > requirements.txt
```

## 📋 Common Commands

```bash
# Create venv
uv venv

# Install from requirements.txt
uv pip install -r requirements.txt

# Install a package
uv pip install package-name

# List installed packages
uv pip list

# Show package info
uv pip show scikit-learn

# Uninstall a package
uv pip uninstall package-name

# Deactivate venv (when activated)
deactivate  # Works on all platforms
```

## ⚡ Pro Tips

1. **Sync dependencies**: `uv pip sync requirements.txt` (removes packages not in requirements)
2. **Faster installs**: uv is 10-100x faster than pip
3. **No activation needed**: You can run `uv run python train.py` without activating venv
4. **Lock file**: Consider using `uv pip compile requirements.txt` to generate a lock file

## 🎯 Auto-Activation with direnv

**If direnv is configured** (Mac/Linux/WSL), the environment activates automatically when you `cd` into this directory.

### How it works:
- **No manual activation needed** - just `cd` into the project directory
- **Auto-deactivates** when you leave the directory
- Works with `.envrc` file in this directory

### Manual activation (if direnv not available):

**Mac/Linux/WSL:**
```bash
source .venv/bin/activate
deactivate
```

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
deactivate
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
deactivate
```

## 🔄 Alternative: Standard Python venv

If you prefer using standard Python instead of `uv`:

**Mac/Linux/WSL:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows PowerShell:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Windows CMD:**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

## 📚 More Information

- **First-time setup**: See [README.md](README.md) for complete installation instructions
- **Windows support**: See README.md for Windows 11 specific instructions
- **direnv setup**: See README.md for auto-activation configuration

