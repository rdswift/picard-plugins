# Script Logger

This plugin provides a new script function `$logline()` to write entries to Picard's system log.  By default, the log level is set at `Info`, but any level can be used by providing the level as an optional second parameter to the function.  The function is available to both user scripts and file naming scripts.

## Usage

The function is used as `$logline(text[,level])`, where `text` is the text to write to the log.  The entry will be written at log level `Info` by default, but this can be changed by specifying a different level as an optional second parameter.  Allowable log levels are:

- E (Error)
- W (Warning)
- I (Info)
- D (Debug)

If an unknown level is entered, the function will use the default `Info` level.

## Examples

`$logline(This is a text message.)` will add "Script Logger: This is a test message." to the log at the `Info` level.

`$logline(This is another text message.,)` will add "Script Logger: This is another test message." to the log at the `Info` level.

`$logline(This is an error message.,E)` will add "Script Logger: This is an error message." to the log at the `Error` level.

`$logline(This is another error message.,Error)` will add "Script Logger: This is another error message." to the log at the `Error` level.
