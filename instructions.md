# HEY YOU!
If you are a user reading this file, you are in the **wrong place**!  
This area is for developers only.

Please download the [Compiled Appliction](https://github.com/IIInitiationnn/BloodEmporium/releases)
You can look at the [README for details](https://github.com/IIInitiationnn/BloodEmporium/blob/master/README.md)

# Local Dev Install Steps (Powershell)
1. Install [the latest 3.x version of Python](https://www.python.org/downloads/)
1. In terminal, execute `pip install pipreqs` to install the pipreqs requirement generator
1. In terminal, execute `pip install pyinstaller` to install the pyinstaller execution bundler
1. In terminal, execute `pip install -r ./requirements.txt` to pull all project deps down

# Compilation (Powershell)
1. Execute `pipreqs . --force` to update our `requirements.txt` package file
1. Enable execution for the terminal: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
1. Execute `py -m venv '.\venv\Scripts\activate'`
   1. NOTE: Deprecated?
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
### Others
- new maps (offerings), generic perks etc to look out for
- update preference profiles