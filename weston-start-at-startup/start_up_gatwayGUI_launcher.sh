export PYTHONPATH=$PYTHONPATH:/usr/local/gatewayGUI/

/usr/local/Cube-M4-examples/STM32MP157C-DK2/Examples/GPIO/GPIO_EXTI/fw_cortex_m4.sh stop
sleep 1
/usr/local/Cube-M4-examples/STM32MP157C-DK2/Examples/GPIO/GPIO_EXTI/fw_cortex_m4.sh start
sleep 1

python3 /usr/local/gatewayGUI/gui/mpuhub.py &
sleep 1

/usr/local/MyRemoteProcTTYApp &
sleep 1
python3 /usr/local/gatewayGUI/gui/main_gateway_gui.py
