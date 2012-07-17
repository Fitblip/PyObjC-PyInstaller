#!/usr/bin/env python
#
# Automatically build spec files containing a description of the project
#
# Copyright (C) 2005, Giovanni Bajo
# Based on previous work under copyright (c) 2002 McMillan Enterprises, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import sys, os

from PyInstaller import HOMEPATH
from PyInstaller import is_win, is_cygwin, is_darwin


onefiletmplt = """# -*- mode: python -*-
a = Analysis(%(scripts)s,
             pathex=%(pathex)s,
             hiddenimports=%(hiddenimports)r,
             hookspath=%(hookspath)r)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join(%(distdir)s, '%(exename)s'),
          debug=%(debug)s,
          strip=%(strip)s,
          upx=%(upx)s,
          console=%(console)s %(exe_options)s)
"""

onefilepyobjc = """# -*- mode: python -*-
a = Analysis(%(scripts)s,
             pathex=%(pathex)s,
             hiddenimports=%(hiddenimports)r,
             hookspath=%(hookspath)r)
a.datas += [
                ('bridge/AddressBook.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/AddressBook/PyObjC.bridgesupport','DATA'),
                ('bridge/AppKit.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/AppKit/PyObjC.bridgesupport','DATA'),
                ('bridge/AppleScriptKit.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/AppleScriptKit/PyObjC.bridgesupport','DATA'),
                ('bridge/Automator.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Automator/PyObjC.bridgesupport','DATA'),
                ('bridge/CalendarStore.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/CalendarStore/PyObjC.bridgesupport','DATA'),
                ('bridge/CFNetwork.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/CFNetwork/PyObjC.bridgesupport','DATA'),
                ('bridge/Collaboration.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Collaboration/PyObjC.bridgesupport','DATA'),
                ('bridge/CoreData.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/CoreData/PyObjC.bridgesupport','DATA'),
                ('bridge/CoreFoundation.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/CoreFoundation/PyObjC.bridgesupport','DATA'),
                ('bridge/CoreText.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/CoreText/PyObjC.bridgesupport','DATA'),
                ('bridge/DictionaryServices.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/DictionaryServices/PyObjC.bridgesupport','DATA'),
                ('bridge/ExceptionHandling.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/ExceptionHandling/PyObjC.bridgesupport','DATA'),
                ('bridge/Foundation.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Foundation/PyObjC.bridgesupport','DATA'),
                ('bridge/FSEvents.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/FSEvents/PyObjC.bridgesupport','DATA'),
                ('bridge/InputMethodKit.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/InputMethodKit/PyObjC.bridgesupport','DATA'),
                ('bridge/InstallerPlugins.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/InstallerPlugins/PyObjC.bridgesupport','DATA'),
                ('bridge/InstantMessage.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/InstantMessage/PyObjC.bridgesupport','DATA'),
                ('bridge/InterfaceBuilderKit.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/InterfaceBuilderKit/PyObjC.bridgesupport','DATA'),
                ('bridge/JavaScriptCore.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/JavaScriptCore/PyObjC.bridgesupport','DATA'),
                ('bridge/LatentSemanticMapping.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/LatentSemanticMapping/PyObjC.bridgesupport','DATA'),
                ('bridge/LaunchServices.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/LaunchServices/PyObjC.bridgesupport','DATA'),
                ('bridge/Message.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Message/PyObjC.bridgesupport','DATA'),
                ('bridge/PreferencePanes.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/PreferencePanes/PyObjC.bridgesupport','DATA'),
                ('bridge/PubSub.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/PubSub/PyObjC.bridgesupport','DATA'),
                ('bridge/QTKit.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/QTKit/PyObjC.bridgesupport','DATA'),
                ('bridge/Quartz.CoreGraphics.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Quartz/CoreGraphics/PyObjC.bridgesupport','DATA'),
                ('bridge/Quartz.CoreVideo.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Quartz/CoreVideo/PyObjC.bridgesupport','DATA'),
                ('bridge/Quartz.ImageIO.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Quartz/ImageIO/PyObjC.bridgesupport','DATA'),
                ('bridge/Quartz.ImageKit.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Quartz/ImageKit/PyObjC.bridgesupport','DATA'),
                ('bridge/Quartz.PDFKit.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Quartz/PDFKit/PyObjC.bridgesupport','DATA'),
                ('bridge/Quartz.QuartzComposer.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Quartz/QuartzComposer/PyObjC.bridgesupport','DATA'),
                ('bridge/Quartz.QuartzCore.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Quartz/QuartzCore/PyObjC.bridgesupport','DATA'),
                ('bridge/Quartz.QuartzFilters.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/Quartz/QuartzFilters/PyObjC.bridgesupport','DATA'),
                ('bridge/ScreenSaver.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/ScreenSaver/PyObjC.bridgesupport','DATA'),
                ('bridge/ScriptingBridge.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/ScriptingBridge/PyObjC.bridgesupport','DATA'),
                ('bridge/SearchKit.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/SearchKit/PyObjC.bridgesupport','DATA'),
                ('bridge/SyncServices.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/SyncServices/PyObjC.bridgesupport','DATA'),
                ('bridge/SystemConfiguration.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/SystemConfiguration/PyObjC.bridgesupport','DATA'),
                ('bridge/WebKit.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/WebKit/PyObjC.bridgesupport','DATA'),
                ('bridge/XgridFoundation.PyObjC.bridgesupport','/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC/XgridFoundation/PyObjC.bridgesupport','DATA'),
           ]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join(%(distdir)s, '%(exename)s'),
          debug=%(debug)s,
          strip=%(strip)s,
          upx=%(upx)s,
          console=%(console)s %(exe_options)s)
"""

onedirtmplt = """# -*- mode: python -*-
a = Analysis(%(scripts)s,
             pathex=%(pathex)s,
             hiddenimports=%(hiddenimports)r,
             hookspath=%(hookspath)r)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join(%(builddir)s, '%(exename)s'),
          debug=%(debug)s,
          strip=%(strip)s,
          upx=%(upx)s,
          console=%(console)s %(exe_options)s)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=%(strip)s,
               upx=%(upx)s,
               name=os.path.join(%(distdir)s, '%(name)s'))
"""

comsrvrtmplt = """# -*- mode: python -*-
a = Analysis(%(scripts)s,
             pathex=%(pathex)s,
             hiddenimports=%(hiddenimports)r,
             hookspath=%(hookspath)r)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join(%(builddir)s, '%(exename)s'),
          debug=%(debug)s,
          strip=%(strip)s,
          upx=%(upx)s,
          console=%(console)s %(exe_options)s)
dll = DLL(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join(%(builddir)s, '%(dllname)s'),
          debug=%(debug)s)
coll = COLLECT(exe, dll,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=%(strip)s,
               upx=%(upx)s,
               name=os.path.join(%(distdir)s, '%(name)s'))
"""

bundleexetmplt = """app = BUNDLE(exe,
             name=os.path.join(%(distdir)s, '%(exename)s.app'))
"""

bundletmplt = """app = BUNDLE(coll,
             name=os.path.join(%(distdir)s, '%(name)s.app'))
"""


def quote_win_filepath( path ):
    # quote all \ with another \ after using normpath to clean up the path
    return os.path.normpath(path).replace('\\', '\\\\')

# Support for trying to avoid hard-coded paths in the .spec files.
# Eg, all files rooted in the Installer directory tree will be
# written using "HOMEPATH", thus allowing this spec file to
# be used with any Installer installation.
# Same thing could be done for other paths too.
path_conversions = (
    (HOMEPATH, "HOMEPATH"),
    )

def make_variable_path(filename, conversions = path_conversions):
    for (from_path, to_name) in conversions:
        assert os.path.abspath(from_path)==from_path, (
            "path '%s' should already be absolute" % from_path)
        if filename[:len(from_path)] == from_path:
            rest = filename[len(from_path):]
            if rest[0] in "\\/":
                rest = rest[1:]
            return to_name, rest
    return None, filename

# An object used in place of a "path string" which knows how to repr()
# itself using variable names instead of hard-coded paths.
class Path:
    def __init__(self, *parts):
        self.path = apply(os.path.join, parts)
        self.variable_prefix = self.filename_suffix = None
    def __repr__(self):
        if self.filename_suffix is None:
            self.variable_prefix, self.filename_suffix = make_variable_path(self.path)
        if self.variable_prefix is None:
            return repr(self.path)
        return "os.path.join(" + self.variable_prefix + "," + repr(self.filename_suffix) + ")"

def __add_options(parser):
    """
    Add the `Makespec` options to a option-parser instance or a
    option group.
    """
    g = parser.add_option_group('What to generate')
    g.add_option("-F", "--onefile", dest="onefile",
                 action="store_true", default=False,
                 help="create a single file deployment")
    g.add_option("-D", "--onedir", dest="onefile",
                 action="store_false",
                 help="create a single directory deployment (default)")
    g.add_option("-o", "--out",
                 dest="workdir", metavar="DIR",
                 help="generate the spec file in the specified directory "
                      "(default: current directory)")
    g.add_option("-n", "--name",
                 help="name to assign to the project "
                      "(default: first script's basename)")

    g = parser.add_option_group('What to bundle, where to search')
    g.add_option("-p", "--paths", default=[], dest="pathex",
                 metavar="DIR", action="append",
                 help="set base path for import (like using PYTHONPATH). "
                      "Multiple directories are allowed, separating them "
                      "with %s, or using this option multiple times"
                      % repr(os.pathsep))
    g.add_option('--hidden-import',
                 action='append',
                 metavar="MODULENAME", dest='hiddenimports',
                 help='import hidden in the script(s). This option can '
                 'be used multiple times.')
    g.add_option("--additional-hooks-dir", action="append", dest="hookspath",
                 help="additional path to search for hooks "
                      "(may be given several times)")    

    g = parser.add_option_group('How to generate')
    g.add_option("-d", "--debug", action="store_true", default=False,
                 help=("use the debug (verbose) build of the executable for "
                       "packaging. This will make the packaged executable be "
                       "more verbose when run."))
    g.add_option("-s", "--strip", action="store_true",
                 help="strip the exe and shared libs "
                      "(don't try this on Windows)")
    g.add_option("--noupx", action="store_true", default=False,
                 help="do not use UPX even if available (works differently "
                      "between Windows and *nix)")
    #p.add_option("-Y", "--crypt", metavar="FILE",
    #             help="encrypt pyc/pyo files")

    g = parser.add_option_group('Windows and Mac OS X specific options')
    g.add_option("-c", "--console", "--nowindowed", dest="console",
                 action="store_true", default=True,
                 help="use a console subsystem executable (default)")
    g.add_option("-w", "--windowed", "--noconsole", dest="console",
                 action="store_false",
                 help="use a windowed subsystem executable, which on Windows "
                      "does not open the console when the program is launched."
                      'Mandatory whe creating .app bundle on Mac OS X')
    g.add_option("-i", "--icon", dest="icon_file",
                 metavar="FILE.ICO or FILE.EXE,ID or FILE.ICNS",
                 help="If FILE is an .ico file, add the icon to the final "
                      "executable. Otherwise, the syntax 'file.exe,id' to "
                      "extract the icon with the specified id "
                      "from file.exe and add it to the final executable. "
                      "If FILE is an .icns file, add the icon to the final "
                      ".app bundle on Mac OS X (for Mac not yet implemented)")
    g.add_option("-P","--PyObjC","--objc",dest="uses_PyObjC",
                 action="store_true", default=False,
                 help="Use this flag to include the necessary .bridgesupport "
                      "files needed by PyObjC properly use the module. Doesn't "
                      "work without a patched version of PyObjC found at "
                      "https://github.com/Fitblip/PyObjC-PyInstaller")

    g = parser.add_option_group('Windows specific options')
    g.add_option("--version-file",
                 dest="version_file", metavar="FILE",
                 help="add a version resource from FILE to the exe")
    g.add_option("-m", "--manifest", metavar="FILE or XML",
                 help="add manifest FILE or XML to the exe")
    g.add_option("-r", "--resource", default=[], dest="resources",
                 metavar="FILE[,TYPE[,NAME[,LANGUAGE]]]", action="append",
                 help="add/update resource of the given type, name and language "
                      "from FILE to the final executable. FILE can be a "
                      "data file or an exe/dll. For data files, atleast "
                      "TYPE and NAME need to be specified, LANGUAGE defaults "
                      "to 0 or may be specified as wildcard * to update all "
                      "resources of the given TYPE and NAME. For exe/dll "
                      "files, all resources from FILE will be added/updated "
                      "to the final executable if TYPE, NAME and LANGUAGE "
                      "are omitted or specified as wildcard *."
                      "Multiple resources are allowed, using this option "
                      "multiple times.")


def main(scripts, name=None, onefile=0,
         console=True, debug=False, strip=0, noupx=0, comserver=0,
         workdir=None, pathex=[], version_file=None,
         icon_file=None, manifest=None, resources=[], crypt=None,
         hiddenimports=None,uses_PyObjC=False, hookspath=None, **kwargs):
    if not name:
        name = os.path.splitext(os.path.basename(scripts[0]))[0]

    distdir = "dist"
    builddir = os.path.join('build', 'pyi.' + sys.platform, name)
    pathex = pathex[:]
    if workdir is None:
        workdir = os.getcwd()
        pathex.append(workdir)
    else:
        pathex.append(os.getcwd())
    if workdir == HOMEPATH:
        workdir = os.path.join(HOMEPATH, name)
    if not os.path.exists(workdir):
        os.makedirs(workdir)
    exe_options = ''
    if version_file:
        exe_options = "%s, version='%s'" % (exe_options, quote_win_filepath(version_file))
    if icon_file:
        exe_options = "%s, icon='%s'" % (exe_options, quote_win_filepath(icon_file))
    if manifest:
        if "<" in manifest:
            # Assume XML string
            exe_options = "%s, manifest='%s'" % (exe_options, manifest.replace("'", "\\'"))
        else:
            # Assume filename
            exe_options = "%s, manifest='%s'" % (exe_options, quote_win_filepath(manifest))
    if resources:
        resources = map(quote_win_filepath, resources)
        exe_options = "%s, resources=%s" % (exe_options, repr(resources))

    hiddenimports = hiddenimports or []
    scripts = map(Path, scripts)

    d = {'scripts':scripts,
         'pathex' :pathex,
         'hiddenimports': hiddenimports,
         'hookspath': hookspath,
         #'exename': '',
         'name': name,
         'distdir': repr(distdir),
         'builddir': repr(builddir),
         'debug': debug,
         'strip': strip,
         'upx' : not noupx,
         'crypt' : repr(crypt),
         'crypted': crypt is not None,
         'console': console or debug,
         'uses_PyObjC': uses_PyObjC,
         'exe_options': exe_options}

    if is_win or is_cygwin:
        d['exename'] = name+'.exe'
        d['dllname'] = name+'.dll'
    else:
        d['exename'] = name

    # only Windows and Mac OS X distinguish windowed and console apps
    if not is_win and not is_darwin:
        d['console'] = True

    specfnm = os.path.join(workdir, name+'.spec')
    specfile = open(specfnm, 'w')
    if onefile and uses_PyObjC:
        specfile.write(onefilepyobjc % d)
    elif onefile and not uses_PyObjC:
        specfile.write(onefiletmplt % d)
        if not console:
            specfile.write(bundleexetmplt % d)
    elif comserver:
        specfile.write(comsrvrtmplt % d)
        if not console:
            specfile.write(bundletmplt % d)
    else:
        specfile.write(onedirtmplt % d)
        if not console:
            specfile.write(bundletmplt % d)
    specfile.close()
    return specfnm

