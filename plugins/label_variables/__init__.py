# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Bob Swift (rdswift)
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

PLUGIN_NAME = 'Label Variables'
PLUGIN_AUTHOR = 'Bob Swift (rdswift)'
PLUGIN_DESCRIPTION = '''
This plugin provides variables containing label information for a
release for use in user or file naming scripts.
<br /><br />
Please see the <a href="https://github.com/rdswift/picard-plugins/blob/2.0_RDS_Plugins/plugins/label_variables/README.md">user
guide</a> on GitHub for more information.
'''
PLUGIN_VERSION = '0.1'
PLUGIN_API_VERSIONS = ['2.0', '2.1', '2.2', '2.3', '2.4']
PLUGIN_LICENSE = 'GPL-2.0-or-later'
PLUGIN_LICENSE_URL = 'https://www.gnu.org/licenses/gpl-2.0.html'

PLUGIN_USER_GUIDE_URL = 'https://github.com/rdswift/picard-plugins/blob/2.0_RDS_Plugins/plugins/label_variables/README.md'

from picard import log
from picard.metadata import register_album_metadata_processor
from picard.plugin import PluginPriority


def process_labels(album_id, source_metadata, destination_metadata):
    # Test for valid metadata node.
    # The 'label-info' key should always be there.
    # This check is to avoid a runtime error if it doesn't exist for some reason.
    if 'label-info' in source_metadata:
        # Initialize variables to default values
        label_id_list = []
        label_name_list = []
        label_sort_name_list = []
        label_disambig_list = []
        label_count = 0
        catalog_number_list = []
        catalog_number_count = 0
        for label_info in source_metadata['label-info']:
            if 'catalog-number' in label_info and label_info['catalog-number']:
                catalog_number_count += 1
                catalog_number_list.append(label_info['catalog-number'])
            if 'label' in label_info and label_info['label']:
                label_count += 1
                label_data = label_info['label']
                label_id_list.append(label_data['id'] if 'id' in label_data and label_data['id'] else 'Unknown-Label-ID')
                label_name_list.append(label_data['name'] if 'name' in label_data and label_data['name'] else 'Unknown Label Name')
                label_sort_name_list.append(label_data['sort-name'] if 'sort-name' in label_data and label_data['sort-name'] else 'Unknown Label Sort Name')
                label_disambig_list.append(label_data['disambiguation'] if 'disambiguation' in label_data else '')
        destination_metadata['~label_label_count'] = label_count
        destination_metadata['~label_catalog_count'] = catalog_number_count
        if label_id_list:
            destination_metadata['~label_ids_multi'] = label_id_list
        if label_name_list:
            destination_metadata['~label_names_multi'] = label_name_list
        if label_sort_name_list:
            destination_metadata['~label_sort_names_multi'] = label_sort_name_list
        if label_disambig_list:
            destination_metadata['~label_disambig_multi'] = label_disambig_list
        if catalog_number_list:
            destination_metadata['~label_catalog_multi'] = catalog_number_list
    else:
        # No valid metadata found.  Log as error.
        metadata_error(album_id, 'label-info')


def make_label_vars(album, album_metadata, release_metadata):
    album_id = release_metadata['id'] if release_metadata else 'No Album ID'
    process_labels(album_id, release_metadata, album_metadata)


def metadata_error(album_id, metadata_element):
    log.error("{0}: {1!r}: Missing '{2}' in release metadata.".format(PLUGIN_NAME, album_id, metadata_element,))


# Register the plugin to run at a LOW priority so that other plugins that
# modify the information can complete their processing and this plugin is
# working with the latest updated data.
register_album_metadata_processor(make_label_vars, priority=PluginPriority.LOW)
