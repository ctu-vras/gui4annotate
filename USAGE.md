# Usage
## gui4annotate

## Table of contents

1. [Running the program](#run)
2. [Description of GUI](#gui)
6. [Navigating through folders and adding other folders](#folders)
3. [Image frame](#image)
4. [Adding and removing annotations](#anno)
5. [Changing annotations](#change-anno)
7. [Saving annotations](#save)
8. [Keyboard shortcuts](#key)

## Running the program <a name="#run"></a>

To be sure your system meets all the requirements, read file `INSTALL.md` first

#### Command-line

`python3 gui.py` - only for Linux/OS X

#### Double clicking

The file `gui.py` itself is made executable, so you should be able to run file `gui.py` by regular double clicking. Don't worry if a console pops up when running on Windows - this happens normally.

## Description of GUI <a name="#gui"></a>

When you run the program, you will notice a toolbar with couple icons, and two big areas, that are directly after starting up blank.
The toolbar consists of these controls (from left to right):

+ Folder chooser
+ Save annotations for current image
+ Save annotations for all images
+ Previous image
+ Next image
+ Zoom buttons with a scale bar
+ Three buttons for changing modes (see [Image](#image) section)
+ Help 
+ About

The left area is for navigation through folders and right area is for viewing the image.

## Navigating through folders and adding folders <a name="#folders"></a>

When you choose a folder to load by Folder chooser button, a new directory structure will apper in left area. The directory structure contains all its subfolders, however, only image files are present as files. For each image for which there was found corresponding annotation file, the image is populated with all annotation data saved on computer. The bold number next to image filename is number of annotations.

Each annotation includes name of class (default name is 'Blyskacek') and 4 points denoting left-top and right-bottom corners of annotation

Left (right) button will select previous (next) image across folders

You can have multiple folders loaded inside a program.

## Image frame <a name="#image"></a>

When you select an image from folder view, it will load into image frame.

Image can be zoomed by zoom buttons or a scale bar.

There are three modes of operation within image frame:

+ Moving 
+ Drawing annotations
+ Removing annotations

Moving around the image can be done only when the image is zoomed enough. Adding and removing annotations is described in [next part](#anno)

## Adding and removing annotations <a name="#anno"></a>

When the image frame is in adding mode, you can simply draw annotations whenever in the image you want. Note that however, you will not be able to draw outside of your viewport, which might be rather small with zoomed out image. Every drawn annotation will be given default tag which is 'Default bug'. This can be changed in file `gui_annotation.constants` in variable `Constants.DEFAULT_ANNOTATION` (*might have change in the future to a more user-friendly setting*)

When the image frame is in removing mode, clicking anywhere inside anyannotation will remove the annotation. Note that when there are multiple overlapping annotation and the click occurs inside the overlapping region, **ALL** annotations will be removed.

## Changing annotations <a name="#change-anno"></a>

If the annotation is selected inside Folder view and double-clicked, every item in the annotation can be edited. Any string is allowed as annotation class, only numbers within the range (0, size_of_image) are allowed. Note that first two numbers in folder view **always** represent left-top corner and other two always represent right-bottom corner, so the values you have entered might have switch their position after edited

## Saving annotations <a name="#save"></a>

The first saving button will save annotations for current image opened in Image view. Each annotation for a file is on one line, values on a line are separated by comma (`,`). First four values are describing left-top corner and right-bottom corner of annotation in order `lt.x,lt.y,rb.x,rb.y`. Last value is annotation class. Such a file is saved under same filename as image filename with image extension being replaced by extension `.txt`

All decimal values are rounded to digit.

Second saving button will save annotations for all changed files in folder view.

If some image has 0 annotations, empty file will **NOT** be created and if there existed annotation file for such image file in the past, it will be deleted.

All unsaved annotations and folders containing them will be shown red in folder view until they are saved.


## Keyboard shortcuts <a name="#key"></a>

None of the keyboard shortcuts work while editing values of annotations manually. Shortcuts work only if performed action is available through standard GUI

+ <kbd>Ctrl</kbd> + <kbd>s</kbd>
  + Save annotations for current image file
+ <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>s</kbd>
  + Save annotations for all changed files
+ <kbd>&larr;</kbd>
  + Previous image
+ <kbd>&rarr;</kbd>
  + Next image
+ <kbd>+</kbd>
  + Zoom in
+ <kbd>-</kbd>
  + Zoom out
+ <kbd>m</kbd>
  + Moving mode
+ <kbd>a</kbd>
  + Drawing mode (Adding annotations)
+ <kbd>r</kbd>
  + Removing mode
+ <kbd>d</kbd>
  + Automatically detect ROIs
+ <kbd>ctrl</kbd> + <kbd>d</kbd>
  + Detector settings
+ <kbd>h</kbd>
  + Shows help
+ <kbd>i</kbd>
  + Creates new annotation in the current image with values `lt = rb = [0,0]` and annotation class is 'Default bug' to modify manually.
+ <kbd>Del</kbd>
  + If the current selection in folder view is annotation, deletes this annotation
  + If the current selection in folder view is image file, deletes **ALL** annotations for this image file
+ <kbd>c</kbd>
  + If the current selection in folder view is annotation, enters edit mode for annotation's class, using <kbd>Tab</kbd>/<kbd>Shift</kbd> + <kbd>Tab</kbd> you can rotate through all fields of annotation
  + If the current selection in folder view is image file, enters edit mode for first annotation of this image


#### Intended workflow for keyboard

1. Load folder (only by GUI)
2. Navigate to desired image by <kbd>&larr;</kbd>/<kbd>&rarr;</kbd> arrows.
3. Create new annotation by <kbd>a</kbd>
4. Change annotation value by <kbd>c</kbd> and <kbd>Tab</kbd>
5. Repeat steps 2-4
6. Save all annotations by <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>s</kbd>


