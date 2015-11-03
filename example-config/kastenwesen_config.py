#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

config_containers = []

#########################################
# my_linux_base                         #
# ===================================== #
# Linux (Ubuntu 14.04) base image       #
#########################################
my_linux_base = DockerContainer("my-linux-base", "./my-linux-base/", tests={})
config_containers.append(my_linux_base)

# TODO dependency on my_linux_base, without linking

#########################################
# web                                   #
# ===================================== #
# A web server listening on port 80     #
#########################################
web = DockerContainer(
    "webserver", "./webserver/",
    docker_options="-p 80:80 -v " + os.getcwd() + "/webserver/webroot:/var/www:ro",
    tests={'sleep_before': 2, 'http_urls': ['http://localhost'], 'ports': [80]})
config_containers.append(web)

#########################################
# test1                                 #
# ===================================== #
# A testserver listening on port 1231   #
#########################################
test1 = DockerContainer(
    "test1", "./test1/",
    docker_options="-p 1231:1234",
    tests={'sleep_before': 0, 'ports': [1231]})
config_containers.append(test1)

#########################################
# test2                                 #
# ===================================== #
# A testserver listening on port 1232   #
#########################################
test2 = DockerContainer(
    "test2", "./test2/",
    links=[test1],
    docker_options="-p 1232:1234",
    tests={'sleep_before': 0, 'ports': [1232]})
config_containers.append(test2)

#########################################
# portforwarder_to_test2                #
# ===================================== #
# A portforwarder that forwards the     #
# port of test2 to 1337                 #
# (like a reverse proxy)                #
#########################################
portforwarder_to_test2 = DockerContainer(
    "portforwarder-to-test2", "./portforwarder-to-test2/",
    links=[test2],
    docker_options="-p 1337:1234",
    tests={'sleep_before': 0, 'ports': [1337]})
config_containers.append(portforwarder_to_test2)
