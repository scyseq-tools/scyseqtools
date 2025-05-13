.. codix documentation master file, created by
   sphinx-quickstart on Thu May  8 18:27:44 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

codix documentation
===================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.

.. figure:: illustrations/flowchart.png
   :align: center
   :width: 80%

   Flowchart of the encoder

.. mermaid::

   sequenceDiagram
      participant Alice
      participant Bob
      Alice->John: Hello John, how are you?
      loop Healthcheck
          John->John: Fight against hypochondria
      end
      Note right of John: Rational thoughts <br/>prevail...
      John-->Alice: Great!
      John->Bob: How about you?
      Bob-->John: Jolly good!


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   userguide
   devguide
   todo.md
