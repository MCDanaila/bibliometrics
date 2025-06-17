import datetime
import fcntl
import time
import zipfile as zf
from glob import glob
from typing import List
from typing import Optional
from typing import Set

import xmltodict
from rich import print
from rich.progress import track

from libbiblio.db.session import get_db
from libbiblio.sources.common import DB_Errors
from libbiblio.sources.common import error_to_db
from libbiblio.sources.scopus.scopus_parser import scopus_parser


def append_to_output(lines: List[str], output: str):
    """append to output file"""
    with open(output, "a") as f:
        # get an EXCLUSIVE LOCK to ensure that only one
        # process is writing to the file at a time
        fcntl.flock(f, fcntl.LOCK_EX)
        f.writelines(f"{line}\n" for line in lines)
        # release the lock
        fcntl.flock(f, fcntl.LOCK_UN)


def scopus_ingest_publication(
    xml_file: zf.ZipExtFile, *, dir_path: str, zip_name: str, xml_name: str
):
    try:
        data = xml_file.read()
        data = xmltodict.parse(data)
        db = next(get_db())
        publication, bibliography = scopus_parser(db, data)
        if publication:
            db.add(publication)
        if bibliography:
            for citation in bibliography:
                db.add(citation)
        db.commit()
    except DB_Errors as e:
        db.rollback()
        error_to_db(
            e,
            source="scopus",
            dir_path=dir_path,
            zip_name=zip_name,
            xml_name=xml_name,
        )


def scopus_ingest_xml(xml_name: str, dir_path: str):
    # CLI use only
    with open(f"{dir_path}/{xml_name}", mode="r") as xml_file:
        scopus_ingest_publication(
            xml_file,
            dir_path=dir_path,
            zip_name="",
            xml_name=xml_name,
        )


def scopus_ingest_zip(
    zip_name: str,
    dir_path: str,
    ingested: Optional[Set[str]] = None,
    output: Optional[str] = None,
):

    with zf.ZipFile(f"{dir_path}/{zip_name}", "r") as archive:
        xml_names = [
            xml_name
            for xml_name in archive.namelist()
            if xml_name.endswith(".xml")
        ]
        for xml_name in track(
            xml_names,
            description=zip_name,
            transient=True,
        ):
            if (not ingested) or (xml_name not in ingested):
                try:
                    with archive.open(xml_name, mode="r") as xml_file:
                        scopus_ingest_publication(
                            xml_file,
                            dir_path=dir_path,
                            zip_name=zip_name,
                            xml_name=xml_name,
                        )
                except DB_Errors as e:
                    error_to_db(
                        e,
                        source="scopus",
                        dir_path=dir_path,
                        zip_name=zip_name,
                        xml_name=xml_name,
                    )
            else:
                print(
                    f"Skipped [blue]{dir_path}/{zip_name} -> {xml_name}[/blue]"
                )
        if output:
            append_to_output([zip_name], output)


def scopus_ingest_dir(
    dir_path: str,
    ingested: Optional[Set[str]] = None,
    output: Optional[str] = None,
):
    # list of all xml files in `dir_path`
    glob_xml = [
        _xml[len(dir_path) + 1 :] for _xml in glob(f"{dir_path}/*.xml")
    ]
    # list of all zip files in `dir_path`
    glob_zip = [
        _zip[len(dir_path) + 1 :] for _zip in glob(f"{dir_path}/*.zip")
    ]

    # Ingest all the xml files in `dir_path`
    if glob_xml:
        now = datetime.datetime.now()
        print(
            (
                f"([green]{now.day:02}/{now.month:02}/{now.year}[/green] - "
                f"[green]{now.hour:02}:{now.minute:02})[/green] "
                f"[white]{dir_path}/[/white][bold green]*.xml[/bold green]"
            )
        )
        ingested_xml = []
        start = time.perf_counter()
        for xml_name in track(glob_xml, description=dir_path, transient=True):
            if (not ingested) or (xml_name not in ingested):
                try:
                    with open(f"{dir_path}/{xml_name}", mode="r") as xml_file:
                        scopus_ingest_publication(
                            xml_file,
                            dir_path=dir_path,
                            zip_name="",
                            xml_name=xml_name,
                        )
                    ingested_xml.append(xml_name)
                except DB_Errors as e:
                    error_to_db(
                        e,
                        source="scopus",
                        dir_path=dir_path,
                        xml_name=xml_name,
                    )
            else:
                print(f"Skipped [blue]{dir_path}/{xml_name}[/blue]")
        stop = time.perf_counter()
        if output:
            append_to_output(ingested_xml, output)
        print(f"⏱️  [red]{stop-start:.2f}s[/red]")

    # Ingest all the zip files in `dir_path`

    for zip_name in glob_zip:
        if (not ingested) or (zip_name not in ingested):
            try:
                now = datetime.datetime.now()
                print(
                    (
                        f"[green]({now.day:02}/{now.month:02}/{now.year}[/green]"
                        " - "
                        f"[green]{now.hour:02}:{now.minute:02})[/green] "
                        f"[white]{dir_path}/[/white][bold green]{zip_name}[/bold green]"
                    )
                )
                start = time.perf_counter()
                scopus_ingest_zip(
                    zip_name,
                    dir_path=dir_path,
                )
                if output:
                    append_to_output([zip_name], output)
                stop = time.perf_counter()
                print(f"⏱️  [red]{stop-start:.2f}s[/red]")
            except DB_Errors as e:
                error_to_db(
                    e,
                    source="scopus",
                    dir_path=dir_path,
                    zip_name=zip_name,
                )
        else:
            print(f"Skipped [blue]{dir_path}/{zip_name}[/blue]")
