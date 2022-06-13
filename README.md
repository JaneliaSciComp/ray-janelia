# ray-janelia

These scripts let you run [Ray](https://github.com/ray-project/ray) on the Janelia cluster (and maybe other LSF clusters).

You must have a Conda environment with [Ray installed](https://docs.ray.io/en/latest/ray-overview/installation.html).


## Create a cluster

This command will start a 20 slot cluster, using a conda environment called `ray-python`:

```bash
ray-janelia/ray-launch.sh -n 20 -e ray-python
```

By default, the cluster will be divided into nodes of 4 slots each. To use a different tiling, specify the number of nodes you want with `-d <nodes>`.

This command will start a cluster with 20 CPU and 2 GPU slots on a GPU enabled queue `gpu_queue`:

```bash
ray-janelia/ray-launch.sh -n 20 -e ray-python -b "-q gpu_queue -gpu num=2"
```

## Run a job on a cluster

The output of launching the cluster above will print a remote address like `ray://head_node:10001`. You can simply pass this address into your job when creating your Ray client, like this:

```python
ray.init(address="ray://head_node:10001")
```

The output will also print the address of the [Ray dashboard](https://docs.ray.io/en/latest/ray-core/ray-dashboard.html) for the launched Ray cluster.

## Create a cluster, run a job, then shut it down

Another option is to create a cluster and run a python job with a single command:

```bash
./ray-launch.sh -n 20 -e ray-python -p "/path/to/job.py --options"
```

In this case, to connect to the Ray cluster created with the `ray-launch.sh` script, the python script `job.py` should contain:

```python
ray.init(address="auto")
```

When the python script completes, the Ray cluster will be automatically shut down and the Janelia cluster job will be terminated.
