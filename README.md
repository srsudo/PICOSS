
# PICOSS
> A Python Interface for the Classification of Seismic Signals.

PICOSS is a Python GUI designed as a modular data-curator platform for volcano-seismic data analysis. Detection, 
segmentation and classification. With exportability and standardization at its core, users can select automatic 
or manual workflows to annotate seismic data from the suite of included tools. 

Originally, PICOSS was designed for the purposes of seismicity research as a collaboration between University of Granada 
(UGR) and University of Liverpool (UoL). However, the system can be used within a wide range of geophysical applications.


# We are currently working on switching the interface from Python 2.7 to Python 3.0+

# New features include buttons for Zooming, Spanning and Undo, along latest improvements and feedback received



![PICOSS logo](https://github.com/srsudo/PICOSS/tree/master/info/img/picos_header.png)


## Installation

PICOSS works in OS X & Linux and Windows systems. We strongly recommend to install [Docker containers](https://docs.docker.com/engine/installation/) 
or [Anaconda environment](https://conda.io/docs/user-guide/install/index.html) first. 

Requisites can be found in [requirements] (requirements.md) file. See [Installing PICOSS](https://github.com/srsudo/PICOSS/tree/master/info/installation.md) 
for detailed instructions about the installation of PICOSS. 

## Usage example

Once all dependencies are installed, we can run PICOSS from the Python CLI (or terminal): 

```sh
$ python run_picos.py
```

The main GUI window should appear, and data can be accessed normally. For detailed explanations and more 
examples about how to use PICOSS, please refer to the [tutorial](https://github.com/srsudo/PICOSS/tree/master/info/tutorials/howto.md)_


## Release History

* 0.1.0
    * First release with expanded functionalities
    * code-ready for submission at journal
* 0.0.1
    * Work in progress

## Meta: 

Angel Bueno - angelbueno@ugr.es
Alejandro Diaz - aledm@liverpool.ac.uk
Jack Woolam - jack.woollam@liverpool.ac.uk
Luciano Zuccarello - lzuk@ugr.es

Distributed under the MIT license. See ``LICENSE`` for more information.


## Contributing

1. Fork it on your own github (<https://github.com/srsudo/picoss/fork>)
2. Create your feature branch (`git checkout -b feature/awesome_feature`)
3. Commit your changes (`git commit -am 'Add some awesome feature'`)
4. Push to the branch (`git push origin feature/awesome_feature`)
5. Create a new Pull Request

### Funding

This project is funded by TEC2015-68752 (MINECO/FEDER),  NERC Grant NE/P00105X/1 and by Marie Sklodowska-Curie Grant Agreement
no 798480.

<!-- Markdown link & img dfn's -->
[wiki]: https://github.com/srsudo/picoss/wiki

