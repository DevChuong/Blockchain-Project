if choice == 3:
    input_qr_code = int(input("Enter your qr code : "))
    sent_qrCode = str(input_qr_code)
    s.send(sent_qrCode.encode())

    print("Trainee record for trainee record's QR Code " + sent_qrCode)
    record_received = s.recv(1024).decode('utf-8')
    print(record_received)