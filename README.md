Documentation
-------------

A simple utility for logging attributes from your infiniTV Eth. 

Usage:
	python server.py ip log_rate

For example:
	python server.py 192.168.1.122 5

Logs statistics from my InfiniTV Eth with IP address "192.168.1.122" once every 5 seconds (recommended).

To view the currently logged stats point your browser to:
	http://localhost:8000/stats.py

Understanding Output:
	Non-integer values are represented without modification. Integer/boolean values (Channel, Playstate) are slightly offset by the tuner index to make it easy to differentiate between tuners. 

![Example Output](screenshots/8a3db400-529e-4c6b-81a1-90bda282e64a.png)
![Example Output](screenshots/99740001-62db-42dc-87cf-007163e30bfa.png)
![Example Output](screenshots/a7d03ed0-a50a-4b79-90ba-416efa4d0919.png)
