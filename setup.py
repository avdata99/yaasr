import setuptools
from yaasr import __VERSION__


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="yaasr",
    version=__VERSION__,
    author="Andres Vazquez",
    author_email="andres@data99.com.ar",
    description="Yet another audio stream recorder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avdata99/yaasr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License GPLv3+",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers"
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
