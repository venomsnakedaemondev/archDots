#! /bin/bash
sudo pacman -Syu --noconfirm 
echo "instalando programas base" && sleep 1 
sudo pacman -S xf86-video-ati bspwm unzip ttf-iosevka-nerd ttf-fantasque-sans-mono numlockx sxhkd picom code feh wget htop make lsd bat npm  xorg xorg-xinit xorg-server mesa mesa-demos curl gdm nano volumeicon pavucontrol firefox rofi base-devel arandr ranger net-tools neofetch  libxcb xcb-util xcb-util-wm xcb-util-keysyms locate kitty git polybar btop zsh thunar speedtest-cli firejail lm_sensors proxychains tor python-requests python-beautifulsoup4  --noconfirm
#otros 
systemctl enable gdm.service
mkdir ~/repos && cd ~/repos
# #paru 
sudo git clone https://aur.archlinux.org/paru-bin.git
sudo chown -R vnmsnake /home/vnmsnake/repos/paru-bin
cd ~/repos/paru-bin && makepkg -si
# #intalaciones paru
paru -S scrub ttf-icomoon-feather --noconfirm
##yay
cd ~/repos
git clone https://aur.archlinux.org/yay.git
sudo chown -R vnmsnake ~/repos/yay
cd ~/repos/yay && makepkg -si
#fonts 
cd /usr/share/fonts
sudo wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.1.1/Hack.zip
sudo unzip Hack.zip && sudo rm -rf Hack.zip 
sudo cp -rf ~/archdot/polybar/fonts/* /usr/share/fonts && fc-cache -v
#polybar 
chmod +x ~/archdot/polybar/scripts/* && chmod +x ~/archdot/polybar/launch.sh
cp -rf ~/archdot/polybar ~/.config/
#bspwm
chmod +x ~/archdot/bspwm/* && cp -rf ~/archdot/bspwm ~/.config/
chmod +x ~/archdot/sxhkd/sxhkdrc && cp -rf ~/archdot/sxhkd/ ~/.config/
cp -rf ~/archdot/kitty ~/.config/
cp -rf ~/archdot/picom ~/.config/
#wallpapers
cd && wget https://download1501.mediafire.com/jl9eqaw11k7g5-mMIB1kHgDzuCyoC02AcOcJA5C64qZeOdqfCG122zQ47DWsqxTq1b8pYOWMfVuzPFhKCPmN8-lCyDvJ2NM2EHaUd3aLhSJ6BUhw-Wkr1TV1nnQSMjBUl_pvRWK4kArwAz2_HgO3H-TK1waPs6JY9usS_4_88zN5vKb-/wdw7bmmai7obyzy/wallpaper.zip
unzip wallpaper.zip 
rm -rf wallpaper.zip