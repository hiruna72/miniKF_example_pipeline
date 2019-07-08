import kfp
import os
component_root="/home/jovyan/src"
# Load the component by calling load_component_from_file or load_component_from_url
# To load the component, the pipeline author only needs to have access to the component.yaml file.
# The Kubernetes cluster executing the pipeline needs access to the container image specified in the component.
echo = kfp.components.load_component_from_file(os.path.join(component_root, 'component.yaml')) 
# dummy_op = kfp.components.load_component_from_url('http://....../component.yaml')

# Define a pipeline and create a task from a component:
@kfp.dsl.pipeline(name='My pipeline', description='')
def my_pipeline():
        
    compo1 = echo(
        input_1_uri='https://www.w3.org/TR/PNG/iso_8859-1.txt')
    
if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(my_pipeline, 'norok_reusable_compo_pipeline.tar.gz')