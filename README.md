## XlsxReports  🐼 ➡️ 📊 📈

Create simple Excel reports from nested arrays or pandas DataFrame objects.

## Why? 🤔 💭 

Excel is usually the accepted way to present data to non-tech savvy clients. Pandas is the one of the best libraries for performing data computations. When you combine these things, you have a nice way to create simple and flexible automated Excel reports. 

## Features ✨ ✨ ✨

* Write individual DataFrame objects to worksheets
* Write many DataFrame objects to each tab
* Keep track of each tab and DataFrames on those tabs
* Write conditional formatting to specific tables
* Auto generate type formatting based on data types

## Getting Started 

_Coming soon .._

## Basic Usage 

```python
from reports import Writer, ReportFrame

data = ReportFrame(pandas.core.data.Dataframe) # create ReportFrame object
data.totals() # add totals row to ReportFrame object

writer = Writer("filename.xlsx", verbose=True)
writer.write("sheet", data)
writer.apply("sheet", "table 1", feature="conditional formatting", column="spend", type="data_bar")
writer.close()
```

## Testing 

You can run the available tests by executing:

```bash
pytest -v -s --test_filename="/tmp/your_test_write_file.xlsx"
```


