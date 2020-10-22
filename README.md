# UnRAID XML Transcriber.

This is a JSON to XML transcriber that allows the use of RainMeter to Monitor your unRAID servers. Currently you need [unRAIDAPI](https://tinyurl.com/y5zwvfx3) installed alongside this container to work, and the container needs the environment variable `API_HOST` set to the IP of the container hosting unRAIDAPI.

- Docker containers and VMs will be able to be padded so that they can still be correctly parsed by Rainmeter as it expects a static XML structure.