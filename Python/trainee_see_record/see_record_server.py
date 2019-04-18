def querying_record(db_conn,qr_code):
    cur = db_conn.cursor()
    cur.execute("SELECT Finished_Task, Self_Rating from traineeRecord where QR_Code = ?",(qr_code,))
    rows = cur.fetchall()
    for row in rows:
        return row


elif choice == "3":
# now receiving qr code for querying database.
received_qr_code = int(socketConnection.recv(1024).decode('utf-8'))
record_result = querying_record(dbConnection ,received_qr_code)
record_sent = json.dumps(record_result)
print("Record =  " +record_sent)
with socketConnection:
    socketConnection.send(record_sent.encode())