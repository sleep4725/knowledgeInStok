import copy
from SeleniumObject.seleniumClient import ret_selenium_client
from Url.setupUrl import Url

from selenium.webdriver.common.by import By
from XlObject.xlClient import XlClient
from InvestmentClient.investClient import InvestmentList
##
# 작성자 : 김준현
# 작성일 : 2021-01-13
##
class Itooza:

    def __init__(self):
        """
        :param investment.yml: 투자종목
        """
        self.investment_list = InvestmentList.get_investment_list(file_path="InvestmentList/investment.yml")
        self.selenium_client = None
        self.item1 = ["PER", "PBR", "ROE = ROS * S/A * A/E", "EPS", "BPS"]
        self.item2 = ["5년ROE", "5년EPS성장률"]
        self.data = dict()
        self.total_element = list()
        self.xl_client = XlClient()

    def item_header(self, resp):
        """

        :return:
        """
        item_header = resp.find_element(By.CLASS_NAME, "item-wrap").\
            find_element(By.CLASS_NAME, "item-head").\
            find_element(By.TAG_NAME, "h1")

        investment = item_header.find_element(By.CLASS_NAME, "name") # 주가 종목
        code = item_header.find_element(By.CLASS_NAME, "code.floatleft")

        self.data["name"] = str(investment.text)
        self.data["code"] = str(code.text)


    def item_body(self, resp):
        """

        :return:
        """
        for page in range(1, 3): # body의 구조가 페이지 1과2가 모두 동일하다
            body = resp.find_element(By.ID, "stockItem").\
                find_element(By.CLASS_NAME, "item-body").\
                find_element(By.CLASS_NAME, "ar").\
                find_element(By.CLASS_NAME, "item-data{0}".format(page)).\
                find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")


            for indx, b in enumerate(body):
                if indx == 0:
                    th_list = [th.text for th in b.find_elements(By.TAG_NAME, "th")]
                elif indx == 1:
                    td_list = [th.text for th in b.find_elements(By.TAG_NAME, "td")]

            tmp_key_dict = {}

            if page == 1:
                for k, v in zip(th_list, td_list):
                    if k in self.item1:
                        if k == "ROE = ROS * S/A * A/E":
                            if v != "(-)":
                                tmp_key_dict["ROE"] = float(str(v.split("=")[0].strip()).rstrip("%"))
                            else:
                                tmp_key_dict["ROE"] = 0.00
                        else:
                            if v != "(-)":
                                tmp_key_dict[k] = float(v.replace(",", "."))
                            else:
                                tmp_key_dict[k] = 0.00

                self.data.update(tmp_key_dict)

            elif page == 2:
                for k, v in zip(th_list, td_list):
                    if k in self.item2:
                        if v != "N/A":
                            tmp_key_dict[k] = float(str(v).strip().rstrip("%"))
                        else:
                            # v == "N/A"
                            tmp_key_dict[k] = 0.00

                self.data.update(tmp_key_dict)

    def req(self):
        """

        :return:
        """
        for indx, invest in enumerate(self.investment_list):
            url = Url.ret_request_url(target=invest)
            print(url)
            self.selenium_client = ret_selenium_client()
            # ======================================

            self.selenium_client.get(url)
            self.selenium_client.implicitly_wait(3)

            resp = self.selenium_client.find_element(By.ID, "content")
            self.item_header(resp)
            self.item_body(resp)
            self.data["num"] = indx + 1
            self.total_element.append(copy.deepcopy(self.data))

            self.data.clear()
            self.selenium_client.close()
            # =======================================
            self.xl_client.xl_file_write(data=self.total_element)



def main():
    o = Itooza()
    o.req()

if __name__ == "__main__":
    main()