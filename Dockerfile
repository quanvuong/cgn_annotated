FROM nvidia/cudagl:11.2.2-devel-ubuntu20.04

# for CGN fine-tuning

# ========= CUDA, CUDNN, Vulkan ========
ENV NV_CUDNN_VERSION=8.1.1.33

ENV NV_CUDNN_PACKAGE="libcudnn8=$NV_CUDNN_VERSION-1+cuda11.2" \
    NV_CUDNN_PACKAGE_DEV="libcudnn8-dev=$NV_CUDNN_VERSION-1+cuda11.2" \
    NV_CUDNN_PACKAGE_NAME="libcudnn8"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ${NV_CUDNN_PACKAGE} \
    ${NV_CUDNN_PACKAGE_DEV} \
  && apt-mark hold ${NV_CUDNN_PACKAGE_NAME} \
  && rm -rf /var/lib/apt/lists/*

# Vulkan ICD
RUN mkdir -p /usr/share/vulkan/icd.d \
  && echo '{"file_format_version": "1.0.0", "ICD": {"library_path": "libGLX_nvidia.so.0", "api_version": "1.1.84"}}' > /usr/share/vulkan/icd.d/nvidia_icd.json


# ========= ubuntu essentials ======== 
# from kolin mobile_pnp
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim git curl wget yasm cmake unzip pkg-config \
    checkinstall build-essential ca-certificates \
    software-properties-common apt-utils bash-completion \
    libeigen3-dev \
  && apt-get upgrade -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install -y --no-install-recommends locales \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && locale-gen "en_US.UTF-8" \
  && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 \
  && ln -fs /usr/share/zoneinfo/America/Los_Angeles /etc/localtime  # Set timezone
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8


RUN apt-get update && apt-get install -y --no-install-recommends \
    zlib1g-dev libjpeg-dev libpng-dev xvfb ffmpeg xorg-dev \
    xorg-dev libboost-all-dev libsdl2-dev swig \
    libblas-dev liblapack-dev \
    libopenblas-base libatlas-base-dev graphviz \
  && apt-get upgrade -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# ======== Python ========
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && python3 -m pip install --upgrade pip    # Upgrade pip

RUN python3 -m pip install jupyter_contrib_nbextensions \
  && jupyter contrib nbextension install \
  && python3 -m pip install jupyter_nbextensions_configurator \
  && jupyter nbextensions_configurator enable

RUN mkdir /.local && chmod a+rwx /.local

RUN python3 -m pip install argcomplete \
  && activate-global-python-argcomplete

# ======== CGN env with miniconda ========
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
ENV PATH="${PATH}:/miniconda/pcondabin:/miniconda/bin"

COPY ./contact_graspnet_env.yml /tmp/
RUN conda env create -f /tmp/contact_graspnet_env.yml \
  && rm -r /tmp/*

ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
RUN ln -s /usr/local/cuda-11.2/lib64/libcusolver.so.11 /usr/local/cuda-11.2/lib64/libcusolver.so.10

