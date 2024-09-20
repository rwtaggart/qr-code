# qr-code
Simple command-line utility for generating QR codes with an icon overlay

# Install
1. Create personal `lib` and `bin` directories
    ```sh
    mkdir $HOME/lib;
    mkdir $HOME/bin;
    ```

1. Clone the repo and link it up
    ```sh
    git clone https://github.com/rwtaggart/qr-code.git $HOME/lib/qr-code;
    ln -s $HOME/lib/qr-code/qr_png.py $HOME/bin/qr_png;
    ```

1. Install dependencies
    ```sh
    pip3 install -r $HOME/lib/qr-code/requirements.txt
    ```

1. Show usage and help documentation
    ```sh
    qr_png --help
    ```


# Dependencies
Name | URL
--: | ---
pillow | [https://pypi.org/project/pillow/](https://pypi.org/project/pillow/)
qrcode | [https://pypi.org/project/qrcode/](https://pypi.org/project/qrcode/)


# Virtual Environments
Note, it's recommended to use [virtual environments](https://docs.python.org/3/library/venv.html#creating-virtual-environments) when installing Python packages and dependencies
```sh
python3 -m venv ./venv
. ./venv/bin/activate
```


# WiFi QR Code
Wi-Fi network information can be specified using the MeCard format for mobile devices
```
WIFI:S:<SSID>;T:<WEP|WPA|nopass>;P:<PASSWORD>;H:<true|false|blank>;;
```

See _"Joining a Wi-Fi network"_ in [https://en.wikipedia.org/wiki/QR_code](https://en.wikipedia.org/wiki/QR_code)
