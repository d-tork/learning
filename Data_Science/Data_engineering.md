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

### Give Data Products a Frontend with Latent Documentation
Emily Riederer

> Many of the artifacts that data consumers want can be created with little to no incremental 
> effort if engineers embrase **latent documentation**: systematically documenting their own thought 
> processes and decision making during the engineering process in a way that can be easily 
> shared with and interpreted by users.

* Generate a data dictionary while gathering user requirements.
* Utilize a hierarchical variable-naming taxonomy. 
	- e.g., `ENTITY_ATTRIBUTE_DESCRIPTOR_TYPE`
	- taxonomy can both help encode metadata so users interpret field names and intent correctly,
	and make it easier to program on top of data (e.g. by selecting all fields containing certain
	common "stubs")
* Publicly answer user questions in a FAQ.
	- _passive documentation_ is answering user questions in public forums like Slack or GitHub 
	instead of private channels such as direct messages to create a permanent record
* Visualize the data pipeline
* Share your expectations and quality checks. 
	- these tools (like Great Expectations) can not only help validate data and catch errors, but
	also force you to more clearly articulate how you intend the data to behave

### Know the Value per Byte of your Data
Dhruba Borthakur

**cost-per-byte**: total dataset size divided by the cost of storage

**value per byte**: how much value is each byte providing to the business (a better metric than
cost, since costs are so low now)

> If a query touches one specific byte of data, the value for that bute is 1. If a specific byte
> is not touched by any query, the value of that byte is 0. I compute my value per byte as the
> percentage of unique bytes that were used to serve any query. 

### Learn to use a NoSQL database, but not like an RDBMS
Kirk Kirkconnell

NoSQL databases are for fast, pre-computed queries, views, and application access patterns. 
Traditional databases are for transactions, rigid schemas, and exploration/querying (OLAP).

> NoSQL databases perform and scale best when your schema is designed to model the application's
> access patterns, the frequency with which those patterns are called, and the velocity of access.
> The goal should be to precompute the answers to these access patterns, and only rarely ask 
> questions of the data (ad hoc querying). 
