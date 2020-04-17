# i3blocks-config
This is my default i3blocks configuration.
![Thumbnail1](resources/i3blocks-thumbnail-5.png)
<br/>
![Thumbnail2](resources/i3blocks-thumbnail-6.png)
***

<h2> Standard installation: </h2>

<h4> &nbsp;&nbsp; 1. Install i3blocks: </h4>

Start of by installing [i3blocks](https://www.archlinux.org/packages/community/x86_64/i3blocks/). Ideally istallation should be performed with your package manager.

<h4> &nbsp;&nbsp; 2. Install an emojicon font: </h4>

Recommended font: [noto-fonts-emoji](https://www.archlinux.org/packages/extra/any/noto-fonts-emoji/). All you need to do is install the font, i3 should recognice it and use it automatically.

<h4> &nbsp;&nbsp; 3. Copy the i3blocks configuration: </h4>

From the repository root, invoke `./install.sh`. This script will copy the configuration to your home directory. __Caution:__ if you already have a i3blocks configuration setup in *~/.config/i3blocks* you might want to back it up first. Also note that i3blocks is __not__ the same software as i3status/i3bar and such will not modify them. If you haven't used i3blocks before you can proceed without worrying.

<h4> &nbsp;&nbsp; 4. Modify i3 configuration file: </h4>

*~/.config/i3/config*:
```
bar {
  position top                  # Position should be 'bottom' or 'top'.
  status_command i3blocks       # Invoke i3blocks.

  # Possible other bar configurations go here...
  # ...
}
```
You could also modify the font and font size in this file. The default font *pango* will do just fine but you might want to increese the font size based on your needs and also switch to monospace (*pango:monospace*).
```
# Font for window titles. Will also be used by the bar unless a different font
# is used in the bar {} block below.
font pango:monospace 12
```
Another good monospace bold font, [ttf-hack](https://www.archlinux.org/packages/extra/any/ttf-hack/):
```
font pango:Hack Bold 16
```

<h4> &nbsp;&nbsp; 5. Make audio changes signal the bar: </h4>

The sound level indicator is updated once every tenth second. If you want a more responsive sound level indicator you can use `pkill -RTMIN+1 i3blocks` to send a signal on sound level changes. This will update the sound level blocklet instantly. Here is an __example__ of how this could be accomplished.

*~/.config/i3/config*:
```
# User-added function keys:
bindsym XF86AudioMute         exec --no-startup-id pamixer -t     && pkill -RTMIN+1 i3blocks
bindsym XF86AudioLowerVolume  exec --no-startup-id pamixer -d 3   && pkill -RTMIN+1 i3blocks
bindsym XF86AudioRaiseVolume  exec --no-startup-id pamixer -i 3   && pkill -RTMIN+1 i3blocks
```

<h2> Modification: </h2>

It is easy to modify the bar. Take a look at [.config/i3blocks/config](https://github.com/miklhh/i3blocks-config/blob/master/.config/i3blocks/config) and see for yourself how easy it is to modify any of the blocklets. If any blocklet is malfunctioning, this should be the entypoint for bug searching.
<br/> <br/>
If you want to modify the weather location data, take a look into [config/i3blocks/weather/weather.py](.config/i3blocks/weather/weather.py) (line 9). This too is easy to modify, just change the [YR.no](yr.no) XML weblink. To get desired XML weblink, go to the YR webpage and find a location. Add */forecast.xml* to the end of the URL (english YR version only) to get the appropriate weblink for the weather script.


<h3>Thumbnail:</h3>

![Thumbnail1](resources/i3blocks-thumbnail-5.png)
<br/>
![Thumbnail2](resources/i3blocks-thumbnail-6.png)
***

<h2>Requiered software packages.</h2>

| Software          | Arch Linux Package | Gentoo Package       |
|-------------------|--------------------|----------------------|
| i3blocks          | [community/i3blocks](https://www.archlinux.org/packages/community/x86_64/i3blocks/)       | [x11-misc/i3blocks](https://packages.gentoo.org/packages/x11-misc/i3blocks)           |
| Noto Color Emoji  | [extra/noto-fonts-emoji](https://www.archlinux.org/packages/extra/any/noto-fonts-emoji/)  | [media-fonts/noto-emoji](https://packages.gentoo.org/packages/media-fonts/noto-emoji) |
| ACPI              | [community/acpi](https://www.archlinux.org/packages/community/x86_64/acpi/)               | [sys-power/acpid](https://packages.gentoo.org/packages/sys-power/acpid)               |
| Sysstat           | [community/sysstat](https://www.archlinux.org/packages/community/x86_64/sysstat/)         | [app-admin/sysstat](https://packages.gentoo.org/packages/app-admin/sysstat)           |
| Python 3          | [extra/python](https://www.archlinux.org/packages/extra/x86_64/python/)                   | >=[dev-lang/python](https://packages.gentoo.org/packages/dev-lang/python)-3.6         |
| Python Requests   | [extra/python-requests](https://www.archlinux.org/packages/extra/any/python-requests/)    | [dev-python/requests](https://packages.gentoo.org/packages/dev-python/requests)       |
| lm_sensors        | [extra/lm_sensors](https://www.archlinux.org/packages/extra/x86_64/lm_sensors/)           | [sys-apps/lm-sensors](https://packages.gentoo.org/packages/sys-apps/lm-sensors)       |

Note: Gentoo users need to emerge [media-libs/freetype](https://packages.gentoo.org/packages/media-libs/freetype) with USE=png for Noto Color Emoji to render.
