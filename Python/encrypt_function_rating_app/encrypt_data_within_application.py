def return_publicKey(db_conn, ID):
    cur = db_conn.cursor()
    cur.execute("SELECT Public_Key FROM employeeList WHERE ID_Employee = ?", (ID,))

    rows = cur.fetchall()

    for row in rows:
        return row




elif choice == "2":
    received_category_result = socketConnection.recv(1024).decode('utf-8')
    print(received_category_result)
########Call CRYPTO API HERE###########
    data = received_category_result.encode('utf-8')
    print(data)
    file_out = open("Data Storage\Tran Hoang Chuong\E_Task_Completed.bin", "wb")

    tuple_publicKey = return_publicKey(dbConnection, ID_Returned)
    queried_publicKey = tuple_publicKey[0]

    recipient_key = RSA.import_key(open(queried_publicKey).read())  # Your key is used in here
    session_key = get_random_bytes(16)  # your session key here

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)  # public key = recipient_key
    enc_session_key = cipher_rsa.encrypt(session_key)  # session key has been encrypted

# Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)  # session key is brought to here
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)  # data is encrypted with cipher_aes (session key)
    [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    received_category_result = "Data Storage\Tran Hoang Chuong\E_Task_Completed.bin"
#######################################
    update_status = update_performed_task(dbConnection, received_category_result, ID_Returned)
    if update_status == 1:
        print("Update task successfully")
    data = str.encode("Data stored successfully !")
    with socketConnection:
        socketConnection.send(data)