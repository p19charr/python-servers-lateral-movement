# Project components

This project contains three server components:

- A frontend python server which executes every command passed in the HTML form (command_server_html.py).
- A middle-end python server which executes every command passed in the URL under command parameter (command_server.py).
- A backend python server, which when queried with the correct string returns the IP address of the sender (bdd_server.py).  

Every component has a python file that allows launching and testing the server in a local environment, and a YAML file that allows deploying to Kubernetes. For the YAML files to be used, the namespace.yaml file must first be applied to create the required namespace. All YAML files for the components can be applied using the command ```kubectl apply -f <file_name>.yaml```


Each component has a network policy assiocated with it:

- The frontend network policy should stay commented and hsould not be used, as it will prevent outside access to the frontend pods.
- The middle-end network policy allows TCP calls from and to the frontend pods, and from and to the backend pods.
- The backend network policy allows TCP calls from and to the middle-end pods only.

The network policies files must be applied using ```calicoctl apply -f <file_name>.yaml```
