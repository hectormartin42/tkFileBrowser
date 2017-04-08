#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tkFileBrowser - Alternative to filedialog for Tkinter
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkFileBrowser is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkFileBrowser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


The icons are modified versions of icons from the elementary project
(the xfce fork to be precise https://github.com/shimmerproject/elementary-xfce)
Copyright 2007-2013 elementary LLC.


Constants and functions
"""


import locale
import time
import os
from math import log10

PATH = os.path.dirname(__file__)

### images
IM_HOME = os.path.join(PATH, "images", "home.png")
IM_FOLDER = os.path.join(PATH, "images", "dossier.png")
IM_FOLDER_LINK = os.path.join(PATH, "images", "dossier_link.png")
IM_NEW = os.path.join(PATH, "images", "new_folder.png")
IM_FILE = os.path.join(PATH, "images", "file.png")
IM_FILE_LINK = os.path.join(PATH, "images", "file_link.png")
IM_DRIVE = os.path.join(PATH, "images", "drive.png")


### translation
lang = locale.getdefaultlocale()[0][:2]

EN = {}
FR = {"B": "octets", "MB": "Mo", "kB": "ko", "GB": "Go", "TB": "To",
      "Name: ": "Nom : ", "Folder: ": "Dossier : ", "Size": "Taille",
      "Modified": "Modifié", "Save": "Enregistrer", "Open": "Ouvrir",
      "Cancel": "Annuler", "Confirmation": "Confirmation", "Today": "Aujourd'hui",
      "The file {file} already exists, do you want to replace it?": "Le fichier {file} existe déjà, voulez-vous le remplacer ?",
      "Shortcuts": "Raccourcis", "Save As": "Enregistrer sous"}
LANGUAGES = {"fr": FR, "en": EN}
if lang == "fr":
    TR = LANGUAGES["fr"]
else:
    TR = LANGUAGES["en"]


def _(text):
    """ translation function """
    return TR.get(text, text)

SIZES = [(_("B"), 1), ("kB", 1e3), ("MB", 1e6), ("GB", 1e9), ("TB", 1e12)]

### locale settings for dates
locale.setlocale(locale.LC_ALL, "")
TODAY = time.strftime("%x")
YEAR = time.strftime("%Y")
DAY = int(time.strftime("%j"))

### functions
def add_trace(variable, mode, callback):
    """ ensure compatibility with old and new trace method
        mode: "read", "write", "unset" (new syntax)
    """
    try:
        variable.trace_add(mode, callback)
    except AttributeError:
        # fallback to old method
        variable.trace(mode[0], callback)

def get_modification_date(file):
    tps = time.localtime(os.path.getmtime(file))
    date = time.strftime("%x", tps)
    if date == TODAY:
        date = _("Today") + time.strftime(" %H:%M", tps)
    elif time.strftime("%Y", tps) == YEAR and (DAY - int(time.strftime("%j", tps))) < 7:
        date = time.strftime("%A %H:%M", tps)
    return date

def get_size(file):
    size_o = os.path.getsize(file)
    if size_o > 0:
        m = int(log10(size_o)//3)
        if m < len(SIZES):
            unit, div = SIZES[m]
        else:
            unit, div = SIZES[-1]
        size = "%s %s" % (locale.format("%.1f", size_o/div), unit)
    else:
        size = "0 " + _("B")
    return size