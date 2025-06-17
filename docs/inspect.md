Another useful CLI command is `inspect`.

Here, too, we have two cases
```console
$ poetry run biblio scopus inspect
```
and
```console
$ poetry run biblio wos inspect
```

This command prints out a summary of the current state of the DB.<br>
For example
```console
$ poetry run biblio scopus inspect

ScopusSource             :         32
NotLinkedScopusCitation  :       5201
ScopusPublication        :        165
ScopusCitation           :          0
ScopusAuthorship         :        335
ScopusAffiliation        :        198
ScopusAuthor             :        136

IngestionLog             :          0
```

This command can also be used while there are ongoing ingestion processes, to monitor their progress.
