# Additional Artists Variables \[[Download](https://github.com/rdswift/picard-plugins/raw/2.0_RDS_Plugins/plugins/additional_artists_variables/additional_artists_variables.zip)\]

## Overview

This plugin provides specialized album and track variables for use in naming scripts. It is based on the
"Album Artist Extension" plugin, but expands the functionality to also include track artists. Note that it
cannot be used as a direct drop-in replacement for the "Album Artist Extension" plugin because the variables
are provided with different names.  This will require changes to existing scripts if switching to this plugin.

---

## What it Does

This plugin reads the album and track metadata provided to Picard and exposes the information in a number
of additional variables for use in Picard scripts.  The plugin has been designed such that the information
is presented consistently regardless of whether or not the `Use standardized artist names` option is selected.
This means that some of the information available through the standard Picard tags will be duplicated in the
variables provided by this plugin.

***NOTE:*** This plugin makes no additional calls to the MusicBrainz website api for the information.

### Album Variables

* **_artists_album_primary_id** - The ID of the primary / first album artist listed
* **_artists_album_primary_std** - The primary / first album artist listed (standardized)
* **_artists_album_primary_cred** - The primary / first album artist listed (as credited)
* **_artists_album_primary_sort** - The primary / first album artist listed (sort name)
* **_artists_album_primary_legal** - The primary / first album artist listed (legal name)
* **_artists_album_primary_sort_legal** - The primary / first album artist listed (sort legal name)
* **_artists_album_primary_tags** - The primary / first album artist tags (limited to 'Maximum number of genres' setting in Picard configuration), as a multi-value
* **_artists_album_additional_id** - The IDs of all album artists listed except for the primary / first artist, as a multi-value
* **_artists_album_additional_std** - All album artists listed (standardized) except for the primary / first artist, separated by strings provided from the release entry
* **_artists_album_additional_cred** - All album artists listed (as credited) except for the primary / first artist, separated by strings provided from the release entry
* **_artists_album_additional_sort** - All album artists listed (sort names) except for the primary / first artist, separated by strings provided from the release entry
* **_artists_album_additional_legal** - All album artists listed (legal names) except for the primary / first artist, separated by strings provided from the release entry
* **_artists_album_additional_std_multi** - All album artists listed (standardized) except for the primary / first artist, as a multi-value
* **_artists_album_additional_cred_multi** - All album artists listed (as credited) except for the primary / first artist, as a multi-value
* **_artists_album_additional_sort_multi** - All album artists listed (sort names) except for the primary / first artist, as a multi-value
* **_artists_album_additional_legal_multi** - All album artists listed (legal names) except for the primary / first artist, as a multi-value
* **_artists_album_all_std** - All album artists listed (standardized), separated by strings provided from the release entry
* **_artists_album_all_cred** - All album artists listed (as credited), separated by strings provided from the release entry
* **_artists_album_all_sort** - All album artists listed (sort names), separated by strings provided from the release entry
* **_artists_album_all_legal** - All album artists listed (legal names), separated by strings provided from the release entry
* **_artists_album_all_std_multi** - All album artists listed (standardized), as a multi-value
* **_artists_album_all_cred_multi** - All album artists listed (as credited), as a multi-value
* **_artists_album_all_sort_multi** - All album artists listed (sort names), as a multi-value
* **_artists_album_all_legal_multi** - All album artists listed (legal names), as a multi-value
* **_artists_album_all_sort_primary** - The primary / first album artist listed (sort name) followed by all additional album artists (standardized), separated by strings provided from the release entry
* **_artists_album_all_types** - All album artist types, as a multi-value
* **_artists_album_all_join_phrases** - All album artist join phrases, as a multi-value
* **_artists_album_all_count** - The number of artists listed as album artists

### Track Variables

* **_artists_track_primary_id** - The ID of the primary / first track artist listed
* **_artists_track_primary_std** - The primary / first track artist listed (standardized)
* **_artists_track_primary_cred** - The primary / first track artist listed (as credited)
* **_artists_track_primary_sort** - The primary / first track artist listed (sort name)
* **_artists_track_primary_legal** - The primary / first track artist listed (legal name)
* **_artists_track_primary_sort_legal** - The primary / first track artist listed (sort legal name)
* **_artists_track_additional_id** - The IDs of all track artists listed except for the primary / first artist, as a multi-value
* **_artists_track_additional_std** - All track artists listed (standardized) except for the primary / first artist, separated by strings provided from the track entry
* **_artists_track_additional_cred** - All track artists listed (as credited) except for the primary / first artist, separated by strings provided from the track entry
* **_artists_track_additional_sort** - All track artists listed (sort names) except for the primary / first artist, separated by strings provided from the track entry
* **_artists_track_additional_legal** - All track artists listed (legal names) except for the primary / first artist, separated by strings provided from the track entry
* **_artists_track_additional_std_multi** - All track artists listed (standardized) except for the primary / first artist, as a multi-value
* **_artists_track_additional_cred_multi** - All track artists listed (as credited) except for the primary / first artist, as a multi-value
* **_artists_track_additional_sort_multi** - All track artists listed (sort names) except for the primary / first artist, as a multi-value
* **_artists_track_additional_legal_multi** - All track artists listed (legal names) except for the primary / first artist, as a multi-value
* **_artists_track_all_std** - All track artists listed (standardized), separated by strings provided from the track entry
* **_artists_track_all_cred** - All track artists listed (as credited), separated by strings provided from the track entry
* **_artists_track_all_sort** - All track artists listed (sort names), separated by strings provided from the track entry
* **_artists_track_all_legal** - All track artists listed (legal names), separated by strings provided from the track entry
* **_artists_track_all_std_multi** - All track artists listed (standardized), as a multi-value
* **_artists_track_all_cred_multi** - All track artists listed (as credited), as a multi-value
* **_artists_track_all_sort_multi** - All track artists listed (sort names), as a multi-value
* **_artists_track_all_legal_multi** - All track artists listed (legal names), as a multi-value
* **_artists_track_all_sort_primary** - The primary / first track artist listed (sort name) followed by all additional track artists (standardized), separated by strings provided from the track entry
* **_artists_track_all_types** - All track artist types, as a multi-value
* **_artists_track_all_join_phrases** - All track artist join phrases, as a multi-value
* **_artists_track_all_count** - The number of artists listed as track artists

***NOTE:*** If a legal name alias is not available for an artist, the standardized name will be used for **_artists_album_additional_legal**, **_artists_album_all_legal**, **_artists_track_additional_legal** and **_artists_track_all_legal**, 'n/a' will be used in **_artists_album_additional_legal_multi**, **_artists_album_all_legal_multi**, **_artists_track_additional_legal_multi** and **_artists_track_all_legal_multi**, and the variables **_artists_album_primary_legal**, **_artists_album_primary_sort_legal**, **_artists_track_primary_legal** and **_artists_track_primary_sort_legal** will not be set if there is no legal name alias available for the primary (first) artist.
If a join phrase is empty, a unicode zero-length space (\\u200B) will be returned in its place. If a type is empty, a value of 'unknown' will be returned in its place.

---

## Examples

The following are some examples using actual information from MusicBrainz:

### Example 1:

Using the single "[Fairytale of New York](https://musicbrainz.org/release/e428018c-5536-47f7-aca7-581e748b6fd5)"
by [Walk Off The Earth](https://musicbrainz.org/artist/e2a5eaeb-7de7-4ffe-a519-e18e427a5060) (credited as
"Gianni and Sarah"), the additional artist variables created are:

* **_artists_album_primary_id** = e2a5eaeb-7de7-4ffe-a519-e18e427a5060
* **_artists_album_primary_std** = Walk off The Earth
* **_artists_album_primary_cred** = Gianni and Sarah
* **_artists_album_primary_sort** = Walk off The Earth
* **_artists_album_all_std** = Walk off The Earth
* **_artists_album_all_cred** = Gianni and Sarah
* **_artists_album_all_sort** = Walk off The Earth
* **_artists_album_all_legal** = Walk off the Earth
* **_artists_album_all_legal_multi** = \['n/a'\]
* **_artists_album_all_sort_primary** = Walk Off The Earth
* **_artists_album_all_types** = \['Group'\]
* **_artists_album_all_count** = 1
* **_artists_track_primary_id** = e2a5eaeb-7de7-4ffe-a519-e18e427a5060
* **_artists_track_primary_std** = Walk off The Earth
* **_artists_track_primary_cred** = Gianni and Sarah
* **_artists_track_primary_sort** = Walk off The Earth
* **_artists_track_all_std** = Walk off The Earth
* **_artists_track_all_cred** = Gianni and Sarah
* **_artists_track_all_sort** = Walk off The Earth
* **_artists_track_all_legal** = Walk off the Earth
* **_artists_track_all_std_multi** = \['Walk Off The Earth'\]
* **_artists_track_all_cred_multi** = \['Gianni and Sarah'\]
* **_artists_track_all_legal_multi** = \['n/a'\]
* **_artists_track_all_sort_primary** = Walk off The Earth
* **_artists_track_all_types** = \['Group'\]
* **_artists_track_all_count** = 1

Because there is only one artist associated with this single, the **_artists_album_additional\_\***, **_artists_track_additional\_\***, **_artists_album_all_join_phrases**, and **_artists_track_all_join_phrases** variables are not created.
Because there is no legal name alias for the artist, the **_artists_album_primary_legal**, **_artists_album_primary_sort_legal**, **_artists_track_primary_legal** and **_artists_track_primary_sort_legal** variables are not created.

### Example 2:

Using the single "[Wrecking Ball](https://musicbrainz.org/release/8c759d7a-2ade-4201-abc2-a2a7c1a6ad6c)" by
[Sarah Blackwood](https://musicbrainz.org/artist/af7e5ea9-bd58-4346-8f78-d672e9f297f7),
[Jenni Pleau](https://musicbrainz.org/artist/07fa21a9-c253-4ed0-b711-d63f7965b723) &
[Emily Bones](https://musicbrainz.org/artist/541d331c-f041-4895-b8f2-7db9e27dc5ab), the additional artist variables
created are:

* **_artists_album_primary_id** = af7e5ea9-bd58-4346-8f78-d672e9f297f7
* **_artists_album_primary_std** = Sarah Blackwood
* **_artists_album_primary_cred** = Sarah Blackwood
* **_artists_album_primary_sort** = Blackwood, Sarah
* **_artists_album_primary_legal** = Sarah Nicole Blackwood
* **_artists_album_primary_sort_legal** = Blackwood, Sarah Nicole
* **_artists_album_additional_id** = \['07fa21a9-c253-4ed0-b711-d63f7965b723', '541d331c-f041-4895-b8f2-7db9e27dc5ab'\]
* **_artists_album_additional_std** = Jenni Pleau & Emily Bones
* **_artists_album_additional_cred** = Jenni Pleau & Emily Bones
* **_artists_album_additional_sort** = Pleau, Jenni & Bones, Emily
* **_artists_album_additional_legal** = Jenni Pleau & Emily Bones
* **_artists_album_additional_std_multi** = \['Jenni Pleau', 'Emily Bones'\]
* **_artists_album_additional_cred_multi** = \['Jenni Pleau', 'Emily Bones'\]
* **_artists_album_additional_sort_multi** = \['Pleau, Jenni', 'Bones, Emily'\]
* **_artists_album_additional_legal_multi** = \['n/a', 'n/a'\]
* **_artists_album_all_std** = Sarah Blackwood, Jenni Pleau & Emily Bones
* **_artists_album_all_cred** = Sarah Blackwood, Jenni Pleau & Emily Bones
* **_artists_album_all_sort** = Blackwood, Sarah, Pleau, Jenni & Bones, Emily
* **_artists_album_all_legal** = Sarah Nicole Blackwood, Jenni Pleau & Emily Bones
* **_artists_album_all_legal_multi** = \['Sarah Nicole Blackwood', 'n/a', 'n/a'\]
* **_artists_album_all_sort_primary** = Blackwood, Sarah, Jenni Pleau & Emily Bones
* **_artists_album_all_join_phrases** = \[', ', ' & '\]
* **_artists_album_all_types** = \['Person', 'Person', 'Person'\]
* **_artists_album_all_count** = 3
* **_artists_track_primary_id** = af7e5ea9-bd58-4346-8f78-d672e9f297f7
* **_artists_track_primary_std** = Sarah Blackwood
* **_artists_track_primary_cred** = Sarah Blackwood
* **_artists_track_primary_sort** = Blackwood, Sarah
* **_artists_track_primary_sort** = Blackwood, Sarah
* **_artists_track_primary_legal** = Sarah Nicole Blackwood
* **_artists_track_additional_id** = \['07fa21a9-c253-4ed0-b711-d63f7965b723', '541d331c-f041-4895-b8f2-7db9e27dc5ab'\]
* **_artists_track_additional_std** = Jenni Pleau & Emily Bones
* **_artists_track_additional_cred** = Jenni Pleau & Emily Bones
* **_artists_track_additional_sort** = Pleau, Jenni & Bones, Emily
* **_artists_track_additional_legal** = Jenni Pleau & Emily Bones
* **_artists_track_additional_std_multi** = \['Jenni Pleau', 'Emily Bones'\]
* **_artists_track_additional_cred_multi** = \['Jenni Pleau', 'Emily Bones'\]
* **_artists_track_additional_sort_multi** = \['Pleau, Jenni', 'Bones, Emily'\]
* **_artists_track_additional_legal_multi** = \['n/a', 'n/a'\]
* **_artists_track_all_std** = Sarah Blackwood, Jenni Pleau & Emily Bones
* **_artists_track_all_cred** = Sarah Blackwood, Jenni Pleau & Emily Bones
* **_artists_track_all_sort** = Blackwood, Sarah, Pleau, Jenni & Bones, Emily
* **_artists_track_all_legal** = Sarah Nicole Blackwood, Jenni Pleau & Emily Bones
* **_artists_track_all_std_multi** = \['Sarah Blackwood', 'Jenni Pleau', 'Emily Bones'\]
* **_artists_track_all_cred_multi** = \['Sarah Blackwood', 'Jenni Pleau', 'Emily Bones'\]
* **_artists_track_all_legal_multi** = \['Sarah Nicole Blackwood', 'n/a', 'n/a'\]
* **_artists_track_all_sort_primary** = Blackwood, Sarah, Jenni Pleau & Emily Bones
* **_artists_track_all_join_phrases** = \[', ', ' & '\]
* **_artists_track_all_types** = \['Person', 'Person', 'Person'\]
* **_artists_track_all_count** = 3

Because there are multiple artists associated with both the album and the track, all artist variables are created.

### Example 3:

Using the album "[Kermit Unpigged](https://musicbrainz.org/release/860fd92f-6899-4b31-a205-d6b746da734e)" by
[The Muppets](https://musicbrainz.org/artist/2ca340a6-e8f2-489d-90c2-f37c5c802d49), the additional artist variables
created for track 4, "[All I Have to Do Is Dream](https://musicbrainz.org/recording/5d98e4d4-be42-4412-94ad-f19562faa416)"
by [Linda Ronstadt](https://musicbrainz.org/artist/498f2581-be21-4eef-8756-fbb89d79b1c0) and
[Kermit the Frog](https://musicbrainz.org/artist/992a7ea8-96c1-4058-ba96-f811c8d01c77), are:

* **_artists_album_primary_id** = 2ca340a6-e8f2-489d-90c2-f37c5c802d49
* **_artists_album_primary_std** = The Muppets
* **_artists_album_primary_cred** = The Muppets
* **_artists_album_primary_sort** = Muppets, The
* **_artists_album_all_std** = The Muppets
* **_artists_album_all_cred** = The Muppets
* **_artists_album_all_sort** = Muppets, The
* **_artists_album_all_std_multi** = \['The Muppets'\]
* **_artists_album_all_cred_multi** = \['The Muppets'\]
* **_artists_album_all_legal** = The Muppets
* **_artists_album_all_legal_multi** = \['n/a'\]
* **_artists_album_all_sort_primary** = Muppets, The
* **_artists_album_all_types** = \['Group'\]
* **_artists_album_all_count** = 1
* **_artists_track_primary_id** = 498f2581-be21-4eef-8756-fbb89d79b1c0
* **_artists_track_primary_std** = Linda Ronstadt
* **_artists_track_primary_cred** = Linda Ronstadt
* **_artists_track_primary_sort** = Ronstadt, Linda
* **_artists_track_primary_legal** = Linda Maria Ronstadt
* **_artists_track_primary_sort_legal** = Ronstadt, Linda Maria
* **_artists_track_additional_id** = \['992a7ea8-96c1-4058-ba96-f811c8d01c77'\]
* **_artists_track_additional_std** = Kermit the Frog
* **_artists_track_additional_cred** = Kermit the Frog
* **_artists_track_additional_sort** = Kermit the Frog
* **_artists_track_additional_legal** = Kermit the Frog
* **_artists_track_additional_std_multi** = \['Kermit the Frog'\]
* **_artists_track_additional_cred_multi** = \['Kermit the Frog'\]
* **_artists_track_additional_sort_multi** = \['Kermit the Frog'\]
* **_artists_album_additional_legal_multi** = \['n/a'\]
* **_artists_track_all_std** = Linda Ronstadt and Kermit the Frog
* **_artists_track_all_cred** = Linda Ronstadt and Kermit the Frog
* **_artists_track_all_sort** = Ronstadt, Linda and Kermit the Frog
* **_artists_track_all_legal** = Linda Maria Ronstadt and Kermit the Frog
* **_artists_track_all_std_multi** = \['Linda Ronstadt', 'Kermit the Frog'\]
* **_artists_track_all_cred_multi** = \['Linda Ronstadt', 'Kermit the Frog'\]
* **_artists_track_all_legal_multi** = \['Linda Maria Ronstadt', 'n/a'\]
* **_artists_track_all_sort_primary** = Ronstadt, Linda and Kermit the Frog
* **_artists_track_all_join_phrases** = \[' and '\]
* **_artists_track_all_types** = \['Person', 'Character'\]
* **_artists_track_all_count** = 2

Because there is only one artist associated with the album the **_artists_album_additional\_\*** and **_artists_album_all_join_phrases** variables are not created.
