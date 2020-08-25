cp MyRemoteProcTTYApp /usr/local/
echo "Application for communicating with M4 core copied to /usr/local"
mkdir /usr/local/weston-start-at-startup/
cp weston-start-at-startup/start_up_gatwayGUI_launcher.sh /usr/local/weston-start-at-startup/
echo "Package start-up script copied to /usr/local/weston-start-at-startup/"
cp -rf gatewayGUI/ /usr/local/
echo "Your Package is Installed @/usr/local/gatewayGUI"
