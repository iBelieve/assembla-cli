============
Assembla CLI
============

Assembla CLI is an unofficial command-line interface to Assembla. It provides commands to easily open and apply merge requests, as well as commands to open different Assembla views in your project.


Installation
------------

Install using `pip` (both Python 2 and 3 are supported)::

    pip install assembla-cli


Usage
-----

Run using::

    assembla COMMAND [ARGS...]

The following commands are available:

- ``apply MERGE_URL``

  Rebases a merge request on top of the target branch and then fast-forward merges it onto the target branch. The merge request is then closed. The merged commits are not pushed to Assembla, so you are able to use ``git rebase`` to interactively edit, squash, or remove commits.

- ``apply BRANCH_NAME``

  Rebases a branch on top of the current branch and then fast-forward merges it onto the current branch. The merged commits are not pushed to Assembla, so you are able to use ``git rebase`` to interactively edit, squash, or remove commits.

- ``review``

  Opens your web browser to the Merge Requests page in your Assembla space so you can review open merge requests.

- ``merge-request``

  Opens your web browser to the New Merge Request page for your Assembla space, prefilled with the current branch as the source branch and your main branch (``develop`` or ``master``) as the target branch.

- ``tickets``

  Opens your web browser to the Tickets page in your Assembla space.

- ``new-ticket``

  Opens your web browser to the New Ticket page in your Assembla space.


Licensing
---------

Assembla CLI is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
