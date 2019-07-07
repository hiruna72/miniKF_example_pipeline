# MiniKF_example_pipeline
use miniKF to understand kubernetes and kubeflow concepts by creating a small pipeline

##### disclaimer

The following guide is prepared with what I have learnt using MiniKF, the content below may no be accurate.


#### Installation

[intall in your machine](https://www.kubeflow.org/docs/started/getting-started-minikf/)

tips in case of failure

* make sure you have the latest virtualbox version
* try restarting the virtual environment (`vagrant reload`)
* `vagrant reload` may fail to do a fresh restart sometimes, in that case open virtualbox GUI and delete the VM manually
* make sure to upgrade miniKF as mentioned in the [installation page](https://www.kubeflow.org/docs/started/getting-started-minikf/)
* if miniKF keeps pending forever use `vagrant ssh` to check the log files (ex: provisions.log)


#### Quick Run

Follow this [guide](https://medium.com/kubeflow/an-end-to-end-ml-pipeline-on-prem-notebooks-kubeflow-pipelines-on-the-new-minikf-33b7d8e9a836) Just do the clicks! If you are lucky you will finish the guide in 5 minutes

##### what you just did?

let's create our own pipeline and understand better. keep reading


#### MinikF overview

minikF has following collaborators

* [JupyterLab](https://www.kubeflow.org/docs/components/jupyter/) - in the quick run we created a jupyter notebook server with specifications such as CPU,GPU,RAM and Volumes. This server is similar to a real cloud service like AWS/GCS. The volumes we have mounted on the server contain the training data that we want to use in the pipeline. We used the notebook's terminal which has [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/) and [Kubeflow Pipelines SDK](https://www.kubeflow.org/docs/pipelines/sdk/sdk-overview/) commands.
* [Rok](https://www.arrikto.com/how-it-works/) - since miniKF runs locally the pipeline has no access to online resouces(trianing data). Hence we should create virtual volumes and pass them to the components at run time from where the components can read/write data. This makes it easy to define the components in the same file where the pipeline is defined. However this is not the ideal way to define a component. The [best practices](https://www.kubeflow.org/docs/pipelines/sdk/component-development/) for building components cannot be used when working with miniKF.


#### Building a Pipeline

##### Summary 

* Building a pipeline with three components. The first two components are ideal. Each of them has a text file as input and outputs to a file. The third component reads the two output files and concatenates the content.

![pipeline](https://github.com/hiruna72/miniKF_example_pipeline/blob/master/small_pipeline.png)

##### Steps

Step number 1,2 & 3 are optional as the docker images are already hosted in docker hub. To learn how to build and host docker images read [Docker images](#docker-images)

1. write python scripts implementing the given objective https://github.com/hiruna72/miniKF_example_pipeline/tree/master/python_scripts
2. build docker containers to run the scripts - one container for one script
3. host the docker images in a cloud
4. define components and the pipeline in a python script https://github.com/hiruna72/miniKF_example_pipeline/blob/master/small_pipeline.py
5. compile the pipeline using Kubeflow Pipelines SDK https://github.com/hiruna72/miniKF_example_pipeline/blob/master/small_pipeline.tar.gz
6. Use Rok to get a snapshot of the data directory (copy [this content](https://github.com/hiruna72/miniKF_example_pipeline/tree/master/data) to the data volume of the notebook server)
7. Upload and run the pipeline on miniKF

#### Docker Images

Once you have the Dockerfile ready easiest way to build and host docker image is to use a bash script. In the following example `dockerhubusername` should be set 

```bash
docker login --username ${dockerhubusername}
image_name_1=${dockerhubusername}/multiplier # Specify the image name here
image_tag_1=multiplier
full_image_name_1=${image_name_1}:${image_tag_1}
base_image_tag_1=1.12.0-py3

docker build --build-arg BASE_IMAGE_TAG=${base_image_tag_1} -t "${full_image_name_1}" .
docker push "$full_image_name_1"
docker inspect --format="{{index .RepoDigests 0}}" "${full_image_name_1}"
```

`docker inspect` command outputs a hash link to the hosted image. This should be used when [defining components](https://github.com/hiruna72/miniKF_example_pipeline/blob/2629e0aab48c82dd925e763a608f1ef1a1c1da43/small_pipeline.py#L27)

