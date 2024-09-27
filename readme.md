# Project components

This project contains three server components:

- A frontend python server which executes every command passed in the HTML form (command_server_html.py).
- A middle end python server which executes every command passed in the URL under command parameter (command_server.py).
- A backend python server, which when queried with the correct string returns the IP address of the sender (bdd_server.py).  

Every component has a python file that allows launching and testing the server in a local environment, and a YAML file that allows deploying to Kubernetes. For the YAML files to be used, the namspace.yaml file must first be applied to create the required namespace. All YAML files can be applied using the command ```kubectl apply -f <file_name>.yaml```
