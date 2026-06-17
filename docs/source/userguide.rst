User Guide
==========

ScySeqTools provides tools for coding behaviours from media and analysing the
resulting coded data. The public commands are ``scyseq-encoder`` and
``scyseq-analyser``.

Installation
------------

The common requirements are `Python <https://www.python.org>`_ and
`VLC <https://www.videolan.org/vlc/>`_. VLC is required by the encoder through
``python-vlc``.

Install ScySeqTools with:

.. code-block:: bash

   python -m pip install scyseqtools

For local development from a cloned repository, install the project in editable
mode instead:

.. code-block:: bash

   python -m pip install -e .

Encoder Guide
-------------

Launch the encoder from a terminal with:

.. code-block:: bash

   scyseq-encoder

The encoder opens a graphical interface and asks you to choose a working
directory. ScySeqTools expects or creates ``media`` and ``data`` folders inside
that working directory.

For a graphical version of the encoder workflow, open the
:ref:`encoder-workflow-flowchart` on the flowcharts page.

Project Setup
^^^^^^^^^^^^^

When starting work, choose a working directory for the project. The encoder uses
that directory as the project root:

* Put source media files in ``media/``.
* Store code definitions, HTML reports, and coded data in ``data/``.

For a new project, first define a code file, then start a coding session. For an
existing project, load an existing ``.jod`` code file or retrieve an unfinished
``.cdx`` session.

Define a Code
^^^^^^^^^^^^^

Create a code file from **Actions > Define a new code**.

Fill in the requested fields:

1. In the *Project* section, enter the project *Name* and *Description*.
2. In the *Specifications* section, enable **Regular sampling** only if the
   code should use fixed time intervals. Enter the *Interval* in seconds.
   Leave it disabled for continuous coding.
3. In *Coding definitions*, enter each *Code name* and its *List of items*,
   then click **Record**. For example, a ``movement`` code might use items
   such as ``small`` and ``large``.
4. In *Recording sites*, enter each *Recording site*, select the relevant
   *Available codes*, then click **Record**.
5. Click **Save code** and save the file in ``data/``.

The encoder saves a ``.jod`` code file and an accompanying ``.html`` report.

New Session
^^^^^^^^^^^

Start a new coding session from **Actions > Start a new session**.

1. Click **Load** in the *Media file* row and select a media file, normally
   from ``media/``.
2. Click **Load** in the *Code file* row and select the ``.jod`` code file,
   normally from ``data/``.
3. Use **Play/Pause**, **Forward**, and **Back** to navigate the media.
4. If you need fixed playback steps, enable **By period of** and enter the
   number of seconds.
5. Click **Start processing** and enter the observer or coder name.
6. Select one item for each displayed code, click **Record**, and repeat the
   play, code, record cycle.

To edit previous codes, click **Back** to reach the desired segment, restart the
video if needed, correct the selected items, and click **Record**.

The first **Record** prompts you to save a ``.cdx`` data file, normally in
``data/``. Later records update that session file. To exit the session, use
**Actions > Quit**.

Resume Session
^^^^^^^^^^^^^^

Resume an unfinished coding session from **Actions > Retrieve a session**.

1. Click **Load** in the *Data file* row.
2. Select the desired ``.cdx`` session file from ``data/``.
3. Click **Start processing**.
4. Enter the observer or coder name used for the original session.

The encoder restores the media file, code file, comments, and recorded steps,
then resumes from the last saved position.

Analysis Guide
--------------

Launch the analysis interface from a terminal with:

.. code-block:: bash

   scyseq-analyser

For a graphical version of loading data, choosing an analysis, and saving
outputs, open the :ref:`analyser-workflow-flowchart` on the flowcharts page.

Analysis Workflow
^^^^^^^^^^^^^^^^^

1. Click **Choose data directory** and select the folder containing coded
   ``.cdx`` files.
2. Select one or more entries in *Available files*.
3. Click **Select file(s)**. Loaded file names appear in *Selected files*.
4. Choose an analysis tab and select the required sites, codes, sequences, and
   parameters.
5. Click **Launch** or **Compute kappa**, depending on the selected tab.
6. Choose the output folder when prompted.

The analyser creates or uses an ``analyzer_files/`` folder next to the selected
data directory. Each analysis tab proposes a subfolder inside
``analyzer_files/`` as the default output location.

Analysis Tabs
^^^^^^^^^^^^^

Use these tabs according to the output you need:

* **Kappa** computes Cohen kappa between selected file pairs. Select sites and
  codes, use **Update codes** if you change the site selection, then click
  **Compute kappa**. Results are written to ``kappa.csv``.
* **Statistics** summarizes sequence length and symbol frequencies for one
  selected site/code sequence.
* **Mutual Information** computes mutual information between two selected
  sequences.
* **Complexity** computes normalized Lempel-Ziv complexity for one selected
  sequence.
* **Transition Probability** computes transition probabilities for one selected
  sequence and a step value.
* **Influence Probability** computes influence probabilities from a source
  sequence to a target sequence for a step value.
* **Join** combines two selected sequences and saves recoded ``.cdx`` output.
* **Change Code** recodes one selected sequence using a new code name,
  correspondence values, and alphabet labels.

Table-style analyses save ``.csv`` files. Recoding analyses such as **Join**
and **Change Code** save ``.cdx`` files that can be reused in later analyser
workflows.


Practical Tips
^^^^^^^^^^^^^^

* Always verify your folder organization before running an analysis.
* Use consistent file names to make results easier to read.
* Regularly back up your original data.
