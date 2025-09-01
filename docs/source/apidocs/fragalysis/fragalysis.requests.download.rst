:py:mod:`fragalysis.requests.download`
======================================

.. py:module:: fragalysis.requests.download

.. autodoc2-docstring:: fragalysis.requests.download
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`target_list <fragalysis.requests.download.target_list>`
     - .. autodoc2-docstring:: fragalysis.requests.download.target_list
          :summary:
   * - :py:obj:`download_target <fragalysis.requests.download.download_target>`
     - .. autodoc2-docstring:: fragalysis.requests.download.download_target
          :summary:

API
~~~

.. py:function:: target_list(stack: str = 'production', token: str | None = None) -> list[dict]
   :canonical: fragalysis.requests.download.target_list

   .. autodoc2-docstring:: fragalysis.requests.download.target_list

.. py:function:: download_target(name: str, tas: str, stack: str = 'production', token: str | None = None, destination: str = '.') -> None
   :canonical: fragalysis.requests.download.download_target

   .. autodoc2-docstring:: fragalysis.requests.download.download_target
