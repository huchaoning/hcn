install:
    pip install -e .


uninstall:
    pip uninstall -y hcn


build: clean
    python -m build


clean:
    rm -rf dist/


clean-up: clean
    find . -name '*.egg-info' -exec rm -rf {} +
    find . -name '__pycache__' -exec rm -rf {} +
    find . -name '*.pyc' -exec rm -rf {} +


reinstall: uninstall clean install


push:
    git add . && git commit -m "work in progress... | $(date '+%Y-%m-%d %H:%M:%S')" && git push


serve:
    mkdocs serve --livereload

