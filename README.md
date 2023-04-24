<!-- Declare hyper links to DataSet, Autors GitHub, and the project GitHub -->

[asl alphabet dataset]: https://www.kaggle.com/datasets/grassknoted/asl-alphabet
[denis]: https://github.com/Denloob
[itai]: https://github.com/ItaiAviad
[yoav]: https://github.com/EazyIf

# About the project

Unfortunately, not all people can hear or speak, and communication that is taking a very big part of our daily basis becomes a big problem.
Aslearn helps you learn the sign language for free using AI.

#### Made by

[Denis], [Itai] and [Yoav] from Israel, The New Bosmat School

DM Den_loob#2209 using [discord](https://discord.com/) or using github to get in touch with the project.

##### Thanks to Akash for the [ASL Alphabet DataSet]

# Demo
#### Site Demo
[aslearn.tk](https://aslearn.tk)

#### Video Demo
![aslearn demo](https://user-images.githubusercontent.com/83463243/202922672-4280c456-b4ee-4250-b9a1-d77b3ba0ad3c.gif)

# Server Usage

After cloning the project and installing docker, you can run the server by
running the following commands:

```bash
docker build -t aslearn .
docker run -p 80:80 --name aslearn -it aslearn
```

Now you can access the aslearn website on http://localhost:80

# Our Goals

As we mentioned before, we want to make a platform that helps you learn the sign language for free to make communication and the sign language more accessible for everyone. The AI is able to recognize the letter through your camera in live and will provide qualified and reliable feedback.

The more people will use our project, the more people will be able to use the sign language on a daily basis, which will make the barrier of communication between people thinner and thinner until it disappears completely.

<!-- image images/dataset_probe.png-->

![dataset probe](images/dataset_probe.png)
