from scrapli.response import Response
from scrapli_netconf import NetconfScrape


def test_netconf_get(nornir_netconf, monkeypatch):
    from nornir_scrapli.tasks import netconf_get

    def mock_open(cls):
        pass

    def mock_get(cls, filter_, filter_type):
        response = Response(host="fake_as_heck", channel_input="blah")
        response._record_response(b"some stuff about whatever")
        return response

    monkeypatch.setattr(NetconfScrape, "open", mock_open)
    monkeypatch.setattr(NetconfScrape, "get", mock_get)

    result = nornir_netconf.run(task=netconf_get, filter_="blah", filter_type="subtree")
    assert result["sea-ios-1"].result == "some stuff about whatever"
    assert result["sea-ios-1"].failed is False
    assert result["sea-ios-1"].changed is False
