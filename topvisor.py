import json
import requests
import os

class Topvisor:


    def __init__(self):
        print('Authorizing Topvisor')
        self.user = '296177'
        self.key = 'c1414daa91881b0b278c'
        self.headers = {'Content-type': 'application/json', 'User-Id': self.user, 'Authorization': f'bearer {self.key}'}
        self.server = 'https://api.topvisor.com'

        if not os.path.exists("topvisor_data/"):
            os.mkdir("topvisor_data/")


    def get_projects(self):

        payload = {
            "show_site_stat": True,
            "show_searchers_and_regions": True
        }
        response = requests.post(f'{self.server}/v2/json/get/projects_2/projects', headers=self.headers, data=json.dumps(payload))

        with open('topvisor_data/projects.json', "w", encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()


    # def get_region_indexes(self, project_id):
    #
    #     with open('topvisor_data/projects.json', 'r', encoding='utf-8') as data:
    #         "id": 4944800
    #
    #
    #
    #     return yandex_index
    #


    def get_competitors(self, project_id):

        payload = {
            "project_id": project_id,
            "only_enabled": True,
            "include_project": True
        }
        response = requests.post(f'{self.server}/v2/json/get/projects_2/competitors', headers=self.headers, data=json.dumps(payload))

        with open(f'topvisor_data/competitors_{project_id}.json', "w", encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()

        return response.json()


    def get_project_positions_summary(self, project_id, region_index, dates):

        payload = {
            "project_id": project_id,
            "region_index": region_index,
            "dates": dates,
            "show_dynamics": True,
            "show_tops": True,
            "show_avg": True,
            "show_visibility": True
        }

        response = requests.post(f'{self.server}/v2/json/get/positions_2/summary', headers=self.headers,
                                 data=json.dumps(payload))

        with open(f'topvisor_data/summary_{project_id}_region_{region_index}_{dates}.json', "w", encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()

        return response.json()

    # def get_project_positions_summary_chart(self, project_id, region_index, dates):
    #


if __name__ == '__main__':

    project_id = 4944800
    yandex_region = 3
    google_region = 6
    dates = ['2022-01-31', '2022-02-07']
    tv = Topvisor()
    # tv.get_competitors(project_id)
    # tv.get_projects()
    # tv.get_region_indexes(project_id)

    print(tv.get_project_positions_summary(project_id, yandex_region, dates))
    print(tv.get_project_positions_summary(project_id, google_region, dates))
