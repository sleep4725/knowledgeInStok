import os
import yaml


class InvestmentList:

    @classmethod
    def get_investment_list(cls, file_path: str):
        """

        :return:
        """
        result = os.path.exists(file_path)
        if not result:
            raise FileNotFoundError
        else:
            with open(file_path, "r", encoding="utf-8") as fr:
                data = yaml.safe_load(fr)
                fr.close()
                print(data)

                return data["investment"]