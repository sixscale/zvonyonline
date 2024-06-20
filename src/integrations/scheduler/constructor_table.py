from django.conf import settings

from .db_requests import get_active_project_titles, get_active_projects
from .formuls import (
    get_projects_formulas,
    get_projects_total_formulas,
    get_clients_total_formulas,
)
from ..services.google_sheets import google_sheets_api


def create_new_sheet_with_header(sheet_name: str):
    sheet_id = google_sheets_api.create_sheet_copy(
        settings.GS_LEADS_TABLE_ID,
        settings.GS_LEADS_HEADER_SHEET_ID,
    )
    google_sheets_api.update_sheet_property(settings.GS_LEADS_TABLE_ID, sheet_id, "title", sheet_name)
    google_sheets_api.update_sheet_property(settings.GS_LEADS_TABLE_ID, sheet_id, "index", "0")
    return sheet_id


def normalize_data(data_projects: list) -> dict[str, list[dict[str, str]]]:
    """
    Возвращает данные такого формата:
    {
        "client1": [{"project": "project_1", "scenario": "scenario_1"}, {"project": "project_2", "scenario": "scenario_2"}], 
        "client2": [{"project": "project_3", "scenario": "scenario_3"}, {"project": "project_4", "scenario": "scenario_4"}], 
    }
    """
    data_projects_new_format = {}
    for item in data_projects:
        if item["client"] in data_projects_new_format:
            data_projects_new_format[item["client"]].append({"project": item["project_title"], "scenario": item["scenario_title"]})
        else:
            data_projects_new_format[item["client"]] = [{"project": item["project_title"], "scenario": item["scenario_title"]}]
    return data_projects_new_format


def get_table_shift(data_projects_new_format: dict) -> int:
    total_projects = 0
    for project in data_projects_new_format.values():
        total_projects += len(project) + 1
    return google_sheets_api.START_CELL_NUM + total_projects + 1 + 2


def create_report_sheet(sheet_name: str):
    """
    создает новый лист на основе шаблона и заносит данные из прошлого диапазона
    :param sheet_name: имя листа
    """
    create_new_sheet_with_header(sheet_name)

    table_data = []

    data_projects_new_format = normalize_data(get_active_projects())

    start_cell = google_sheets_api.START_CELL_NUM
    list_for_total_overall = []
    for client, client_info in data_projects_new_format.items():
        for i, project in enumerate(client_info):
            current_client = ""
            if i == len(client_info) - 1:
                current_client = client
            table_data.append([current_client, project["project"]] + get_projects_formulas(int(start_cell + i), get_table_shift(data_projects_new_format)),)
        start_cell += len(client_info)
        # Вывод итого по клиенту
        table_data.append(get_projects_total_formulas(start_cell, get_table_shift(data_projects_new_format), len(client_info)))
        #     # TODO: заменить BC на AZ
        list_for_total_overall.append(f"{start_cell}")
        # Вывод клиента
        start_cell += 1
    table_data.append(get_clients_total_formulas(start_cell, list_for_total_overall, get_table_shift(data_projects_new_format)))
    google_sheets_api.write_to_google_sheet(
        table_data,
        settings.GS_LEADS_TABLE_ID,
        sheet_name,
        f"A{google_sheets_api.START_CELL_NUM}",
    )

    google_sheets_api.write_to_google_sheet(
        previous_table_constructor(start_cell, list_for_total_overall, sheet_name, data_projects_new_format, client_info),
        settings.GS_LEADS_TABLE_ID,
        sheet_name,
        f"A{start_cell + 2}",
    )

def previous_table_constructor(start_cell, list_for_total_overall, sheet_name, data_projects_new_format, client_info):
    active_titles = get_active_project_titles()
    prev_data = google_sheets_api.get_table_data(
        settings.GS_LEADS_TABLE_ID,
        sheet_name,
        f"A8:AZ{start_cell}",
    )
    get_table_header = google_sheets_api.get_table_data(
        settings.GS_LEADS_TABLE_ID,
        sheet_name,
        f"A1:AW7",
    )
    previous_table_constructor_data = []
    for line in get_table_header:
        previous_table_constructor_data.append(line)

    for line in prev_data:
        current_project = line[1]
        if current_project in active_titles:
            line = list(filter(lambda x: x[1] == current_project, prev_data))[0]
            previous_table_constructor_data.append(line)
        elif 'Итого:' or 'Итого по всем:' in line:
            if 'Итого по всем:' in line:
                previous_table_constructor_data.append(get_clients_total_formulas(start_cell, list_for_total_overall, get_table_shift(data_projects_new_format)))
            else:
                previous_table_constructor_data.append(get_projects_total_formulas(start_cell, get_table_shift(data_projects_new_format), len(client_info)))
        else:
            previous_table_constructor_data.append([0])
    
    return previous_table_constructor_data

    # Вывод итого по всем клиентам будет ниже, вне цикла
