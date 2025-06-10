# Integer LabelMe Features 
### (and development notes)

#### Simple features:

- [ ] Log.txt file

#### Complex features:

- [ ] Remove label feature

---
## Unrelated development/setup notes
#### Python version
- Installed **version 3.9.9**
- Check install with `py -3.9 --version`

*To make sure this version (3.9) is not set as my primary version of python on windows, I had to move the '39' paths beneath my main paths in environment variables*

#### Python virtual environment
```bash
py -3.9 -m venv venv39
venv39\Scripts\activate
```

#### Installing dependencies
```bash
python -m pip install --upgrade pip
pip install -e .
```
*This ultizes pyproject.toml (where dependencies are located)
installing newer version of pip for the venv is important, editable (-e) install of libaries doesn't work with older versions*

###### Run labelme in your venv (with ```labelme``` in the command line) to check if dependencies are properly installed

