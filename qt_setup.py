import os, sys


project = 'gui'

def ui_to_py():
    pyuic5 = 'pyuic5.exe'
    return '{0} {1}.ui -o {1}.py'.format(pyuic5, project)

def update_resources():
    resource = 'resource'
    pyrcc5 = 'pyrcc5.exe'
    return '{0} {1}.qrc -o {1}_rc.py'.format(pyrcc5, resource)

def port_webengine():
    with open(project+'.py', 'r') as fp:
        filedata = fp.read()

    replacements = {'QtWebKitWidgets': 'QtWebEngineWidgets',
                    'QWebView':        'QWebEngineView',
                    }

    for old, new in replacements.items():
        filedata = filedata.replace(old, new)

    with open(project+'.py', 'w') as fp:
      fp.write(filedata)


if __name__ == '__main__':
    os.system(update_resources())
    os.system(ui_to_py())
    port_webengine()
