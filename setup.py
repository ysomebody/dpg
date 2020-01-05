import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dpg",
    version="1.0.0dev0",
    author="ysomebody",
    author_email="ysomebody@163.com",
    description="DigitalPatternGenerator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ysomebody/dpg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    python_requires='>=3.7',
)
