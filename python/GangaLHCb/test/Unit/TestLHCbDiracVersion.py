""" Test the ability to change the LHCbDIRAC version from the configuration"""


try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os, os.path

from Ganga.Utility.logging import getLogger
from Ganga.testlib.mark import external
from Ganga.testlib.GangaUnitTest import GangaUnitTest

from Ganga.Core.exceptions import PluginError

logger = getLogger(modulename=True)


@external
class TestLHCbDiracVersion(GangaUnitTest):
    """Test how the LHCbDIRAC versino is set"""

    def test_missing_env(self):
        """Check that missing CMTCONFIG is caught correctly"""
	from GangaLHCb.Utility.LHCbDIRACenv import store_dirac_environment
        keep = None
        if 'CMTCONFIG' in os.environ:
            keep = os.environ.pop('CMTCONFIG')
        self.assertRaises(PluginError, store_dirac_environment)
        if keep:
            os.environ['CMTCONFIG'] = keep

    def test_wildcard(self):
        """See if version can be specified as a wildcard"""
	from GangaLHCb.Utility.LHCbDIRACenv import select_dirac_version
        version = select_dirac_version('v*')
        assert version[0] == 'v'
        assert len(version) > 1

    def test_dereference(self):
        """Test that soft-links are dereferenced"""

	from GangaLHCb.Utility.LHCbDIRACenv import select_dirac_version

        version = select_dirac_version('prod')
        assert version[0] == 'v'
        assert len(version) > 1

    def test_store(self):
        """Make sure that file with environment is stored GANGADIRACENVIRONMENT env variable"""
	from GangaLHCb.Utility.LHCbDIRACenv import store_dirac_environment

        keep = os.environ.pop('GANGADIRACENVIRONMENT')
        store_dirac_environment()
        assert 'GANGADIRACENVIRONMENT' in os.environ
        os.environ['GANGADIRACENVIRONMENT'] = keep

    def test_write_cache(self):
        """Test that cache file is written"""

	from GangaLHCb.Utility.LHCbDIRACenv import store_dirac_environment

        fnamekeep = None
        if 'GANGADIRACENVIRONMENT' in os.environ:
            fnamekeep = os.environ['GANGADIRACENVIRONMENT']
            os.rename(fnamekeep, fnamekeep+'.keep')
        store_dirac_environment()
        fname = os.environ['GANGADIRACENVIRONMENT']
        assert os.path.exists(fname)
        assert os.path.getsize(fname)
        os.unlink(fname)
        if fnamekeep:
            os.rename(fnamekeep+'.keep', fnamekeep)
