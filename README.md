# Description

This blender addon is made to solve blenders problem of [horribly slow saves to the network](https://blender.stackexchange.com/questions/149926/saving-blend-files-straight-to-server-nets-0-5-speed-of-a-windows-file-copy-ho).
As I found out in the meantime, the same is true for saves to slower thumbdrives.

The reason for this is that Blender uses a very small buffer. This is good as it decreases the RAM needed to save a project, but gets plumetting performance whenever you try to a location with a higher latency.
This is especially true with bigger files. This plugin tries to solve this by first saving your file to your default temporary files location, and then copying it to the final location.

For saves to a local drive, the time difference should not really matter. 
For saves to a network location of a 3.5GB blend file we saw a difference of 5x the speed when saving to a low latency 10Gbps FreeNAS SMB share.
For saves to a windows share on a 1Gbps location we saw a difference 28x the speed.

For more information, see the [BENCHMARKS](BENCHMARKS.md) file.

# Installation

- Download the `save_by_proxy.py` file from the repository or find it on [Gumroad](https://gum.co/LDanY); Save it to your desktop
- Add it through Blenders addon manager.
- Finally enable it by toggling the checkbox before the plugin name.

# Usage

While there still is an issue with showing the button in the menu system of 2.80, this plugin works by remapping your `CTRL + S` or `CMD + S` keyboard shortcut.

# Deinstallation

Want your default save behavior back? Just disable the checkbox of the plugin in Blenders addon manager.

# Want to help?

Feel free to solve the problem of the plugin not showing up in the file menu. I haven't figured it out yet, and I mostly save using `ctrl+s` anyhow. But for other users this might be a huge help.
