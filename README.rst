========================
ArabGr1 Rubrics
========================

.. image:: tests/xml_validation_badge.svg
   :alt: XML validation badge

See the TEI XML files for the raw data and view the HTML reports in the reports directory to see the collation of the rubrics.

Report Generation
========================

To generate the HTML reports, first install teirubrics:

.. code-block:: bash

    pip install git+https://github.com/rbturnbull/teirubrics.git

Then run the following commands to generate the reports:

.. code-block:: bash

    ./mk-reports.sh

Credit
=========================

For further background, see the forthcoming chapter:

Turnbull, Robert. “The Arabic Tradition: Hagiopolite Rubrics in an Arabic Version of Paul.” 
In *The Ecumene of the Jerusalem Rite: Lectionary Traditions of the First Millennium*,  
edited by Jost Gippert, Mariam Kamarauli, and Eka Kvirkvelia.  
`Eastern Christian Cultures in Contact <https://www.brepols.net/series/ECCIC>`_. Turnhout: Brepols, 2026.

.. code-block:: bibtex

    @bookchapter{hagiopoliterubrics,
        author = {Turnbull, Robert},
        title = {{The Arabic Tradition: Hagiopolite Rubrics in an Arabic Version of Paul}},
        year = {2026},
        booktitle = {{The Ecumene of the Jerusalem Rite: Lectionary Traditions of the First Millennium}},
        publisher = {Brepols},
        address = {Turnhout},
        series = {Eastern Christian Cultures in Contact},
        editor = {Gippert, Jost and Kamarauli, Mariam and Kvirkvelia, Eka}
    }


Author: `Robert Turnbull <https://robturnbull.com>`_
