## Installation

You need python3 and pip3 to use this character generator. Please install python3/pip3 before completing this tutorial.

**Step 1**: Install the package dependencies. This will install `pdfrw`, `z3`, `names` and other dependencies.

    pip3 install -r requirements.txt 

## Quickstart

The `character_generator.py` script generates random characters that satisfy a set of user-defined character generation constraints. the following script generates three characters that satisfies the constraints described in `prefabs/random.cfg`

    python3 character_generator.py 3 --chargen-guide prefabs/random.cfg

The generated characters will be in the `output/` directory. The above command will generate three characters at the following file location:

    output/char-0.pdf
    output/char-1.pdf
    output/char-2.pdf
