# pyweb-gen
A static site generator written in python.
Currently compatible with Linux.

## Dependencies
The following must be installed in your linux system:
* python3
* pandoc

## Downloading
Currently this program not available on PyPi. To download it, go to the releases page.

## Running
Follow the below steps:
* Download the latest release from the releases page.
* In a new directory, run `$ pip install <location_of_the_downloaded_whl_file>`
* Now, to initialize the direcotry, run `$ pyweb-gen init`. This will set up the directory structure for your blog.
* To add a new post, run `$ pyweb-gen new-post --title title_of_the_post --image[optional] --description[optional]`
* You can edit the md of the post using a text editor of your choice from inside the `data` folder.
* Once done editing, you can run `$ pyweb-gen refresh` to publish it to your blog.

