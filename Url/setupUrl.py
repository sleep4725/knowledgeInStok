from urllib.parse import urlencode

## ==============================
# 작성자 : 김준현
# 작성일 : 2022-01-13
## ==============================
class Url:

    @classmethod
    def ret_request_url(cls, target: str):
        """

        :param target:
        :return:
        """
        _url = "https://search.itooza.com/search.htm"
        _params = urlencode({
            "seName": target.encode("euc-kr"),
            "jl": None,
            "search_ck": None,
            "sm": None,
            "sd": None,
            "ed": None,
            "ds_de": None,
            "page": None,
            "cpv": None
        })

        return _url + "?" + _params

