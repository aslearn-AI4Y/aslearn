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

# Server Usage

After cloning the project, installing docker and changing working directory to the project folder, you can run the server by running the following commands:

```bash
docker build -t aslearn .
docker run -p 80:80 -p 22:22 --name aslearn -it aslearn
docker exec -it aslearn /bin/bash
nohup /usr/sbin/sshd -D & nohup python app.py &
```

Now you can access the aslearn on http://localhost:80 and ssh to the server with `ssh root@localhost`.

Change the password to your liking in the [Dockerfile](Dockerfile) and the port to your liking in the bash script from above.

# Our Goals

As we mentioned before, we want to make a platform that helps you learn the sign language for free to make communication and the sign language more accessible for everyone. The AI is able to recognize the letter through your camera in live and will provide qualified and reliable feedback.

The more people will use our project, the more people will be able to use the sign language on a daily basis, which will make the barrier of communication between people thinner and thinner until it disappears completely

<!-- image images/dataset_probe.png-->

![dataset probe](images/dataset_probe.png)
