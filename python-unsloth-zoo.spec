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
Requires:	python%{pyver}dist(tyro)
Requires:	python%{pyver}dist(hf-transfer)
Requires:	python%{pyver}dist(msgspec)
Requires:	python%{pyver}dist(sentencepiece)
Requires:	python%{pyver}dist(datasets)
Requires:	python%{pyver}dist(trl)
Recommends:	python%{pyver}dist(triton)
Recommends:	python%{pyver}dist(torchao)

# NVIDIA-only extras must not become hard generated Requires.
%global __requires_exclude ^python[0-9.]+dist\\((triton|torchao|cut-cross-entropy)\\)

%description
Helper library used by Unsloth for model patching, checkpoint
handling and export helpers. Install python-unsloth for the
fine-tuning frontend.

%prep -a
python - <<'PY'
from pathlib import Path
import re
p = Path("pyproject.toml")
t = p.read_text()
t = t.replace('"torch>=2.4.0,<2.13.0 ; (sys_platform != \'darwin\' or platform_machine != \'arm64\')"',
              '"torch>=2.4.0 ; (sys_platform != \'darwin\' or platform_machine != \'arm64\')"')
t = t.replace('"datasets>=3.4.1,!=4.0.*,!=4.1.0,<4.4.0"', '"datasets>=3.4.1"')
t = t.replace('"trl>=0.18.2,!=0.19.0,<=0.24.0 ; (sys_platform != \'darwin\' or platform_machine != \'arm64\')"',
              '"trl>=0.18.2 ; (sys_platform != \'darwin\' or platform_machine != \'arm64\')"')
t = re.sub(r'"transformers>=4\.51\.3,[^"]+"', '"transformers>=4.51.3"', t)
out = []
for line in t.splitlines(True):
    if any(k in line for k in ("triton>=", "torchao>=", "cut_cross_entropy")):
        continue
    out.append(line)
p.write_text("".join(out))
print("patched zoo pyproject.toml")
PY

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
