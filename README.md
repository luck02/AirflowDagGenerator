# AirflowDagGenerator
Add standards and tags to allow for the generation of DAGS based on parsing annotations and tags in python comments or annotations.  

## Goal:
* Writing DAGs independent from your pipeline jobs is a horrible development experience and ultimately your DAGS are probably cross domain so
it's hard to keep them sorted and logical.
* We want to add annotations to the raw python code of the format:
In module 'a':
```python
@dependency:database:origin_schema.table
#dependency:database:origin_schema.table")
def get_source_data(etc: etc):
  #select * from schema.table
  
  
@sink:s3:bucket/path
def write_to_destination(values: val):
  #val.write_to_s3('s3a://bucket/path')
```

In module 'b':
```python
@dependency:s3:bucket/path
def get_data():
    data = s3Reader('s3a://bucket/path')


@sink:database:destination_schema.table
def save_data(values: val):
    values.write.jdbc("destination_schema.table")
```

On consuming this file you'd end up with a dag structure that looks like this:
```yaml

DAG:
    dependencies:
    - module_a:
      module_b: database:origin_schema.table
    - module_b:
      module_a: s3:bucket/path
SOURCES:
    module_a:
    - database.origin_schema.table
    module_b:
    - s3.bucket.path
SINKS:
    module_a:
    - s3.bucket.path
    module_b:
    - database.destination_schema.table

```

### Assumptions:
* We may have to be opinionated for generating dags.
* I don't think python package semantics are effective for determining how dags are layed out.
  We will start with assuming that the tool will get called on a directory and any subdirectories
  will be scanned for annotations that could be used to generate a dag.
* Each subdirectory will be considered a pipeline job.
```bash 
  ./ # is project root
  ./job_a/code.py # everything in ./job_a will be interpreted as a single job.  
  ./job_a/other_code.py # will be intrepeted as being part of ./job_a
  ./job_b/code.py # As above except will be generated as belonging to job_b
``` 
* If another more skilled pythonista has a suggestion for how to decompose this kind of structure
I'm all ears.
* We will only be interpreting python code at this stage.

### Process:
* Traverse a source tree: For each subdirectory:
  * Process subdirectory, assume each subdirectory is a standalone pipeline.
  * Build up a list of sources and sinks.
  * Additional metadata could include:
    * Schedule.
    * Pass through metadata (compute resources?)
  * Generate a DAG for interproject dependencies (presumably in YAML or some easy to read format)
    * DAG should include dependencies between JOBS
  * Generate a set of unmet dependencies.
    * IE job_a depends on a table that isn't defined within this job.
* At a single project level you'd end up with
  * An artifact that we will call a 'project dag' 
    * This artifact will contain all dependencies within the project 
      expressed as a depends on b etc.
  * A list of unmet dependencies.
    * These would either be met in another project or they would be dependencies
    that are met outside of the current context (IE another whole DAG)
  * A list of unused resources.
* The next stage would be to run the tool on a collection of 'project dags'.
  * The list of unused resources from the individual dags will be matched with the list of 
  unmet dependencies.
  * We will generate a further set of 'final dags' from this data which will include 
  references to the source for all known sources and sinks.
  * We will generate a final list of all dependencies without sinks
  * We will generate a final list of all sinks without dependencies
* Each stage of the process will be expected to throw an error if:
  * The same sink is defined more than once.

## Usage:
* Create jobs and decorate sources and sinks.
* Create tests that determine correct wiring at each level.  IE if jobs have internal wiring:
  * IE compute / load steps then a test should be created asserting that those are wired together properly
  * At the project level a test that asserts correct wiring within the project.
  * At the cross project layer we are leaving that undefined, this is not a satisfactory state of affairs.
* Local development may or may not make use of DAGs.  It should be running tests.
* CI should be generating dags and executing tests.
* When a project is deployed the DAG artifacts should be uploaded to Airflow for execution.
* One potential pattern for integrating this would be to maintain a list of unused sources and sinks.
* When CI generates a new document that includes a new source / sink that is unused it should trigger a warning.

## Open questions:
* The testing pattern seems potentially questionable, if we're defining how the DAG ought to look in tests then
why not just use that as the source of truth?  
* Can we leverage this: https://github.com/rambler-digital-solutions/airflow-declarative
* Presumably we want to be able to pass through variables to the underlying DAG / operator.
  * We could provide a syntax that allows for pass through IE something that looks like this:
```python
@dag:passthrough: """
compute_cpu = 2
compute_ram = 12
operator: kubernetes_operator
"""
```
