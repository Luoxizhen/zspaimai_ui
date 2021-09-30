#!/usr/bin/env python3
import sys

__version__ = "1.0.8"

from setuptools import setup, find_packages

# We do not support Python <3.8
if sys.version_info < (3, 8):
    print(
        "Unfortunately, your python version is not supported!\n"
        "Please upgrade at least to Python 3.8!",
        file=sys.stderr,
    )
    sys.exit(1)

install_requires = [
    "ddt",
    "pyyaml",
    "websocket_client",
    "requests",
    "facebook-wda",
    # "matplotlib",
    "future",
    # "cssselect"
]

entry_points = {
    "console_scripts": [
        "minitest=minium.framework.loader:main",
        "miniruntest=minium.framework.loader:main",
        "minireport=minium.framework.report:main",
        "miniErrorReport=minium.framework.errorReport:main",
        "mininative=minium.native.nativeapp:start_server",
    ]
}


config_path = "miniprogram/base_driver/version.json"
package_data = {
    "minium": [
        config_path,
        "framework/dist/*",
        "framework/dist/*/*",
        "native/wx_native/*/*",
        "native/qq_native/*/*",
        "native/*/*",
        "native/*/*/*/*",
        "native/*/*/*/*/*",
        "native/*/*/*/*/*/*",
    ]
}

exclude_package_data = {"": ["*pyc", "readme.md", "build.py"]}

if __name__ == "__main__":
    setup(
        name="minium",
        version=__version__,
        license="MIT",
        url="https://git.weixin.qq.com/minitest/minium-doc",
        packages=find_packages(),
        description="Minium is the best MiniProgram auto test framework.",
        long_description="""""",
        package_data=package_data,
        exclude_package_data=exclude_package_data,
        entry_points=entry_points,
        install_requires=install_requires,
        setup_requires=["setuptools"],
        python_requires=">=3.8",
        author="WeChat-Test",
        author_email="lockerzhang@tencent.com",
        platforms=["MacOS", "Windows"],
        keywords=["minium", "WeApp", "MiniProgram", "Automation", "Test"]
    )
