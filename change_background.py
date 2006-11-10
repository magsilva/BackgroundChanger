#!/usr/bin/python
# -*- coding: latin-1 -*-
#
# change-background.py
#
# A script to change to a random background image
#
# (c) 2004, Davyd Madeley <davyd@madeley.id.au>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2, or (at your option)
#   any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
#
#   Script modified by Marco Aurelio Graciotto Silva <magsilva@gmail.com>
#   Added support for alternative filename's encodings (western and utf8 ones).
#   Recursive search for files suitable for background.


backgrounds = ".backgrounds"
encoding = ("utf8", "iso-8859-1", "latin-1", "ascii")

import gconf
import os
import random
import mimetypes

class GConfClient:
        def __init__(self):
                self.__client__ = gconf.client_get_default()
                self.items = []

        def get_background(self):
                return self.__client__.get_string("/desktop/gnome/background/picture_filename")

        def set_background(self, background):
                # print background
                self.__client__.set_string("/desktop/gnome/background/picture_filename", background)

        def update_available_backgrounds(self, path):
                for root, dirs, files in os.walk(path):
                        for item in files:
                                mimetype = mimetypes.guess_type(item)[0]
                                if mimetype and mimetype.split('/')[0] == "image":
                                          self.items.append(os.path.join(root, item))
                        for item in dirs:
                                self.update_available_backgrounds(os.path.join(root, item))

client = GConfClient()
client.update_available_backgrounds(os.path.join(os.environ["HOME"], backgrounds))

item = random.randint(0, len(client.items) - 1)
current_bg = client.get_background()

filename = ""
while (len(filename) == 0):
        item = random.randint(0, len(client.items) - 1)

        encoding_index = 0
        while (len(filename) == 0 and encoding_index != len(encoding)):
                try:
                        filename = unicode(client.items[item], encoding[encoding_index]).encode('utf-8')
                except UnicodeDecodeError:
                        # print client.items[item]
                        encoding_index = encoding_index + 1 
        
client.set_background(filename)
