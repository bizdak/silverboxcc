Reverse engineered android malware called Red Alert V2.0. 
At the time of analysis, there were no longer any C2 servers running and so we were unable to observe any traffic between the malware and the C2 server. 
So we figured out the C2 protocol and wrote this control panel.

Bot's traffic from the device can be redirected using iptables so all bot communication is sent to our C2 server. 

	iptables -t nat -A OUTPUT -p tcp --dport <BOT’s port> -j DNAT --to-destination <you IP Address>:<port>


See it in action:
https://youtu.be/nDHsv5IMgZQ