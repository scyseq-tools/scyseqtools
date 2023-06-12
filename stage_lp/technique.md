# Structure of the softwares

## Structure of the encoder

The encoder is a GUI that commands VLC player and favors the encoding of a video.

`encoder`
  : this is the main script which is the enter point of the codix-encoder software
     
`applicationmenu.py`
  : the menu of the application (a very simple menu since the software is simple on purpose).

`codingframe.py`
  : the part of the interface which is dynamically built using an encoding definition read in a `.cod` file

`ib.py`
  : this is an old file and **I think this file should dissapear** 

`infoframe.py`
  : the frame which displays the informations about the code file (`.cod`), media file and data file (`ext?`).

`playercontrol.py`
  : the file where the functions that command the VLC player should be grouped (not done in the codix3.0.1...)

`utils.py`
  : I think this file does not have any further used function **Check this**.

`newcode.py`
  : an independent application which can be launched from the main `encoder` script
 
 `htmlreport.py`
  : the templates for the html report  after a new code has been defined.

## Struture of the analyzer

The analyzer is built on a client / server architecture. It is supposed to propose (some of) the `scikits-symbolic` procedures via a webservice server based on [Ladon](https://pypi.org/project/ladon/) library **Is it the right technique? Is Ladon still maintained?**. (see also [jsonwspclient](https://pypi.org/project/jsonwspclient/) for a client in replacement of Ladon client side).
