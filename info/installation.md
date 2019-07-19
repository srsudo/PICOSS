# Installation

*PICOSS is not public at the moment, and it is not on PyPI yet. These installation instructions may change in a near future.*

PICOSS works on Linux & OSX & Windows. Installation from source can be made. However, we strongly recommend [Docker containers](https://docs.docker.com/engine/installation/) or [Anaconda environments](https://conda.io/docs/user-guide/install/index.html) with obspy insalled. 

First, download (and unzip) or clone the repository: 
```sh
$ git clone https://github.com/srsudo/picos.git
$ cd picos
```

## pypi
TBD

### conda
If you use conda/Anaconda environments, the environment is already prepared for you. Run the following:: 

```sh
$ conda env create -f conda_env/picos_light.yml
```

Once conda finished the installation of all the dependencies, we activate the conda environment and run the program: 

```sh
$ source activate picos_light
$ python run_picos.py
```

## Docker

Once docker is installed in your system, we can install PICOSS image by using _docker-compose_. The main reason behind this
is that we have several volumes that need to be used in order to keep the data and avoid catastrophic losses.

*Assuming you are executing docker inside the downloaded repository folder (e.g: "picoss/") folder, just run:*

```sh
docker-compose build
```

The docker-compose command assumes two volumes to share the data between the container and the host and your machine:
    - ./data: the folder to access all data
    - ./segmented_data: the folder where all the segmented data will be stored.

Once the building process is finished, just run PICOSS:

```sh
docker-compose run interface_picos
```

If X11 server does not start, just run: ```sh xhost +local:root ```

#### NOTE: If you want to manipulate the Dockerfile yourself:

You can install PICOSS directly from the container, just by running:

```sh
$ docker build -t picos .
```

Any extra package can be directly modified/added at the container if needed. A possible command to run the container directly is: 

```sh
$ docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY docker/picos:latest 
```

## Troubleshooting

### Pip and/or apt-get does not work in dockerfile

If you are working on a proxy, there is a high probability that docker containers do not reach internet at all. You can test this by running **busybox** test container::

```sh
$ docker pull busybox
$ docker run -it busybox sh
ping google.com
```

If it hangs, it means your proxy configuration is giving some troubles. Have a look [here](https://stackoverflow.com/questions/46694556/docker-curriculum-tutorial-python-pip-fails)

### The X11 server

If you are running docker on, PyQt GUI interface requires X11 server available.

To run PICOSS, execute the following:

```sh
xhost +local:root
```

### About MAC.OSX and the X-server

MACOS my not work properly with the X-server. However, there is a quick fix to solve this. We need to know which port your X11 is
(also, make sure you have *quartz* already).  We can solve it two ways: 

* #### The "easy" way:

In this case, you need to **introduce and re-run these commands every time you run docker-compose up**. From a terminal, run:

`ifconfig en0 | grep inet | awk '$1=="inet" {print $2}`

An IP number will appear as output. Copy that IP and run: 

`xhost + #ip-you-just-copied`

A message saying something like: "this IP has been added to te list of known host" will be added. On the "docker-compose.yml", 
change this line:

```
      - DISPLAY=unix$DISPLAY
```

for this one: 

```
      - DISPLAY=ip-you-just-copied:0
```

And then run `sh docker-compose run interface_picos`


* #### The "bash" way:
Just create a ".sh" file (with vim for example, named "connect_X11.sh"), in the main picoss folder, and copy the following lines: 

```
ip = $(ifconfig en | grep inet | awk '$1=="inet" {print $2}')
xhost + $ip
```

then, an ip address will appear. Copy that ip address. At the "docker-compose.yml", change this line:

```
      - DISPLAY=unix$DISPLAY
```

for this one: 

```
      - DISPLAY=ip-you-just-copied:0
```

Then run again: ```sh docker-compose run interface_picos```. 