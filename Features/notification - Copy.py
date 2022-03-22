
import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print ("Accepted connection from ",address)

data = client_sock.recv(1024)
print ("received [%s]" % data)

client_sock.close()
server_sock.close()
'''
import bluetooth

target_name = "b"
target_address = None

nearby_devices = bluetooth.discover_devices()
for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print ("found target bluetooth device with address ", target_address)
else:
    print ("could not find target bluetooth device nearby")
'''