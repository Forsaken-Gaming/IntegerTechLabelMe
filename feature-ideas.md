# Integer LabelMe Features 
### (and development notes)

#### Simple features:

- [ ] Log.txt file when creating video for additional metrics (label enters/exits frame, unannotated frame, etc.) (simples os opperations, prototype already created)
- [ ] Test threading by saving dummy png/json files from server to local machine to see if it's possible to improve times for video compiling (despite network limitations) (```concurrent.futures import ThreadPoolExecutor```)

#### Complex features:

- [ ] Remove specified label from all frames (or range of frames), working without flaw even if there is multiple labels with the same class name

#### Minor changes that affect no one or anything:

- [ ] --

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
installing newer version of pip for the venv is important, editable install (-e) of libaries doesn't work with older versions*

###### Run labelme in your venv (with ```labelme``` in the command line) to check if dependencies are properly installed

