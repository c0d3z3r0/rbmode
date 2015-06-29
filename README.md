# rbMode

Tool for setting LAN/WAN mode on riverbed servers

## Installation

* Copy rbmode.py to `/usr/local/sbin/rbmode` and run `chmod +x /usr/local/sbin/rbmode`
* Load i2c-dev on boot: `echo i2c-dev >>/dev/modules`
* Create a systemd service. Change `<mode>` to the mode you want to set on boot.

	~~~bash
	cat <<"EOF" >/etc/systemd/system/rbmode.service
	[Unit]
	Description=rbMode
	After=network.target

	[Service]
	Type=oneshot
	ExecStart=/usr/local/sbin/rbmode <mode>

	[Install]
	WantedBy=multi-user.target
	Alias=rbmode.service
	EOF
	
	systemctl enable rbmode.service
	~~~
	
* Load i2c-dev and set the mode

	~~~bash
	modprobe i2c-dev
	rbmode u
	~~~