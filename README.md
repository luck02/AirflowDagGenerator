# AirflowDagGenerator
Add standards and tags to allow for the generation of DAGS based on parsing annotations and tags in python comments or annotations.  

## Goal:
* Writing DAGs independent from your pipeline jobs is a horrible development experience and ultimately your DAGS are probably cross domain so
it's hard to keep them sorted and logical.
* We want to add annotations to the raw python code of the format:
```
@source:database:schema.table
def get_source_data(etc: etc):
  select * from schema.table
  
  
@destination:s3:bucket/path
def write_to_destination(values: val)
  val.write_to_s3('s3a://bucket/path')
```

On consuming this file you'd end up with a dag structure that looks like this:
