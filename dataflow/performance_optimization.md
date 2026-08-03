1. Reduce unnecessary shuffles->use filter before using group by
2. Use Combine instead of GroupByKey
3. Increase Parallelism ->write inside the options regarding max workers
4. Avoid expensive operations in process() ->don't keep connections inside the process. Connections should be inside the setup
5. Use Batch Writes
