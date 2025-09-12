:py:mod:`fragalysis.requests.jobs`
==================================

.. py:module:: fragalysis.requests.jobs

.. autodoc2-docstring:: fragalysis.requests.jobs
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`transfer_snapshot <fragalysis.requests.jobs.transfer_snapshot>`
     - .. autodoc2-docstring:: fragalysis.requests.jobs.transfer_snapshot
          :summary:
   * - :py:obj:`create_session_project <fragalysis.requests.jobs.create_session_project>`
     - .. autodoc2-docstring:: fragalysis.requests.jobs.create_session_project
          :summary:
   * - :py:obj:`create_snapshot <fragalysis.requests.jobs.create_snapshot>`
     - .. autodoc2-docstring:: fragalysis.requests.jobs.create_snapshot
          :summary:
   * - :py:obj:`get_last_session_project_id <fragalysis.requests.jobs.get_last_session_project_id>`
     - .. autodoc2-docstring:: fragalysis.requests.jobs.get_last_session_project_id
          :summary:

API
~~~

.. py:function:: transfer_snapshot(token: str, snapshot_id: int, session_project_id: int, target_id: int, stack: str = 'production')
   :canonical: fragalysis.requests.jobs.transfer_snapshot

   .. autodoc2-docstring:: fragalysis.requests.jobs.transfer_snapshot

.. py:function:: create_session_project(token: str, author_id: int, target_id: int, project_id: int, *, stack: str = 'production', title: str = 'API created project', description: str = 'API created project')
   :canonical: fragalysis.requests.jobs.create_session_project

   .. autodoc2-docstring:: fragalysis.requests.jobs.create_session_project

.. py:function:: create_snapshot(token: str, author_id: int, session_project_id: int, *, stack='production', title: str = 'API created snapshot', description: str = 'API created snapshot')
   :canonical: fragalysis.requests.jobs.create_snapshot

   .. autodoc2-docstring:: fragalysis.requests.jobs.create_snapshot

.. py:function:: get_last_session_project_id(target_id: int, author_id: int, stack: str = 'production')
   :canonical: fragalysis.requests.jobs.get_last_session_project_id

   .. autodoc2-docstring:: fragalysis.requests.jobs.get_last_session_project_id
