branch|state
:---|:---
develop|![](https://github.com/greyhypotheses/augmentation/workflows/Derma%20Python%20Package/badge.svg?branch=develop)
master|![](https://github.com/greyhypotheses/augmentation/workflows/Derma%20Python%20Package/badge.svg?branch=master)

<br>

# Augmentation

This repository complements the

* [derma](https://github.com/greyhypotheses/derma)
* [dermatology](https://github.com/greyhypotheses/dermatology)

repositories. It augments the original images of [dermatology](https://github.com/greyhypotheses/dermatology) for the models of [derma](https://github.com/greyhypotheses/derma).  This is a critical step because the models of [derma](https://github.com/greyhypotheses/derma) include deep transfer learning models that require specific image dimensions.  An upcoming update to this project is a **runtime image dimensions argument**, i.e., a tuple of the required width & height.

<br>
<br>

## Technical Notes
**for Linux Machines**

The augmentation algorithms of this repository can be run via Docker.  Using an Amazon EC2 Linux machine to illustrate:
  * Amazon Linux AMI 2018.03.0.20190826 x86_64 HVM gp2
  * amzn-ami-hvm-2018.03.0.20190826-x86_64-gp2 (ami-00eb20669e0990cb4)

<br>
<br>

### Docker

**Within the Amazon EC2 machine**

In the code snippets below, the required image is *pulled* from Docker Hub after ascertaining that docker is running.

#### Is docker running?

```bash
# Update the environment
sudo yum update -y

# Install Docker
sudo yum install -y docker
docker --version
sudo service docker start

# In order to use docker commands without 'sudo'
sudo usermod -a -G docker ec2-user
exit

# Login again
ssh -i ***.pem ec2-user@**.**.***.**

# Hence
docker info

```

#### Hence, pull image

```bash

# Pull image
docker pull greyhypotheses/derma:augmentation

# Container
# Help: https://docs.docker.com/engine/reference/commandline/run/
# -v ~/images:/app/images => mapping local path ~/images to the volume of the container, i.e., /app/images
# -d => run the container in the background
docker run -d -v ~/images:/app/images greyhypotheses/derma:augmentation

# Thus far, how many images?
cd images
ls | wc -l

# Zip?
# Into zip files of maximum size 99MB each
sudo zip -9 images.zip *.png
sudo zipsplit -n 99000000 images.zip
sudo rm images.zip

```

<br>
<br>

#### Download Option

Local, a cloud repository, etc.  Case local:

```bash
scp -i ***.pem ec2-user@**.**.***.**:~/images/*.csv augmentation/images/
scp -i ***.pem ec2-user@**.**.***.**:~/images/*zip augmentation/images/
```

<br>
<br>

### Miscellaneous Docker Notes

For readers new to docker:

#### Clearing Docker Containers
```bash
# -v ensures that associated volumes are also deleted
docker rm -v ... [container code]
```

#### Clearing Docker Volumes

```bash
# List volumes
docker volume ls

# Delete all volumes
docker volume rm $(docker volume ls -q)
```

#### Clearing Docker Images
```bash
# -v ensures that associated volumes are also deleted
docker rmi ... [image code]
```
