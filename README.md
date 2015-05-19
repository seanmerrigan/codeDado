# codeDado
Create abridged copies of files based on inline tags.

This is a tool for creating multiple smaller versions of a large file in an attempt to easily share code between similar versions.

The specific case this tool was created for is a JS file which can embed HTML or Flash assets to a page in a number of ways.  Originally one file was used to handle all cases, but as the code for each case grew it was decided that smaller files should be created for each type of delivery.
I wanted to avoid copying and pasting the same code all over the place, and I also wanted to avoid having multiple small files that get stitched together as needed.  (And the output has to be a single file, as it is served from a DB.)

Here are some advantages to starting with one large all-encompassing file, then stripping out the unnecessary pieces to create smaller files for specific purposes:
* **Sharing code is dead simple.**  This tool strips out code that is specific to certain purposes, so if something needs to be shared, just don't tag it.
* **Debugging is facilitated.**  An intermediary file is created, which can later be minified.  When code is omitted from the intermediary file, line breaks are added so that line numbers are maintained.  If your browser's debugger says there's an error on line 347, you can go to line 347 in your code.
* **IDEs can do their thing.**  Since the file you're editing has all the code (not just blocks of it broken down across multiple un-runable files for reuse) you can rely on all the code-hinting, error-underlining, refactoring goodness that your IDE offers.

To use, add begin and end tags to your code, then run the tool.

Example of code tagging (if 'flash-video-adunit' is not passed to code_dado as an argument, the section between the two tags will be omitted):
```
…
					break;
				}
				if (TM.Util.isNull(embed)) {
					embed = getErrorEmbed();
				}
				return embed;
			},
/*--[BEGIN:flash-video-adunit]--*/
			getNewFlashEmbed = function () {
				var str = "",
					isIE = /*@cc_on!@*/false;
				if (isIE) {
					str = '<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" id="FlashUnit"' +
					' name="FlashUnit" width="' + width + '" height="' + height + '" >' +
					'<param … /></object>';
				} else {
					str = '<embed id="FlashUnit" name="FlashUnit" width="' + width + '" height="' +
					…
					'" allowscriptaccess="always" allowfullscreen="true" />';
				}
				str += getExtraHtml();
				return str;
			},
/*--[END:flash-video-adunit]--*/
/*--[BEGIN:flash-standard-display]--*/
			getFlashStdDispEmbed = function () {
				var str = null,
					assetUrl,
					H, i,
…
```

Syntax:

`python2.7 code_dado.py [source_file] [target_file] [tag_to_keep1] ... [tag_to_keep*n*]`

I recommend using a bash script to automatically generate your multiple versions of code.  In the example below, each derivative file gets run through this tool, then minified with a comment on top.

Example: build_all.sh
```
#!/usr/bin/env bash

# Tags currently in use:
# flash-video-adunit
# html-video-adunit
# flash-standard-display
# 3rd-party-mraid

# pass the path of the python file (code_dado.py) as the paramater
# E.g., ./build_all.sh ~/PythonProjects/CodeDado/code_dado.py

# Build Flash Ad Unit template
eval "python2.7 "$1" master_ad_template.js flash_unit_ad_template.js flash-video-adunit"
java -jar yuicompressor-2.4.2.jar flash_unit_ad_template.js > flash_unit_ad_template.min.tmp
echo "//Flash Unit Template" | cat - flash_unit_ad_template.min.tmp > flash_unit_ad_template.min.js

# Build Mobile Ad Unit template
eval "python2.7 "$1" master_ad_template.js mobile_ad_template.js 3rd-party-mraid html-video-adunit"
java -jar yuicompressor-2.4.2.jar mobile_ad_template.js > mobile_ad_template.min.tmp
echo "//Mobile Template" | cat - mobile_ad_template.min.tmp > mobile_ad_template.min.js

# Build Standard Display template
eval "python2.7 "$1" master_ad_template.js standard_display_ad_template.js flash-standard-display"
java -jar yuicompressor-2.4.2.jar standard_display_ad_template.js > standard_display_ad_template.min.tmp
echo "//Standard Display Template" | cat - standard_display_ad_template.min.tmp > standard_display_ad_template.min.js

# Build legacy inbanner template
# Build Standard Display template
eval "python2.7 "$1" master_ad_template.js legacy_inbanner_ad_template.js flash-standard-display 3rd-party-mraid"
java -jar yuicompressor-2.4.2.jar legacy_inbanner_ad_template.js > legacy_inbanner_ad_template.min.tmp
echo "//Standard Display Template" | cat - legacy_inbanner_ad_template.min.tmp > legacy_inbanner_ad_template.min.js

rm  flash_unit_ad_template.min.tmp mobile_ad_template.min.tmp standard_display_ad_template.min.tmp legacy_inbanner_ad_template.min.tmp
```
