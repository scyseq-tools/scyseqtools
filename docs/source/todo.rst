todos
=====

This is the list of things to do or decide:

1. **Configuration**

   * working directory
   * theme

.. todo:: choose the name of codix working directory

2. **File format**

3. **Operations**

   * *Compute khappa*
   * *recode* e.g. change to binary
   * *associate* e.g. group sequences together
   * *join / concatenate (shouldn't be usefull with new encoder version)*
   * *recurrences*
   * *simple stats*

.. todo::   How can we organize the data to make the kappa computation easy?

Organisation
------------

.. code-block:: bash

    codix_wd
    |
    |- project1 (may be pre-project for kappa for example)
       |
       |  codingframe.json
       |  structure.json?
       |
       |- media
       |
       |- data
           |
           |- (recording) session1
           |  |
           |  | metadata.json
           |  | data.json (i.e. alphabets + sequences file or make one file per
           |               sequence?)
           |
           |- session2

.. todo:: Choose if we zip files and at which level 

.. todo:: What level of the project does the user want to see explicitely?

.. todo:: how do we (decide / save / code) the structure of a project?

.. todo:: Choose if we keep diffs.

