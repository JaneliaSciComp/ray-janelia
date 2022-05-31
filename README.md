# ray-janelia

These scripts let you run Ray on the Janelia cluster (and maybe other LSF clusters).

You must have a Conda environment with [Ray installed](https://docs.ray.io/en/latest/ray-overview/installation.html).


## Create a cluster

This command will start a 20 slot cluster, using a conda environment called `ray-python`:

```bash
ray-janelia/ray-launch.sh -n 20 -e ray-python"
```

By default, the cluster will be divided into nodes of 4 slots each. To use a different tiling, specify the number of nodes you want with `-d <nodes>`.


## Run a job on a cluster

The output of launching the cluster above will print a remote address like `ray://head_node:10001`. You can simply pass this address into your job when creating your Ray client, like this:

```python
ray.init("ray://head_node:10001")
```


## Create a cluster, run a job, then shut it down

```bash
./ray-launch.sh -n 20 -e ray-python -p "/path/to/job.py --options"
```


