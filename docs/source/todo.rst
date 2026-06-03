Todos
=====

This is the list of things to do or decide for ScySeqTools.

1. **Configuration**

   * working directory
   * theme

.. todo:: Choose the final name and location for the ScySeqTools working directory.

2. **File format**

3. **Operations**

   * *Compute kappa*
   * *recode*, for example change to binary
   * *associate*, for example group sequences together
   * *join / concatenate*
   * *recurrences*
   * *simple stats*

.. todo:: How can we organize the data to make the kappa computation easy?

Organisation
------------

.. code-block:: bash

   scyseqtools_workdir
   |
   |- project1
      |
      |  codingframe.json
      |  structure.json?
      |
      |- media
      |
      |- data
         |
         |- session1
         |  |
         |  | metadata.json
         |  | data.json
         |
         |- session2

.. todo:: Choose if we zip files and at which level.

.. todo:: What level of the project does the user want to see explicitly?

.. todo:: How do we decide, save, and code the structure of a project?

.. todo:: Choose if we keep diffs.
