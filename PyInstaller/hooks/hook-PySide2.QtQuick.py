#-----------------------------------------------------------------------------
# Copyright (c) 2013-2019, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

import os

from PyInstaller.utils import misc
from PyInstaller import log as logging
from PyInstaller.utils.hooks.qt import pyside2_library_info

logger = logging.getLogger(__name__)


def qt5_qml_dir():
    qmldir = pyside2_library_info.location['Qml2ImportsPath']
    if not qmldir:
        logger.error('Cannot find QT_INSTALL_QML directory')
    elif not os.path.exists(qmldir):
        logger.error("Directory QT_INSTALL_QML: %s doesn't exist", qmldir)

    qmldir = os.path.normpath(qmldir)
    return qmldir


def qt5_qml_data(qmldir, directory):
    """
    Return Qml library directory formatted for data.
    """
    return os.path.join(qmldir, directory), os.path.join('qml', directory)


def qt5_qml_plugins_binaries(qmldir, directory):
    """
    Return list of dynamic libraries formatted for mod.binaries.
    """
    binaries = []

    qt5_qml_plugin_dir = os.path.join(qmldir, directory)
    files = misc.dlls_in_subdirs(qt5_qml_plugin_dir)

    for f in files:
        relpath = os.path.relpath(f, qmldir)
        instdir, file = os.path.split(relpath)
        instdir = os.path.join("qml", instdir)
        logger.debug("qt5_qml_plugins_binaries installing %s in %s",
                     f, instdir)
        binaries.append((f, instdir))
    return binaries


def qt5_qml_plugins_datas(qmldir, directory):
    """
    Return list of data files for ``mod.binaries. (qmldir, *.qmltypes)``
    """
    datas = []

    qt5_qml_plugin_dir = os.path.join(qmldir, directory)

    files = []
    for root, _dirs, _files in os.walk(qt5_qml_plugin_dir):
        files.extend(misc.files_in_dir(root, ["qmldir", "*.qmltypes"]))

    for f in files:
        relpath = os.path.relpath(f, qmldir)
        instdir, file = os.path.split(relpath)
        instdir = os.path.join("qml", instdir)
        logger.debug("qt5_qml_plugins_datas installing %s in %s",
                     f, instdir)
        datas.append((f, instdir))
    return datas


hiddenimports = ['PySide2.QtCore',
                 'PySide2.QtQml',
                 'PySide2.QtGui',
                 'PySide2.QtNetwork'
                 ]

# TODO: we should parse the Qml files to see what we need to import.
dirs = ['Qt',
        # 'QtAudioEngine',
        # 'QtGraphicalEffects',
        # 'QtMultiMedia',
        'Qt3D',
        'QtQml',
        'QtQuick',
        'QtQuick.2',
        # 'QtSensors',
        # 'QtTest'
        ]

qmldir = qt5_qml_dir()

# Add base qml directories
datas = [qt5_qml_data(qmldir, dir) for dir in dirs]

# Add qmldir and *.qmltypes files
for dir in dirs:
    datas.extend(qt5_qml_plugins_datas(qmldir, dir))

# Add binaries
binaries = []
for dir in dirs:
    binaries.extend(qt5_qml_plugins_binaries(qmldir, dir))
