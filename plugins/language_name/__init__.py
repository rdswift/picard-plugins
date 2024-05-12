# -*- coding: utf-8 -*-
#
# Copyright (C) 2019, 2024 Bob Swift (rdswift)
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

############################################################################
#                                                                          #
#  ISO 639-3 codes: https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes  #
#                                                                          #
#  Translation contributors to this plugin:                                #
#     - hiccup: Dutch                                                      #
#                                                                          #
############################################################################

# pylint: disable=missing-module-docstring
# pylint: disable=line-too-long
# pylint: disable=import-error
# pyright: reportMissingImports=false
# pyright: reportUndefinedVariable=false


from importlib import import_module

from picard import (
    config,
    log,
)
from picard.const import UI_LANGUAGES
from picard.script import register_script_function
from picard.ui.options import (
    OptionsPage,
    register_options_page,
)

from .ui_options_language_name import Ui_LanguageNameOptionsPage


PLUGIN_NAME = 'Language Name'
PLUGIN_AUTHOR = 'Bob Swift (rdswift)'
PLUGIN_DESCRIPTION = '''
This plugin provides a new script function `$language_name()` to replace the
three-character language code with the full name of the language.

By default, the language used for the return values will be based on the
user's interface language set in the Picard options.  This can be overridden
in the 'Plugins'->'Language Name' section of Picard's options settings.

Languages currently supported are English, French, German, Spanish, Dutch,
Russian and Chinese.  Note that some translations may be incorrect or incomplete.
Any help correcting / completing the current translations or translation to other
languages would be appreciated.  English is the language used for all user
interface languages not currently supported.
'''

PLUGIN_VERSION = '0.5'
PLUGIN_API_VERSIONS = ['2.0', '2.11']
PLUGIN_LICENSE = 'GPL-2.0-or-later'
PLUGIN_LICENSE_URL = 'https://www.gnu.org/licenses/gpl-2.0.html'

PLUGIN_USER_GUIDE_URL = 'https://github.com/rdswift/picard-plugins/blob/2.0_RDS_Plugins/plugins/language_name/docs/README.md'

SUPPORTED_LANGUAGES = ['en', 'fr', 'de', 'es', 'nl', 'ru', 'zh']


def language_name(_parser, text: str) -> str:
    """Return the full language name for the supplied language code.

    Args:
        _parser (ScriptParser): Script parser used by the tagger
        text (str): Language code

    Returns:
        str: Full name of the language
    """
    text = text.strip().lower()
    if text:
        return LanguageList.get_language(text)
    return 'missing'


################################################################################
#                                                                              #
#  Use a new class to hold language names to allow configuration settings to   #
#  be loaded before selecting the language file to load.  The selected output  #
#  language is checked with each language name lookup, and the language file   #
#  is only loaded / reloaded if the selected output language has changed.      #
#  This allows changing the selection without having to restart Picard.        #
#                                                                              #
################################################################################

class LanguageList():
    """Provides the language names for ISO 639-3 codes."""
    # pylint: disable=too-few-public-methods

    RETURN_LANGUAGE = ''
    LANGUAGE_LIST = {}

    def __init__(self):
        pass

    @classmethod
    def get_language(cls, text: str) -> str:
        """Return the full language name from the configured language list for
        the supplied three-character language code.

        Args:
            text (str): Language code

        Returns:
            str: Full name of the language
        """
        user_lang = config.setting['ui_language'][:2]
        user_lang = user_lang if (user_lang in SUPPORTED_LANGUAGES) else 'en'
        new_lang = config.setting['language_name_language'] \
            if config.setting['language_name_override'] and config.setting['language_name_language'] in SUPPORTED_LANGUAGES \
            else user_lang

        if new_lang != cls.RETURN_LANGUAGE:
            log.debug(f"{PLUGIN_NAME}: Selected language changed from '{cls.RETURN_LANGUAGE}' to '{new_lang}'")
            cls.RETURN_LANGUAGE = new_lang
            cls.LANGUAGE_LIST = dict(import_module(f'{cls.__module__}.languages_{new_lang}').LANGUAGE_LIST)
            log.debug(f"{PLUGIN_NAME}: Loaded language list for '{new_lang}'")
        return cls.LANGUAGE_LIST[text] if text in cls.LANGUAGE_LIST and cls.LANGUAGE_LIST[text] else 'unknown'


class LanguageNameOptionsPage(OptionsPage):
    """Option settings page for the Language Name plugin."""

    NAME = 'language_name'
    TITLE = 'Language Name'
    PARENT = 'plugins'

    options = [
        config.BoolOption('setting', 'language_name_override', False),
        config.TextOption('setting', 'language_name_language', 'en'),
    ]

    def __init__(self, parent=None):
        # pylint: disable=undefined-variable
        super().__init__(parent)
        self.ui = Ui_LanguageNameOptionsPage()
        self.ui.setupUi(self)

        temp = {}
        for lang_code, native, translation in [(lang[0], lang[1], _(lang[2])) for lang in UI_LANGUAGES]:
            if native and native != translation:
                name = f'{translation} ({native})'
            else:
                name = translation
            lang_code = lang_code[:2]
            if lang_code in SUPPORTED_LANGUAGES and lang_code not in temp:
                temp[lang_code] = name
        for lang_code in sorted(temp):
            self.ui.language_name_language.addItem(temp[lang_code], lang_code)

    def load(self):
        """Load the configuration settings."""
        self.ui.language_name_override.setChecked(config.setting['language_name_override'])
        current_language = config.setting['language_name_language'] if (config.setting['language_name_language'] in SUPPORTED_LANGUAGES) else 'en'
        self.ui.language_name_language.setCurrentIndex(self.ui.language_name_language.findData(current_language))

    def save(self):
        """Save the configuration settings."""
        config.setting['language_name_override'] = self.ui.language_name_override.isChecked()
        config.setting['language_name_language'] = self.ui.language_name_language.itemData(self.ui.language_name_language.currentIndex())


register_script_function(language_name)
register_options_page(LanguageNameOptionsPage)
