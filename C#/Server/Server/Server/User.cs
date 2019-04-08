using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

namespace Server
{
    public class User
    {
        //Tên người chơi
        string userName;

        public string UserName
        {
            get { return userName; }
            set { userName = value; }
        }
        Socket socket;

        public Socket _Socket
        {
            get { return socket; }
            set { socket = value; }
        }
        bool inRoom; // trạng thái ở ngoài phòng hay trong phòng, false: ngoài, true: trong

        public bool InRoom
        {
            get { return inRoom; }
            set { inRoom = value; }
        }
        int roomNumber; // mã số phòng

        public int RoomNumber
        {
            get { return roomNumber; }
            set { roomNumber = value; }
        }

        bool statusConnect; // trạng thái kết nối

        public bool StatusConnect
        {
            get { return statusConnect; }
            set { statusConnect = value; }
        }

        int luotDi;

        public int LuotDi
        {
            get { return luotDi; }
            set { luotDi = value; }
        }

        public User()
        {
            userName = "";
            inRoom = false;
            statusConnect = false;
        }

        public User(string us, Socket s)
        {
            this.userName = us;
            this.socket = s;
            this.inRoom = false;
            this.roomNumber = 0;
            this.statusConnect = true;
        }

        public User(string us, Socket s, bool ir, int rn, bool stt)
        {
            this.userName = us;
            this.socket = s;
            this.inRoom = ir;
            this.roomNumber = rn;
            this.statusConnect = stt;
        }
    }
}
