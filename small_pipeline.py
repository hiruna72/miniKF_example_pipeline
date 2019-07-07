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

def multiply(input_file, multiplier,
               output_uri, output_uri_in_file,
               volume,
               step_name='multiply',
              mount_output_to='/data'):
    return kfp.dsl.ContainerOp(
        name=step_name,
        image='hiruna72/multiplier@sha256:3016c55dcb8015ef9b457dce839206b5704afacd71a42a688132569d97684f99',
        arguments=[
            '--input1-path', input_file,
            '--param1', multiplier,
            '--output1-path', output_uri,
            '--output1-path-file', output_uri_in_file,
        ],
        command=['python3', '/pipelines/component/src/multiplier.py'],
        file_outputs={
            'output_file': output_uri,
            'output_uri_in_file': output_uri_in_file,
        },
        pvolumes={mount_output_to: volume}
    )

def concatenate(input_file1, input_fi1e2,
               output_uri, output_uri_in_file,
               volume,
               step_name='concat',
              mount_output_to='/data'):
    return kfp.dsl.ContainerOp(
        name=step_name,
        image='hiruna72/concatenate@sha256:2119c2f95d5b65eb02cfca29dbbe6d8d9c1e61d900498ae45381ed9e28b0e48c',
        arguments=[
            '--input1-path', input_file1,
            '--input2-path', input_fi1e2,
            '--output1-path', output_uri,
            '--output1-path-file', output_uri_in_file,
        ],
        command=['python3', '/pipelines/component/src/concat.py'],
        file_outputs={
            'output_file': output_uri,
            'output_uri_in_file': output_uri_in_file,
        },
        pvolumes={mount_output_to: volume}
    )


# Define a pipeline and create a task from a component:
@kfp.dsl.pipeline(name='My pipeline', description='')
def my_pipeline(
        rok_url,
        pvc_size='1Gi'):
    
    vop = kfp.dsl.VolumeOp(
        name='create-volume',
        resource_name='helloPipeline_data',
        annotations={"rok/origin": rok_url},
        size=pvc_size
    )
    
    compo1 = multiply(
        input_file='/data/input_compo1.txt',
        multiplier=7,
        output_uri='/data/output_compo1.txt',
        output_uri_in_file='/data/output_compo1_uri.txt',
        volume=vop.volume
    )
    
    compo2 = multiply(
        input_file='/data/input_compo2.txt',
        multiplier=7,
        output_uri='/data/output_compo2.txt',
        output_uri_in_file='/data/output_compo2_uri.txt',
        volume=vop.volume
    )
    
#     compo3 = concatenate(
#         input_file1='/data/input_compo1.txt',
#         input_file2='/data/input_compo2.txt',
#         output_uri='/data/output_compo3.txt',
#         output_uri_in_file='/data/output_compo3_uri.txt',
#         volume=vop.volume
#     )
    
    compo3 = concatenate(
        input_file1=compo1.outputs['output_uri_in_file'],
        input_fi1e2=compo2.outputs['output_uri_in_file'],
        output_uri='/data/output_compo3.txt',
        output_uri_in_file='/data/output_compo3_uri.txt',
        volume=vop.volume
    )
    
if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(my_pipeline, 'small_pipeline.tar.gz')