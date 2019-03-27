from Jumpscale import j

import hashlib
from datetime import datetime, timedelta
from tfchain.encoders import encoder_rivine_get, encoder_sia_get
from tfchain.crypto.utils import blake2_string
from tfchain.types.PrimitiveTypes import BinaryData, Hash

from tfchain.types.ConditionTypes import ConditionFactory, OutputLock
from tfchain.jsutils import duration, jsdatetime, jstime


def test_conditiontypes_factory():
    """
    js_shell 'types_factory.conditions.test()'
    """
    factory = ConditionFactory()
    # some util test methods

    def test_encoded(encoder, obj, expected):
        encoder.add(obj)
        output = encoder.data.hex()
        if expected != output:
            msg = "{} != {}".format(expected, output)
            raise Exception("unexpected encoding result: " + msg)

    def test_sia_encoded(obj, expected):
        test_encoded(encoder_sia_get(), obj, expected)

    def test_rivine_encoded(obj, expected):
        test_encoded(encoder_rivine_get(), obj, expected)

    # Nil conditions are supported
    for n_json in [{}, {"type": 0}, {"type": 0, "data": None}, {"type": 0, "data": {}}]:
        cn = factory.from_json(n_json)
        assert cn.json() == {"type": 0}
        test_sia_encoded(cn, '000000000000000000')
        test_rivine_encoded(cn, '0000')
        assert str(
            cn.unlockhash) == '000000000000000000000000000000000000000000000000000000000000000000000000000000'

    # UnlockHash conditions are supported
    uh_json = {"type": 1, "data": {
        "unlockhash": "000000000000000000000000000000000000000000000000000000000000000000000000000000"}}
    cuh = factory.from_json(uh_json)
    assert cuh.json() == uh_json
    test_sia_encoded(
        cuh, '012100000000000000000000000000000000000000000000000000000000000000000000000000000000')
    test_rivine_encoded(
        cuh, '0142000000000000000000000000000000000000000000000000000000000000000000')
    assert str(
        cuh.unlockhash) == '000000000000000000000000000000000000000000000000000000000000000000000000000000'

    # AtomicSwap conditions are supported
    as_json = {"type": 2, "data": {"sender": "01e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f70b1ccc65e2105",
                                   "receiver": "01a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc353bdcf54be7d8", "hashedsecret": "abc543defabc543defabc543defabc543defabc543defabc543defabc543defa", "timelock": 1522068743}}
    cas = factory.from_json(as_json)
    assert cas.json() == as_json
    test_sia_encoded(cas, '026a0000000000000001e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35abc543defabc543defabc543defabc543defabc543defabc543defabc543defa07edb85a00000000')
    test_rivine_encoded(cas, '02d401e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35abc543defabc543defabc543defabc543defabc543defabc543defabc543defa07edb85a00000000')
    assert str(
        cas.unlockhash) == '026e18a53ec6e571985ea7ed404a5d51cf03a72240065952034383100738627dbf949046789e30'

    # MultiSig conditions are supported
    ms_json = {"type": 4, "data": {"unlockhashes": ["01e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f70b1ccc65e2105",
                                                    "01a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc353bdcf54be7d8"], "minimumsignaturecount": 2}}
    cms = factory.from_json(ms_json)
    assert cms.json() == ms_json
    test_sia_encoded(cms, '0452000000000000000200000000000000020000000000000001e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35')
    test_rivine_encoded(
        cms, '049602000000000000000401e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35')
    assert str(
        cms.unlockhash) == '0313a5abd192d1bacdd1eb518fc86987d3c3d1cfe3c5bed68ec4a86b93b2f05a89f67b89b07d71'

    # LockTime conditions are supported:
    # - wrapping a nil condition
    lt_n_json = {"type": 3, "data": {
        "locktime": 500000000, "condition": {"type": 0}}}
    clt_n = factory.from_json(lt_n_json)
    assert clt_n.json() == lt_n_json
    test_sia_encoded(clt_n, '0309000000000000000065cd1d0000000000')
    test_rivine_encoded(clt_n, '03120065cd1d0000000000')
    assert str(
        clt_n.unlockhash) == '000000000000000000000000000000000000000000000000000000000000000000000000000000'
    # - wrapping an unlock hash condition
    lt_uh_json = {"type": 3, "data": {
        "locktime": 500000000, "condition": uh_json}}
    clt_uh = factory.from_json(lt_uh_json)
    assert clt_uh.json() == lt_uh_json
    test_sia_encoded(
        clt_uh, '032a000000000000000065cd1d0000000001000000000000000000000000000000000000000000000000000000000000000000')
    test_rivine_encoded(
        clt_uh, '03540065cd1d0000000001000000000000000000000000000000000000000000000000000000000000000000')
    assert str(
        clt_uh.unlockhash) == '000000000000000000000000000000000000000000000000000000000000000000000000000000'
    # - wrapping a multi-sig condition
    lt_ms_json = {"type": 3, "data": {
        "locktime": 500000000, "condition": ms_json}}
    clt_ms = factory.from_json(lt_ms_json)
    assert clt_ms.json() == lt_ms_json
    test_sia_encoded(clt_ms, '035b000000000000000065cd1d00000000040200000000000000020000000000000001e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35')
    test_rivine_encoded(
        clt_ms, '03a80065cd1d000000000402000000000000000401e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35')
    assert str(
        clt_ms.unlockhash) == '0313a5abd192d1bacdd1eb518fc86987d3c3d1cfe3c5bed68ec4a86b93b2f05a89f67b89b07d71'

    # FYI, Where lock times are used, it should be known that these are pretty flexible in definition
    assert OutputLock().value == 0
    assert OutputLock(value=0).value == 0
    assert OutputLock(value=1).value == 1
    assert OutputLock(value=1549483822).value == 1549483822
    # if current_timestamp is not defined, the current time is used: int(datetime.now().timestamp)
    assert OutputLock(value='+7d', current_timestamp=1).value == 604801
    assert OutputLock(value='+7d12h5s',
                      current_timestamp=1).value == 648006
    assert OutputLock(value='30/11/2020').value == 1606690800
    assert OutputLock(value='11/30').value == OutputLock(
        value='30/11/{}'.format(datetime.now().year)).value  # year is optional
    assert OutputLock(value='30/11/2020 23:59:59').value == 1606777199
    # seconds is optional
    assert OutputLock(value='30/11/2020 23:59').value == 1606777140
