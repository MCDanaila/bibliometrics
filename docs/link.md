This command requires a technical explanation to understand its usefulness.

Citation tables have two foreign keys: the _citing_ paper id and the _cited_ paper id.
When we ingest a publication, we certainly have the _citing id_ (i.e. the id of the publication we are ingesting) but the _cited id_ we have may not correspond to the id of any of the publications ingested so far.<br>
This will cause an `IntegrityError` problem.

To overcome this problem, we introduced the tables `NotLinkedScopusCitation` and `NotLinkedWoSCitation`.
These tables are identical to the original ones, the only difference being that no Foreign Key constriant is imposed.

This allows us to ingest all the data without any problems while leaving the quotations in a `NotLinked` state, and this is where the `link` command comes in.

By running
```console
$ poetry run biblio scopus link
```
or
```console
$ poetry run biblio wos link
```
the link process will start.

Bibliometric will turn `NotLinkedCitation`s into regular `Citation`s whenever possible, also taking care of deleting `NotLinked` that have been converted.
