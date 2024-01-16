* The reason there is a difference between rows in the excel file and the database entries for the factoryOnData is because there are
duplicate values in the excel file, so when creating the hash, the upsert skips those entries

* Pickling is the process where a Python object is converted into a byte stream. This is used to tests functions that import files and compare the result of the import function to a previously vetted result.
