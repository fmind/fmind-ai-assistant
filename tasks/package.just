# run package tasks
[group('package')]
package: package-requirements

# build package requirements
[group('package')]
package-requirements:
	uv export --format=requirements-txt --no-dev \
	--no-hashes --no-editable --no-emit-project \
	--output-file=requirements.txt
