# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys,os
import sysconfig,glob,json,shutil
path_info = json.load(open('path.cfg'))
ue4path=path_info['UE4']

libdir=sysconfig.get_config_var('LIBPL')
libfile=sysconfig.get_config_var('LDLIBRARY')
include_path=sysconfig.get_path('include')
file_dir=os.path.abspath(os.path.dirname(__file__))

pfile=glob.glob(path_info['project_path']+'/*.uproject')[0]
pdata=json.load(open(pfile))
pname=pdata['Modules'][0]['Name']
prj_src_path=path_info['project_path']+'/Source/'+pname
print(prj_src_path)
dest_src_dir=prj_src_path+'/PyServer'
if os.path.isdir(dest_src_dir):
    shutil.rmtree(dest_src_dir)
os.mkdir(dest_src_dir)
src_files=glob.glob('src/cpp/*.cpp')+glob.glob('src/cpp/*.h')
for fl in src_files:
    open(dest_src_dir+'/'+os.path.basename(fl),'wb').write(open(fl).read().replace('PyServerPrivatePCH.h',pname+'.h').encode())
    


fd=open(dest_src_dir+'/PyConfig.h','w')
print('//this is autogenerated file by build.py Dont Edit!!!',file=fd)
print('#pragma once',file=fd)
assert(os.path.isfile(libdir+'/'+libfile))
print('#define PYTHON_LIB "'+libdir+'/'+libfile+'"',file=fd)
print('#define SYSPATH "'+file_dir+'/src"',file=fd)
assert(os.path.isfile(include_path+'/Python.h'))
print('#include "'+include_path+'/Python.h"',file=fd)
fd.close()
#print('}',file=fd)
#assert(os.system("python3 -m compileall .")==0) #saves time incase of syntax errors in python files
#sys.exit(0)

#trying to guess project name and project file

if 1:
    os.system("mono "+ue4path+'/Engine/Binaries/DotNET/UnrealBuildTool.exe '+pname+' Development Linux -project="'+pfile+\
    '" -editorrecompile -progress -noubtmakefiles -NoHotReloadFromIDE')

fd=open(path_info['project_path']+'/run.sh','w')
print('#!/bin/bash',file=fd)
print('#This is auto generated script Don\'t Edit!!!',file=fd)
print('cd '+ue4path,file=fd)
print('export PATH_FILE='+os.path.abspath('path.cfg'),file=fd)
print('Engine/Binaries/Linux/UE4Editor "'+pfile+'" -nocore -project='+pfile,file=fd)
fd.close()
assert(os.system('chmod +x '+path_info['project_path']+'/run.sh')==0)
# /local/UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool.exe testprj7_14_4 Development Linux -project="/project_files/testprj7_14_4/testprj7_14_4.uproject" -editorrecompile -progress -noubtmakefiles -NoHotReloadFromIDE
#	mono /local/ori/GameEngines/UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool.exe testplugin Development Linux -project="/local/learn/ur4/testplugin/testplugin.uproject" -editorrecompile -progress -noubtmakefiles -NoHotReloadFromIDE
