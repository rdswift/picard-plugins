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


from picard import log
from picard.metadata import register_track_metadata_processor


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


def metadata_error(album_id, metadata_element, track_number):
    log.error(f"{PLUGIN_NAME}: {album_id}: Missing '{metadata_element}' in track {track_number} metadata.")


def combine_performer_tags(album, album_metadata, track_metadata, release_metadata):     # pylint: disable=unused-argument
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

    for relation in track_metadata['recording']['relations']:
        if (
            'artist' not in relation or not relation['artist']
            or 'type' not in relation or relation['type'] not in ('instrument', 'vocal')
            or 'attributes' not in relation or not relation['attributes']
        ):
            continue

        performer = relation['artist']['name']
        instrument = relation['attributes'][0]

        # Get as credited name for the instrument or vocal
        if 'attribute-credits' in relation and instrument in relation['attribute-credits']:
            instrument = relation['attribute-credits'][instrument]

        # Add any additional attributes such as 'guest' or 'solo'
        for attr in relation['attributes'][1:]:
            instrument = f"{attr} {instrument}"

        if performer not in performers:
            performers[performer] = set()

        performers[performer].add(instrument)

    for performer, instruments in performers.items():
        if not instruments:
            instruments = {'not specified'}
        performers_tag.append(f"{performer} ({', '.join(instruments)})")
    album_metadata['~performers'] = performers_tag


# Register the plugin
register_track_metadata_processor(combine_performer_tags)
