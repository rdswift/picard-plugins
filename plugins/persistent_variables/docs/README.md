# Persistent Variables \[[Download](https://github.com/rdswift/picard-plugins/raw/2.0_RDS_Plugins/plugins/persistent_variables/persistent_variables.zip)\]

## Overview

This plugin provides the ability to store and retrieve script variables that persist across tracks and albums.  This allows things like finding and storing the earliest recording date of all of the tracks on an album.

There are two types of persistent variables maintained - album variables and session variables. Album variables persist across all tracks on an album.  Each album's information is stored separately, and is reset when the album is refreshed. The information is cleared when an album is removed.  Session variables persist across all albums and tracks, and are cleared when Picard is shut down or restarted.

## Scripting Functions Added

This plugin adds eight new scripting functions to allow management of persistent script variables:

### $set_a(name,value)

Sets the album persistent variable `name` to `value`.

### $unset_a(name)

Unsets the album persistent variable `name`.

### $get_a(name)

Gets the album persistent variable `name`.

### $clear_a()

Clears all album persistent variables.

### $set_s(name,value)

Sets the session persistent variable `name` to `value`.

### $unset_s(name)

Unsets the session persistent variable `name`.

### $get_s(name)

Gets the session persistent variable `name`.

### $clear_s()

Clears all session persistent variables.

## Persistent Variables Viewer

You can view the persistent variables currently set by right-clicking on a file, track or album and selecting "View persistent variables" from the Plugins section of the context menu.  This will display the variables associated with the selected album as well as all session variables.

## Examples

### Example 1

Find the disc and album playing lengths, so that they can be included in the file metadata and used in the file naming script.

Create a tagging script containing the following:

```
$if($get_a(_pt_%discnumber%_%tracknumber%),,
  $if(%_length%,
    $set(_pt_pos,$find(%_length%,:))
    $if(%_pt_pos%,
      $set(_pt_m,$add($if2($left(%_length%,%_pt_pos%),0),0))
      $set(_pt_s,$add($if2($substr(%_length%,$add(%_pt_pos%,1)),0),0))
      $set_a(pt_d%discnumber%_d,$if2($get_a(pt_d%discnumber%_d),0))
      $set_a(pt_d%discnumber%_h,$if2($get_a(pt_d%discnumber%_h),0))
      $set_a(pt_d%discnumber%_m,$add($if2($get_a(pt_d%discnumber%_m),0),%_pt_m%))
      $set_a(pt_d%discnumber%_s,$add($if2($get_a(pt_d%discnumber%_s),0),%_pt_s%))
      $set_a(pt_r_d,$if2($get_a(pt_r_d),0))
      $set_a(pt_r_h,$if2($get_a(pt_r_h),0))
      $set_a(pt_r_m,$add($if2($get_a(pt_r_m),0),%_pt_m%))
      $set_a(pt_r_s,$add($if2($get_a(pt_r_s),0),%_pt_s%))
      $if($gt($get_a(pt_d%discnumber%_s),59),
        $set_a(pt_d%discnumber%_m,$add($get_a(pt_d%discnumber%_m),1))
        $set_a(pt_d%discnumber%_s,$sub($get_a(pt_d%discnumber%_s),60))
      )
      $if($gt($get_a(pt_r_s),59),
        $set_a(pt_r_m,$add($get_a(pt_r_m),1))
        $set_a(pt_r_s,$sub($get_a(pt_r_s),60))
      )
      $if($gt($get_a(pt_d%discnumber%_m),59),
        $set_a(pt_d%discnumber%_h,$add($get_a(pt_d%discnumber%_h),1))
        $set_a(pt_d%discnumber%_m,$sub($get_a(pt_d%discnumber%_m),60))
      )
      $if($gt($get_a(pt_r_m),59),
        $set_a(pt_r_h,$add($get_a(pt_r_h),1))
        $set_a(pt_r_m,$sub($get_a(pt_r_m),60))
      )
      $if($gt($get_a(pt_d%discnumber%_h),23),
        $set_a(pt_d%discnumber%_d,$add($get_a(pt_d%discnumber%_d),1))
        $set_a(pt_d%discnumber%_h,$sub($get_a(pt_d%discnumber%_h),24))
      )
      $if($gt($get_a(pt_r_h),23),
        $set_a(pt_r_d,$add($get_a(pt_r_d),1))
        $set_a(pt_r_h,$sub($get_a(pt_r_h),24))
      )
      $set_a(_pt_%discnumber%_%tracknumber%,1)
    )
  )
)
```

Now to make the times available as tags for all tracks, you need to create another tagging script which should be run manually just before saving the files.  This script should contain the following:

```
$set(_temp,)
$if($gt($get_a(pt_d%discnumber%_d),0),$set(_temp,$get_a(pt_d%discnumber%_d)d $get_a(pt_d%discnumber%_h)h $get_a(pt_d%discnumber%_m)m $get_a(pt_d%discnumber%_s)s),
  $if($gt($get_a(pt_d%discnumber%_h),0),$set(_temp,$get_a(pt_d%discnumber%_h)h $get_a(pt_d%discnumber%_m)m $get_a(pt_d%discnumber%_s)s),
    $if($gt($get_a(pt_d%discnumber%_m),0),$set(_temp,$get_a(pt_d%discnumber%_m)m $get_a(pt_d%discnumber%_s)s),
      $set(_temp,$get_a(pt_d%discnumber%_h)h $get_a(pt_d%discnumber%_m)m $get_a(pt_d%discnumber%_s)s)
    )
  )
)
$set(Disc Playing Time,%_temp%)

$set(_temp,)
$if($gt($get_a(pt_r_d),0),$set(_temp,$get_a(pt_r_d)d $get_a(pt_r_h)h $get_a(pt_r_m)m $get_a(pt_r_s)s),
  $if($gt($get_a(pt_r_h),0),$set(_temp,$get_a(pt_r_h)h $get_a(pt_r_m)m $get_a(pt_r_s)s),
    $if($gt($get_a(pt_r_m),0),$set(_temp,$get_a(pt_r_m)m $get_a(pt_r_s)s),
      $set(_temp,$get_a(pt_r_h)h $get_a(pt_r_m)m $get_a(pt_r_s)s)
    )
  )
)
$set(Release Playing Time,%_temp%)
```

The disc and release playing times will now be stored in each of the track files under the tag names `Disc Playing Time` and `Release Playing Time`.  These tags are also available for use in the file naming script.

### Example 2

Find the earliest recording date of any of the tracks on the album, so that it can be used in the file naming script.

Create a tagging script containing the following:

```
$set(_testdate1,$if2($get_a(earliest_date),9999))
$set_a(earliest_date,$min(%_testdate1%,$if2(%_recording_firstreleasedate%,9999)))
```

The date for the album is now available in the file naming script using `$get_a(earliest_date)`.

### Example 3

If you prefer the genre from first track of the album to be the new genre tag for all tracks.

First, from the [Genres](https://picard-docs.musicbrainz.org/en/config/options_genres.html) section of the Metadata Options, set the maximum number of genres to 1.  You might also want to enable the "Fall back on album's artists genres..." setting.  This will help ensure that you end up with one and only one genre per track (although they may still be different between tracks at this point).

The next step is to create a new tagging script in the [Scripting Options](https://picard-docs.musicbrainz.org/en/config/options_scripting.html) page.  The script should be enabled (checked) and the "Enable Tagger Script(s)" option should also be checked.  The script should contain the following:

```
$if($and($eq(%tracknumber%,1),$eq(%discnumber%,1)),$set_a(_common_genre,%genre%))
$set(genre,$if2($get_a(_common_genre),None))
```

This script retrieves the value of the `%genre%` tag from the first track on the first CD and stores it in a special album-level variable called `_common_genre`.  It then stores it in the `%genre%` tag for each of the tracks in the album.  If there was no genre found for the first track of the first disc, the `%genre%` tag will be set to "None".  If you would like a different default genre value to be used, simply replace "None" in the second script with your preferred default.

### Example 4

Get a list of all tracks on the album so that it can be included as a tag in each of the tracks.

Create a tagging script containing the following:

```
$set_a(all_tracks,$if($get_a(all_tracks),; )%tracknumber%. %title%)
```

Now to make the combined list available as a tag for all tracks, you need to create another tagging script after the previous one containing the following:

```
$set(all_tracks,$get_a(all_tracks))
```

The complete track list will now be stored in each of the track files under the tag name `all_tracks`.

### Example 5

Renumber album tracks to remove the first track from Mixed Mode CDs, where the first track is a data track.

The first step is to create a new tagging script in the [Scripting Options](https://picard-docs.musicbrainz.org/en/config/options_scripting.html) page.  The script should be enabled (checked) and the "Enable Tagger Script(s)" option should also be checked.  The script should contain the following:

```
$set(_old_tracknumber,$if2(%_old_tracknumber%,%tracknumber%))
$set(_old_totaltracks,$if2(%_old_totaltracks%,%totaltracks%))
$if($and($eq(%tracknumber%,1),$in(%title%,[data)),$set_a(_track_adjust,1))
$if($get_a(_track_adjust),
  $set(tracknumber,$sub(%_old_tracknumber%,1))
  $set(totaltracks,$sub(%_old_totaltracks%,1))
)
```

This script first stores the original values of the `%tracknumber%` and `%totaltracks%` tags and saves them in backup variables for later use.  It then checks if the `%title%` tag from the first track on the CD contains "\[data" (matching \[data\] or \[data track\]).  If it matches, then "1" is stored in a special album-level variable called `_track_adjust`.  It then adjusts (reduces) the `%tracknumber%` and `%totaltracks%` values by one for each of the tracks in the album if the `_track_adjust` variable is set.

### Example 6

When there is a pregap track (track 0), you might want to add the track 0 title to track 1 and reduce the number of total tracks by 1 to match the number of tracks excluding the pregap track.

This can be done by creating a new tagging script in the [Scripting Options](https://picard-docs.musicbrainz.org/en/config/options_scripting.html) page.  The script should be enabled (checked) and the "Enable Tagger Script(s)" option should also be checked.  The script should contain the following:

```
$if($eq(%tracknumber%,0),
  $set_a(_zero_track_title,%title% / )
  $set_a(_new_track_count,$sub(%totaltracks%,1))
)

$if($and($get_a(_zero_track_title),$eq(%tracknumber%,1),$not($startswith(%title%,$get_a(_zero_track_title)))),
  $set(title,$get_a(_zero_track_title)%title%)
)
$if($gt(%tracknumber%,0)
  $set(totaltracks,$if2($get_a(_new_track_count),%totaltracks%))
)
```

This script first stores the original title of track 0 with a separating slash in a persistent `_zero_track_title` variable.  It also stores a new (reduced) total track count in a persistent `_new_track_count` variable if there is a track number 0.  It then updates the title of track 1 to include the `_zero_track_title` variable, first checking to ensure that it hasn't already been updated, and updates the value `%totaltracks%` tag for all track numbers greater than 0 if the variable `_new_track_count` has been set.

### Example 7

When a release is a vinyl with the tracks on each side listed with the side as part of the `_musicbrainz_tracknumber` variable (such as A1, A2, B1, etc.), you might want to include the number of tracks on the side as part of the number (such as A1/3, A2/3, B1/6, etc. where side A contains 3 tracks and side B contains 6 tracks).  To do this, you need to have 2 separate tagging scripts – one to collect the track-per-side count, and the other to apply the value.

**Script 1 - Collect the information**

```
$if($resarch(%_musicbrainz_tracknumber%,^[0-9]),
  $noop(Normal numeric track number beginning with a digit)
  $noop(Do nothing)
,
  $noop(Vinyl track number beginning with a letter)
  $noop(Increment the track count for this disc number and side)
  $set(_counter,$upper($left(%_musicbrainz_tracknumber%,1))%discnumber%)
  $if($get_a(%_counter%%tracknumber%),,
    $noop(Only increment if not already processed)
    $set_a(%_counter%,$add($if2($get_a(%_counter%),0),1))
    $set_a(%_counter%%tracknumber%,1)
  )
)
```

**Script 2 - Apply the information**

```
$if($resarch(%_musicbrainz_tracknumber%,^[0-9]),
  $noop(Normal numeric track number beginning with a digit)
  $noop(Do nothing)
,
  $noop(Vinyl track number beginning with a letter)
  $noop(Save the total track count for this disc number and side)
  $set(_counter,$upper($left(%_musicbrainz_tracknumber%,1))%discnumber%)
  $set(tracknumber,%_musicbrainz_tracknumber%/$get_a(%_counter%))
)
```

This will store the updated vinyl track numbers (such as A1/3, A2/3, B1/6, etc.) to the `tracknumber` tag.  Note that some file formats (such as MP4) do not allow any non-digit (0-9) characters in the `tracknumber` tag.
