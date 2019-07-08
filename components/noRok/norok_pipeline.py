import kfp
# import os
# component_root="/home/jovyan"
# Load the component by calling load_component_from_file or load_component_from_url
# To load the component, the pipeline author only needs to have access to the component.yaml file.
# The Kubernetes cluster executing the pipeline needs access to the container image specified in the component.
# dummy_op = kfp.components.load_component_from_file(os.path.join(component_root, 'component.yaml')) 
# dummy_op = kfp.components.load_component_from_url('http://....../component.yaml')

# dummy_op is now a "factory function" that accepts the arguments for the component's inputs
# and produces a task object (e.g. ContainerOp instance).
# Inspect the dummy_op function in Jupyter Notebook by typing "dummy_op(" and pressing Shift+Tab
# You can also get help by writing help(dummy_op) or dummy_op? or dummy_op??
# The signature of the dummy_op function corresponds to the inputs section of the component.
# Some tweaks are performed to make the signature valid and pythonic:
# 1) All inputs with default values will come after the inputs without default values
# 2) The input names are converted to pythonic names (spaces and symbols replaced
#    with underscores and letters lowercased).

def echo(input_file,
               step_name='echo_online_txt'):
    return kfp.dsl.ContainerOp(
        name=step_name,
        image='hiruna72/norok@sha256:9bd1a6b6129b6750335a685bbf839cca4b5b5b95c96a3ad634c79ceb41ffce0d',
        arguments=[
            '--input1-path', input_file,
        ],
        command=['python3', '/pipelines/component/src/noRok.py'],
    )


# Define a pipeline and create a task from a component:
@kfp.dsl.pipeline(name='My pipeline', description='')
def my_pipeline():
        
    compo1 = echo(
        input_file='https://www.w3.org/TR/PNG/iso_8859-1.txt')
    
if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(my_pipeline, 'norok_pipeline.tar.gz')