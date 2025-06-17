import datetime
import fcntl
import gzip
import time
import zipfile as zf
from glob import glob
from typing import List
from typing import Optional
from typing import Set

import xmltodict
from devtools import debug
from lxml import etree
from rich import print
from rich.progress import track

from libbiblio.db.session import get_db
from libbiblio.sources.common import DB_Errors
from libbiblio.sources.common import error_to_db
from libbiblio.sources.wos.wos_parser import wos_parser

TAG = "{http://clarivate.com/schema/wok5.30/public/FullRecord}REC"


def append_to_output(lines: List[str], output: str):
    """append to output file"""
    with open(output, "a") as f:
        # get an EXCLUSIVE LOCK to ensure that only one
        # process is writing to the file at a time
        fcntl.flock(f, fcntl.LOCK_EX)
        f.writelines(f"{line}\n" for line in lines)
        # release the lock
        fcntl.flock(f, fcntl.LOCK_UN)


def wos_ingest_publication(
    publication, *, dir_path: str, zip_name: str, xml_name: str
):
    try:
        data = xmltodict.parse(etree.tostring(publication))
        db = next(get_db())
        publication, bibliography = wos_parser(db, data["REC"])
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
            source="wos",
            dir_path=dir_path,
            zip_name=zip_name,
            xml_name=xml_name,
        )


def wos_ingest_zip(
    zip_name: str,
    dir_path: str,
    ingested: Optional[Set[str]] = None,
    output: Optional[str] = None,
):
    with zf.ZipFile(f"{dir_path}/{zip_name}", "r") as archive:
        xmlgz_names = [
            xmlgz_name
            for xmlgz_name in archive.namelist()
            if xmlgz_name.endswith(".xml.gz")
        ]
        for xmlgz_name in track(
            xmlgz_names,
            description=zip_name,
            transient=True,
        ):
            if (not ingested) or (xmlgz_name not in ingested):
                try:
                    with archive.open(xmlgz_name, mode="r") as xmlgz_file:
                        with gzip.GzipFile(
                            fileobj=xmlgz_file, mode="r"
                        ) as xml_file:
                            record_el_iterator = etree.iterparse(
                                xml_file, tag=TAG
                            )
                            for _, record_el in record_el_iterator:
                                wos_ingest_publication(
                                    record_el,
                                    dir_path=dir_path,
                                    zip_name=zip_name,
                                    xml_name=xmlgz_name,
                                )
                                # https://stackoverflow.com/questions/12160418/
                                record_el.clear()
                            del record_el_iterator
                except DB_Errors as e:
                    error_to_db(
                        e,
                        source="wos",
                        dir_path=dir_path,
                        zip_name=zip_name,
                        xml_name=xmlgz_name,
                    )
            else:
                print(
                    f"Skipped [blue]{dir_path}/{zip_name} -> {xmlgz_name}[/blue]"
                )
        if output:
            append_to_output([zip_name], output)


def wos_ingest_dir(
    dir_path: str,
    ingested: Optional[Set[str]] = None,
    output: Optional[str] = None,
):
    # list of all xml files in `dir_path`
    glob_xmlgz = [
        _xml[len(dir_path) + 1 :] for _xml in glob(f"{dir_path}/*.xml.gz")
    ]
    # list of all zip files in `dir_path`
    glob_zip = [
        _zip[len(dir_path) + 1 :] for _zip in glob(f"{dir_path}/*.zip")
    ]

    # Ingest all the xml.gz files in `dir_path`
    if glob_xmlgz:
        now = datetime.datetime.now()
        print(
            (
                f"([green]{now.day:02}/{now.month:02}/{now.year}[/green] - "
                f"[green]{now.hour:02}:{now.minute:02})[/green] "
                f"[white]{dir_path}/[/white][bold green]*.xml[/bold green]"
            )
        )
        ingested_xmlgz = []
        start = time.perf_counter()
        for xmlgz_name in track(
            glob_xmlgz, description=dir_path, transient=True
        ):
            if (not ingested) or (xmlgz_name not in ingested):
                try:
                    with open(xmlgz_name, mode="r") as xmlgz_file:
                        with gzip.GzipFile(
                            fileobj=xmlgz_file, mode="r"
                        ) as xml_file:
                            wos_ingest_publication(
                                xml_file,
                                dir_path=dir_path,
                                zip_name=zip_name,
                                xml_name=xmlgz_name,
                            )
                except DB_Errors as e:
                    error_to_db(
                        e,
                        source="wos",
                        dir_path=dir_path,
                        zip_name=zip_name,
                        xml_name=xmlgz_name,
                    )
            else:
                print(f"Skipped [blue]{dir_path}/{xmlgz_name}[/blue]")
        stop = time.perf_counter()
        if output:
            append_to_output(ingested_xmlgz, output)
        print(f"⏱️  [red]{stop-start:.2f}s[/red]")

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
                wos_ingest_zip(
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
                    source="wos",
                    dir_path=dir_path,
                    zip_name=zip_name,
                )
        else:
            print(f"Skipped [blue]{dir_path}/{zip_name}[/blue]")
