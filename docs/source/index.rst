Welcome to ``FHash``
====================

``FHash`` is a GUI enabled python script to compute hash files in a directory
and verify the hashes generated to check if files were changed/altered.

Requirements
++++++++++++

    * Python 2.7

Usage
+++++

Using ``FHash`` is as easy as running the ``FHash`` python script.

.. code-block:: console

   $ python FHash.py

Why `HASH`_ Files?
++++++++++++++++++

Cryptographically hashing files and maintaining a record of hashes helps to
verify if a files was altered or tampered with. As cryptographically secure hash
functions are collision resistant, so if someone alters the file it is very
difficult to forge the hash.

Message Digests currently supported
+++++++++++++++++++++++++++++++++++
	* MD5
	* SHA1
	* SHA224
	* SHA256
	* SHA384
	* SHA512

.. warning::
   MD5 and SHA1 have known known hash collision weakness. It is highly
   recommended to not use these digests.

.. toctree::
   :maxdepth: 3
   :caption: FHash

   FHash_link
   SUPPORTED_PLATFORMS
   changelog_link


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _`HASH`: https://en.wikipedia.org/wiki/Cryptographic_hash_function