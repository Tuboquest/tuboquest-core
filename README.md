[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">TuboQuest - Core</h3>

  <p align="center">
    Remote device and its AI.
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->

  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>



<!-- ABOUT THE PROJECT -->

## About The Project

This repository contains the code for the Raspberry Pi, which is responsible for controlling the remote device, as well
as the AI components housed within the remote device. The AI section includes the dataset, trained model, and other
related elements.

### Built With

* ![Python][Python]
* ![Raspberry PI][RaspberryPI]
* [![Hailo][Hailo]][Hailo-url]
* [![Tappas][Tappas]][Tappas-url]
* [![Ultralytics][Ultralytics]][Ultralytics-url]
* [![Yolo][Yolo]][Yolo-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Make sure you have the following installed on your Raspberry Pi:

- Python 3.x
- Git

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Tuboquest/tuboquest-core.git
   ```
3. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```

#### Assembly Instructions

For detailed instructions on how to assemble the remote device, please refer to
the [assembly guide](https://github.com/Tuboquest/docs/blob/main/TuboPark%20-%20Remote%20device.pdf).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

## Usage

For more information on the AI usage & model training, please refer to
this [Documentation](https://github.com/Tuboquest/docs/blob/main/TuboPark%20-%20AI.pdf)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge

[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt

[product-screenshot]: images/screenshot.png

[Python]: https://img.shields.io/badge/python-213e53?style=for-the-badge&logo=python&logoColor=white

[RaspberryPI]: https://img.shields.io/badge/Raspberry--PI-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white

[Hailo]: https://img.shields.io/badge/Hailo-35495E?style=for-the-badge

[Hailo-url]: https://hailo.ai/

[Ultralytics]: https://img.shields.io/badge/Ultralytics-0089FF?style=for-the-badge

[Ultralytics-url]: https://www.ultralytics.com/

[Tappas]: https://img.shields.io/badge/Tappas-27021f?style=for-the-badge

[Tappas-url]: https://github.com/hailo-ai/tappas

[Yolo]: https://img.shields.io/badge/Yolo-ffffff?style=for-the-badge

[Yolo-url]: https://pjreddie.com/darknet/yolo/