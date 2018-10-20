# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Bob Swift (rdswift)
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

PLUGIN_NAME = 'Performer Tag Replace'
PLUGIN_AUTHOR = 'Bob Swift (rdswift)'
PLUGIN_DESCRIPTION = '''
This plugin provides the ability to replace text in performer tags.  It
has been developed using the 'Standardise Performers' plugin by Sophist
as the basis for retrieving and processing the performer data for each
of the tracks.  The original/replacement pairs used can be customized
in the option settings page.
'''

PLUGIN_VERSION = "0.01"
PLUGIN_API_VERSIONS = ["2.0"]
PLUGIN_LICENSE = "GPL-2.0 or later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-2.0.html"

DEV_TESTING = False

import re
from picard import config, log
from picard.metadata import register_track_metadata_processor
from picard.plugin import PluginPriority
from picard.ui.options import register_options_page, OptionsPage
from picard.plugins.performer_tag_replace.ui_options_performer_tag_replace import Ui_PerformerTagReplaceOptionsPage

pairs_split = re.compile(r"\r\n|\n\r|\n").split

def performer_tag_replace(album, metadata, *args):
    replacements = []
    for pair in pairs_split(config.setting["performer_tag_replacement_pairs"]):
        if "=" not in pair:
            continue
        original, replacement = pair.split('=', 1)
        if original:
            replacements.append((original, replacement))
            if DEV_TESTING:
                log.debug("%s: Add pair: '%s' = '%s'", PLUGIN_NAME, original, replacement,)
    if replacements:
        for key, values in list(metadata.rawitems()):
            if not key.startswith('performer:') and not key.startswith('~performersort:'):
                continue
            mainkey, subkey = key.split(':', 1)
            if not subkey:
                continue
            log.debug("%s: Original key: '%s'", PLUGIN_NAME, subkey,)
            for (original, replacement) in replacements:
                subkey = subkey.replace(original, replacement)
                if DEV_TESTING:
                    log.debug("%s: Applying pair: '%s' = '%s'", PLUGIN_NAME, original, replacement,)
                    log.debug("%s: Updated key: '%s'", PLUGIN_NAME, subkey,)
            log.debug("%s: Replacement key: '%s'", PLUGIN_NAME, subkey,)
            del metadata[key]
            newkey = ('%s:%s' % (mainkey, subkey,)).strip()
            for value in values:
                if config.setting["performer_tag_replace_performers"]:
                    log.debug("%s: Original value: '%s'", PLUGIN_NAME, subkey,)
                    for (original, replacement) in replacements:
                        value = value.replace(original, replacement)
                        if DEV_TESTING:
                            log.debug("%s: Applying pair: '%s' = '%s'", PLUGIN_NAME, original, replacement,)
                            log.debug("%s: Updated value: '%s'", PLUGIN_NAME, value,)
                    log.debug("%s: Replacement value: '%s'", PLUGIN_NAME, value,)
                metadata.add_unique(newkey, value)
    else:
        log.debug("%s: No replacement pairs found.", PLUGIN_NAME,)


class PerformerTagReplaceOptionsPage(OptionsPage):

    NAME = "performer_tag_replace"
    TITLE = "Performer Tag Replacement"
    PARENT = "plugins"

    options = [
        config.TextOption("setting", "performer_tag_replacement_pairs", ''),
        config.BoolOption("setting", "performer_tag_replace_performers", False),
    ]

    def __init__(self, parent=None):
        super(PerformerTagReplaceOptionsPage, self).__init__(parent)
        self.ui = Ui_PerformerTagReplaceOptionsPage()
        self.ui.setupUi(self)

    def load(self):
        # Enable external link
        self.ui.format_description.setOpenExternalLinks(True)

        # Replacement settings
        self.ui.performer_tag_replacement_pairs.setPlainText(config.setting["performer_tag_replacement_pairs"])
        self.ui.performer_tag_replace_performers.setChecked(config.setting["performer_tag_replace_performers"])

    def save(self):
        # Replacement settings
        config.setting["performer_tag_replacement_pairs"] = self.ui.performer_tag_replacement_pairs.toPlainText()
        config.setting["performer_tag_replace_performers"] = self.ui.performer_tag_replace_performers.isChecked()


# Register the plugin to run at a LOW priority.
register_track_metadata_processor(performer_tag_replace, priority=PluginPriority.LOW)
register_options_page(PerformerTagReplaceOptionsPage)
