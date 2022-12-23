import os
import shutil
import subprocess
import sys
from contextlib import suppress

import setuptools
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py

# Based on https://github.com/pybind/python_example

os.environ["PATH"] += os.pathsep + os.path.join(sys.prefix, "bin")
base_path = os.path.abspath(os.path.dirname(__file__))
scripts_directory = os.path.join(base_path, "scripts")
requirements_installed = False


class BuildExtensionCommand(build_ext):
    compiler_options = {
        "msvc": ["/EHsc"],
        "unix": [],
    }

    if sys.platform == "darwin":
        compiler_options["unix"] += [
            "-stdlib=libc++",
            "-mmacosx-version-min=10.7",
        ]

    def build_extensions(self):
        compiler_type = self.compiler.compiler_type
        options = self.compiler_options.get(compiler_type, [])

        if compiler_type == "unix":
            options.append(
                '-DVERSION_INFO="{}"'.format(self.distribution.get_version())
            )
            options.append(self._cpp_flag())

            if self._has_flag("-fvisibility=hidden"):
                options.append("-fvisibility=hidden")
        elif compiler_type == "msvc":
            options.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())

        for extension in self.extensions:
            extension.extra_compile_args = options

        super().build_extensions()

    # As of Python 3.6, CCompiler has a `has_flag` method.
    # cf http://bugs.python.org/issue26689
    def _has_flag(self, flag):
        """Return a boolean indicating whether a flag name is supported on
        the specified compiler.
        """
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".cpp") as output_file:
            output_file.write("int main (int argc, char **argv) { return 0; }")
            try:
                self.compiler.compile([output_file.name], extra_postargs=[flag])
            except setuptools.distutils.errors.CompileError:
                return False

        return True

    def _cpp_flag(self):
        """Return the -std=c++[11/14] compiler flag.
        The c++14 is prefered over c++11 (when it is available).
        """
        if self._has_flag("-std=c++14"):
            return "-std=c++14"
        elif self._has_flag("-std=c++11"):
            return "-std=c++11"
        else:
            raise RuntimeError(
                "Unsupported compiler -- at least C++11 support is needed!"
            )


def install_python_packages():
    requirements = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "wheel",
        "pybind11~=2.9.0",
    ]

    with suppress(Exception):
        subprocess.check_call(
            requirements,
            cwd=scripts_directory,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
    with suppress(Exception):
        subprocess.check_call(
            ["sudo"] + requirements,
            cwd=scripts_directory,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )


class InstallRequirements(build_py):
    def run(self) -> None:
        subprocess.check_call(
            ["bash", os.path.join(scripts_directory, "install_requirements.sh")],
            cwd=scripts_directory,
        )
        install_python_packages()

        if not shutil.which("mecab"):
            subprocess.check_call(
                ["bash", os.path.join(scripts_directory, "install_mecab_ko_dic.sh")],
                cwd=scripts_directory,
            )

        return super(InstallRequirements, self).run()


def lazy(func):
    class Decorator:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __str__(self):
            return func(*self.args, **self.kwargs)

        def __add__(self, other):
            return str(self) + other

        def __radd__(self, other):
            return other + str(self)

    return Decorator


@lazy
def get_pybind_include(user=False):
    install_python_packages()

    import pybind11

    return pybind11.get_include(user)


@lazy
def get_mecab_include_directory():
    return (
        subprocess.check_output(["mecab-config", "--inc-dir"]).decode("utf-8").strip()
    )


@lazy
def get_mecab_library_directory():
    return (
        subprocess.check_output(["mecab-config", "--libs-only-L"])
        .decode("utf-8")
        .strip()
    )


version = None
with open(os.path.join("mecab", "__init__.py"), encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("__version__"):
            version = line.split("=")[1].strip().replace('"', "").replace("'", "")

with open("README.md", "r", encoding="utf-8") as input_file:
    long_description = input_file.read()

setup(
    name="python-mecab-kor",
    version=version,
    url="https://github.com/hyunwoongko/python-mecab-kor",
    author="Hyunwoong Ko",
    author_email="gusdnd852@gmail.com",
    description="Yet another python binding for mecab-ko",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    keywords="mecab mecab-ko python-mecab python-mecab-ko python-mecab-kor",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: Korean",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
    ],
    zip_safe=False,
    python_requires=">=3",
    data_files=[
        ("scripts", ["scripts/install_requirements.sh"]),
        ("scripts", ["scripts/install_mecab_ko_dic.sh"]),
    ],
    ext_modules=[
        Extension(
            name="_mecab",
            sources=[
                "mecab/pybind/_mecab/node.cpp",
                "mecab/pybind/_mecab/path.cpp",
                "mecab/pybind/_mecab/lattice.cpp",
                "mecab/pybind/_mecab/dictionaryinfo.cpp",
                "mecab/pybind/_mecab/tagger.cpp",
                "mecab/pybind/_mecab/_mecab.cpp",
            ],
            include_dirs=[
                get_pybind_include(),
                get_pybind_include(user=True),
                get_mecab_include_directory(),
            ],
            libraries=["mecab"],
            library_dirs=[get_mecab_library_directory()],
            runtime_library_dirs=[get_mecab_library_directory()],
            language="c++",
        ),
    ],
    packages=find_packages(),
    cmdclass={
        "build_py": InstallRequirements,
        "build_ext": BuildExtensionCommand,
    },
)
