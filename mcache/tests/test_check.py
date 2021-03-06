# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.mcache.mcache import InvalidConfigError

from .common import HOST, PORT, SERVICE_CHECK


def test_bad_config(check):
    """
    If misconfigured, the check should raise an InvalidConfigError
    """
    with pytest.raises(InvalidConfigError):
        check.check({})


def test_service_ko(check, aggregator):
    """
    If the service is down, the service check should be sent accordingly
    """
    tags = ['host:{}'.format(HOST), 'port:{}'.format(PORT), 'foo:bar']
    with pytest.raises(ConfigurationError):
        check.check({'url': '{}'.format(HOST), 'port': PORT, 'tags': ['foo:bar']})
    assert len(aggregator.service_checks(SERVICE_CHECK)) == 1
    sc = aggregator.service_checks(SERVICE_CHECK)[0]
    assert sc.status == check.CRITICAL
    assert sc.tags == tags
