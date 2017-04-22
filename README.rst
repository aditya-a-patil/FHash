``FHash``
=========

``FHash`` is GUI enabled python script to compute hash files in a directory.
And also verify the hashes generated to check if files were changed/altered.

Requirements
++++++++++++

    * Python 2.7

Usage
+++++

Using ``FHash`` is as easy as running the ``FHash`` python script.

.. code-block:: console

   $ python FHash.py

Message Digests currently supported
	* MD5
	* SHA1
	* SHA224
	* SHA256
	* SHA384
	* SHA512

.. warning::
   MD5 and SHA1 have known known hash collision weakness. It is highly
   recommended to not use these digests.