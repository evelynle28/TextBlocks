# TextBlock
TextBlock is a Python desktop app to retrieve text position and content from your uploaded images.

## Requirements
To run this application, the OpenVINO™ toolkit and its dependencies must already be installed either locally or on the server. More details on OpenVINO installation may be found [here](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)

### Hardware
- 6th to 10th generation Intel® Core™ and Intel® Xeon® processors.
- OR use of Intel® Neural Compute Stick 2 (NCS2)Processors

See more at [OpenVINO Prerequisites](https://docs.openvinotoolkit.org/latest/index.html)

### Operating system
- Ubuntu* 18.04.3 LTS (64 bit)
- Windows® 10 (64 bit)
- CentOS* 7.4 (64 bit)
- macOS* 10.13, 10.14 (64 bit)


### Software
CMake 3.9 or higher
Python 3.5 - 3.7


## Set up

 Clone this repository

```sh
$ git clone https://github.com/evelynle28/TextBlocks.git
```

Install dependencies from pipfile.lock

```sh
$ pipenv install --deploy --ignore-pipfile
```

Update the your server's IP address and port in `server.py` and `TextBlock.py`
Run `server.py`  locally or on your preferred development server

```sh
$ python3 server.py
```

## Run

Run `TextBlock.py`

```sh
$ python3 TextBlock.py
```

![@demo_app | center | 200x0](https://raw.githubusercontent.com/evelynle28/TextBlocks/master/img/demo_img.png)


