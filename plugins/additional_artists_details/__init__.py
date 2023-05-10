# -*- coding: utf-8 -*-
"""Additional Artists Details
"""
# Copyright (C) 2023 Bob Swift (rdswift)
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

# pylint: disable=line-too-long
# pylint: disable=import-error
# pylint: disable=too-many-arguments

from collections import namedtuple
from functools import partial

from picard import log
from picard.metadata import (
    register_album_metadata_processor,
    register_track_metadata_processor,
)
from picard.plugin import PluginPriority
from picard.webservice.api_helpers import MBAPIHelper


PLUGIN_NAME = 'Additional Artists Details'
PLUGIN_AUTHOR = 'Bob Swift (rdswift)'
PLUGIN_DESCRIPTION = '''
This plugin provides specialized album and track variables with artist details for use in tagging and naming scripts.  Note that this creates
additional calls to the MusicBrainz API for the artist and area information, and this will slow down processing.  This will be particularly
noticable when there are many different album or track artists, such as on a [Various Artists] release.
<br /><br />
Please see the <a href="https://github.com/rdswift/picard-plugins/blob/2.0_RDS_Plugins/plugins/additional_artists_details/docs/README.md">user
guide</a> on GitHub for more information.
'''
PLUGIN_VERSION = '0.1'
PLUGIN_API_VERSIONS = ['2.0', '2.1', '2.2', '2.7', '2.8']
PLUGIN_LICENSE = 'GPL-2.0-or-later'
PLUGIN_LICENSE_URL = 'https://www.gnu.org/licenses/gpl-2.0.html'

PLUGIN_USER_GUIDE_URL = 'https://github.com/rdswift/picard-plugins/blob/2.0_RDS_Plugins/plugins/additional_artists_details/docs/README.md'

# Named tuples for code clarity
Area = namedtuple('Area', ['parent', 'name', 'country', 'type'])
MetadataPair = namedtuple('MetadataPair', ['source', 'target'])

# MusicBrainz ID codes for relationship and entity types
COUNTRY_TYPE_ID = '06dd0ae4-8c74-30bb-b43d-95dcedf961de'
PART_OF_TYPE_ID = 'de7cc874-8b1b-3a05-8272-f3834c968fb7'
MUNICIPALITY_TYPE_ID = '17246454-5ac4-36a1-b81a-4753eb2dab20'

# Area types to exclude from the location string
EXCLUDE_AREA_TYPES = {MUNICIPALITY_TYPE_ID}

# Standard text for arguments
ARTIST = 'artist'
ARTIST_REQUESTS = 'artist_requests'
AREA = 'area'
AREA_REQUESTS = 'area_requests'
ISO_CODES = 'iso-3166-1-codes'


def log_helper(text, *args):
    """Logging helper to prepend the plugin name to the text.

    Args:
        text (str): Text to log.

    Returns:
        tuple: updated text and replacement arguments
    """
    return "%s: " + text, PLUGIN_NAME, *args


class CustomHelper(MBAPIHelper):
    """Custom MusicBrainz API helper to retrieve artist and area information.
    """

    def get_artist_by_id(self, _id, handler, inc=None, priority=False, important=False,
                         mblogin=False, refresh=False):
        """Get information for the specified artist MBID.

        Args:
            _id (str): Artist MBID to retrieve.
            handler (object): Callback used to process the returned information.
            inc (list, optional): List of includes to add to the API call. Defaults to None.
            priority (bool, optional): Process the request at a high priority. Defaults to False.
            important (bool, optional): Identify the request as important. Defaults to False.
            mblogin (bool, optional): Request requires logging into MusicBrainz. Defaults to False.
            refresh (bool, optional): Request triggers a refresh. Defaults to False.

        Returns:
            RequestTask: Requested task object
        """
        return self._get_by_id(ARTIST, _id, handler, inc, priority=priority, important=important, mblogin=mblogin, refresh=refresh)

    def get_area_by_id(self, _id, handler, inc=None, priority=False, important=False, mblogin=False, refresh=False):
        """Get information for the specified area MBID.

        Args:
            _id (str): Area MBID to retrieve.
            handler (object): Callback used to process the returned information.
            inc (list, optional): List of includes to add to the API call. Defaults to None.
            priority (bool, optional): Process the request at a high priority. Defaults to False.
            important (bool, optional): Identify the request as important. Defaults to False.
            mblogin (bool, optional): Request requires logging into MusicBrainz. Defaults to False.
            refresh (bool, optional): Request triggers a refresh. Defaults to False.

        Returns:
            RequestTask: Requested task object
        """
        if inc is None:
            inc = ['area-rels']
        return self._get_by_id(AREA, _id, handler, inc, priority=priority, important=important, mblogin=mblogin, refresh=refresh)


class ArtistDetailsPlugin:
    """Plugin to retrieve artist details, including area and country information.
    """
    result_cache = {
        ARTIST: {},
        ARTIST_REQUESTS: set(),
        AREA: {},
        AREA_REQUESTS: set(),
    }
    processing_count = 0
    ALBUMS = {}

    def _add_target(self, album_id, source_metadata, target_metadata):
        if album_id not in self.ALBUMS:
            self.ALBUMS[album_id] = []
        self.ALBUMS[album_id].append(MetadataPair(source_metadata, target_metadata))

    def _remove_album(self, album_id):
        log.debug(*log_helper("Removing album '%s'", album_id))
        self.ALBUMS.pop(album_id, None)

    def _album_add_request(self, album):
        self.processing_count += 1
        album._requests += 1

    def _album_remove_request(self, album):
        self.processing_count -= 1
        album._requests -= 1
        album._finalize_loading(None)   # pylint: disable=protected-access

    def make_album_vars(self, album, album_metadata, release_metadata):
        """Process album artists.
        """
        album_id = release_metadata['id'] if release_metadata else 'No Album ID'
        self._process_artists(album, album_id, release_metadata, album_metadata, 'album')

    def make_track_vars(self, album, album_metadata, track_metadata, release_metadata):
        """Process track artists.
        """
        album_id = release_metadata['id'] if release_metadata else 'No Album ID'
        self._process_artists(album, album_id, track_metadata, album_metadata, 'track')

    def _process_artists(self, album, album_id, source_metadata, destination_metadata, source_type):
        """Extracts a list of artists to process from the source metadata, and retrieves the
        information for artists not already processed.

        Args:
            album (album): The source album object
            album_id (str): MBID of the album
            source_metadata (metadata): Source metadata to check for artists
            destination_metadata (metadata): Metadata to update with new variables
            source_type (str): Source type (album or track) for error messages
        """
        # Test for valid metadata node.
        # The 'artist-credit' key should always be there.
        # This check is to avoid a runtime error if it doesn't exist for some reason.
        if 'artist-credit' in source_metadata:
            for artist_credit in source_metadata['artist-credit']:
                if 'artist' in artist_credit:
                    if 'id' in artist_credit['artist']:
                        temp_id = artist_credit['artist']['id']
                        if temp_id not in self.result_cache[ARTIST_REQUESTS]:
                            self.result_cache[ARTIST_REQUESTS].add(temp_id)
                            log.debug(*log_helper('Retrieving artist ID %s information from MusicBrainz.', temp_id))
                            self._get_artist_info(temp_id, album, album_id, source_metadata, destination_metadata, source_type)
                        else:
                            log.debug(*log_helper('Artist ID %s information retrieved from cache.', temp_id))
                else:
                    # No 'artist' specified.  Log as an error.
                    self._metadata_error(album_id, 'artist-credit.artist', source_type)
        else:
            # No valid metadata found.  Log as error.
            self._metadata_error(album_id, 'artist-credit', source_type)
        self._add_target(album_id, source_metadata, destination_metadata)
        self._save_artist_metadata(album_id, source_type)

    def _save_artist_metadata(self, album_id, source_type):
        """Extracts a list of artists to process from the source metadata, and retrieves the
        information for artists not already processed.

        Args:
            album (album): The source album object
            album_id (str): MBID of the album
            source_metadata (metadata): Source metadata to check for artists
            destination_metadata (metadata): Metadata to update with new variables
            source_type (str): Source type (album or track) for error messages
        """
        if self.processing_count:
            return
        if album_id not in self.ALBUMS or not self.ALBUMS[album_id]:
            log.error(*log_helper("No metadata targets found for album '%s'", album_id))
            return
        for item in self.ALBUMS[album_id]:
            source_metadata = item.source
            destination_metadata = item.target
            # Test for valid metadata node.
            # The 'artist-credit' key should always be there.
            # This check is to avoid a runtime error if it doesn't exist for some reason.
            if 'artist-credit' not in source_metadata:
                # No valid metadata found.  Log as error.
                self._metadata_error(album_id, 'artist-credit', source_type)
                continue
            for artist_credit in source_metadata['artist-credit']:
                if 'artist' not in artist_credit:
                    # No 'artist' specified.  Log as an error.
                    self._metadata_error(album_id, 'artist-credit.artist', source_type)
                    continue
                if 'id' not in artist_credit['artist']:
                    continue
                temp_id = artist_credit['artist']['id']
                if temp_id in self.result_cache[ARTIST]:
                    self._set_artist_metadata(destination_metadata, temp_id, self.result_cache[ARTIST][temp_id])

    def _set_artist_metadata(self, destination_metadata, artist_id, artist_info):
        """Adds the artist information to the destination metadata.

        Args:
            destination_metadata (metadata): Metadata object to update
            artist_id (str): MBID of the artist
            artist_info (dict): Dictionary of information for the artist
        """
        def _set_item(key, value):
            destination_metadata[f"~artist_{artist_id}_{key.replace('-', '_')}"] = value

        for item in artist_info.keys():
            if item in {'area', 'begin-area', 'end-area'}:
                country, location = self._drill_area(artist_info[item])
                if country:
                    _set_item(item.replace('area', 'country'), country)
                if location:
                    _set_item(item.replace('area', 'location'), location)
            else:
                _set_item(item, artist_info[item])

    def _get_artist_info(self, artist_id, album, album_id, source_metadata, destination_metadata, source_type):
        """Gets the artist information from the MusicBrainz website.

        Args:
            artist_id (str): MBID of the artist
            webservice (webservice): The Picard webservice to use for the request
            destination_metadata (metadata): Metadata object to update
        """
        self._album_add_request(album)
        helper = CustomHelper(album.tagger.webservice)
        handler = partial(
            self._artist_submission_handler,
            album_id=album_id,
            source_metadata=source_metadata,
            destination_metadata=destination_metadata,
            artist=artist_id,
            album=album,
            source_type=source_type,
            )
        return helper.get_artist_by_id(artist_id, handler)

    def _artist_submission_handler(self, document, _reply, error, source_metadata=None, destination_metadata=None,
                                   artist=None, album=None, album_id=None, source_type=None):
        """Handles the response from the webservice requests for artist information.
        """
        try:
            if error:
                log.error(*log_helper("Artist '%s' information retrieval error.", artist))
                return
            artist_info = {}
            for item in ['type', 'gender', 'name', 'sort-name', 'disambiguation']:
                if item in document and document[item]:
                    artist_info[item] = document[item]
            if 'life-span' in document:
                for item in ['begin', 'end']:
                    if item in document['life-span'] and document['life-span'][item]:
                        artist_info[item] = document['life-span'][item]
            for item in ['area', 'begin-area', 'end-area']:
                if item in document and document[item] and 'id' in document[item] and document[item]['id']:
                    area_id = document[item]['id']
                    artist_info[item] = area_id
                    if area_id not in self.result_cache[AREA_REQUESTS]:
                        self._get_area_info(area_id, album, album_id, source_metadata, destination_metadata, source_type)
            self.result_cache[ARTIST][artist] = artist_info
            log.debug(*log_helper("Completed artist '%s' information retrieval.", artist))
        finally:
            self._album_remove_request(album)
            self._save_artist_metadata(album_id, source_type)

    def _get_area_info(self, area_id, album, album_id, source_metadata, destination_metadata, source_type):
        """Gets the area information from the MusicBrainz website.
        """
        self.result_cache[AREA_REQUESTS].add(area_id)
        self._album_add_request(album)
        log.debug(*log_helper('Retrieving area ID %s from MusicBrainz.', area_id))
        helper = CustomHelper(album.tagger.webservice)
        handler = partial(
            self._area_submission_handler,
            area=area_id,
            album=album,
            album_id=album_id,
            source_metadata=source_metadata,
            destination_metadata=destination_metadata,
            source_type=source_type,
            )
        return helper.get_area_by_id(area_id, handler)

    def _area_submission_handler(self, document, _reply, error, area=None, album=None, album_id=None,
                                 source_metadata=None, destination_metadata=None, source_type=None):
        try:
            if error:
                log.error(*log_helper("Area '%s' information retrieval error.", area))
                return
            (_id, name, country, _type) = self._parse_area(document)
            if _type == COUNTRY_TYPE_ID:
                if _id not in self.result_cache[AREA]:
                    log.error(*log_helper("Adding area as country: %s => %s (%s)", _id, name, country))
                    self.result_cache[AREA][_id] = Area('', name, country, _type)
            if 'relations' in document:
                for rel in document['relations']:
                    self._parse_area_relation(_id, rel, album, name, _type, album_id, source_metadata,
                                              destination_metadata, source_type)
            log.debug(*log_helper("Completed area '%s' information retrieval.", area))
        finally:
            self._album_remove_request(album)
            self._save_artist_metadata(album_id, source_type)

    def _parse_area_relation(self, area_id, area_relation, album, area_name, area_type, album_id,
                             source_metadata, destination_metadata, source_type):
        if 'type-id' not in area_relation or 'area' not in area_relation or area_relation['type-id'] != PART_OF_TYPE_ID:
            return
        (_id, name, country, _type) = self._parse_area(area_relation['area'])
        if not _id:
            return

        def _area_logger(area_id, area_name, area_type):
            log.debug(*log_helper("Adding area: %s => %s as %s", area_id, area_name, area_type))

        if 'direction' in area_relation and area_relation['direction'] == 'backward':
            if area_id not in self.result_cache[AREA]:
                _area_logger(area_id, area_name, area_type)
                self.result_cache[AREA][area_id] = Area(_id, area_name, '', area_type)
                self.result_cache[AREA_REQUESTS].add(area_id)
            if _type == COUNTRY_TYPE_ID:
                if _id not in self.result_cache[AREA]:
                    _area_logger(_id, f"{name} ({country})", _type)
                    self.result_cache[AREA][_id] = Area('', name, country, _type)
                    self.result_cache[AREA_REQUESTS].add(_id)
            else:
                if _id not in self.result_cache[AREA] and _id not in self.result_cache[AREA_REQUESTS]:
                    # _area_logger(_id, name, _type)
                    self._get_area_info(_id, album, album_id, source_metadata, destination_metadata, source_type)
        else:
            _area_logger(_id, name, _type)
            self.result_cache[AREA_REQUESTS].add(_id)
            self.result_cache[AREA][_id] = Area(area_id, name, '', _type)

    @staticmethod
    def _parse_area(area_info):
        if 'id' not in area_info:
            return ('', '', '', '')
        area_id = area_info['id']
        area_name = area_info['name'] if 'name' in area_info else 'Unknown Name'
        area_type = area_info['type-id'] if 'type-id' in area_info else ''
        if area_type == COUNTRY_TYPE_ID:
            country = area_info[ISO_CODES][0] if ISO_CODES in area_info and area_info[ISO_CODES] else ''
        else:
            country = ''
        return (area_id, area_name, country, area_type)

    @staticmethod
    def _metadata_error(album_id, metadata_element, metadata_group):
        """Logs metadata-related errors.

        Args:
            album_id (str): MBID of the album
            metadata_element (str): Metadata element
            metadata_group (str): Metadata group
        """
        log.error(*log_helper("Album '%s' missing '%s' in %s metadata.", album_id, metadata_element, metadata_group))

    def _drill_area(self, area_id):
        country = ''
        location = []
        i = 5   # Counter to avoid potential runaway processing
        while i and area_id and not country:
            i -= 1
            area = self.result_cache[AREA][area_id] if area_id in self.result_cache[AREA] else Area('', '', '', '')
            country = area.country
            area_id = area.parent
            if not location or area.type not in EXCLUDE_AREA_TYPES:
                location.append(area.name)
        return country, ', '.join(location)


plugin = ArtistDetailsPlugin()

# Register the plugin to run at a LOW priority so that other plugins that
# modify the artist information can complete their processing and this plugin
# is working with the latest updated data.
register_album_metadata_processor(plugin.make_album_vars, priority=PluginPriority.LOW)
register_track_metadata_processor(plugin.make_track_vars, priority=PluginPriority.LOW)
