Lambda Sidecar Service
======

This is an example of using pyinstaller to build a binary to run as a lambda sidecar.
The main purposes of this is to run a proxy or service alongside a lambda for workload utility functions that require credentials.

This service is built using Pulumi, lambda dependencies are installed and packaged from pulumi using pulumi-command.

The only requirement here is that the lambdas are built in an environment with the same GLIBC version as AWS Lambda.
