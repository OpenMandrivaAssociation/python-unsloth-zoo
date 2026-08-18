Name:		python-unsloth-zoo
Version:	2026.8.12
Release:	1
Summary:	Shared utilities for Unsloth fine-tuning
License:	LGPL-3.0-or-later
Group:		Development/Python
URL:		https://github.com/unslothai/unsloth-zoo
Source0:	https://files.pythonhosted.org/packages/source/u/unsloth-zoo/unsloth_zoo-%{version}.tar.gz
BuildArch:	noarch
BuildSystem:	python
BuildRequires:	python
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
BuildRequires:	python%{pyver}dist(wheel)

# Upstream pins torch<2.13 and transformers<=5.5; we ship newer
# working versions. RPM requires the modules, not the upper bounds.
Requires:	python%{pyver}dist(torch)
Requires:	python%{pyver}dist(transformers)
Requires:	python%{pyver}dist(peft)
Requires:	python%{pyver}dist(accelerate)
Requires:	python%{pyver}dist(huggingface-hub)
Requires:	python%{pyver}dist(numpy)
Requires:	python%{pyver}dist(packaging)
Requires:	python%{pyver}dist(tqdm)
Requires:	python%{pyver}dist(psutil)
Requires:	python%{pyver}dist(protobuf)
Requires:	python%{pyver}dist(pillow)
Requires:	python%{pyver}dist(regex)
Requires:	python%{pyver}dist(filelock)
Requires:	python%{pyver}dist(typing-extensions)
Recommends:	python%{pyver}dist(sentencepiece)
Recommends:	python%{pyver}dist(datasets)
Recommends:	python%{pyver}dist(trl)

%description
Helper library used by Unsloth for model patching, checkpoint
handling and export helpers. Install python-unsloth for the
fine-tuning frontend.

# pip writes .pyc then touches .py; extra tests treat that as
# python-bytecode-inconsistent-mtime (100+ files, over the badness cap).
%install -a
find %{buildroot} -type d -name '__pycache__' -exec rm -rf {} +
find %{buildroot} -name '*.pyc' -delete

%files
%doc README.md
%license LICENSE
%{py_sitedir}/unsloth_zoo
%{py_sitedir}/unsloth_zoo-*.*-info
