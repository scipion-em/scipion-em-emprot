=======================
EMProt plugin
=======================

**Documentation under development, sorry for the inconvenience**

This is a **Scipion** plugin that offers `EMProt <https://github.com/huang-laboratory/EMProt>`_


==========================
Install this plugin
==========================

You will need to first install
`Scipion3 <https://scipion-em.github.io/docs/release-3.0.0/docs/scipion-modes/how-to-install.html>`_


1. **Install the plugin in Scipion**

EMProt is installed automatically by scipion.

- **Install the stable version (Not available yet)**

    Through the plugin manager GUI by launching Scipion and following **Configuration** >> **Plugins**

    or

.. code-block::

    scipion3 installp -p scipion-em-emprot


- **Developer's version**

    1. **Download repository**:

    .. code-block::

        git clone https://github.com/scipion-em/scipion-em-emprot.git

    2. **Switch to the desired branch** (master or devel):

    scipion-em-emprot is constantly under development and including new features.
    If you want a relatively older an more stable version, use master branch (default).
    If you want the latest changes and developments, user devel branch.

    .. code-block::

                cd scipion-em-emprot
                git checkout devel

    3. **Install**:

    .. code-block::

        scipion3 installp -p path_to_scipion-em-emprot --devel




