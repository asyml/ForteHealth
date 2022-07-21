"""
this file defines sqlite3 related utils for inserting data to
the database of stave.
"""
import json
from typing import List
import sqlite3
import yaml
from stave_backend.lib.stave_session import StaveSession
from forte.common import Config


def sqlite_insert(conn, table, row):
    """
    Args:
        conn: connection
        table: table name
        row: inserted item
    """
    cols: str = ", ".join('"{}"'.format(col) for col in row.keys())
    vals: str = ", ".join(":{}".format(col) for col in row.keys())
    sql: str = f'INSERT INTO "{table}" ({cols}) VALUES ({vals})'
    cursor = conn.cursor()
    cursor.execute(sql, row)
    conn.commit()
    return cursor.lastrowid


def create_links(url_stub: str, ids: List[int]) -> List[str]:
    """
    Args:
        url_stub: url of stave
        ids: the doc ids of the reports
    """
    links: List[str] = []

    url_stub: str = url_stub.strip("/")
    for temp_idm in ids:
        links.append(
            f"<a href={url_stub}/documents/{temp_idm}><font size='6'>Report #{temp_idm}</font></a>"
        )
    return links


def get_json(path: str):
    """
    Args:
        path: the file path of the json file
    """
    file_obj = open(path)
    data = json.load(file_obj)
    file_obj.close()
    return data


def update_stave_db(default_project_json, config):
    """
    Args:
        default_project_json: the ontology configuration file
        config: the configuration of Stave, including url, name, password, etc.
    """
    project_id_base = 0
    with StaveSession(url=config.Stave.url) as session:
        session.login(username=config.Stave.username, password=config.Stave.pw)

        projects = session.get_project_list().json()
        project_names = [project["name"] for project in projects]

        if default_project_json["name"] in project_names:

            base_project = [
                proj
                for proj in projects
                if proj["name"] == default_project_json["name"]
            ][0]
            return base_project["id"]

        resp1 = session.create_project(default_project_json)
        project_id_base = json.loads(resp1.text)["id"]

        config = yaml.safe_load(open("stave_config.yml", "r"))
        config = Config(config, default_hparams=None)
        con = sqlite3.connect(config.Stave.stave_db_path)

        cursorObj = con.cursor()
        cursorObj.execute(
            f"SELECT ontology, config FROM stave_backend_project WHERE id = {project_id_base}"
        )
        results = cursorObj.fetchall()
        onto = results[0][0]
        conf = results[0][1]

        onto_new = onto.replace("'", '"')
        conf_new = (
            conf.replace("'", '"').replace("True", "true").replace("False", "false")
        )

        cursorObj.execute(
            "UPDATE stave_backend_project SET ontology ='"
            + onto_new
            + f"' WHERE id = {project_id_base}"
        )
        cursorObj.execute(
            "UPDATE stave_backend_project SET config ='"
            + conf_new
            + f"' WHERE id = {project_id_base}"
        )

        con.commit()

    return project_id_base
