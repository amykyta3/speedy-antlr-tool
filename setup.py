import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


with open(os.path.join("speedy_antlr_tool", "__about__.py")) as f:
    v_dict = {}
    exec(f.read(), v_dict)
    version = v_dict['__version__']


setuptools.setup(
    name="speedy-antlr-tool",
    version=version,
    author="Alex Mykyta",
    author_email="amykyta3@github.com",
    description="Generate an accelerator extension that makes your Antlr parser in Python super-fast!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amykyta3/speedy-antlr-tool",
    packages=setuptools.find_packages(exclude=["test"]),
    include_package_data=True,
    python_requires='>=3.4',
    install_requires=[
        "antlr4-python3-runtime",
    ],
    project_urls={
        "Source": "https://github.com/amykyta3/speedy-antlr-tool",
        "Tracker": "https://github.com/amykyta3/speedy-antlr-tool/issues",
    },
)