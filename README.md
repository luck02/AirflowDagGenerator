# More thoughts:  Airflow is a hairball.

Maybe a better idea is to start fresh with a k8s native scheduler/ dag traversal tool
Things in the space: 
* https://github.com/kubeflow/kubeflow
  * Not really a direct comparison, but super close... Has notion of a pipeline, but looks like it's married to ML pipelines, however maybe that's one and the same for ETL style work.
  * The docs really want to make it sound like a tool to productionize your ML learning workflows.
    * https://www.kubeflow.org/docs/pipelines/build-component/ every second word is ML related.
* Obviously airflow: https://github.com/apache/airflow
  * There's literally no standard airflow docker image (wow)
  * The code and processing model appears to be a hairball.
    * Scheduler / UI / Persistence notions are muddled together (last I looked)
    * The operators are known for being difficult.
    * The only 'safe' operators are 'generic' operators (if we use it that's what we'll do).
    * Cross dag dependency is a challenge.
  * Questionable HA configuration.  
    * Multiple web servers ok
    * Multiple executors are fine.
    * One scheduler / DB.  HA isn't possible to the best of my knowledge.
  * TLDR lots of moving parts, tons of configs etc.  IT's a standard monolithic project after 5+ years of development.
* Luigi:
  * 
  
Axis of comparison:
* Incremental updates:
  * initial thoughts are:  Let this be an executor agent concern, if you want an incremental process then bake it into your executor.
  * We could add primitives: For a given executor, here's a set of time buckets to be handed in per execution, probably not super complex.
* Partial Recomputes
  * Initial thoughts are let the execution handle this, detecting when to recompute isn't a trivial task and will probably need either a nuclear option (recompute on every change) or very manual steps etc.
* Dependency chains:
  * find a DSL for DAG's that supports our required primitives or invent one. 
    * A DAG is 
    <code>
    job --> job --> job --> job --> job  
        --> job --> job --> job -->  ^  
      ^ -->  ^  --> job ---------->  ^  
   </code>
    * primitives are:
      * DAG 
        * Schedule
        * unit of execution
        * Maybe target / artifact
* Scheduler:
  * Nothing fancy here, could be cron
* Monitoring and notifications:
  * Could be a first class notion.
    * event on:
      * Dag started
        * Job started.
        * Job completed.
        * Job errored
      * Dag completed
      * Cron event fired
* Development mode:
  * More of a challenge, but workable.  
  * Most desktops have a suitable desktop k8s available
    * That includes a cron notion
    * Basically everything we need, this should be pretty lightweight.
* Deployment:
  * CI level concern:
    * On build, executed artifact is a container image.
      * Container image is pushed to repository.
    * Any other bits of pipeline are executed (secrets are validated / uploaded etc)
    * DAG is validated and pushed to server
    * Server runs basic validity checks:
      * Does the DAG have any dependencies that are unmet? if so fail
        * IE does it have a container image:tag that doesn't exist.  Does it reference secrets / env's that don't exist.
  * We'll probably want a way to signify that this is a breaking change for incremental in order to automate that process.  IT'll be messy.
  
Core components:
* Scheduler API
  * GET/SET schedules and dags.
    * Literally is a backend for storing k8s cron jobs.
    * Give me a list of cron jobs.
    * Here's a new cron job
    * Probably needs to some sanity checking on new jobs.
    * Remove this job.
* Executor
  * k8s cron job:
    * Has a DAG, k8s is the scheduler.
    * Is a shell executor, just creates pods that represent the DAG.
    * Traverse DAG, execute nodes, monitor job progress, Retry on failure etc.
    * Spits out events for collection into backend.
    * On starting we tell the orchestrator what we're doing and each step.  
    * We have a execution-instance-id
      * we can use that to recover current state, if my pod goes away I'll 
* Orchestrator
  * Consumes all events.
  * Maintains views.
  * Needs a stable reliable storage.
    
