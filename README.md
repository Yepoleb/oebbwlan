# OEBB WLAN

Automatically dismisses the portal page of OEBB train WLAN, so you don't have to manually open it in your browser. NetworkManager integration is provided, but you can easily integrate it with any network manager that allows scripting on connection events.

## Dependencies

* Python 3 (python3)
* Beautiful Soup 4 (python3-bs4)
* Requests (python3-requests)

## Install

```sh
sudo install oebbnetworkmanager.py /etc/NetworkManager/dispatcher.d/10-oebb
sudo systemctl enable NetworkManager-dispatcher.service
```

Make sure your connection is called `OEBB` or the script won't trigger.

## License

CC-BY-4.0
