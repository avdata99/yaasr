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
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers"
    ],
    packages=setuptools.find_packages(),
    package_data={
        "yaasr": [
            "streams/*/data.json",
            "terminal/tpl/supervisor.ini"
            ]
        },
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.25.1',
        'pydub>=0.24.1',   # Process audios
        'paramiko>=2.7.2',  # Upload ssh
        'google-cloud-storage>=1.36.0',  # Google cloud storage
        'jinja2>=2.11.3',  # Supervisor templates creation
    ],
    entry_points={
        'console_scripts': [
            'yaasr=yaasr.terminal:main',
            ],
    },
)
