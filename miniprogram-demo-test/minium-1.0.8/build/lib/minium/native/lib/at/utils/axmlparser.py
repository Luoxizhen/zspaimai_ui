# -*- coding: utf-8 -*-
"""解析axml格式,copy from androguard
"""
from __future__ import print_function

# This file is part of Androguard.
#
# Copyright (C) 2012, Anthony Desnos <desnos at t0t0.fr>
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from struct import pack, unpack
from xml.sax.saxutils import escape
import sys

from xml.dom import minidom

NS_ANDROID_URI = "http://schemas.android.com/apk/res/android"


def show_Certificate(cert):
    print(
        "Issuer: C=%s, CN=%s, DN=%s, E=%s, L=%s, O=%s, OU=%s, S=%s"
        % (
            cert.issuerC(),
            cert.issuerCN(),
            cert.issuerDN(),
            cert.issuerE(),
            cert.issuerL(),
            cert.issuerO(),
            cert.issuerOU(),
            cert.issuerS(),
        )
    )
    print(
        "Subject: C=%s, CN=%s, DN=%s, E=%s, L=%s, O=%s, OU=%s, S=%s"
        % (
            cert.subjectC(),
            cert.subjectCN(),
            cert.subjectDN(),
            cert.subjectE(),
            cert.subjectL(),
            cert.subjectO(),
            cert.subjectOU(),
            cert.subjectS(),
        )
    )


################################## AXML FORMAT ########################################
# Translated from
# http://code.google.com/p/android4me/source/browse/src/android/content/res/AXmlResourceParser.java

UTF8_FLAG = 0x00000100
CHUNK_STRINGPOOL_TYPE = 0x001C0001
CHUNK_NULL_TYPE = 0x00000000


class StringBlock(object):
    def __init__(self, buff):
        self.start = buff.get_idx()
        self._cache = {}
        self.header_size, self.header = self.skipNullPadding(buff)

        self.chunkSize = unpack("<i", buff.read(4))[0]
        self.stringCount = unpack("<i", buff.read(4))[0]
        self.styleOffsetCount = unpack("<i", buff.read(4))[0]

        self.flags = unpack("<i", buff.read(4))[0]
        self.m_isUTF8 = (self.flags & UTF8_FLAG) != 0

        self.stringsOffset = unpack("<i", buff.read(4))[0]
        self.stylesOffset = unpack("<i", buff.read(4))[0]

        self.m_stringOffsets = []
        self.m_styleOffsets = []
        self.m_charbuff = ""
        self.m_styles = []

        for i in range(0, self.stringCount):
            self.m_stringOffsets.append(unpack("<i", buff.read(4))[0])

        for i in range(0, self.styleOffsetCount):
            self.m_styleOffsets.append(unpack("<i", buff.read(4))[0])

        size = self.chunkSize - self.stringsOffset
        if self.stylesOffset != 0:
            size = self.stylesOffset - self.stringsOffset

        # FIXME
        if (size % 4) != 0:
            print >>sys.stderr, ("ooo")

        self.m_charbuff = buff.read(size)

        if self.stylesOffset != 0:
            size = self.chunkSize - self.stylesOffset

            # FIXME
            if (size % 4) != 0:
                print >>sys.stderr, ("ooo")

            for i in range(0, size / 4):
                self.m_styles.append(unpack("<i", buff.read(4))[0])

    def skipNullPadding(self, buff):
        def readNext(buff, first_run=True):
            header = unpack("<i", buff.read(4))[0]

            if header == CHUNK_NULL_TYPE and first_run:
                print >>sys.stderr, ("Skipping null padding in StringBlock header")
                header = readNext(buff, first_run=False)
            elif header != CHUNK_STRINGPOOL_TYPE:
                print >>sys.stderr, ("Invalid StringBlock header")

            return header

        header = readNext(buff)
        return header >> 8, header & 0xFF

    def getString(self, idx):
        if idx in self._cache:
            return self._cache[idx]

        if idx < 0 or not self.m_stringOffsets or idx >= len(self.m_stringOffsets):
            return ""

        offset = self.m_stringOffsets[idx]

        if self.m_isUTF8:
            self._cache[idx] = self.decode8(offset)
        else:
            self._cache[idx] = self.decode16(offset)

        return self._cache[idx]

    def getStyle(self, idx):
        # FIXME
        return self.m_styles[idx]

    def decode8(self, offset):
        str_len, skip = self.decodeLength(offset, 1)
        offset += skip

        encoded_bytes, skip = self.decodeLength(offset, 1)
        offset += skip

        data = self.m_charbuff[offset : offset + encoded_bytes]

        return self.decode_bytes(data, "utf-8", str_len)

    def decode16(self, offset):
        str_len, skip = self.decodeLength(offset, 2)
        offset += skip

        encoded_bytes = str_len * 2

        data = self.m_charbuff[offset : offset + encoded_bytes]

        return self.decode_bytes(data, "utf-16", str_len)

    def decode_bytes(self, data, encoding, str_len):
        string = data.decode(encoding, "replace")
        if len(string) != str_len:
            print >>sys.stderr, ("invalid decoded string length")
        return string

    def decodeLength(self, offset, sizeof_char):
        length = ord(self.m_charbuff[offset])

        sizeof_2chars = sizeof_char << 1
        fmt_chr = "B" if sizeof_char == 1 else "H"
        fmt = "<2" + fmt_chr

        length1, length2 = unpack(
            fmt, self.m_charbuff[offset : (offset + sizeof_2chars)]
        )

        highbit = 0x80 << (8 * (sizeof_char - 1))

        if (length & highbit) != 0:
            return ((length1 & ~highbit) << (8 * sizeof_char)) | length2, sizeof_2chars
        else:
            return length1, sizeof_char

    def show(self):
        print(
            "StringBlock(%x, %x, %x, %x, %x, %x"
            % (
                self.start,
                self.header,
                self.header_size,
                self.chunkSize,
                self.stringsOffset,
                self.flags,
            )
        )
        for i in range(0, len(self.m_stringOffsets)):
            print(i, repr(self.getString(i)))


ATTRIBUTE_IX_NAMESPACE_URI = 0
ATTRIBUTE_IX_NAME = 1
ATTRIBUTE_IX_VALUE_STRING = 2
ATTRIBUTE_IX_VALUE_TYPE = 3
ATTRIBUTE_IX_VALUE_DATA = 4
ATTRIBUTE_LENGHT = 5

CHUNK_AXML_FILE = 0x00080003
CHUNK_RESOURCEIDS = 0x00080180
CHUNK_XML_FIRST = 0x00100100
CHUNK_XML_START_NAMESPACE = 0x00100100
CHUNK_XML_END_NAMESPACE = 0x00100101
CHUNK_XML_START_TAG = 0x00100102
CHUNK_XML_END_TAG = 0x00100103
CHUNK_XML_TEXT = 0x00100104
CHUNK_XML_LAST = 0x00100104

START_DOCUMENT = 0
END_DOCUMENT = 1
START_TAG = 2
END_TAG = 3
TEXT = 4


class SV(object):
    def __init__(self, size, buff):
        self.__size = size
        self.__value = unpack(self.__size, buff)[0]

    def _get(self):
        return pack(self.__size, self.__value)

    def __str__(self):
        return "0x%x" % self.__value

    def __int__(self):
        return self.__value

    def get_value_buff(self):
        return self._get()

    def get_value(self):
        return self.__value

    def set_value(self, attr):
        self.__value = attr


class BuffHandle(object):
    def __init__(self, buff):
        self.__buff = buff
        self.__idx = 0

    def size(self):
        return len(self.__buff)

    def set_idx(self, idx):
        self.__idx = idx

    def get_idx(self):
        return self.__idx

    def readNullString(self, size):
        data = self.read(size)
        return data

    def read_b(self, size):
        return self.__buff[self.__idx : self.__idx + size]

    def read_at(self, offset, size):
        return self.__buff[offset : offset + size]

    def read(self, size):
        if isinstance(size, SV):
            size = size.value

        buff = self.__buff[self.__idx : self.__idx + size]
        self.__idx += size

        return buff

    def end(self):
        return self.__idx == len(self.__buff)


resources = {
    "style": {
        "Animation": 16973824,
        "Animation.Activity": 16973825,
        "Animation.Dialog": 16973826,
        "Animation.InputMethod": 16973910,
        "Animation.Toast": 16973828,
        "Animation.Translucent": 16973827,
        "DeviceDefault.ButtonBar": 16974287,
        "DeviceDefault.ButtonBar.AlertDialog": 16974288,
        "DeviceDefault.Light.ButtonBar": 16974290,
        "DeviceDefault.Light.ButtonBar.AlertDialog": 16974291,
        "DeviceDefault.Light.SegmentedButton": 16974292,
        "DeviceDefault.SegmentedButton": 16974289,
        "Holo.ButtonBar": 16974053,
        "Holo.ButtonBar.AlertDialog": 16974055,
        "Holo.Light.ButtonBar": 16974054,
        "Holo.Light.ButtonBar.AlertDialog": 16974056,
        "Holo.Light.SegmentedButton": 16974058,
        "Holo.SegmentedButton": 16974057,
        "MediaButton": 16973879,
        "MediaButton.Ffwd": 16973883,
        "MediaButton.Next": 16973881,
        "MediaButton.Pause": 16973885,
        "MediaButton.Play": 16973882,
        "MediaButton.Previous": 16973880,
        "MediaButton.Rew": 16973884,
        "TextAppearance": 16973886,
        "TextAppearance.DeviceDefault": 16974253,
        "TextAppearance.DeviceDefault.DialogWindowTitle": 16974264,
        "TextAppearance.DeviceDefault.Inverse": 16974254,
        "TextAppearance.DeviceDefault.Large": 16974255,
        "TextAppearance.DeviceDefault.Large.Inverse": 16974256,
        "TextAppearance.DeviceDefault.Medium": 16974257,
        "TextAppearance.DeviceDefault.Medium.Inverse": 16974258,
        "TextAppearance.DeviceDefault.SearchResult.Subtitle": 16974262,
        "TextAppearance.DeviceDefault.SearchResult.Title": 16974261,
        "TextAppearance.DeviceDefault.Small": 16974259,
        "TextAppearance.DeviceDefault.Small.Inverse": 16974260,
        "TextAppearance.DeviceDefault.Widget": 16974265,
        "TextAppearance.DeviceDefault.Widget.ActionBar.Menu": 16974286,
        "TextAppearance.DeviceDefault.Widget.ActionBar.Subtitle": 16974279,
        "TextAppearance.DeviceDefault.Widget.ActionBar.Subtitle.Inverse": 16974283,
        "TextAppearance.DeviceDefault.Widget.ActionBar.Title": 16974278,
        "TextAppearance.DeviceDefault.Widget.ActionBar.Title.Inverse": 16974282,
        "TextAppearance.DeviceDefault.Widget.ActionMode.Subtitle": 16974281,
        "TextAppearance.DeviceDefault.Widget.ActionMode.Subtitle.Inverse": 16974285,
        "TextAppearance.DeviceDefault.Widget.ActionMode.Title": 16974280,
        "TextAppearance.DeviceDefault.Widget.ActionMode.Title.Inverse": 16974284,
        "TextAppearance.DeviceDefault.Widget.Button": 16974266,
        "TextAppearance.DeviceDefault.Widget.DropDownHint": 16974271,
        "TextAppearance.DeviceDefault.Widget.DropDownItem": 16974272,
        "TextAppearance.DeviceDefault.Widget.EditText": 16974274,
        "TextAppearance.DeviceDefault.Widget.IconMenu.Item": 16974267,
        "TextAppearance.DeviceDefault.Widget.PopupMenu": 16974275,
        "TextAppearance.DeviceDefault.Widget.PopupMenu.Large": 16974276,
        "TextAppearance.DeviceDefault.Widget.PopupMenu.Small": 16974277,
        "TextAppearance.DeviceDefault.Widget.TabWidget": 16974268,
        "TextAppearance.DeviceDefault.Widget.TextView": 16974269,
        "TextAppearance.DeviceDefault.Widget.TextView.PopupMenu": 16974270,
        "TextAppearance.DeviceDefault.Widget.TextView.SpinnerItem": 16974273,
        "TextAppearance.DeviceDefault.WindowTitle": 16974263,
        "TextAppearance.DialogWindowTitle": 16973889,
        "TextAppearance.Holo": 16974075,
        "TextAppearance.Holo.DialogWindowTitle": 16974103,
        "TextAppearance.Holo.Inverse": 16974076,
        "TextAppearance.Holo.Large": 16974077,
        "TextAppearance.Holo.Large.Inverse": 16974078,
        "TextAppearance.Holo.Medium": 16974079,
        "TextAppearance.Holo.Medium.Inverse": 16974080,
        "TextAppearance.Holo.SearchResult.Subtitle": 16974084,
        "TextAppearance.Holo.SearchResult.Title": 16974083,
        "TextAppearance.Holo.Small": 16974081,
        "TextAppearance.Holo.Small.Inverse": 16974082,
        "TextAppearance.Holo.Widget": 16974085,
        "TextAppearance.Holo.Widget.ActionBar.Menu": 16974112,
        "TextAppearance.Holo.Widget.ActionBar.Subtitle": 16974099,
        "TextAppearance.Holo.Widget.ActionBar.Subtitle.Inverse": 16974109,
        "TextAppearance.Holo.Widget.ActionBar.Title": 16974098,
        "TextAppearance.Holo.Widget.ActionBar.Title.Inverse": 16974108,
        "TextAppearance.Holo.Widget.ActionMode.Subtitle": 16974101,
        "TextAppearance.Holo.Widget.ActionMode.Subtitle.Inverse": 16974111,
        "TextAppearance.Holo.Widget.ActionMode.Title": 16974100,
        "TextAppearance.Holo.Widget.ActionMode.Title.Inverse": 16974110,
        "TextAppearance.Holo.Widget.Button": 16974086,
        "TextAppearance.Holo.Widget.DropDownHint": 16974091,
        "TextAppearance.Holo.Widget.DropDownItem": 16974092,
        "TextAppearance.Holo.Widget.EditText": 16974094,
        "TextAppearance.Holo.Widget.IconMenu.Item": 16974087,
        "TextAppearance.Holo.Widget.PopupMenu": 16974095,
        "TextAppearance.Holo.Widget.PopupMenu.Large": 16974096,
        "TextAppearance.Holo.Widget.PopupMenu.Small": 16974097,
        "TextAppearance.Holo.Widget.TabWidget": 16974088,
        "TextAppearance.Holo.Widget.TextView": 16974089,
        "TextAppearance.Holo.Widget.TextView.PopupMenu": 16974090,
        "TextAppearance.Holo.Widget.TextView.SpinnerItem": 16974093,
        "TextAppearance.Holo.WindowTitle": 16974102,
        "TextAppearance.Inverse": 16973887,
        "TextAppearance.Large": 16973890,
        "TextAppearance.Large.Inverse": 16973891,
        "TextAppearance.Material": 16974317,
        "TextAppearance.Material.Body1": 16974320,
        "TextAppearance.Material.Body2": 16974319,
        "TextAppearance.Material.Button": 16974318,
        "TextAppearance.Material.Caption": 16974321,
        "TextAppearance.Material.DialogWindowTitle": 16974322,
        "TextAppearance.Material.Display1": 16974326,
        "TextAppearance.Material.Display2": 16974325,
        "TextAppearance.Material.Display3": 16974324,
        "TextAppearance.Material.Display4": 16974323,
        "TextAppearance.Material.Headline": 16974327,
        "TextAppearance.Material.Inverse": 16974328,
        "TextAppearance.Material.Large": 16974329,
        "TextAppearance.Material.Large.Inverse": 16974330,
        "TextAppearance.Material.Medium": 16974331,
        "TextAppearance.Material.Medium.Inverse": 16974332,
        "TextAppearance.Material.Menu": 16974333,
        "TextAppearance.Material.Notification": 16974334,
        "TextAppearance.Material.Notification.Emphasis": 16974335,
        "TextAppearance.Material.Notification.Info": 16974336,
        "TextAppearance.Material.Notification.Line2": 16974337,
        "TextAppearance.Material.Notification.Time": 16974338,
        "TextAppearance.Material.Notification.Title": 16974339,
        "TextAppearance.Material.SearchResult.Subtitle": 16974340,
        "TextAppearance.Material.SearchResult.Title": 16974341,
        "TextAppearance.Material.Small": 16974342,
        "TextAppearance.Material.Small.Inverse": 16974343,
        "TextAppearance.Material.Subhead": 16974344,
        "TextAppearance.Material.Title": 16974345,
        "TextAppearance.Material.Widget": 16974347,
        "TextAppearance.Material.Widget.ActionBar.Menu": 16974348,
        "TextAppearance.Material.Widget.ActionBar.Subtitle": 16974349,
        "TextAppearance.Material.Widget.ActionBar.Subtitle.Inverse": 16974350,
        "TextAppearance.Material.Widget.ActionBar.Title": 16974351,
        "TextAppearance.Material.Widget.ActionBar.Title.Inverse": 16974352,
        "TextAppearance.Material.Widget.ActionMode.Subtitle": 16974353,
        "TextAppearance.Material.Widget.ActionMode.Subtitle.Inverse": 16974354,
        "TextAppearance.Material.Widget.ActionMode.Title": 16974355,
        "TextAppearance.Material.Widget.ActionMode.Title.Inverse": 16974356,
        "TextAppearance.Material.Widget.Button": 16974357,
        "TextAppearance.Material.Widget.DropDownHint": 16974358,
        "TextAppearance.Material.Widget.DropDownItem": 16974359,
        "TextAppearance.Material.Widget.EditText": 16974360,
        "TextAppearance.Material.Widget.IconMenu.Item": 16974361,
        "TextAppearance.Material.Widget.PopupMenu": 16974362,
        "TextAppearance.Material.Widget.PopupMenu.Large": 16974363,
        "TextAppearance.Material.Widget.PopupMenu.Small": 16974364,
        "TextAppearance.Material.Widget.TabWidget": 16974365,
        "TextAppearance.Material.Widget.TextView": 16974366,
        "TextAppearance.Material.Widget.TextView.PopupMenu": 16974367,
        "TextAppearance.Material.Widget.TextView.SpinnerItem": 16974368,
        "TextAppearance.Material.Widget.Toolbar.Subtitle": 16974369,
        "TextAppearance.Material.Widget.Toolbar.Title": 16974370,
        "TextAppearance.Material.WindowTitle": 16974346,
        "TextAppearance.Medium": 16973892,
        "TextAppearance.Medium.Inverse": 16973893,
        "TextAppearance.Small": 16973894,
        "TextAppearance.Small.Inverse": 16973895,
        "TextAppearance.StatusBar.EventContent": 16973927,
        "TextAppearance.StatusBar.EventContent.Title": 16973928,
        "TextAppearance.StatusBar.Icon": 16973926,
        "TextAppearance.StatusBar.Title": 16973925,
        "TextAppearance.SuggestionHighlight": 16974104,
        "TextAppearance.Theme": 16973888,
        "TextAppearance.Theme.Dialog": 16973896,
        "TextAppearance.Widget": 16973897,
        "TextAppearance.Widget.Button": 16973898,
        "TextAppearance.Widget.DropDownHint": 16973904,
        "TextAppearance.Widget.DropDownItem": 16973905,
        "TextAppearance.Widget.EditText": 16973900,
        "TextAppearance.Widget.IconMenu.Item": 16973899,
        "TextAppearance.Widget.PopupMenu.Large": 16973952,
        "TextAppearance.Widget.PopupMenu.Small": 16973953,
        "TextAppearance.Widget.TabWidget": 16973901,
        "TextAppearance.Widget.TextView": 16973902,
        "TextAppearance.Widget.TextView.PopupMenu": 16973903,
        "TextAppearance.Widget.TextView.SpinnerItem": 16973906,
        "TextAppearance.WindowTitle": 16973907,
        "Theme": 16973829,
        "ThemeOverlay": 16974407,
        "ThemeOverlay.Material": 16974408,
        "ThemeOverlay.Material.ActionBar": 16974409,
        "ThemeOverlay.Material.Dark": 16974411,
        "ThemeOverlay.Material.Dark.ActionBar": 16974412,
        "ThemeOverlay.Material.Light": 16974410,
        "Theme.Black": 16973832,
        "Theme.Black.NoTitleBar": 16973833,
        "Theme.Black.NoTitleBar.Fullscreen": 16973834,
        "Theme.DeviceDefault": 16974120,
        "Theme.DeviceDefault.Dialog": 16974126,
        "Theme.DeviceDefault.DialogWhenLarge": 16974134,
        "Theme.DeviceDefault.DialogWhenLarge.NoActionBar": 16974135,
        "Theme.DeviceDefault.Dialog.MinWidth": 16974127,
        "Theme.DeviceDefault.Dialog.NoActionBar": 16974128,
        "Theme.DeviceDefault.Dialog.NoActionBar.MinWidth": 16974129,
        "Theme.DeviceDefault.InputMethod": 16974142,
        "Theme.DeviceDefault.Light": 16974123,
        "Theme.DeviceDefault.Light.DarkActionBar": 16974143,
        "Theme.DeviceDefault.Light.Dialog": 16974130,
        "Theme.DeviceDefault.Light.DialogWhenLarge": 16974136,
        "Theme.DeviceDefault.Light.DialogWhenLarge.NoActionBar": 16974137,
        "Theme.DeviceDefault.Light.Dialog.MinWidth": 16974131,
        "Theme.DeviceDefault.Light.Dialog.NoActionBar": 16974132,
        "Theme.DeviceDefault.Light.Dialog.NoActionBar.MinWidth": 16974133,
        "Theme.DeviceDefault.Light.NoActionBar": 16974124,
        "Theme.DeviceDefault.Light.NoActionBar.Fullscreen": 16974125,
        "Theme.DeviceDefault.Light.NoActionBar.Overscan": 16974304,
        "Theme.DeviceDefault.Light.NoActionBar.TranslucentDecor": 16974308,
        "Theme.DeviceDefault.Light.Panel": 16974139,
        "Theme.DeviceDefault.NoActionBar": 16974121,
        "Theme.DeviceDefault.NoActionBar.Fullscreen": 16974122,
        "Theme.DeviceDefault.NoActionBar.Overscan": 16974303,
        "Theme.DeviceDefault.NoActionBar.TranslucentDecor": 16974307,
        "Theme.DeviceDefault.Panel": 16974138,
        "Theme.DeviceDefault.Settings": 16974371,
        "Theme.DeviceDefault.Wallpaper": 16974140,
        "Theme.DeviceDefault.Wallpaper.NoTitleBar": 16974141,
        "Theme.Dialog": 16973835,
        "Theme.Holo": 16973931,
        "Theme.Holo.Dialog": 16973935,
        "Theme.Holo.DialogWhenLarge": 16973943,
        "Theme.Holo.DialogWhenLarge.NoActionBar": 16973944,
        "Theme.Holo.Dialog.MinWidth": 16973936,
        "Theme.Holo.Dialog.NoActionBar": 16973937,
        "Theme.Holo.Dialog.NoActionBar.MinWidth": 16973938,
        "Theme.Holo.InputMethod": 16973951,
        "Theme.Holo.Light": 16973934,
        "Theme.Holo.Light.DarkActionBar": 16974105,
        "Theme.Holo.Light.Dialog": 16973939,
        "Theme.Holo.Light.DialogWhenLarge": 16973945,
        "Theme.Holo.Light.DialogWhenLarge.NoActionBar": 16973946,
        "Theme.Holo.Light.Dialog.MinWidth": 16973940,
        "Theme.Holo.Light.Dialog.NoActionBar": 16973941,
        "Theme.Holo.Light.Dialog.NoActionBar.MinWidth": 16973942,
        "Theme.Holo.Light.NoActionBar": 16974064,
        "Theme.Holo.Light.NoActionBar.Fullscreen": 16974065,
        "Theme.Holo.Light.NoActionBar.Overscan": 16974302,
        "Theme.Holo.Light.NoActionBar.TranslucentDecor": 16974306,
        "Theme.Holo.Light.Panel": 16973948,
        "Theme.Holo.NoActionBar": 16973932,
        "Theme.Holo.NoActionBar.Fullscreen": 16973933,
        "Theme.Holo.NoActionBar.Overscan": 16974301,
        "Theme.Holo.NoActionBar.TranslucentDecor": 16974305,
        "Theme.Holo.Panel": 16973947,
        "Theme.Holo.Wallpaper": 16973949,
        "Theme.Holo.Wallpaper.NoTitleBar": 16973950,
        "Theme.InputMethod": 16973908,
        "Theme.Light": 16973836,
        "Theme.Light.NoTitleBar": 16973837,
        "Theme.Light.NoTitleBar.Fullscreen": 16973838,
        "Theme.Light.Panel": 16973914,
        "Theme.Light.WallpaperSettings": 16973922,
        "Theme.Material": 16974372,
        "Theme.Material.Dialog": 16974373,
        "Theme.Material.DialogWhenLarge": 16974379,
        "Theme.Material.DialogWhenLarge.NoActionBar": 16974380,
        "Theme.Material.Dialog.Alert": 16974374,
        "Theme.Material.Dialog.MinWidth": 16974375,
        "Theme.Material.Dialog.NoActionBar": 16974376,
        "Theme.Material.Dialog.NoActionBar.MinWidth": 16974377,
        "Theme.Material.Dialog.Presentation": 16974378,
        "Theme.Material.InputMethod": 16974381,
        "Theme.Material.Light": 16974391,
        "Theme.Material.Light.DarkActionBar": 16974392,
        "Theme.Material.Light.Dialog": 16974393,
        "Theme.Material.Light.DialogWhenLarge": 16974399,
        "Theme.Material.Light.DialogWhenLarge.NoActionBar": 16974400,
        "Theme.Material.Light.Dialog.Alert": 16974394,
        "Theme.Material.Light.Dialog.MinWidth": 16974395,
        "Theme.Material.Light.Dialog.NoActionBar": 16974396,
        "Theme.Material.Light.Dialog.NoActionBar.MinWidth": 16974397,
        "Theme.Material.Light.Dialog.Presentation": 16974398,
        "Theme.Material.Light.NoActionBar": 16974401,
        "Theme.Material.Light.NoActionBar.Fullscreen": 16974402,
        "Theme.Material.Light.NoActionBar.Overscan": 16974403,
        "Theme.Material.Light.NoActionBar.TranslucentDecor": 16974404,
        "Theme.Material.Light.Panel": 16974405,
        "Theme.Material.Light.Voice": 16974406,
        "Theme.Material.NoActionBar": 16974382,
        "Theme.Material.NoActionBar.Fullscreen": 16974383,
        "Theme.Material.NoActionBar.Overscan": 16974384,
        "Theme.Material.NoActionBar.TranslucentDecor": 16974385,
        "Theme.Material.Panel": 16974386,
        "Theme.Material.Settings": 16974387,
        "Theme.Material.Voice": 16974388,
        "Theme.Material.Wallpaper": 16974389,
        "Theme.Material.Wallpaper.NoTitleBar": 16974390,
        "Theme.NoDisplay": 16973909,
        "Theme.NoTitleBar": 16973830,
        "Theme.NoTitleBar.Fullscreen": 16973831,
        "Theme.NoTitleBar.OverlayActionModes": 16973930,
        "Theme.Panel": 16973913,
        "Theme.Translucent": 16973839,
        "Theme.Translucent.NoTitleBar": 16973840,
        "Theme.Translucent.NoTitleBar.Fullscreen": 16973841,
        "Theme.Wallpaper": 16973918,
        "Theme.WallpaperSettings": 16973921,
        "Theme.Wallpaper.NoTitleBar": 16973919,
        "Theme.Wallpaper.NoTitleBar.Fullscreen": 16973920,
        "Theme.WithActionBar": 16973929,
        "Widget": 16973842,
        "Widget.AbsListView": 16973843,
        "Widget.ActionBar": 16973954,
        "Widget.ActionBar.TabBar": 16974068,
        "Widget.ActionBar.TabText": 16974067,
        "Widget.ActionBar.TabView": 16974066,
        "Widget.ActionButton": 16973956,
        "Widget.ActionButton.CloseMode": 16973960,
        "Widget.ActionButton.Overflow": 16973959,
        "Widget.AutoCompleteTextView": 16973863,
        "Widget.Button": 16973844,
        "Widget.Button.Inset": 16973845,
        "Widget.Button.Small": 16973846,
        "Widget.Button.Toggle": 16973847,
        "Widget.CalendarView": 16974059,
        "Widget.CompoundButton": 16973848,
        "Widget.CompoundButton.CheckBox": 16973849,
        "Widget.CompoundButton.RadioButton": 16973850,
        "Widget.CompoundButton.Star": 16973851,
        "Widget.DatePicker": 16974062,
        "Widget.DeviceDefault": 16974144,
        "Widget.DeviceDefault.ActionBar": 16974187,
        "Widget.DeviceDefault.ActionBar.Solid": 16974195,
        "Widget.DeviceDefault.ActionBar.TabBar": 16974194,
        "Widget.DeviceDefault.ActionBar.TabText": 16974193,
        "Widget.DeviceDefault.ActionBar.TabView": 16974192,
        "Widget.DeviceDefault.ActionButton": 16974182,
        "Widget.DeviceDefault.ActionButton.CloseMode": 16974186,
        "Widget.DeviceDefault.ActionButton.Overflow": 16974183,
        "Widget.DeviceDefault.ActionButton.TextButton": 16974184,
        "Widget.DeviceDefault.ActionMode": 16974185,
        "Widget.DeviceDefault.AutoCompleteTextView": 16974151,
        "Widget.DeviceDefault.Button": 16974145,
        "Widget.DeviceDefault.Button.Borderless": 16974188,
        "Widget.DeviceDefault.Button.Borderless.Small": 16974149,
        "Widget.DeviceDefault.Button.Inset": 16974147,
        "Widget.DeviceDefault.Button.Small": 16974146,
        "Widget.DeviceDefault.Button.Toggle": 16974148,
        "Widget.DeviceDefault.CalendarView": 16974190,
        "Widget.DeviceDefault.CheckedTextView": 16974299,
        "Widget.DeviceDefault.CompoundButton.CheckBox": 16974152,
        "Widget.DeviceDefault.CompoundButton.RadioButton": 16974169,
        "Widget.DeviceDefault.CompoundButton.Star": 16974173,
        "Widget.DeviceDefault.DatePicker": 16974191,
        "Widget.DeviceDefault.DropDownItem": 16974177,
        "Widget.DeviceDefault.DropDownItem.Spinner": 16974178,
        "Widget.DeviceDefault.EditText": 16974154,
        "Widget.DeviceDefault.ExpandableListView": 16974155,
        "Widget.DeviceDefault.FastScroll": 16974313,
        "Widget.DeviceDefault.GridView": 16974156,
        "Widget.DeviceDefault.HorizontalScrollView": 16974171,
        "Widget.DeviceDefault.ImageButton": 16974157,
        "Widget.DeviceDefault.Light": 16974196,
        "Widget.DeviceDefault.Light.ActionBar": 16974243,
        "Widget.DeviceDefault.Light.ActionBar.Solid": 16974247,
        "Widget.DeviceDefault.Light.ActionBar.Solid.Inverse": 16974248,
        "Widget.DeviceDefault.Light.ActionBar.TabBar": 16974246,
        "Widget.DeviceDefault.Light.ActionBar.TabBar.Inverse": 16974249,
        "Widget.DeviceDefault.Light.ActionBar.TabText": 16974245,
        "Widget.DeviceDefault.Light.ActionBar.TabText.Inverse": 16974251,
        "Widget.DeviceDefault.Light.ActionBar.TabView": 16974244,
        "Widget.DeviceDefault.Light.ActionBar.TabView.Inverse": 16974250,
        "Widget.DeviceDefault.Light.ActionButton": 16974239,
        "Widget.DeviceDefault.Light.ActionButton.CloseMode": 16974242,
        "Widget.DeviceDefault.Light.ActionButton.Overflow": 16974240,
        "Widget.DeviceDefault.Light.ActionMode": 16974241,
        "Widget.DeviceDefault.Light.ActionMode.Inverse": 16974252,
        "Widget.DeviceDefault.Light.AutoCompleteTextView": 16974203,
        "Widget.DeviceDefault.Light.Button": 16974197,
        "Widget.DeviceDefault.Light.Button.Borderless.Small": 16974201,
        "Widget.DeviceDefault.Light.Button.Inset": 16974199,
        "Widget.DeviceDefault.Light.Button.Small": 16974198,
        "Widget.DeviceDefault.Light.Button.Toggle": 16974200,
        "Widget.DeviceDefault.Light.CalendarView": 16974238,
        "Widget.DeviceDefault.Light.CheckedTextView": 16974300,
        "Widget.DeviceDefault.Light.CompoundButton.CheckBox": 16974204,
        "Widget.DeviceDefault.Light.CompoundButton.RadioButton": 16974224,
        "Widget.DeviceDefault.Light.CompoundButton.Star": 16974228,
        "Widget.DeviceDefault.Light.DropDownItem": 16974232,
        "Widget.DeviceDefault.Light.DropDownItem.Spinner": 16974233,
        "Widget.DeviceDefault.Light.EditText": 16974206,
        "Widget.DeviceDefault.Light.ExpandableListView": 16974207,
        "Widget.DeviceDefault.Light.FastScroll": 16974315,
        "Widget.DeviceDefault.Light.GridView": 16974208,
        "Widget.DeviceDefault.Light.HorizontalScrollView": 16974226,
        "Widget.DeviceDefault.Light.ImageButton": 16974209,
        "Widget.DeviceDefault.Light.ListPopupWindow": 16974235,
        "Widget.DeviceDefault.Light.ListView": 16974210,
        "Widget.DeviceDefault.Light.ListView.DropDown": 16974205,
        "Widget.DeviceDefault.Light.MediaRouteButton": 16974296,
        "Widget.DeviceDefault.Light.PopupMenu": 16974236,
        "Widget.DeviceDefault.Light.PopupWindow": 16974211,
        "Widget.DeviceDefault.Light.ProgressBar": 16974212,
        "Widget.DeviceDefault.Light.ProgressBar.Horizontal": 16974213,
        "Widget.DeviceDefault.Light.ProgressBar.Inverse": 16974217,
        "Widget.DeviceDefault.Light.ProgressBar.Large": 16974216,
        "Widget.DeviceDefault.Light.ProgressBar.Large.Inverse": 16974219,
        "Widget.DeviceDefault.Light.ProgressBar.Small": 16974214,
        "Widget.DeviceDefault.Light.ProgressBar.Small.Inverse": 16974218,
        "Widget.DeviceDefault.Light.ProgressBar.Small.Title": 16974215,
        "Widget.DeviceDefault.Light.RatingBar": 16974221,
        "Widget.DeviceDefault.Light.RatingBar.Indicator": 16974222,
        "Widget.DeviceDefault.Light.RatingBar.Small": 16974223,
        "Widget.DeviceDefault.Light.ScrollView": 16974225,
        "Widget.DeviceDefault.Light.SeekBar": 16974220,
        "Widget.DeviceDefault.Light.Spinner": 16974227,
        "Widget.DeviceDefault.Light.StackView": 16974316,
        "Widget.DeviceDefault.Light.Tab": 16974237,
        "Widget.DeviceDefault.Light.TabWidget": 16974229,
        "Widget.DeviceDefault.Light.TextView": 16974202,
        "Widget.DeviceDefault.Light.TextView.SpinnerItem": 16974234,
        "Widget.DeviceDefault.Light.WebTextView": 16974230,
        "Widget.DeviceDefault.Light.WebView": 16974231,
        "Widget.DeviceDefault.ListPopupWindow": 16974180,
        "Widget.DeviceDefault.ListView": 16974158,
        "Widget.DeviceDefault.ListView.DropDown": 16974153,
        "Widget.DeviceDefault.MediaRouteButton": 16974295,
        "Widget.DeviceDefault.PopupMenu": 16974181,
        "Widget.DeviceDefault.PopupWindow": 16974159,
        "Widget.DeviceDefault.ProgressBar": 16974160,
        "Widget.DeviceDefault.ProgressBar.Horizontal": 16974161,
        "Widget.DeviceDefault.ProgressBar.Large": 16974164,
        "Widget.DeviceDefault.ProgressBar.Small": 16974162,
        "Widget.DeviceDefault.ProgressBar.Small.Title": 16974163,
        "Widget.DeviceDefault.RatingBar": 16974166,
        "Widget.DeviceDefault.RatingBar.Indicator": 16974167,
        "Widget.DeviceDefault.RatingBar.Small": 16974168,
        "Widget.DeviceDefault.ScrollView": 16974170,
        "Widget.DeviceDefault.SeekBar": 16974165,
        "Widget.DeviceDefault.Spinner": 16974172,
        "Widget.DeviceDefault.StackView": 16974314,
        "Widget.DeviceDefault.Tab": 16974189,
        "Widget.DeviceDefault.TabWidget": 16974174,
        "Widget.DeviceDefault.TextView": 16974150,
        "Widget.DeviceDefault.TextView.SpinnerItem": 16974179,
        "Widget.DeviceDefault.WebTextView": 16974175,
        "Widget.DeviceDefault.WebView": 16974176,
        "Widget.DropDownItem": 16973867,
        "Widget.DropDownItem.Spinner": 16973868,
        "Widget.EditText": 16973859,
        "Widget.ExpandableListView": 16973860,
        "Widget.FastScroll": 16974309,
        "Widget.FragmentBreadCrumbs": 16973961,
        "Widget.Gallery": 16973877,
        "Widget.GridView": 16973874,
        "Widget.Holo": 16973962,
        "Widget.Holo.ActionBar": 16974004,
        "Widget.Holo.ActionBar.Solid": 16974113,
        "Widget.Holo.ActionBar.TabBar": 16974071,
        "Widget.Holo.ActionBar.TabText": 16974070,
        "Widget.Holo.ActionBar.TabView": 16974069,
        "Widget.Holo.ActionButton": 16973999,
        "Widget.Holo.ActionButton.CloseMode": 16974003,
        "Widget.Holo.ActionButton.Overflow": 16974000,
        "Widget.Holo.ActionButton.TextButton": 16974001,
        "Widget.Holo.ActionMode": 16974002,
        "Widget.Holo.AutoCompleteTextView": 16973968,
        "Widget.Holo.Button": 16973963,
        "Widget.Holo.Button.Borderless": 16974050,
        "Widget.Holo.Button.Borderless.Small": 16974106,
        "Widget.Holo.Button.Inset": 16973965,
        "Widget.Holo.Button.Small": 16973964,
        "Widget.Holo.Button.Toggle": 16973966,
        "Widget.Holo.CalendarView": 16974060,
        "Widget.Holo.CheckedTextView": 16974297,
        "Widget.Holo.CompoundButton.CheckBox": 16973969,
        "Widget.Holo.CompoundButton.RadioButton": 16973986,
        "Widget.Holo.CompoundButton.Star": 16973990,
        "Widget.Holo.DatePicker": 16974063,
        "Widget.Holo.DropDownItem": 16973994,
        "Widget.Holo.DropDownItem.Spinner": 16973995,
        "Widget.Holo.EditText": 16973971,
        "Widget.Holo.ExpandableListView": 16973972,
        "Widget.Holo.GridView": 16973973,
        "Widget.Holo.HorizontalScrollView": 16973988,
        "Widget.Holo.ImageButton": 16973974,
        "Widget.Holo.Light": 16974005,
        "Widget.Holo.Light.ActionBar": 16974049,
        "Widget.Holo.Light.ActionBar.Solid": 16974114,
        "Widget.Holo.Light.ActionBar.Solid.Inverse": 16974115,
        "Widget.Holo.Light.ActionBar.TabBar": 16974074,
        "Widget.Holo.Light.ActionBar.TabBar.Inverse": 16974116,
        "Widget.Holo.Light.ActionBar.TabText": 16974073,
        "Widget.Holo.Light.ActionBar.TabText.Inverse": 16974118,
        "Widget.Holo.Light.ActionBar.TabView": 16974072,
        "Widget.Holo.Light.ActionBar.TabView.Inverse": 16974117,
        "Widget.Holo.Light.ActionButton": 16974045,
        "Widget.Holo.Light.ActionButton.CloseMode": 16974048,
        "Widget.Holo.Light.ActionButton.Overflow": 16974046,
        "Widget.Holo.Light.ActionMode": 16974047,
        "Widget.Holo.Light.ActionMode.Inverse": 16974119,
        "Widget.Holo.Light.AutoCompleteTextView": 16974011,
        "Widget.Holo.Light.Button": 16974006,
        "Widget.Holo.Light.Button.Borderless.Small": 16974107,
        "Widget.Holo.Light.Button.Inset": 16974008,
        "Widget.Holo.Light.Button.Small": 16974007,
        "Widget.Holo.Light.Button.Toggle": 16974009,
        "Widget.Holo.Light.CalendarView": 16974061,
        "Widget.Holo.Light.CheckedTextView": 16974298,
        "Widget.Holo.Light.CompoundButton.CheckBox": 16974012,
        "Widget.Holo.Light.CompoundButton.RadioButton": 16974032,
        "Widget.Holo.Light.CompoundButton.Star": 16974036,
        "Widget.Holo.Light.DropDownItem": 16974040,
        "Widget.Holo.Light.DropDownItem.Spinner": 16974041,
        "Widget.Holo.Light.EditText": 16974014,
        "Widget.Holo.Light.ExpandableListView": 16974015,
        "Widget.Holo.Light.GridView": 16974016,
        "Widget.Holo.Light.HorizontalScrollView": 16974034,
        "Widget.Holo.Light.ImageButton": 16974017,
        "Widget.Holo.Light.ListPopupWindow": 16974043,
        "Widget.Holo.Light.ListView": 16974018,
        "Widget.Holo.Light.ListView.DropDown": 16974013,
        "Widget.Holo.Light.MediaRouteButton": 16974294,
        "Widget.Holo.Light.PopupMenu": 16974044,
        "Widget.Holo.Light.PopupWindow": 16974019,
        "Widget.Holo.Light.ProgressBar": 16974020,
        "Widget.Holo.Light.ProgressBar.Horizontal": 16974021,
        "Widget.Holo.Light.ProgressBar.Inverse": 16974025,
        "Widget.Holo.Light.ProgressBar.Large": 16974024,
        "Widget.Holo.Light.ProgressBar.Large.Inverse": 16974027,
        "Widget.Holo.Light.ProgressBar.Small": 16974022,
        "Widget.Holo.Light.ProgressBar.Small.Inverse": 16974026,
        "Widget.Holo.Light.ProgressBar.Small.Title": 16974023,
        "Widget.Holo.Light.RatingBar": 16974029,
        "Widget.Holo.Light.RatingBar.Indicator": 16974030,
        "Widget.Holo.Light.RatingBar.Small": 16974031,
        "Widget.Holo.Light.ScrollView": 16974033,
        "Widget.Holo.Light.SeekBar": 16974028,
        "Widget.Holo.Light.Spinner": 16974035,
        "Widget.Holo.Light.Tab": 16974052,
        "Widget.Holo.Light.TabWidget": 16974037,
        "Widget.Holo.Light.TextView": 16974010,
        "Widget.Holo.Light.TextView.SpinnerItem": 16974042,
        "Widget.Holo.Light.WebTextView": 16974038,
        "Widget.Holo.Light.WebView": 16974039,
        "Widget.Holo.ListPopupWindow": 16973997,
        "Widget.Holo.ListView": 16973975,
        "Widget.Holo.ListView.DropDown": 16973970,
        "Widget.Holo.MediaRouteButton": 16974293,
        "Widget.Holo.PopupMenu": 16973998,
        "Widget.Holo.PopupWindow": 16973976,
        "Widget.Holo.ProgressBar": 16973977,
        "Widget.Holo.ProgressBar.Horizontal": 16973978,
        "Widget.Holo.ProgressBar.Large": 16973981,
        "Widget.Holo.ProgressBar.Small": 16973979,
        "Widget.Holo.ProgressBar.Small.Title": 16973980,
        "Widget.Holo.RatingBar": 16973983,
        "Widget.Holo.RatingBar.Indicator": 16973984,
        "Widget.Holo.RatingBar.Small": 16973985,
        "Widget.Holo.ScrollView": 16973987,
        "Widget.Holo.SeekBar": 16973982,
        "Widget.Holo.Spinner": 16973989,
        "Widget.Holo.Tab": 16974051,
        "Widget.Holo.TabWidget": 16973991,
        "Widget.Holo.TextView": 16973967,
        "Widget.Holo.TextView.SpinnerItem": 16973996,
        "Widget.Holo.WebTextView": 16973992,
        "Widget.Holo.WebView": 16973993,
        "Widget.ImageButton": 16973862,
        "Widget.ImageWell": 16973861,
        "Widget.KeyboardView": 16973911,
        "Widget.ListPopupWindow": 16973957,
        "Widget.ListView": 16973870,
        "Widget.ListView.DropDown": 16973872,
        "Widget.ListView.Menu": 16973873,
        "Widget.ListView.White": 16973871,
        "Widget.Material": 16974413,
        "Widget.Material.ActionBar": 16974414,
        "Widget.Material.ActionBar.Solid": 16974415,
        "Widget.Material.ActionBar.TabBar": 16974416,
        "Widget.Material.ActionBar.TabText": 16974417,
        "Widget.Material.ActionBar.TabView": 16974418,
        "Widget.Material.ActionButton": 16974419,
        "Widget.Material.ActionButton.CloseMode": 16974420,
        "Widget.Material.ActionButton.Overflow": 16974421,
        "Widget.Material.ActionMode": 16974422,
        "Widget.Material.AutoCompleteTextView": 16974423,
        "Widget.Material.Button": 16974424,
        "Widget.Material.ButtonBar": 16974431,
        "Widget.Material.ButtonBar.AlertDialog": 16974432,
        "Widget.Material.Button.Borderless": 16974425,
        "Widget.Material.Button.Borderless.Colored": 16974426,
        "Widget.Material.Button.Borderless.Small": 16974427,
        "Widget.Material.Button.Inset": 16974428,
        "Widget.Material.Button.Small": 16974429,
        "Widget.Material.Button.Toggle": 16974430,
        "Widget.Material.CalendarView": 16974433,
        "Widget.Material.CheckedTextView": 16974434,
        "Widget.Material.CompoundButton.CheckBox": 16974435,
        "Widget.Material.CompoundButton.RadioButton": 16974436,
        "Widget.Material.CompoundButton.Star": 16974437,
        "Widget.Material.DatePicker": 16974438,
        "Widget.Material.DropDownItem": 16974439,
        "Widget.Material.DropDownItem.Spinner": 16974440,
        "Widget.Material.EditText": 16974441,
        "Widget.Material.ExpandableListView": 16974442,
        "Widget.Material.FastScroll": 16974443,
        "Widget.Material.GridView": 16974444,
        "Widget.Material.HorizontalScrollView": 16974445,
        "Widget.Material.ImageButton": 16974446,
        "Widget.Material.Light": 16974478,
        "Widget.Material.Light.ActionBar": 16974479,
        "Widget.Material.Light.ActionBar.Solid": 16974480,
        "Widget.Material.Light.ActionBar.TabBar": 16974481,
        "Widget.Material.Light.ActionBar.TabText": 16974482,
        "Widget.Material.Light.ActionBar.TabView": 16974483,
        "Widget.Material.Light.ActionButton": 16974484,
        "Widget.Material.Light.ActionButton.CloseMode": 16974485,
        "Widget.Material.Light.ActionButton.Overflow": 16974486,
        "Widget.Material.Light.ActionMode": 16974487,
        "Widget.Material.Light.AutoCompleteTextView": 16974488,
        "Widget.Material.Light.Button": 16974489,
        "Widget.Material.Light.ButtonBar": 16974496,
        "Widget.Material.Light.ButtonBar.AlertDialog": 16974497,
        "Widget.Material.Light.Button.Borderless": 16974490,
        "Widget.Material.Light.Button.Borderless.Colored": 16974491,
        "Widget.Material.Light.Button.Borderless.Small": 16974492,
        "Widget.Material.Light.Button.Inset": 16974493,
        "Widget.Material.Light.Button.Small": 16974494,
        "Widget.Material.Light.Button.Toggle": 16974495,
        "Widget.Material.Light.CalendarView": 16974498,
        "Widget.Material.Light.CheckedTextView": 16974499,
        "Widget.Material.Light.CompoundButton.CheckBox": 16974500,
        "Widget.Material.Light.CompoundButton.RadioButton": 16974501,
        "Widget.Material.Light.CompoundButton.Star": 16974502,
        "Widget.Material.Light.DatePicker": 16974503,
        "Widget.Material.Light.DropDownItem": 16974504,
        "Widget.Material.Light.DropDownItem.Spinner": 16974505,
        "Widget.Material.Light.EditText": 16974506,
        "Widget.Material.Light.ExpandableListView": 16974507,
        "Widget.Material.Light.FastScroll": 16974508,
        "Widget.Material.Light.GridView": 16974509,
        "Widget.Material.Light.HorizontalScrollView": 16974510,
        "Widget.Material.Light.ImageButton": 16974511,
        "Widget.Material.Light.ListPopupWindow": 16974512,
        "Widget.Material.Light.ListView": 16974513,
        "Widget.Material.Light.ListView.DropDown": 16974514,
        "Widget.Material.Light.MediaRouteButton": 16974515,
        "Widget.Material.Light.PopupMenu": 16974516,
        "Widget.Material.Light.PopupMenu.Overflow": 16974517,
        "Widget.Material.Light.PopupWindow": 16974518,
        "Widget.Material.Light.ProgressBar": 16974519,
        "Widget.Material.Light.ProgressBar.Horizontal": 16974520,
        "Widget.Material.Light.ProgressBar.Inverse": 16974521,
        "Widget.Material.Light.ProgressBar.Large": 16974522,
        "Widget.Material.Light.ProgressBar.Large.Inverse": 16974523,
        "Widget.Material.Light.ProgressBar.Small": 16974524,
        "Widget.Material.Light.ProgressBar.Small.Inverse": 16974525,
        "Widget.Material.Light.ProgressBar.Small.Title": 16974526,
        "Widget.Material.Light.RatingBar": 16974527,
        "Widget.Material.Light.RatingBar.Indicator": 16974528,
        "Widget.Material.Light.RatingBar.Small": 16974529,
        "Widget.Material.Light.ScrollView": 16974530,
        "Widget.Material.Light.SearchView": 16974531,
        "Widget.Material.Light.SeekBar": 16974532,
        "Widget.Material.Light.SegmentedButton": 16974533,
        "Widget.Material.Light.Spinner": 16974535,
        "Widget.Material.Light.Spinner.Underlined": 16974536,
        "Widget.Material.Light.StackView": 16974534,
        "Widget.Material.Light.Tab": 16974537,
        "Widget.Material.Light.TabWidget": 16974538,
        "Widget.Material.Light.TextView": 16974539,
        "Widget.Material.Light.TextView.SpinnerItem": 16974540,
        "Widget.Material.Light.TimePicker": 16974541,
        "Widget.Material.Light.WebTextView": 16974542,
        "Widget.Material.Light.WebView": 16974543,
        "Widget.Material.ListPopupWindow": 16974447,
        "Widget.Material.ListView": 16974448,
        "Widget.Material.ListView.DropDown": 16974449,
        "Widget.Material.MediaRouteButton": 16974450,
        "Widget.Material.PopupMenu": 16974451,
        "Widget.Material.PopupMenu.Overflow": 16974452,
        "Widget.Material.PopupWindow": 16974453,
        "Widget.Material.ProgressBar": 16974454,
        "Widget.Material.ProgressBar.Horizontal": 16974455,
        "Widget.Material.ProgressBar.Large": 16974456,
        "Widget.Material.ProgressBar.Small": 16974457,
        "Widget.Material.ProgressBar.Small.Title": 16974458,
        "Widget.Material.RatingBar": 16974459,
        "Widget.Material.RatingBar.Indicator": 16974460,
        "Widget.Material.RatingBar.Small": 16974461,
        "Widget.Material.ScrollView": 16974462,
        "Widget.Material.SearchView": 16974463,
        "Widget.Material.SeekBar": 16974464,
        "Widget.Material.SegmentedButton": 16974465,
        "Widget.Material.Spinner": 16974467,
        "Widget.Material.Spinner.Underlined": 16974468,
        "Widget.Material.StackView": 16974466,
        "Widget.Material.Tab": 16974469,
        "Widget.Material.TabWidget": 16974470,
        "Widget.Material.TextView": 16974471,
        "Widget.Material.TextView.SpinnerItem": 16974472,
        "Widget.Material.TimePicker": 16974473,
        "Widget.Material.Toolbar": 16974474,
        "Widget.Material.Toolbar.Button.Navigation": 16974475,
        "Widget.Material.WebTextView": 16974476,
        "Widget.Material.WebView": 16974477,
        "Widget.PopupMenu": 16973958,
        "Widget.PopupWindow": 16973878,
        "Widget.ProgressBar": 16973852,
        "Widget.ProgressBar.Horizontal": 16973855,
        "Widget.ProgressBar.Inverse": 16973915,
        "Widget.ProgressBar.Large": 16973853,
        "Widget.ProgressBar.Large.Inverse": 16973916,
        "Widget.ProgressBar.Small": 16973854,
        "Widget.ProgressBar.Small.Inverse": 16973917,
        "Widget.RatingBar": 16973857,
        "Widget.ScrollView": 16973869,
        "Widget.SeekBar": 16973856,
        "Widget.Spinner": 16973864,
        "Widget.Spinner.DropDown": 16973955,
        "Widget.StackView": 16974310,
        "Widget.TabWidget": 16973876,
        "Widget.TextView": 16973858,
        "Widget.TextView.PopupMenu": 16973865,
        "Widget.TextView.SpinnerItem": 16973866,
        "Widget.Toolbar": 16974311,
        "Widget.Toolbar.Button.Navigation": 16974312,
        "Widget.WebView": 16973875,
    },
    "attr": {
        "theme": 16842752,
        "label": 16842753,
        "icon": 16842754,
        "name": 16842755,
        "manageSpaceActivity": 16842756,
        "allowClearUserData": 16842757,
        "permission": 16842758,
        "readPermission": 16842759,
        "writePermission": 16842760,
        "protectionLevel": 16842761,
        "permissionGroup": 16842762,
        "sharedUserId": 16842763,
        "hasCode": 16842764,
        "persistent": 16842765,
        "enabled": 16842766,
        "debuggable": 16842767,
        "exported": 16842768,
        "process": 16842769,
        "taskAffinity": 16842770,
        "multiprocess": 16842771,
        "finishOnTaskLaunch": 16842772,
        "clearTaskOnLaunch": 16842773,
        "stateNotNeeded": 16842774,
        "excludeFromRecents": 16842775,
        "authorities": 16842776,
        "syncable": 16842777,
        "initOrder": 16842778,
        "grantUriPermissions": 16842779,
        "priority": 16842780,
        "launchMode": 16842781,
        "screenOrientation": 16842782,
        "configChanges": 16842783,
        "description": 16842784,
        "targetPackage": 16842785,
        "handleProfiling": 16842786,
        "functionalTest": 16842787,
        "value": 16842788,
        "resource": 16842789,
        "mimeType": 16842790,
        "scheme": 16842791,
        "host": 16842792,
        "port": 16842793,
        "path": 16842794,
        "pathPrefix": 16842795,
        "pathPattern": 16842796,
        "action": 16842797,
        "data": 16842798,
        "targetClass": 16842799,
        "colorForeground": 16842800,
        "colorBackground": 16842801,
        "backgroundDimAmount": 16842802,
        "disabledAlpha": 16842803,
        "textAppearance": 16842804,
        "textAppearanceInverse": 16842805,
        "textColorPrimary": 16842806,
        "textColorPrimaryDisableOnly": 16842807,
        "textColorSecondary": 16842808,
        "textColorPrimaryInverse": 16842809,
        "textColorSecondaryInverse": 16842810,
        "textColorPrimaryNoDisable": 16842811,
        "textColorSecondaryNoDisable": 16842812,
        "textColorPrimaryInverseNoDisable": 16842813,
        "textColorSecondaryInverseNoDisable": 16842814,
        "textColorHintInverse": 16842815,
        "textAppearanceLarge": 16842816,
        "textAppearanceMedium": 16842817,
        "textAppearanceSmall": 16842818,
        "textAppearanceLargeInverse": 16842819,
        "textAppearanceMediumInverse": 16842820,
        "textAppearanceSmallInverse": 16842821,
        "textCheckMark": 16842822,
        "textCheckMarkInverse": 16842823,
        "buttonStyle": 16842824,
        "buttonStyleSmall": 16842825,
        "buttonStyleInset": 16842826,
        "buttonStyleToggle": 16842827,
        "galleryItemBackground": 16842828,
        "listPreferredItemHeight": 16842829,
        "expandableListPreferredItemPaddingLeft": 16842830,
        "expandableListPreferredChildPaddingLeft": 16842831,
        "expandableListPreferredItemIndicatorLeft": 16842832,
        "expandableListPreferredItemIndicatorRight": 16842833,
        "expandableListPreferredChildIndicatorLeft": 16842834,
        "expandableListPreferredChildIndicatorRight": 16842835,
        "windowBackground": 16842836,
        "windowFrame": 16842837,
        "windowNoTitle": 16842838,
        "windowIsFloating": 16842839,
        "windowIsTranslucent": 16842840,
        "windowContentOverlay": 16842841,
        "windowTitleSize": 16842842,
        "windowTitleStyle": 16842843,
        "windowTitleBackgroundStyle": 16842844,
        "alertDialogStyle": 16842845,
        "panelBackground": 16842846,
        "panelFullBackground": 16842847,
        "panelColorForeground": 16842848,
        "panelColorBackground": 16842849,
        "panelTextAppearance": 16842850,
        "scrollbarSize": 16842851,
        "scrollbarThumbHorizontal": 16842852,
        "scrollbarThumbVertical": 16842853,
        "scrollbarTrackHorizontal": 16842854,
        "scrollbarTrackVertical": 16842855,
        "scrollbarAlwaysDrawHorizontalTrack": 16842856,
        "scrollbarAlwaysDrawVerticalTrack": 16842857,
        "absListViewStyle": 16842858,
        "autoCompleteTextViewStyle": 16842859,
        "checkboxStyle": 16842860,
        "dropDownListViewStyle": 16842861,
        "editTextStyle": 16842862,
        "expandableListViewStyle": 16842863,
        "galleryStyle": 16842864,
        "gridViewStyle": 16842865,
        "imageButtonStyle": 16842866,
        "imageWellStyle": 16842867,
        "listViewStyle": 16842868,
        "listViewWhiteStyle": 16842869,
        "popupWindowStyle": 16842870,
        "progressBarStyle": 16842871,
        "progressBarStyleHorizontal": 16842872,
        "progressBarStyleSmall": 16842873,
        "progressBarStyleLarge": 16842874,
        "seekBarStyle": 16842875,
        "ratingBarStyle": 16842876,
        "ratingBarStyleSmall": 16842877,
        "radioButtonStyle": 16842878,
        "scrollbarStyle": 16842879,
        "scrollViewStyle": 16842880,
        "spinnerStyle": 16842881,
        "starStyle": 16842882,
        "tabWidgetStyle": 16842883,
        "textViewStyle": 16842884,
        "webViewStyle": 16842885,
        "dropDownItemStyle": 16842886,
        "spinnerDropDownItemStyle": 16842887,
        "dropDownHintAppearance": 16842888,
        "spinnerItemStyle": 16842889,
        "mapViewStyle": 16842890,
        "preferenceScreenStyle": 16842891,
        "preferenceCategoryStyle": 16842892,
        "preferenceInformationStyle": 16842893,
        "preferenceStyle": 16842894,
        "checkBoxPreferenceStyle": 16842895,
        "yesNoPreferenceStyle": 16842896,
        "dialogPreferenceStyle": 16842897,
        "editTextPreferenceStyle": 16842898,
        "ringtonePreferenceStyle": 16842899,
        "preferenceLayoutChild": 16842900,
        "textSize": 16842901,
        "typeface": 16842902,
        "textStyle": 16842903,
        "textColor": 16842904,
        "textColorHighlight": 16842905,
        "textColorHint": 16842906,
        "textColorLink": 16842907,
        "state_focused": 16842908,
        "state_window_focused": 16842909,
        "state_enabled": 16842910,
        "state_checkable": 16842911,
        "state_checked": 16842912,
        "state_selected": 16842913,
        "state_active": 16842914,
        "state_single": 16842915,
        "state_first": 16842916,
        "state_middle": 16842917,
        "state_last": 16842918,
        "state_pressed": 16842919,
        "state_expanded": 16842920,
        "state_empty": 16842921,
        "state_above_anchor": 16842922,
        "ellipsize": 16842923,
        "x": 16842924,
        "y": 16842925,
        "windowAnimationStyle": 16842926,
        "gravity": 16842927,
        "autoLink": 16842928,
        "linksClickable": 16842929,
        "entries": 16842930,
        "layout_gravity": 16842931,
        "windowEnterAnimation": 16842932,
        "windowExitAnimation": 16842933,
        "windowShowAnimation": 16842934,
        "windowHideAnimation": 16842935,
        "activityOpenEnterAnimation": 16842936,
        "activityOpenExitAnimation": 16842937,
        "activityCloseEnterAnimation": 16842938,
        "activityCloseExitAnimation": 16842939,
        "taskOpenEnterAnimation": 16842940,
        "taskOpenExitAnimation": 16842941,
        "taskCloseEnterAnimation": 16842942,
        "taskCloseExitAnimation": 16842943,
        "taskToFrontEnterAnimation": 16842944,
        "taskToFrontExitAnimation": 16842945,
        "taskToBackEnterAnimation": 16842946,
        "taskToBackExitAnimation": 16842947,
        "orientation": 16842948,
        "keycode": 16842949,
        "fullDark": 16842950,
        "topDark": 16842951,
        "centerDark": 16842952,
        "bottomDark": 16842953,
        "fullBright": 16842954,
        "topBright": 16842955,
        "centerBright": 16842956,
        "bottomBright": 16842957,
        "bottomMedium": 16842958,
        "centerMedium": 16842959,
        "id": 16842960,
        "tag": 16842961,
        "scrollX": 16842962,
        "scrollY": 16842963,
        "background": 16842964,
        "padding": 16842965,
        "paddingLeft": 16842966,
        "paddingTop": 16842967,
        "paddingRight": 16842968,
        "paddingBottom": 16842969,
        "focusable": 16842970,
        "focusableInTouchMode": 16842971,
        "visibility": 16842972,
        "fitsSystemWindows": 16842973,
        "scrollbars": 16842974,
        "fadingEdge": 16842975,
        "fadingEdgeLength": 16842976,
        "nextFocusLeft": 16842977,
        "nextFocusRight": 16842978,
        "nextFocusUp": 16842979,
        "nextFocusDown": 16842980,
        "clickable": 16842981,
        "longClickable": 16842982,
        "saveEnabled": 16842983,
        "drawingCacheQuality": 16842984,
        "duplicateParentState": 16842985,
        "clipChildren": 16842986,
        "clipToPadding": 16842987,
        "layoutAnimation": 16842988,
        "animationCache": 16842989,
        "persistentDrawingCache": 16842990,
        "alwaysDrawnWithCache": 16842991,
        "addStatesFromChildren": 16842992,
        "descendantFocusability": 16842993,
        "layout": 16842994,
        "inflatedId": 16842995,
        "layout_width": 16842996,
        "layout_height": 16842997,
        "layout_margin": 16842998,
        "layout_marginLeft": 16842999,
        "layout_marginTop": 16843000,
        "layout_marginRight": 16843001,
        "layout_marginBottom": 16843002,
        "listSelector": 16843003,
        "drawSelectorOnTop": 16843004,
        "stackFromBottom": 16843005,
        "scrollingCache": 16843006,
        "textFilterEnabled": 16843007,
        "transcriptMode": 16843008,
        "cacheColorHint": 16843009,
        "dial": 16843010,
        "hand_hour": 16843011,
        "hand_minute": 16843012,
        "format": 16843013,
        "checked": 16843014,
        "button": 16843015,
        "checkMark": 16843016,
        "foreground": 16843017,
        "measureAllChildren": 16843018,
        "groupIndicator": 16843019,
        "childIndicator": 16843020,
        "indicatorLeft": 16843021,
        "indicatorRight": 16843022,
        "childIndicatorLeft": 16843023,
        "childIndicatorRight": 16843024,
        "childDivider": 16843025,
        "animationDuration": 16843026,
        "spacing": 16843027,
        "horizontalSpacing": 16843028,
        "verticalSpacing": 16843029,
        "stretchMode": 16843030,
        "columnWidth": 16843031,
        "numColumns": 16843032,
        "src": 16843033,
        "antialias": 16843034,
        "filter": 16843035,
        "dither": 16843036,
        "scaleType": 16843037,
        "adjustViewBounds": 16843038,
        "maxWidth": 16843039,
        "maxHeight": 16843040,
        "tint": 16843041,
        "baselineAlignBottom": 16843042,
        "cropToPadding": 16843043,
        "textOn": 16843044,
        "textOff": 16843045,
        "baselineAligned": 16843046,
        "baselineAlignedChildIndex": 16843047,
        "weightSum": 16843048,
        "divider": 16843049,
        "dividerHeight": 16843050,
        "choiceMode": 16843051,
        "itemTextAppearance": 16843052,
        "horizontalDivider": 16843053,
        "verticalDivider": 16843054,
        "headerBackground": 16843055,
        "itemBackground": 16843056,
        "itemIconDisabledAlpha": 16843057,
        "rowHeight": 16843058,
        "maxRows": 16843059,
        "maxItemsPerRow": 16843060,
        "moreIcon": 16843061,
        "max": 16843062,
        "progress": 16843063,
        "secondaryProgress": 16843064,
        "indeterminate": 16843065,
        "indeterminateOnly": 16843066,
        "indeterminateDrawable": 16843067,
        "progressDrawable": 16843068,
        "indeterminateDuration": 16843069,
        "indeterminateBehavior": 16843070,
        "minWidth": 16843071,
        "minHeight": 16843072,
        "interpolator": 16843073,
        "thumb": 16843074,
        "thumbOffset": 16843075,
        "numStars": 16843076,
        "rating": 16843077,
        "stepSize": 16843078,
        "isIndicator": 16843079,
        "checkedButton": 16843080,
        "stretchColumns": 16843081,
        "shrinkColumns": 16843082,
        "collapseColumns": 16843083,
        "layout_column": 16843084,
        "layout_span": 16843085,
        "bufferType": 16843086,
        "text": 16843087,
        "hint": 16843088,
        "textScaleX": 16843089,
        "cursorVisible": 16843090,
        "maxLines": 16843091,
        "lines": 16843092,
        "height": 16843093,
        "minLines": 16843094,
        "maxEms": 16843095,
        "ems": 16843096,
        "width": 16843097,
        "minEms": 16843098,
        "scrollHorizontally": 16843099,
        "password": 16843100,
        "singleLine": 16843101,
        "selectAllOnFocus": 16843102,
        "includeFontPadding": 16843103,
        "maxLength": 16843104,
        "shadowColor": 16843105,
        "shadowDx": 16843106,
        "shadowDy": 16843107,
        "shadowRadius": 16843108,
        "numeric": 16843109,
        "digits": 16843110,
        "phoneNumber": 16843111,
        "inputMethod": 16843112,
        "capitalize": 16843113,
        "autoText": 16843114,
        "editable": 16843115,
        "freezesText": 16843116,
        "drawableTop": 16843117,
        "drawableBottom": 16843118,
        "drawableLeft": 16843119,
        "drawableRight": 16843120,
        "drawablePadding": 16843121,
        "completionHint": 16843122,
        "completionHintView": 16843123,
        "completionThreshold": 16843124,
        "dropDownSelector": 16843125,
        "popupBackground": 16843126,
        "inAnimation": 16843127,
        "outAnimation": 16843128,
        "flipInterval": 16843129,
        "fillViewport": 16843130,
        "prompt": 16843131,
        "startYear": 16843132,
        "endYear": 16843133,
        "mode": 16843134,
        "layout_x": 16843135,
        "layout_y": 16843136,
        "layout_weight": 16843137,
        "layout_toLeftOf": 16843138,
        "layout_toRightOf": 16843139,
        "layout_above": 16843140,
        "layout_below": 16843141,
        "layout_alignBaseline": 16843142,
        "layout_alignLeft": 16843143,
        "layout_alignTop": 16843144,
        "layout_alignRight": 16843145,
        "layout_alignBottom": 16843146,
        "layout_alignParentLeft": 16843147,
        "layout_alignParentTop": 16843148,
        "layout_alignParentRight": 16843149,
        "layout_alignParentBottom": 16843150,
        "layout_centerInParent": 16843151,
        "layout_centerHorizontal": 16843152,
        "layout_centerVertical": 16843153,
        "layout_alignWithParentIfMissing": 16843154,
        "layout_scale": 16843155,
        "visible": 16843156,
        "variablePadding": 16843157,
        "constantSize": 16843158,
        "oneshot": 16843159,
        "duration": 16843160,
        "drawable": 16843161,
        "shape": 16843162,
        "innerRadiusRatio": 16843163,
        "thicknessRatio": 16843164,
        "startColor": 16843165,
        "endColor": 16843166,
        "useLevel": 16843167,
        "angle": 16843168,
        "type": 16843169,
        "centerX": 16843170,
        "centerY": 16843171,
        "gradientRadius": 16843172,
        "color": 16843173,
        "dashWidth": 16843174,
        "dashGap": 16843175,
        "radius": 16843176,
        "topLeftRadius": 16843177,
        "topRightRadius": 16843178,
        "bottomLeftRadius": 16843179,
        "bottomRightRadius": 16843180,
        "left": 16843181,
        "top": 16843182,
        "right": 16843183,
        "bottom": 16843184,
        "minLevel": 16843185,
        "maxLevel": 16843186,
        "fromDegrees": 16843187,
        "toDegrees": 16843188,
        "pivotX": 16843189,
        "pivotY": 16843190,
        "insetLeft": 16843191,
        "insetRight": 16843192,
        "insetTop": 16843193,
        "insetBottom": 16843194,
        "shareInterpolator": 16843195,
        "fillBefore": 16843196,
        "fillAfter": 16843197,
        "startOffset": 16843198,
        "repeatCount": 16843199,
        "repeatMode": 16843200,
        "zAdjustment": 16843201,
        "fromXScale": 16843202,
        "toXScale": 16843203,
        "fromYScale": 16843204,
        "toYScale": 16843205,
        "fromXDelta": 16843206,
        "toXDelta": 16843207,
        "fromYDelta": 16843208,
        "toYDelta": 16843209,
        "fromAlpha": 16843210,
        "toAlpha": 16843211,
        "delay": 16843212,
        "animation": 16843213,
        "animationOrder": 16843214,
        "columnDelay": 16843215,
        "rowDelay": 16843216,
        "direction": 16843217,
        "directionPriority": 16843218,
        "factor": 16843219,
        "cycles": 16843220,
        "searchMode": 16843221,
        "searchSuggestAuthority": 16843222,
        "searchSuggestPath": 16843223,
        "searchSuggestSelection": 16843224,
        "searchSuggestIntentAction": 16843225,
        "searchSuggestIntentData": 16843226,
        "queryActionMsg": 16843227,
        "suggestActionMsg": 16843228,
        "suggestActionMsgColumn": 16843229,
        "menuCategory": 16843230,
        "orderInCategory": 16843231,
        "checkableBehavior": 16843232,
        "title": 16843233,
        "titleCondensed": 16843234,
        "alphabeticShortcut": 16843235,
        "numericShortcut": 16843236,
        "checkable": 16843237,
        "selectable": 16843238,
        "orderingFromXml": 16843239,
        "key": 16843240,
        "summary": 16843241,
        "order": 16843242,
        "widgetLayout": 16843243,
        "dependency": 16843244,
        "defaultValue": 16843245,
        "shouldDisableView": 16843246,
        "summaryOn": 16843247,
        "summaryOff": 16843248,
        "disableDependentsState": 16843249,
        "dialogTitle": 16843250,
        "dialogMessage": 16843251,
        "dialogIcon": 16843252,
        "positiveButtonText": 16843253,
        "negativeButtonText": 16843254,
        "dialogLayout": 16843255,
        "entryValues": 16843256,
        "ringtoneType": 16843257,
        "showDefault": 16843258,
        "showSilent": 16843259,
        "scaleWidth": 16843260,
        "scaleHeight": 16843261,
        "scaleGravity": 16843262,
        "ignoreGravity": 16843263,
        "foregroundGravity": 16843264,
        "tileMode": 16843265,
        "targetActivity": 16843266,
        "alwaysRetainTaskState": 16843267,
        "allowTaskReparenting": 16843268,
        "searchButtonText": 16843269,
        "colorForegroundInverse": 16843270,
        "textAppearanceButton": 16843271,
        "listSeparatorTextViewStyle": 16843272,
        "streamType": 16843273,
        "clipOrientation": 16843274,
        "centerColor": 16843275,
        "minSdkVersion": 16843276,
        "windowFullscreen": 16843277,
        "unselectedAlpha": 16843278,
        "progressBarStyleSmallTitle": 16843279,
        "ratingBarStyleIndicator": 16843280,
        "apiKey": 16843281,
        "textColorTertiary": 16843282,
        "textColorTertiaryInverse": 16843283,
        "listDivider": 16843284,
        "soundEffectsEnabled": 16843285,
        "keepScreenOn": 16843286,
        "lineSpacingExtra": 16843287,
        "lineSpacingMultiplier": 16843288,
        "listChoiceIndicatorSingle": 16843289,
        "listChoiceIndicatorMultiple": 16843290,
        "versionCode": 16843291,
        "versionName": 16843292,
        "marqueeRepeatLimit": 16843293,
        "windowNoDisplay": 16843294,
        "backgroundDimEnabled": 16843295,
        "inputType": 16843296,
        "isDefault": 16843297,
        "windowDisablePreview": 16843298,
        "privateImeOptions": 16843299,
        "editorExtras": 16843300,
        "settingsActivity": 16843301,
        "fastScrollEnabled": 16843302,
        "reqTouchScreen": 16843303,
        "reqKeyboardType": 16843304,
        "reqHardKeyboard": 16843305,
        "reqNavigation": 16843306,
        "windowSoftInputMode": 16843307,
        "imeFullscreenBackground": 16843308,
        "noHistory": 16843309,
        "headerDividersEnabled": 16843310,
        "footerDividersEnabled": 16843311,
        "candidatesTextStyleSpans": 16843312,
        "smoothScrollbar": 16843313,
        "reqFiveWayNav": 16843314,
        "keyBackground": 16843315,
        "keyTextSize": 16843316,
        "labelTextSize": 16843317,
        "keyTextColor": 16843318,
        "keyPreviewLayout": 16843319,
        "keyPreviewOffset": 16843320,
        "keyPreviewHeight": 16843321,
        "verticalCorrection": 16843322,
        "popupLayout": 16843323,
        "state_long_pressable": 16843324,
        "keyWidth": 16843325,
        "keyHeight": 16843326,
        "horizontalGap": 16843327,
        "verticalGap": 16843328,
        "rowEdgeFlags": 16843329,
        "codes": 16843330,
        "popupKeyboard": 16843331,
        "popupCharacters": 16843332,
        "keyEdgeFlags": 16843333,
        "isModifier": 16843334,
        "isSticky": 16843335,
        "isRepeatable": 16843336,
        "iconPreview": 16843337,
        "keyOutputText": 16843338,
        "keyLabel": 16843339,
        "keyIcon": 16843340,
        "keyboardMode": 16843341,
        "isScrollContainer": 16843342,
        "fillEnabled": 16843343,
        "updatePeriodMillis": 16843344,
        "initialLayout": 16843345,
        "voiceSearchMode": 16843346,
        "voiceLanguageModel": 16843347,
        "voicePromptText": 16843348,
        "voiceLanguage": 16843349,
        "voiceMaxResults": 16843350,
        "bottomOffset": 16843351,
        "topOffset": 16843352,
        "allowSingleTap": 16843353,
        "handle": 16843354,
        "content": 16843355,
        "animateOnClick": 16843356,
        "configure": 16843357,
        "hapticFeedbackEnabled": 16843358,
        "innerRadius": 16843359,
        "thickness": 16843360,
        "sharedUserLabel": 16843361,
        "dropDownWidth": 16843362,
        "dropDownAnchor": 16843363,
        "imeOptions": 16843364,
        "imeActionLabel": 16843365,
        "imeActionId": 16843366,
        "imeExtractEnterAnimation": 16843368,
        "imeExtractExitAnimation": 16843369,
        "tension": 16843370,
        "extraTension": 16843371,
        "anyDensity": 16843372,
        "searchSuggestThreshold": 16843373,
        "includeInGlobalSearch": 16843374,
        "onClick": 16843375,
        "targetSdkVersion": 16843376,
        "maxSdkVersion": 16843377,
        "testOnly": 16843378,
        "contentDescription": 16843379,
        "gestureStrokeWidth": 16843380,
        "gestureColor": 16843381,
        "uncertainGestureColor": 16843382,
        "fadeOffset": 16843383,
        "fadeDuration": 16843384,
        "gestureStrokeType": 16843385,
        "gestureStrokeLengthThreshold": 16843386,
        "gestureStrokeSquarenessThreshold": 16843387,
        "gestureStrokeAngleThreshold": 16843388,
        "eventsInterceptionEnabled": 16843389,
        "fadeEnabled": 16843390,
        "backupAgent": 16843391,
        "allowBackup": 16843392,
        "glEsVersion": 16843393,
        "queryAfterZeroResults": 16843394,
        "dropDownHeight": 16843395,
        "smallScreens": 16843396,
        "normalScreens": 16843397,
        "largeScreens": 16843398,
        "progressBarStyleInverse": 16843399,
        "progressBarStyleSmallInverse": 16843400,
        "progressBarStyleLargeInverse": 16843401,
        "searchSettingsDescription": 16843402,
        "textColorPrimaryInverseDisableOnly": 16843403,
        "autoUrlDetect": 16843404,
        "resizeable": 16843405,
        "required": 16843406,
        "accountType": 16843407,
        "contentAuthority": 16843408,
        "userVisible": 16843409,
        "windowShowWallpaper": 16843410,
        "wallpaperOpenEnterAnimation": 16843411,
        "wallpaperOpenExitAnimation": 16843412,
        "wallpaperCloseEnterAnimation": 16843413,
        "wallpaperCloseExitAnimation": 16843414,
        "wallpaperIntraOpenEnterAnimation": 16843415,
        "wallpaperIntraOpenExitAnimation": 16843416,
        "wallpaperIntraCloseEnterAnimation": 16843417,
        "wallpaperIntraCloseExitAnimation": 16843418,
        "supportsUploading": 16843419,
        "killAfterRestore": 16843420,
        "restoreNeedsApplication": 16843421,
        "smallIcon": 16843422,
        "accountPreferences": 16843423,
        "textAppearanceSearchResultSubtitle": 16843424,
        "textAppearanceSearchResultTitle": 16843425,
        "summaryColumn": 16843426,
        "detailColumn": 16843427,
        "detailSocialSummary": 16843428,
        "thumbnail": 16843429,
        "detachWallpaper": 16843430,
        "finishOnCloseSystemDialogs": 16843431,
        "scrollbarFadeDuration": 16843432,
        "scrollbarDefaultDelayBeforeFade": 16843433,
        "fadeScrollbars": 16843434,
        "colorBackgroundCacheHint": 16843435,
        "dropDownHorizontalOffset": 16843436,
        "dropDownVerticalOffset": 16843437,
        "quickContactBadgeStyleWindowSmall": 16843438,
        "quickContactBadgeStyleWindowMedium": 16843439,
        "quickContactBadgeStyleWindowLarge": 16843440,
        "quickContactBadgeStyleSmallWindowSmall": 16843441,
        "quickContactBadgeStyleSmallWindowMedium": 16843442,
        "quickContactBadgeStyleSmallWindowLarge": 16843443,
        "author": 16843444,
        "autoStart": 16843445,
        "expandableListViewWhiteStyle": 16843446,
        "installLocation": 16843447,
        "vmSafeMode": 16843448,
        "webTextViewStyle": 16843449,
        "restoreAnyVersion": 16843450,
        "tabStripLeft": 16843451,
        "tabStripRight": 16843452,
        "tabStripEnabled": 16843453,
        "logo": 16843454,
        "xlargeScreens": 16843455,
        "immersive": 16843456,
        "overScrollMode": 16843457,
        "overScrollHeader": 16843458,
        "overScrollFooter": 16843459,
        "filterTouchesWhenObscured": 16843460,
        "textSelectHandleLeft": 16843461,
        "textSelectHandleRight": 16843462,
        "textSelectHandle": 16843463,
        "textSelectHandleWindowStyle": 16843464,
        "popupAnimationStyle": 16843465,
        "screenSize": 16843466,
        "screenDensity": 16843467,
        "allContactsName": 16843468,
        "windowActionBar": 16843469,
        "actionBarStyle": 16843470,
        "navigationMode": 16843471,
        "displayOptions": 16843472,
        "subtitle": 16843473,
        "customNavigationLayout": 16843474,
        "hardwareAccelerated": 16843475,
        "measureWithLargestChild": 16843476,
        "animateFirstView": 16843477,
        "dropDownSpinnerStyle": 16843478,
        "actionDropDownStyle": 16843479,
        "actionButtonStyle": 16843480,
        "showAsAction": 16843481,
        "previewImage": 16843482,
        "actionModeBackground": 16843483,
        "actionModeCloseDrawable": 16843484,
        "windowActionModeOverlay": 16843485,
        "valueFrom": 16843486,
        "valueTo": 16843487,
        "valueType": 16843488,
        "propertyName": 16843489,
        "ordering": 16843490,
        "fragment": 16843491,
        "windowActionBarOverlay": 16843492,
        "fragmentOpenEnterAnimation": 16843493,
        "fragmentOpenExitAnimation": 16843494,
        "fragmentCloseEnterAnimation": 16843495,
        "fragmentCloseExitAnimation": 16843496,
        "fragmentFadeEnterAnimation": 16843497,
        "fragmentFadeExitAnimation": 16843498,
        "actionBarSize": 16843499,
        "imeSubtypeLocale": 16843500,
        "imeSubtypeMode": 16843501,
        "imeSubtypeExtraValue": 16843502,
        "splitMotionEvents": 16843503,
        "listChoiceBackgroundIndicator": 16843504,
        "spinnerMode": 16843505,
        "animateLayoutChanges": 16843506,
        "actionBarTabStyle": 16843507,
        "actionBarTabBarStyle": 16843508,
        "actionBarTabTextStyle": 16843509,
        "actionOverflowButtonStyle": 16843510,
        "actionModeCloseButtonStyle": 16843511,
        "titleTextStyle": 16843512,
        "subtitleTextStyle": 16843513,
        "iconifiedByDefault": 16843514,
        "actionLayout": 16843515,
        "actionViewClass": 16843516,
        "activatedBackgroundIndicator": 16843517,
        "state_activated": 16843518,
        "listPopupWindowStyle": 16843519,
        "popupMenuStyle": 16843520,
        "textAppearanceLargePopupMenu": 16843521,
        "textAppearanceSmallPopupMenu": 16843522,
        "breadCrumbTitle": 16843523,
        "breadCrumbShortTitle": 16843524,
        "listDividerAlertDialog": 16843525,
        "textColorAlertDialogListItem": 16843526,
        "loopViews": 16843527,
        "dialogTheme": 16843528,
        "alertDialogTheme": 16843529,
        "dividerVertical": 16843530,
        "homeAsUpIndicator": 16843531,
        "enterFadeDuration": 16843532,
        "exitFadeDuration": 16843533,
        "selectableItemBackground": 16843534,
        "autoAdvanceViewId": 16843535,
        "useIntrinsicSizeAsMinimum": 16843536,
        "actionModeCutDrawable": 16843537,
        "actionModeCopyDrawable": 16843538,
        "actionModePasteDrawable": 16843539,
        "textEditPasteWindowLayout": 16843540,
        "textEditNoPasteWindowLayout": 16843541,
        "textIsSelectable": 16843542,
        "windowEnableSplitTouch": 16843543,
        "indeterminateProgressStyle": 16843544,
        "progressBarPadding": 16843545,
        "animationResolution": 16843546,
        "state_accelerated": 16843547,
        "baseline": 16843548,
        "homeLayout": 16843549,
        "opacity": 16843550,
        "alpha": 16843551,
        "transformPivotX": 16843552,
        "transformPivotY": 16843553,
        "translationX": 16843554,
        "translationY": 16843555,
        "scaleX": 16843556,
        "scaleY": 16843557,
        "rotation": 16843558,
        "rotationX": 16843559,
        "rotationY": 16843560,
        "showDividers": 16843561,
        "dividerPadding": 16843562,
        "borderlessButtonStyle": 16843563,
        "dividerHorizontal": 16843564,
        "itemPadding": 16843565,
        "buttonBarStyle": 16843566,
        "buttonBarButtonStyle": 16843567,
        "segmentedButtonStyle": 16843568,
        "staticWallpaperPreview": 16843569,
        "allowParallelSyncs": 16843570,
        "isAlwaysSyncable": 16843571,
        "verticalScrollbarPosition": 16843572,
        "fastScrollAlwaysVisible": 16843573,
        "fastScrollThumbDrawable": 16843574,
        "fastScrollPreviewBackgroundLeft": 16843575,
        "fastScrollPreviewBackgroundRight": 16843576,
        "fastScrollTrackDrawable": 16843577,
        "fastScrollOverlayPosition": 16843578,
        "customTokens": 16843579,
        "nextFocusForward": 16843580,
        "firstDayOfWeek": 16843581,
        "showWeekNumber": 16843582,
        "minDate": 16843583,
        "maxDate": 16843584,
        "shownWeekCount": 16843585,
        "selectedWeekBackgroundColor": 16843586,
        "focusedMonthDateColor": 16843587,
        "unfocusedMonthDateColor": 16843588,
        "weekNumberColor": 16843589,
        "weekSeparatorLineColor": 16843590,
        "selectedDateVerticalBar": 16843591,
        "weekDayTextAppearance": 16843592,
        "dateTextAppearance": 16843593,
        "solidColor": 16843594,
        "spinnersShown": 16843595,
        "calendarViewShown": 16843596,
        "state_multiline": 16843597,
        "detailsElementBackground": 16843598,
        "textColorHighlightInverse": 16843599,
        "textColorLinkInverse": 16843600,
        "editTextColor": 16843601,
        "editTextBackground": 16843602,
        "horizontalScrollViewStyle": 16843603,
        "layerType": 16843604,
        "alertDialogIcon": 16843605,
        "windowMinWidthMajor": 16843606,
        "windowMinWidthMinor": 16843607,
        "queryHint": 16843608,
        "fastScrollTextColor": 16843609,
        "largeHeap": 16843610,
        "windowCloseOnTouchOutside": 16843611,
        "datePickerStyle": 16843612,
        "calendarViewStyle": 16843613,
        "textEditSidePasteWindowLayout": 16843614,
        "textEditSideNoPasteWindowLayout": 16843615,
        "actionMenuTextAppearance": 16843616,
        "actionMenuTextColor": 16843617,
        "textCursorDrawable": 16843618,
        "resizeMode": 16843619,
        "requiresSmallestWidthDp": 16843620,
        "compatibleWidthLimitDp": 16843621,
        "largestWidthLimitDp": 16843622,
        "state_hovered": 16843623,
        "state_drag_can_accept": 16843624,
        "state_drag_hovered": 16843625,
        "stopWithTask": 16843626,
        "switchTextOn": 16843627,
        "switchTextOff": 16843628,
        "switchPreferenceStyle": 16843629,
        "switchTextAppearance": 16843630,
        "track": 16843631,
        "switchMinWidth": 16843632,
        "switchPadding": 16843633,
        "thumbTextPadding": 16843634,
        "textSuggestionsWindowStyle": 16843635,
        "textEditSuggestionItemLayout": 16843636,
        "rowCount": 16843637,
        "rowOrderPreserved": 16843638,
        "columnCount": 16843639,
        "columnOrderPreserved": 16843640,
        "useDefaultMargins": 16843641,
        "alignmentMode": 16843642,
        "layout_row": 16843643,
        "layout_rowSpan": 16843644,
        "layout_columnSpan": 16843645,
        "actionModeSelectAllDrawable": 16843646,
        "isAuxiliary": 16843647,
        "accessibilityEventTypes": 16843648,
        "packageNames": 16843649,
        "accessibilityFeedbackType": 16843650,
        "notificationTimeout": 16843651,
        "accessibilityFlags": 16843652,
        "canRetrieveWindowContent": 16843653,
        "listPreferredItemHeightLarge": 16843654,
        "listPreferredItemHeightSmall": 16843655,
        "actionBarSplitStyle": 16843656,
        "actionProviderClass": 16843657,
        "backgroundStacked": 16843658,
        "backgroundSplit": 16843659,
        "textAllCaps": 16843660,
        "colorPressedHighlight": 16843661,
        "colorLongPressedHighlight": 16843662,
        "colorFocusedHighlight": 16843663,
        "colorActivatedHighlight": 16843664,
        "colorMultiSelectHighlight": 16843665,
        "drawableStart": 16843666,
        "drawableEnd": 16843667,
        "actionModeStyle": 16843668,
        "minResizeWidth": 16843669,
        "minResizeHeight": 16843670,
        "actionBarWidgetTheme": 16843671,
        "uiOptions": 16843672,
        "subtypeLocale": 16843673,
        "subtypeExtraValue": 16843674,
        "actionBarDivider": 16843675,
        "actionBarItemBackground": 16843676,
        "actionModeSplitBackground": 16843677,
        "textAppearanceListItem": 16843678,
        "textAppearanceListItemSmall": 16843679,
        "targetDescriptions": 16843680,
        "directionDescriptions": 16843681,
        "overridesImplicitlyEnabledSubtype": 16843682,
        "listPreferredItemPaddingLeft": 16843683,
        "listPreferredItemPaddingRight": 16843684,
        "requiresFadingEdge": 16843685,
        "publicKey": 16843686,
        "parentActivityName": 16843687,
        "isolatedProcess": 16843689,
        "importantForAccessibility": 16843690,
        "keyboardLayout": 16843691,
        "fontFamily": 16843692,
        "mediaRouteButtonStyle": 16843693,
        "mediaRouteTypes": 16843694,
        "supportsRtl": 16843695,
        "textDirection": 16843696,
        "textAlignment": 16843697,
        "layoutDirection": 16843698,
        "paddingStart": 16843699,
        "paddingEnd": 16843700,
        "layout_marginStart": 16843701,
        "layout_marginEnd": 16843702,
        "layout_toStartOf": 16843703,
        "layout_toEndOf": 16843704,
        "layout_alignStart": 16843705,
        "layout_alignEnd": 16843706,
        "layout_alignParentStart": 16843707,
        "layout_alignParentEnd": 16843708,
        "listPreferredItemPaddingStart": 16843709,
        "listPreferredItemPaddingEnd": 16843710,
        "singleUser": 16843711,
        "presentationTheme": 16843712,
        "subtypeId": 16843713,
        "initialKeyguardLayout": 16843714,
        "widgetCategory": 16843716,
        "permissionGroupFlags": 16843717,
        "labelFor": 16843718,
        "permissionFlags": 16843719,
        "checkedTextViewStyle": 16843720,
        "showOnLockScreen": 16843721,
        "format12Hour": 16843722,
        "format24Hour": 16843723,
        "timeZone": 16843724,
        "mipMap": 16843725,
        "mirrorForRtl": 16843726,
        "windowOverscan": 16843727,
        "requiredForAllUsers": 16843728,
        "indicatorStart": 16843729,
        "indicatorEnd": 16843730,
        "childIndicatorStart": 16843731,
        "childIndicatorEnd": 16843732,
        "restrictedAccountType": 16843733,
        "requiredAccountType": 16843734,
        "canRequestTouchExplorationMode": 16843735,
        "canRequestEnhancedWebAccessibility": 16843736,
        "canRequestFilterKeyEvents": 16843737,
        "layoutMode": 16843738,
        "keySet": 16843739,
        "targetId": 16843740,
        "fromScene": 16843741,
        "toScene": 16843742,
        "transition": 16843743,
        "transitionOrdering": 16843744,
        "fadingMode": 16843745,
        "startDelay": 16843746,
        "ssp": 16843747,
        "sspPrefix": 16843748,
        "sspPattern": 16843749,
        "addPrintersActivity": 16843750,
        "vendor": 16843751,
        "category": 16843752,
        "isAsciiCapable": 16843753,
        "autoMirrored": 16843754,
        "supportsSwitchingToNextInputMethod": 16843755,
        "requireDeviceUnlock": 16843756,
        "apduServiceBanner": 16843757,
        "accessibilityLiveRegion": 16843758,
        "windowTranslucentStatus": 16843759,
        "windowTranslucentNavigation": 16843760,
        "advancedPrintOptionsActivity": 16843761,
        "banner": 16843762,
        "windowSwipeToDismiss": 16843763,
        "isGame": 16843764,
        "allowEmbedded": 16843765,
        "setupActivity": 16843766,
        "fastScrollStyle": 16843767,
        "windowContentTransitions": 16843768,
        "windowContentTransitionManager": 16843769,
        "translationZ": 16843770,
        "tintMode": 16843771,
        "controlX1": 16843772,
        "controlY1": 16843773,
        "controlX2": 16843774,
        "controlY2": 16843775,
        "transitionName": 16843776,
        "transitionGroup": 16843777,
        "viewportWidth": 16843778,
        "viewportHeight": 16843779,
        "fillColor": 16843780,
        "pathData": 16843781,
        "strokeColor": 16843782,
        "strokeWidth": 16843783,
        "trimPathStart": 16843784,
        "trimPathEnd": 16843785,
        "trimPathOffset": 16843786,
        "strokeLineCap": 16843787,
        "strokeLineJoin": 16843788,
        "strokeMiterLimit": 16843789,
        "colorControlNormal": 16843817,
        "colorControlActivated": 16843818,
        "colorButtonNormal": 16843819,
        "colorControlHighlight": 16843820,
        "persistableMode": 16843821,
        "titleTextAppearance": 16843822,
        "subtitleTextAppearance": 16843823,
        "slideEdge": 16843824,
        "actionBarTheme": 16843825,
        "textAppearanceListItemSecondary": 16843826,
        "colorPrimary": 16843827,
        "colorPrimaryDark": 16843828,
        "colorAccent": 16843829,
        "nestedScrollingEnabled": 16843830,
        "windowEnterTransition": 16843831,
        "windowExitTransition": 16843832,
        "windowSharedElementEnterTransition": 16843833,
        "windowSharedElementExitTransition": 16843834,
        "windowAllowReturnTransitionOverlap": 16843835,
        "windowAllowEnterTransitionOverlap": 16843836,
        "sessionService": 16843837,
        "stackViewStyle": 16843838,
        "switchStyle": 16843839,
        "elevation": 16843840,
        "excludeId": 16843841,
        "excludeClass": 16843842,
        "hideOnContentScroll": 16843843,
        "actionOverflowMenuStyle": 16843844,
        "documentLaunchMode": 16843845,
        "maxRecents": 16843846,
        "autoRemoveFromRecents": 16843847,
        "stateListAnimator": 16843848,
        "toId": 16843849,
        "fromId": 16843850,
        "reversible": 16843851,
        "splitTrack": 16843852,
        "targetName": 16843853,
        "excludeName": 16843854,
        "matchOrder": 16843855,
        "windowDrawsSystemBarBackgrounds": 16843856,
        "statusBarColor": 16843857,
        "navigationBarColor": 16843858,
        "contentInsetStart": 16843859,
        "contentInsetEnd": 16843860,
        "contentInsetLeft": 16843861,
        "contentInsetRight": 16843862,
        "paddingMode": 16843863,
        "layout_rowWeight": 16843864,
        "layout_columnWeight": 16843865,
        "translateX": 16843866,
        "translateY": 16843867,
        "selectableItemBackgroundBorderless": 16843868,
        "elegantTextHeight": 16843869,
        "searchKeyphraseId": 16843870,
        "searchKeyphrase": 16843871,
        "searchKeyphraseSupportedLocales": 16843872,
        "windowTransitionBackgroundFadeDuration": 16843873,
        "overlapAnchor": 16843874,
        "progressTint": 16843875,
        "progressTintMode": 16843876,
        "progressBackgroundTint": 16843877,
        "progressBackgroundTintMode": 16843878,
        "secondaryProgressTint": 16843879,
        "secondaryProgressTintMode": 16843880,
        "indeterminateTint": 16843881,
        "indeterminateTintMode": 16843882,
        "backgroundTint": 16843883,
        "backgroundTintMode": 16843884,
        "foregroundTint": 16843885,
        "foregroundTintMode": 16843886,
        "buttonTint": 16843887,
        "buttonTintMode": 16843888,
        "thumbTint": 16843889,
        "thumbTintMode": 16843890,
        "fullBackupOnly": 16843891,
        "propertyXName": 16843892,
        "propertyYName": 16843893,
        "relinquishTaskIdentity": 16843894,
        "tileModeX": 16843895,
        "tileModeY": 16843896,
        "actionModeShareDrawable": 16843897,
        "actionModeFindDrawable": 16843898,
        "actionModeWebSearchDrawable": 16843899,
        "transitionVisibilityMode": 16843900,
        "minimumHorizontalAngle": 16843901,
        "minimumVerticalAngle": 16843902,
        "maximumAngle": 16843903,
        "searchViewStyle": 16843904,
        "closeIcon": 16843905,
        "goIcon": 16843906,
        "searchIcon": 16843907,
        "voiceIcon": 16843908,
        "commitIcon": 16843909,
        "suggestionRowLayout": 16843910,
        "queryBackground": 16843911,
        "submitBackground": 16843912,
        "buttonBarPositiveButtonStyle": 16843913,
        "buttonBarNeutralButtonStyle": 16843914,
        "buttonBarNegativeButtonStyle": 16843915,
        "popupElevation": 16843916,
        "actionBarPopupTheme": 16843917,
        "multiArch": 16843918,
        "touchscreenBlocksFocus": 16843919,
        "windowElevation": 16843920,
        "launchTaskBehindTargetAnimation": 16843921,
        "launchTaskBehindSourceAnimation": 16843922,
        "restrictionType": 16843923,
        "dayOfWeekBackground": 16843924,
        "dayOfWeekTextAppearance": 16843925,
        "headerMonthTextAppearance": 16843926,
        "headerDayOfMonthTextAppearance": 16843927,
        "headerYearTextAppearance": 16843928,
        "yearListItemTextAppearance": 16843929,
        "yearListSelectorColor": 16843930,
        "calendarTextColor": 16843931,
        "recognitionService": 16843932,
        "timePickerStyle": 16843933,
        "timePickerDialogTheme": 16843934,
        "headerTimeTextAppearance": 16843935,
        "headerAmPmTextAppearance": 16843936,
        "numbersTextColor": 16843937,
        "numbersBackgroundColor": 16843938,
        "numbersSelectorColor": 16843939,
        "amPmTextColor": 16843940,
        "amPmBackgroundColor": 16843941,
        "searchKeyphraseRecognitionFlags": 16843942,
        "checkMarkTint": 16843943,
        "checkMarkTintMode": 16843944,
        "popupTheme": 16843945,
        "toolbarStyle": 16843946,
        "windowClipToOutline": 16843947,
        "datePickerDialogTheme": 16843948,
        "showText": 16843949,
        "windowReturnTransition": 16843950,
        "windowReenterTransition": 16843951,
        "windowSharedElementReturnTransition": 16843952,
        "windowSharedElementReenterTransition": 16843953,
        "resumeWhilePausing": 16843954,
        "datePickerMode": 16843955,
        "timePickerMode": 16843956,
        "inset": 16843957,
        "letterSpacing": 16843958,
        "fontFeatureSettings": 16843959,
        "outlineProvider": 16843960,
        "contentAgeHint": 16843961,
        "country": 16843962,
        "windowSharedElementsUseOverlay": 16843963,
        "reparent": 16843964,
        "reparentWithOverlay": 16843965,
        "ambientShadowAlpha": 16843966,
        "spotShadowAlpha": 16843967,
        "navigationIcon": 16843968,
        "navigationContentDescription": 16843969,
        "fragmentExitTransition": 16843970,
        "fragmentEnterTransition": 16843971,
        "fragmentSharedElementEnterTransition": 16843972,
        "fragmentReturnTransition": 16843973,
        "fragmentSharedElementReturnTransition": 16843974,
        "fragmentReenterTransition": 16843975,
        "fragmentAllowEnterTransitionOverlap": 16843976,
        "fragmentAllowReturnTransitionOverlap": 16843977,
        "patternPathData": 16843978,
        "strokeAlpha": 16843979,
        "fillAlpha": 16843980,
        "windowActivityTransitions": 16843981,
        "colorEdgeEffect": 16843982,
    },
}

SYSTEM_RESOURCES = {
    "attributes": {
        "forward": {k: v for k, v in resources["attr"].items()},
        "inverse": {v: k for k, v in resources["attr"].items()},
    },
    "styles": {
        "forward": {k: v for k, v in resources["style"].items()},
        "inverse": {v: k for k, v in resources["style"].items()},
    },
}


class AXMLParser(object):
    def __init__(self, raw_buff):
        self.reset()

        self.valid_axml = True
        self.buff = BuffHandle(raw_buff)

        axml_file = unpack("<L", self.buff.read(4))[0]

        if axml_file == CHUNK_AXML_FILE:
            self.buff.read(4)

            self.sb = StringBlock(self.buff)

            self.m_resourceIDs = []
            self.m_prefixuri = {}
            self.m_uriprefix = {}
            self.m_prefixuriL = []

            self.visited_ns = []
        else:
            self.valid_axml = False
            print >>sys.stderr, ("Not a valid xml file")

    def is_valid(self):
        return self.valid_axml

    def reset(self):
        self.m_event = -1
        self.m_lineNumber = -1
        self.m_name = -1
        self.m_namespaceUri = -1
        self.m_attributes = []
        self.m_idAttribute = -1
        self.m_classAttribute = -1
        self.m_styleAttribute = -1

    def next(self):
        self.doNext()
        return self.m_event

    def doNext(self):
        if self.m_event == END_DOCUMENT:
            return

        event = self.m_event

        self.reset()
        while True:
            chunkType = -1

            # Fake END_DOCUMENT event.
            if event == END_TAG:
                pass

            # START_DOCUMENT
            if event == START_DOCUMENT:
                chunkType = CHUNK_XML_START_TAG
            else:
                if self.buff.end():
                    self.m_event = END_DOCUMENT
                    break
                chunkType = unpack("<L", self.buff.read(4))[0]

            if chunkType == CHUNK_RESOURCEIDS:
                chunkSize = unpack("<L", self.buff.read(4))[0]
                # FIXME
                if chunkSize < 8 or chunkSize % 4 != 0:
                    print >>sys.stderr, ("Invalid chunk size")

                for i in range(0, int(chunkSize / 4) - 2):
                    self.m_resourceIDs.append(unpack("<L", self.buff.read(4))[0])

                continue

            # FIXME
            if chunkType < CHUNK_XML_FIRST or chunkType > CHUNK_XML_LAST:
                print >>sys.stderr, ("invalid chunk type")

            # Fake START_DOCUMENT event.
            if chunkType == CHUNK_XML_START_TAG and event == -1:
                self.m_event = START_DOCUMENT
                break

            self.buff.read(4)  # /*chunkSize*/
            lineNumber = unpack("<L", self.buff.read(4))[0]
            self.buff.read(4)  # 0xFFFFFFFF

            if (
                chunkType == CHUNK_XML_START_NAMESPACE
                or chunkType == CHUNK_XML_END_NAMESPACE
            ):
                if chunkType == CHUNK_XML_START_NAMESPACE:
                    prefix = unpack("<L", self.buff.read(4))[0]
                    uri = unpack("<L", self.buff.read(4))[0]

                    self.m_prefixuri[prefix] = uri
                    self.m_uriprefix[uri] = prefix
                    self.m_prefixuriL.append((prefix, uri))
                    self.ns = uri
                else:
                    self.ns = -1
                    self.buff.read(4)
                    self.buff.read(4)
                    (prefix, uri) = self.m_prefixuriL.pop()

                continue

            self.m_lineNumber = lineNumber

            if chunkType == CHUNK_XML_START_TAG:
                self.m_namespaceUri = unpack("<L", self.buff.read(4))[0]
                self.m_name = unpack("<L", self.buff.read(4))[0]

                # FIXME
                self.buff.read(4)  # flags

                attributeCount = unpack("<L", self.buff.read(4))[0]
                self.m_idAttribute = (attributeCount >> 16) - 1
                attributeCount = attributeCount & 0xFFFF
                self.m_classAttribute = unpack("<L", self.buff.read(4))[0]
                self.m_styleAttribute = (self.m_classAttribute >> 16) - 1

                self.m_classAttribute = (self.m_classAttribute & 0xFFFF) - 1

                for i in range(0, attributeCount * ATTRIBUTE_LENGHT):
                    self.m_attributes.append(unpack("<L", self.buff.read(4))[0])

                for i in range(
                    ATTRIBUTE_IX_VALUE_TYPE, len(self.m_attributes), ATTRIBUTE_LENGHT
                ):
                    self.m_attributes[i] = self.m_attributes[i] >> 24

                self.m_event = START_TAG
                break

            if chunkType == CHUNK_XML_END_TAG:
                self.m_namespaceUri = unpack("<L", self.buff.read(4))[0]
                self.m_name = unpack("<L", self.buff.read(4))[0]
                self.m_event = END_TAG
                break

            if chunkType == CHUNK_XML_TEXT:
                self.m_name = unpack("<L", self.buff.read(4))[0]

                # FIXME
                self.buff.read(4)
                self.buff.read(4)

                self.m_event = TEXT
                break

    def getPrefixByUri(self, uri):
        try:
            return self.m_uriprefix[uri]
        except KeyError:
            return -1

    def getPrefix(self):
        try:
            return self.sb.getString(self.m_uriprefix[self.m_namespaceUri])
        except KeyError:
            return u""

    def getName(self):
        if self.m_name == -1 or (self.m_event != START_TAG and self.m_event != END_TAG):
            return u""

        return self.sb.getString(self.m_name)

    def getText(self):
        if self.m_name == -1 or self.m_event != TEXT:
            return u""

        return self.sb.getString(self.m_name)

    def getNamespacePrefix(self, pos):
        prefix = self.m_prefixuriL[pos][0]
        return self.sb.getString(prefix)

    def getNamespaceUri(self, pos):
        uri = self.m_prefixuriL[pos][1]
        return self.sb.getString(uri)

    def getXMLNS(self):
        buff = ""
        for i in self.m_uriprefix:
            if i not in self.visited_ns:
                buff += 'xmlns:%s="%s"\n' % (
                    self.sb.getString(self.m_uriprefix[i]),
                    self.sb.getString(self.m_prefixuri[self.m_uriprefix[i]]),
                )
                self.visited_ns.append(i)
        return buff

    def getNamespaceCount(self, pos):
        pass

    def getAttributeOffset(self, index):
        # FIXME
        if self.m_event != START_TAG:
            print >>sys.stderr, ("Current event is not START_TAG.")

        offset = index * 5
        # FIXME
        if offset >= len(self.m_attributes):
            print >>sys.stderr, ("Invalid attribute index")

        return offset

    def getAttributeCount(self):
        if self.m_event != START_TAG:
            return -1

        return len(self.m_attributes) / ATTRIBUTE_LENGHT

    def getAttributePrefix(self, index):
        offset = self.getAttributeOffset(index)
        uri = self.m_attributes[offset + ATTRIBUTE_IX_NAMESPACE_URI]

        prefix = self.getPrefixByUri(uri)

        if prefix == -1:
            return ""

        return self.sb.getString(prefix)

    def getAttributeName(self, index):
        offset = self.getAttributeOffset(index)
        name = self.m_attributes[offset + ATTRIBUTE_IX_NAME]

        if name == -1:
            return ""

        res = self.sb.getString(name)
        if not res:
            attr = self.m_resourceIDs[name]
            if attr in SYSTEM_RESOURCES["attributes"]["inverse"]:
                res = "android:" + SYSTEM_RESOURCES["attributes"]["inverse"][attr]

        return res

    def getAttributeValueType(self, index):
        offset = self.getAttributeOffset(index)
        return self.m_attributes[offset + ATTRIBUTE_IX_VALUE_TYPE]

    def getAttributeValueData(self, index):
        offset = self.getAttributeOffset(index)
        return self.m_attributes[offset + ATTRIBUTE_IX_VALUE_DATA]

    def getAttributeValue(self, index):
        offset = self.getAttributeOffset(index)
        valueType = self.m_attributes[offset + ATTRIBUTE_IX_VALUE_TYPE]
        if valueType == TYPE_STRING:
            valueString = self.m_attributes[offset + ATTRIBUTE_IX_VALUE_STRING]
            return self.sb.getString(valueString)
        # WIP
        return ""


TYPE_ATTRIBUTE = 2
TYPE_DIMENSION = 5
TYPE_FIRST_COLOR_INT = 28
TYPE_FIRST_INT = 16
TYPE_FLOAT = 4
TYPE_FRACTION = 6
TYPE_INT_BOOLEAN = 18
TYPE_INT_COLOR_ARGB4 = 30
TYPE_INT_COLOR_ARGB8 = 28
TYPE_INT_COLOR_RGB4 = 31
TYPE_INT_COLOR_RGB8 = 29
TYPE_INT_DEC = 16
TYPE_INT_HEX = 17
TYPE_LAST_COLOR_INT = 31
TYPE_LAST_INT = 31
TYPE_NULL = 0
TYPE_REFERENCE = 1
TYPE_STRING = 3

TYPE_TABLE = {
    TYPE_ATTRIBUTE: "attribute",
    TYPE_DIMENSION: "dimension",
    TYPE_FLOAT: "float",
    TYPE_FRACTION: "fraction",
    TYPE_INT_BOOLEAN: "int_boolean",
    TYPE_INT_COLOR_ARGB4: "int_color_argb4",
    TYPE_INT_COLOR_ARGB8: "int_color_argb8",
    TYPE_INT_COLOR_RGB4: "int_color_rgb4",
    TYPE_INT_COLOR_RGB8: "int_color_rgb8",
    TYPE_INT_DEC: "int_dec",
    TYPE_INT_HEX: "int_hex",
    TYPE_NULL: "null",
    TYPE_REFERENCE: "reference",
    TYPE_STRING: "string",
}

RADIX_MULTS = [0.00390625, 3.051758e-005, 1.192093e-007, 4.656613e-010]
DIMENSION_UNITS = ["px", "dip", "sp", "pt", "in", "mm"]
FRACTION_UNITS = ["%", "%p"]

COMPLEX_UNIT_MASK = 15


def complexToFloat(xcomplex):
    return (float)(xcomplex & 0xFFFFFF00) * RADIX_MULTS[(xcomplex >> 4) & 3]


def getPackage(id):
    if id >> 24 == 1:
        return "android:"
    return ""


def format_value(_type, _data, lookup_string=lambda ix: "<string>"):
    if _type == TYPE_STRING:
        return lookup_string(_data)

    elif _type == TYPE_ATTRIBUTE:
        return "?%s%08X" % (getPackage(_data), _data)

    elif _type == TYPE_REFERENCE:
        return "@%s%08X" % (getPackage(_data), _data)

    elif _type == TYPE_FLOAT:
        return "%f" % unpack("=f", pack("=L", _data))[0]

    elif _type == TYPE_INT_HEX:
        return "0x%08X" % _data

    elif _type == TYPE_INT_BOOLEAN:
        if _data == 0:
            return "false"
        return "true"

    elif _type == TYPE_DIMENSION:
        return "%f%s" % (
            complexToFloat(_data),
            DIMENSION_UNITS[_data & COMPLEX_UNIT_MASK],
        )

    elif _type == TYPE_FRACTION:
        return "%f%s" % (
            complexToFloat(_data) * 100,
            FRACTION_UNITS[_data & COMPLEX_UNIT_MASK],
        )

    elif _type >= TYPE_FIRST_COLOR_INT and _type <= TYPE_LAST_COLOR_INT:
        return "#%08X" % _data

    elif _type >= TYPE_FIRST_INT and _type <= TYPE_LAST_INT:
        return "%d" % long2int(_data)

    return "<0x%X, type 0x%02X>" % (_data, _type)


def long2int(l):
    if l > 0x7FFFFFFF:
        l = (0x7FFFFFFF & l) - 0x80000000
    return l


class AXMLPrinter(object):
    def __init__(self, raw_buff):
        self.axml = AXMLParser(raw_buff)
        self.xmlns = False

        self.buff = u""

        while True and self.axml.is_valid():
            _type = self.axml.next()

            if _type == START_DOCUMENT:
                self.buff += u'<?xml version="1.0" encoding="utf-8"?>\n'
            elif _type == START_TAG:
                self.buff += (
                    u"<"
                    + self.getPrefix(self.axml.getPrefix())
                    + self.axml.getName()
                    + u"\n"
                )
                self.buff += self.axml.getXMLNS()

                for i in range(0, self.axml.getAttributeCount()):
                    self.buff += '%s%s="%s"\n' % (
                        self.getPrefix(self.axml.getAttributePrefix(i)),
                        self.axml.getAttributeName(i),
                        self._escape(self.getAttributeValue(i)),
                    )

                self.buff += u">\n"

            elif _type == END_TAG:
                self.buff += "</%s%s>\n" % (
                    self.getPrefix(self.axml.getPrefix()),
                    self.axml.getName(),
                )

            elif _type == TEXT:
                self.buff += "%s\n" % self.axml.getText()

            elif _type == END_DOCUMENT:
                break

    # pleed patch
    def _escape(self, s):
        s = s.replace("&", "&amp;")
        s = s.replace('"', "&quot;")
        s = s.replace("'", "&apos;")
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        return escape(s)

    def get_buff(self):
        return self.buff.encode("utf-8")

    def get_xml(self):
        return minidom.parseString(self.get_buff()).toprettyxml(encoding="utf-8")

    def get_xml_obj(self):
        return minidom.parseString(self.get_buff())

    def getPrefix(self, prefix):
        if prefix is None or len(prefix) == 0:
            return u""

        return prefix + u":"

    def getAttributeValue(self, index):
        _type = self.axml.getAttributeValueType(index)
        _data = self.axml.getAttributeValueData(index)

        return format_value(_type, _data, lambda _: self.axml.getAttributeValue(index))
