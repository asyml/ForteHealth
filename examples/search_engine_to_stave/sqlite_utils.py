from typing import Dict, Any, Optional, List
from stave_backend.lib.stave_session import StaveSession
import json


def sqlite_insert(conn, table, row):
    cols: str = ", ".join('"{}"'.format(col) for col in row.keys())
    vals: str = ", ".join(":{}".format(col) for col in row.keys())
    sql: str = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    cursor = conn.cursor()
    cursor.execute(sql, row)
    conn.commit()
    return cursor.lastrowid


def create_links(url_stub: str, ids: List[int]) -> List[str]:
    links: List[str] = []

    url_stub: str = url_stub.strip("/")
    for temp_idm in ids:
        links.append(
            f"<a href={url_stub}/documents/{temp_idm}><font size='6'>Report #{temp_idm}</font></a>"
        )
    return links


def get_json(path: str):
    file_obj = open(path)
    data = json.load(file_obj)
    file_obj.close()
    return data


def update_stave_db(default_project_json, config):
    project_id_base = 0
    with StaveSession(url=config.Stave.url) as session:
        session.login(username=config.Stave.username, password=config.Stave.pw)

        projects = session.get_project_list().json()
        project_names = [project["name"] for project in projects]

        if (
            default_project_json["name"] in project_names
            ):

            base_project = [
                proj
                for proj in projects
                if proj["name"] == default_project_json["name"]
            ][0]
            return base_project["id"]

        resp1 = session.create_project(default_project_json)
        project_id_base = json.loads(resp1.text)["id"]

        # project_list = session.get_project_list().json()

    return project_id_base
