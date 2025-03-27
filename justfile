# https://just.systems/man/en/

# REQUIRES

docker := require("docker")
find := require("find")
rm := require("rm")
uv := require("uv")

# VARIABLES

REPOSITORY := "fmind-ai-assistant"
SOURCES := "*.py"

# DEFAULTS

# display help information
default:
    @just --list

# IMPORTS

import 'tasks/app.just'
import 'tasks/check.just'
import 'tasks/clean.just'
import 'tasks/docker.just'
import 'tasks/format.just'
import 'tasks/install.just'
import 'tasks/package.just'
