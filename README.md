# MiniKF_example_pipeline
use miniKF to understand kubernetes and kubeflow concepts by creating a small pipeline

##### disclaimer

The following guide is prepared with the knowledge that I have gained, the information below may no be accurate

---

#### Installation

[intall in your machine](https://www.kubeflow.org/docs/started/getting-started-minikf/)

tips in case of failure

* make sure you have the latest virtualbox version
* try restarting the virtual environment (`vagrant reload`)
* `vagrant reload` may fail to do a fresh restart sometimes, in that case open virtualbox GUI and delete the VM manually
* make sure to upgrade miniKF as mentioned in the [installation page](https://www.kubeflow.org/docs/started/getting-started-minikf/)
* if miniKF keeps pending forever use `vagrant ssh` to check the log files (ex: provisions.log)

---

#### Quick Run

Follow this [guide](https://medium.com/kubeflow/an-end-to-end-ml-pipeline-on-prem-notebooks-kubeflow-pipelines-on-the-new-minikf-33b7d8e9a836) Just do the clicks! If you are lucky you will finish the guide in 5 minutes

##### what you just did?

let's create our own pipeline and understand better. keep reading

---

#### MinikF overview

minikF has following collaborators

* [JupyterLab](https://www.kubeflow.org/docs/components/jupyter/) - in the quick run we created a jupyter notebook server with specifications such as CPU,GPU,RAM and Volumes. This server is similar to a real cloud service like AWS/GCS. The volumes we have mounted on the server contain the training data that we want to use in the pipeline. We used the notebook's terminal which has [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/) and [Kubeflow Pipelines SDK] (https://www.kubeflow.org/docs/pipelines/sdk/sdk-overview/) commands.
* [Rok](https://www.arrikto.com/how-it-works/) - since miniKF runs locally the pipeline has no access to online resouces(trianing data). Hence we should create virtual volumes and pass them to the components at run time from where the components can read/write data. This makes it easy to define the components in the same file where the pipeline is defined. However this is not the ideal way to define a component. The [best practices](https://www.kubeflow.org/docs/pipelines/sdk/component-development/) for building components cannot be used when working with miniKF.

---

#### Building a Pipeline

##### Summary 

* Building a pipeline with three components. The first two components are ideal. Each of them has a text file as input and outputs to a file. The third component reads the two output files and concatenates the content.

##### Steps

* write python scripts implementing the given objective
* build docker containers to run the scripts - one container for one script
* host the docker images in a cloud
* define components followed by the pipeline in a python script
* compile the pipeline using Kubeflow Pipelines SDK
* Use Rok to get a snapshot of the data directory
* Upload and run the pipeline on miniKF
