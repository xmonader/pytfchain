from tfchain.TFChainExplorerClient import TFChainExplorerClient
from tfchain.jsutils import json_loads

def test_explorer_client():
    client = TFChainExplorerClient()
    resp = client.get(addresses=['https://explorer2.threefoldtoken.com'], endpoint='/explorer/constants')
    data = json_loads(resp)
    assert data['chaininfo']['Name'] == 'tfchain'
    assert data['chaininfo']['CoinUnit'] == 'TFT'