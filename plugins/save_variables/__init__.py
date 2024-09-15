# -*- coding: utf-8 -*-
"""
MusicBrainz Picard: Save Variables Plugin

Copyright (c) Bob Swift 2024

This plugin uses code from the 'View script variables' plugin by Sophist.
"""
# pylint: disable=wrong-import-position
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring

PLUGIN_NAME = 'Save Script Variables'
PLUGIN_AUTHOR = 'Bob Swift (rdswift)'
PLUGIN_DESCRIPTION = '''This is an enhanced version of the 'View script variables'
plugin by Sophist, that also allows the list of variables to be saved to a text
file as a tab-separated list. Most of the original plugin code has been reused.

The plugin displays a dialog box listing the metadata variables for the track/file.
This allows you to see metadata variables beginning with "~" which are not normally
visible in the metadata pane of the main Picard window, which can be useful when you
are writing tagging or file naming scripts. This list can optionally be saved to a
text file.
'''
PLUGIN_VERSION = '1.0'
PLUGIN_API_VERSIONS = ['2.0']
PLUGIN_LICENSE = "GPL-2.0"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-2.0.html"

import os
import re

from PyQt5 import (
    QtCore,
    QtWidgets,
)
from picard.config import get_config
from picard.const.sys import IS_WIN
from picard.file import File
from picard.track import Track
from picard.ui.itemviews import (
    BaseAction,
    register_file_action,
    register_track_action,
)
from picard.util import (
    normpath,
    replace_win32_incompat,
    sanitize_filename,
)
from picard.util.textencoding import replace_non_ascii


try:
    from picard.util.tags import PRESERVED_TAGS
except ImportError:
    PRESERVED_TAGS = File._default_preserved_tags

from picard.plugins.save_variables.ui_save_variables_dialog import (
    Ui_SaveVariablesDialog,
)


RE_REPLACE_UNDERSCORES = re.compile(r'[\s_]+')


def make_filename(text: str) -> str:
    """Sanitize the file name provided so that it can be used safely.

    Args:
        text (str): File name to sanitize.

    Returns:
        str: Sanitized file name.
    """
    config = get_config()
    settings = config.setting
    win_compat = IS_WIN or settings['windows_compatibility']

    # Set default for Picard versions earlier than v2.9
    replace_dir_separator = settings['replace_dir_separator'] if settings['replace_dir_separator'] is not None else '_'

    sanitized = text

    # replace non-ASCII characters
    if settings['ascii_filenames']:
        sanitized = replace_non_ascii(sanitized, win_compat=win_compat)

    # replace incompatible characters
    if win_compat:
        # In Picard versions earlier than v2.9 the `win_compat_replacements` parameter isn't supported and returns None
        sanitized = replace_win32_incompat(sanitized, replacements=settings['win_compat_replacements'])

    if settings["replace_spaces_with_underscores"]:
        sanitized = RE_REPLACE_UNDERSCORES.sub('_', sanitized.strip())

    # remove null characters
    sanitized = sanitized.replace("\x00", "")

    return sanitize_filename(sanitized, repl=replace_dir_separator, win_compat=win_compat)


class SaveVariables(BaseAction):    # pylint: disable=too-few-public-methods
    NAME = 'View / Save Script Variables'

    def callback(self, objs):   # pylint: disable=missing-function-docstring
        obj = objs[0]
        files = self.tagger.get_files_from_objects(objs)
        if files:
            obj = files[0]
        dialog = SaveVariablesDialog(obj)
        dialog.exec_()


class SaveVariablesDialog(QtWidgets.QDialog):

    def __init__(self, obj, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_SaveVariablesDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self._save_file)
        self.ui.buttonBox.rejected.connect(self.reject)
        metadata = obj.metadata
        if isinstance(obj, File):
            self.setWindowTitle(f"File: {obj.base_filename}")
            self.base_name = f"[File] {obj.base_filename}"
        elif isinstance(obj, Track):
            tn = metadata['tracknumber']
            if len(tn) == 1:
                tn = "0" + tn
            self.setWindowTitle(f"Track: {tn} {metadata['title']}")
            self.base_name = f"[Track] {tn} {metadata['title']}"
        else:
            self.setWindowTitle("Variables")
            self.base_name = 'Variables'
        self.text_lines = []
        self._display_metadata(metadata)

    def _display_metadata(self, metadata):
        keys = metadata.keys()
        keys = sorted(keys, key=lambda key:
                      '0' + key if key in PRESERVED_TAGS and key.startswith('~') else
                      '1' + key if key.startswith('~') else
                      '2' + key)
        media = hidden = album = False
        table = self.ui.metadata_table
        key_example, value_example = self._get_table_items(table, 0)
        self.key_flags = key_example.flags()
        self.value_flags = value_example.flags()
        table.setRowCount(len(keys) + 3)
        i = 0
        for key in keys:
            if key in PRESERVED_TAGS and key.startswith('~'):
                if not media:
                    self._add_separator_row(table, i, "File variables")
                    i += 1
                    media = True
            elif key.startswith('~'):
                if not hidden:
                    self._add_separator_row(table, i, "Hidden variables")
                    i += 1
                    hidden = True
            else:
                if not album:
                    self._add_separator_row(table, i, "Tag variables")
                    i += 1
                    album = True

            key_item, value_item = self._get_table_items(table, i)
            i += 1
            key_item.setText("_" + key[1:] if key.startswith('~') else key)
            if key in metadata:
                value = metadata.getall(key)
                if len(value) == 1 and value[0] != '':
                    value = value[0]
                else:
                    value = repr(value)
                value_item.setText(value)
                self.text_lines.append(f"{key_item.text()}\t{value}")

    def _add_separator_row(self, table, i, title):
        key_item, _value_item = self._get_table_items(table, i)
        font = key_item.font()
        font.setBold(True)
        key_item.setFont(font)
        key_item.setText(title)

    def _get_table_items(self, table, i):
        key_item = table.item(i, 0)
        value_item = table.item(i, 1)
        if not key_item:
            key_item = QtWidgets.QTableWidgetItem()
            key_item.setFlags(self.key_flags)
            table.setItem(i, 0, key_item)
        if not value_item:
            value_item = QtWidgets.QTableWidgetItem()
            value_item.setFlags(self.value_flags)
            table.setItem(i, 1, value_item)
        return key_item, value_item

    def _save_file(self):
        file_path = self._get_file_path()
        if not file_path:
            return

        error = None
        title = 'Export Variables'
        file_name = os.path.split(file_path)[1]

        try:
            with open(file_path, 'w', encoding='utf-8') as o_file:
                o_file.write('\n'.join(self.text_lines) + '\n')
            icon = QtWidgets.QMessageBox.Icon.Information
            text = f"Variables successfully exported to \"{file_name}\""

        except OSError as error:
            icon = QtWidgets.QMessageBox.Icon.Critical
            text = f"Error exporting variables to \"{file_name}\"\n\nError message: {error.strerror}"

        dialog = QtWidgets.QMessageBox(
            icon,
            title,
            text,
            QtWidgets.QMessageBox.StandardButton.Ok,
            self,
        )
        dialog.exec()

        if error is None:
            self.close()

    def _get_file_path(self):
        config = get_config()
        default_directory = (
            config.setting['move_files_to'] or
            os.path.normpath(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.DocumentsLocation))
            )
        default_extension = 'txt'
        default_filename = f"{make_filename(self.base_name).strip() or 'Script_Variables'}.{default_extension}"
        default_path = os.path.normpath(os.path.join(default_directory, default_filename))

        filename, _file_type = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption='',
            directory=default_path,
            filter='Text Files (*.txt);;All Files (*)',
            initialFilter='All Files (*)',
        )
        if not filename:
            return ''

        # Fix issue where Qt may set the extension twice
        (name, ext) = os.path.splitext(filename)
        if ext and str(name).endswith('.' + ext):
            filename = name

        return normpath(filename)


sv = SaveVariables()
register_file_action(sv)
register_track_action(sv)
