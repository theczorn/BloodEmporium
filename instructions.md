If you are a user reading this file, you are in the wrong place!
Please download the non-source code archive from https://github.com/IIInitiationnn/BloodEmporium/releases

# Local Dev Install Steps (Powershell)
1. Install [Python](https://www.python.org/downloads/)
1. In terminal, execute `pip install pipreqs`
1. In terminal, execute `pip install pyinstaller`
1. In terminal, execute `pip install -r ./requirements.txt`

# Compilation (Powershell)
1. Execute `pipreqs . --force` to update our `requirements.txt` package file
1. Enable execution for the terminal: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
1. .\venv\Scripts\activate
1. Execute  
    `.\compile.sh \<version_here> [optional: "dev"]`  
    OR  
    `.\compile-onefile.sh \<version_here> [optional: "dev"]`  
1. Disable execution for the terminal: `Set-ExecutionPolicy Restricted -Scope CurrentUser`

# New Content
- add to killers in db
### Killer (Addons)
- add addons unlockables in db
- add addons to assets/<killer>
### Killer + Survivor (Perks)
- add perks to unlockables in db
- add perks to assets/killer and assets/survivor
OTHERS
- new maps (offerings), generic perks etc to look out for

- update preference profiles