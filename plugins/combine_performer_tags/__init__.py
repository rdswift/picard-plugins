# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Bob Swift (rdswift)
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

# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=too-many-boolean-expressions
# pylint: disable=import-error


from picard import (
    config,
    log,
)
from picard.metadata import register_track_metadata_processor
from picard.plugins.combine_performer_tags.ui_options_combine_performer_tags import (
    Ui_CombinePerformerTagsOptionsPage,
)
from picard.ui.options import (
    OptionsPage,
    register_options_page,
)


PLUGIN_NAME = 'Combine Performer Tags'
PLUGIN_AUTHOR = 'Bob Swift'
PLUGIN_DESCRIPTION = '''
This plugin combines all performer tags into a multi-value variable `%_performers%`.
'''

PLUGIN_VERSION = "0.2"
PLUGIN_API_VERSIONS = ['2.0', '2.1', '2.2', '2.7', '2.9', '2.10', '2.11']
PLUGIN_LICENSE = "GPL-2.0-or-later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-2.0.html"

PLUGIN_USER_GUIDE_URL = "https://github.com/rdswift/picard-plugins/blob/2.0_RDS_Plugins/plugins/combine_performer_tags/docs/README.md"

OPT_USE_TRACK_RELS = 'track_ars'

OPT_CREDITED_ARTIST = 'cpt_cred_artist'
OPT_CREDITED_INSTRUMENT = 'cpt_cred_instrument'
OPT_CREDITED_VOCAL = 'cpt_cred_vocal'

OPT_INSTRUMENT_ATTR_ADDITIONAL = 'cpt_inst_attr_additional'
OPT_INSTRUMENT_ATTR_GUEST = 'cpt_inst_attr_guest'
OPT_INSTRUMENT_ATTR_SOLO = 'cpt_inst_attr_solo'

OPT_VOCAL_ATTR_ADDITIONAL = 'cpt_vocal_attr_additional'
OPT_VOCAL_ATTR_GUEST = 'cpt_vocal_attr_guest'
OPT_VOCAL_ATTR_SOLO = 'cpt_vocal_attr_solo'


class PerformerTags():
    """Collection of instruments and vocals for a performer.
    """
    def __init__(self) -> None:
        self.instruments = set()
        self.vocals = set()

    def combine(self) -> list:
        combined = list(sorted(self.instruments))
        combined.extend(sorted(self.vocals))
        return combined


def metadata_error(album_id, metadata_element, track_number):
    log.error(f"{PLUGIN_NAME}: {album_id}: Missing '{metadata_element}' in track {track_number} metadata.")


def combine_performer_tags(album, album_metadata, track_metadata, release_metadata):
    # pylint: disable=unused-argument
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches

    if not config.setting[OPT_USE_TRACK_RELS]:
        log.error(f"{PLUGIN_NAME}: Use track relationships is not enabled in Options -> Metadata.")
        return

    album_id = release_metadata['id'] if release_metadata else 'No Album ID'
    track_number = track_metadata['number'] if track_metadata and 'number' in track_metadata else 'No Track Number'

    if 'recording' not in track_metadata:
        metadata_error(album_id, 'recording', track_number)
        return

    if 'relations' not in track_metadata['recording']:
        metadata_error(album_id, 'recording->relations', track_number)
        return

    performers = {}
    performers_tag = []

    cred_artist = config.setting[OPT_CREDITED_ARTIST]
    cred_instrument = config.setting[OPT_CREDITED_INSTRUMENT]
    cred_vocal = config.setting[OPT_CREDITED_VOCAL]

    inst_attr_additional = config.setting[OPT_INSTRUMENT_ATTR_ADDITIONAL]
    inst_attr_guest = config.setting[OPT_INSTRUMENT_ATTR_GUEST]
    inst_attr_solo = config.setting[OPT_INSTRUMENT_ATTR_SOLO]

    vocal_attr_additional = config.setting[OPT_VOCAL_ATTR_ADDITIONAL]
    vocal_attr_guest = config.setting[OPT_VOCAL_ATTR_GUEST]
    vocal_attr_solo = config.setting[OPT_VOCAL_ATTR_SOLO]

    for relation in track_metadata['recording']['relations']:
        if (
            'artist' not in relation or not relation['artist']
            or 'type' not in relation or relation['type'] not in ('instrument', 'vocal')
            or 'attributes' not in relation or not relation['attributes']
        ):
            continue

        performer = relation['target-credit'] if cred_artist and relation['target-credit'] else relation['artist']['name']
        instrument = relation['attributes'][0]

        # Get as credited name for the instrument or vocal
        if (
            'attribute-credits' in relation and instrument in relation['attribute-credits']
            and (
                    (relation['type'] == 'instrument' and cred_instrument)
                    or
                    (relation['type'] == 'vocal' and cred_vocal)
                )
        ):
            instrument = relation['attribute-credits'][instrument]

        # Add any additional attributes such as 'guest' or 'solo'
        for attr in relation['attributes'][1:]:
            if (
                attr == 'additional' and (
                    (relation['type'] == 'instrument' and not inst_attr_additional)
                    or
                    (relation['type'] == 'vocal' and not vocal_attr_additional)
                )
            ):
                continue

            if (
                attr == 'guest' and (
                    (relation['type'] == 'instrument' and not inst_attr_guest)
                    or
                    (relation['type'] == 'vocal' and not vocal_attr_guest)
                )
            ):
                continue

            if (
                attr == 'solo' and (
                    (relation['type'] == 'instrument' and not inst_attr_solo)
                    or
                    (relation['type'] == 'vocal' and not vocal_attr_solo)
                )
            ):
                continue

            instrument = f"{attr} {instrument}"

        if performer not in performers:
            performers[performer] = PerformerTags()

        if relation['type'] == 'instrument':
            performers[performer].instruments.add(instrument)
        elif relation['type'] == 'vocal':
            performers[performer].vocals.add(instrument)

    for performer, tags in performers.items():
        instruments = tags.combine()
        if not instruments:
            instruments = ['not specified']
        performers_tag.append(f"{performer} ({', '.join(instruments)})")
    album_metadata['~performers'] = performers_tag


class CombinePerformerTagsOptionsPage(OptionsPage):
    """Options page for the Combine Performer Tags plugin.
    """

    NAME = "combine_performer_tags"
    TITLE = "Combine Performer Tags"
    PARENT = "plugins"

    options = [
        config.BoolOption('setting', OPT_CREDITED_ARTIST, True),
        config.BoolOption('setting', OPT_CREDITED_INSTRUMENT, True),
        config.BoolOption('setting', OPT_CREDITED_VOCAL, True),
        config.BoolOption('setting', OPT_INSTRUMENT_ATTR_ADDITIONAL, True),
        config.BoolOption('setting', OPT_INSTRUMENT_ATTR_GUEST, True),
        config.BoolOption('setting', OPT_INSTRUMENT_ATTR_SOLO, True),
        config.BoolOption('setting', OPT_VOCAL_ATTR_ADDITIONAL, True),
        config.BoolOption('setting', OPT_VOCAL_ATTR_GUEST, True),
        config.BoolOption('setting', OPT_VOCAL_ATTR_SOLO, True),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_CombinePerformerTagsOptionsPage()
        self.ui.setupUi(self)

        # Enable external link
        self.ui.format_description.setOpenExternalLinks(True)

    def load(self):
        """Load the option settings.
        """
        self.ui.cb_credited_artists.setChecked(config.setting[OPT_CREDITED_ARTIST])
        self.ui.cb_credited_instruments.setChecked(config.setting[OPT_CREDITED_INSTRUMENT])
        self.ui.cb_credited_vocals.setChecked(config.setting[OPT_CREDITED_VOCAL])
        self.ui.cb_additional_instruments.setChecked(config.setting[OPT_INSTRUMENT_ATTR_ADDITIONAL])
        self.ui.cb_guest_instruments.setChecked(config.setting[OPT_INSTRUMENT_ATTR_GUEST])
        self.ui.cb_solo_instruments.setChecked(config.setting[OPT_INSTRUMENT_ATTR_SOLO])
        self.ui.cb_additional_vocals.setChecked(config.setting[OPT_VOCAL_ATTR_ADDITIONAL])
        self.ui.cb_guest_vocals.setChecked(config.setting[OPT_VOCAL_ATTR_GUEST])
        self.ui.cb_solo_vocals.setChecked(config.setting[OPT_VOCAL_ATTR_SOLO])

    def save(self):
        """Save the option settings.
        """
        config.setting[OPT_CREDITED_ARTIST] = self.ui.cb_credited_artists.isChecked()
        config.setting[OPT_CREDITED_INSTRUMENT] = self.ui.cb_credited_instruments.isChecked()
        config.setting[OPT_CREDITED_VOCAL] = self.ui.cb_credited_vocals.isChecked()
        config.setting[OPT_INSTRUMENT_ATTR_ADDITIONAL] = self.ui.cb_additional_instruments.isChecked()
        config.setting[OPT_INSTRUMENT_ATTR_GUEST] = self.ui.cb_guest_instruments.isChecked()
        config.setting[OPT_INSTRUMENT_ATTR_SOLO] = self.ui.cb_solo_instruments.isChecked()
        config.setting[OPT_VOCAL_ATTR_ADDITIONAL] = self.ui.cb_additional_vocals.isChecked()
        config.setting[OPT_VOCAL_ATTR_GUEST] = self.ui.cb_guest_vocals.isChecked()
        config.setting[OPT_VOCAL_ATTR_SOLO] = self.ui.cb_solo_vocals.isChecked()


# Register the plugin
register_track_metadata_processor(combine_performer_tags)
register_options_page(CombinePerformerTagsOptionsPage)
