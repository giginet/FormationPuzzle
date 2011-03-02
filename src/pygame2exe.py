# -*- coding: utf-8 -*-
# make standalone, needs at least pygame-1.5.3 and py2exe-0.3.1
# fixed for py2exe-0.6.x by RyoN3 at 03/15/2006

from distutils.core import setup
import sys, os, pygame, shutil
import py2exe

while 1:
    workdir = raw_input('Input script directry:')
    try:
        os.chdir(workdir)
    except:
        print "Change directry is failed."
        print "Please re-try input directry."
        continue
    print "Setup directry:%s"%os.getcwd()
    break


######
#
script = raw_input('Input starting script:')
icon_file = '../resources/icon16.ico'
optimize = 2
extra_modules = ['pygame.locals']  

###
project_name = 'FormationPuzzle'
description = u'新感覚アクションパズル！' 
version = "0.9.0"              
company_name = "www.kawaz.org"
copy_right = "Kawaz"
pj_name = "FormationPuzzle"
####

dll_excludes = ['SDL_mixer.dll','SDL.dll','SDL_ttf.dll',
                'smpeg.dll',
                'SDL_image.dll','jpeg.dll', 'libogg-0.dll',
                'libpng13.dll', 'libtiff.dll', 'libvorbis-0.dll',
                'libvorbisfile-3.dll', 'zlib1.dll',
                'libpng12-0.dll','libfreetype-6.dll'] 

options = {"py2exe": {"compressed": 1,
                      "optimize"  : optimize,
                      "bundle_files": 2,
                      "dll_excludes": dll_excludes,
                      "packages": ['settings',],
                      }
           }

#
#####


class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)

#use the default pygame icon, if none given
if icon_file is None:
    path = os.path.split(pygame.__file__)[0]
    icon_file = os.path.join(path, 'pygame.ico')
#unfortunately, this cool icon stuff doesn't work in current py2exe :(
#icon_file = ''


#create the proper commandline args
args = ['py2exe']
sys.argv[1:] = args + sys.argv[1:]

target = Target(
                script = script,
                icon_resources = [(1,icon_file)],
                company_name = company_name,
                copyright = copy_right,
                name = pj_name,
                )



#this will create the executable and all dependencies
setup(
      version = version,
      description = description,
      name = project_name,
      options = options,
      zipfile = None,
      windows=[target],
      )

pygamedir = os.path.split(pygame.base.__file__)[0]
for src in dll_excludes:
    f = os.path.join(pygamedir, src)
    d = 'dist'
    print 'copying', f, '->', d
    try:
        shutil.copy(f, d)
    except:
        print 'not found: %s'%src


# end.
