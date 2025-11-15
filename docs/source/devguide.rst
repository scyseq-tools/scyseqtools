Developer's guide
=================

The `GitHub codix repository <https://github.com/lrtpzd/codix-suite>`_ is
*private* (for now...). So you need a github account and an invitation to join
the codix project to start working with us.

The project thus uses the `git` version control system through the `GitHub`
service to keep track of the changes. You will have to learn the git procedure
to contribute. This can be done either using the command line interface (CLI) or the
`GitHub Desktop <https://github.com/apps/desktop>`_ application if you do not
feel comfortable with the CLI.

The theory of the process is the following:

1. Install the requirements and the files from GitHub to your computer i.e.
   `clone` the GitHub repository.

2. Get used to the main concepts of git to be able to contribute either to the
   documentation or the code. The concepts are the same in both cases. The main
   difference is that in the former case you will write either reStructuredText
   or markdown files (more on that later) and in the latter you will write
   Python code.

3. Decide whether you want to contribute to the documentation or to the code and
   read the corresponding section below.

Installation
------------

The process is explained in CLI but the operations are the same using the
desktop application. Just find the right buttons, menus, etc.

1. Install requirements
^^^^^^^^^^^^^^^^^^^^^^^

The common requirements are `Python <https://www.python.org>`_ and 
`vlc <https://www.videolan.org/vlc/>`_

Then in a shell:

.. code-block:: bash

   pip install hatch

2. Clone the Repository
^^^^^^^^^^^^^^^^^^^^^^^^

If you haven’t already, clone the repository to your local machine:

**Using SSH (recommended):**

.. code-block:: bash

   git clone git@github.com:lrtpzd/codix-suite.git

**Or using HTTPS:**

.. code-block:: bash

   git clone https://github.com/lrtpzd/codix-suite.git

.. note::
   If using SSH, make sure your SSH key is added to your GitHub account.

2. Navigate into the Project Folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   cd your-repo

Main git concepts/operations
----------------------------

The process is explained using the CLI but the operations are the same using the
desktop application. Just find the right buttons, menus, etc.

The main idea of a version control is to keep track of the changes made by
several collaborators on the same project, ease the "fusion" (merge) of their
contribution using a safe process and provide means to solve "conflicts". 

For short, there is a "main" branch and collaborators work in their own branch.
Once they are done with their changes they "record" (commit) them locally,
"send" (push) them to the repository and ask for "insertion" in the main branch
(pull request).

The complete `git documentation <https://git-scm.com/doc>`_ is freely available on the web.

1. (Optional) Configure Your Git Identity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Only needed if not already configured:

.. code-block:: bash

   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"

2. Create a New Branch
^^^^^^^^^^^^^^^^^^^^^^

You should avoid pushing directly to ``main``. Always create a new branch:

.. code-block:: bash

   git checkout -b my-new-branch-name

3. Make Changes and Commit
^^^^^^^^^^^^^^^^^^^^^^^^^^

After editing files:

.. code-block:: bash

   git add .
   git commit -m "Describe your changes here"

4. Push Your Changes
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   git push origin my-new-branch-name

5. Open a Pull Request
^^^^^^^^^^^^^^^^^^^^^^

Go to the repository on GitHub. You should see a prompt to open a **pull request**. This allows others to review your changes before merging.

6. Stay Up to Date with ``main``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before starting new work, sync your local repo with the latest changes from ``main``:

.. code-block:: bash

   git checkout main
   git pull origin main

Then update your feature branch:

.. code-block:: bash

   git checkout new-feature-name
   git merge main

.. note::
   Alternatively, you can use ``git rebase main`` **only** if you're comfortable with rebasing.

Writing documentation
---------------------

The documentation of ``codix`` uses the `sphinx documentation system
<https://www.sphinx-doc.org/en/master/index.html>`_.

The default format for writing the documentation is ``reStructuredText``. It is
documented in the `sphinx reStrucuturedText documentation
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_ or in
the `docutils documentation <https://docutils.sourceforge.io/rst.html>`_.  Files
written in reStructuredText format have the ``.rst`` extension.

If you are more comfortable with ``markdown`` format you can also use this
format and save your files with the ``.md`` extension.

To build the documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   hatch shell
   cd docs
   make html

Making diagrams
^^^^^^^^^^^^^^^

The solution chosen here is to use the ``mermaid`` directive in the
reStructuredText files

See the doc: 

* `sphinxcontrib-mermaid <https://sphinxcontrib-mermaid-demo.readthedocs.io/en/latest/>`_

* `mermaid website <http://mermaid.js.org/>`_ (there is a mermaid live editor
   online)

For flowcharts see: `mermaid doc for flowcharts
<http://mermaid.js.org/syntax/flowchart.html>`_

_But_, it does not produce the diagram after ``make latexpdf``.

So ``.png`` file are generated using the `mermaid CLI
<https://github.com/mermaid-js/mermaid-cli>`_ 

In `conf.py` the `mermaid_output_format` is set to `png`.

`mermaid-cli` is installed using:

.. code-block::

   npm install --prefix ~/mermaid-cli @mermaid-js/mermaid-cli

Since the global installation (using `-g` as on the github page) did not work
for me. It leads to set the `mermaid_cmd` in the `conf.py` of Sphinx. The `.mmd`
files in `_static` are converted and inserted in both `html` and `latexpdf` as
png images.

.. todo::
   When public repository, use the extension githubpages to publish the doc
   using a branch gh-pages.
