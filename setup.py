import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ao3downloader",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "ao3downloader"},
    packages=setuptools.find_packages(where="ao3downloader"),
    python_requires=">=3.7",
    install_requires=[
    'beautifulsoup4==4.9.3',
    'certifi==2020.12.5',
    'cffi==1.15.0',
    'chardet==4.0.0',
    'colorama==0.4.4',
    'cryptography==36.0.1',
    'cssselect==1.1.0',
    'EbookLib==0.17.1',
    'idna==2.10',
    'loguru==0.5.3',
    'lxml==4.6.3',
    'mobi==0.3.2',
    'pdfminer.six==20211012',
    'pdfquery==0.4.3',
    'pycparser==2.21',
    'pyquery==1.4.3',
    'requests==2.25.1',
    'roman==3.3',
    'six==1.16.0',
    'soupsieve==2.2.1',
    'tqdm==4.60.0',
    'urllib3==1.26.4',
    'win32-setctime==1.1.0'
    ],
)