image2sgf
=========

Command line script to create an SGF file from an image for Go/Baduk/Weiqi

##### Requirements:
* Python2
* PIL (Python Image Library)

I used this script to convert images of the Korean Problem Academy tsumego to SGF.

Variables in the script must be tweaked for the images you are trying to convert.
* Change BORDER, INTERVAL and OFFSET.
* Use ORIGIN_CORNER and TARGET_CORNER to move the image to a different corner of the board

They are currently configured for the KPA problems I had.

To use the script:
`python2 image2sgf.py '/path/with/images/'`
