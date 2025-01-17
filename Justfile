# Variables
env-name := "moodleconv"
env-file := "env.yml"

@_default:
    just --list

# Create conda environment from the environment file
@environment:
    echo "{{GREEN}}Creating environment {{env-name}} from {{env-file}}{{NORMAL}}"
    mamba env create -n {{env-name}} -f {{env-file}}
    echo "{{GREEN}}Environment has been created{{NORMAL}}"

# Update conda environment from the environment file
@env-update:
    echo "{{GREEN}}Updating environment {{env-name}} from {{env-file}}{{NORMAL}}"
    mamba env update -n {{env-name}} -f {{env-file}}
    echo "{{GREEN}}Environment has been updated{{NORMAL}}"