#!/bin/bash

# the path to the interpreter and all of the originally intended arguments
args=("$@")

## the extra options to pass to the interpreter
#extra_args=()
#
## insert the extra options
#args=("${args[@]:0:$#-1}" "${extra_args[@]}" "${args[@]: -1}")

/opt/sidecar

# start the runtime with the extra options
exec "${args[@]}"
