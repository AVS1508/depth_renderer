FROM nvidia/cuda:11.1.1-devel-ubuntu20.04

# Remove any third-party apt sources to avoid issues with expiring keys.
RUN rm -f /etc/apt/sources.list.d/*.list

# Install some basic utilities.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    wget \
    libxml2-dev \
    cmake \
    python-numpy \
    python-nose \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
&& rm -rf /var/lib/apt/lists/*

# Download and install Micromamba.
RUN curl -sL https://micro.mamba.pm/api/micromamba/linux-64/1.1.0 \
    | sudo tar -xvj -C /usr/local bin/micromamba

ENV MAMBA_EXE=/usr/local/bin/micromamba \
    MAMBA_ROOT_PREFIX=/home/user/micromamba \
    CONDA_PREFIX=/home/user/micromamba \
    PATH=/home/user/micromamba/bin:$PATH

# Copy the environment file.
# RUN mkdir /workspace
# COPY Dockerfile /workspace/
# COPY environment.yml /workspace/
COPY . /workspace

# Create a new environment.
RUN --mount=type=cache,target=/home/user/micromamba/pkgs/ micromamba create -qy -f /workspace/environment.yml -v
RUN micromamba shell init --shell=bash --prefix="$MAMBA_ROOT_PREFIX"
RUN micromamba clean -qya

# default
RUN echo "micromamba activate renderer" >> ~/.bashrc
ENV PATH /home/user/micromamba/envs/renderer/bin:$PATH

# Install PyFusion
RUN mkdir /workspace/external/pyfusion/build
WORKDIR /workspace/external/pyfusion/build
RUN cmake ..
RUN make

# Compile the cython code
WORKDIR /workspace/external/pyfusion/
RUN python3 setup.py build_ext --inplace
RUN pip install imageio

# Specify the path of the Blender executable in setting.py
ENV g_blender_excutable_path="/workspace/blender-2.79b-linux-glibc219-x86_64/blender"

# Set the working directory.
WORKDIR /workspace

# Run bash when the container launches.
ENTRYPOINT ["tail", "-f", "/dev/null"]
