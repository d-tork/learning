# Data Engineering

## from _97 Things Every Data Engineer Should Know_
Safari book

### 13. Column Names as Contracts
* `ID` : Integer. Non-null. Unique identifier for an entity. Likely a primary key. 
* `IND` : Binary. Non-null. Indicator of an event occurrence.
* `N` : Integer. Non-null. Non-negative count of quantity of event occurrences.
* `AMT` : Numeric. Summable, continuous “denominator-free” amount.
* `VAL` : Numeric. Not inherently summable (e.g., a rate, ratio, latitude, or longitude).
* `DT` : Date. Always in YYYY-MM-DD form.
* `TM` : Timestamp.

> The second level might characterize the _subject_ of the measure, such as a `DRIVER, RIDER, TRIP,
> ORIG,` or `DEST`. Additional levels would provide "adjectives" to modify the measure objects. For
> example, we might have `CITY, ZIP, LAT,` and `LON.`

Metadata management and data discoverability tasks can be partially automated by reconstructing 
variable definitions from stubs. Similarly, you can perform automated data-validation checks 
("everything that starts with `DT` should be cast as a date," "nothing in `AMT` fields should be 
a decimal").

### 16. Data Engineering != Spark
A data pipeline needs components from three general types of technologies:
* Computation
* Storage
* Messaging

> _Data Engineering = Computation + Storage + Messaging + Coding + Architecture + 
> Domain Knowledge + Use Cases_

Left off at 32
